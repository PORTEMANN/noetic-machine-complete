#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E45 — CAPTURE DE L'ENLACEMENT NUCLÉÉ   [protocole E45-CAPTURE-1.0 gelé]
========================================================================
Harnais officiel de la campagne E45. Le protocole est gelé dans
e45_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée (byte-level) : le détecteur est celui d'E44 —
e44_core.py inchangé (sha256 604c2232…60ae1ac7, copie locale jointe) ;
paramètres du modèle et seuils identiques au protocole v1 d'E44
(42c65a0c…, amendement v2 bc977f17…).

Structure (gelée) :
  Phase 1 — nucléation : 24 graines (440101–440106 = filiation E44,
  440107–440124 = extension déclarée), γ=0,3, snapshots t=8,12,16,20.
  Branchement — tout run avec ≥1 paire liée (|Lk|≥0,5) à un snapshot
  t≤20 est continué en DEUX copies depuis l'état à t=20 :
    OFF : γ=0,3 (amortissement maintenu — témoin)
    ON  : γ=0,0 (coupure de l'amortissement — mécanisme testé)
  jusqu'à t=90, snapshots t=45 et t=90.
  Persistance : ≥1 paire liée au snapshot (niveau population — déclaré :
  l'identité de paire n'est pas suivie à travers les reconnexions).

Usage : python3 e45_run.py            (campagne — interdit avant décision)
        python3 e45_run.py --smoke    (validation technique déclarée :
                                       N=16, graine hors campagne, non
                                       comptée comme donnée)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (identiques à E44 v1/v2, sauf mention) ---
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24, déclaré
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]   # phase 1
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]                            # branches
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_):
    """Pas Strang — identique à e44_core.gp_step sans l'argument fix
    (ensemble libre : pas de paroi ; déclaré)."""
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    return psi


def detecte_paires(psi):
    """Détecteur E44 (filiation) : ≥1 paire liée |Lk|≥0,5 ? Rend le
    booléen, le nombre de boucles et les paires (gelé)."""
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
    return len(pairs) > 0, len(loops), pairs, anom, amb


def phase_nucleation(graine, N_=N, pas_max=400):
    """Phase 1 gelée : trempe libre, snapshots t=8,12,16,20.
    Rend (historique des snapshots, état ψ à t=20, bool nucléé)."""
    rng = np.random.default_rng(graine)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N_,) * 3))
    lin = gp_linear(N_, A, GAMMA, DT)
    snaps = {}
    nucle = False
    for step in range(1, pas_max + 1):
        psi = gp_step(psi, lin, GAMMA, DT)
        for pas, t in SNAP_NUCLE:
            if step == pas and pas <= pas_max:
                lie, nboucles, pairs, anom, amb = detecte_paires(psi)
                snaps[t] = {"lie": lie, "nboucles": nboucles,
                            "npaires": len(pairs), "paires": pairs,
                            "anom": anom, "amb": amb}
                nucle = nucle or lie
                print(f"  graine {graine} t={t:.0f} : boucles={nboucles} "
                      f"liées={len(pairs)} anom={anom}", flush=True)
    return snaps, psi, nucle


def branche(psi_t20, gamma_br, N_=N, pas_debut=400):
    """Continuation gelée depuis t=20 : γ=γ_br, snapshots t=45,90."""
    psi = psi_t20.copy()
    lin = gp_linear(N_, A, gamma_br, DT)
    snaps = {}
    for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin, gamma_br, DT)
        for pas, t in SNAP_SUITE:
            if step == pas:
                lie, nboucles, pairs, anom, amb = detecte_paires(psi)
                snaps[t] = {"lie": lie, "nboucles": nboucles,
                            "npaires": len(pairs), "paires": pairs,
                            "anom": anom, "amb": amb}
    return snaps


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : grille réduite, graine hors
        # campagne (999999), aucune donnée de campagne produite.
        print("SMOKE — validation technique (hors campagne)")
        snaps, psi, nucle = phase_nucleation(999999, N_=16, pas_max=160)
        s_off = branche(psi, GAMMA, N_=16)
        s_on = branche(psi, 0.0, N_=16)
        print("SMOKE OK :", {"nucle": nucle, "off": list(s_off),
                             "on": list(s_on)})
        return

    t0 = time.time()
    res = {"campagne": "E45", "protocole": "E45-CAPTURE-1.0 (gelé)",
           "runs": {}}
    runs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for graine in SEEDS:
        print(f"graine {graine} — phase nucléation", flush=True)
        snaps, psi20, nucle = phase_nucleation(graine)
        run = {"nucleation": snaps, "nucle": nucle}
        if nucle:
            run["OFF"] = branche(psi20, GAMMA)
            print(f"  graine {graine} : branche OFF terminée", flush=True)
            run["ON"] = branche(psi20, 0.0)
            print(f"  graine {graine} : branche ON terminée", flush=True)
        res["runs"][str(graine)] = run
        # écriture incrémentale (réparation harnais du 09/09/2026 :
        # plus aucune perte de données en cas d'incident d'agrégation)
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles de verdict : e45_protocole.json) ----
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
                       "..", "data", "e45_capture_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", res["agregation"], flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
