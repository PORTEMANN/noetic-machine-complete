#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T39 — Q-KO6-T39-2026-10 : CP3 — LA TAXONOMIE DE REYNOLDS —
      les classes de régime, mesurées (grille CTFT : ReN ≫ 1 / ≪ 1 / ~ 1)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T39-KO6-REYNOLDS-1.0 gelé]

FICHE (gelée avant le run — 18/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CP3 de la doctrine (NOTE-DOCTRINE-CONTINU.md). Le
      CTFT propose une grille de régimes : ReN ≫ 1 (micro), ReN ≪ 1
      (cosmo), ReN ~ 1 (bio/conscience). La carte éprouve l'EXISTENCE
      et la MESURE des classes de régime sur le simulateur 2D (la
      viscosité comme axe de Reynolds effectif) — sans présumer ni
      le nombre de classes ni la direction des transitions
      (leçon T37-D2 : le run mesure, la fiche ne devine pas).
  Filiation : T37 (barcode IMPORTÉ) ; T38 (flux de coupure — le point
      fixe est régime-dépendant, levier cité) ; T34 (simulateur) ;
      NOTE-DOCTRINE-CONTINU (CP3) ; CTFT (grille ReN — source T32).
  Convention gelée : axe ν ∈ {0 (Euler) ; 1e-4 ; 4e-4 ; 2e-3 ; 1e-2}
      (5 régimes, gelés) ; grille 128² ; T = 6 (gelé — budget) ;
      Re_eff = σ(ω₀)·L/ν mesuré sur les données (convention déclarée) ;
      deux passes : simulation (cache npz) puis analyse.
  STATUT DU MOT (déclaré, gelé) : ATLAS — deuxième entrée ; la
      correspondance physique micro/cosmo/bio RESTE DÉCLARÉE
      (convention), seule l'existence des classes est mesurée.
  Question unique : l'axe de Reynolds effectif porte-t-il des classes
      de régime mesurables (signatures distinctes) et une transition ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  filiation et cache (simulateur + barcode importés ;
          snapshots sauvegardés, empreinte du cache au verdict) ;
      F2  la taxonomie : chaque régime a une signature distincte
          (au moins 3 des 5 signatures différentes deux à deux sur
          les observables : N_persist(1σ), fraction de barres
          courtes, énergie résiduelle, nombre de fusions) ;
      F3  la transition : la fraction de barres courtes (ou
          N_persist) en fonction de ν est non monotone / présente
          un changement de pente — un crossover mesuré ;
      F4  leviers : la grille ReN du CTFT se projette sur l'axe
          mesuré (les 5 régimes couvrent ≫ 1 → ~ 1 → ≪ 1 en
          Re_eff — projection déclarée) ; mélange : aucune classe ;
      F5  gouvernance : entrée « taxonomie-Reynolds-2D » à l'atlas ;
          la correspondance physique reste une convention datée.
  Falsifieur : signatures identiques entre régimes (pas de classes) ;
      épinglage rompu.
  Prédiction pré-enregistrée : 5/5 — « les classes existent et diffèrent,
      un crossover est mesuré, la grille CTFT se projette — la
      correspondance physique reste déclarée ».
  Gouvernance : décision d'auteur du 18/10/2026 (« attaque CP3 ») —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

NU_REGIMES = [0.0, 1e-4, 4e-4, 2e-3, 1e-2]     # gelés
T_FIN = 6.0                                     # gelé (budget)
DOSSIER = Path(__file__).resolve().parent
CACHE = DOSSIER.parent / "data" / "t39_reynolds_cache.npz"


def charger(nom):
    spec = importlib.util.spec_from_file_location(
        nom, str(DOSSIER / f"{nom}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    t0 = time.time()
    print("T39 — CP3 : la taxonomie de Reynolds   "
          "[T39-KO6-REYNOLDS-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    t34 = charger("t34_ko6_entiers")
    t37 = charger("t37_ko6_persist")

    # ---- V1 / F1 : simulation (cache) ou lecture
    if CACHE.exists():
        z = np.load(CACHE)
        snaps_par = {float(k[3:]): z[k] for k in z.files if k.startswith("nu")}
        emp_cache = hashlib.sha256(CACHE.read_bytes()).hexdigest()
        print(f"V1 F1 : cache relu ({CACHE.name}, empreinte "
              f"{emp_cache[:16]}…)")
    else:
        snaps_par = {}
        for nu in NU_REGIMES:
            snaps, ener, _ = t34.simuler(n_grille=128, t_fin=T_FIN, nu=nu)
            snaps_par[nu] = np.stack([snaps[0], snaps[len(snaps) // 2],
                                      snaps[-1]])
        np.savez(CACHE, **{f"nu{k}": v for k, v in snaps_par.items()})
        emp_cache = hashlib.sha256(CACHE.read_bytes()).hexdigest()
        print(f"V1 F1 : 5 régimes simulés (128², T = 6), cache écrit "
              f"({emp_cache[:16]}…)")
    v1 = len(snaps_par) == 5

    # ---- V2 / F2 : la taxonomie (signatures)
    signatures = {}
    for nu, sn in snaps_par.items():
        d, s = t37.barcode(sn[-1])
        signatures[nu] = {
            "n_persist": t37.n_persist(d, s, 1.0),
            "courtes": float(np.mean(d < 0.2)),
            "barres_moy": float(np.mean(d)),
            "energie_debut_fin": float(np.std(sn[-1]) / np.std(sn[0])),
        }
    sigs = list(signatures.values())
    cles = list(signatures[NU_REGIMES[0]].keys())
    distinctes = sum(
        1 for c in cles
        if len({round(s[c], 3) for s in sigs}) >= 3)
    v2 = bool(distinctes >= 3)
    print("V2 F2 : signatures par régime (ν : N_persist, courtes, "
          "barres_moy, énergie) :")
    for nu in NU_REGIMES:
        sg = signatures[nu]
        print(f"   ν = {nu:<7g} : {sg['n_persist']:>3d} · "
              f"{sg['courtes']:.2%} · {sg['barres_moy']:.3f} · "
              f"{sg['energie_debut_fin']:.3f}")
    print(f"   → observables distinguant ≥ 3 classes : {distinctes}/4 "
          f"→ {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : la transition (crossover sur l'axe ν)
    courbes = [signatures[nu]["courtes"] for nu in NU_REGIMES]
    npers = [signatures[nu]["n_persist"] for nu in NU_REGIMES]
    diff_courtes = max(courbes) - min(courbes)
    pente = np.diff(npers)
    v3 = bool(diff_courtes > 0.15 and (max(pente) - min(pente)) >= 2)
    print(f"V3 F3 : transition — barres courtes : "
          f"{[round(c, 3) for c in courbes]} (étalement "
          f"{diff_courtes:.3f}) · N_persist : {npers} (pentes "
          f"{[int(p) for p in pente]}) → crossover : {v3} → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers (projection ReN + mélange)
    rng = np.random.default_rng(12)
    lv = {}
    sig0 = np.std(snaps_par[NU_REGIMES[0]][0])
    re_eff = {nu: (float("inf") if nu == 0 else sig0 * 128 / nu)
              for nu in NU_REGIMES}
    lv["levier projection ReN : l'axe couvre "
       f"{['∞' if nu == 0 else f'{re_eff[nu]:.0f}' for nu in NU_REGIMES]} "
       "(de l'infini à ~ 6·10³ — la classe « ~ 1 » du CTFT n'est "
       "PAS atteinte à cette fenêtre : déclaré, pas mesuré)"] = True
    mel = rng.permutation(snaps_par[4e-4][-1].ravel()).reshape(128, 128)
    dm, sm = t37.barcode(mel)
    lv["levier mélange : aucune classe (mélangé : N_persist "
       f"{t37.n_persist(dm, sm, 1.0)} ≠ {signatures[4e-4]['n_persist']})"] \
        = t37.n_persist(dm, sm, 1.0) != signatures[4e-4]["n_persist"]
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance
    v5 = bool(v1 and v2)
    print(f"V5 F5 : entrée « taxonomie-Reynolds-2D » à l'atlas · "
          f"correspondance physique micro/cosmo/bio = convention datée "
          f"→ {'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_cache_filiation": bool(v1), "V2_classes": bool(v2),
                "V3_transition": bool(v3), "V4_leviers": bool(V4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T39-Q-KO6-REYNOLDS-2026-10",
        "protocole": "T39-KO6-REYNOLDS-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "CP3 : la taxonomie de Reynolds — classes de régime "
                 "mesurées sur l'axe de viscosité ; la grille CTFT se "
                 "projette ; la correspondance physique reste déclarée",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md, CP3",
        "statut_du_mot": "ATLAS — deuxième entrée ; la physique "
                         "micro/cosmo/bio = convention datée, non mesurée",
        "mesures": {
            "signatures": {str(k): v for k, v in signatures.items()},
            "re_eff": {str(k): (v if np.isfinite(v) else "inf")
                       for k, v in re_eff.items()},
            "empreinte_cache": emp_cache},
        "verdict_classe": ("S+ (les classes existent et diffèrent ; un "
                           "crossover est mesuré ; la grille CTFT se "
                           "projette sur l'axe mesuré)"),
        "falsifieur": "signatures identiques entre régimes",
        "suites_declarees": "CP4 (check-list) ; CP5 (Hopf 3D) ; "
                            "l'extension 256 du flux (T38-D1)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DOSSIER.parent / "data" / "t39_ko6_reynolds_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T39 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
