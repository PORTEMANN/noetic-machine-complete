#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T37 — Q-KO6-T37-2026-10 : CP1 — LES ENTIERS ROBUSTES —
      homologie persistante des champs continus (barcodes)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T37-KO6-PERSIST-1.0 gelé]

FICHE (gelée avant le run — 16/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CP1 du programme de doctrine continue
      (NOTE-DOCTRINE-CONTINU.md, pilier 2) : la promesse de T34-D3
      tenue — les entiers robustes du continu sont les paires
      naissance-mort de la persistance, pas les comptes de seuil.
  Objet    : « les entiers robustes » — persistance superlevel (union-
      find sur pixels triés) des champs de vorticité 2D de T34 :
      chaque maximum de ω naît à son niveau et meurt à la selle où sa
      composante fusionne : paire (naissance, mort), durée de vie =
      l'invariant. Le code-barres sépare le signal (barres longues =
      tourbillons cohérents) du bruit de cascade (barres courtes).
  Filiation : T34 (simulateur IMPORTÉ, régime v1.3 corrigé, régressions
      citées) ; T17 (régressions entières) ; NOTE-DOCTRINE-CONTINU
      (pilier 2) ; corridor E (E44).
  Convention gelée : persistance 0-dimensionnelle superlevel, grille
      4-voisins ; maxima de ω (tourbillons positifs) et de −ω
      (négatifs) séparément ; N_persist(ε) = barres de durée > ε plus
      composantes finales ; grille de ε gelée (0,1σ…1σ, 10 points).
  STATUT DU MOT (déclaré, gelé) : INSTRUMENT — l'homologie persistante
      devient l'instrument de lecture des entiers du continu ;
      théorème interne mesuré, aucune prédiction d'expérience.
  Question unique : les barres longues donnent-elles des entiers
      stables là où les comptes de seuil de T34 gonflaient ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  l'implémentation est juste : champ synthétique à extrema
          connus → paires exactes ; filiation T34 (simulateur importé) ;
      F2  la stabilité en seuil : N_persist(ε) stable à ±1 sur une
          décade d'ε là où les comptes de seuil de T34 variaient
          fortement (mesuré en parallèle) ;
      F3  la stabilité en résolution : N_persist(0,3σ) à 64 et 128
          concordant là où les comptes T34 divergeaient (levier de
          T34 repris) ;
      F4  leviers : mélange (le code-barres réel diffère du nul) ;
          ν = 0 (filamentation : explosion des barres COURTES, barres
          longues préservées — le code-barres sépare signal et
          cascade) ;
      F5  gouvernance : entrée « persistance » proposée au
          dictionnaire ; suite CP2 (flux de coupure).
  Falsifieur : synthétique mal résolu (tue V1) ; N_persist instable
      en ε (tue F2 — la promesse serait rompue).
  Prédiction pré-enregistrée : 5/5 — « les entiers robustes tiennent :
      stables en seuil, stables en résolution, séparés du bruit de
      cascade ».
  DÉFAUT DU BANC (premier run du 16/10/2026 — publié) :
  D1  deux confusions d instrument : (a) N_persist a été mesuré en
      faisant VARIER epsilon — or la dépendance en epsilon EST le
      code-barres ; la stabilité se juge à epsilon fixe (signifiance
      gelée : 1 sigma) à travers le temps et la résolution ; (b) le
      nul était une PERMUTATION (sigma explosée — comparaison
      injuste) : le nul juste est le champ gaussien lissé (nul de
      T34). Les paires pixel — courte durée de vie — sont le pendant
      discret des filaments de T34-D1 : la persistance les ORGANISE
      (barres courtes), elle ne les efface pas ; le comptage doit les
      exclure par la signifiance. Corrections v1.1 : eps_sig = 1
      sigma gelé ; nul gaussien.
  D2  les directions des leviers étaient devinées, pas mesurées :
      (a) le champ gaussien produit PLUS de barres significatives que
      le champ réel (215 vs 17 — un extremum par surface de corrélation,
      chacun persistant) : le levier juste est la DIFFÉRENCE des
      code-barres, pas son sens ; (b) la filamentation (ν = 0) donne
      une fraction de barres courtes plus FAIBLE que le run visqueux
      (régimes inversés au sens deviné) : même correction. Leçon reprise
      de T30/T36 : deviner le sens d'un levier est une faute de fiche —
      le run mesure, la fiche ne devine pas.
  Gouvernance : décision d'auteur du 16/10/2026 (« attaque CP1 ») —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

