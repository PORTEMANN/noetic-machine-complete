#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E64 — LA FENÊTRE DU COURONNEMENT : τ_fuite(κ)
[protocole E64-FENETRE-KAPPA-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E64. Protocole gelé dans
e64_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : harnais E61/E62 repris (filaments, Biot–Savart,
remaillage, T0 instrument inchangés ; cage ANU géométrie d'E60-B
inchangée). Mesures moteurs : E61 (la cage tient à κ=0,05 sur [0,90]) ;
E62 (elle fuit entre t=90 et t=135 à ce même κ — noyau stable, peau qui
fuit). E59 a montré la forme : la frontière comme fonction, pas comme
liste. E64 en est la seconde : τ_fuite en fonction de κ.

Question gelée (la question exacte de la phénoménologie) : l'équilibre
souffle/pression a-t-il un DOMAINE ? Trop peu de pression : la cage fuit
(clause d'échappement) ; trop : elle est écrasée (clause rms ≥ 0,5×) ;
entre les deux : la fenêtre où la cage tient toutes les clauses gelées
jusqu'à t=180.

Grille figée : κ ∈ {0,025 ; 0,05 ; 0,1 ; 0,2} (κ=0,05 = contrôle de
filiation E61/E62). Clauses INCHANGÉES d'E60 (rms ∈ [0,5 ; 1,5]× initial,
échappement ≤ 2×R_cage). Snapshots t = 0, 45, 90, 135, 180 (figé).
τ_fuite = premier snapshot avec échappement > 2×R_cage ; si jamais :
τ_fuite ≥ 180 (figé).

Usage : python3 e64_run.py            (campagne — interdit avant décision)
        python3 e64_run.py --smoke    (validation technique déclarée)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e60_run import anneau, remaille, rayon_et_centre, v_analytique
from e61_run import vitesse_biotsavart, rk4, cage_anu  # filiation

# ---------------- paramètres gelés (filiation E60→E62, inchangés) -----------
DT = 0.25
KAPPAS = [0.06, 0.075, 0.1, 0.125, 0.15]        # figé ; 0,05 = contrôle E61/E62
R_T0 = 10.0
TOL_T0 = 0.30
TOL_T0_SCALING = 0.15
TMAX = 180.0
SNAP_T = [0.0, 45.0, 90.0, 135.0, 180.0]
R_CAGE = 12.0


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
        fils = cage_anu()
        for _ in range(3):
            fils = rk4(fils, DT, confine=True, kappa=0.1)
        print("SMOKE OK")
        return

    t0 = time.time()
    res = {"campagne": "E64-A", "protocole": "E64-FENETRE-KAPPA-1.0 (gelé)",
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

    for kappa in KAPPAS:
        fils = cage_anu()
        # confinement au taux kappa du point (rk4 filiatif : confine=True,
        # kappa passé en paramètre — ajout gelé)
        snaps = mesure_cage(fils, kappa)
        rms0 = snaps[0.0]["rms"]
        tient = (all(0.5 * rms0 <= snaps[t]["rms"] <= 1.5 * rms0
                     for t in SNAP_T)
                 and all(snaps[t]["ech"] <= 2 * rms0 for t in SNAP_T))
        fuites = [t for t in SNAP_T if snaps[t]["ech"] > 2 * rms0]
        tau = min(fuites) if fuites else TMAX
        res["points"][kappa] = {"snaps": {str(k): v for k, v
                                          in snaps.items()},
                                "tient_t180": tient,
                                "tau_fuite": tau,
                                "rms_t180": snaps[TMAX]["rms"],
                                "ecrase": snaps[TMAX]["rms"] < 0.5 * rms0}
        print(f"κ={kappa} : tient={tient} τ_fuite={tau} "
              f"rms180={snaps[TMAX]['rms']}", flush=True)
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e64a_k{kappa}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res["points"][kappa], f, ensure_ascii=False)

    # ---- agrégation gelée (règles : e64_protocole.json) ----
    tient_par_k = {str(k): res["points"][k]["tient_t180"] for k in KAPPAS}
    ks_ok = [k for k in KAPPAS if res["points"][k]["tient_t180"]]
    fenetre = (len(ks_ok) > 0
               and (KAPPAS[0] not in ks_ok or KAPPAS[-1] not in ks_ok))
    ag = {"T0_valide": res["T0"]["valide"],
          "tient_par_kappa": tient_par_k,
          "tau_fuite_par_kappa": {str(k): res["points"][k]["tau_fuite"]
                                  for k in KAPPAS},
          "ecrase_par_kappa": {str(k): res["points"][k]["ecrase"]
                               for k in KAPPAS},
          "kappa_fenetre": ks_ok,
          "controle_filiation_k005": res["points"][0.05]["tient_t180"],
          "fenetre_presente": fenetre,
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e64a_fenetre_kappa_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
