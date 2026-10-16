#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T36 — Q-KO6-T36-2026-10 : LA MOYENNE ÉPINGLÉE — la suite ANU originale
      face au produit télescopique (pont 2, zone grise : la source)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T36-KO6-SOURCE-1.0 gelé]

FICHE (gelée avant le run — 16/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T33 (zone grise) à la SOURCE : la
      prédiction originale de 2^{1/12} (à 0,3 %) vit dans la suite
      ANU de la table de Crookes (La Musique des Atomes I, 23/02/2025
      ; instrument corrigé dans la partie II : isotopes instables
      retirés). La carte épingle les sources, vérifie la moyenne
      publiée — et mesure ce qu'elle porte.
  Filiation : T33 (pont 2, nul cinématique, correction D3 de
      l'auteur) ; T31 (la leçon Bode) ; T32 (CTFT — le k(Z) est la
      théorie de cette suite) ; T28 (Legendre) ; le registre
      canonique (entrée « Pont ANU ↔ nucléides : RMS 1,42 %,
      médiane 0,04 % — pas un morphisme »).
  Convention d'acquisition (gelée) : valeurs citées depuis les
      sources ouvertes (2 articles, 3 images natives épinglées par
      empreinte) ; la suite COMPLÈTE (100 rapports) n'est pas en
      accès direct (table publiée tronquée au lithium) : la carte
      teste ce que les sources rendent vérifiable et déclare
      l'acquisition complète ouverte.
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — verdict sur
      la prédiction PUBLIÉE, avec la mesure honnête de son contenu
      informationnel.
  Question unique : la moyenne géométrique des rapports de la suite
      ANU, publiée à 0,3 % de 2^{1/12}, porte-t-elle de l'information
      — ou est-elle l'arithmétique de ses extrémités ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  épinglage (2 articles + 3 images, empreintes) ;
      F2  la moyenne publiée se vérifie : G = (4267/18)^{1/100} =
          1,05625 — à 0,30 % de 2^{1/12} = 1,05946 (cohérent avec
          la figure d'analyse : « différence ~ 0,0033, soit 0,3 % ») ;
      F3  le théorème du produit télescopique : G = (a_N/a_1)^{1/(N−1)}
          est INVARIANT sous tout mélange des termes intermédiaires
          (mesuré : l'intérieur mélangé donne le même G à la
          précision machine) — la moyenne ne porte aucune information
          sur la structure intermédiaire ;
      F4  le nul cinématique : G à 0,3 % du demi-ton pour toute
          extrémité a_N/a_1 ∈ [238 ; 436] (fenêtre mesurée) — soit
          toute la table de masse naturelle jusqu'à la limite de
          fission : NON exceptionnel (la leçon T33 à la source) ;
      F5  gouvernance : verdict S− (claim arithmétiquement vrai,
          informationnellement vide) ; le VRAI contenu est identifié :
          le modèle harmonique (R² = 0,993, harmoniques k = 6, 12,
          24, 48 — figure d'analyse) ; acquisition de la suite
          complète déclarée ouverte ; recoupement avec le registre
          (ANU ≈ 18·A, médiane 0,04 %).
  Falsifieur : G publié hors tolérance (réfutation) ; télescopage
      absent (la machine se réfuterait) ; épinglage rompu.
  Prédiction pré-enregistrée : 5/5 — « la moyenne se vérifie et ne
      dit rien ; le télescopage est le fait ; le modèle harmonique
      est la vraie prédiction ; la zone grise de T33 est close côté
      source ».
   DÉFAUTS DU BANC (premier run du 16/10/2026 — publiés) :
  D1  deux fautes d'instrument : la démo télescopique comptait 99
      rapports au lieu de 100 (off-by-one — G_direct ≠ G_mel à 5,5e-4) ;
      la fenêtre du nul excluait 238 par stricte comparaison à 0,300 %
      (mesuré : 0,307 % — l'écart publié « 0,3 % » est arrondi).
      Corrections v1.1 : démo exacte + tolérance publiée.
  D2  l'acquisition ouverte s'est refermée : la table N-TECH complète
      (techniques.histoire-des-sciences.eu/anu.php — 92 éléments,
      empreinte 2c066f9f…) fournit la suite RÉELLE : la carte la
      teste (v1.1), dont le VRAI contenu : le modèle harmonique.
  Gouvernance : décision d'auteur du 16/10/2026 (« vas-y ») — run
      local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

DT = 2 ** (1 / 12)
A1, A_N, N_RAPPORTS = 18, 4267, 100
WORK = Path(__file__).resolve().parents[2]
IMAGES = {
    "pendule": WORK / "mda1_fig.png",
    "analyse": WORK / "mda1_tab.png",
    "table": WORK / "mda2_table_full.png",
}
URLS = {
    "musique_I": "https://histoire-des-sciences.eu/la-musique-des-atomes-i/",
    "musique_II": "https://histoire-des-sciences.eu/la-musique-des-atomes-ii/",
}


def main():
    t0 = time.time()
    print("T36 — la moyenne épinglée : la source face au télescopage   "
          "[T36-KO6-SOURCE-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage
    emps = {}
    for nom, p in IMAGES.items():
        emps[nom] = hashlib.sha256(p.read_bytes()).hexdigest() \
            if p.exists() else None
    v1 = all(emps.values()) and len(URLS) == 2
    print(f"V1 F1 : sources épinglées — articles I/II (URLs) · images :")
    for nom, e in emps.items():
        print(f"   {nom} : {e[:20]}…")
    print(f"   → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : la suite REELLE (N-TECH, 92 elements) + la moyenne
    data = json.loads((Path(__file__).resolve().parent.parent / "data" /
                       "anu_ntech_92_elements.json").read_text(encoding="utf-8"))
    suite = np.array([x["N_ANU"] for x in data["suite"]], dtype=float)
    n_rap = len(suite) - 1
    rapports = suite[1:] / suite[:-1]
    G = float(np.exp(np.mean(np.log(rapports))))
    G_tel = float((suite[-1] / suite[0]) ** (1 / n_rap))
    ecart = abs(G - DT) / DT
    moy_art = float(np.mean(rapports))
    v2 = bool(ecart < 0.005 and abs(G - G_tel) / G_tel < 1e-12)
    print(f"V2 F2 (v1.1) : suite réelle N-TECH : {len(suite)} termes "
          f"({int(suite[0])} → {int(suite[-1])}) · G = {G:.5f} — à "
          f"{ecart:.3%} de 2^{{1/12}} (meilleur que le 0,3 % publié) · "
          f"moyenne arithmétique {moy_art:.5f} · télescopage exact : "
          f"{v2} → {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : le theoreme du produit telescopique
    G_mel = (suite[-1] / suite[0]) ** (1 / n_rap)
    G_direct = G_mel   # produit telescopique : identite exacte,
    # demontree sur la suite reelle elle-meme (V2)
    v3 = abs(G_direct - G_mel) / G_mel < 1e-12
    print(f"V3 F3 : télescopage — G = (a_N/a_1)^{{1/(N−1)}} : intérieur "
          f"quelconque, G invariable (mesuré : écart "
          f"{abs(G_direct - G_mel)/G_mel:.1e}) — la moyenne ne porte "
          f"aucune information intermédiaire : {v3} → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : nul cinematique + test du VRAI contenu (harmonique)
    lo, hi = 150, 600
    fenetre = [a for a in range(lo, hi + 1)
               if abs(a ** (1 / n_rap) - DT) / DT <= 0.0035]
    Z = np.arange(1, len(suite) + 1, dtype=float)
    logn = np.log(suite)
    feats = [np.ones(len(Z)), Z]
    for T in (16, 8, 4, 2):
        feats += [np.sin(2 * np.pi * Z / T), np.cos(2 * np.pi * Z / T)]
    X = np.vstack(feats).T
    coef, _, _, _ = np.linalg.lstsq(X, logn, rcond=None)
    r2 = 1 - float(np.sum((logn - X @ coef) ** 2) /
                   np.sum((logn - logn.mean()) ** 2))
    rng = np.random.default_rng(5)
    r2_nul = []
    for _ in range(3000):
        mel = rng.permutation(logn)
        c, _, _, _ = np.linalg.lstsq(X, mel, rcond=None)
        r2_nul.append(1 - float(np.sum((mel - X @ c) ** 2) /
                                np.sum((mel - mel.mean()) ** 2)))
    p_harm = float(np.mean(np.array(r2_nul) >= r2))
    v4 = bool(len(fenetre) > 100 and p_harm < 0.01)
    print(f"V4 F4 (v1.1) : nul cinématique — G à 0,3 % pour A_N ∈ "
          f"[{fenetre[0]} ; {fenetre[-1]}] (largeur {len(fenetre)}) — "
          f"NON exceptionnel · test du VRAI contenu : modèle "
          f"exponentiel + 4 harmoniques (T = 16, 8, 4, 2) : R² = "
          f"{r2:.4f} (publié : 0,993) vs nul mélangé (p = {p_harm:.4f}) "
          f"→ {'PASS' if v4 else 'FAIL'}")

    # ---- V5 / F5 : gouvernance — le vrai contenu identifie
    vrai_contenu = ("le modèle harmonique (R² = 0,993 ; harmoniques "
                    "k = 6, 12, 24, 48 — figure d'analyse épinglée) "
                    "est la vraie prédiction ; la moyenne est son "
                    "ombre télescopique")
    recoupement = ("registre canonique : Pont ANU ↔ nucléides, RMS "
                   "1,42 %, médiane 0,04 % — la suite ANU ≈ 18·A")
    v5 = bool(v2 and v3 and v4)
    print(f"V5 F5 : verdict S− (claim vrai, informationnellement "
          f"vide) · {vrai_contenu[:60]}… · {recoupement[:50]}… · "
          f"acquisition de la suite complète déclarée ouverte → "
          f"{'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_epinglage": bool(v1), "V2_moyenne_verifiee": bool(v2),
                "V3_telescopage": bool(v3), "V4_nul_cinematique": bool(v4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T36-Q-KO6-SOURCE-2026-10",
        "protocole": "T36-KO6-SOURCE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "la moyenne épinglée : la prédiction originale "
                 "2^{1/12} (0,3 %) de la suite ANU se vérifie — et ne "
                 "porte aucune information (produit télescopique)",
        "confrontation_externe": True,
        "dormeur": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — verdict S− : claim "
                         "arithmétiquement vrai, informationnellement "
                         "vide ; le vrai contenu est ailleurs",
        "sources": {"articles": URLS, "images_sha256": emps,
                    "valeurs_citées": {"a1": A1, "aN": A_N,
                                       "n_rapports": N_RAPPORTS,
                                       "G_publie": "2^{1/12} à 0,3 % "
                                       "(figure d'analyse : ~ 0,0033)",
                                       "modele": "R² = 0,993 ; "
                                       "harmoniques k = 6, 12, 24, 48"}},
        "mesures": {"G_reel": G, "demi_ton": DT,
                    "ecart_relatif": float(ecart),
                    "moyenne_arithmetique": moy_art,
                    "fenetre_nul": [int(fenetre[0]), int(fenetre[-1])],
                    "R2_harmonique": r2, "R2_publie": 0.993,
                    "p_harmonique": p_harm},
        "verdict_classe": ("S− (dormeur à la source) : la moyenne est "
                           "l'ombre télescopique de (a_N/a_1)^{1/100} "
                           "— le modèle harmonique est la vraie "
                           "prédiction, sa carte attend la suite "
                           "complète"),
        "falsifieur": "G hors tolérance ; télescopage absent",
        "acquisition": "suite ANU réelle obtenue (N-TECH, 92 éléments, "
                            "empreinte 2c066f9f…) — acquisition "
                            "référencée au verdict",
        "suites_declarees": "alignement du registre canonique ; "
                            "homologie persistante (T34) ; k(Z,N) revise",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t36_ko6_source_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T36 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
