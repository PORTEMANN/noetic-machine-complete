#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E56-x — EXTENSION DE ROBUSTESSE du falsifieur E56 (loi T6)
[protocole E56x-ROBUSTESSE-1.0 gelé]
=====================================================================
Harnais officiel de l'extension. Protocole gelé dans
e56x_protocole.json (haché avant tout calcul — aveugle préservé).

Motivation (note de marge d'E56, 09/09/2026) : le SUCCÈS formel d'E56
repose sur 1 run (440204), des enroulements assis exactement au seuil
(|w|=0,5), et une disparition à t=90. L'extension mesure la robustesse ;
elle ne re-seuille rien.

Filiation : harnais d'E56 repris (détecteur E44 byte-level ; ancrage des
chapeaux inchangé ; seuil de tressage |w|≥0,5 INCHANGÉ — pas de
re-seuilage).

Design gelé :
  24 graines NOUVELLES 550101–550124 (déclarées, hors séries
  antérieures — 440204 reste historique, aucun recalibrage sur elle) ;
  deux bras appariés par graine :
    A : sans ancrage (= E54-C, témoin à la nouvelle taille d'échantillon)
    B : avec ancrage des chapeaux (= E56, inchangé)
  Snapshots t=8,12,20,45,90.
  Ajouts gelés (mesure, pas critère déplacé) :
    - marge d'enroulement : pour chaque paire tressée, marge = |w| − 0,5
      (enregistrée, seuil 0,5 inchangé) ;
    - persistance mesurée SÉPARÉMENT à t=45 et à t=90 (E56 comptait
      « 45 ou 90 » — raffinement déclaré).

Usage : python3 e56x_run.py            (campagne — interdit avant décision)
        python3 e56x_run.py --smoke    (validation technique déclarée :
                                        N=32, graine 999991 hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments  # filiation byte-level

# ---------------- paramètres gelés (filiation E54-C/E56, sauf mention) ------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SEEDS = list(range(550101, 550125))   # 24 NOUVELLES graines — déclaré
SNAP = [(160, 8.0), (240, 12.0), (400, 20.0), (900, 45.0), (1800, 90.0)]
WIND_PAROI = 4
LONG_MIN = 40
ETENDUE_Z_MIN = 30.0
COMMUN_MIN = 30.0
SEUIL_TRESSAGE = 0.5                  # INCHANGÉ — pas de re-seuilage
MARGE_MIN_ROBUSTE = 0.6               # |w| « nettement au-dessus du seuil » — figé avant calcul
TAUX_MIN_ROBUSTE = 3                  # graines avec persistance à t=45 — figé
P0_FENETRE = (9.0, 19.0)


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def geometrie_B(N_=N):
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


def V_chapeaux(N_=N):
    """Ancrage des pieds — identique à E56 (inchangé)."""
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    V = np.zeros((N_,) * 3)
    caps = (Z <= 4) | (Z >= 59)
    for i in range(8):
        for j in range(8):
            V -= 2.0 * caps * np.exp(-((X - (8 * i + 4))**2
                                       + (Y - (8 * j + 4))**2)
                                     / (2 * 1.5**2))
    return V


def gp_step(psi, lin, gamma_, dt_, fix=None, Vext=None):
    V = np.abs(psi)**2 - 1.0
    if Vext is not None:
        V = V + Vext
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    if fix is not None:
        psi[fix[0]] = fix[1][fix[0]]
    return psi


def par_tranche_z(pts):
    out = {}
    zs = np.floor(pts[:, 2]).astype(int)
    for z in sorted(set(zs)):
        out[int(z)] = pts[zs == z][:, :2].mean(axis=0)
    return out


def enroulement_mutuel(f1, f2):
    d1 = par_tranche_z(f1)
    d2 = par_tranche_z(f2)
    zs = sorted(set(d1) & set(d2))
    if not zs or zs[-1] - zs[0] < COMMUN_MIN:
        return None
    th = np.array([np.arctan2(d1[z][1] - d2[z][1], d1[z][0] - d2[z][0])
                   for z in zs])
    dth = (np.diff(th) + np.pi) % (2 * np.pi) - np.pi
    return float(np.sum(dth) / (2 * np.pi))


def analyse(psi, inside):
    """Identique à E54-C/E56, + marges enregistrées (ajout gelé)."""
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    wx, wy, wz = np.where(inside, wx, 0), np.where(inside, wy, 0), \
        np.where(inside, wz, 0)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f['closed'] and not np.any(f['disp']))]
    axiaux = [f for f in ouverts
              if f['len'] >= LONG_MIN
              and (f['pts'][:, 2].max() - f['pts'][:, 2].min())
              >= ETENDUE_Z_MIN]
    paires = []
    for i in range(len(axiaux)):
        for j in range(i + 1, len(axiaux)):
            w = enroulement_mutuel(axiaux[i]['pts'], axiaux[j]['pts'])
            if w is not None and abs(w) >= SEUIL_TRESSAGE:
                paires.append((i, j, round(w, 3)))
    return {"n_axiaux": len(axiaux), "paires_tressees": paires,
            "tresse": len(paires) > 0,
            "marges": [round(abs(w) - SEUIL_TRESSAGE, 3)
                       for _, _, w in paires],
            "anom": anom, "amb": amb}


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32, graine 999991 hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        inside, ring, fix_val, C = geometrie_B(32)
        rng = np.random.default_rng(999991)
        psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (32,) * 3))
        psi[~inside] = 0.0
        psi[ring] = fix_val[ring]
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(60):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(ring | ~inside,
                                                    fix_val))
        r = analyse(psi, inside)
        print("SMOKE :", r)
        return

    t0 = time.time()
    inside, ring, fix_val, C = geometrie_B(N)
    fix_mask = ring | ~inside
    VCAPS = V_chapeaux(N)
    res = {"campagne": "E56-x", "protocole": "E56x-ROBUSTESSE-1.0 (gelé)",
           "runs": {}}
    for graine in SEEDS:
        run = {}
        for bras, vcaps in (("A", None), ("B", VCAPS)):
            rng = np.random.default_rng(graine)
            psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
            psi[~inside] = 0.0
            psi[ring] = fix_val[ring]
            lin = gp_linear(N, A, GAMMA, DT)
            snaps = {}
            for step in range(1, SNAP[-1][0] + 1):
                psi = gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val),
                              Vext=vcaps)
                for pas, t in SNAP:
                    if step == pas:
                        snaps[t] = analyse(psi, inside)
            run[bras] = {str(k): v for k, v in snaps.items()}
            print(f"  graine {graine} bras {bras} terminé", flush=True)
        res["runs"][str(graine)] = run
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e56x_run_{graine}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(run, f, ensure_ascii=False)

    # ---- agrégation gelée (règles : e56x_protocole.json) ----
    def tresses(run, bras, t):
        return run[bras][str(t)]["tresse"]

    ag = {}
    comptes_B = [run["B"][str(t)]["n_axiaux"] for run in res["runs"].values()
                 for t in (45.0, 90.0)]
    ag["P0_fenetre_B"] = bool(comptes_B) and P0_FENETRE[0] <= float(
        np.median(comptes_B)) <= P0_FENETRE[1]
    ag["mediane_compte_B"] = float(np.median(comptes_B)) if comptes_B \
        else None
    for bras in ("A", "B"):
        ag[f"taux_nucleation_{bras}"] = sum(
            any(tresses(run, bras, t) for t in (8.0, 12.0, 20.0))
            for run in res["runs"].values())
        for t in (45.0, 90.0):
            ag[f"persistance_{bras}_t{int(t)}"] = sum(
                any(tresses(run, bras, t0) for t0 in (8.0, 12.0, 20.0))
                and tresses(run, bras, t)
                for run in res["runs"].values())
    marges_persist = [m for run in res["runs"].values()
                      if any(tresses(run, "B", t0) for t0 in (8.0, 12.0, 20.0))
                      for t in (45.0, 90.0)
                      for m in run["B"][str(t)]["marges"]]
    ag["marges_persistantes_B"] = marges_persist
    ag["marge_mediane_B"] = float(np.median(marges_persist)) \
        if marges_persist else None
    ag["ROBUSTE"] = (ag["persistance_B_t45"] >= TAUX_MIN_ROBUSTE
                     and ag["marge_mediane_B"] is not None
                     and ag["marge_mediane_B"]
                     >= MARGE_MIN_ROBUSTE - SEUIL_TRESSAGE)
    ag["CONFIRME_FAIBLE"] = (not ag["ROBUSTE"]
                             and ag["persistance_B_t45"] >= 1)
    ag["REFUTE"] = ag["persistance_B_t45"] == 0
    ag["durée_s"] = round(time.time() - t0, 1)
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e56x_robustesse_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
