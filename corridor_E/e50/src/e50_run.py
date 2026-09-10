#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E50 — CONSERVATION PURE : le gel de Kelvin conserve-t-il un lien de Hopf
IMPRIMÉ ?   [protocole E50-IMPRIME-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E50. Protocole gelé dans
e50_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; suivi spatial d'E48/E49 inchangé ;
relaxation d'un lien imprimé validée par E44-T0 (Lk = +0,994 attendu
±1 — le présent P0 reprend ce contrôle).

Motivation (corridor E44–E49) : la conservation a posteriori est close
(le lien meurt en < 5 unités, par reconnexion, avant toute intervention).
E50 isole la question de la conservation PURE : un lien né protégé
(imprimé, relaxé, puis gelé immédiatement) survit-il ? L'état initial
est propre (une paire, pas d'enchevêtrement) — la lisibilité est
attendue (directionnel pré-enregistré).

Construction gelée du lien imprimé (Hopf) :
  anneau 1 : plan xy, centre (31,5 ; 31,5 ; 31,5), rayon R = 10
  anneau 2 : plan xz, centre (41,5 ; 31,5 ; 31,5), rayon r = 8
  (le centre de l'anneau 2 est sur l'anneau 1 ; r < R → enlacement
  exactement 1 ; distance inter-cœurs constante = 8 mailles > cœur)
  ψ = tanh(d1/δ)·tanh(d2/δ)·exp(i(φ1+φ2)), δ = 1,5 maille (cœur ≈ 2,
  filiation E44) ; puis relaxation : 100 pas (5 unités), γ=0,3, sans mur.
Bras depuis l'état relaxé :
  A : γ=0,3, sans mur, jusqu'à t=90 (témoin — évaporation sous tension)
  B : γ=0, mur +C=100, plancher ρ_min=0,5 (gel de Kelvin immédiat)
Snapshots : t=5 (entrée du gel), t=45, t=90. Suivi : paire détectée à
t=5 (max |Lk|), retrouvée ⟺ médiane des distances < 3 mailles,
conservée ⟺ deux retrouvées et |Lk| ≥ 0,5 — identique à E48/E49.
Campagne déterministe (condition initiale figée, pas de graine) :
test d'existence, pas de statistique — déclaré.

Usage : python3 e50_run.py            (campagne — interdit avant décision)
        python3 e50_run.py --smoke    (validation technique déclarée :
                                       N=32, lien réduit, hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E49, sauf mention) --------
N, A, DT = 64, 2.0, 0.05
GAMMA_RELAX = 0.3
PAS_RELAX = 100          # 5 unités — relaxation gelée (filiation E44-T0)
R_ANNEAU1 = 10.0         # plan xy, centre (31.5,31.5,31.5)
R_ANNEAU2 = 8.0          # plan xz, centre (41.5,31.5,31.5)
DELTA_COEUR = 1.5        # mailles
RHO_MIN = 0.5
C_WALL = 100.0
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]   # t=5 géré à part (entrée du gel)
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
DIST_TRACK = 3.0
MIN_LEN_CAND = 20
AMB_MAX = 4
P0_BORNE = (0.9, 1.1)    # |Lk| attendu après relaxation (filiation T0)


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


def lien_imprime(N_=N):
    """Construction gelée du lien de Hopf (voir docstring d'en-tête)."""
    C = (N_ - 1) / 2.0
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    s = N_ / 64.0  # homothétie déclarée (smoke : N=32)
    R1, R2, dl = R_ANNEAU1 * s, R_ANNEAU2 * s, DELTA_COEUR * s
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
    """Détecteur E44 (filiation) — identique à E48/E49."""
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
    """Identique à E48/E49 (figé)."""
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


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32 (homothétie), hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        psi = lien_imprime(32)
        lin = gp_linear(32, A, GAMMA_RELAX, DT)
        for _ in range(20):
            psi = gp_step(psi, lin, GAMMA_RELAX, DT)
        s = detecte(psi, avec_loops=True)
        print("SMOKE :", {"nboucles": s["nboucles"], "npaires": s["npaires"],
                          "paires": s["paires"], "anom": s["anom"],
                          "amb": s["amb"]})
        return

    t0 = time.time()
    res = {"campagne": "E50", "protocole": "E50-IMPRIME-1.0 (gelé)"}

    # ---- construction + relaxation (gelés) ----
    psi = lien_imprime(N)
    lin_relax = gp_linear(N, A, GAMMA_RELAX, DT)
    for step in range(1, PAS_RELAX + 1):
        psi = gp_step(psi, lin_relax, GAMMA_RELAX, DT, mur=0.0)

    # ---- snapshot d'entrée (t=5) : P0 filiation T0 + paire suivie ----
    s5 = detecte(psi, avec_loops=True)
    res["entree_relaxee"] = {k: v for k, v in s5.items()
                             if not k.startswith('_')}
    if not s5["lie"]:
        res["agregation"] = {"P0_filiation_T0": False,
                             "note": "pas de paire détectée après relaxation "
                                     "— B3-FAIL technique, harnais à réparer"}
        _ecris(res, t0)
        return
    i, j, lk0 = max(s5["_pairs_brut"], key=lambda p: abs(p[2]))
    suivies = [s5["_loops"][i]['pts'].copy(), s5["_loops"][j]['pts'].copy()]
    res["paire_suivie"] = {"lk_entree": round(lk0, 3),
                           "P0_filiation_T0": bool(
                               P0_BORNE[0] <= abs(lk0) <= P0_BORNE[1])}
    print(f"t=5 (entrée du gel) : boucles={s5['nboucles']} "
          f"paire suivie Lk={lk0:.3f} anom={s5['anom']}", flush=True)

    # ---- bras A (témoin) et B (gel de Kelvin immédiat) ----
    for bras, (gamma_, mur_) in {"A": (0.3, 0.0), "B": (0.0, +C_WALL)}.items():
        psi_b = psi.copy()
        lin = gp_linear(N, A, gamma_, DT)
        snaps = {5.0: snapshot_suivi(psi_b, suivies, N)}
        for step in range(PAS_RELAX + 1, SNAP_SUITE[-1][0] + 1):
            psi_b = gp_step(psi_b, lin, gamma_, DT, mur=mur_)
            for pas, t in SNAP_SUITE:
                if step == pas:
                    snaps[t] = snapshot_suivi(psi_b, suivies, N)
                    print(f"  bras {bras} t={t:.0f} : conservée="
                          f"{snaps[t]['paire_conservee']} boucles="
                          f"{snaps[t]['nboucles']} anom={snaps[t]['anom']} "
                          f"amb={snaps[t]['amb']}", flush=True)
        res[f"bras_{bras}"] = {str(k): v for k, v in snaps.items()}
        print(f"bras {bras} terminé", flush=True)

    # ---- agrégation gelée (règles : e50_protocole.json) ----
    def pers(b):
        return any(res[f"bras_{b}"][str(t)]["paire_conservee"]
                   for t in (45.0, 90.0))

    def lisible(b):
        return all(res[f"bras_{b}"][str(t)]["lisible"]
                   for t in ("5.0", "45.0", "90.0"))

    ag = {"P0_filiation_T0": res["paire_suivie"]["P0_filiation_T0"],
          "lk_entree": res["paire_suivie"]["lk_entree"],
          "P0b_temoin_A_zero": not pers("A"),
          "persistance_identifiee_A": pers("A"),
          "persistance_identifiee_B": pers("B"),
          "P1_B_conserve": pers("B"),
          "P2_B_lisible": lisible("B"),
          "lisibilite_A": lisible("A"),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e50_imprime_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
