#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E57 — CRISTALLISATION SOUS ROTATION FORTE : le réseau d'Abrikosov comme
relation conservée   [protocole E57-CRISTAL-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E57. Protocole gelé dans
e57_protocole.json (haché avant tout calcul — aveugle préservé).

Motivation (corridor, 09/09/2026) : la persistance de la relation est au
plancher (~4 %, sans facteur mécanique — E56-x) ; le seul précédent de
relation conservée est le réseau ordonné (R4b, Abrikosov — documentaire).
E44-P3 a mesuré la NON-cristallisation à la circulation 4 (médiane 14
lignes vs 4±2 attendus). E57 balaie des circulations plus fortes :
{4, 8, 16, 24} (figé) — n=4 est le contrôle de filiation.

Mesure gelée (ordre hexatique) : positions moyennes (x,y) des lignes
axiales longues (≥ 40 segments, étendue z ≥ 30 — filiation E54-C) ;
ψ6 = |⟨ (1/n_j) Σ_{k∈nn(j)} e^{6iθ_jk} ⟩_j |, voisins nn(j) = points à
distance ≤ 1,3 × distance médiane au plus proche voisin (figé) ;
calculé si ≥ 6 lignes (sinon : non cristallisé, déclaré). Cristallisé
⟺ ψ6 ≥ 0,7 (figé).
Design : 4 circulations × 3 graines (660101–660112, déclarées) ; snapshots
t=8, 12, 20, 45, 90 ; tout le reste filiation E54-C.

Usage : python3 e57_run.py            (campagne — interdit avant décision)
        python3 e57_run.py --smoke    (validation technique déclarée :
                                       N=32, graine 999990 hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments  # filiation byte-level

# ---------------- paramètres gelés (filiation E44→E56x, sauf mention) -------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
CIRCULATIONS = [4, 8, 16, 24]         # balayage figé ; n=4 = filiation E44-B
SEEDS_PAR_CIRC = [660101, 660102, 660103]   # 3 par circulation (décalées)
SNAP = [(160, 8.0), (240, 12.0), (400, 20.0), (900, 45.0), (1800, 90.0)]
LONG_MIN = 40
ETENDUE_Z_MIN = 30.0
SEUIL_PSI6 = 0.7                      # cristallisé ⟺ ψ6 ≥ 0,7 (figé)
FACTEUR_VOISINS = 1.3                 # nn ≤ 1,3 × d_plus proche (figé)
P0_FENETRE = (9.0, 19.0)              # fenêtre publiée d'E44-B (n=4)
RATIO_COMPTAGE = (0.7, 1.3)           # compte ≈ n × [0,7 ; 1,3] (figé)


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def geometrie_B(N_, wind):
    """Récipient d'E44-B ; circulation de la paroi = wind (balayage)."""
    C = (N_ - 1) / 2.0
    Xg, Yg, Zg = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                             indexing='ij')
    Rg = np.sqrt((Xg - C)**2 + (Yg - C)**2)
    z0, z1 = int(2 * N_ / 64), int(61 * N_ / 64)
    inside = (Rg < 26 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    ring = (Rg >= 26 * N_ / 64) & (Rg < 28 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    PHI = np.arctan2(Yg - C, Xg - C)
    fix_val = np.zeros((N_,) * 3, dtype=complex)
    fix_val[ring] = np.exp(1j * wind * PHI[ring])
    return inside, ring, fix_val, C


def gp_step(psi, lin, gamma_, dt_, fix=None):
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    if fix is not None:
        psi[fix[0]] = fix[1][fix[0]]
    return psi


def positions_lignes(psi, inside):
    """Positions moyennes (x,y) des lignes axiales longues — filiation
    E54-C (mêmes filtres)."""
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    wx, wy, wz = np.where(inside, wx, 0), np.where(inside, wy, 0), \
        np.where(inside, wz, 0)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f['closed'] and not np.any(f['disp']))]
    axiaux = [f for f in ouverts
              if f['len'] >= LONG_MIN
              and (f['pts'][:, 2].max() - f['pts'][:, 2].min())
              >= ETENDUE_Z_MIN]
    pos = np.array([f['pts'][:, :2].mean(axis=0) for f in axiaux]) \
        if axiaux else np.zeros((0, 2))
    return pos, len(axiaux), anom, amb


def psi6(pos):
    """Paramètre d'ordre hexatique — formule et voisinage figés."""
    n = len(pos)
    if n < 6:
        return None
    D = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    d_med = float(np.median(D.min(axis=1)))
    r_nn = FACTEUR_VOISINS * d_med
    tot = 0.0 + 0.0j
    for j in range(n):
        nn = [k for k in range(n) if D[j, k] <= r_nn]
        if not nn:
            continue
        th = [np.arctan2(pos[k, 1] - pos[j, 1], pos[k, 0] - pos[j, 0])
              for k in nn]
        tot += np.mean(np.exp(6j * np.array(th)))
    return float(np.abs(tot / n))


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, graine 999990 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        inside, ring, fix_val, C = geometrie_B(32, 4)
        rng = np.random.default_rng(999990)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (32,) * 3))
        psi[~inside] = 0.0
        psi[ring] = fix_val[ring]
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(60):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(ring | ~inside,
                                                    fix_val))
        pos, nl, anom, amb = positions_lignes(psi, inside)
        # contrôle de l'hexatique sur un réseau triangulaire synthétique
        tri = np.array([[i + 0.5 * (j % 2), j * 0.866]
                        for i in range(8) for j in range(8)])
        print("SMOKE :", {"n_axiaux": nl, "anom": anom,
                          "psi6_synth_triangulaire": round(psi6(tri), 3),
                          "psi6_aleatoire": round(psi6(pos), 3)
                          if nl >= 6 else None})
        return

    t0 = time.time()
    res = {"campagne": "E57", "protocole": "E57-CRISTAL-1.0 (gelé)",
           "runs": {}}
    for wind in CIRCULATIONS:
        inside, ring, fix_val, C = geometrie_B(N, wind)
        fix_mask = ring | ~inside
        for k, graine in enumerate(SEEDS_PAR_CIRC):
            g = graine + CIRCULATIONS.index(wind) * 10
            rng = np.random.default_rng(g)
            psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
            psi[~inside] = 0.0
            psi[ring] = fix_val[ring]
            lin = gp_linear(N, A, GAMMA, DT)
            snaps = {}
            for step in range(1, SNAP[-1][0] + 1):
                psi = gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
                for pas, t in SNAP:
                    if step == pas:
                        pos, nl, anom, amb = positions_lignes(psi, inside)
                        p6 = psi6(pos)
                        snaps[t] = {"n_lignes": nl, "psi6": p6,
                                    "cristallise": (p6 is not None
                                                    and p6 >= SEUIL_PSI6),
                                    "anom": anom, "amb": amb}
                        print(f"  n={wind} graine {g} t={t:.0f} : lignes="
                              f"{nl} ψ6={p6 if p6 is None else round(p6, 3)}"
                              f" cristal={snaps[t]['cristallise']}",
                              flush=True)
            res["runs"][f"{wind}_{g}"] = {str(k2): v for k2, v
                                          in snaps.items()}
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "data", f"e57_run_{wind}_{g}.json")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res["runs"][f"{wind}_{g}"], f,
                          ensure_ascii=False)
            print(f"n={wind} graine {g} terminée", flush=True)

    # ---- agrégation gelée (règles : e57_protocole.json) ----
    ag = {}
    c4 = [v for k, v in res["runs"].items() if k.startswith("4_")]
    comptes4 = [v[str(t)]["n_lignes"] for v in c4 for t in (45.0, 90.0)]
    ag["P0_filiation_n4"] = (comptes4 and P0_FENETRE[0]
                             <= float(np.median(comptes4)) <= P0_FENETRE[1]
                             and not any(v[str(t)]["cristallise"]
                                         for v in c4 for t in (45.0, 90.0)))
    for wind in CIRCULATIONS:
        runs_w = [v for k, v in res["runs"].items()
                  if k.startswith(f"{wind}_")]
        comptes = [v[str(t)]["n_lignes"] for v in runs_w
                   for t in (45.0, 90.0)]
        ag[f"compte_median_n{wind}"] = float(np.median(comptes)) \
            if comptes else None
        ag[f"ratio_compte_n{wind}"] = (float(np.median(comptes)) / wind
                                       if comptes else None)
        ag[f"cristal_t45_90_n{wind}"] = sum(
            v[str(t)]["cristallise"] for v in runs_w for t in (45.0, 90.0))
    ag["P1_cristal_n24"] = ag["cristal_t45_90_n24"] >= 2
    ag["P1_ratio_n24"] = (ag["ratio_compte_n24"] is not None
                          and RATIO_COMPTAGE[0] <= ag["ratio_compte_n24"]
                          <= RATIO_COMPTAGE[1])
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e57_cristal_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
