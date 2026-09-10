#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E61 — LA PRESSION DU VIDE : la cage ANU sous confinement
[protocole E61-PRESSION-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E61. Protocole gelé dans
e61_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : harnais E60 repris (filaments, Biot–Savart
désingularisé, RK4, remaillage, T0 instrument — inchangés) ; verdict E60
(B3-FAIL, 09/09/2026) : les composites libres sont cohérents de forme
mais non liés en position — la cage gonfle (+26 %) et un filament
s'échappe ; lecture mesurée : le Biot–Savart libre n'a PAS de pression
du vide. La phénoménologie fondatrice exige l'équilibre : la cavité
repousse la pression du vide. E61 ajoute ce terme.

Ajout gelé (le seul) : v_conf(x) = −κ · x/|x| — dérive radiale
confinante à taux constant κ = 0,05 (pression constante sur la cavité —
figé ; dimensionné sur la mesure d'E60 : gonflement ≈ 0,035/unité).

Design gelé : la cavité ANU (géométrie d'E60-B inchangée) ; deux bras :
A — libre (témoin : doit reproduire le gonflement d'E60) ; B — confiné
(κ=0,05). Clauses identiques à E60 (figées, inchangées) : rms de la cage
dans [0,5 ; 1,5]× l'initial, échappement ≤ 2×R_cage, snapshots t = 0, 5,
12, 20, 45, 90.

Usage : python3 e61_run.py            (campagne — interdit avant décision)
        python3 e61_run.py --smoke    (validation technique déclarée)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e60_run import (anneau, remaille, gauss_link, v_analytique,
                     rayon_et_centre)  # filiation E60 (fonctions pures)

# ---------------- paramètres gelés (filiation E60, sauf mention) ------------
GAMMA_CIRC = 1.0
A_CUT = 0.5
DT = 0.25
KAPPA = 0.05            # taux de dérive confinante — figé (mesure E60)
R_CAGE, R_ANU, N_ANU = 12.0, 6.0, 18
R_T0 = 10.0
TOL_T0 = 0.30
TOL_T0_SCALING = 0.15
TMAX = 90.0
SNAP_T = [0.0, 5.0, 12.0, 20.0, 45.0, 90.0]


def vitesse_biotsavart(fils, confine=False):
    """Filiation E60 ; confinement ajouté si confine (ajout gelé)."""
    pts = np.concatenate(fils)
    v = np.zeros_like(pts)
    for P in fils:
        seg = np.roll(P, -1, axis=0) - P
        mid = P + seg / 2
        R = pts[:, None, :] - mid[None, :, :]
        dl = seg[None, :, :]
        den = (np.sum(R**2, axis=2) + A_CUT**2) ** 1.5
        contrib = np.cross(R, dl) / den[:, :, None]
        v -= GAMMA_CIRC / (4 * np.pi) * contrib.sum(axis=1)
    if confine:
        r = np.linalg.norm(pts, axis=1, keepdims=True)
        v -= KAPPA * pts / np.maximum(r, 1e-9)
    return v


def rk4(fils, dt, confine=False):
    def f(F):
        return vitesse_biotsavart(F, confine)
    k1 = f(fils)
    k2 = f([P + dt * k1[i] / 2 for i, P in enumerate(fils)])
    k3 = f([P + dt * k2[i] / 2 for i, P in enumerate(fils)])
    k4 = f([P + dt * k3[i] for i, P in enumerate(fils)])
    return [remaille(P + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6)
            for i, P in enumerate(fils)]


def cage_anu():
    cage = []
    for k in range(N_ANU):
        phi = 2 * np.pi * k / N_ANU
        theta = np.pi * (k % 3) / 3 + np.pi / 6
        n = np.array([np.sin(theta) * np.cos(phi),
                      np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(n * R_CAGE, R_ANU, n))
    return cage


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée (hors campagne).
        print("SMOKE — mécanique (hors campagne)")
        fils = cage_anu()
        for _ in range(4):
            fils = rk4(fils, DT, confine=True)
        cents = np.array([rayon_et_centre(P)[1] for P in fils])
        print("SMOKE :", {"rms_cage": round(float(np.sqrt(np.mean(
            np.sum(cents**2, axis=1)))), 3)})
        return

    t0 = time.time()
    res = {"campagne": "E61", "protocole": "E61-PRESSION-1.0 (gelé)"}

    # ---- T0 (instrument — filiation E60, inchangé) ----
    vs, va = {}, {}
    for R_ in (5.0, R_T0, 20.0):
        fils = [anneau([0, 0, 0], R_, [0, 0, 1])]
        z0 = fils[0][:, 2].mean()
        for _ in range(int(20.0 / DT)):
            fils = rk4(fils, DT)
        vs[R_] = (fils[0][:, 2].mean() - z0) / 20.0
        va[R_] = v_analytique(R_)
    ecart = abs(vs[R_T0] / va[R_T0] - 1.0)
    rap_mes = (vs[5.0] / vs[R_T0], vs[20.0] / vs[R_T0])
    rap_an = (va[5.0] / va[R_T0], va[20.0] / va[R_T0])
    ecart_forme = max(abs(rap_mes[i] / rap_an[i] - 1.0) for i in (0, 1))
    res["T0"] = {"ecart_niveau": round(ecart, 4),
                 "ecart_forme": round(ecart_forme, 4),
                 "valide": bool(ecart <= TOL_T0
                                and ecart_forme <= TOL_T0_SCALING)}
    print(f"T0 : écarts {ecart:.4f} / {ecart_forme:.4f} → "
          f"{'PASS' if res['T0']['valide'] else 'FAIL'}", flush=True)
    if not res["T0"]["valide"]:
        res["agregation"] = {"verdict": "B3-FAIL-TECHNIQUE"}
        _ecris(res, t0)
        return

    # ---- les deux bras de la cage ----
    for bras, conf in (("A_libre", False), ("B_confine", True)):
        fils = cage_anu()
        snaps = {}
        steps = int(TMAX / DT)
        for s in range(steps + 1):
            t = s * DT
            if abs(t - min(SNAP_T, key=lambda x: abs(x - t))) < DT / 2:
                tt = min(SNAP_T, key=lambda x: abs(x - t))
                cents = np.array([rayon_et_centre(P)[1] for P in fils])
                snaps[tt] = {"rms_cage": round(float(np.sqrt(np.mean(
                    np.sum(cents**2, axis=1)))), 3),
                    "echappement_max": round(float(np.abs(cents).max()), 3)}
                print(f"  {bras} t={tt:.0f} : rms={snaps[tt]['rms_cage']} "
                      f"éch={snaps[tt]['echappement_max']}", flush=True)
            if s < steps:
                fils = rk4(fils, DT, confine=conf)
        res[bras] = {"snaps": {str(k): v for k, v in snaps.items()}}
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e61_{bras}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res[bras], f, ensure_ascii=False)
        print(f"{bras} terminé", flush=True)

    # ---- agrégation gelée (clauses d'E60 inchangées) ----
    A_, B_ = res["A_libre"]["snaps"], res["B_confine"]["snaps"]
    rms0 = A_["0.0"]["rms_cage"]

    def tient(snaps):
        return (all(0.5 * rms0 <= snaps[str(t)]["rms_cage"] <= 1.5 * rms0
                    for t in SNAP_T)
                and max(snaps[str(t)]["echappement_max"] for t in SNAP_T)
                <= 2 * rms0)

    ag = {"T0_valide": res["T0"]["valide"],
          "rms0": rms0,
          "A_tient": tient(A_), "B_tient": tient(B_),
          "rms_A": {str(t): A_[str(t)]["rms_cage"] for t in SNAP_T},
          "rms_B": {str(t): B_[str(t)]["rms_cage"] for t in SNAP_T},
          "ech_max_A": max(A_[str(t)]["echappement_max"] for t in SNAP_T),
          "ech_max_B": max(B_[str(t)]["echappement_max"] for t in SNAP_T),
          "A_reproduit_E60": (A_[str(90.0)]["rms_cage"] > rms0),
          "P1_confinement_tient": tient(B_) and not tient(A_),
          "verdict": None,
          "durée_s": round(time.time() - t0, 1)}
    ag["verdict"] = ("SUCCÈS" if ag["P1_confinement_tient"]
                     and ag["A_reproduit_E60"] else
                     "B3-FAIL" if not tient(B_) else "PARTIEL")
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e61_pression_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
