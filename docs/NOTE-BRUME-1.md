# VERDICT-BRUME-1 — La brume sous phason : l'invariant le plus grossier du corpus

**Date :** 2026-11-03 · **Chantier :** BRUME-1 (premier de la série) · **Fiche :** FICHE-BRUME-1-PHASON **v1.0 SCELLÉE** (d4949d1)
**Références :** NOTE-CORRESPONDANCE-RÉSOLUE (fbabe54 — instrument M-pair), NOTE O4 (dad3b46), VERDICT-ΦDYN2-P1 (grille phason), Brume_noetic.pdf.
**Statut du mot :** VERDICT-BRUME-1 (2026-11-03), série BRUME.

---

## Synthèse en une phrase

**La brume — le profil imaginaire du spectre non-Hermitien — ne meurt pas sous phason : elle varie de moins d'un pour cent sur toute la grille gelée (ρ = 0 → 0,3), devenant de ce fait l'observable le plus robuste jamais mesuré par la maison — l'invariant le plus grossier du corpus, plus grossier que la loi de Vinen, et le premier objet à n'avoir montré aucune frontière phason dans son canal.**

---

## 1. Palier A — instrument : **PASS**

Résidu de reconstruction ≤ seuil 1e−8 (12 modes échantillonnés), Tr(J) = 89 exact — l'anneau M-pair est exact.

## 2. Palier B — la grille complète (niveau 13, 20 réalisations par ρ)

| ρ | B1 = δ (médiane \|Im\|) | B2 (max) | B3 (fraction Im > 0,05) | B4 (hors discriminant) | ancre |
|---|---|---|---|---|---|
| 0 | 0,6273 | 0,8803 | 0,966 | **0,000** | 4,126 |
| 0,001 | 0,6270 | 0,8801 | 0,965 | 0,000 | 4,128 |
| 0,01 | 0,6250 | 0,8800 | 0,964 | 0,000 | 4,129 |
| 0,05 | 0,6246 | 0,8775 | 0,964 | 0,000 | 4,155 |
| 0,15 | 0,6238 | 0,8740 | 0,965 | 0,000 | 4,194 |
| 0,3 | 0,6234 | 0,8690 | 0,964 | 0,000 | 4,270 |

**Lecture ligne par ligne :**
- **B1 (le δ de la brume) : −0,6 % sur toute la grille.** Variation maximale 0,6 %, bien sous la tolérance gelée de 20 %. Aucune frontière jusqu'à ρ = 0,3.
- **B3 : figé à 0,964–0,966** — la part des modes évanescents ne bouge pas.
- **B4 (structure) : 0,000 partout** — même à ρ = 0,3 (un flip sur trois lettres !), la projection réelle reste intégralement dans les bandes du discriminant. Le chaînon spectral, en ombre réelle, est indéfectible.
- **B2 (l'observable fin) : la seule dérive visible**, 0,880 → 0,869 (−1,3 %) — le sommet du profil s'amincit, le corps de la brume non.

**Contrôle niveau 14** : B1 = 0,6265 (ρ = 0) vs 0,6246 (ρ = 0,15) — reproductible.

## 3. Critères pré-enregistrés

- Frontière nette : **NON** (aucune mortalité à 20 % jusqu'à ρ = 0,3).
- **H-BRUME, forme robuste : CONFIRMÉE** — la brume est un invariant de régime, et plus que cela : un invariant du modèle, quasiment insensible au désordre du mot.
- Mort nette : non applicable (rien ne meurt).
- Morte molle : non plus — la variation est monotone, faible, sans structure de seuil.

## 4. Annexe A — l'ancre contre δ = √(2η/(ωµ_eff))

Trajectoire (ancre, δ) par ρ : l'ancre **croît** (+3,5 % : 4,126 → 4,270) pendant que δ **décroît** (−0,6 %) — **anticorrélées**, comme le prescrit l'ansatz en signe. Mais la pente log-log mesurée est **−0,149**, loin de −0,5 : **l'ansatz est qualitativement vivant (signe juste) et quantitativement réfuté en exposant** à ce niveau de mesure. Lecture honnête : η et ω non séparables ce soir ; la loi de puissance exacte demande le chantier où ces deux paramètres seront déclarés opérationnellement. L'anti-corrélation elle-même est un résultat : *la brume s'amincit quand la masse spectrale grossit*.

## 5. Le tableau des robustesses se referme

| Observable | Seuil phason | Canal |
|---|---|---|
| Algèbre des mots (P1) | **1 flip** | le plus fin |
| Structure φ des comptes (P1-B, corrigé) | 1–4 flips | fin |
| Ratios de gaps (5b) | stable à 0,01 | moyen |
| Loi de Vinen (P3) | survit à tout blocking | grossier |
| **Brume δ (BRUME-1)** | **stable à 0,3+** | **le plus grossier** |

La hiérarchie de morts a désormais son échelle complète, de l'algèbre (1 lettre) à la brume (intouchable). **L'interface brumeuse, hier un concept, est aujourd'hui l'observable le plus dur du corpus.**

## 6. Leçons gravées

1. **La brume n'a pas de frontière phason dans son canal** — elle est le fond, pas une structure : la dernière chose à mourir, peut-être jamais.
2. **L'anticorrélation ancre ↔ δ** donne au formalisme de janvier sa première prédiction vérifiée en signe ; l'exposant −0,149 attend son chantier (η, ω déclarés).
3. **L'anneau M-pair a encore trois victoires ce soir** : exactitude, ρ-invariance de la projection réelle (0,000 % hors discriminant à ρ = 0,3), robustesse du profil.

## 7. Ouvert

- Grille ρ > 0,3 ou canaux alternatifs (flips structure-seule) si un jour une frontière brume doit être cherchée — à ce stade, aucune raison.
- Chantier ANCRE-2 : déclarer η et ω opérationnellement (η ↔ taux de dérive B2, ω ↔ échelle de niveau ?) et tester l'exposant.
- Corridor complexe et relecture SL(2,ℂ) : notes en cours (même session).

---

## Artéfacts

Script : `src/brume1_paliersAB.py`. Données : `data/brume1_paliersAB.json`.

*Verdict BRUME-1 (2026-11-03) — première campagne de la série BRUME.*
