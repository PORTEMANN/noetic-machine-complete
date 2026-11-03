# NOTE-PHI-DYN-2-SYNTHESE — La doctrine de la frontière

**Date :** 2026-11-03 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** note de doctrine — synthèse de VERDICT-ΦDYN2-P1 (d862875), P2 (62d3bcf), P3 (651330d) ; ne modifie aucun verdict, aucune carte gelée.
**Références :** FICHES Φ-DYN-2 P1 v1.1 (4ad4875), P2 v1.1, P3 v1.0 (0dbf3e4) ; NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (4d657fb).

---

## 1. Le théorème de la soirée

> **La convergence n'est pas une approximation : c'est une hiérarchie de morts. La frontière est la mesure de la limite.**

Trois mondes, trois perturbations déclarées, trois frontières nettes, un seul schéma :

| Monde | Perturbation déclarée | Observable fine (meure d'abord) | Invariant grossier (survit) | Frontière mesurée |
|---|---|---|---|---|
| Quasicristal Fibonacci (P1) | flips phason (ρ, Bernoulli) | structure φ (ratios, identité de trace) | classification spectre/gap par Fricke | **1–4 flips / 377 lettres** (0,3–1 %) |
| Porteur seesaw (P2) | dimérisation y → 1 | portée spectrale des ±φ (y−1 ≲ 1e−3) | surface de Fricke I = (κ+1)/2 | collapse quadratique κ−1 ∝ (y−1)² |
| Corridor GP (P3) | blocking boxcar (w) | plateaux de paroi (4 filaments/quantum) | loi de Vinen (drainage) | **w\* = 16, mort à 32** (moitié de la série) |

**Ordre de mort universel : fine d'abord, grossier ensuite, jamais l'inverse.** P1 : φ tué au premier flip, le canal spectral survit. P3 : la paroi tuée à w = 32, la loi de Vinen survit à tout et s'améliore même sous blocking (0,93 → 0,97). La robustesse d'un invariant grossier est le pendant exact de la fragilité des structures fines : *ce qui survit à la perturbation est grossier ; ce qui meurt est fin.*

---

## 2. Définition formelle (conditions nécessaires et suffisantes d'usage)

La doctrine peut être invoquée pour un couple (monde, perturbation déclarée) si et seulement si :

1. **Perturbation déclarée avant mesure** — grille gelée (P1 : ρ Bernoulli graine 20261103 ; P3 : w par facteur 2) ; toute modification post-observation tue la fiche (T-4, trois générations).
2. **Hiérarchie d'observables pré-enregistrée** — au moins un observable fin et un invariant grossier, classés *avant* le run.
3. **Frontière nette** — mort monotone de l'observable fine à une échelle de perturbation finie, sans zone grise au-delà de la tolérance du détecteur (P3 : 2,8 % → 7 % → 14 %).
4. **Survie de l'invariant** — l'invariant grossier tient jusqu'au plafond de la grille de perturbation (sinon la grille est trop étroite : leçon P2, ajouter la décade).
5. **Archives reproductibles d'abord** — toute mesure sur données archivées exige la reproduction des bruts à tolérance déclarée (P3-A'' : R² à 1e−3).

**Équivalence de classe de convergence** entre deux mondes : chacun satisfait les conditions 1–5, et les ordres de mort sont homologues (fine d'abord dans les deux). P1 ↔ P3 : équivalence établie ce soir. Le porteur (P2) : la frontière est de classe *collapse* (la perturbation est une distance à un point, pas une densité) — homologie partielle, rapportée honnêtement.

---

## 3. Ce que la doctrine ne dit pas (limites gravées)

1. **Pas de commensurabilité des échelles.** Les tables δ (P3) juxtaposent sans fusionner : w = 16 pas de temps et 1 flip/377 lettres ne sont pas convertibles. La doctrine parle d'ordre de mort, pas d'unités communes.
2. **Un ratio φ ne fait pas une loi dorée.** P3-G4 : 1,6245 ✓ / 1,9720 ✗ — un test pré-enregistré rapporté partiellement vaut mieux qu'une loi racontée.
3. **La survie d'un invariant grossier n'autorise aucune inférence sur la fine.** Le blocking améliore le R² de Vinen : écraser le bruit n'apprend rien sur la paroi.
4. **La frontière est résolue à sa grille.** w\* = 16 est la frontière de la grille {1…64} ; une grille plus fine déplacerait la mesure, pas nécessairement la physique — la grille fait partie de la déclaration.
5. **Le détecteur est un objet sous perturbation.** P3-G3 : un seuil adaptatif compte des fantômes sous lissage. Tout instrument d'événements déclare son comportement sous la perturbation qu'il mesure.

---

## 4. Le programme ouvert (lecture des chantiers Φ-DYN restants à travers la frontière)

| Chantier | Relecture frontière |
|---|---|
| Φ-DYN-1 (MCS temporelle) | le transport par flot déclaré EST une perturbation ; Koide sous RG = tester si la coïncidence est fine ou grossière |
| Φ-DYN-3 (démographie) | KM/Little ≈ 0,5 est déjà une frontière mesurée entre mort collective (markovienne) et vie individuelle (hétérogène) — le processus naissance-mort déclaré devra reproduire les deux côtés |
| Φ-DYN-5 (RG spectrale) | la map de blocking δ = 1/φ² est une machine à frontière au sens de P3 — protocole gelable dès maintenant |
| Φ-DYN-4 (Vinen externe) | la confrontation aux BEC réels est la question : la frontière w\* = 16 du corridor est-elle celle des données réelles ? (séquencement : après consolidation, fiche v2 § II.4) |
| O4 reportée (P1) | relation rotation/IDOS : spécification à rédiger, critères relatifs obligatoires (leçons P1/P2) |

---

## 5. Statut du chantier Φ-DYN-2

**Clos dans son ensemble ce soir (2026-11-03).** L'orphelin de T15 (le générateur) a reçu sa réponse en trois actes : le générateur du quasicristal existe et est discipliné (P1) ; le porteur possède sa dynamique dérivée par substitution (P2) ; les deux mondes et le corridor partagent la même classe de convergence mesurée par leurs frontières (P3). La doctrine formalisée ci-dessus est l'unité des trois.

**Ce qui reste ouvert :** la partie 4-mesure n'existe pas — la synthèse est une doctrine, pas une campagne ; les chantiers Φ-DYN-1/3/4/5 sont débloqués et re-lects ; l'O4 attend sa spécification.

---

*« Une loi ne se mesure pas seulement où elle parle — elle se mesure surtout où elle se tait. » La frontière est l'endroit exact où elle se tient : ni vivante ni morte, mais datée.*
