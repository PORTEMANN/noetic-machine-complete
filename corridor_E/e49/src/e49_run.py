#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E49 — NETTOYAGE PUIS GEL : conservation lisible de la paire nuclée
[protocole E49-NETTOIE-GELE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E49. Protocole gelé dans
e49_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; harnais E48 (branchement à la nucléation,
suivi spatial de la paire, écriture incrémentale) repris.

Verdict E48 (B3-FAIL propre, 09/09/2026) : branché à la nucléation, le
gel de Kelvin fige la configuration spatiale (boucles suivies
retrouvées en place à 1,0–3,1 mailles, stables t=45→t=90) mais le lien
lu est nul (Lk_suivi = 0) sous saturation du détecteur (amb ~2×10⁴).
Deux causes déclarées non tranchées : (i) le lien meurt entre la
nucléation et l'immobilisation effective ; (ii) la lecture est corrompue
par la densité de l'enchevêtrement figé. E49 les distingue par un
calendrier à trois temps : nucléation libre → NETTOYAGE amorti court
(déclaré : 5 unités, γ=0,3, sans mur — draine l'enchevêtrement, mesuré
en E44/E45) → GEL (γ=0, mur +C). Snapshot de suivi à l'ENTRÉE du gel :
si le lien est déjà mort à t_n+5, cause (i) ; s'il est vivant à l'entrée
et mort après, le gel échoue ; s'il survit lisiblement, SUCCÈS.

Design gelé — deux bras depuis l'état ψ(t_n) :
  A  : γ=0,3, sans mur, jusqu'à t=90 (témoin — reproduit E48-A)
  B2 : nettoyage γ=0,3 sans mur de t_n à t_n+5 (100 pas, figé), avec
       snapshot de suivi à t_n+5 (entrée du gel), puis gel γ=0 + mur +C
       jusqu'à t=90 ; snapshots t=45 et t=90.

Usage : python3 e49_run.py            (campagne — interdit avant décision)
        python3 e49_run.py --smoke    (validation technique déclarée :
                                       N=16, graine 999995 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E48, sauf mention) --------
N, A, DT = 64, 2.0, 0.05
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
RHO_MIN = 0.5
C_WALL = 100.0
DIST_TRACK = 3.0
MIN_LEN_CAND = 20
AMB_MAX = 4
PAS_NETTOYAGE = 100      # 5 unités de temps — figé


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
    return s


def dist_median_mi(P, Q, L):
    """Médiane des distances minimales (image minimale) — figée (E48)."""
    best = np.full(len(P), np.inf)
    for c in range(0, len(Q), 512):
        R = P[:, None, :] - Q[None, c:c + 512, :]
        R = (R + L / 2) % L - L / 2
        best = np.minimum(best, np.linalg.norm(R, axis=2).min(axis=1))
    return float(np.median(best))


def suivi(loops, suivies, L):
    """E48 inchangé : retrouvée ⟺ médiane < DIST_TRACK (candidates de
    longueur ≥ MIN_LEN_CAND) ; conservée ⟺ deux retrouvées et
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
    """Phase 1 gelée — identique à E48 (états conservés, branchement au
    premier snapshot nucléant)."""
    rng = np.random.default_rng(graine)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N_,) * 3))
    lin = gp_linear(N_, A, 0.3, DT)
    snaps = {}
    branchement = None
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
                    pairs = [(i, j, lk) for i, j, lk in
                             ((p[0], p[1], p[2]) for p in s["paires"])]
                    i, j, lk = max(pairs, key=lambda p: abs(p[2]))
                    suivies = [s["_loops"][i]['pts'].copy(),
                               s["_loops"][j]['pts'].copy()]
                    branchement = (t, psi.copy(), suivies, lk)
                    print(f"  graine {graine} : PAIRE SUIVIE à t={t:.0f} "
                          f"(Lk={lk:.3f})", flush=True)
    return snaps, branchement


def snapshot_suivi(psi, suivies, N_=N):
    s = detecte(psi, avec_loops=True)
    conservee, lk, dists = suivi(s["_loops"], suivies, N_)
    out = {k: v for k, v in s.items() if not k.startswith('_')}
    out["paire_conservee"] = conservee
    out["lk_suivi"] = round(lk, 3) if lk is not None else None
    out["dist_suivi"] = [round(d, 2) if d is not None else None
                         for d in dists]
    return out


def branche_B2(psi_n, t_n, suivies, N_=N):
    """Nettoyage (γ=0,3, sans mur, 100 pas) → snapshot entrée du gel →
    gel (γ=0, mur +C) jusqu'à t=90, snapshots t=45, 90."""
    psi = psi_n.copy()
    pas_debut = int(round(t_n / DT))
    lin_damp = gp_linear(N_, A, 0.3, DT)
    for step in range(pas_debut + 1, pas_debut + PAS_NETTOYAGE + 1):
        psi = gp_step(psi, lin_damp, 0.3, DT, mur=0.0)
    snaps = {}
    snaps[t_n + 5.0] = snapshot_suivi(psi, suivies, N_)  # entrée du gel
    lin_gel = gp_linear(N_, A, 0.0, DT)
    for step in range(pas_debut + PAS_NETTOYAGE + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin_gel, 0.0, DT, mur=+C_WALL)
        for pas, t in SNAP_SUITE:
            if step == pas:
                snaps[t] = snapshot_suivi(psi, suivies, N_)
    return snaps


def branche_A(psi_n, t_n, suivies, N_=N):
    """Témoin : γ=0,3 sans mur jusqu'à t=90 (reproduit E48-A)."""
    psi = psi_n.copy()
    pas_debut = int(round(t_n / DT))
    lin = gp_linear(N_, A, 0.3, DT)
    snaps = {}
    for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
        psi = gp_step(psi, lin, 0.3, DT, mur=0.0)
        for pas, t in SNAP_SUITE:
            if step == pas:
                snaps[t] = snapshot_suivi(psi, suivies, N_)
    return snaps


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=16, graine 999995 hors campagne.
        print("SMOKE — validation technique (hors campagne)")
        snaps, br = phase_nucleation(999995, N_=16, pas_max=160)
        if br is None:
            rng = np.random.default_rng(999995)
            psi16 = np.exp(1j * rng.uniform(0, 2 * np.pi, (16,) * 3))
            T = [np.array([[0., 0., 0.], [8., 8., 8.]]),
                 np.array([[4., 4., 4.], [12., 12., 12.]])]
            s1 = branche_A(psi16, 8.0, T, N_=16)
            s2 = branche_B2(psi16, 8.0, T, N_=16)
            print("SMOKE OK :", {"A": list(s1), "B2": list(s2)})
        else:
            print("SMOKE OK (nucléation inattendue à N=16)")
        return

    t0 = time.time()
    res = {"campagne": "E49", "protocole": "E49-NETTOIE-GELE-1.0 (gelé)",
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
            run["lk_nucleation"] = round(lk0, 3)
            run["A"] = branche_A(psi_n, t_n, suivies)
            print(f"  graine {graine} : bras A terminé", flush=True)
            run["B2"] = branche_B2(psi_n, t_n, suivies)
            print(f"  graine {graine} : bras B2 terminé", flush=True)
        res["runs"][str(graine)] = run
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles : e49_protocole.json) ----
    def pers_ident(run, b):
        return any(run[b][t]["paire_conservee"] for t in (45.0, 90.0))

    def lisible(run, b):
        return all(run[b][t]["lisible"] for t in (45.0, 90.0))

    branches = [g for g, r in res["runs"].items() if r["nucle"]]
    ag = {"P0_filiation_440103_t12":
          res["runs"]["440103"]["nucleation"][12.0]["lie"],
          "n_runs_nucles": len(branches), "runs_nucles": branches,
          "t_n_par_run": {g: res["runs"][g]["t_n"] for g in branches}}
    ag["persistance_identifiee_A"] = sum(
        1 for g in branches if pers_ident(res["runs"][g], "A"))
    ag["persistance_identifiee_B2"] = sum(
        1 for g in branches if pers_ident(res["runs"][g], "B2"))
    ag["lisibilite_B2"] = sum(
        1 for g in branches if lisible(res["runs"][g], "B2"))
    ag["lien_vivant_entree_gel"] = sum(
        1 for g in branches
        if res["runs"][g]["B2"][res["runs"][g]["t_n"] + 5.0][
            "paire_conservee"])
    ag["P0b_temoin_A_zero"] = ag["persistance_identifiee_A"] == 0
    ag["P1_B2>A"] = (ag["persistance_identifiee_B2"]
                     > ag["persistance_identifiee_A"])
    ag["P2_B2_lisible"] = ag["lisibilite_B2"] == len(branches)
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e49_nettoie_gele_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
