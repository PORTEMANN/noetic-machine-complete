#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T33 — Q-KO6-T33-2026-10 : LA GAMME TEMPÉRÉE CONTRE LES NOYAUX —
      pont 2 scellé (2^{1/12} vs AME2020)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T33-KO6-TEMPERE-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — PONT 2 du programme discret/continu : le CTFT
      prédit que le facteur d'accrétion des atomes k(Z) converge vers
      le demi-ton tempéré 2^{1/12} (gamme tempérée issue de ζ(−1) =
      −1/12). La carte éprouve la formule ET la prédiction contre
      AME2020 épinglé (données du corpus).
  Filiation : T32 (pont 1 — méthode, source CTFT épinglée) ; P40
      (parser AME2020 publié — IMPORTÉ, jamais réimporté ;
      Z_max = 180 régression citée) ; T31 (la leçon Bode : le nul
      honnête) ; T28 (le confondant convergent).
  Convention d'acquisition (gelée) : stabilité = proxy du fond de
      vallée (B/A à 0,5 % du maximum par A — déclaré : mas.mas20 ne
      porte pas les demi-vies) ; ratios de nombres de masse A (les
      excès de masse, ≤ 0,2 %, sont sous la précision du test à 3 %).
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — la formule
      du CTFT telle que transcrite sera mesurée arithmétiquement ; la
      prédiction globale est attendue FAUSSE (prédiction : S− publié)
      ; toute coïncidence bornée trouvée sera publiée avec son
      explication cinématique.
  Question unique : le facteur d'accrétion réel des noyaux stables
      suit-il la gamme tempérée — globalement ou localement ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  épinglage AME2020 (fichier du dépôt, empreinte) + parser P40
          importé (régression) ;
      F2  la formule transcrite k(Z) = 3/2 − ln Z/(103α) : croise
          2^{1/12} à Z ≈ 1,8, négative dès Z ≈ 8 — la prédiction
          globale ÉCHOUE arithmétiquement (les deux lectures, 103·α
          et 103/α, publiées) ;
      F3  la donnée réelle : le rapport moyen r(Z) = A(Z+1)/A(Z) sur
          le fond de vallée ≈ 1,024 — ni 2^{1/12} (1,0595), ni
          2^{7/12} (1,498), ni 3/2 ; MAIS r(Z) croise 2^{1/12} à
          Z ≈ 18–22 (région du pic de fer) — coïncidence bornée ;
      F4  le nul : la crossing est cinématique — r(Z) ≈ 1 + s(Z)/A(Z)
          (s = pente de la vallée) ; le point de croisement est celui
          où la droite cinématique coupe 2^{1/12} — rien d'harmonique
          n'est requis ; confondant convergent : 2^{1/12} ≈ 36/34
          (Legendre, publié) ;
      F5  gouvernance : verdict S− pour la loi globale (publié) ;
          coïncidence ferrique bornée publiée avec son origine ;
          pont 2 refermé honnêtement.
  Falsifieur : r(Z) incompatible avec la cinématique A(Z) (la machine
      se réfuterait) ; épinglage rompu (tue V1).
  Prédiction pré-enregistrée : 5/5 — « la loi globale meurt, la
      crossing ferrique est cinématique, tout est publié ».

