#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E68 — LA FENÊTRE κ PAR n : le parking avant la barrière est-il universel ?
[protocole E68-FENETRE-N-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E68. Protocole gelé dans
e68_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : harnais E64/E64-A repris (filaments, Biot–Savart,
remaillage, T0 instrument inchangés ; géométrie d'E60 : 3 latitudes,
R_cage=12, anneaux rayon 6 — inchangée). Mesures moteurs : E64-A
(fenêtre n=18 : κ ∈ ]0,075 ; 0,125[ — parking avant la barrière) ; E67
(paysages par n : barrière et vallée varient — n=18 : 16/22, n=14 :
15/17, n=24 : 13,5/14).

Question gelée : la fenêtre du couronnement est-elle par n ? Prédiction
directionnelle pré-enregistrée (déclarée) : la largeur de la fenêtre
suit la largeur du bassin crête→vallée du paysage (E67) — n=18
(séparation 6,0) : fenêtre la plus large ; n=24 (séparation 0,5) : la
plus étroite, voire aucune ; n=14 (séparation 2,0) : intermédiaire.

Design gelé : cages n ∈ {14, 18, 24} (figé — les trois cages
significatives : optimum de tenue E63, cage du corpus, paysage le plus
étroit E67) ; grille κ = {0,05 ; 0,075 ; 0,1 ; 0,125 ; 0,15} par n
(figé) ; clauses INCHANGÉES d'E60 (rms ∈ [0,5 ; 1,5]× initial,
échappement ≤ 2×R_cage à tous les snapshots) ; snapshots t = 0, 45, 90,
135, 180 ; τ_fuite figé comme en E64. Filiation : n=18, κ=0,1 doit
reproduire E64-A (tient à t=180).

Usage : python3 e68_fenetre_n.py            (campagne — interdit avant décision)
        python3 e68_fenetre_n.py --smoke    (validation technique déclarée)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e60_run import anneau, remaille, rayon_et_centre, v_analytique
from e61_run import vitesse_biotsavart, rk4  # filiation E61 (κ paramétré)

# ---------------- paramètres gelés (filiation E60→E67, inchangés) -----------
DT = 0.25
KAPPAS = [0.05, 0.075, 0.1, 0.125, 0.15]   # figé (grille d'E64-A)
NS = [14, 18, 24]                          # figé (les trois cages)
R_CAGE, R_ANU = 12.0, 6.0
R_T0 = 10.0
TOL_T0 = 0.30
TOL_T0_SCALING = 0.15
TMAX = 180.0
SNAP_T = [0.0, 45.0, 90.0, 135.0, 180.0]


def cage_n(n):
    """Géométrie d'E60 (3 latitudes), R_cage=12, anneaux rayon 6 —
    inchangée (E63/E66/E67)."""
    cage = []
    for k in range(n):
        phi = 2 * np.pi * k / n
        theta = np.pi * (k % 3) / 3 + np.pi / 6
        ax = np.array([np.sin(theta) * np.cos(phi),
                       np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(ax * R_CAGE, R_ANU, ax))
    return cage


def mesure_cage(fils, kappa):
    snaps = {}
    steps = int(TMAX / DT)
    for s in range(steps + 1):
        t = s * DT
        if abs(t - min(SNAP_T, key=lambda x: abs(x - t))) < DT / 2:
            tt = min(SNAP_T, key=lambda x: abs(x - t))
            cents = np.array([rayon_et_centre(P)[1] for P in fils])
            snaps[tt] = {"rms": round(float(np.sqrt(np.mean(
                np.sum(cents**2, axis=1)))), 3),
                "ech": round(float(np.abs(cents).max()), 3)}
        if s < steps:
            fils = rk4(fils, DT, confine=True, kappa=kappa)
    return snaps


def main():
    if "--smoke" in sys.argv:
        print("SMOKE — mécanique (hors campagne)")
        fils = cage_n(14)
        for _ in range(3):
            fils = rk4(fils, DT, confine=True, kappa=0.1)
        print("SMOKE OK :", len(fils), "anneaux (n=14)")
        return

    t0 = time.time()
    res = {"campagne": "E68", "protocole": "E68-FENETRE-N-1.0 (gelé)",
           "points": {}}

    # ---- T0 (instrument — filiation, inchangé) ----
    vs, va = {}, {}
    for R_ in (5.0, R_T0, 20.0):
        fils = [anneau([0, 0, 0], R_, [0, 0, 1])]
        z0 = fils[0][:, 2].mean()
        for _ in range(int(20.0 / DT)):
            fils = rk4(fils, DT)
        vs[R_] = (fils[0][:, 2].mean() - z0) / 20.0
        va[R_] = v_analytique(R_)
    ecart = abs(vs[R_T0] / va[R_T0] - 1.0)
    rap = abs((vs[5.0] / vs[R_T0]) / (va[5.0] / va[R_T0]) - 1.0)
    res["T0"] = {"ecart_niveau": round(ecart, 4),
                 "ecart_forme": round(rap, 4),
                 "valide": bool(ecart <= TOL_T0 and rap <= TOL_T0_SCALING)}
    print(f"T0 : {ecart:.4f} / {rap:.4f} → "
          f"{'PASS' if res['T0']['valide'] else 'FAIL'}", flush=True)
    if not res["T0"]["valide"]:
        res["agregation"] = {"verdict": "B3-FAIL-TECHNIQUE"}
        _ecris(res, t0)
        return

    for n in NS:
        for kappa in KAPPAS:
            snaps = mesure_cage(cage_n(n), kappa)
            rms0 = snaps[0.0]["rms"]
            tient = (all(0.5 * rms0 <= snaps[t]["rms"] <= 1.5 * rms0
                         for t in SNAP_T)
                     and all(snaps[t]["ech"] <= 2 * rms0 for t in SNAP_T))
            fuites = [t for t in SNAP_T if snaps[t]["ech"] > 2 * rms0]
            tau = min(fuites) if fuites else TMAX
            res["points"][f"n{n}_k{kappa}"] = {
                "snaps": {str(k): v for k, v in snaps.items()},
                "tient_t180": tient, "tau_fuite": tau,
                "rms_t180": snaps[TMAX]["rms"]}
            print(f"n={n} κ={kappa} : tient={tient} τ={tau} "
                  f"rms180={snaps[TMAX]['rms']}", flush=True)
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "data", f"e68_n{n}_k{kappa}.json")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res["points"][f"n{n}_k{kappa}"], f,
                          ensure_ascii=False)

    # ---- agrégation gelée (règles : e68_protocole.json) ----
    ag = {"T0_valide": res["T0"]["valide"],
          "fenetre_par_n": {},
          "filiation_n18_k01": res["points"]["n18_k0.1"]["tient_t180"],
          "durée_s": round(time.time() - t0, 1)}
    for n in NS:
        ks_ok = [k for k in KAPPAS
                 if res["points"][f"n{n}_k{k}"]["tient_t180"]]
        ag["fenetre_par_n"][str(n)] = {
            "tient_par_kappa": {str(k): res["points"][f"n{n}_k{k}"]["tient_t180"]
                                for k in KAPPAS},
            "tau_fuite_par_kappa": {str(k): res["points"][f"n{n}_k{k}"]["tau_fuite"]
                                    for k in KAPPAS},
            "kappa_fenetre": ks_ok}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e68_fenetre_n_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
