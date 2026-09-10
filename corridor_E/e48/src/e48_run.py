#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E48 — RÉPARATION DU BRANCHEMENT + SUIVI DE PAIRE : le gel de Kelvin
conserve-t-il LA paire nucléée ?   [protocole E48-TRACKING-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E48. Protocole gelé dans
e48_protocole.json (haché avant tout calcul — aveugle préservé).

ERRATUM DE CONCEPTION (déclaré, 09/09/2026) : E45/E46/E47 branchaient
depuis t=20 — or les 5 runs nucléés n'ont plus de lien détecté à t=20
(la paire s'évapore avant ; cohérent avec E44). Ces campagnes ont mesuré
l'absence de ré-apparition spontanée du lien, pas la conservation. Leurs
verdicts de non-conservation sont donc déclassés en « non testé —
branchement post-évaporation » (les mesures elles-mêmes restent exactes).
E48 répare : branchement AU snapshot de nucléation t_n (le plus précoce
avec ≥1 paire), et suivi spatial de la paire d'origine.

Design gelé — deux bras depuis l'état ψ(t_n) :
  A : γ=0,3, sans mur  (témoin — évaporation attendue)
  B : γ=0, mur +C      (gel de Kelvin — E47-B a montré un enchevêtrement
                        figé mais saturé au détecteur ; ici la question
                        porte sur la paire SUIVIE, pas sur l'état global)
Suivi gelé (tracking) : la paire suivie = celle de max |Lk| à t_n
(égalité : la première par ordre d'énumération — déclaré). Une boucle
d'un snapshot de branche « retrouve » une boucle suivie si la médiane
des distances (image minimale) de ses points à la boucle suivie est
< 3 mailles (figé). Paire conservée identifiée ⟺ les deux boucles
retrouvées ET |Lk| entre elles ≥ 0,5.
Lisibilité rapportée (anom, amb par snapshot ; borne anom=0, amb≤4) ;
la persistance identifiée est mesurée quel que soit l'état global, et
l'ANOMALIE est prononcée si elle ne repose que sur des snapshots
illisibles.

Usage : python3 e48_run.py            (campagne — interdit avant décision)
        python3 e48_run.py --smoke    (validation technique déclarée :
                                       N=16, graine 999996 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E47, sauf mention) --------
N, A, DT = 64, 2.0, 0.05
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
RHO_MIN = 0.5
C_WALL = 100.0
DIST_TRACK = 3.0       # mailles, figé
MIN_LEN_CAND = 20      # longueur minimale des candidates au suivi, figé
AMB_MAX = 4
BRAS = {"A": {"gamma": 0.3, "mur": 0.0},
        "B": {"gamma": 0.0, "mur": +C_WALL}}


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def V_terme(rho2, mur):
    if mur == 0.0:
        return rho2 - 1.0
    return rho2 - 1.0 + mur * np.maximum(0.0, RHO_MIN - np.sqrt(rho2))**2


def gp_step(psi, lin, gamma_, dt_, mur=0.0):
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V_terme(np.abs(psi)**2, mur) * dt_ / 2)
    return psi


def detecte(psi, avec_loops=False):
    """Détecteur E44 (filiation) ; rend les boucles si avec_loops."""
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
            pairs.append((i, j, lk))
    s = {"lie": len(pairs) > 0, "nboucles": len(loops),
         "longueur_totale": int(sum(f['len'] for f in loops)),
         "npaires": len(pairs),
         "paires": [(i, j, round(lk, 3)) for i, j, lk in pairs],
         "anom": anom, "amb": amb,
         "lisible": (anom == 0) and (amb <= AMB_MAX)}
    if avec_loops:
        s["_loops"] = loops
        s["_pairs_brut"] = pairs
    return s


def dist_median_mi(P, Q, L):
    """Médiane des distances minimales (image minimale) des points de P
    à l'ensemble Q — mesure de suivi spatial (figée)."""
    best = np.full(len(P), np.inf)
    for c in range(0, len(Q), 512):
        R = P[:, None, :] - Q[None, c:c + 512, :]
        R = (R + L / 2) % L - L / 2
        best = np.minimum(best, np.linalg.norm(R, axis=2).min(axis=1))
    return float(np.median(best))


def suivi(loops, paires_brut, suivies, L):
    """La paire suivie est-elle conservée identifiée dans ce snapshot ?
    Retrouvée ⟺ médiane des distances < DIST_TRACK (candidates de
    longueur ≥ MIN_LEN_CAND, figé). Conservée ⟺ deux retrouvées et
    |Lk| ≥ SEUIL_LK entre elles."""
    cands = [f for f in loops if f['len'] >= MIN_LEN_CAND]
    retrouvees = []
    dists = []
    for T in suivies:
        best = None
        for f in cands:
            d = dist_median_mi(f['pts'], T, L)
            if best is None or d < best[0]:
                best = (d, f)
        dists.append(best[0] if best else None)
        retrouvees.append(best[1] if (best and best[0] < DIST_TRACK)
                          else None)
    conservee = False
    lk = None
    if all(r is not None for r in retrouvees):
        lk = gauss_link_mi(retrouvees[0]['pts'], retrouvees[1]['pts'], L)
        conservee = abs(lk) >= SEUIL_LK
    return conservee, lk, dists


def phase_nucleation(graine, N_=N, pas_max=400):
    """Phase 1 gelée — évolution identique à E45/E46/E47, MAIS états ψ
    conservés à chaque snapshot et branchement au PREMIER snapshot avec
    ≥1 paire liée (réparation déclarée)."""
    rng = np.random.default_rng(graine)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N_,) * 3))
    lin = gp_linear(N_, A, 0.3, DT)
    snaps = {}
    branchement = None  # (t_n, psi_n, paire_suivie)
    for step in range(1, pas_max + 1):
        psi = gp_step(psi, lin, 0.3, DT, mur=0.0)
        for pas, t in SNAP_NUCLE:
            if step == pas and pas <= pas_max:
                s = detecte(psi, avec_loops=True)
                snaps[t] = {k: v for k, v in s.items()
                            if not k.startswith('_')}
                print(f"  graine {graine} t={t:.0f} : boucles={s['nboucles']} "
                      f"liées={s['npaires']} anom={s['anom']}", flush=True)
                if branchement is None and s["lie"]:
                    i, j, lk = max(s["_pairs_brut"], key=lambda p: abs(p[2]))
                    suivies = [s["_loops"][i]['pts'].copy(),
                               s["_loops"][j]['pts'].copy()]
                    branchement = (t, psi.copy(), suivies, round(lk, 3))
                    print(f"  graine {graine} : PAIRE SUIVIE à t={t:.0f} "
                          f"(Lk={lk:.3f})", flush=True)
    return snaps, branchement


