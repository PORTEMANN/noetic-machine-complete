#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E59 — LA FONCTION DE FRONTIÈRE τ(A, γ) : durée de vie du lien en fonction
de la non-idéalité de la dynamique   [protocole E59-FRONTIERE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E59. Protocole gelé dans
e59_protocole.json (haché avant tout calcul — aveugle préservé).

Conversion déclarée (du catalogue des mécanismes à la fonction de
frontière) : les 17 campagnes du corridor ont mesuré un seul point —
τ < 5 unités à (A=2, γ=0,3). Point d'appui : le théorème de Kelvin
(écoulement idéal : topologie conservée exactement). La non-idéalité de
GP est la déplétion du cœur, paramétrée par la longueur de guérison
ξ ∝ √A et par γ. E59 mesure τ sur la grille figée
A ∈ {0,5 ; 1 ; 2 ; 4 ; 8} × γ ∈ {0 ; 0,3} — la frontière comme fonction,
pas comme liste (précédent de style : P32, la loi de Z-dépendance).

Filiation déclarée : construction du lien imprimé d'E50 (byte-level) ;
détecteur E44 (e44_core.py, sha256 604c2232…60ae1ac7) ; suivi spatial
d'E48→E51 (inchangé ; seuil |Lk| ≥ 0,5 inchangé — pas de re-seuilage).

Design gelé :
  Construction identique à E50 (anneaux R=10, r=8, δ=1,5 ; relaxation
  100 pas à γ=0,3, A=2, sans paroi) — l'état d'entrée est UNIQUE et mesuré
  une fois (t=5) ; chaque point de la grille part de COPIES de cet état
  et évolue avec SON (A, γ) jusqu'à t=90.
  Snapshots denses (figés) : t = 5, 10, 15, 20, 25, 30, 45, 60, 90.
  τ = dernier snapshot avec paire suivie liée (|Lk_suivi| ≥ 0,5) — figé.
  A=0,5 est au bord de résolution de la grille (ξ ≈ 0,7 maille < maille) —
  inclus et marqué (déclaré) ; les compteurs anom/amb le contrôlent.

Usage : python3 e59_run.py            (campagne — interdit avant décision)
        python3 e59_run.py --smoke    (validation technique déclarée :
                                       N=32, 2 points de grille,
                                       hors campagne)
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
N, DT = 64, 0.05
A_PREP, GAMMA_PREP = 2.0, 0.3
GRILLE_A = [0.5, 1.0, 2.0, 4.0, 8.0]     # figé ; 0,5 = bord de résolution
GRILLE_GAMMA = [0.0, 0.3]                # figé
PAS_RELAX = 100
SNAP_PAS = [100, 200, 300, 400, 500, 600, 900, 1200, 1800]
SNAP_T = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 45.0, 60.0, 90.0]
R_ANNEAU1 = 10.0
R_ANNEAU2 = 8.0
DELTA_COEUR = 1.5
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
DIST_TRACK = 3.0
MIN_LEN_CAND = 20
AMB_MAX = 4
P0_BORNE = (0.9, 1.1)


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_):
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    return psi


