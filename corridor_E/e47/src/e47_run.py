#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E47 — SÉPARATION DES COMPOSANTES DU MUR : gel de Kelvin vs plancher
dissipatif   [protocole E47-SEPARATION-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E47. Protocole gelé dans
e47_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; harnais E45/E46 (écriture incrémentale
reprise) ; phase 1 inchangée (reproduit E45/E46 à l'identique).

Verdict E46 (ANOMALIE, 09/09/2026) : la règle gelée était formellement
satisfaite (5/5 ON vs 0/5 OFF) mais les compteurs gelés du détecteur
l'ont annulée (saturation : anom ≤ 2880, amb ≤ 48125, puis effondrement
à t=90). Analyse : le mur V = ρ²−1 + C·max(0,ρ_min−ρ)² à γ=0,3 mêle
deux composantes qui s'affrontent — plancher de pression (partie i,
conservative, type Kelvin) et anti-restauration dissipative (partie γ
avec V>0 sous le plancher). E47 les sépare.

Design gelé — 2×2 sur chaque run branché depuis l'état ψ à t=20 :
  A : γ=0,3, sans mur   (témoin — doit reproduire E46-OFF à l'identique)
  B : γ=0,   mur +C     (gel de Kelvin pur : plancher de pression
                         conservatif, sans dissipation)
  C : γ=0,3, mur −C     (plancher dissipatif : V<0 sous ρ_min →
                         restauration active de la densité)
  D : γ=0,   sans mur   (témoin — doit reproduire E45-ON : 0/5)
Critère de lisibilité gelé (issu de l'anomalie E46) : un snapshot ne
statue que si anom == 0 ET amb <= 4 (référence : l'événement E44 valide
avait amb = 1 ; les snapshots saturés d'E46-ON avaient amb ≥ 5699).

Usage : python3 e47_run.py            (campagne — interdit avant décision)
        python3 e47_run.py --smoke    (validation technique déclarée :
                                       N=16, graine 999997 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44/E45/E46, sauf mention) ----
N, A, DT = 64, 2.0, 0.05
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
RHO_MIN = 0.5      # plancher gelé
C_WALL = 100.0     # raideur gelée (même qu'E46)
AMB_MAX = 4        # borne de lisibilité gelée (événement E44 : amb=1)
BRAS = {"A": {"gamma": 0.3, "mur": 0.0},
        "B": {"gamma": 0.0, "mur": +C_WALL},
        "C": {"gamma": 0.3, "mur": -C_WALL},
        "D": {"gamma": 0.0, "mur": 0.0}}


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def V_terme(rho2, mur):
    """ρ²−1 ; + mur de pression (+C) ou plancher dissipatif (−C) sous
    ρ_min. Signe gelé : +C = pression conservative ; −C = restauration
    active sous damping."""
    if mur == 0.0:
        return rho2 - 1.0
    return rho2 - 1.0 + mur * np.maximum(0.0, RHO_MIN - np.sqrt(rho2))**2


def gp_step(psi, lin, gamma_, dt_, mur=0.0):
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    return psi


def detecte(psi):
    """Détecteur E44 (filiation) + lisibilité gelée (anom==0, amb<=4)."""
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
    lisible = (anom == 0) and (amb <= AMB_MAX)
    return {"lie": len(pairs) > 0, "nboucles": len(loops),
            "longueur_totale": int(sum(f['len'] for f in loops)),
            "npaires": len(pairs), "paires": pairs, "anom": anom,
            "amb": amb, "lisible": lisible}


def phase_nucleation(graine, N_=N, pas_max=400):
    """Phase 1 gelée — identique à E45/E46 (pas de mur, γ=0,3)."""
    rng = np.random.default_rng(graine)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N_,) * 3))
    lin = gp_linear(N_, A, 0.3, DT)
    snaps = {}
    nucle = False
    for step in range(1, pas_max + 1):
        psi = gp_step(psi, lin, 0.3, DT, mur=0.0)
        for pas, t in SNAP_NUCLE:
            if step == pas and pas <= pas_max:
                s = detecte(psi)
                snaps[t] = s
                nucle = nucle or s["lie"]
                print(f"  graine {graine} t={t:.0f} : boucles={s['nboucles']} "
                      f"liées={s['npaires']} anom={s['anom']}", flush=True)
    return snaps, psi, nucle


def branche(psi_t20, gamma_, mur_, N_=N, pas_debut=400):
    """Continuation gelée depuis t=20 pour un bras du 2×2."""
    psi = psi_t20.copy()
    lin = gp_linear(N_, A, gamma_, DT)
    snaps = {}
    for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin, gamma_, DT, mur=mur_)
        for pas, t in SNAP_SUITE:
            if step == pas:
                snaps[t] = detecte(psi)
    return snaps


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : grille réduite, graine hors
        # campagne (999997), aucune donnée de campagne produite.
        print("SMOKE — validation technique (hors campagne)")
        snaps, psi, nucle = phase_nucleation(999997, N_=16, pas_max=160)
        etats = {b: list(branche(psi, p["gamma"], p["mur"], N_=16))
                 for b, p in BRAS.items()}
        print("SMOKE OK :", {"nucle": nucle, "bras": etats})
        return

    t0 = time.time()
    res = {"campagne": "E47", "protocole": "E47-SEPARATION-1.0 (gelé)",
           "runs": {}}
    runs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for graine in SEEDS:
        print(f"graine {graine} — phase nucléation", flush=True)
        snaps, psi20, nucle = phase_nucleation(graine)
        run = {"nucleation": snaps, "nucle": nucle}
        if nucle:
            for b, p in BRAS.items():
                run[b] = branche(psi20, p["gamma"], p["mur"])
                print(f"  graine {graine} : bras {b} terminé", flush=True)
        res["runs"][str(graine)] = run
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles : e47_protocole.json) ----
    def pers(run, b):
        return any(run[b][t]["lie"] and run[b][t]["lisible"]
                   for t in (45.0, 90.0))

    def lisibilite(run, b):
        return all(run[b][t]["lisible"] for t in (45.0, 90.0))

    branches = [g for g, r in res["runs"].items() if r["nucle"]]
    ag = {"P0_filiation_440103_t12":
          res["runs"]["440103"]["nucleation"][12.0]["lie"],
          "n_runs_nucles": len(branches), "runs_nucles": branches}
    for b in BRAS:
        ag[f"persistance_{b}"] = sum(1 for g in branches
                                     if pers(res["runs"][g], b))
        ag[f"lisibilite_{b}"] = sum(1 for g in branches
                                    if lisibilite(res["runs"][g], b))
    ag["P1_Kelvin_B>A_et_B>D"] = ag["persistance_B"] > ag["persistance_A"] \
        and ag["persistance_B"] > ag["persistance_D"]
    ag["P2_plancher_C>A"] = ag["persistance_C"] > ag["persistance_A"]
    ag["P0b_temoins"] = (ag["persistance_A"] == 0 and ag["persistance_D"] == 0)
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e47_separation_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
