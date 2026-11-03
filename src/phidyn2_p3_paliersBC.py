#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P3 — PALIERS B'' (voie γ) + C'' (voie δ) — fiche v1.0 SCELLEE (0dbf3e4)
================================================================================
Voie γ : frontiere de blocking du corridor — moyenne glissante boxcar de
largeur w (padding de bord par replication de bord, numpy convolve 'same'),
grille w ∈ {1,2,4,8,16,32,64} gelée.

Observables (definitions EXACTES reprises de src/t47_ko6_vinen.py) :
  G1 — R2 de 1/longueur affine en t, fenetre [12, 60] (vinensigne) ;
       seuil de survie R2 >= 0.90 (gelé) ; run discriminateur n8_440201 ;
  G2 — plateau = moyenne des 'ouverts' pour t >= 45 ; deviation <= 5 %
       des valeurs brutes archivees {9.8125, 15.9375, 31.4375} ;
  G3 — comptage de sauts : |ΔΛ| > 0.5 * écart-type local (fenêtre 5) ;
       compte à ±1 de la série brute (n8_440201) ;
  G4 — ratios des plateaux bruts : 15.9375/9.8125 et 31.4375/15.9375,
       test |ratio − φ| ≤ 0.02 (standard maison, pré-enregistré).
Note d'implémentation déclarée : w=64 sur séries de 60 points donne 1
échantillon — mort par dégénérescence de longueur (R² = 0 par garde),
rapportée comme telle.
Voie δ : table des échelles (annexe descriptive, sans critère — décision 4).
Sortie : data/phidyn2_p3_paliersBC.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
GRILLE_W = [1, 2, 4, 8, 16, 32, 64]
SEUIL_R2 = 0.90
TOL_PLATEAU = 0.05
FENETRE_VINEN = (12.0, 60.0)
PLATEAUX_BRUTS = {"n2_440201": 9.8125, "n4_440201": 15.9375,
                  "n8_440201": 31.4375}
DATA = Path("noetic-machine-complete/data")


