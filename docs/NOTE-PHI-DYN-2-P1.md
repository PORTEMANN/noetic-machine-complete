# VERDICT-ΦDYN2-P1 — Le générateur reconnu (Fricke comme charge conservée)

**Date :** 2026-11-03 · **Chantier :** Φ-DYN-2 partie 1 · **Fiche :** FICHE-PHI-DYN-2-P1-GENERATEUR **v1.1 SCELLÉE** (commit 4ad4875 ; run 1 : CALIBRATION v1.0, défauts de rédaction documentés dans la fiche §6.3 et changelog 8 bis)
**Références :** T24 (conventions canoniques reprises sans modification), T41–T47 (données corridor), NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (4d657fb).
**Statut du mot :** hors-série Φ-DYN (décision d'auteur, fiche §8 point 5). Rétro-référence T24 inscrite au registre.

---

## Synthèse en une phrase

**La trace map est confirmée comme générateur : Fricke est une charge conservée exacte (dérive ≤ 2,6·10⁻³⁰ à 30 chiffres), la classification spectre/gap par l'orbite est parfaite (80/80), et la structure φ est exacte à zéro défaut de phason — mais elle est fine-structure : le premier flip phason la dégrade, quatre flips la tuent.**

---

## 1. Résultats par pilier (fiche v1.1)

### Pilier A — re-vérification du générateur : **PASS 3/3**

| Critère gelé | Seuil | Mesuré | Verdict |
|---|---|---|---|
| O1 Fricke parmi seeds de bandes | ≥ 95 % | **39/39 = 100 %** | PASS |
| O2 ratios φ, fenêtre T24 (niveaux 9–14, 3 derniers ratios ± 0,02 + récursion comptes ± 4) | conforme | 1,625 / 1,6154 / 1,6032, récursion OK | PASS |
| O3 classification Fricke ↔ référence exacte (limsup N ≤ 120) | ≥ 99 % | **80/80 = 100 %** | PASS |

Mesures annexes : **contrôle 30 chiffres (mpmath) : dérive max 2,6·10⁻³⁰** sur 5 orbites de bandes — la conservation de Fricke est exacte au dernier chiffre de la précision demandée. Lyapunov en bande : 0,34–0,44 (mesure nouvelle — dynamique faiblement chaotique sur le spectre) ; ≈ 11 près d'une arête. O4 (rotation/IDOS) : reporté en note — relation non spécifiée par la fiche, deux implémentations divergent, aucune troisième tentative (pas de calibration à l'aveugle).

Leçon du run 1 (conservée) : le test grille par interpolation de |x₂₀| est invalide (x_N est un polynôme de degré F_N ; pente locale jusqu'à 3·10⁴ par cellule à 2¹⁸). La classification passe par l'arithmétique exacte au seed.

### Pilier B — levier phason (grille gelée ρ ∈ {0 ; 0,001 ; 0,01 ; 0,05 ; 0,15 ; 0,3}, 20 réalisations, graine 20261103) : **réponse nette — TUÉ PROPREMENT**

| ρ | flips/mot (moy.) | ratio médian c₁₄/c₁₃ | dans φ ± 0,02 | résidu identité de trace |
|---|---|---|---|---|
| 0 | 0 | **1,6180** (φ exact) | 20/20 | 2,2·10⁻¹⁵ (epsilon machine) |
| 0,001 | 0,38 | 1,6180 | 12/20 | 2,2·10⁻¹⁵ (0 flip) à 16 (1 flip) |
| 0,01 | 3,8 | 1,3535 | 0/20 | 5,2 |
| 0,05 | 18,9 | 0,768 | 0/20 | 1,2·10³ |
| 0,15 | 56,6 | 0,378 | 0/20 | 1,0·10⁵ |
| 0,3 | 113 | 0,202 | 0/20 | 3,2·10⁵ |

**Lecture grain par grain (ρ = 0,001, réalisations Bernoulli) :** 0 flip → ratio = φ exactement, identité de trace exacte ; 1 flip → ratio 1,55–1,60, résidu 0,7–16 (map brisée, structure proche) ; 2 flips → ratio 1,46–1,50. **La frontière mesurée se situe entre 1 flip (≈ 0,3 % du mot de 377 lettres) et 4 flips (≈ 1 %).**

Deux corrections d'implémentation documentées (run 1) : indexation des mots W_N (mot_fibonacci(n) a longueur F_{n+2} — l'alias de grille du polynôme de degré 987 produisait 982 « bandes » fantômes) ; densité de flips par Bernoulli par position (le nombre fixe floor(ρL) quantifiait ρ = 0,001 à zéro flip).

### Pilier C — carte d'échelles (annexe descriptive, hors critères §3.6 — pas de tolérance gelée pour la coïncidence)

