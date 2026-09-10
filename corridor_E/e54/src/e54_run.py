#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E54 — LIGNES TRESSÉES SOUS ROTATION : la nucléation et la persistance du
tressage de lignes axiales   [protocole E54-TRESSAGE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E54. Protocole gelé dans
e54_protocole.json (haché avant tout calcul — aveugle préservé).

Changement d'objet (désigné par le corridor) : les boucles meurent par
contraction (E51) ; une ligne axiale dans un récipient en rotation ne
peut pas rétrécir — elle ne meurt que par reconnexion ou drainage. Le
tressage (enroulement mutuel de deux lignes) est discret (groupe de
tresses) ; sa nucléation et sa persistance sont la question.

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) pour la vorticité de plaquette ; géométrie du
récipient en rotation EXACTEMENT celle d'E44-B (cylindre r<26, z∈[2,61],
paroi fixée à e^{4iφ}, chapeaux nuls). NOUVEAU (déclaré) : le traceur de
lignes axiales et la mesure d'enroulement mutuel (tressage) — ajout de
détecteur, gelé ici, non rétro-appliqué.

Design gelé :
  6 graines 440201–440206 (= ensemble B d'E44, filiation) ; trempe GP
  amortie (mêmes paramètres : N=64, A=2, γ=0,3, dt=0,05) ; snapshots
  t=8, 12, 20, 45, 90.
  Détection : vorticité de plaquette xy par tranche z (amp_gate=0,
  masquage géométrique hors récipient, filiation E44-B) ; points de
  vortex par tranche ; lignes axiales = pistes d'appariement au plus
  proche entre tranches consécutives (saut max 2 mailles, figé) ;
  ligne longue : portée ≥ 40 tranches (figé).
  Tressage d'une paire de lignes : enroulement mutuel
  w = Σ_z wrap(Δθ(z))/2π sur la portée commune (figé : paire tressée
  ⟺ |w| ≥ 0,5 sur ≥ 40 tranches communes).

Usage : python3 e54_run.py            (campagne — interdit avant décision)
        python3 e54_run.py --smoke    (validation technique déclarée :
                                       N=32, graine 999993 hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity  # filiation (vorticité de plaquette)

# ---------------- paramètres gelés (filiation E44-B, sauf mention) ----------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(440201, 440207))   # ensemble B d'E44 — filiation
SNAP = [(160, 8.0), (240, 12.0), (400, 20.0), (900, 45.0), (1800, 90.0)]
WIND_PAROI = 4                        # circulation imposée e^{4iφ} (E44-B)
SAUT_MAX = 2.0                        # appariement inter-tranches, figé
PORTEE_MIN = 40                       # tranches, figé
SEUIL_TRESSAGE = 0.5                  # |w|, figé
COMMUN_MIN = 40                       # tranches communes, figé


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_, fix=None):
    """Filiation e44_core.gp_step (fix = paroi du récipient B)."""
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    if fix is not None:
        psi[fix[0]] = fix[1][fix[0]]
    return psi


def geometrie_B(N_=N):
    """Récipient en rotation d'E44-B, à l'identique."""
    C = (N_ - 1) / 2.0
    Xg, Yg, Zg = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                             indexing='ij')
    Rg = np.sqrt((Xg - C)**2 + (Yg - C)**2)
    z0, z1 = int(2 * N_ / 64), int(61 * N_ / 64)
    inside = (Rg < 26 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    ring = (Rg >= 26 * N_ / 64) & (Rg < 28 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    PHI = np.arctan2(Yg - C, Xg - C)
    fix_val = np.zeros((N_,) * 3, dtype=complex)
    fix_val[ring] = np.exp(1j * WIND_PAROI * PHI[ring])
    return inside, ring, fix_val


# ---------------- détecteur de tressage (NOUVEAU — déclaré, gelé) -----------
def points_par_tranche(psi, inside):
    """Points de vortex par tranche z : vorticité de plaquette xy
    (wz de e44_core.vorticity), masquée au récipient (filiation E44-B)."""
    _, _, wz = vorticity(psi, amp_gate=0.0)
    wz = np.where(inside, wz, 0)
    N_ = psi.shape[0]
    tranches = {}
    for k in range(N_):
        pts = np.array(list(zip(*np.nonzero(wz[:, :, k]))), dtype=float)
        if len(pts):
            tranches[k] = pts
    return tranches


def trace_lignes(tranches, z0, z1):
    """Pistes au plus proche entre tranches consécutives (saut max
    SAUT_MAX, figé). Rend les lignes : listes de (z, point)."""
    lignes = []
    for z in range(z0, z1):
        if z not in tranches:
            continue
        if z + 1 not in tranches:
            continue
        P, Q = tranches[z], tranches[z + 1]
        D = np.linalg.norm(P[:, None, :] - Q[None, :, :], axis=2)
        paires = []
        used = set()
        for a in range(len(P)):
            b = int(np.argmin(D[a]))
            if D[a, b] <= SAUT_MAX and b not in used:
                used.add(b)
                paires.append((a, b))
        nouv = []
        for lg in lignes:
            a0 = lg["dernier_idx"]
            if lg["dernier_z"] == z and a0 is not None:
                m = [b for a, b in paires if a == a0]
                if m:
                    lg["pts"].append((z + 1, tranches[z + 1][m[0]]))
                    lg["dernier_idx"] = m[0]
                    lg["dernier_z"] = z + 1
                    nouv.append(lg)
                    continue
            nouv.append(lg)   # ligne morte si non prolongée
        deja = {b for _, b in paires}
        for b in range(len(Q)):
            if b not in deja:
                nouv.append({"pts": [(z + 1, tranches[z + 1][b])],
                             "dernier_idx": b, "dernier_z": z + 1})
        lignes = nouv
    return [lg["pts"] for lg in lignes if len(lg["pts"]) >= 1]


def enroulement_mutuel(L1, L2):
    """w = Σ wrap(Δθ(z))/2π sur la portée commune (figé)."""
    d1 = {z: p for z, p in L1}
    d2 = {z: p for z, p in L2}
    zs = sorted(set(d1) & set(d2))
    if len(zs) < COMMUN_MIN:
        return None
    th = np.array([np.arctan2(d1[z][1] - d2[z][1], d1[z][0] - d2[z][0])
                   for z in zs])
    dth = (np.diff(th) + np.pi) % (2 * np.pi) - np.pi
    return float(np.sum(dth) / (2 * np.pi))


def analyse_tressage(psi, inside, N_):
    z0, z1 = int(2 * N_ / 64), int(61 * N_ / 64)
    tranches = points_par_tranche(psi, inside)
    lignes = trace_lignes(tranches, z0, z1)
    longues = [lg for lg in lignes
               if lg[-1][0] - lg[0][0] + 1 >= PORTEE_MIN * N_ / 64]
    paires = []
    for i in range(len(longues)):
        for j in range(i + 1, len(longues)):
            w = enroulement_mutuel(longues[i], longues[j])
            if w is not None and abs(w) >= SEUIL_TRESSAGE:
                paires.append((i, j, round(w, 3)))
    return {"n_lignes_longues": len(longues), "paires_tressees": paires,
            "tresse": len(paires) > 0}


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, graine 999993 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        inside, ring, fix_val = geometrie_B(32)
        rng = np.random.default_rng(999993)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (32,) * 3))
        psi[~inside] = 0.0
        psi[ring] = fix_val[ring]
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(80):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(ring | ~inside, fix_val))
        r = analyse_tressage(psi, inside, 32)
        print("SMOKE :", r)
        return

    t0 = time.time()
    inside, ring, fix_val = geometrie_B(N)
    fix_mask = ring | ~inside
    res = {"campagne": "E54", "protocole": "E54-TRESSAGE-1.0 (gelé)",
           "runs": {}}
    for graine in SEEDS:
        rng = np.random.default_rng(graine)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
        psi[~inside] = 0.0
        psi[ring] = fix_val[ring]
        lin = gp_linear(N, A, GAMMA, DT)
        snaps = {}
        for step in range(1, SNAP[-1][0] + 1):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
            for pas, t in SNAP:
                if step == pas:
                    r = analyse_tressage(psi, inside, N)
                    snaps[t] = r
                    print(f"  graine {graine} t={t:.0f} : lignes longues="
                          f"{r['n_lignes_longues']} tressées="
                          f"{len(r['paires_tressees'])}", flush=True)
        res["runs"][str(graine)] = {str(k): v for k, v in snaps.items()}
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e54_run_{graine}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res["runs"][str(graine)], f, ensure_ascii=False)
        print(f"graine {graine} terminée", flush=True)

    # ---- agrégation gelée (règles : e54_protocole.json) ----
    ag = {}
    ag["P0_structure_axiale"] = all(
        res["runs"][g][str(t)]["n_lignes_longues"] >= 1
        for g in res["runs"] for t in (8.0, 12.0, 20.0))
    ag["P1_tressage_nucle"] = any(
        res["runs"][g][str(t)]["tresse"]
        for g in res["runs"] for t in (8.0, 12.0, 20.0))
    ag["P2_tressage_persiste"] = any(
        res["runs"][g][str(t)]["tresse"]
        and any(res["runs"][g][str(t2)]["tresse"] for t2 in (45.0, 90.0))
        for g in res["runs"] for t in (8.0, 12.0, 20.0))
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e54_tressage_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