def lien_imprime(N_=N):
    """Identique à E50 (filiation byte-level de la construction)."""
    C = (N_ - 1) / 2.0
    s = N_ / 64.0
    R1, R2, dl = R_ANNEAU1 * s, R_ANNEAU2 * s, DELTA_COEUR * s
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    rho1 = np.sqrt((X - C)**2 + (Y - C)**2)
    u1, w1 = rho1 - R1, Z - C
    d1 = np.sqrt(u1**2 + w1**2)
    phi1 = np.arctan2(w1, u1)
    rho2 = np.sqrt((X - (C + R1))**2 + (Z - C)**2)
    u2, w2 = rho2 - R2, Y - C
    d2 = np.sqrt(u2**2 + w2**2)
    phi2 = np.arctan2(w2, u2)
    return np.tanh(d1 / dl) * np.tanh(d2 / dl) * np.exp(1j * (phi1 + phi2))


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
    s = {"lie": len(pairs) > 0, "nboucles": len(loops), "anom": anom,
         "amb": amb, "lisible": (anom == 0) and (amb <= AMB_MAX)}
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
    for T in suivies:
        best = None
        for f in cands:
            d = dist_median_mi(f['pts'], T, L)
            if best is None or d < best[0]:
                best = (d, f)
        retrouvees.append(best[1] if (best and best[0] < DIST_TRACK)
                          else None)
    conservee = False
    lk = None
    if all(r is not None for r in retrouvees):
        lk = gauss_link_mi(retrouvees[0]['pts'], retrouvees[1]['pts'], L)
        conservee = abs(lk) >= SEUIL_LK
    return conservee, lk


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, 2 points de grille,
        # hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        psi = lien_imprime(32)
        lin = gp_linear(32, A_PREP, GAMMA_PREP, DT)
        for _ in range(20):
            psi = gp_step(psi, lin, GAMMA_PREP, DT)
        s = detecte(psi, avec_loops=True)
        print("SMOKE :", {"nboucles": s["nboucles"], "npaires_raw": len(
            s.get("_pairs_brut", [])), "anom": s["anom"], "amb": s["amb"]})
        return

    t0 = time.time()
    res = {"campagne": "E59", "protocole": "E59-FRONTIERE-1.0 (gelé)",
           "grille": {"A": GRILLE_A, "gamma": GRILLE_GAMMA}, "points": {}}

    # ---- construction + relaxation uniques (identiques à E50) ----
    psi = lien_imprime(N)
    lin = gp_linear(N, A_PREP, GAMMA_PREP, DT)
    for step in range(1, PAS_RELAX + 1):
        psi = gp_step(psi, lin, GAMMA_PREP, DT)
    s5 = detecte(psi, avec_loops=True)
    res["entree"] = {k: v for k, v in s5.items() if not k.startswith('_')}
    if not s5["lie"]:
        res["agregation"] = {"P0": False, "note": "B3-FAIL technique"}
        _ecris(res, t0)
        return
    i, j, lk0 = max(s5["_pairs_brut"], key=lambda p: abs(p[2]))
    suivies = [s5["_loops"][i]['pts'].copy(), s5["_loops"][j]['pts'].copy()]
    res["paire_suivie"] = {"lk_entree": round(lk0, 3),
                           "P0": bool(P0_BORNE[0] <= abs(lk0)
                                      <= P0_BORNE[1])}
    print(f"entrée t=5 : Lk={lk0:.3f} anom={s5['anom']}", flush=True)

    # ---- grille ----
    for A_ in GRILLE_A:
        for gamma_ in GRILLE_GAMMA:
            psi_g = psi.copy()
            lin_g = gp_linear(N, A_, gamma_, DT)
            etats = {}
            # mesure de l'entrée (t=5, pas 100) AVANT l'évolution —
            # réparation du 09/09/2026 (KeyError au premier point) ;
            # l'état d'entrée est identique pour tous les points (copie)
            s = detecte(psi_g, avec_loops=True)
            conservee, lk = suivi(s["_loops"], suivies, N)
            etats[5.0] = {"conservee": conservee,
                          "lk_suivi": round(lk, 3) if lk is not None
                          else None,
                          "nboucles": s["nboucles"],
                          "anom": s["anom"], "amb": s["amb"],
                          "lisible": s["lisible"]}
            for step in range(PAS_RELAX + 1, SNAP_PAS[-1] + 1):
                psi_g = gp_step(psi_g, lin_g, gamma_, DT)
                if step in SNAP_PAS:
                    t = SNAP_T[SNAP_PAS.index(step)]
                    s = detecte(psi_g, avec_loops=True)
                    conservee, lk = suivi(s["_loops"], suivies, N)
                    etats[t] = {"conservee": conservee,
                                "lk_suivi": round(lk, 3) if lk is not None
                                else None,
                                "nboucles": s["nboucles"],
                                "anom": s["anom"], "amb": s["amb"],
                                "lisible": s["lisible"]}
            # τ gelé : dernier snapshot lié
            ts_lies = [t for t in SNAP_T if etats[t]["conservee"]]
            tau = max(ts_lies) if ts_lies else SNAP_T[0]
            res["points"][f"A{A_}_g{gamma_}"] = {
                "etats": {str(t): v for t, v in etats.items()},
                "tau": tau}
            print(f"A={A_} γ={gamma_} : τ={tau}", flush=True)
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "data",
                               f"e59_A{A_}_g{gamma_}.json")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res["points"][f"A{A_}_g{gamma_}"], f,
                          ensure_ascii=False)

    # ---- agrégation gelée (règles : e59_protocole.json) ----
    taus = {A_: {g_: res["points"][f"A{A_}_g{g_}"]["tau"]
                 for g_ in GRILLE_GAMMA} for A_ in GRILLE_A}
    monotone_A = all(taus[GRILLE_A[i]][g] >= taus[GRILLE_A[i + 1]][g]
                     for i in range(len(GRILLE_A) - 1)
                     for g in GRILLE_GAMMA)
    monotone_g = all(taus[A_][0.0] >= taus[A_][0.3] for A_ in GRILLE_A)
    ag = {"P0": res["paire_suivie"]["P0"],
          "lk_entree": res["paire_suivie"]["lk_entree"],
          "tau_par_point": {f"A{A_}_g{g_}": taus[A_][g_]
                            for A_ in GRILLE_A for g_ in GRILLE_GAMMA},
          "P1_tau_non_croissant_en_A": monotone_A,
          "P1_tau_non_decroissant_sans_gamma": monotone_g,
          "P2_tau_atteint_90_au_bord": taus[GRILLE_A[0]][0.0] >= 90.0,
          "tau_max": max(taus[A_][g] for A_ in GRILLE_A
                         for g in GRILLE_GAMMA),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e59_frontiere_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