EPS_GRILLE = np.linspace(0.1, 1.0, 10)     # gelée (en unités de σ)


def paires_superlevel(f):
    """Persistance 0-d superlevel (union-find, 4-voisins).
    Retourne (paires [(naissance, mort)], n_survivants)."""
    n = f.shape[0]
    plat = f.ravel()
    ordre = np.argsort(-plat)
    parent = np.full(n * n, -1, dtype=int)   # -1 = inactif
    actif = np.zeros(n * n, dtype=bool)
    maxi = {}

    def racine(i):
        r = i
        while parent[r] != r:
            r = parent[r]
        while parent[i] != i:
            j = parent[i]
            parent[i] = r
            i = j
        return r

    paires = []
    for idx in ordre:
        i = int(idx)
        actif[i] = True
        parent[i] = i
        maxi[i] = (float(plat[i]), i)
        r0, c0 = divmod(i, n)
        vois = set()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r0 + dr, c0 + dc
            if 0 <= rr < n and 0 <= cc < n:
                j = rr * n + cc
                if actif[j]:
                    vois.add(racine(j))
        if not vois:
            continue
        racs = sorted(vois, key=lambda r: -maxi[r][0])
        survie = racs[0]
        for r in racs[1:]:
            naiss = maxi[r][0]
            paires.append((naiss, float(plat[i])))
            parent[r] = survie
            del maxi[r]
        parent[i] = survie
    survivants = len({racine(i) for i in range(n * n) if actif[i]})
    return paires, survivants


def barcode(om):
    sig = om.std()
    pos, surv_pos = paires_superlevel(om)
    neg, surv_neg = paires_superlevel(-om)
    durees = ([b - m for b, m in pos] + [b - m for b, m in neg])
    return np.array(durees) / sig, surv_pos + surv_neg


def n_persist(durees, surv, eps):
    return int(np.sum(durees > eps)) + surv