def branche(psi_n, t_n, suivies, gamma_, mur_, N_=N):
    """Continuation gelée depuis t_n ; suivi de la paire à t=45,90."""
    psi = psi_n.copy()
    lin = gp_linear(N_, A, gamma_, DT)
    pas_debut = int(round(t_n / DT))
    snaps = {}
    for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin, gamma_, DT, mur=mur_)
        for pas, t in SNAP_SUITE:
            if step == pas:
                s = detecte(psi, avec_loops=True)
                conservee, lk, dists = suivi(s["_loops"], s["_pairs_brut"],
                                             suivies, N_)
                snaps[t] = {k: v for k, v in s.items()
                            if not k.startswith('_')}
                snaps[t]["paire_conservee"] = conservee
                snaps[t]["lk_suivi"] = (round(lk, 3)
                                        if lk is not None else None)
                snaps[t]["dist_suivi"] = [round(d, 2) if d is not None
                                          else None for d in dists]
    return snaps


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=16, graine 999996 hors campagne.
        print("SMOKE — validation technique (hors campagne)")
        snaps, br = phase_nucleation(999996, N_=16, pas_max=160)
        if br is None:
            rng = np.random.default_rng(999996)
            psi16 = np.exp(1j * rng.uniform(0, 2 * np.pi, (16,) * 3))
            T1 = np.array([[0., 0., 0.], [8., 8., 8.]])
            T2 = np.array([[4., 4., 4.], [12., 12., 12.]])
            s = detecte(psi16, avec_loops=True)
            ok, lk, dd = suivi(s["_loops"], [], [T1, T2], 16)
            print("SMOKE OK (pas de nucléation ; suivi testé sur détecteur "
                  "vide):", {"conservee": ok, "lk": lk, "dists": dd})
        else:
            print("SMOKE OK (nucléation)")
        return

    t0 = time.time()
    res = {"campagne": "E48", "protocole": "E48-TRACKING-1.0 (gelé)",
           "runs": {}}
    runs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for graine in SEEDS:
        print(f"graine {graine} — phase nucléation", flush=True)
        snaps, br = phase_nucleation(graine)
        run = {"nucleation": snaps, "nucle": br is not None}
        if br is not None:
            t_n, psi_n, suivies, lk0 = br
            run["t_n"] = t_n
            run["lk_nucleation"] = lk0
            for b, p in BRAS.items():
                run[b] = branche(psi_n, t_n, suivies, p["gamma"], p["mur"])
                print(f"  graine {graine} : bras {b} terminé", flush=True)
        res["runs"][str(graine)] = run
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles : e48_protocole.json) ----
    def pers_ident(run, b):
        return any(run[b][t]["paire_conservee"] for t in (45.0, 90.0))

    def pers_lisible(run, b):
        return any(run[b][t]["paire_conservee"] and run[b][t]["lisible"]
                   for t in (45.0, 90.0))

    branches = [g for g, r in res["runs"].items() if r["nucle"]]
    ag = {"P0_filiation_440103_t12":
          res["runs"]["440103"]["nucleation"][12.0]["lie"],
          "n_runs_nucles": len(branches), "runs_nucles": branches,
          "t_n_par_run": {g: res["runs"][g]["t_n"] for g in branches}}
    for b in BRAS:
        ag[f"persistance_identifiee_{b}"] = sum(
            1 for g in branches if pers_ident(res["runs"][g], b))
        ag[f"persistance_lisible_{b}"] = sum(
            1 for g in branches if pers_lisible(res["runs"][g], b))
    ag["P0b_temoin_A_zero"] = ag["persistance_identifiee_A"] == 0
    ag["P1_B>A"] = (ag["persistance_identifiee_B"]
                    > ag["persistance_identifiee_A"])
    ag["P1_repose_sur_lisible"] = ag["persistance_lisible_B"] > 0
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e48_tracking_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