- Côté orbites : comptes 19 → 202 (niveaux 9–14, T24 reproduit) ; **échelle de la bande médiane : ratios 0,48 / 0,52 / 0,56 / 0,53 / 0,52 par niveau** (≈ 0,52 en moyenne, sans cible gelée — mesure nouvelle reportée telle quelle) ; gap maximal et bande maximale dominés par les objets extrémaux (constants sur les niveaux — non informatifs sur l'auto-similarité).
- Côté corridor (archive, descriptif) : sauts unitaires datés t = 3,50/3,55 (T44) ; saut de Lk à t = 7,5 (T43) ; plateaux 9,8/15,9/31,4 = paroi à 4 filaments/quantum (T47) ; Q verrouillé sauf singularité (T42).
- La coïncidence « dans les deux sens » demandée par la fiche n'a pas de tolérance gelée : **reportée, non jugée**.

### Pilier D — invariance adiabatique (analyse a posteriori, force réduite §3.5 — jamais au titre de classe (iii))

- Trajectoires de déformation non singulières (T42) : hamiltonien, dissipation seule, Rabi seul — **Q ∈ [0,9987 ; 1,0000] sur les trois chemins → invariants adiabatiques (critère gelé ± 0,005 tenu, 3/3)**.
- Chemin des masses A2→6 : Q décroît de 1,0000 à 0,0088 **uniquement** quand ρ_min → 0 (approche de la singularité SU(2)) ; fenêtre Δρ = 0,1 croisant la singularité : max |ΔQ| = 0,986 — écart entièrement porté par la traversée de la singularité, conforme à la leçon T42 (« la topologie se conserve lisse et se brise en un point »).
- **Verdict D : Q est un invariant adiabatique du flot déclaré ; sa mort exige une singularité, pas une déformation lente.** (Force réduite : analyse de séries archivées, pas un run gelé avant mesure.)

---

## 2. Verdict global (critères §3.6 de la fiche v1.1)

| Exigence | Résultat |
|---|---|
| O1 ≥ 95 % | 100 % ✓ |
| O2 conforme (fenêtre T24) | ✓ |
| O3 ≥ 99 % | 100 % ✓ |
| O6 réponse nette | ✓ **TUÉ PROPREMENT — frontière mesurée entre 1 et 4 flips par mot de 377** |

**PARTIE 1 TENUE — GÉNÉRATEUR RECONNU, AVEC RÉSERVE STRUCTURELLE T-1 (fine-structure).**

Formulation exacte : la trace map de Kohmoto est le générateur du spectre de Cantor Fibonacci — Fricke en est la charge conservée, vérifiée à 2,6·10⁻³⁰ à 30 chiffres, et l'orbite seule classifie parfaitement le spectre (c'est le critère « spectre ⇔ orbite bornée », 80/80). La structure dorée (ratios → φ, identité de trace) est **exacte à zéro défaut de phason et britannique au désordre** : un seul flip sur 377 lettres brise l'identité de trace (résidu 0,7–16) et dégrade le ratio ; ~1 % de flips tue la structure. **φ est ici du réglage fin, pas du régime** — le tueur T-1 de la fiche est déclenché, publié au même titre qu'une confirmation.

**Conséquence pour H-ΦDYN2a :** le générateur est réel (la dynamique discrète porte le continu, la classification est exacte), mais la portée du pont est bornée : la signature φ ne survit pas au désordre phason. La partie 2 (trace map du porteur seesaw) reste débloquée — avec la leçon supplémentaire que toute structure candidate devra être testée contre ses propres perturbations déclarées.

**Piliers C et D :** annexe descriptive (C) et analyse réduite (D) — D fournit néanmoins un résultat propre : Q est adiabatiquement invariant sous les flots déclarés, mortel seulement par singularité.

---

## 3. Leçons gravées au dossier

1. **« On ne tue pas un entier en le frottant »** (T42) — vérifié ici dans l'autre sens : on ne sauve pas une structure dorée en la frottant non plus. Le premier flip est déjà une brisure.
2. **Le spectre de Cantor se juge en arithmétique exacte, jamais sur grille** : x_N est de degré F_N ; à 2¹⁸, l'interpolation est mensongère aux arêtes (démontré), et le comptage de bandes s'effondre dès le niveau 15–16 (alias).
3. **La mesure nulle du spectre est une donnée du protocole** : un échantillonnage aveugle de l'intervalle touche presque toujours le gap — le seuil d'un observable doit dire où il s'applique.
4. **Un levier quantifié discrètement (flips) se lit grain par grain** : la Bernoulli par position est la lecture fidèle d'une densité ; floor(ρL) rend les petites densités muettes.
5. **Le générateur était déjà en main** : T24 l'avait livré avec sa charge conservée ; il aura fallu la fiche Φ-DYN-2 pour le reconnaître — c'est la réponse à l'orphelin de T15, en partie.

---

## 4. Artéfacts

Scripts : `src/phidyn2_p1_pilierA.py` (sha256 `94e3f88b…`, run 2 v1.1), `src/phidyn2_p1_pilierB.py`, `src/phidyn2_p1_pilierCD.py`.
Données : `data/phidyn2_p1_pilierA.json`, `data/phidyn2_p1_pilierB_rho{0, 0p001, 0p01, 0p05, 0p15, 0p3}.json`, `data/phidyn2_p1_pilierCD.json`.

*Verdict hors-série Φ-DYN, nommé VERDICT-ΦDYN2-P1 (2026-11-03), conformément à la décision d'auteur de la fiche §8 point 5.*