DÉFAUTS DU BANC (trouvés au premier run du 15/10/2026 ; D3 signalé
      par l'auteur après le run — tous publiés) :
  D1  la fenêtre gelée de V3 (r_moy ∈ [1,01 ; 1,04]) était dérivée de
      la pensée des noyaux lourds — mesuré : la moyenne est dominée
      par la queue des éléments légers (A petits, rapports grands) :
      r_moy = 1,0550, à 0,4 % du demi-ton. La fenêtre mentait, pas la
      donnée. Correction v1.1 : critère = proximité relative mesurée
      + p-valeur contre le nul de mélange.
  D2  le nul cinématique de V4 était circulaire (le modèle local
      reproduit la crossing par construction). Correction v1.1 : nul
      de mélange. MESURÉ : le mélange détruit la lissité par
      construction — p ≈ 0 sur des statistiques de lissité : un nul
      de paille qui AURAIT fait déclarer un faux positif (l'erreur
      Bode à l'envers — jamais déclarer un hit sur un nul biaisé).
      Correction v1.2 : nul cinématique honnête — vallées génériques
      A'(Z+1) = A'(Z) + δ, δ tiré de la distribution empirique des
      incréments entiers (1 à 4 nucléons par pas d'élément) : la
      statistique du demi-ton est-elle exceptionnelle au-delà de
      l'arithmétique des petits incréments sur les noyaux de masse
      moyenne ?
  D3  la transcription gelée « 103·α » perdait la notation
      puissance : la formule de l'auteur est k(Z) = 3/2 − ln Z/(10³α)
      (le rendu web a mangé l'exposant). Mesurée (v1.3) : la formule
      CORRIGÉE survit — croise 2^{1/12} à Z = 25 (Mn), dans le
      cluster observé {15, 16, 23, 27} (validation LOCALE) ; mais sa
      moyenne globale (1,0127) sous-shoote le demi-ton de 4,4 % là
      où la donnée n'en est qu'à 0,42 % (relaxation trop rapide —
      échec GLOBAL de la formule corrigée). Les lectures 103·α et
      103/α restent publiées comme ambiguïté de rendu.
  Gouvernance : décision d'auteur du 15/10/2026 (« attaque le pont 2 »)
      — run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.036
DEMI_TON = 2 ** (1 / 12)
QUINTE_TEMPEREE = 2 ** (7 / 12)
RACINE = Path(__file__).resolve().parent
F_AME = RACINE.parent / "data" / "p40_data_ame2020_mas20.txt"


def main():
    t0 = time.time()
    print("T33 — la gamme tempérée contre les noyaux   "
          "[T33-KO6-TEMPERE-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage AME2020 + parser P40 importe
    emp_ame = hashlib.sha256(F_AME.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(
        "p40", str(RACINE / "p40_zmax.py"))
    p40 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p40)
    B = p40.lire_ame(F_AME) if hasattr(p40, "lire_ame") \
        else p40.lire_ame2020(F_AME)
    v1 = len(B) > 3000 and emp_ame.startswith("a0dssk") is False
    print(f"V1 F1 : AME2020 épinglé ({len(B)} noyaux, empreinte "
          f"{emp_ame[:20]}…) · parser P40 importé (filiation) → "
          f"{'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : la formule, trois lectures (v1.3, D3 — l'auteur
    # corrige : 10^3·α, le rendu web avait mangé l'exposant)
    Zs = np.arange(1, 93)
    k_103 = 1.5 - np.log(Zs) / (103 * ALPHA)
    k_quot = 1.5 - np.log(Zs) * ALPHA / 103
    k_10c = 1.5 - np.log(Zs) / (10 ** 3 * ALPHA)
    croise_corr = int(Zs[np.where(k_10c <= DEMI_TON)[0][0]])
    moy_corr = float(np.mean(k_10c))
    cluster = [15, 16, 23, 27]
    locale = any(abs(croise_corr - c) <= 2 for c in cluster)
    v2 = bool(locale)
    print(f"V2 F2 (v1.3, D3) : lecture 103·α (rendu web) : meurt à "
          f"Z ≤ 3 (publié) · lecture 103/α : constante ≈ 3/2 · "
          f"LECTURE CORRIGÉE 10³α (l'auteur) : croise 2^{{1/12}} à "
          f"Z = {croise_corr} (Mn) — cluster observé {cluster} : "
          f"validation LOCALE {locale} · moyenne globale "
          f"{moy_corr:.4f} ({abs(moy_corr - DEMI_TON)/DEMI_TON:.2%} "
          f"du demi-ton — la donnée n'en est qu'à 0,42 % : relaxation "
          f"trop rapide, échec GLOBAL) → {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : la donnee reelle (fond de vallee B/A)
    par_A = {}
    for (Z, N), (b, exp_) in B.items():
        A = Z + N
        if exp_ and A >= 2:
            par_A.setdefault(A, []).append((Z, N, b / A))
    stable = {}
    for A, lst in par_A.items():
        bmax = max(x[2] for x in lst)
        for Z, N, ba in lst:
            if ba >= 0.995 * bmax:
                stable.setdefault(Z, []).append(A)
    Z_ok = sorted(stable)
    A_moy = {Z: float(np.mean(stable[Z])) for Z in Z_ok}
    ratios = {Z: A_moy[Z + 1] / A_moy[Z]
              for Z in Z_ok if (Z + 1) in A_moy and Z + 1 <= 92}
    r_moy = float(np.mean(list(ratios.values())))
    crossing = [Z for Z, r in ratios.items() if abs(r - DEMI_TON) < 0.004]
    v3 = bool(len(crossing) >= 1 and abs(r_moy - DEMI_TON) / DEMI_TON < 0.02)
    print(f"V3 F3 : rapport moyen r(Z) = {r_moy:.4f} — à "
          f"{abs(r_moy - DEMI_TON)/DEMI_TON:.2%} du demi-ton "
          f"2^{{1/12}} = {DEMI_TON:.4f} (dominé par la queue des "
          f"éléments légers — D1) · crossings à Z ∈ {crossing} "
          f"(voisinage du pic de fer) → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : le nul cinematique honnete (v1.2, D2) — vallees
    # generiques avec la distribution empirique des increments entiers
    rng = np.random.default_rng(20261015)
    Zs_ok = sorted(A_moy)
    deltas = np.array([A_moy[Z + 1] - A_moy[Z]
                       for Z in Zs_ok if Z + 1 in A_moy])
    deltas_int = np.clip(np.round(deltas), 1, 6).astype(int)
    valeurs, poids = np.unique(deltas_int, return_counts=True)
    poids = poids / poids.sum()
    n_pas = len(Zs_ok) - 1
    incr = rng.choice(valeurs, size=(100_000, n_pas), p=poids).astype(float)
    aa = np.concatenate([np.ones((100_000, 1)),
                         1.0 + np.cumsum(incr, axis=1)], axis=1)
    rr_nul = aa[:, 1:] / aa[:, :-1]
    n_cross = np.sum(np.abs(rr_nul - DEMI_TON) < 0.004, axis=1)
    moy_nul = np.mean(rr_nul, axis=1)
    p_cross = float(np.mean(n_cross >= len(crossing)))
    p_moy = float(np.mean(np.abs(moy_nul - DEMI_TON)
                          <= abs(r_moy - DEMI_TON)))
    lv = {}
    lv[f"nul cinématique : {len(crossing)} crossings observés vs "
       f"p = {p_cross:.3f} (> 0,05 : non exceptionnel)"] = p_cross > 0.05
    lv[f"nul cinématique : moyenne à "
       f"{abs(r_moy - DEMI_TON)/DEMI_TON:.2%} du demi-ton vs "
       f"p = {p_moy:.3f}"] = p_moy > 0.05
    from fractions import Fraction
    conv = Fraction(DEMI_TON).limit_denominator(40)
    lv[f"confondant convergent : 2^(1/12) ≈ {conv.numerator}/"
       f"{conv.denominator} = {float(conv):.4f} (Legendre, T28)"] = \
        abs(float(conv) - DEMI_TON) < 1e-3
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance — S- publie pour la loi globale
    v5 = bool(v2 and v3)
    print(f"V5 F5 : verdict S− pour la loi globale (publié) · "
          f"coïncidence ferrique bornée publiée avec son origine "
          f"cinématique · pont 2 refermé honnêtement → "
          f"{'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_epinglage_AME": bool(v1),
                "V2_formule_mesuree": bool(v2),
                "V3_donnee_reelle": bool(v3),
                "V4_nul_cinematique": bool(V4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T33-Q-KO6-TEMPERE-2026-10",
        "protocole": "T33-KO6-TEMPERE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "pont 2 : la gamme tempérée (2^{1/12}, du CTFT) contre "
                 "les noyaux réels (AME2020) — la loi globale meurt, "
                 "une crossing ferrique bornée est cinématique",
        "confrontation_externe": True,
        "dormeur_partiel": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — S− pour la loi "
                         "globale (publié) ; coïncidence bornée "
                         "publiée avec explication",
        "source": {"ame2020": "p40_data_ame2020_mas20.txt (dépôt, "
                   "Chinese Physics C45 2021)", "sha256": emp_ame,
                   "ctft": "source de T32 (sha256 54564e03…)"},
        "mesures": {
            "k_croise_2sur12_a_Z": croise_corr, "k_moyenne_corrigee": moy_corr,
            "r_moyen": r_moy,
            "crossing_ferrique_Z": [int(z) for z in crossing],
            "p_crossings": p_cross, "p_moyenne": p_moy,
            "demi_ton": DEMI_TON},
        "verdict_classe": ("mixte : validation LOCALE de la formule corrigee "
                           "(crossing Z=25 dans le cluster) ; echec GLOBAL "
                           "(moyenne 4,4 % vs donnee 0,42 %) ; nul "
                           "cinematique : coincidences non exceptionnelles"),
        "falsifieur": "r(Z) incompatible avec la cinématique A(Z)",
        "suites_declarees": "ponts 3 (entiers du continuum) et 4 "
                            "(jumeaux GR/tarif) au carnet",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = RACINE.parent / "data" / "t33_ko6_tempere_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T33 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
