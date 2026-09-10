#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E65 — L'ÉNERGIE DES CAGES PAR n : le « pourquoi 18 » par l'énergie
[protocole E65-ENERGIE-1.0 gelé]
=====================================================================
Tiroir banc. Calcul statique (pas de dynamique) — la géométrie des
cages d'E60/E63 est figée ; on mesure l'énergie de la configuration.

Filiation déclarée : géométrie des cages d'E60 (anneaux rayon 6, axes
radiaux, 3 latitudes, sphère R_cage=12) inchangée ; cutoff a=0,5 (filiation
E60, Rosenhead–Moore) ; Γ=1.

Énergie gelée (filaments de vortex, forme régularisée standard) :
  E = Γ²/(8π) Σ_i Σ_j Σ_{s_i,s_j} (dl_i · dl_j) / √(|r_i − r_j|² + a²)
  somme sur toutes les paires de segments de tous les filaments,
  auto-interaction incluse (régularisée par a — figé).
Mesures par n ∈ {12, …, 24} (figé, balayage d'E63) : E(n), E(n)/n,
E(n)/L(n) (énergie par anneau et par longueur totale de filament).

Questions gelées : l'énergie a-t-elle un minimum en n ? Est-il à 18 ?
Comparaison déclarée avec la marge de stabilité d'E63 (optimum mesuré :
n=14).

Usage : python3 e65_energie.py
"""

import json
import time
from pathlib import Path

import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e60_run import anneau  # filiation E60 (construction des anneaux)

# ---------------- paramètres gelés (filiation E60/E63, inchangés) -----------
GAMMA_CIRC = 1.0
A_CUT = 0.5
R_CAGE, R_ANU = 12.0, 6.0
N_BALAYAGE = [12, 14, 16, 18, 20, 22, 24]   # figé (balayage d'E63)


def cage_n(n):
    """Géométrie d'E60, inchangée (3 latitudes)."""
    cage = []
    for k in range(n):
        phi = 2 * np.pi * k / n
        theta = np.pi * (k % 3) / 3 + np.pi / 6
        ax = np.array([np.sin(theta) * np.cos(phi),
                       np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(ax * R_CAGE, R_ANU, ax))
    return cage


def energie_cage(cage):
    """Énergie des filaments — forme régularisée figée (ci-dessus)."""
    E = 0.0
    for P in cage:
        dP = np.roll(P, -1, axis=0) - P
        midP = P + dP / 2
        for Q in cage:
            dQ = np.roll(Q, -1, axis=0) - Q
            midQ = Q + dQ / 2
            R = midP[:, None, :] - midQ[None, :, :]
            dist2 = np.sum(R**2, axis=2)
            # l'auto-segment (distance nulle exacte) reste régularisé par a
            prod = dP @ dQ.T
            E += float(np.sum(prod / np.sqrt(dist2 + A_CUT**2)))
    L = sum(float(np.linalg.norm(np.roll(P, -1, axis=0) - P,
                                 axis=1).sum()) for P in cage)
    return GAMMA_CIRC**2 / (8 * np.pi) * E, L


def main():
    t0 = time.time()
    print("E65 — l'énergie des cages par n   [E65-ENERGIE-1.0 gelé]")
    print("=" * 70)
    res = {"campagne": "E65", "protocole": "E65-ENERGIE-1.0 (gelé)",
           "points": {}}
    for n in N_BALAYAGE:
        cage = cage_n(n)
        E, L = energie_cage(cage)
        res["points"][n] = {"E": round(E, 3), "L": round(L, 3),
                            "E_par_n": round(E / n, 3),
                            "E_par_L": round(E / L, 4)}
        print(f"n={n} : E={E:.1f} E/n={E/n:.2f} E/L={E/L:.3f}", flush=True)

    Es = {n: res["points"][n]["E"] for n in N_BALAYAGE}
    ag = {"E_par_n": {str(n): res["points"][n]["E"] for n in N_BALAYAGE},
          "E_par_anneau": {str(n): res["points"][n]["E_par_n"]
                           for n in N_BALAYAGE},
          "E_par_longueur": {str(n): res["points"][n]["E_par_L"]
                             for n in N_BALAYAGE},
          "n_min_E": min(Es, key=Es.get),
          "n_min_E_par_anneau": min(N_BALAYAGE,
                                    key=lambda n: res["points"][n]["E_par_n"]),
          "comparaison_E63": {"optimum_marge_E63": 14,
                              "n_min_E": min(Es, key=Es.get)},
          "durée_s": round(time.time() - t0, 2)}
    res["agregation"] = ag
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "e65_energie_verdict.json"
    f.write_text(json.dumps(res, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict →", f)


if __name__ == "__main__":
    main()