def r2_affine(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) < 3 or np.std(y) == 0:
        return 0.0
    a, b = np.polyfit(x, y, 1)
    ss_res = float(np.sum((y - (a * x + b)) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def boxcar(x, w):
    if w == 1:
        return np.asarray(x, float).copy()
    x = np.asarray(x, float)
    pad = w // 2
    xp = np.concatenate([np.full(pad, x[0]), x, np.full(pad, x[-1])])
    return np.convolve(xp, np.ones(w) / w, mode="valid")[:len(x)]


def vinensigne_bloque(h, w):
    lg = boxcar(h["longueur"], w)
    xs, ys = [], []
    for i, t in enumerate(h["t"]):
        if FENETRE_VINEN[0] <= t <= FENETRE_VINEN[1] and lg[i] > 0:
            xs.append(t)
            ys.append(1.0 / lg[i])
    return r2_affine(xs, ys), len(xs)


def plateau_bloque(h, w):
    ov = boxcar(h["ouverts"], w)
    idx = [i for i, t in enumerate(h["t"]) if t >= 45.0]
    return float(np.mean([ov[i] for i in idx]))


def compte_sauts(serie, w):
    s = boxcar(serie, w)
    n = 0
    for i in range(1, len(s)):
        lo = max(0, i - 2)
        hi = min(len(s), i + 3)
        ecart = np.std(s[lo:hi])
        if abs(s[i] - s[i - 1]) > 0.5 * ecart:
            n += 1
    return n


def main():
    t0 = time.time()
    print("Φ-DYN-2 P3 — PALIERS B'' (voie γ) + C'' (voie δ) [fiche v1.0 SCELLÉE]")
    print("=" * 78)
    d47 = json.loads((DATA / "t47_ko6_vinen_verdict.json").read_text(encoding="utf-8"))
    runs = {k: v for k, v in d47["mesures"]["historiques"].items()}

    # ---- A'' intégré : reproduction des bruts (sanité)
    print("A'' — reproduction des bruts archivés (tolérance 1e−3) :")
    vg_brut = d47["mesures"]["R2_vinen_1surLambda"]
    sane = True
    for cle, h in runs.items():
        r2_re, npts = vinensigne_bloque(h, 1)
        ref = vg_brut[cle]
        ok = abs(r2_re - ref) <= 1e-3
        sane &= ok
        print(f"  {cle} : R² reproductible {r2_re:.4f} vs archivé {ref:.4f} : {ok}"
              f" · {len(h['t'])} points, t ∈ [{h['t'][0]}, {h['t'][-1]}]")

    # ---- B'' voie γ
    print("\nB'' — frontière de blocking (boxcar, grille w) :")
    gamma = {}
    discriminant = "n8_440201"
    h8 = runs[discriminant]
    r2_brut8, _ = vinensigne_bloque(h8, 1)
    sauts_brut = compte_sauts(h8["longueur"], 1)
    print(f"  référence brute {discriminant} : R² = {r2_brut8:.4f} · "
          f"sauts = {sauts_brut}")
    for w in GRILLE_W:
        r2, npts = vinensigne_bloque(h8, w)
        pl = {cle: plateau_bloque(h, w) for cle, h in runs.items()}
        dev_pl = {cle: abs(pl[cle] - PLATEAUX_BRUTS[cle]) / PLATEAUX_BRUTS[cle]
                  for cle in PLATEAUX_BRUTS}
        sauts = compte_sauts(h8["longueur"], w)
        g1 = r2 >= SEUIL_R2
        g2 = all(d <= TOL_PLATEAU for d in dev_pl.values())
        g3 = abs(sauts - sauts_brut) <= 1
        g4 = {f"{a}/{b}": abs(PLATEAUX_BRUTS[b] / PLATEAUX_BRUTS[a] - PHI) <= 0.02
              for a, b in [("n2_440201", "n4_440201"),
                           ("n4_440201", "n8_440201")]}
        mort = "dégénérée (longueur)" if w >= len(h8["t"]) else (
            "MORTE" if not (g1 and g2) else "vivante")
        gamma[str(w)] = {"R2_vinen_n8": r2, "n_points_fenetre": npts,
                         "plateaux": pl, "deviations_plateaux": dev_pl,
                         "sauts": sauts, "G1": bool(g1), "G2": bool(g2),
                         "G3": bool(g3), "G4": g4, "statut": mort}
        print(f"  w={w:2d} : R²={r2:.4f} ({npts} pts) · plateaux dev "
              f"{[round(dev_pl[c], 3) for c in dev_pl]} · sauts {sauts} · "
              f"G1 {'✓' if g1 else '✗'} G2 {'✓' if g2 else '✗'} G3 {'✓' if g3 else '✗'}"
              f" · ratios φ {g4} · {mort}")
    frontieres = [w for w in GRILLE_W
                  if gamma[str(w)]["statut"] == "vivante"]
    w_star = max(frontieres) if frontieres else None
    premier_mort = next((w for w in GRILLE_W if gamma[str(w)]["statut"] != "vivante"),
                        None)
    print(f"\n  frontière w* = {w_star} · premier mort = {premier_mort}")

    # ---- C'' voie δ (annexe descriptive)
    delta = {
        "corridor": {"plateaux_ouverts": PLATEAUX_BRUTS,
                     "ratios": [PLATEAUX_BRUTS["n4_440201"] / PLATEAUX_BRUTS["n2_440201"],
                                PLATEAUX_BRUTS["n8_440201"] / PLATEAUX_BRUTS["n4_440201"]],
                     "ecarts_a_phi": [PLATEAUX_BRUTS["n4_440201"] / PLATEAUX_BRUTS["n2_440201"] - PHI,
                                      PLATEAUX_BRUTS["n8_440201"] / PLATEAUX_BRUTS["n4_440201"] - PHI],
                     "sauts_unitaires_dates_T44": [3.50, 3.55],
                     "drainage_T46": "÷43",
                     "heterogeneite_T55": "KM/Little ≈ 0.5"},
        "porteur": {"echelle_bande_mediane_P1C": 0.52,
                    "kappa_moins_1_quadratique_P2": "κ−1 ∝ (y−1)²",
                    "frontiere_flips_P1B": "1–4 flips / mot de 377"},
        "statut": "ANNEXE DESCRIPTIVE — sans critère de coïncidence (décision 4)",
    }
    print("\nC'' — voie δ : table des échelles (annexe descriptive) consolidée.")

    out = {
        "chantier": "PHI-DYN-2-P3-PALIERS-BC",
        "fiche": "FICHE-PHI-DYN-2-P3-CORRIDOR v1.0 SCELLÉE (0dbf3e4)",
        "archives_saines": bool(sane),
        "gamma": gamma, "w_etoile": w_star, "premier_mort": premier_mort,
        "delta": delta,
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn2_p3_paliersBC.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
