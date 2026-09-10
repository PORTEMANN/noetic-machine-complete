#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E54-A — LIGNES TRESSÉES SOUS ROTATION, harnais recalibré
[amendement E54-A gelé : b495267e…964c1189 — haché avant tout calcul]
=====================================================================
Réparation déclarée (verdict v1 : B3-FAIL-TECHNIQUE) : le traceur de
lignes maison n'a pas reproduit l'observable publiée d'E44-B. Le harnais
recalibré utilise le détecteur E44 LUI-MÊME (trace_filaments de
e44_core.py — filiation byte-level, sha256 604c2232…60ae1ac7) :
filaments ouverts, filtre axial (longueur ≥ 40 segments ET étendue z
≥ 30 mailles, figé), enroulement axial (formule d'E44), enroulement
mutuel par tranche z entière (étendue commune ≥ 30 mailles, figé).

P0 recalibré (gelé dans e54a_amendement.json) : à t=45 et t=90, ≥ 1
filament axial dans ≥ 4/6 graines ET médiane de l'enroulement axial du
plus long filament par (graine, snapshot) dans [9, 19] (fenêtre publiée
d'E44-B). Sinon : B3-FAIL-TECHNIQUE, deuxième série.

Tout le reste : INCHANGÉ (géométrie E44-B, graines 440201–440206,
paramètres GP, snapshots, P1/P2/P3 de v1, seuil de tressage |w| ≥ 0,5).

Usage : python3 e54a_run.py            (campagne — interdit avant décision)
        python3 e54a_run.py --smoke    (validation technique déclarée :
                                        N=32, graine 999993 hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Filiation byte-level : le détecteur E44 complet (trace_filaments inclus)
from e44_core import vorticity, trace_filaments  # noqa: F401

# ---------------- paramètres gelés (inchangés sauf mention — amendement) ----
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(440201, 440207))
SNAP = [(160, 8.0), (240, 12.0), (400, 20.0), (900, 45.0), (1800, 90.0)]
WIND_PAROI = 4
LONG_MIN = 40          # segments — observable publiée d'E44-B
ETENDUE_Z_MIN = 30.0   # mailles — filtre axial, figé (amendement)
COMMUN_MIN = 30.0      # mailles communes pour l'enroulement mutuel, figé
SEUIL_TRESSAGE = 0.5
P0_FENETRE = (9.0, 19.0)   # fenêtre publiée d'E44-B (médiane 14)
P0_MIN_GRAINES = 4


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_, fix=None):
    """Filiation e44_core.gp_step."""
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    if fix is not None:
        psi[fix[0]] = fix[1][fix[0]]
    return psi


def geometrie_B(N_=N):
    """Récipient en rotation d'E44-B, à l'identique (inchangé)."""
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
    return inside, ring, fix_val, C


def mask_hors_recipient(wx, wy, wz, inside):
    """Masquage géométrique : plaquettes dont un coin est hors récipient
    → 0 (filiation E44-B, version tranche)."""
    keep = inside
    wx = np.where(keep, wx, 0)
    wy = np.where(keep, wy, 0)
    wz = np.where(keep, wz, 0)
    return wx, wy, wz


def axial_winding(P, C):
    """Formule d'E44 (e44_run.py), inchangée."""
    dx = P[:, 0] - C
    dy = P[:, 1] - C
    ph = np.arctan2(dy, dx)
    ph2 = np.roll(ph, -1)
    return float(np.sum((ph2 - ph + np.pi) % (2 * np.pi) - np.pi)
                 / (2 * np.pi))


def par_tranche_z(pts):
    """Position moyenne du filament par tranche z entière (figé)."""
    out = {}
    zs = np.floor(pts[:, 2]).astype(int)
    for z in sorted(set(zs)):
        sel = pts[zs == z]
        out[int(z)] = sel[:, :2].mean(axis=0)
    return out


def enroulement_mutuel(f1, f2):
    """w = Σ wrap(Δθ(z))/2π sur l'étendue z commune ≥ COMMUN_MIN (figé)."""
    d1 = par_tranche_z(f1)
    d2 = par_tranche_z(f2)
    zs = sorted(set(d1) & set(d2))
    if not zs or zs[-1] - zs[0] < COMMUN_MIN:
        return None
    th = np.array([np.arctan2(d1[z][1] - d2[z][1], d1[z][0] - d2[z][0])
                   for z in zs])
    dth = (np.diff(th) + np.pi) % (2 * np.pi) - np.pi
    return float(np.sum(dth) / (2 * np.pi))


def analyse(psi, inside, C):
    """Détecteur E44 complet (filiation) + filtre axial + tressage
    (amendement gelé)."""
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    wx, wy, wz = mask_hors_recipient(wx, wy, wz, inside)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f['closed'] and not np.any(f['disp']))]
    axiaux = [f for f in ouverts
              if f['len'] >= LONG_MIN
              and (f['pts'][:, 2].max() - f['pts'][:, 2].min())
              >= ETENDUE_Z_MIN]
    windings = [round(axial_winding(f['pts'], C), 2) for f in axiaux]
    paires = []
    for i in range(len(axiaux)):
        for j in range(i + 1, len(axiaux)):
            w = enroulement_mutuel(axiaux[i]['pts'], axiaux[j]['pts'])
            if w is not None and abs(w) >= SEUIL_TRESSAGE:
                paires.append((i, j, round(w, 3)))
    return {"n_ouverts": len(ouverts), "n_axiaux": len(axiaux),
            "windings_axiaux": windings, "paires_tressees": paires,
            "tresse": len(paires) > 0, "anom": anom, "amb": amb}


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, graine 999993 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        inside, ring, fix_val, C = geometrie_B(32)
        rng = np.random.default_rng(999993)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (32,) * 3))
        psi[~inside] = 0.0
        psi[ring] = fix_val[ring]
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(80):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(ring | ~inside, fix_val))
        r = analyse(psi, inside, C)
        print("SMOKE :", r)
        return

    t0 = time.time()
    inside, ring, fix_val, C = geometrie_B(N)
    fix_mask = ring | ~inside
    res = {"campagne": "E54-A", "amendement": "b495267e…964c1189 (gelé)",
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
                    r = analyse(psi, inside, C)
                    snaps[t] = r
                    print(f"  graine {graine} t={t:.0f} : axiaux="
                          f"{r['n_axiaux']} windings={r['windings_axiaux']} "
                          f"tressées={len(r['paires_tressees'])}", flush=True)
        res["runs"][str(graine)] = {str(k): v for k, v in snaps.items()}
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e54a_run_{graine}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res["runs"][str(graine)], f, ensure_ascii=False)
        print(f"graine {graine} terminée", flush=True)

    # ---- agrégation gelée (amendement E54-A + protocole v1) ----
    # P0 recalibré : à t=45 et t=90 — ≥1 axial dans ≥4/6 graines ET
    # médiane des windings du plus long filament dans [9, 19]
    n_avec_axial = 0
    windings_max = []
    for g, snaps in res["runs"].items():
        ok_g = False
        for t in (45.0, 90.0):
            s = snaps[str(t)]
            if s["n_axiaux"] >= 1:
                ok_g = True
                windings_max.append(s["windings_axiaux"][0])
        n_avec_axial += ok_g
    med = float(np.median(windings_max)) if windings_max else None
    ag = {"P0_recalibre": (n_avec_axial >= P0_MIN_GRAINES
                           and med is not None
                           and P0_FENETRE[0] <= med <= P0_FENETRE[1]),
          "n_graines_avec_axial_t45_90": n_avec_axial,
          "mediane_winding_max": med,
          "P1_tressage_nucle": any(
              res["runs"][g][str(t)]["tresse"]
              for g in res["runs"] for t in (8.0, 12.0, 20.0)),
          "P2_tressage_persiste": any(
              res["runs"][g][str(t)]["tresse"]
              and any(res["runs"][g][str(t2)]["tresse"]
                      for t2 in (45.0, 90.0))
              for g in res["runs"] for t in (8.0, 12.0, 20.0)),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e54a_tressage_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
