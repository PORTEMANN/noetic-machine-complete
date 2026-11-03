# Fiche chantier Φ-DYN-5b — Existe-t-il une RG déclarée pour laquelle φ EST fixe ?

**Date :** 2026-11-03 · **Version :** 1.3 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.3** (v1.0 : critère F1 sourd au bruit → v1.1 ; v1.2 : instrument anneau imposé par l'erratum VERDICT-ΦDYN2-P1 ; **v1.3 : contrôle croisé du palier A corrigé** — la « borne L − c_N » de la v1.2 était une conjecture fautive : les gaps de l'anneau incluent les espacements intra-bandes (~L−1 ≫ L − c_N) ; le contrôle correct est l'**adéquation des supports spectraux** : tout eigenvalue de l'anneau doit appartenir à l'union des bandes du trace map (T24) à la tolérance de grille près). Toute exécution suit cette version ; tout écart la tue (T-4).
**Références :** VERDICT-ΦDYN5 (261d41e — value-blocking : φ s'écoule), VERDICT-ΦDYN2-P1 (d862875 — φ fine-structure, tuée par 1 flip), T24, NOTE-PHI-DYN-2-SYNTHESE (18a7ab1).

---

## 1. Contexte et l'enchaînement logique

**Où Φ-DYN-5 a fermé une porte.** Le blocking sur les *valeurs propres* (fusion des écarts < δ) tue φ à tous les δ : φ est un objet UV qui s'intègre au flot ; l'ancre est le couplage qui tourne. Porte fermée : φ comme point fixe d'une RG de valeurs.

**Où cette fiche rouvre la question.** VERDICT-ΦDYN2-P1 a établi que φ est *fine-structure* : exacte sur le mot Fibonacci pur, tuée par le premier flip phason. Or la **self-similarité** du spectre de Cantor (échelle φ, P1-C) suggère que φ devrait être fixe pour une RG de **décimation par substitution** — non pas fusionner des valeurs, mais *remonter la hiérarchie* : le niveau N+1 raffine le niveau N, et si la distribution des ratios de gaps est invariante sous raffinement, φ est le point fixe de cette RG-là. L'instabilité est alors prédite, pas redoutée : le point fixe doit être attractif seulement le long de la variété propre (mot exact), et la grille phason de P1 mesure déjà cette stabilité.

**Hypothèse H-ΦDYN5b.** *φ est un point fixe de la RG déclarée par décimation de substitution sur la hiérarchie spectrale de Cantor — point fixe instable : la distance à la distribution fixe décroît avec le niveau sur le mot pur, et ne décroît pas sous désordre phason.*

Si H-ΦDYN5b tient : φ n'est ni un accident UV (Φ-DYN-5) ni un décor — c'est un **point fixe instable** : la générité existe, mais elle n'est visible que depuis la variété exacte. C'est la formulation la plus forte compatible avec les trois verdicts antérieurs.

---

## 2. Sens charter

Classe (ii) — la machine simule la générité sans connaître les équations. Zéro paramètre ajusté, gel avant mesure, échec publié. Numérique pure, outillage existant (P1 : trace map sur grille 2¹⁸, mots W_N, grille phason Bernoulli).

---

## 3. Objets déclarés (à sceller)

### 3.1 La RG déclarée (décimation de substitution) et l'instrument anneau (v1.2)

- **Hiérarchie spectrale :** anneaux périodiques de Jacobi aux niveaux 12, 13, 14 (W₁₂/W₁₃/W₁₄ = 144/233/377 sites ; diagonale = motif onsite A→0, B→1 ; saut 1 ; bouclage périodique). Spectre par `eigvalsh` — instrument **stable et exact** (à la différence des produits de transfert grid-wide, aliasés — erratum VERDICT-ΦDYN2-P1). Le spectre de l'anneau échantillonne directement la mesure spectrale finie : gaps = écarts entre eigenvalues consécutives.
- **Contrôle croisé (v1.3, forme finale après diagnostic) :** le croisement anneau/trace map est déclaré **NON APPLICABLE** — la récurrence de T24 et le Jacobi anneau à sauts uniformes ne correspondent pas modèle pour modèle (diagnostic : 41–45 % des eigenvalues exactes de l'anneau ont |x_N(λ)| > 1 au discriminant de la récurrence, évalué à 60 chiffres ; les graines de la récurrence ne sont pas les traces des mots du modèle à sauts uniformes). L'anneau est auto-suffisant (`eigvalsh` exact) : le contrôle retenu est l'**exactitude interne** — réalité, N = L, trace = somme des onsites. La correspondance exacte des modèles reste **ouverte** (non feuilletée ce soir).
- **Opérateur de blocking :** la décimation n'est pas une opération à paramètre — c'est le *passage de niveau* N → N+1 (le raffinement par substitution est la RG elle-même). Le levier de perturbation reste la grille phason ρ (§3.3).
- **Observable :** distribution empirique des **ratios de gaps consécutifs** r_i = g_{i+1}/g_i sur le spectre de l'anneau du niveau N, gaps < 10⁻⁴ exclus (plancher de résolution déclaré — l'échelle spectrale est ~[−1,7 ; 2,5]). Le point fixe est la distribution limite D\* ; φ fixe signifie D\* concentrée sur les ratios dorés (1/φ, 1/φ², … selon la structure trois-gap).

### 3.2 Mesures (gelées)

| # | Mesure | Définition | Critère pré-enregistré |
|---|---|---|---|
| F1 | convergence propre | distance de Kolmogorov-Smirnov D(N, N+1) entre distributions de ratios, N = 12, 13 (mot pur, anneau) | **v1.2 : strictement décroissante** (l'instrument anneau est exact — pas de bruit de grille ; la bande v1.1 est conservée comme garde mais ne devrait pas se lier) ; la bande v1.1 (0,27·√((n+m)/(n·m))) reste déclarée comme réserve |
| F2 | distribution fixe | D(13, 14) — distance au niveau le plus fin ; **test de permutation gelé** : p-valeur par 1 000 permutations de la liste fusionnée des ratios (graine 20261103) ; **observable complémentaire v1.1 : ratio de comptes c_{N+1}/c_N avec la fenêtre T24 gelée** (3 derniers ratios dans φ ± 0,02 + récursion des comptes ± 4 — protocole P1-O2/T24 verbatim, référence prior, pas sélection nouvelle) | rapportée ; test φ sur les ratios de gaps : fraction dans {1/φ ± 0,02, 1/φ² ± 0,02} ; KS asymptotique rapportée avec réserve (~200 gaps) |
| F3 | instabilité phason | même F1 sous grille ρ ∈ {0, 0.001, 0.01} (Bernoulli, graine 20261103, 20 réalisations par ρ — reprise gelée de P1) | à ρ = 0 : F1 tient ; à ρ ≥ 0.001 : F1 ne tient plus (au moins 15/20 réalisations en échec) |
| F4 | échelle de convergence | pente log-log de D vs niveau | mesure nouvelle, sans cible gelée |

### 3.3 Grille phason (gelée, reprise P1 §3.3)

Densités Bernoulli par position, ρ ∈ {0, 0.001, 0.01}, graine 20261103, 20 réalisations par ρ. Les mots déformés se propagent aux structures de bandes par le produit de transfert vectorisé (implémentation P1-B, corrigée d'indexation).

### 3.4 Tolérances

Grille 2¹⁸ (P1). Gaps < 3 cellules grille déclarés non résolus et exclus (leçon P1 : arêtes). KS par statistique exacte à distribution continue (asymptotique, échantillons ~200 — rapportée avec cette réserve). Aucune tolérance modifiable après le premier run (T-4, quatrième génération).

---

## 4. Programme

**Palier A — instrument.** Structures de bandes niveaux 9–14 (mot pur) reproduites (comptes 19/30/48/78/126/202 de T24) ; distributions de ratios calculables ; KS implémentée ; contrôle : à ρ = 0, F3 se réduit à F1. Effort : minutes.

**Palier B — mesure.** F1, F2 (mot pur) ; F3 (grille phason) ; F4. Effort : < 1 h.

---

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict si déclenché |
|---|---|---|
| T-1⁗ Non convergence propre | D(N, N+1) non décroissante à ρ = 0 | pas de point fixe de décimation : φ est UV même pour la RG de substitution — publié (renforce Φ-DYN-5) |
| T-2⁗ Instabilité non mesurée | F3 échoue à discriminer ρ = 0 vs ρ = 0.001 (réalisations pures indistinguables du désordonné) | la grille phason est trop fine pour ce test → calibration documentée |
| T-3⁗ Résolution | les distributions de ratios dépendent du seuil d'exclusion des gaps (< 3 cellules) | calibration documentée, seuil re-déclaré |
| T-4⁗ | sélection a posteriori | B3-FAIL de fiche, mort datée |

**Levier discriminant :** ρ phason — le même qu'en P1, mais lu cette fois comme la *stabilité du point fixe* et non comme la *mort de la structure* : deux questions, un levier.

---

## 6. Verdicts possibles

1. **CONFIRMÉ :** F1 décroissante à ρ = 0, distribution fixe φ-signée (F2), instabilité mesurée (F3) → **φ = point fixe instable de la RG de décimation** : la générité existe, elle est fine. Les quatre verdicts (P1, P2, Φ-DYN-5, 5b) forment alors un tableau cohérent : φ UV pour la RG de valeurs, fixe instable pour la RG de substitution.
2. **RÉFUTÉ :** T-1⁗ → pas de point fixe même par décimation : φ n'est générique pour aucune RG déclarée à ce jour — publié.
3. **CALIBRATION :** T-2⁗/T-3⁗/T-4⁗ → erratum +0.1.

---

## 7. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **Niveaux 9–14 — VALIDÉ, sans extension à 15** : le niveau 15 est sous-résolu à 2¹⁸ (mesuré en P1 : alias du polynôme de degré F₁₅) ; l'étendre avec une réserve explicite serait une invitation à lire du bruit.
2. **Seuil d'exclusion des gaps < 3 cellules grille — VALIDÉ** : standard P1 (arêtes et tangences dégénérées), cohérent avec toute la chaîne de mesure.
3. **Grille phason {0, 0.001, 0.01} — VALIDÉE telle quelle** : reprise gelée de P1, comparabilité directe des deux verdicts ; resserrer autour de la frontière 1–4 flips serait un nouveau protocole, pas celui-ci.
4. **KS asymptotique — ACCEPTÉE AVEC RÉSERVE, renforcé d'une permutation gelée** : la statistique asymptotique sur ~200 gaps est rapportée avec sa réserve ; le test de permutation (1 000 permutations, graine 20261103) est gelé comme référence principale pour F2.
5. **Nom — CONFIRMÉ :** verdict publié comme **VERDICT-ΦDYN5B (daté)**, hors-série Φ-DYN, précédent P1–P3/5.

---

*Cette fiche ne modifie aucun verdict ni carte gelée. Elle est la question qui restait : si φ s'écoule pour toute RG de valeurs, est-il fixe pour une RG de structure ? La réponse prédite est oui — instable. Mesurons-le.*
