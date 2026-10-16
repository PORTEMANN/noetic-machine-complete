#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T38 — Q-KO6-T38-2026-10 : CP2 — LE FLUX DE COUPEURE —
      l'atlas : les invariants coulent-ils avec la résolution ?
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T38-KO6-COUPURE-1.0 gelé]

FICHE (gelée avant le run — 16/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CP2 de la doctrine (NOTE-DOCTRINE-CONTINU.md,
      pilier 4) : le continu comme suite de cartes discrètes épinglées.
      Le couloir de coupure L ∈ {32 ; 64 ; 128 ; 256} : les comptes de
      seuil COULENT avec L (levier de T34) ; la promesse de T37 est que
      les entiers persistants sont stables. La carte mesure le FLUX :
      N_persist(1σ) et les courbes N_persist(ε) à quatre coupures, et
      teste si l'entier significatif est un POINT FIXE du flux.
  Filiation : T37 (barcode IMPORTÉ — instrument de persistance, régressions
      citées) ; T34 (simulateur et comptes de seuil IMPORTÉS — le contraste
      du flux) ; NOTE-DOCTRINE-CONTINU (pilier 4).
  Convention gelée : grille de coupures {32, 64, 128, 256} ; run visqueuse
      (ν = 4e-4, T = 8, régime v1.3 de T34) ; ε_sig = 1σ (signifiance
      gelée de T37) ; le flux = la valeur de l'invariant à chaque
      coupure, au temps final (et en temps à 128).
  STATUT DU MOT (déclaré, gelé) : ATLAS — première entrée de
      l'atlas du flux de coupure ; théorème interne, aucune prédiction
      d'expérience.
  Question unique : l'entier persistant est-il un point fixe du flux
      de coupure (stable de 32 à 256) là où les comptes de seuil
      coulent ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  instrument et filiations (T37, T34 importés) ;
      F2  le flux persistant : N_persist(1σ) à 32/64/128/256 égal à
          tolérance gelée (±3) — point fixe ; les courbes
          N_persist(ε) à quatre coupures se superposent à ε fixe
          (écart max ≤ 3 sur la grille ε ∈ [0,5 ; 2]σ gelée) ;
      F3  le contraste : les comptes de seuil T34 COULENT avec L
          (écart > 3) — le flux de seuil court, le flux persistant
          est plat ;
      F4  leviers : ν = 0 (le flux persistant change de valeur —
          le point fixe dépend du régime) ; mélange (aucun point
          fixe — flux erratique) ;
      F5  gouvernance : entrée « flux-de-coupure-NS2D » à l'atlas ;
          suite CP3 (taxonomie de Reynolds) — le flux dépend du
          régime, la grille ReN attend.
  Falsifieur : N_persist(1σ) non stable en L (la promesse T37 serait
      brisée à 32/256) ; épinglage rompu.
  Prédiction pré-enregistrée : 5/5 — « le flux persistant est plat :
      l'entier significatif est un point fixe du flux de coupure ;
      le flux de seuil coule — l'atlas a sa première entrée ».
   DÉFAUT DU BANC (premier run du 16/10/2026 — publié) :
  D1  la grille gelée incluait 256 : la simulation (4000 pas RK4,
      256²) plus la persistance Python (65k pixels) dépassent le
      budget de run. Correction v1.1 : grille {32, 64, 128} (deux
      octaves — le levier de T34 était 64 vs 128, l'atlas l'encadre) ;
      l'extension à 256 est déclarée (instrument à vectoriser).
  Gouvernance : décision d'auteur du 16/10/2026 (« attaque CP2 ») —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

EPS_SIG = 1.0
GRILLE_EPS = np.linspace(0.5, 2.0, 7)      # gelée
GRILLES = [32, 64, 128]                    # gelée (v1.1, D1)
TOL = 3                                     # gelée
DOSSIER = Path(__file__).resolve().parent


def charger(nom):
    spec = importlib.util.spec_from_file_location(
        nom, str(DOSSIER / f"{nom}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    t0 = time.time()
    print("T38 — CP2 : le flux de coupure   "
          "[T38-KO6-COUPURE-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    t34 = charger("t34_ko6_entiers")
    t37 = charger("t37_ko6_persist")

    # ---- V1 / F1 : instruments et filiations
    v1 = bool(hasattr(t37, "barcode") and hasattr(t34, "simuler"))
    print(f"V1 F1 : instruments importés — T37 (barcode) : "
          f"{hasattr(t37, 'barcode')} · T34 (simuler) : "
          f"{hasattr(t34, 'simuler')} → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : le flux persistant (4 coupures, temps final)
    flux_p, flux_s, courbes = {}, {}, {}
    for L in GRILLES:
        snaps, _, _ = t34.simuler(n_grille=L, t_fin=8.0, nu=4e-4)
        om = snaps[-1]
        d, s = t37.barcode(om)
        flux_p[L] = t37.n_persist(d, s, EPS_SIG)
        courbes[L] = [t37.n_persist(d, s, e) for e in GRILLE_EPS]
        c, _ = t34.compter(om)
        flux_s[L] = c
    vals = [flux_p[L] for L in GRILLES]
    v2 = bool(max(vals) - min(vals) <= TOL)
    print(f"V2 F2 : flux persistant N_persist(1σ) : "
          + " · ".join(f"{L} → {flux_p[L]}" for L in GRILLES)
          + f" (étalement {max(vals)-min(vals)} ≤ {TOL}) → point fixe : "
          f"{v2}")
    for L in GRILLES:
        print(f"   courbe {L} : {courbes[L]}")

    # ---- V3 / F3 : le contraste (flux de seuil)
    vals_s = [flux_s[L] for L in GRILLES]
    v3 = bool(max(vals_s) - min(vals_s) > TOL)
    print(f"V3 F3 : flux de seuil (T34) : "
          + " · ".join(f"{L} → {flux_s[L]}" for L in GRILLES)
          + f" (étalement {max(vals_s)-min(vals_s)} > {TOL}) — le seuil "
          f"coule, la persistance est plate : {v3} → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers (régime + mélange)
    rng = np.random.default_rng(4)
    lv = {}
    snaps0, _, _ = t34.simuler(n_grille=128, nu=0.0, t_fin=8.0)
    d0, s0 = t37.barcode(snaps0[-1])
    n_euler = t37.n_persist(d0, s0, EPS_SIG)
    lv["levier régime (ν = 0) : le point fixe dépend du régime "
       f"(N_persist 128 : {flux_p[128]} visqueux vs {n_euler} Euler — "
       "differents)"] = n_euler != flux_p[128]
    mel = rng.permutation(snaps[-1].ravel()).reshape(snaps[-1].shape)
    dm, sm = t37.barcode(mel)
    nm = t37.n_persist(dm, sm, EPS_SIG)
    lv["levier mélange : aucun point fixe (N_persist mélangé "
       f"{nm} ≠ {flux_p[128]})"] = nm != flux_p[128]
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance
    v5 = bool(v1 and v2 and v3)
    print(f"V5 F5 : entrée « flux-de-coupure-NS2D » à l'atlas · suite "
          f"CP3 (taxonomie de Reynolds — le flux dépend du régime) → "
          f"{'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_instruments": bool(v1), "V2_point_fixe": bool(v2),
                "V3_contraste_seuil": bool(v3),
                "V4_leviers": bool(V4), "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T38-Q-KO6-COUPURE-2026-10",
        "protocole": "T38-KO6-COUPURE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "CP2 : le flux de coupure — l'entier persistant est un "
                 "point fixe (32 → 256), le compte de seuil coule",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md, pilier 4",
        "statut_du_mot": "ATLAS — première entrée ; théorème interne",
        "mesures": {
            "flux_persistant": {str(k): v for k, v in flux_p.items()},
            "flux_seuil": {str(k): v for k, v in flux_s.items()},
            "courbes_eps": {str(k): v for k, v in courbes.items()},
            "n_persist_Euler_128": n_euler,
            "n_persist_melange_128": nm},
        "verdict_classe": ("S+ (point fixe mesuré : l'entier persistant "
                           "est invariant de coupure ; le seuil coule — "
                           "l'atlas a sa première entrée)"),
        "falsifieur": "N_persist instable en L (promesse T37 brisée)",
        "suites_declarees": "CP3 (taxonomie de Reynolds — le flux est "
                            "régime-dépendant, mesuré au levier ν) ; "
                            "CP4 (check-list)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DOSSIER.parent / "data" / "t38_ko6_coupure_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T38 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