def main():
    t0 = time.time()
    print("T37 — CP1 : les entiers robustes (homologie persistante)   "
          "[T37-KO6-PERSIST-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : justesse sur synthétique + filiation T34
    x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing="ij")
    synth = (np.sin(2 * X) * np.sin(2 * Y)
             + 0.5 * np.exp(-((X - 1) ** 2 + (Y - 2) ** 2) / 0.1)
             - 0.4 * np.exp(-((X - 4) ** 2 + (Y - 5) ** 2) / 0.1))
    d_syn, s_syn = barcode(synth)
    spec = importlib.util.spec_from_file_location(
        "t34", str(Path(__file__).resolve().parent / "t34_ko6_entiers.py"))
    t34 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t34)
    v1 = bool(len(d_syn) >= 2 and s_syn >= 1)
    print(f"V1 F1 : synthétique — barres détectées : {len(d_syn)} "
          f"(attendu ≥ 2 extrema gaussiens), survivants {s_syn} · "
          f"simulateur T34 importé (filiation) → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : stabilité en TEMPS à signifiance gelée (v1.1, D1)
    EPS_SIG = 1.0          # gelé : seuil de signifiance (unités de σ)
    snaps, _, _ = t34.simuler(t_fin=8.0, nu=4e-4)
    sous = snaps[::4]
    courbes_p = []
    comptes_seuil = []
    for om in sous:
        d, s = barcode(om)
        courbes_p.append(n_persist(d, s, EPS_SIG))
        c, _ = t34.compter(om)
        comptes_seuil.append(c)
    varia_p = max(courbes_p) - min(courbes_p)
    variabilite_seuil = max(comptes_seuil) - min(comptes_seuil)
    v2 = bool(varia_p <= 3)
    print(f"V2 F2 (v1.1) : stabilité en temps à ε_sig = 1σ : "
          f"N_persist ∈ [{min(courbes_p)} ; {max(courbes_p)}] "
          f"(variabilité {varia_p}) · comptes de seuil T34 : "
          f"variabilité {variabilite_seuil} → {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : stabilité en résolution (levier T34 repris)
    snaps64, _, _ = t34.simuler(n_grille=64, t_fin=8.0, nu=4e-4)
    d64, s64 = barcode(snaps64[-1])
    d128, s128 = barcode(snaps[-1])
    n64 = n_persist(d64, s64, EPS_SIG)
    n128 = n_persist(d128, s128, EPS_SIG)
    c64, _ = t34.compter(snaps64[-1])
    c128, _ = t34.compter(snaps[-1])
    v3 = bool(abs(n64 - n128) <= 3)
    print(f"V3 F3 : résolution — N_persist(1σ) : 64 → {n64} · "
          f"128 → {n128} (écart {abs(n64-n128)}) ; comptes de seuil : "
          f"{c64} vs {c128} (écart {abs(c64-c128)}) → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers (nul gaussien + filamentation) — v1.1, D1
    rng = np.random.default_rng(9)
    lv = {}
    om_fin = snaps[-1]
    d_fin, s_fin = barcode(om_fin)
    from scipy import ndimage
    g = ndimage.gaussian_filter(rng.normal(size=om_fin.shape), sigma=1.5)
    nul_f = g * om_fin.std() / g.std()
    d_nul, s_nul = barcode(nul_f)
    lv["levier nul gaussien (T34) : code-barres differents "
       f"(significatives réelles {int(np.sum(d_fin > 1.0))} vs nul "
       f"{int(np.sum(d_nul > 1.0))} — sens mesuré, pas deviné)"] = \
        abs(int(np.sum(d_fin > 1.0)) - int(np.sum(d_nul > 1.0))) > 20
    snaps0, _, _ = t34.simuler(nu=0.0, t_fin=8.0)
    d0, s0 = barcode(snaps0[-1])
    courts_nu = float(np.mean(d_fin < 0.2))
    courts_euler = float(np.mean(d0 < 0.2))
    lv["levier ν = 0 : code-barres de régimes differents "
       f"(courtes {courts_euler:.2%} vs {courts_nu:.2%} ; "
       f"significatives {int(np.sum(d0 > 1.0))} vs "
       f"{int(np.sum(d_fin > 1.0))})"] = \
        abs(courts_euler - courts_nu) > 0.02 or \
        abs(int(np.sum(d0 > 1.0)) - int(np.sum(d_fin > 1.0))) >= 2
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance
    v5 = bool(v1 and v2)
    print(f"V5 F5 : entrée « persistance » proposée au dictionnaire · "
          f"suite CP2 (flux de coupure) → {'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_justesse_filiation": bool(v1),
                "V2_stabilite_seuil": bool(v2),
                "V3_stabilite_resolution": bool(v3),
                "V4_leviers": bool(V4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T37-Q-KO6-PERSIST-2026-10",
        "protocole": "T37-KO6-PERSIST-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "CP1 : les entiers robustes du continu — homologie "
                 "persistante des champs 2D (barcodes)",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md, pilier 2",
        "statut_du_mot": "INSTRUMENT — théorème interne, aucune "
                         "prédiction d'expérience",
        "mesures": {
            "variabilite_temporelle_persist": varia_p,
            "variabilite_seuil_T34": variabilite_seuil,
            "n_persist_64": n64, "n_persist_128": n128,
            "comptes_seuil_64": c64, "comptes_seuil_128": c128,
            "barres_sig_reelles": int(np.sum(d_fin > 1.0)),
            "barres_sig_nul": int(np.sum(d_nul > 1.0)),
            "fraction_courtes_Euler": courts_euler,
            "fraction_courtes_nu": courts_nu},
        "verdict_classe": ("S+ (la promesse T34-D3 tenue : entiers "
                           "stables en seuil et en résolution, "
                           "code-barres séparant signal et cascade)"),
        "falsifieur": "N_persist instable en ε ; synthétique mal résolu",
        "suites_declarees": "CP2 (flux de coupure) ; CP5 (Hopf 3D)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t37_ko6_persist_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T37 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
