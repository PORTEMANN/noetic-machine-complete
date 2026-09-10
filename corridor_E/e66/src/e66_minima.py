#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E66 — L'ÉNERGIE PAR ANNEAU DE n=2 À n=4000 : les autres minima
[protocole E66-MINIMA-1.0 gelé]
=====================================================================
Tiroir banc — calcul statique. Protocole gelé dans e66_protocole.json
(haché avant tout calcul).

Filiation déclarée : formule d'énergie d'E65 (gelée, inchangée) ; règle
de cage d'E60 (anneaux rayon 6, axes radiaux, 3 latitudes) inchangée.
Question (de l'auteur) : le « 18 » est l'optimum énergétique dans la
fenêtre ; les « ovoïdes » historiques du corpus (3, 5, 7, 12, 63, 110…)
sont-ils d'autres minima énergétiques entre n=2 et n=4000 ?

Règle de mise à l'échelle GELÉE (déclarée) : à grand n, les anneaux de
rayon fixe 6 ne tiennent plus sur une sphère fixe — le rayon de cage
est mis à l'échelle : R_cage(n) = 12·n/18 (espacement angulaire
constant ; coïncide avec la configuration du corpus à n=18 par
construction). Points par anneau : 32 (déclaré).

Prédiction pré-enregistrée (déclarée avant calcul) : la géométrie à 3
latitudes remplit les bandes uniformément quand n est multiple de 3 —
minima locaux d'E/n aux multiples de 3 (dont 3, 12, 18, 63) ; élévation
aux non-multiples (dont 5, 7, 110). Enveloppe attendue : décroissante
vers la limite de dilution à grand n (anneaux de rayon fixe dans une
cage qui grandit).

Balayage figé : n dense 2–130 (tous les entiers) ; points grossiers
{150, 200, 300, 500, 1000, 2000, 4000} pour l'asymptote.

Usage : python3 e66_minima.py
"""

import json
import time
from pathlib import Path

import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e60_run import anneau  # filiation E60

GAMMA_CIRC, A_CUT = 1.0, 0.5
R_ANU = 6.0
N_PT = 32          # points par anneau — déclaré
N_DENSE = range(2, 131)
N_GROSSIER = [150, 200, 300, 500, 1000, 2000, 4000]


def cage_n(n):
    """Règle d'E60 (3 latitudes), anneau rayon 6, cage mise à l'échelle
    R_cage = 12·n/18 (espacement angulaire constant — gelé)."""
    R = 12.0 * n / 18.0
    cage = []
    for k in range(n):
        phi = 2 * np.pi * k / n
        theta = np.pi * (k % 3) / 3 + np.pi / 6
        ax = np.array([np.sin(theta) * np.cos(phi),
                       np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(ax * R, R_ANU, ax, n=N_PT))
    return cage


def energie_cage(cage):
    """Formule d'E65 (gelée, inchangée)."""
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
    print("E66 — E/n de 2 à 4000   [E66-MINIMA-1.0 gelé]")
    print("=" * 70)
    res = {"campagne": "E66", "protocole": "E66-MINIMA-1.0 (gelé)",
           "points": {}}
    for n in list(N_DENSE) + N_GROSSIER:
        E = energie_cage(cage_n(n))
        res["points"][n] = {"E": round(E, 3), "E_par_n": round(E / n, 4)}
        if n <= 30 or n in N_GROSSIER or n % 3 == 0 and n <= 130:
            print(f"n={n:4d} : E={E:9.2f}  E/n={E/n:.4f}", flush=True)
    # minima locaux : E/n(n) < E/n(n±1)
    ns = sorted(int(k) for k in res["points"])
    minima = []
    for i, n in enumerate(ns):
        if n in (ns[0], ns[-1]):
            continue
        e = res["points"][n]["E_par_n"]
        voisins = [res["points"][v]["E_par_n"] for v in (n - 1, n + 1)
                   if v in res["points"]]
        if voisins and all(e < v for v in voisins):
            minima.append(n)
    historiques = [3, 5, 7, 12, 18, 63, 110]
    res["agregation"] = {
        "minima_locaux_E_par_n": minima,
        "minima_multiples_de_3": [n for n in minima if n % 3 == 0],
        "minima_non_multiples": [n for n in minima if n % 3 != 0],
        "historiques_minima": [n for n in historiques if n in minima],
        "historiques_non_minima": [n for n in historiques
                                   if n not in minima],
        "E_par_n_historiques": {str(n): res["points"][n]["E_par_n"]
                                for n in historiques if n in res["points"]},
        "E_par_n_asymptote": {str(n): res["points"][n]["E_par_n"]
                              for n in N_GROSSIER},
        "durée_s": round(time.time() - t0, 1)}
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "e66_minima_verdict.json"
    f.write_text(json.dumps(res, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("\nMINIMA LOCAUX :", minima, flush=True)
    print("Verdict →", f)


if __name__ == "__main__":
    main()
