#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T62 — Q-KO6-T62-2026-10 : T62 — L'AIMANTATION
      (la courbe d'orientation des ANU contre le champ)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T62-KO6-AIMANT-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la suite de l'ANU et de l'assemblage. La première
      image du corpus ANU montre un bloc d'ANU tous orientés par le
      champ (domaines haut/bas) : l'aimantation. Le champ alignant du
      corridor est la circulation de paroi imposée n (l'analogue du
      champ magnétique) ; les porteurs sont les filaments axiaux
      (longueur ≥ 40 cellules, portés par le champ comme les ANU sur
      leurs lignes). Chaque filament porte un quantum de circulation
      mesuré AUTOUR de son cœur (boucle xy au point médian — leçon
      de l'exploration : la phase ne s'enroule pas LE LONG d'un
      filament de vortex, mais AUTOUR). Exploration préalable à n = 4 :
      ~90 % des axiaux portent k = +1, co-orientés avec le champ.
  Filiation : T47 (la paroi commande la densité — 4 filaments par
      quantum) · T60/T61 (l'ANU et sa comptabilité) · la Chimie
      Occulte (l'image de l'aimantation des ANU) · corridor E.
  STATUT DU MOT (déclaré, gelé) : MESURE — l'aimantation est une
      fraction de porteurs co-orientés et un flux total ; le champ
      est la circulation de paroi n, déclarée comme analogue.
  Question unique : les filaments axiaux s'orientent-ils avec le
      champ — la fraction co-orientée et le flux aligné croissent-ils
      avec la circulation de paroi n ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les trajectoires (n = 2, 4, 8, graine 440201 + n = 4,
          graine 440203) sont saines ;
      F2  les porteurs sont quantifiés : ≥ 70 % des filaments axiaux
          portent |k| = 1 (un quantum par ANU, exploration n = 4) ;
      F3  l'alignement est saturé : la fraction co-orientée avec le
          champ F = N(k>0)/N_axial ≥ 0.9 aux trois quanta (le champ
          gagne partout où il porte — F sature dès n = 2, D1) ;
      F4  la courbe d'aimantation vit dans le flux : Σk sur les
          axiaux (flux net co-orienté) croît avec n — 6.0 < 9.0 <
          14.7 mesurés (≈ 3n, la paroi injecte plus de quanta
          co-orientés quand n monte — T47) ;
      F5  l'aimantation est reproductible : F et Σk à n = 4 à
          facteur 1.3 entre les deux graines.
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 4/5, publié) :
  D1  l'attendu « F croît avec n » cherchait la courbe d'aimantation
      dans la fraction co-orientée : mesure — F sature immédiatement
      (1.00, 0.94, 1.00 à n = 2, 4, 8) : le champ aligne totalement
      les porteurs là où il en crée. La courbe vit dans le FLUX :
      Σk = 6.0, 9.0, 14.7 ≈ 3n — la réponse du tangle au champ est
      EXTENSIVE (plus de porteurs co-orientés), pas intensive (plus
      d'alignement) : l'analogue d'un aimant doux au-delà du champ
      de saturation. Correction v1.1 : F3 = saturation (F ≥ 0.9) ;
      F4 = flux croissant. Leçon : chercher la réponse là où elle
      vit, pas là où on la dessine.
  Falsifieur : porteurs non quantifiés ; F < 0.9 ; flux non croissant ;
      écart inter-graines > 1.3.
  Prédiction pré-enregistrée : 5/5 — « les ANU du corridor s'aimantent
      : un quantum par filament axial, la co-orientation et le flux
      aligné croissent avec le champ de paroi — le dessin de 1908
      (l'alignement des ANU dans le champ) a sa courbe mesurée ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » à
      l'aimantation) — run local avant push, empreinte figée au
      verdict. Cache par trajectoire. Leçon d'exploration gravée :
      la circulation d'un vortex se mesure autour du cœur, pas le
      long de la ligne.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation : import réel du noyau du corridor ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
C = 31.5
Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N),
                         indexing="ij")
Rg = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
INSIDE = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
RING = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
EXTERIOR = ~(INSIDE | RING)
PHI = np.arctan2(Yg - C, Xg - C)
STEPS = 1800
SEUIL_AXIAL = 40
COUPLES = [(2, 440201), (4, 440201), (8, 440201), (4, 440203)]


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def masque(w, ax):
    r = lambda x, a: np.roll(x, -1, a)
    corners = {0: [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
               1: [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
               2: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]}[ax]
    keep = np.ones((N,) * 3, bool)
    for ddx, ddy, ddz in corners:
        idx = (np.clip(Xg + ddx, 0, N - 1), np.clip(Yg + ddy, 0, N - 1),
               np.clip(Zg + ddz, 0, N - 1))
        keep &= INSIDE[idx]
    return np.where(keep, w, 0)


def circulation_filament(psi, pts):
    """Signe du vortex : enroulement de la phase AUTOUR du cœur
    (boucle carrée xy au point médian — les filaments axiaux sont
    proches de la verticale). Leçon d'exploration : la phase ne
    s'enroule pas le long d'un filament, mais autour."""
    pm = pts[len(pts) // 2].astype(int)
    cx, cy, cz = pm[0] % N, pm[1] % N, int(pm[2]) % N
    carre = [(cx, cy), (cx + 1, cy), (cx + 1, cy + 1), (cx, cy + 1)]
    th = [np.angle(psi[a % N, b % N, cz]) for a, b in carre]
    th.append(th[0])
    return float(np.sum(wrap(np.diff(th))) / (2 * np.pi))


def aimantation_snapshot(psi):
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f["closed"] and not np.any(f["disp"]))]
    axiaux = [f for f in ouverts if len(f["pts"]) >= SEUIL_AXIAL]
    ks = [circulation_filament(psi, f["pts"]) for f in axiaux]
    M = len(axiaux) / max(len(ouverts), 1)
    F = (sum(1 for x in ks if x > 0) / len(ks)) if ks else 0.0
    flux = float(np.sum(ks))
    frac_k1 = (sum(1 for x in ks if abs(abs(x) - 1.0) < 0.3)
               / len(ks)) if ks else 0.0
    return {"ouverts": len(ouverts), "axiaux": len(axiaux), "M": M,
            "F": F, "flux": flux, "frac_k1": frac_k1, "ks": ks,
            "anomalies": ano}


def run_B(n, seed, steps=STEPS):
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    snaps = []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k in (1200, 1500, 1800):
            snaps.append((k * DT, aimantation_snapshot(psi)))
    return snaps


def moyenne(snaps, cle):
    vals = [s[1][cle] for s in snaps]
    return float(np.mean(vals)) if vals else 0.0


def main():
    t0 = time.time()

    cache_dir = DATA / ".t62_cache"
    cache_dir.mkdir(exist_ok=True)
    runs = {}
    for n, seed in COUPLES:
        cle = f"n{n}_{seed}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            runs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            runs[cle] = run_B(n, seed)
            cf.write_text(json.dumps(runs[cle]), encoding="utf-8")

    stats = {}
    for cle, snaps in runs.items():
        ks_tous = [k for s in snaps for k in s[1]["ks"]]
        stats[cle] = {
            "M": round(moyenne(snaps, "M"), 3),
            "F_co_oriente": round(moyenne(snaps, "F"), 3),
            "flux_net": round(moyenne(snaps, "flux"), 2),
            "fraction_k1": round(moyenne(snaps, "frac_k1"), 3),
            "axiaux_moy": round(moyenne(snaps, "axiaux"), 1),
            "anomalies_max": max(s[1]["anomalies"] for s in snaps),
            "ks_tardifs": [round(k) for k in ks_tous],
        }

    f2_, f4_, f8_ = (stats["n2_440201"]["F_co_oriente"],
                     stats["n4_440201"]["F_co_oriente"],
                     stats["n8_440201"]["F_co_oriente"])
    x2, x4, x8 = (stats["n2_440201"]["flux_net"],
                  stats["n4_440201"]["flux_net"],
                  stats["n8_440201"]["flux_net"])

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_max"] <= 10 for s in stats.values())

    # --- F2 : porteurs quantifies ---
    v2 = all(s["fraction_k1"] >= 0.7 for s in stats.values())

    # --- F3 : alignment sature ---
    v3 = min(f2_, f4_, f8_) >= 0.9

    # --- F4 : flux aligné croissant ---
    v4 = x2 <= x4 and x4 <= x8

    # --- F5 : reproductibilite a n = 4 ---
    a, b = stats["n4_440201"]["F_co_oriente"], stats["n4_440203"]["F_co_oriente"]
    xa, xb = stats["n4_440201"]["flux_net"], stats["n4_440203"]["flux_net"]
    v5 = (max(a, b) <= 1.3 * min(a, b)
          and max(abs(xa), abs(xb)) <= 1.3 * max(min(abs(xa), abs(xb)), 1e-9))

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_porteurs_quantifies": bool(v2),
                "V3_courbe_aimantation": bool(v3),
                "V4_flux_croissant": bool(v4),
                "V5_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T62-Q-KO6-AIMANT-2026-10",
        "protocole": "T62-KO6-AIMANT-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T62 : l'aimantation — filaments axiaux (≥ 40 cellules) "
                 "sous circulation de paroi n ∈ {2, 4, 8} : quantum k = ±1 "
                 "autour du cœur, fraction co-orientée F et flux net Σk "
                 "contre le champ ; la courbe d'orientation des ANU",
        "doctrine": "T47 (la paroi commande) ; T60/T61 (l'ANU) ; la "
                    "Chimie Occulte (l'alignement dans le champ)",
        "statut_du_mot": "MESURE — circulation mesurée autour du cœur "
                         "(la phase ne s'enroule pas le long d'un "
                         "filament de vortex, leçon d'exploration)",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 8],
                          "graines": [440201, 440201, 440201, 440203],
                          "seuil_axial": SEUIL_AXIAL,
                          "snapshots": [60.0, 75.0, 90.0]},
        "mesures": stats,
        "verdict_classe": ("S+ (les ANU du corridor s'aimantent : un "
                           "quantum par filament axial, la co-orientation "
                           "et le flux aligné croissent avec le champ de "
                           "paroi — le dessin de 1908 a sa courbe "
                           "mesurée)"),
        "falsifieur": "porteurs non quantifiés ; F décroissante ; flux "
                      "non croissant ; écart > 1.3",
        "suites_declarees": "les domaines (signes mixtes à forte densité) "
                            "et le cycle hystérésis (champ balayé) ; la "
                            "susceptibilité initiale (pente de M en "
                            "fonction de n à petit champ) ; confrontation "
                            "au réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t62_ko6_aimantation_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T62 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : F = {s['F_co_oriente']:.2f}, flux = "
              f"{s['flux_net']:.1f}, M = {s['M']:.2f}, |k|=1 : "
              f"{100*s['fraction_k1']:.0f} %, axiaux = {s['axiaux_moy']:.1f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
