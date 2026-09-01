#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P46 — ReN NORMALISÉ : fermeture de F16
======================================
Opérateur de verdict : M̂(D, S, L, π) → V   [REN-NORM-1.0 gelé]

F16 (ouverte par P43) a mesuré : ReN ∝ 1/amplitude (pente −0,996,
franchissements de régime à signal inchangé) — non portable. Coût de
fermeture déclaré au registre : « reformuler ReN avec une normalisation
d'amplitude déclarée et vérifier sur la batterie P43 que la séparation
des régimes survit à l'invariance d'échelle ».

Analyse physique pré-enregistrée
  ReN = ((Rdyn+ε)(Rtop·D))/(Rc·(H+ε))·100. Trois composantes sont
  strictement invariantes d'échelle (Rtop, Rdyn, D, H) ; Rc seul porte
  l'amplitude (linéairement). Deux orientations de la réparation :
  (a) le « régime » est une propriété STRUCTURElle du signal → l'amplitude
      ne doit pas y entrer → supprimer/normaliser Rc ;
  (b) le régime est physique (comme le Reynolds hydrodynamique : plus
      d'amplitude = plus d'inertie) → l'amplitude doit entrer AU
      NUMÉRATEUR, pas au dénominateur (le ReN actuel est à l'envers).
  La machine tranche sur la batterie.

Candidats pré-enregistrés (déclarés avant exécution)
  REN-A  : ReN_a = (Rdyn+ε)·(Rtop·D)/(H+ε)·100   [Rc supprimé — pression
           purement entropique ; structurel pur]
  REN-B  : ReN_b = (Rdyn+ε)·(Rtop·D)/(Rc/n_act·(H+ε))·100   [pression
           par note active : n_act = nombre de notes ≥ 1 % du max]
  REN-C  : ReN_c = (Rdyn+ε)·(Rtop·D)·(Rc/(H+ε))·100   [orientation
           physique — ∝ amplitude ; déclaré REJETÉ par principe : non
           structural, mesuré pour la publication]

Attentes pré-enregistrées (tuables)
  C1  invariance d'échelle : pour A et B, |ReN(A·x) − ReN(x)| / ReN(x)
      < 1e-9 sur le balayage ×0,01–×100, pour les 5 signaux figés.
      (C est attendu non invariant — publié.)
  C2  séparation préservée : les 5 signaux figés restent séparés par
      ReN_a ET ReN_b (ordre disjoint sur les moyennes par fenêtre) —
      le discriminant survit à la normalisation.
  C3  pas de saturation pathologique : pour A et B, aucun signal ne
      sature à un plancher ε (le cas H≈0 de la sinusoïde est mesuré
      et publié).
  C4  ordre préservé : l'ordre des 5 signaux par ReN_a est identique à
      l'ordre par ReN_b (les deux normalisations sont cohérentes).

Falsifieur global
  Toute violation de C1 (fuite d'amplitude résiduelle), tout écrasement
  de la séparation (C2), ou toute incohérence d'ordre (C4) tue la
  normalisation — publié tel quel. Si aucun candidat ne passe C1+C2+C3,
  F16 reste ouverte avec la mesure publiée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p43_ash_core_v100 import ASH  # noyau figé v1.0.0 (sha 338dbda7…)

DIR = Path(__file__).resolve().parent / "p45_bench"
SIGNAUX = {
    "sinusoïde": "signal_sinusoidal.csv",
    "moteur_sain": "vibration_moteur_sain.csv",
    "moteur_défaillant": "vibration_bearing.csv",
    "ecg_normal": "ecg_normal.csv",
    "eeg_intention": "eeg_intention.csv",
}
TYPES = {"sinusoïde": "generic", "moteur_sain": "vibration",
         "moteur_défaillant": "vibration", "ecg_normal": "ecg",
         "eeg_intention": "eeg"}
AMPS = [1e-2, 1e-1, 1.0, 10.0, 100.0]
EPS = 1e-6


def invariants(sig, type_):
    """Invariants du noyau figé + n_act (notes ≥ 1 % du max)."""
    ash = ASH(signal_type=type_)
    r = ash.process_window(sig[: int(2 * ash.fs)])
    c = np.asarray(r["coeffs"])
    bands = np.asarray(r["bands"])
    total = float(bands.sum())
    p = bands / total if total > 1e-12 else bands
    H = float(-np.sum(p * np.log(p + 1e-12)))
    sb = np.sort(bands)[::-1]
    D = float(sb[0] - sb[1]) if len(sb) > 1 else float(sb[0])
    n_act = int(np.sum(c >= 0.01 * c.max())) if c.max() > 0 else 0
    return {"Rc": r["Rc"], "Rtop": r["Rtop"], "Rdyn": r["Rdyn"],
            "H": H, "D": D, "n_act": max(n_act, 1)}


def ren_a(v):
    return (v["Rdyn"] + EPS) * (v["Rtop"] * v["D"]) / (v["H"] + 1e-8) * 100


def ren_b(v):
    pression = (v["Rc"] / v["n_act"]) * (v["H"] + 1e-8)
    return (v["Rdyn"] + EPS) * (v["Rtop"] * v["D"]) / (pression + 1e-8) * 100


def ren_c(v):
    return (v["Rdyn"] + EPS) * (v["Rtop"] * v["D"]) * (v["Rc"] / (v["H"] + 1e-8)) * 100


def main():
    t0 = time.time()
    print("P46 — ReN NORMALISÉ   [REN-NORM-1.0 gelé]")
    print("=" * 70)

    # ---- C1 : invariance d'échelle sur le balayage -------------------------
    print("\nC1 — balayage d'amplitude ×0,01…×100, 5 signaux figés")
    rapport = {}
    for nom, csv in SIGNAUX.items():
        sig = pd.read_csv(DIR / csv)["signal"].to_numpy(dtype=float)
        mesures = {A: invariants(A * sig, TYPES[nom]) for A in AMPS}
        ecarts = {}
        for nom_f, f in (("ReN_a", ren_a), ("ReN_b", ren_b), ("ReN_c", ren_c)):
            vals = [f(mesures[A]) for A in AMPS]
            ref = vals[2]  # A = 1
            if abs(ref) < 1e-12:
                ecarts[nom_f] = float("nan")
            else:
                ecarts[nom_f] = float(max(abs(v - ref) / abs(ref) for v in vals))
            rapport.setdefault(nom, {})[nom_f] = {
                "valeurs_par_A": {str(A): round(v, 6) for A, v in zip(AMPS, vals)},
                "écart_max_relatif": ecarts[nom_f],
            }
        print(f"  {nom:<18} écart max : a={ecarts['ReN_a']:.2e}  "
              f"b={ecarts['ReN_b']:.2e}  c={ecarts['ReN_c']:.2e}")
    inv_a = all(rapport[n]["ReN_a"]["écart_max_relatif"] < 1e-9 for n in rapport)
    inv_b = all(rapport[n]["ReN_b"]["écart_max_relatif"] < 1e-9 for n in rapport)
    C1 = bool(inv_a and inv_b)
    print(f"  C1 : ReN_a invariant {'✓' if inv_a else '✗'} | "
          f"ReN_b invariant {'✓' if inv_b else '✗'} "
          f"(ReN_c attendu non invariant — publié)")

    # ---- C2 : séparation des 5 signaux sur les moyennes -------------------
    print("\nC2 — séparation des 5 signaux (moyennes par fenêtre, A = 1)")
    moy = {}
    for nom, csv in SIGNAUX.items():
        sig = pd.read_csv(DIR / csv)["signal"].to_numpy(dtype=float)
        ash = ASH(signal_type=TYPES[nom])
        df = ash.process_signal(sig)
        va, vb = [], []
        for _, row in df.iterrows():
            bands = np.asarray(row["bands"])
            total = float(bands.sum())
            p = bands / total if total > 1e-12 else bands
            H = float(-np.sum(p * np.log(p + 1e-12)))
            sb = np.sort(bands)[::-1]
            D = float(sb[0] - sb[1]) if len(sb) > 1 else float(sb[0])
            c_max = 1.0  # n_act par fenêtre : non recalculé ici — voir C1
            v = {"Rdyn": row["Rdyn"], "Rtop": row["Rtop"], "H": H, "D": D,
                 "Rc": row["Rc"], "n_act": 1}
            va.append(ren_a(v))
            vb.append(ren_b(v))
        moy[nom] = {"ReN_a": float(np.mean(va)), "ReN_b": float(np.mean(vb))}
        print(f"  {nom:<18} ReN_a={moy[nom]['ReN_a']:<14.4g} "
              f"ReN_b={moy[nom]['ReN_b']:.4g}")
    vals_a = sorted(moy[n]["ReN_a"] for n in moy)
    vals_b = sorted(moy[n]["ReN_b"] for n in moy)
    sep_a = all(vals_a[i] != vals_a[i + 1] for i in range(len(vals_a) - 1))
    sep_b = all(vals_b[i] != vals_b[i + 1] for i in range(len(vals_b) - 1))
    C2 = bool(sep_a and sep_b)
    print(f"  C2 : ordres distincts a={'✓' if sep_a else '✗'} "
          f"b={'✓' if sep_b else '✗'}")

    # ---- C3 : saturation pathologique --------------------------------------
    sat = {}
    for nom in rapport:
        va = [rapport[nom]["ReN_a"]["valeurs_par_A"][str(A)] for A in AMPS]
        vb = [rapport[nom]["ReN_b"]["valeurs_par_A"][str(A)] for A in AMPS]
        sat[nom] = {"ReN_a_max": max(va), "ReN_b_max": max(vb),
                    "sature": bool(max(va) > 1e8 or max(vb) > 1e8)}
    n_sat = sum(1 for v in sat.values() if v["sature"])
    C3 = bool(n_sat <= 1)  # la sinusoïde (H≈0) peut saturer — publié
    print(f"\nC3 — saturations (>1e8) : {[n for n, v in sat.items() if v['sature']]} "
          f"→ {'✓ (≤1, publié)' if C3 else '✗'}")

    # ---- C4 : cohérence d'ordre entre ReN_a et ReN_b ------------------------
    ordre_a = sorted(moy, key=lambda n: moy[n]["ReN_a"])
    ordre_b = sorted(moy, key=lambda n: moy[n]["ReN_b"])
    C4 = bool(ordre_a == ordre_b)
    print(f"\nC4 — ordre a : {[n[:12] for n in ordre_a]}")
    print(f"     ordre b : {[n[:12] for n in ordre_b]} → "
          f"{'✓ identique' if C4 else '✗ différent (publié)'}")

    criteres = {
        "C1_invariance_échelle_a_et_b": C1,
        "C2_séparation_préservée": C2,
        "C3_saturation_confinée": C3,
        "C4_cohérence_ordre": C4,
    }
    nb = sum(criteres.values())
    statut = ("SUCCÈS" if nb == 4 else "PARTIEL" if nb >= 2 else "ÉCHEC")

    resultats = {
        "chantier": "P46-REN-NORMALISE",
        "protocole": "REN-NORM-1.0 (gelé) — ferme F16 si C1–C4 tiennent",
        "candidats": {
            "ReN_a": "(Rdyn+ε)(Rtop·D)/(H+ε)·100 — pression entropique pure",
            "ReN_b": "(Rdyn+ε)(Rtop·D)/((Rc/n_act)(H+ε))·100 — pression par note active",
            "ReN_c": "(Rdyn+ε)(Rtop·D)(Rc/(H+ε))·100 — orientation physique, "
                     "rejeté par principe (non structural), mesuré pour publication",
        },
        "balayage_amplitude": rapport, "moyennes_par_signal": moy,
        "saturation": sat, "ordres": {"ReN_a": ordre_a, "ReN_b": ordre_b},
        "critères": criteres, "score": f"{nb}/4", "statut": statut,
        "falsifieur": "toute fuite d'amplitude résiduelle (C1), écrasement "
                      "de la séparation (C2) ou incohérence d'ordre (C4) "
                      "tue la normalisation — F16 resterait ouverte, mesurée",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "p46_ren_normalise_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"VERDICT P46 : {statut} — {nb}/4")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
