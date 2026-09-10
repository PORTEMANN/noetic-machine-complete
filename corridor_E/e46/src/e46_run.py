#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E46 — VERROUILLAGE DU CŒUR : conservation de l'enlacement par plancher
de densité   [protocole E46-VERROU-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E46. Le protocole est gelé dans
e46_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; structure du harnais E45 (E45-CAPTURE-1.0,
réparé) reprise — mêmes graines, mêmes snapshots, même branchement.
Verdict E45 (B3-FAIL, 09/09/2026) : la coupure de l'amortissement ne
conserve pas l'enlacement (0/5 ON, 0/5 OFF) — la tension seule détruit
le lien ; le destructeur est la reconnexion, pas la dissipation.

Mécanisme testé (facteur unique gelé) : dans la branche ON, le terme
non linéaire devient V(ρ²) = ρ²−1 + C·max(0, ρ_min−ρ)² avec
ρ_min = 0,5 et C = 100 (figés) — mur raide sous le plancher : la
déplétion du cœur, condition cinématique de la reconnexion, devient
coûteuse. La phase 1 (nucléation) est inchangée : le verrou n'existe
qu'à partir du branchement t=20 (calendrier gelé). γ = 0,3 dans les
deux branches (facteur unique : le mur).

Usage : python3 e46_run.py            (campagne — interdit avant décision)
        python3 e46_run.py --smoke    (validation technique déclarée :
                                       N=16, graine 999998 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44/E45, sauf mention) --------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
RHO_MIN = 0.5      # plancher gelé
C_WALL = 100.0     # raideur du mur, gelée


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def V_terme(rho2, mur):
    """Terme non linéaire : ρ²−1, plus mur raide sous ρ_min si mur=True."""
    if not mur:
        return rho2 - 1.0
    return rho2 - 1.0 + C_WALL * np.maximum(0.0, RHO_MIN - np.sqrt(rho2))**2


def gp_step(psi, lin, gamma_, dt_, mur=False):
    """Pas Strang — filiation e44_core.gp_step ; mur optionnel (ON)."""
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    return psi


def detecte_paires(psi):
    """Détecteur E44 (filiation) — seuils gelés. Rend aussi la longueur
    totale des boucles (observable secondaire déclarée)."""
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    loops = [f for f in fils if f['closed'] and not np.any(f['disp'])
             and f['len'] >= MIN_LEN]
    loops.sort(key=lambda f: -f['len'])
    if len(loops) > MAX_LOOPS:
        loops = loops[:MAX_LOOPS]
    pairs = []
    for i, j in itertools.combinations(range(len(loops)), 2):
        lk = gauss_link_mi(loops[i]['pts'], loops[j]['pts'], psi.shape[0])
        if abs(lk) >= SEUIL_LK:
            pairs.append((i, j, round(lk, 3)))
    long_tot = int(sum(f['len'] for f in loops))
    return len(pairs) > 0, len(loops), long_tot, pairs, anom, amb


def phase_nucleation(graine, N_=N, pas_max=400):
    """Phase 1 gelée — IDENTIQUE à E45 (le mur n'existe pas encore)."""
    rng = np.random.default_rng(graine)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N_,) * 3))
    lin = gp_linear(N_, A, GAMMA, DT)
    snaps = {}
    nucle = False
    for step in range(1, pas_max + 1):
        psi = gp_step(psi, lin, GAMMA, DT, mur=False)
        for pas, t in SNAP_NUCLE:
            if step == pas and pas <= pas_max:
                lie, nboucles, ltot, pairs, anom, amb = detecte_paires(psi)
                snaps[t] = {"lie": lie, "nboucles": nboucles,
                            "longueur_totale": ltot, "npaires": len(pairs),
                            "paires": pairs, "anom": anom, "amb": amb}
                nucle = nucle or lie
                print(f"  graine {graine} t={t:.0f} : boucles={nboucles} "
                      f"liées={len(pairs)} anom={anom}", flush=True)
    return snaps, psi, nucle


def branche(psi_t20, mur, N_=N, pas_debut=400):
    """Continuation gelée depuis t=20 : γ=0,3 dans les deux branches ;
    mur actif si mur=True (ON), absent sinon (OFF)."""
    psi = psi_t20.copy()
    lin = gp_linear(N_, A, GAMMA, DT)
    snaps = {}
    for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin, GAMMA, DT, mur=mur)
        for pas, t in SNAP_SUITE:
            if step == pas:
                lie, nboucles, ltot, pairs, anom, amb = detecte_paires(psi)
                snaps[t] = {"lie": lie, "nboucles": nboucles,
                            "longueur_totale": ltot, "npaires": len(pairs),
                            "paires": pairs, "anom": anom, "amb": amb}
    return snaps


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : grille réduite, graine hors
        # campagne (999998), aucune donnée de campagne produite.
        print("SMOKE — validation technique (hors campagne)")
        snaps, psi, nucle = phase_nucleation(999998, N_=16, pas_max=160)
        s_off = branche(psi, False, N_=16)
        s_on = branche(psi, True, N_=16)
        print("SMOKE OK :", {"nucle": nucle, "off": list(s_off),
                             "on": list(s_on)})
        return

    t0 = time.time()
    res = {"campagne": "E46", "protocole": "E46-VERROU-1.0 (gelé)",
           "runs": {}}
    runs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for graine in SEEDS:
        print(f"graine {graine} — phase nucléation", flush=True)
        snaps, psi20, nucle = phase_nucleation(graine)
        run = {"nucleation": snaps, "nucle": nucle}
        if nucle:
            run["OFF"] = branche(psi20, False)
            print(f"  graine {graine} : branche OFF terminée", flush=True)
            run["ON"] = branche(psi20, True)
            print(f"  graine {graine} : branche ON terminée", flush=True)
        res["runs"][str(graine)] = run
        # écriture incrémentale (réparation harnais issue d'E45)
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles de verdict : e46_protocole.json) ----
    branches = [g for g, r in res["runs"].items() if r["nucle"]]
    pers_on = sum(1 for g in branches
                  if res["runs"][g]["ON"][45.0]["lie"]
                  or res["runs"][g]["ON"][90.0]["lie"])
    pers_off = sum(1 for g in branches
                   if res["runs"][g]["OFF"][45.0]["lie"]
                   or res["runs"][g]["OFF"][90.0]["lie"])
    p0 = res["runs"]["440103"]["nucleation"][12.0]["lie"]
    res["agregation"] = {
        "P0_filiation_440103_t12": p0,
        "n_runs_nucles": len(branches), "runs_nucles": branches,
        "persistance_ON": pers_on, "persistance_OFF": pers_off,
        "P1_ON>OFF": pers_on > pers_off,
        "durée_s": round(time.time() - t0, 1)}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e46_verrou_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", res["agregation"], flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
