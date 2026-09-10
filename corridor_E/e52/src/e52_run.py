#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E52 — PINNING NON APPARIÉ SOUS TREMPE : un paysage de puits fixe crée-t-il
des régions où l'enlacement naît ET persiste ?   [protocole E52-PAYSAGE-1.0
gelé]
=====================================================================
Harnais officiel de la campagne E52. Protocole gelé dans
e52_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; trempe libre d'E44/E45 (mêmes graines, mêmes
paramètres) ; branchement à la nucléation et suivi spatial d'E48/E49
(repris) ; témoin de taux SANS puits = la campagne E45 (5/24 runs
nucléés — publiée en staging local, filiation déclarée, pas de recalcul).

Classe de mécanisme : ancrage spatial (E37) — version non appariée :
le réseau de puits est fixe, régulier, indépendant des configurations
qui naîtront (rien n'est ajusté ; déclaré).

Design gelé :
  Réseau : puits gaussiens V_ext = −U0 Σ_w exp(−|x−w|²/2σ²), U0=2,
  σ=1,5 (figés, identiques à E51), sur grille cubique de pas ℓ=8,
  décalée de 4 mailles (w = (8i+4, 8j+4, 8k+4), figé), présent DÈS t=0
  (la naissance se fait dans le paysage — déclaré : la filiation aux
  runs E44 est donc volontairement rompue ; le taux témoin sans puits
  est celui d'E45 : 5/24).
  Phase 1 : 24 graines (440101–440124, identiques), trempe libre avec
  puits, snapshots t=8,12,16,20 ; branchement au premier snapshot
  nucléant t_n (réparation E48 reprise) ; continuation avec les MÊMES
  puits (γ=0,3) jusqu'à t=90 ; snapshots t=45, t=90.
  Split observationnel gelé : une paire nuclée est « proche-puits » si la
  médiane des distances (image minimale) de chacune de ses boucles au
  puits le plus proche est < 4 mailles (figé) — mesurée à t_n ;
  sinon « loin-puits ».

Usage : python3 e52_run.py            (campagne — interdit avant décision)
        python3 e52_run.py --smoke    (validation technique déclarée :
                                       N=16, graine 999994 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E51, sauf mention) --------
N, A, DT = 64, 2.0, 0.05
GAMMA = 0.3
SEEDS = list(range(440101, 440107)) + list(range(440107, 440125))  # 24
SNAP_NUCLE = [(160, 8.0), (240, 12.0), (320, 16.0), (400, 20.0)]
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
U0_PIN = 2.0
SIGMA_PIN = 1.5
PAS_GRILLE = 8          # ℓ, figé
DECALAGE = 4            # origine de la grille, figé
DIST_PUITS = 4.0        # borne proche-puits, figée
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
DIST_TRACK = 3.0
MIN_LEN_CAND = 20
AMB_MAX = 4


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def grille_puits(N_=N):
    """Grille cubique gelée : w = (ℓi+d, ℓj+d, ℓk+d) dans la boîte."""
    coords = []
    pas = max(1, int(round(PAS_GRILLE * N_ / 64)))
    d = int(round(DECALAGE * N_ / 64))
    for i in range((N_ - d) // pas + 1):
        for j in range((N_ - d) // pas + 1):
            for k in range((N_ - d) // pas + 1):
                coords.append((d + pas * i, d + pas * j, d + pas * k))
    return np.array(coords, dtype=float)


def V_ext_grille(N_=N):
    puits = grille_puits(N_)
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    V = np.zeros((N_,) * 3)
    sig = SIGMA_PIN * N_ / 64.0
    for w in puits:
        V -= U0_PIN * np.exp(-((X - w[0])**2 + (Y - w[1])**2
                               + (Z - w[2])**2) / (2 * sig**2))
    return V, puits


def gp_step(psi, lin, gamma_, dt_, Vext=None):
    V = np.abs(psi)**2 - 1.0
    if Vext is not None:
        V = V + Vext
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    return psi


def detecte(psi, avec_loops=False):
    """Détecteur E44 (filiation) — identique à E48→E51."""
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
    best = np.full(len(P), np.inf)
    for c in range(0, len(Q), 512):
        R = P[:, None, :] - Q[None, c:c + 512, :]
        R = (R + L / 2) % L - L / 2
        best = np.minimum(best, np.linalg.norm(R, axis=2).min(axis=1))
    return float(np.median(best))


def suivi(loops, suivies, L):
    """Identique à E48→E51 (figé)."""
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


def snapshot_suivi(psi, suivies, N_=N):
    s = detecte(psi, avec_loops=True)
    conservee, lk, dists = suivi(s["_loops"], suivies, N_)
    out = {k: v for k, v in s.items() if not k.startswith('_')}
    out["paire_conservee"] = conservee
    out["lk_suivi"] = round(lk, 3) if lk is not None else None
    out["dist_suivi"] = [round(d, 2) if d is not None else None
                         for d in dists]
    return out


def dist_puits(pts, puits, L):
    """Médiane des distances des points de la boucle au puits le plus
    proche (image minimale) — split observationnel gelé."""
    return dist_median_mi(pts, puits, L)


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=16, graine 999994 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=16)")
        V, puits = V_ext_grille(16)
        rng = np.random.default_rng(999994)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (16,) * 3))
        lin = gp_linear(16, A, GAMMA, DT)
        for _ in range(80):
            psi = gp_step(psi, lin, GAMMA, DT, Vext=V)
        s = detecte(psi, avec_loops=True)
        print("SMOKE :", {"n_puits": len(puits), "nboucles": s["nboucles"],
                          "npaires": s["npaires"], "anom": s["anom"],
                          "amb": s["amb"]})
        return

    t0 = time.time()
    V, puits = V_ext_grille(N)
    res = {"campagne": "E52", "protocole": "E52-PAYSAGE-1.0 (gelé)",
           "n_puits": len(puits), "runs": {}}
    runs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for graine in SEEDS:
        print(f"graine {graine} — phase nucléation (avec puits)", flush=True)
        rng = np.random.default_rng(graine)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
        lin = gp_linear(N, A, GAMMA, DT)
        snaps = {}
        branchement = None
        for step in range(1, SNAP_NUCLE[-1][0] + 1):
            psi = gp_step(psi, lin, GAMMA, DT, Vext=V)
            for pas, t in SNAP_NUCLE:
                if step == pas:
                    s = detecte(psi, avec_loops=True)
                    snaps[t] = {k: v for k, v in s.items()
                                if not k.startswith('_')}
                    print(f"  graine {graine} t={t:.0f} : boucles="
                          f"{s['nboucles']} liées={s['npaires']} "
                          f"anom={s['anom']}", flush=True)
                    if branchement is None and s["lie"]:
                        i, j, lk = max(s["_pairs_brut"],
                                       key=lambda p: abs(p[2]))
                        suivies = [s["_loops"][i]['pts'].copy(),
                                   s["_loops"][j]['pts'].copy()]
                        dpuits = [dist_puits(suivies[0], puits, N),
                                  dist_puits(suivies[1], puits, N)]
                        proche = all(d < DIST_PUITS for d in dpuits)
                        branchement = (t, psi.copy(), suivies, lk,
                                       dpuits, proche)
                        print(f"  graine {graine} : PAIRE SUIVIE à "
                              f"t={t:.0f} (Lk={lk:.3f}, dist_puits="
                              f"{[round(d, 2) for d in dpuits]}, "
                              f"proche={proche})", flush=True)
        run = {"nucleation": {str(k): v for k, v in snaps.items()},
               "nucle": branchement is not None}
        if branchement is not None:
            t_n, psi_n, suivies, lk, dpuits, proche = branchement
            run["t_n"] = t_n
            run["lk_nucleation"] = round(lk, 3)
            run["dist_puits"] = [round(d, 2) for d in dpuits]
            run["proche_puits"] = proche
            # continuation : mêmes puits, γ=0,3, jusqu'à t=90
            psi_b = psi_n.copy()
            pas_debut = int(round(t_n / DT))
            snaps_b = {}
            for step in range(pas_debut + 1, SNAP_SUITE[-1][0] + 1):
                psi_b = gp_step(psi_b, lin, GAMMA, DT, Vext=V)
                for pas, t in SNAP_SUITE:
                    if step == pas:
                        snaps_b[t] = snapshot_suivi(psi_b, suivies, N)
            run["suite"] = {str(k): v for k, v in snaps_b.items()}
            print(f"  graine {graine} : suite terminée", flush=True)
        res["runs"][str(graine)] = run
        with open(os.path.join(runs_dir, f"run_{graine}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({str(k): v for k, v in run.items()}, f,
                      ensure_ascii=False, default=str)

    # ---- agrégation gelée (règles : e52_protocole.json) ----
    branches = [g for g, r in res["runs"].items() if r["nucle"]]
    proches = [g for g in branches if res["runs"][g]["proche_puits"]]
    loins = [g for g in branches if not res["runs"][g]["proche_puits"]]

    def pers(g):
        return any(res["runs"][g]["suite"][str(t)]["paire_conservee"]
                   for t in (45.0, 90.0))

    ag = {"n_runs_nucles": len(branches),
          "runs_nucles": branches,
          "taux_nucleation_avec_puits": f"{len(branches)}/24",
          "taux_temoin_sans_puits_E45": "5/24",
          "n_proche_puits": len(proches), "n_loin_puits": len(loins),
          "persistance_proche": sum(1 for g in proches if pers(g)),
          "persistance_loin": sum(1 for g in loins if pers(g)),
          "P1_proche>loin": (len(proches) > 0 and len(loins) >= 0
                             and (sum(1 for g in proches if pers(g))
                                  / max(1, len(proches)))
                             > (sum(1 for g in loins if pers(g))
                                / max(1, len(loins)))),
          "lisibilite_toutes_suites": all(
              res["runs"][g]["suite"][str(t)]["lisible"]
              for g in branches for t in (45.0, 90.0)),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e52_paysage_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
