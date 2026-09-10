#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E63 — LE « POURQUOI 18 » : stabilité de la cage en fonction du nombre
d'anneaux n   [protocole E63-NOMBRE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E63. Protocole gelé dans
e63_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : harnais E61 repris (filaments, Biot–Savart,
confinement κ=0,05 inchangés) ; la cage ANU à n=18 tient (E61, SUCCÈS) ;
sa géométrie est figée mais non optimisée — la question « pourquoi 18 »
devient mesurable.

Design gelé : cages de n anneaux (rayon 6, axes radiaux, 3 latitudes,
sphère R_cage=12 — règle d'E60 inchangée) pour n ∈ {12, 14, 16, 18, 20,
22, 24} (balayage figé) ; confinement κ=0,05 (inchangé) ; snapshots
t = 0, 45, 90 (figé). Mesures par n : tenue des clauses d'E60 (rms dans
[0,5 ; 1,5]×, échappement ≤ 2×R_cage — inchangées) et MARGE aux bornes :
marge_rms = 1,5·R_cage − rms(t=90) ; marge_éch = 2·R_cage − éch_max(t=90)
(figé — plus la marge est grande, plus la cage est stable).

Contrôle de filiation figé : n=18 doit reproduire E61-B (tient).

Usage : python3 e63_run.py            (campagne — interdit avant décision)
        python3 e63_run.py --smoke    (validation technique déclarée)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e60_run import anneau, remaille, rayon_et_centre  # filiation E60
from e61_run import vitesse_biotsavart, rk4           # filiation E61

# ---------------- paramètres gelés (filiation E60/E61, inchangés) -----------
DT = 0.25
R_CAGE, R_ANU = 12.0, 6.0
N_BALAYAGE = [12, 14, 16, 18, 20, 22, 24]   # figé
TMAX = 90.0
SNAP_T = [0.0, 45.0, 90.0]


def cage_n(n):
    cage = []
    for k in range(n):
        phi = 2 * np.pi * k / n
        theta = np.pi * (k % 3) / 3 + np.pi / 6   # règle d'E60, inchangée
        ax = np.array([np.sin(theta) * np.cos(phi),
                       np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(ax * R_CAGE, R_ANU, ax))
    return cage


def main():
    if "--smoke" in sys.argv:
        print("SMOKE — mécanique (hors campagne)")
        fils = cage_n(18)
        for _ in range(3):
            fils = rk4(fils, DT, confine=True)
        print("SMOKE OK :", len(fils), "anneaux")
        return

    t0 = time.time()
    res = {"campagne": "E63", "protocole": "E63-NOMBRE-1.0 (gelé)",
           "points": {}}
    for n in N_BALAYAGE:
        fils = cage_n(n)
        snaps = {}
        steps = int(TMAX / DT)
        for s in range(steps + 1):
            t = s * DT
            if abs(t - min(SNAP_T, key=lambda x: abs(x - t))) < DT / 2:
                tt = min(SAP if False else SNAP_T,
                         key=lambda x: abs(x - t))
                cents = np.array([rayon_et_centre(P)[1] for P in fils])
                snaps[tt] = {"rms": round(float(np.sqrt(np.mean(
                    np.sum(cents**2, axis=1)))), 3),
                    "ech": round(float(np.abs(cents).max()), 3)}
            if s < steps:
                fils = rk4(fils, DT, confine=True)
        rms0 = snaps[0.0]["rms"]
        tient = (all(0.5 * rms0 <= snaps[t]["rms"] <= 1.5 * rms0
                     for t in SNAP_T)
                 and max(snaps[t]["ech"] for t in SNAP_T) <= 2 * rms0)
        res["points"][n] = {"snaps": {str(k): v for k, v in snaps.items()},
                            "tient": tient,
                            "marge_rms": round(1.5 * rms0
                                               - snaps[90.0]["rms"], 3),
                            "marge_ech": round(2 * rms0
                                               - snaps[90.0]["ech"], 3)}
        print(f"n={n} : tient={tient} marge_rms={res['points'][n]['marge_rms']}"
              f" marge_éch={res['points'][n]['marge_ech']}", flush=True)
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e63_n{n}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res["points"][n], f, ensure_ascii=False)

    # ---- agrégation gelée (règles : e63_protocole.json) ----
    ag = {"filiation_n18_reproduit_E61": res["points"][18]["tient"],
          "tenue_par_n": {str(n): res["points"][n]["tient"]
                          for n in N_BALAYAGE},
          "marge_rms_par_n": {str(n): res["points"][n]["marge_rms"]
                              for n in N_BALAYAGE},
          "marge_ech_par_n": {str(n): res["points"][n]["marge_ech"]
                              for n in N_BALAYAGE},
          "n_optimal_marge": max(N_BALAYAGE,
                                 key=lambda n: min(
                                     res["points"][n]["marge_rms"],
                                     res["points"][n]["marge_ech"])),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e63_nombre_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
