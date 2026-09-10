#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E67 — LES PAYSAGES PAR n : barrière et vallée de E_cage(R) en fonction
du nombre d'anneaux   [protocole E67-PAYSAGES-1.0 gelé]
Tiroir banc — calcul statique. Filiation : formule d'E65 (gelée,
inchangée) ; géométrie d'E60 (inchangée) ; R_cage = 12 fixe (la
configuration du corpus — déclaré : les paysages sont ceux de la fenêtre
mesurée en E64/E64-A).
Pour chaque n ∈ {12, 14, 16, 18, 20, 22, 24} (figé) : E_cage(R) sur
R ∈ [8, 30] pas 0,5 ; extraction de la barrière (maximum local) et de la
vallée (minimum local) — positions figées.
"""
import json
import time
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e60_run import anneau

GAMMA_CIRC, A_CUT = 1.0, 0.5
R_ANU = 6.0
N_BALAYAGE = [12, 14, 16, 18, 20, 22, 24]
RS = np.arange(8.0, 30.5, 0.5)


def cage_n_R(n, R):
    cage = []
    for k in range(n):
        phi = 2 * np.pi * k / n
        theta = np.pi * (k % 3) / 3 + np.pi / 6
        ax = np.array([np.sin(theta) * np.cos(phi),
                       np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(ax * R, R_ANU, ax))
    return cage


def energie_cage(cage):
    E = 0.0
    for P in cage:
        dP = np.roll(P, -1, axis=0) - P
        midP = P + dP / 2
        for Q in cage:
            dQ = np.roll(Q, -1, axis=0) - Q
            midQ = Q + dQ / 2
            R = midP[:, None, :] - midQ[None, :, :]
            dist2 = np.sum(R**2, axis=2)
            E += float(np.sum((dP @ dQ.T) / np.sqrt(dist2 + A_CUT**2)))
    return GAMMA_CIRC**2 / (8 * np.pi) * E


def main():
    t0 = time.time()
    res = {"campagne": "E67", "protocole": "E67-PAYSAGES-1.0 (gelé)",
           "paysages": {}}
    for n in N_BALAYAGE:
        Es = np.array([energie_cage(cage_n_R(n, R)) for R in RS])
        # RÉPARATION (extraction) : la barrière est le PREMIER maximum
        # local intérieur (la crête à ~16), pas le maximum global (le bord
        # de grille à 30 peut dépasser la crête) ; la vallée est le premier
        # minimum local après cette crête. Documenté dans E67_NOTE.
        i_max = None
        for i in range(1, len(RS) - 1):
            if Es[i] >= Es[i - 1] and Es[i] >= Es[i + 1]:
                i_max = i
                break
        if i_max is None:
            i_max = int(np.argmax(Es))
        vall = None
        for i in range(max(1, i_max + 1), len(RS) - 1):
            if Es[i] <= Es[i - 1] and Es[i] <= Es[i + 1]:
                vall = i
                break
        res["paysages"][n] = {
            "barriere_R": float(RS[i_max]),
            "barriere_E": round(float(Es[i_max]), 3),
            "vallee_R": float(RS[vall]) if vall is not None else None,
            "vallee_E": round(float(Es[vall]), 3) if vall is not None else None,
            "courbe": [[round(float(r), 1), round(float(e), 3)]
                       for r, e in zip(RS, Es)]}
        print(f"n={n} : barrière R={RS[i_max]} (E={Es[i_max]:.1f}) · "
              f"vallée R={RS[vall] if vall is not None else -1:.1f}",
              flush=True)
    res["agregation"] = {
        "barriere_par_n": {str(n): res["paysages"][n]["barriere_R"]
                           for n in N_BALAYAGE},
        "vallee_par_n": {str(n): res["paysages"][n]["vallee_R"]
                         for n in N_BALAYAGE},
        "note": "positions sur grille 0,5 (figée) — la barrière et la "
                "vallée de la fenêtre du couronnement en fonction de n",
        "durée_s": round(time.time() - t0, 1)}
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "e67_paysages_verdict.json"
    f.write_text(json.dumps(res, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("AGRÉGATION :", json.dumps(res["agregation"], ensure_ascii=False),
          flush=True)


if __name__ == "__main__":
    main()
