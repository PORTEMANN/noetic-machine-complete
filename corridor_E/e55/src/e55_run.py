#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E55 — NAISSANCE PROTÉGÉE : trempe confinée dans deux canaux toriques
enlacés — le lien naît-il, et persiste-t-il ?   [protocole
E55-NAISSANCE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E55. Protocole gelé dans
e55_protocole.json (haché avant tout calcul — aveugle préservé).

Changement d'ère (désigné par le corridor) : la conservation a
posteriori est close (E45–E53) ; la nucléation connue exige l'ère des
reconnexions (E44) — tension mesurée. E55 fait naître DANS la structure
protectrice : deux canaux toriques enlacés (géométrie de Hopf d'E50),
champ initial = phase aléatoire confinée aux tubes, canaux présents dès
t=0. La question : le confinement guide-t-il la formation de boucles
le long des tubes — et donc un lien, protégé dès la naissance ?

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; géométrie des canaux d'E53 (identique,
filiation) ; suivi spatial d'E48→E51 (inchangé).

Design gelé :
  Canaux : V = −U_g·exp(−d1²/2σ²) − U_g·exp(−d2²/2σ²), U_g=2, σ=1,5
  (figés, filiation E53) — anneau 1 (plan xy, centre (31,5;31,5;31,5),
  R=10), anneau 2 (plan xz, centre (41,5;31,5;31,5), r=8).
  Condition initiale : ψ = exp(iφ aléatoire) À L'INTÉRIEUR des tubes
  (d1 < 3 ou d2 < 3, figé), 0 à l'extérieur ; 6 graines 555001–555006
  (déclarées, hors séries E44).
  Bras A (témoin) : même phase aléatoire, boîte libre SANS canaux.
  Évolution : γ=0,3, avec canaux (B) ou sans (A), jusqu'à t=90 ;
  snapshots t=8, 12, 20, 45, 90.
  Mesures : boucles, paires liées (détecteur filiatif) ; attribution
  d'une boucle à un tube : médiane des distances au cercle du tube
  < 3 mailles (figé) ; lien de tubes : paire dont les deux boucles
  sont attribuées à des tubes différents.

Usage : python3 e55_run.py            (campagne — interdit avant décision)
        python3 e55_run.py --smoke    (validation technique déclarée :
                                       N=32, graine 999992 hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E53, sauf mention) --------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(555001, 555007))   # 6 graines déclarées (hors E44)
SNAP = [(160, 8.0), (240, 12.0), (400, 20.0), (900, 45.0), (1800, 90.0)]
R_ANNEAU1 = 10.0
R_ANNEAU2 = 8.0
U_GUIDE = 2.0
SIGMA_GUIDE = 1.5
EPAISSEUR_TUBE = 3.0     # condition initiale confinée, figée
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
DIST_TUBE = 3.0          # attribution d'une boucle à un tube, figé
AMB_MAX = 4


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_, Vext=None):
    V = np.abs(psi)**2 - 1.0
    if Vext is not None:
        V = V + Vext
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    return psi


def geometrie(N_=N):
    """Distances aux cercles des deux anneaux (filiation E53) + masque
    des tubes + potentiel des canaux."""
    C = (N_ - 1) / 2.0
    s = N_ / 64.0
    R1, R2 = R_ANNEAU1 * s, R_ANNEAU2 * s
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    rho1 = np.sqrt((X - C)**2 + (Y - C)**2)
    d1 = np.sqrt((rho1 - R1)**2 + (Z - C)**2)
    rho2 = np.sqrt((X - (C + R1))**2 + (Z - C)**2)
    d2 = np.sqrt((rho2 - R2)**2 + (Y - C)**2)
    sig = SIGMA_GUIDE * s
    V = -U_GUIDE * (np.exp(-d1**2 / (2 * sig**2))
                    + np.exp(-d2**2 / (2 * sig**2)))
    tube1 = d1 < EPAISSEUR_TUBE * s
    tube2 = d2 < EPAISSEUR_TUBE * s
    return V, tube1, tube2, (d1, d2)


def detecte(psi):
    """Détecteur E44 (filiation) — boucles et paires liées."""
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
    return loops, pairs, anom, amb


def dist_median_mi(P, Q, L):
    best = np.full(len(P), np.inf)
    for c in range(0, len(Q), 512):
        R = P[:, None, :] - Q[None, c:c + 512, :]
        R = (R + L / 2) % L - L / 2
        best = np.minimum(best, np.linalg.norm(R, axis=2).min(axis=1))
    return float(np.median(best))


def attribution(loops, cercles, N_):
    """Boucle attribuée à un tube si la médiane des distances de ses
    points au cercle du tube < DIST_TUBE (figé). Rend les indices par
    tube (0, 1) ou -1."""
    attrib = []
    for f in loops:
        d0 = dist_median_mi(f['pts'], cercles[0], N_)
        d1 = dist_median_mi(f['pts'], cercles[1], N_)
        attrib.append(0 if d0 < DIST_TUBE and d0 <= d1 else
                      (1 if d1 < DIST_TUBE else -1))
    return attrib


