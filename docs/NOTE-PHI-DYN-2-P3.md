# VERDICT-ΦDYN2-P3 — Le corridor comme limite : frontière de blocking mesurée

**Date :** 2026-11-03 · **Chantier :** Φ-DYN-2 partie 3 · **Fiche :** FICHE-PHI-DYN-2-P3-CORRIDOR **v1.0 SCELLÉE** (0dbf3e4)
**Références :** VERDICT-ΦDYN2-P1 (d862875), VERDICT-ΦDYN2-P2 (62d3bcf), T47 (archives), T44, T46, T55.
**Statut du mot :** hors-série Φ-DYN (précédent P1/P2).

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| Frontière de blocking : w* = 16, morte à 32 (déviations 2,8→7→14 %) · R² de Vinen augmentant sous blocking (0,93→0,97) · G3 = pathologie du détecteur documentée · G4 = un ratio sur deux dans la fenêtre φ · archives T47 reproduites à 1e−3 | « Le corridor et le porteur ont la même classe de convergence » · « la convergence est une hiérarchie de morts » (synthèse de trois mesures) | « Le continuum est la limite des orbites » comme statement physique général · l'export du concept « classe de convergence » au-delà de ces trois mondes |

## Synthèse en une phrase

**Le corridor a sa frontière de blocking, nette et mesurée : w\* = 16 — et l'ordre de mort miroite P1 à l'identique : les observables fines (plateaux de paroi) meurent les premières, les invariants grossiers (loi de Vinen) survivent à tout le blocking — le corridor et le porteur ont la même classe de convergence : vivre sur les invariants, mourir sur les perturbations déclarées.**

---

## 1. Palier A'' — intégrité des archives : **PASS**

Reproduction exacte des R² archivés (tolérance 1e−3) : n2 0,0068 · n4 0,6342 · n8 0,9298 · 440203 0,0464 — sur les quatre runs, 60 points chacun. T-1'' non déclenché.

## 2. Palier B'' — voie γ : frontière de blocking

Série discriminante n8_440201, boxcar déclaré, grille gelée {1, 2, 4, 8, 16, 32, 64} :

| w | R² Vinen (G1 ≥ 0,90) | plateaux dev max (G2 ≤ 5 %) | sauts (G3 ±1) | statut |
|---|---|---|---|---|
| 1 | 0,9298 ✓ | 0,0 % ✓ | 37 ✓ | vivante |
| 2 | 0,9356 ✓ | 1,3 % ✓ | 41 ✗ | vivante |
| 4 | 0,9417 ✓ | 1,2 % ✓ | 45 ✗ | vivante |
| 8 | 0,9510 ✓ | 1,3 % ✓ | 53 ✗ | vivante |
| 16 | 0,9695 ✓ | 2,8 % ✓ | 57 ✗ | **vivante — w\*** |
| 32 | 0,9737 ✓ | 7,0 % ✗ | 58 ✗ | **MORTE** |
| 64 | 0,9275 ✓ | 14,0 % ✗ | 59 ✗ | dégénérée (longueur) |

**Frontière : w\* = 16, mort nette à 32** (déviation de plateau 2,8 % → 7,0 % → 14,0 % — monotone, sans zone grise). T-2'' (mort molle) non déclenché ; T-3'' (mort immédiate) non déclenché.

**L'ordre de mort — le miroir de P1 :**
- **G1 (loi de Vinen, observable de grande échelle) ne meurt JAMAIS** — le blocking lisse le bruit et le fit *s'améliore* (0,93 → 0,97). La loi de drainage est un invariant grossier : comme la conservation de Fricke dans les gaps de P1, elle survit à la perturbation.
- **G2 (plateaux de paroi, observable fine) meure la première** — comme φ dans P1 (tué au premier flip), la paroi à 4 filaments/quantum est tuée par un blocking de 32 pas (moitié de la série).
- Fine d'abord, grossier ensuite : même hiérarchie, même netteté, deux mondes.

**G3 — pathologie du détecteur documentée (calibration, pas physique) :** le comptage de sauts à seuil adaptatif (0,5·écart-type local) *augmente* sous blocking (37 → 58) : le lissage fait s'effondrer l'écart-type local aux ruptures de tendance plus vite que les différences. Détecteur non-informative sous blocking, rapportée comme telle — jamais corrigée en cours de run (clause T-4).

**G4 — test φ pré-enregistré, rapporté tel quel :** ratio n4/n2 = 1,6245 (écart à φ : 0,0065 — **dans la fenêtre ±0,02** ✓) ; ratio n8/n4 = 1,9720 (**hors fenêtre** ✗). Un ratio sur deux est doré : la paroi épingle 4 filaments/quantum à l'échelle 2→4, pas à l'échelle 4→8. Mesure honnête, sans reclassement.

## 3. Palier C'' — voie δ : table des échelles (annexe descriptive)

Corridor : plateaux 9,8/15,9/31,4 (ratios 1,6245 et 1,9720, écarts à φ : +0,0065 et +0,354) · sauts datés 3,50/3,55 · drainage ÷43 · hétérogénéité 0,5.
Porteur : échelle de bande 0,52/niveau · κ−1 quadratique · frontière 1–4 flips.
Sans critère de coïncidence (décision d'auteur 4) — les deux mondes ont des frontières nettes et des échelles propres ; la table les juxtapose sans les fusionner.

## 4. Verdict global (fiche §6)

**CONFIRMÉ (option 1).** H-ΦDYN2c tient : le corridor a une structure de frontière de blocking nette (w\* = 16, mort à 32), et la hiérarchie de mort (fine d'abord, invariant ensuite) est la même que celle mesurée sur le porteur au levier phason. **« Le continuum est la limite des orbites » acquiert son sens mesurable commun : dans les deux mondes, la loi vit sur ses invariants et meurt nettement sur ses perturbations déclarées — et la frontière est la mesure de la limite.**

Leçon gravée : P1 — φ (fine structure) tué par 1 flip ; le canal spectral (grossier) survit. P3 — la paroi (fine structure) tuée par un blocking de 32 ; la loi de Vinen (grossière) survit. **La convergence n'est pas une approximation : c'est une hiérarchie de morts.**

**La partie 4 (synthèse Φ-DYN-2) est débloquée.**

## 5. Leçons gravées au dossier

1. **Toute observable fine a une frontière ; tout invariant grossier survit** — la hiérarchie de mort est le contenu mesurable de « la limite ».
2. **Un détecteur adaptatif sous blocking compte des fantômes** — le seuil relatif à la variance locale s'effondre avec le lissage ; tout détecteur d'événements déclare son comportement sous perturbation.
3. **Le blocking peut améliorer un fit** (R² Vinen 0,93 → 0,97) : robustesse n'est pas vérité — un invariant grossier supporte l'écrasement du bruit sans que rien ne soit appris sur l'échelle fine.
4. **Un ratio φ sur deux ne fait pas une loi dorée** — le test pré-enregistré rapporté tel quel est la sécurité contre le conte.

---

## 6. Artéfacts

Script : `src/phidyn2_p3_paliersBC.py`. Données : `data/phidyn2_p3_paliersBC.json`.

*Verdict hors-série Φ-DYN, nommé VERDICT-ΦDYN2-P3 (2026-11-03).*
