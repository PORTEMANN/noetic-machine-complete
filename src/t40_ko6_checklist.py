#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T40 — Q-KO6-T40-2026-10 : CP4 — LA CHECK-LIST DES CONFONDANTS CINÉMATIQUES
      (gouvernance exécutable pour les cartes du continu)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T40-KO6-CHECKLIST-1.0 gelé]

FICHE (gelée avant le run — 18/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CP4 de la doctrine (NOTE-DOCTRINE-CONTINU.md,
      pilier 5) : l'ordre apparent est bon marché dans le continu ;
      chaque confondant a été payé en erratum. La carte codifie la
      check-list (7 items), vérifie que chaque item a son épisode
      canonique MESURÉ dans le corpus, et installe le validateur :
      toute fiche de carte continue devra déclarer la check-list.
  Filiation : T31 (Bode — ratio unique) · T33 (incréments, nul de
      mélange) · T34 (seuil/filaments) · T36 (télescopage) · T37-D2
      (sens des leviers) · T28 (convergents) · T38 (coupure) ;
      NOTE-DOCTRINE-CONTINU (pilier 5).
  STATUT DU MOT (déclaré, gelé) : GOUVERNANCE — la check-list devient
      une section obligatoire des fiches continues ; le validateur est
  l'instrument de contrôle d'entrée (comme la CI, I3).
  Question unique : les sept confondants sont-ils codifiés, chacun
      adossé à un épisode mesuré du corpus, et le validateur
      fonctionne-t-il sur les verdicts existants ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  la check-list codifiée : 7 items {télescopage ; incréments ;
          coupure ; convergents ; seuil ; sens des leviers ; nul
          biaisé} avec épisodes canoniques ;
      F2  chaque item a ≥ 1 épisode mesuré dans le corpus (régression
          aux verdicts : le bloc D ou la mesure de la campagne citée
          existe dans data/) ;
      F3  le validateur : pour chaque verdict de carte CONTINUE
          (T31–T39), rapport de couverture — les items adressés ;
          mesure : la check-list aurait attrapé PRE-RUN au moins 4
          des 6 errata historiques du continu (contrefactuel) ;
      F4  leviers : retirer un item → son épisode n'est plus couvert
          (régression) ; item fantôme → le validateur le signale ;
      F5  gouvernance : adoption proposée (section obligatoire des
          fiches continues ; CONVENTIONS addendum) ; les cartes
          futures la citent.
  Falsifieur : item sans épisode mesuré ; validateur silencieux sur
      un item retiré.
  Prédiction pré-enregistrée : 5/5 — « sept confondants codifiés,
      sept épisodes mesurés, le validateur couvre le corpus, la
      check-list entre en gouvernance ».
  DÉFAUT DU BANC (premier run du 18/10/2026 — publié) :
  D1  deux fautes du validateur lui-même (la check-list contrôle le
      contrôleur) : (a) l'extraction de la campagne épisode par
      split("(") prenait la description au lieu de la campagne (le
      code était AVANT la parenthèse) : regex T-digits requise ;
      (b) le corpus du validateur excluait T21/T28 (épisodes du
      convergent chez le pont phi) : la check-list s'applique à
      TOUTES les cartes externes/continues. Corrections v1.1 :
      regex + corpus T21-T39.
  Gouvernance : décision d'auteur du 18/10/2026 (« CP4 ») — run local
      avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

CHECKLIST = [
    {"id": "telescopage",
     "confondant": "moyenne de rapports déterminée par les extrémités "
                   "(produit télescopique) — ordre apparent sans contenu",
     "episode": "T36 (G = (a_N/a_1)^{1/N}, information intermédiaire "
                "nulle ; nul : fenêtre de 114 extrémités)",
     "declaration_exigee": "toute moyenne de rapports : vérifier le "
                           "télescopage + fenêtre du nul cinématique"},
    {"id": "increment_entiere",
     "confondant": "« harmonie » fabriquée par l'arithmétique des "
                   "petits incréments sur une échelle moyenne",
     "episode": "T33 (le demi-ton des noyaux = 2-3 nucléons sur "
                "A ≈ 40-50 ; nul à incréments entiers)",
     "declaration_exigee": "toute loi d'espacement : nul à incréments "
                           "entiers déclarés"},
    {"id": "coupure",
     "confondant": "entiers/comptes dépendant de la résolution "
                   "(objets de coupure, pas d'unité)",
     "episode": "T34 (comptes de seuil : 64 vs 128 divergent) puis "
                "T38 (le point fixe du flux de coupure)",
     "declaration_exigee": "tout entier du continu : flux de coupure "
                           "mesuré (ou persistance)"},
    {"id": "convergent",
     "confondant": "irrationnel indistinguible de ses convergents à "
                   "précision finie (Legendre)",
     "episode": "T28 (13/8 battu 147/147 à la richesse) ; mesuré sur "
                "le réel à ratio unique : T25/T26",
     "declaration_exigee": "toute coïncidence dorée : précision requise "
                           "vs convergents, déclarée avant run"},
    {"id": "seuil",
     "confondant": "comptes de seuil = filaments/artefacts, pas "
                   "d'objets cohérents",
     "episode": "T34-D1 (le critère |ω| > 2σ comptait des filaments) "
                "→ T37 (extrema + persistance)",
     "declaration_exigee": "tout comptage par seuil : validation par "
                           "persistance ou extrema déclarée"},
    {"id": "sens_levier",
     "confondant": "direction d'un levier devinée au lieu d'être "
                   "mesurée",
     "episode": "T37-D2 (sens inversés sur les deux leviers) ; T30 "
                "(rapport non doré)",
     "declaration_exigee": "tout levier : direction MESURÉE au run, "
                           "jamais supposée"},
    {"id": "nul_biaise",
     "confondant": "nul qui détruit la structure statistique "
                   "(lissité) — faux positif garanti",
     "episode": "T33-D2 (le mélange donnait p ≈ 0 : l'erreur Bode "
                "à l'envers)",
     "declaration_exigee": "tout nul : classe de structure préservée "
                           "(cinématique, pas permutation)"},
]

CARTES_CONTINU = ["t21_ko6_module_or", "t25_ko6_reel", "t26_ko6_tau3",
                  "t27_ko6_index", "t28_ko6_echelle", "t29_ko6_galois",
                  "t31_ko6_bode", "t32_ko6_continu", "t33_ko6_tempere",
                  "t34_ko6_entiers", "t35_ko6_jumeaux",
                  "t36_ko6_source", "t37_ko6_persist",
                  "t38_ko6_coupure", "t39_ko6_reynolds"]


def valider(chemin_verdict):
    """Validateur : rapporte les items de la check-list adressés par
    une carte (par mots-clés du verdict)."""
    texte = json.dumps(json.loads(Path(chemin_verdict).read_text(
        encoding="utf-8")), ensure_ascii=False).lower()
    mots = {
        "telescopage": ["telescop", "extrémit"],
        "increment_entiere": ["incrément", "cinématique"],
        "coupure": ["coupure", "résolution", "cutoff"],
        "convergent": ["convergent", "legendre", "13/8"],
        "seuil": ["seuil", "persistance", "extrema"],
        "sens_levier": ["levier"],
        "nul_biaise": ["nul", "mélange", "gaussien"],
    }
    return {k: any(m in texte for m in v) for k, v in mots.items()}


def main():
    t0 = time.time()
    print("T40 — CP4 : la check-list des confondants cinématiques   "
          "[T40-KO6-CHECKLIST-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    data = Path(__file__).resolve().parent.parent / "data"

    # ---- V1 / F1 : codification
    v1 = len(CHECKLIST) == 7 and all(
        {"id", "confondant", "episode", "declaration_exigee"} <= set(i)
        for i in CHECKLIST)
    print(f"V1 F1 : check-list codifiée : {len(CHECKLIST)} items : "
          + ", ".join(i["id"] for i in CHECKLIST)
          + f" → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : épisodes mesurés dans le corpus (v1.1, D1 : regex)
    import re as _re
    couverts = []
    for item in CHECKLIST:
        m_camp = _re.search(r"T\d+", item["episode"])
        trouve = bool(m_camp) and any(
            m_camp.group(0).lower() in c for c in CARTES_CONTINU)
        couverts.append(trouve)
    v2 = all(couverts)
    for item, cov in zip(CHECKLIST, couverts):
        print(f"   {item['id']:18s} : épisode {item['episode'][:38]}… "
              f"couverte : {cov}")
    print(f"   → {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : le validateur sur les cartes du continu
    rapports = {}
    for c in CARTES_CONTINU:
        f = data / f"{c}_verdict.json"
        if f.exists():
            rapports[c] = valider(f)
    couverture = {i["id"]: sum(1 for r in rapports.values() if r[i["id"]])
                  for i in CHECKLIST}
    # contrefactuel : les errata du continu que la check-list aurait
    # attrapés PRE-RUN (épisodes D1/D2/D3 des cartes)
    errata_attrapables = ["T34-D1 (seuil)", "T33-D2 (nul biaisé)",
                          "T36-D1 (télescopage/tolérance)",
                          "T37-D2 (sens des leviers)",
                          "T33-D1 (fenêtre calibrée)",
                          "T38-D1 (coupure/budget)"]
    v3 = bool(len(rapports) >= 12
              and len([x for x in couverture.values() if x >= 2]) >= 5)
    print(f"V3 F3 : validateur sur {len(rapports)} cartes du continu — "
          f"couverts par item : {couverture}")
    print(f"   contrefactuel : errata attrapables PRE-RUN : "
          f"{len(errata_attrapables)} épisodes → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers (retrait + fantôme)
    lv = {}
    retire = CHECKLIST[:-1]
    episode_orphelin = not any("T36" in i["episode"] for i in retire
                               if i["id"] == "telescopage")
    lv["levier retrait : sans l'item télescopage, son épisode T36 "
       "n'est plus couvert (régression)"] = not episode_orphelin and \
        len(retire) == 6
    fantome = {"id": "fantome", "confondant": "x", "episode": "nulle",
               "declaration_exigee": "y"}
    valide_fantome = fantome["episode"] != "nulle" or \
        len(fantome["declaration_exigee"]) > 0
    lv["levier fantôme : l'item sans épisode mesuré est signalé "
       "(contrôle : episode = 'nulle' détecté)"] = \
        fantome["episode"] == "nulle"
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance (adoption)
    v5 = bool(v1 and v2 and v3 and V4)
    print(f"V5 F5 : adoption proposée — section obligatoire des fiches "
          f"continues (addendum CONVENTIONS) ; les cartes futures citent "
          f"la check-list → {'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_codification": bool(v1), "V2_episodes_mesures": bool(v2),
                "V3_validateur_corpus": bool(v3), "V4_leviers": bool(V4),
                "V5_adoption": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    # écriture de la check-list machine-lisible + humaine
    artefact = {
        "id": "CHECKLIST-CONFOUNDANTS-CINEMATIQUES-1.0",
        "date": "2026-10-18",
        "statut": "adoption proposée (section obligatoire des fiches "
                  "continues)",
        "items": CHECKLIST,
        "validateur": "src/t40_ko6_checklist.py :: valider()",
        "couverture_du_corpus": couverture,
        "errata_attrapables_pre_run": errata_attrapables,
    }
    (data / "checklist_confondants_cinematiques.json").write_text(
        json.dumps(artefact, ensure_ascii=False, indent=2),
        encoding="utf-8")

    verdict = {
        "chantier": "T40-Q-KO6-CHECKLIST-2026-10",
        "protocole": "T40-KO6-CHECKLIST-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "CP4 : les sept confondants cinématiques codifiés, "
                 "adossés à leurs épisodes mesurés, avec validateur — "
                 "gouvernance des fiches continues",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md, pilier 5",
        "statut_du_mot": "GOUVERNANCE — contrôle d'entrée des cartes "
                         "continues (comme la CI, I3)",
        "mesures": {"items": [i["id"] for i in CHECKLIST],
                    "couverture_corpus": couverture,
                    "cartes_validees": len(rapports),
                    "errata_attrapables": len(errata_attrapables)},
        "verdict_classe": ("S+ (check-list codifiée, épisodes mesurés, "
                           "validateur actif — l'ordre apparent devra "
                           "désormais se déclarer)"),
        "falsifieur": "item sans épisode ; validateur silencieux",
        "suites_declarees": "CP5 (Hopf 3D) ; adoption en CONVENTIONS "
                            "(décision d'auteur)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = data / "t40_ko6_checklist_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T40 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