def cercle_points(N_):
    """Points de référence des cercles des anneaux (pour l'attribution)."""
    C = (N_ - 1) / 2.0
    s = N_ / 64.0
    R1, R2 = R_ANNEAU1 * s, R_ANNEAU2 * s
    th = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    c1 = np.stack([C + R1 * np.cos(th), C + R1 * np.sin(th),
                   np.full(64, C)], axis=1)
    c2 = np.stack([C + R1 + R2 * np.cos(th), np.full(64, C),
                   C + R2 * np.sin(th)], axis=1)
    return [c1, c2]


def analyse(psi, bras, cercles, N_):
    loops, pairs, anom, amb = detecte(psi)
    attrib = attribution(loops, cercles, N_)
    liens_tubes = []
    for i, j, lk in pairs:
        if attrib[i] >= 0 and attrib[j] >= 0 and attrib[i] != attrib[j]:
            liens_tubes.append((i, j, lk))
    return {"nboucles": len(loops), "npaires": len(pairs),
            "paires": pairs, "attribution": attrib,
            "lien_de_tubes": len(liens_tubes) > 0,
            "liens_tubes": liens_tubes, "anom": anom, "amb": amb,
            "lisible": (anom == 0) and (amb <= AMB_MAX)}


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, graine 999992 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        V, t1, t2, _ = geometrie(32)
        rng = np.random.default_rng(999992)
        psi = np.zeros((32,) * 3, dtype=complex)
        psi[t1 | t2] = np.exp(1j * rng.uniform(0, 2 * np.pi,
                                               int((t1 | t2).sum())))
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(60):
            psi = gp_step(psi, lin, GAMMA, DT, Vext=V)
        r = analyse(psi, "B", cercle_points(32), 32)
        print("SMOKE :", {k: v for k, v in r.items() if k != 'paires'})
        return

    t0 = time.time()
    V, tube1, tube2, _ = geometrie(N)
    cercles = cercle_points(N)
    res = {"campagne": "E55", "protocole": "E55-NAISSANCE-1.0 (gelé)",
           "runs": {}}
    for graine in SEEDS:
        for bras in ("A", "B"):
            rng = np.random.default_rng(graine)
            psi = np.zeros((N,) * 3, dtype=complex)
            if bras == "B":
                mask = tube1 | tube2
            else:
                mask = np.ones((N,) * 3, dtype=bool)   # témoin libre
            psi[mask] = np.exp(1j * rng.uniform(0, 2 * np.pi,
                                                int(mask.sum())))
            lin = gp_linear(N, A, GAMMA, DT)
            Vext = V if bras == "B" else None
            snaps = {}
            for step in range(1, SNAP[-1][0] + 1):
                psi = gp_step(psi, lin, GAMMA, DT, Vext=Vext)
                for pas, t in SNAP:
                    if step == pas:
                        r = analyse(psi, bras, cercles, N)
                        snaps[t] = r
                        print(f"  graine {graine} bras {bras} t={t:.0f} : "
                              f"boucles={r['nboucles']} liées="
                              f"{r['npaires']} tubes={r['lien_de_tubes']} "
                              f"anom={r['anom']}", flush=True)
            res["runs"][f"{graine}_{bras}"] = {str(k): v for k, v
                                               in snaps.items()}
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "data", f"e55_run_{graine}_{bras}.json")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res["runs"][f"{graine}_{bras}"], f,
                          ensure_ascii=False)
            print(f"graine {graine} bras {bras} terminé", flush=True)

    # ---- agrégation gelée (règles : e55_protocole.json) ----
    runs = res["runs"]
    ag = {}
    ag["P0_temoin_A"] = not any(
        runs[f"{g}_A"][str(t)]["lien_de_tubes"] for g in SEEDS
        for t in (8.0, 12.0, 20.0, 45.0, 90.0))
    ag["P1_lien_né_dans_B"] = any(
        runs[f"{g}_B"][str(t)]["lien_de_tubes"] for g in SEEDS
        for t in (8.0, 12.0, 20.0))
    ag["P2_lien_persiste_B"] = any(
        runs[f"{g}_B"][str(t)]["lien_de_tubes"]
        and any(runs[f"{g}_B"][str(t2)]["lien_de_tubes"]
                for t2 in (45.0, 90.0))
        for g in SEEDS for t in (8.0, 12.0, 20.0))
    ag["lisibilite_B"] = all(
        runs[f"{g}_B"][str(t)]["lisible"] for g in SEEDS
        for t in (8.0, 12.0, 20.0, 45.0, 90.0))
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e55_naissance_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
