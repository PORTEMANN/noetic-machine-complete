#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A4 — REGISTRE DES FRONTIÈRES MESURÉES
=====================================
Amélioration de méthode : la frontière devient un objet de première classe.
Jusqu'ici, les frontières du corpus étaient dispersées dans les verdicts
(B3-FAIL, partiels, déclarations). A4 les registre à discipline ash-corpus :
schéma déclaré, SHA-256 par entrée et global, statuts fermés, coût de
fermeture exact — falsifiable entrée par entrée.

Protocole gelé REG-FR-1.0
  1. Schéma déclaré (toute entrée invalide = B3-FAIL du registre) :
     id, type (physique/méthode/hygiène), énoncé, chantier_source, protocole,
     statut ∈ {ouverte, partielle, fermée}, coût_de_fermeture_exact,
     comptage_ddll (verdict sur les degrés de liberté : déficit / mode non
     contraint / hors-domaine, avec justification mesurée), artefacts,
     falsifieur propre.
  2. Une frontière n'entre au registre que si elle a été MESURÉE (verdict
     d'un chantier exécuté) — pas de frontière déclarée sans artefact.
  3. Le registre sert d'entrée à A5 (conjecture des frontières) : le
     comptage_ddll est la seule donnée que A5 agrège.
"""

import hashlib
import json
from pathlib import Path

SCHEMA = ["id", "type", "énoncé", "chantier_source", "protocole", "statut",
          "coût_de_fermeture_exact", "comptage_ddll", "artefacts", "falsifieur"]
STATUTS = {"ouverte", "partielle", "fermée"}
TYPES = {"physique", "méthode", "hygiène"}


def entree(id, type_, enonce, source, protocole, statut, cout, ddll, artefacts,
           falsifieur):
    e = {"id": id, "type": type_, "énoncé": enonce, "chantier_source": source,
         "protocole": protocole, "statut": statut,
         "coût_de_fermeture_exact": cout, "comptage_ddll": ddll,
         "artefacts": artefacts, "falsifieur": falsifieur}
    blob = json.dumps(e, ensure_ascii=False, sort_keys=True).encode()
    e["sha256_entrée"] = hashlib.sha256(blob).hexdigest()
    return e


FRONTIÈRES = [
    entree(
        "F1-XOR", "physique",
        "XOR et XNOR inséparables par un neurone formel unique (hyperplan + seuil)",
        "P34-NEURONE", "LP-SEP-1.0", "fermée",
        "+1 couche cachée : 2 neurones, poids ENTIERS dérivés "
        "(h1=[x1−x2≥1], h2=[x2−x1≥1], sortie OU) — coût exact mesuré",
        {"verdict": "déficit",
         "justification": "1 hyperplan → 2 hyperplans : la fermeture ajoute "
                          "une dimension de séparation (couche cachée)"},
        {"script": "p34_neurone.py", "verdict": "p34_neurone_verdict.json"},
        "toute paire (w,b) séparant XOR avec marge > 0 tue la frontière"),
    entree(
        "F2-SIGMA-DYNAMIQUE", "physique",
        "le neurone formel σ(w·x+b) est réfuté comme modèle du neurone "
        "biologique (tout-ou-rien, train, f–I discontinue, état)",
        "P35-NEURONE-BIOLOGIQUE", "HH-VER-1.0", "fermée",
        "de 0 variable d'état à 2 (Izhikevich, plan) ou 1 sur S¹ "
        "(theta-neuron) — l'excitabilité minimale est une phase sur un cercle",
        {"verdict": "déficit",
         "justification": "0D → 2D plan ou 1D sur S¹ : la fermeture ajoute "
                          "des dimensions d'état (la DYNAMIQUE était le "
                          "constitutif manquant)"},
        {"script": "p35_neurone_biologique.py",
         "verdict": "p35_neurone_biologique_verdict.json"},
        "toute expérience à entrée constante dont la sortie biologique est "
        "statique tue la frontière"),
    entree(
        "F3-R12-PORTEE", "physique",
        "r₁₂ : contact (cusp de Kato, c=1/2) dérivable ; portée du facteur à "
        "deux corps. FERMÉE par P39 (2026-08-30) : à l'intégrateur complet "
        "(forme |∇Ψ|², grille corpus 300×192), la règle de densité "
        "β = 0.42ζ₀ (F1×R3, zéro paramètre) bat la référence split-ζ en TOUT "
        "Z mesuré — Z=2..6 (+18.5→19.4 mHa, constant), Z=7..10 (+19.3 mHa), "
        "H⁻ (+17.2 mHa), Ps⁻ (+3.7 mHa) ; F2×R1/R2/R3 passent aussi 5/5 "
        "(gains jusqu'à 43 mHa). Le verdict P31 « portée non dérivable » "
        "était un artefact : son intégrande mélangeait deux formes IBP "
        "(distorsion mesurée jusqu'à +0.13 Ha, gain écrasé ×5). La loi P32 "
        "« R3 ne gagne qu'en Z=2 » était la signature du domaine de "
        "l'intégrateur delta, pas de la physique",
        "P39-FERMETURE-R12", "R12-FERM-1.0", "fermée",
        "coût payé et mesuré : reconstruction de l'intégrateur complet en "
        "forme |∇Ψ|² (0.7 s/évaluation, volet A : 1444 s) + correction de "
        "l'intégrande P31 (publiée en B3-FAIL corpus) ; la fermeture est la "
        "règle de densité du corpus elle-même, sans paramètre",
        {"verdict": "déficit (confirmé et fermé)",
         "justification": "le degré de liberté manquant était bien le "
                          "2-corps r₁₂ (déficit 1 corps → 2 corps) : une fois "
                          "l'intégrateur corrigé, la portée se DÉRIVE (règle "
                          "de densité) sans paramètre — le déficit se ferme "
                          "par l'ajout du ddll, comme v2 le prédit"},
        {"script": "p39_fermeture_r12.py",
         "verdict": "p39_fermeture_r12_verdict.json",
         "b3_fail_corpus": "intégrande P31 (mélange de formes IBP) — "
                           "republication requise (voir F9)"},
        "toute exécution de R12-FERM-1.0 donnant F1×R3 perdante en un Z du "
        "domaine variationnel rouvre la frontière"),
    entree(
        "F4-KO6-ENUMERATION", "méthode",
        "« 63 160 réalisations certifiées KO-6 » : non reproductible par son "
        "propre moteur (0 solution, plafond inatteignable, certification vide)",
        "A3-KO6-REENUMERATION", "TAMIS-KO6-1.0", "ouverte",
        "implémenter les VRAIS axiomes KO-6 au niveau des représentations "
        "(J_F²=+1, J_FD_F=D_FJ_F, (J_Fγ_F)²=−1, ordre un sur les blocs de "
        "D_F), ré-énumérer sous bornes déclarées, publier le compte",
        {"verdict": "déficit",
         "justification": "les proxys (matrices de multiplicité) sont en "
                          "déficit de structure : la fermeture exige les "
                          "objets de dimension supérieure (opérateurs J_F, "
                          "γ_F, D_F sur H_F), pas seulement leurs traces "
                          "matricielles"},
        {"script": "a3_ko6_reenumeration.py",
         "verdict": "a3_ko6_reenumeration_verdict.json"},
        "toute exécution du moteur commité (plafond retiré) produisant ≥ 1 "
        "solution tue l'entrée"),
    entree(
        "F5-BPS-ECHELLE", "physique",
        "C(ρ=0) = 1 (BPS) n'est pas atteint par relaxation sur boîte finie : "
        "à masse de Higgs nulle, le cœur délocalise jusqu'au bord",
        "A2-MOTEUR-LEVIERS", "LEV-ENG-1.0", "ouverte",
        "fixer l'échelle (mode zéro) : condition asymptotique algébrique "
        "H ~ 1 − 1/ξ imposée, ou volume infini par changement de variable "
        "compact — puis relire C(ρ→0⁺)",
        {"verdict": "mode non contraint",
         "justification": "la frontière n'est pas un déficit mais un SURPLUS "
                          "indéterminé : l'invariance d'échelle du point BPS "
                          "(mode zéro) laisse une direction sans énergie — "
                          "la relaxation la suit hors de la boîte"},
        {"script": "a2_moteur_leviers.py",
         "verdict": "a2_moteur_leviers_verdict.json"},
        "toute relaxation sur boîte finie reproduisant C(ρ=0)=1 sans "
        "fixation d'échelle tue l'entrée"),
    entree(
        "F6-COEUR-DIFFUS", "physique",
        "P9/P11 : le cœur pointu (sharp) ne reproduit pas les rayons de "
        "matière (PREX) — la diffusivité est nécessaire",
        "P9-PREX, P11-VALLEE (corpus)", "C12.1 (corpus)", "partielle",
        "ajout d'un champ de diffusivité a — fermeture partielle mesurée "
        "dans le corpus",
        {"verdict": "déficit",
         "justification": "cœur pointu (0 champ) → +1 champ diffusif a : "
                          "la fermeture ajoute un degré de liberté spatial"},
        {"scripts": "p9_prex.py, p11_vallee.py (corpus)"},
        "toute reproduction des rayons PREX avec cœur pointu sans champ "
        "additionnel tue l'entrée"),
    entree(
        "F7-PARTIELS-PROTOCOLE", "méthode",
        "P13 (stabilité) et P22 (double bêta) sont partiels — le programme A1 "
        "prédit une sensibilité au protocole non encore mesurée",
        "P13, P22 (corpus) — batterie rétroactive A1 à exécuter",
        "PERT-BATT-1.0 (application rétroactive planifiée)", "ouverte",
        "encapsuler P13/P22 en f(π) et passer la batterie A1 ; publier les "
        "couples (V, Σ)",
        {"verdict": "hors-domaine (en attente de mesure)",
         "justification": "tant que la batterie n'a pas tourné, le comptage "
                          "de ddll est indéterminé — le registre refuse les "
                          "verdicts anticipés"},
        {"pré-requis": "a1_batterie_perturbation.py"},
        "l'exécution de la batterie fixe le statut"),
    entree(
        "F8-ZMAX-E8", "physique",
        "Z_max ≈ 179 (échelle koïlon 2^(1/12), N = 12·log₂(1/α) = 120 = "
        "racines E8) : 5 prédictions — P40 a confronté aux masses mesurées : "
        "Z_max EXACT = 180 recomputé à α=2^-10 gelé (le « ≈179 » tient), "
        "cohérent avec masses+modèles (dernière coquille publiée ≤ 168) ; "
        "P-FISSION RÉFUTÉE sur JEFF-3.1.1 (0/8 pics secondaires aux A gelés "
        "{63,110,126,173}) ; P-MASS-EFF, P-ALPHA-VAR, P-KOILON-SON non "
        "confrontables aujourd'hui (discriminateurs déclarés)",
        "koilon-scale-e8 (corpus)", "ZMAX-1.0 (P40)", "partielle",
        "2/5 prédictions tranchées (Z-MAX cohérente, FISSION réfutée) ; "
        "fermeture complète exige les expériences laser, quasars et ondes "
        "gravitationnelles — discriminateurs pré-enregistrés",
        {"verdict": "déficit",
         "justification": "α_K = 2^-10 est un input payé (1 ddll) : la "
                          "fermeture causale achète son échelle"},
        {"dépôt": "github.com/PORTEMANN/koilon-scale-e8",
         "script": "p40_zmax.py",
         "verdict": "p40_zmax_verdict.json"},
        "Z_max recomputé hors {179,180} tue la dérivation ; un élément "
        "stable mesuré au-delà de Z=180 tue la prédiction ; magiques "
        "connus non récupérés tuent l'instrument"),
    entree(
        "F9-HYGIENE-P32-P33", "hygiène",
        "p32_frontiere.py / p33_queue.py publiés en base64 re-wrapé corrompu "
        "(caractères perdus aux frontières de lignes : T<=R1+R2, _ckk]) et "
        "SHA-256 non conformes au registre SHASUMS.txt. Étendu par P39 : "
        "p31_portee.py contient un intégrande cinétique défectueux (mélange "
        "de formes IBP — distorsion mesurée jusqu'à +0.13 Ha) — re-publication "
        "avec la forme |∇Ψ|² de P39",
        "audit A3 + audit P39 (2026-08-30)", "SHASUMS.txt du dépôt", "ouverte",
        "re-publier les sources Python propres (p32, p33) et corrigées (p31, "
        "forme |∇Ψ|²), régénérer les JSON/PNG, mettre SHASUMS.txt à jour — "
        "coût : une republication",
        {"verdict": "hors-domaine",
         "justification": "frontière d'hygiène de publication — aucun "
                          "comptage de degrés de liberté ne s'applique"},
        {"sha_mesurés": "p32 bbf42182… vs registre 60a868bd… ; "
                        "p33 1a4bb130… vs registre 286f9888…"},
        "des sources conformes au registre tuent l'entrée"),
    entree(
        "F10-CODE-FRACTIONNAIRE", "hygiène",
        "Topological-Fractional-AI : résultats publiés (84.1 % AUC, 28 "
        "paramètres) sans code exécutable — la signature fractionnaire "
        "(Mittag-Leffler) n'est pas rejouable",
        "audit empreinte web (2026-08-30)", "dépôt GitHub", "ouverte",
        "publier le script — coût : une republication ; la science suit. "
        "P37 (2026-08-30) fournit la première dynamique fractionnaire "
        "exécutable du corpus (E_α de Pollard contrôlée à 2.6e-16), mais ne "
        "ferme pas l'entrée : le script du modèle 84.1 % reste à publier",
        {"verdict": "hors-domaine",
         "justification": "frontière d'hygiène — pas un comptage de ddll"},
        {"dépôt": "github.com/PORTEMANN/Topological-Fractional-AI",
         "avancée": "p37_neurone_fractionnaire.py (corpus noétique, "
                    "rejouable, zéro paramètre ajusté)"},
        "un script publié et rejouable tue l'entrée"),
    entree(
        "F11-MEMOIRE-FRACTIONNAIRE", "physique",
        "P37 : le neurone fractionnaire (intégrateur ABC d'ordre α) est "
        "réfuté comme modèle du spike (superposition exacte mesurée : 0 "
        "spike sous tout courant constant) — la mémoire Mittag-Leffler "
        "n'est pas l'excitabilité. Queue algébrique t^{−α} constitutive "
        "(pentes −0.25/−0.49/−0.84 vs −α, fenêtre [20,200] ms) ; "
        "persistance mesurable à Δ=100 ms (2.6e-3) où l'exponentielle est "
        "morte (3.7e-44) ; fermeture de rang 2 refusée (erreur 0.152 sur "
        "grille déclarée) — la mémoire exacte est ∞D",
        "P37-NEURONE-FRACTIONNAIRE", "FRAC-NEU-1.0", "ouverte",
        "deux fermetures orthogonales mesurées : excitabilité = phase sur "
        "S¹ (+1 ddll, P35) ; mémoire biologique = approximation de rang "
        "fini du noyau ∞D (le vivant empile des canaux lents — coût "
        "mesuré : rang 2 insuffisant, 0.152 d'erreur max)",
        {"verdict": "déficit",
         "justification": "le candidat fractionnaire possède la mémoire "
                          "(∞D de noyau distribué) mais pas l'excitabilité "
                          "(seuil) : la fermeture exige l'ajout de la phase "
                          "S¹ — et la version biologique de la mémoire "
                          "exige elle-même un ajout de variables lentes "
                          "(approximation de rang fini)"},
        {"script": "p37_neurone_fractionnaire.py",
         "verdict": "p37_neurone_fractionnaire_verdict.json"},
        "toute trajectoire fractionnaire linéaire exhibant un spike "
        "tout-ou-rien ou un train sous courant constant tue l'entrée"),
    entree(
        "F12-PROFONDEUR-CONSTITUTIVE", "physique",
        "P36 : la profondeur devient constitutive dès que la tâche ITÈRE. "
        "Parité n bits : profondeur 1 impossible (LP infaisable, n=2..4), "
        "profondeur 2 exacte à n unités DÉRIVÉES entières (n=2..8). "
        "Oscillations (Telgarsky) : profondeur m largeur 2 exacte (m=1..8) ; "
        "loi serrée mesurée en profondeur 2 : w_min = 2^m unités "
        "(transitions aux demi-dyadiques) — séparation exponentielle "
        "2^m/2m reproduite à construction exacte, zéro apprentissage",
        "P36-PROFONDEUR", "PROF-1.0", "partielle",
        "fermée sur les familles déclarées (séparation unique / parité / "
        "oscillation) ; ouverte en général : la loi complète "
        "profondeur-minimale vs structure de tâche reste à cartographier "
        "(symétries, fonctions périodiques à période non dyadique)",
        {"verdict": "déficit",
         "justification": "la fermeture paie en degrés de liberté : couches "
                          "(réutilisation de coordonnées, coût 2m) ou largeur "
                          "(copie, coût 2^m) — le déficit se paie en "
                          "composition ou en exponentielle"},
        {"script": "p36_profondeur.py",
         "verdict": "p36_profondeur_verdict.json"},
        "tout réseau de profondeur 2 et largeur < 2^m exact sur la tâche à "
        "m oscillations tue l'entrée"),
    entree(
        "F13-ATTENTION-CONSTITUTIVE", "physique",
        "P38 : carte constitutive du bloc d'attention minimal, poids "
        "DÉRIVÉS, zéro apprentissage, exhaustivité déclarée. POSITION "
        "constitutive de tout ce qui n'est pas symétrique (copie : "
        "8/262144 sans, 262144/262144 avec one-hot dérivé) ; SOFTMAX non "
        "constitutif (linéaire exact, coût d'échelle dérivé "
        "β ≥ ln((n−1)/ε)/Δ vérifié à 1e-3/1e-6/1e-9) ; PROFONDEUR "
        "constitutive pour la parité (1 couche : 0.6367 max ; 2 couches "
        "exactes — cohérence P36/F12) ; COMPARAISON non bilinéaire = "
        "constitutif manquant du tri (candidats dérivés 3/27) ; "
        "MULTI-TÊTE constitutif uniquement pour relations incompatibles "
        "simultanées (mono-tête 8/256, 2 têtes dérivées 256/256)",
        "P38-ATTENTION", "ATTN-1.0", "fermée",
        "fermée sur les tâches gelées déclarées (copie, binaire, parité, "
        "tri, double-relation) à vérification exhaustive — la "
        "généralisation aux tâches à contexte long est un chantier "
        "séparé",
        {"verdict": "déficit",
         "justification": "chaque constitutif est un degré de liberté "
                          "ajouté : coordonnée de position (n dims), tête "
                          "supplémentaire (1 distribution), non-linéarité "
                          "de comparaison (absente, à payer)"},
        {"script": "p38_attention.py",
         "verdict": "p38_attention_verdict.json"},
        "copie exacte sans position ; tri exact à scores bilinéaires ; "
        "double-relation exacte en mono-tête — chacun tue l'entrée"),
    entree(
        "F14-PONT-120-E8", "physique",
        "le « 120 » koilon (N_modes = 120, P40) et les 120 racines "
        "positives de E₈ ont une racine commune EXACTE, établie en "
        "arithmétique pure Q(φ) : le groupe binaire icosaédrique 2I "
        "(120 quaternions unitaires construits) a pour carquois de "
        "McKay le diagramme Ẽ₈ affine (A·d = 2d exact, isomorphisme "
        "prouvé contre la référence Bourbaki, det Cartan = 1), série "
        "de Molien calculée = (1+t³⁰)/((1−t¹²)(1−t²⁰)) exacte, "
        "d₁ = 12 ; réécriture N = d₁·log₂(1/α) = |2I| ⟺ "
        "α = 2^(−|2I|/d₁) = 2⁻¹⁰ (l'α_K gelé de P40). Le laplacien "
        "scalaire sur S³/2I donne λ₁ = 168/R² — distinct du 2/R² du "
        "laplacien tordu (champs de Killing, Ric = (2/R²)g vérifié "
        "symboliquement)",
        "P42-PONT-120-E8", "PONT-1.0", "partielle",
        "partielle : le pont arithmétique 2I ↔ Ẽ₈ ↔ α = 2⁻¹⁰ est un "
        "théorème exécuté (fermé) ; l'identification PHYSIQUE des "
        "« 12 demi-tons » koilon avec d₁(2I) = 12 reste une frontière "
        "déclarée (médiation par la musique/spectre non dérivée)",
        {"verdict": "équilibre",
         "justification": "théorème d'arithmétique exacte : rien n'est "
                          "payé, tout est dérivé (groupes, caractères, "
                          "spectre, Molien) — la frontière physique "
                          "restante est déclarée, pas cachée"},
        {"script": "p42_pont_120_e8.py",
         "verdict": "p42_pont_120_e8_verdict.json"},
        "A·d ≠ 2d ; carquois de McKay non isomorphe à Ẽ₈ ; Molien "
        "calculé ≠ série théorique ; Ric ≠ (2/R²)g — chacun tue "
        "l'entrée"),
    entree(
        "F15-EXCITABILITE-REELLE", "physique",
        "le modèle Hodgkin-Huxley (type II, f₀ = 60 Hz à la rhéobase) "
        "n'est PAS représentatif de l'onset cortical réel : sur 32 "
        "cellules Allen Cell Types sélectionnées sans choix humain, "
        "31/32 sont type I (f₀ d'onset 1–10 Hz) au seuil gelé 20 Hz "
        "hérité de P35 — interneurones (aspiny) type II : 1/8 souris, "
        "0/8 humain ; pyramidales (spiny) : 0/8 et 0/8. La classe "
        "d'excitabilité type II existe dans le réel (interneurone "
        "souris 313861411, f₀ = 26 Hz confirmé au brut) mais elle est "
        "rare (1/16 interneurones). Izhikevich RS est le modèle minimal "
        "représentatif de l'onset cortical",
        "P41-NEURONES-REELS", "REEL-1.0", "partielle",
        "partielle : la question pré-enregistrée est tranchée (NON) sur "
        "32 cellules × 2 espèces × 2 classes morphologiques avec "
        "contrôle brut recoupé ±2 Hz ; l'extension à l'ensemble du "
        "catalogue (1781 cellules) et aux autres protocoles de "
        "stimulation reste ouverte",
        {"verdict": "déficit",
         "justification": "le seuil de classement (20 Hz) est payé une "
                          "fois (hérité gelé de P35, non ré-ajusté) : la "
                          "classification du réel achète sa frontière"},
        {"script": "p41_neurones_reels.py",
         "verdict": "p41_neurones_reels_verdict.json"},
        "C0 échoue (HH non type II ou Izhikevich non type I au seuil "
        "gelé) → l'instrument tombe ; recoupement brut/table > ±2 Hz "
        "→ la mesure tombe ; un rééchantillonnage 8-cellules donnant "
        "≥ 4/8 interneurones type II tue l'entrée"),
]


def main():
    # ---- validation de schéma (toute entrée invalide = B3-FAIL) ----------
    erreurs = []
    for e in FRONTIÈRES:
        cles = [k for k in SCHEMA if k not in e]
        if cles:
            erreurs.append(f"{e.get('id','?')} : clés manquantes {cles}")
        if e["statut"] not in STATUTS:
            erreurs.append(f"{e['id']} : statut invalide {e['statut']}")
        if e["type"] not in TYPES:
            erreurs.append(f"{e['id']} : type invalide {e['type']}")
    if erreurs:
        raise SystemExit("B3-FAIL du registre :\n" + "\n".join(erreurs))

    blob = json.dumps([e["sha256_entrée"] for e in FRONTIÈRES],
                      sort_keys=True).encode()
    registre = {
        "registre": "A4-FRONTIÈRES-MESURÉES",
        "protocole": "REG-FR-1.0 (gelé) — schéma déclaré, SHA-256 par entrée "
                     "et global, frontières mesurées uniquement",
        "schéma": SCHEMA,
        "statuts": sorted(STATUTS),
        "n_entrées": len(FRONTIÈRES),
        "par_statut": {s: sum(1 for e in FRONTIÈRES if e["statut"] == s)
                       for s in sorted(STATUTS)},
        "par_type": {t: sum(1 for e in FRONTIÈRES if e["type"] == t)
                     for t in sorted(TYPES)},
        "entrées": FRONTIÈRES,
        "sha256_registre": hashlib.sha256(blob).hexdigest(),
    }
    registre["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("a4_registre_frontieres.json")
    out.write_text(json.dumps(registre, ensure_ascii=False, indent=2),
                   encoding="utf-8")

    print("A4 — REGISTRE DES FRONTIÈRES MESURÉES   [REG-FR-1.0 gelé]")
    print("=" * 70)
    for e in FRONTIÈRES:
        print(f"  {e['id']:<24} [{e['type']:<8}] {e['statut']:<10} "
              f"ddll : {e['comptage_ddll']['verdict']}")
    print("-" * 70)
    print(f"  {registre['n_entrées']} entrées | "
          f"{registre['par_statut']} | schéma validé")
    print(f"  SHA-256 registre : {registre['sha256_registre'][:16]}…")
    print(f"  écrit : {out.name}")


if __name__ == "__main__":
    main()
