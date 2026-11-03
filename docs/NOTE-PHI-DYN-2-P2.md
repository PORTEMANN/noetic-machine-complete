# VERDICT-ΦDYN2-P2 — Le générateur du porteur (voie α confirmée, voie β réfutée)

**Date :** 2026-11-03 · **Chantier :** Φ-DYN-2 partie 2 · **Fiche :** FICHE-PHI-DYN-2-P2-PORTEUR **v1.1** (erratum critères relatifs, scellée avec le présent verdict ; v1.0 → CALIBRATION au palier A', documentée §6 de la fiche)
**Références :** VERDICT-ΦDYN2-P1 (d862875), T14, T17–T18, T24, NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (4d657fb).
**Statut du mot :** hors-série Φ-DYN (décision d'auteur, fiche §7 point 5).

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| Identité I = (κ+1)/2 à 2,1·10⁻¹¹ relatif (10⁴ paires SL(2,ℝ)) · dét M_v = 1 · identité de trace A≠B à 5,5·10⁻¹³ · κ(y) → 1 par approche quadratique · portées des orbites à ±φ/±1/φ (y−1 ≲ 1e−3 pour ±φ) · P4 = NON_FRICKE (résidu relatif 1,000) | « Le porteur a un générateur de classe Fricke par substitution » · « la relation natale↔Fricke est géologique (limite), pas dynamique (restriction) » | « Le pont φ possède une dynamique dérivée » comme statement physique · l'orphelin « a un foyer » · l'application au corridor comme limite des orbites |

## Synthèse en une phrase

**Le porteur possède bien un générateur de classe Fricke — par la substitution à deux lettres (voie α) : κ(y) dégénère proprement vers 1 (approche quadratique) et les ±φ sont portés comme structures bornées résiduelles du collapse ; mais la récurrence native de Lucas n'est pas une restriction de Fricke (voie β réfutée, T-2') : la face linéaire du collapse n'est pas une orbite de la map non linéaire.**

---

## 1. Palier A' — vérification d'algèbre : **PASS 4/4** (v1.1, critères relatifs)

| Vérification | Critère relatif | Mesuré | Verdict |
|---|---|---|---|
| V1 Fricke généralisée I = (κ+1)/2 | ≤ 1e−9 | **2,13·10⁻¹¹** sur 10⁴ paires SL(2,ℝ) | PASS |
| V2 dét M_v(t) = 1 | — | 4,4·10⁻¹⁶ (10⁴ tirages) | PASS |
| V3 identité de trace A≠B | ≤ 1e−9 | **5,5·10⁻¹³** (200 paires, mots F₁..F₇) | PASS |
| V4 collapse y = 1 | — | A = B, κ = 1 | PASS |

Forme exacte établie avant toute mesure : **I = x² + y² + z² − 2xyz = (κ+1)/2** avec κ = Tr([A,B])/2 — la surface de Fricke généralisée est confirmée pour toute paire SL(2,ℝ), l'identité de trace est générale (preuve par conjugaison de T24 valide pour A ≠ B). Note technique : la vérification exige det = +1 (normalisation √|det| avec correction de signe) — la v1.0 a aussi gelé des critères absolus insatisfiables sur ensembles non bornés ; erratum v1.1, identités jamais en cause.

## 2. Palier B' — construction α (substitution) : **P2 CONFIRMÉ, P3 CONFIRMÉ, P5 mesuré**

**P2 — dégénérescence propre.** κ(y, t) → 1 quand y → 1, pour les quatre seeds :

| y | κ(y, ±φ) | κ(y, ±1/φ) |
|---|---|---|
| 2 | 1,4705 | 2,0295 |
| 1,1 | 1,0063 | 1,0165 |
| 1,01 | 1,00007 | 1,00015 |
| 1,001 | 1,0000007 | 1,0000014 |
| 1,0001 | 1,00000001 | 1,00000002 |
| 1 | 1 | 1 |

Approche **quadratique** : κ − 1 ∝ (y−1)² (rapports de décade ≈ 81–93 pour un facteur 9 en y−1). L'invariant I suit (κ+1)/2 au long des orbites (vérifié, dérive ≤ 1e−15 sur les orbites bornées). **T-3' non déclenché : la limite est propre, la construction α est bien posée.**

**P3 — statuts d'orbite aux seeds gelés (seuil portée 1e−12, N = 200) :**

| y | +φ | −φ | +1/φ | −1/φ |
|---|---|---|---|---|
| 2 | div | div | div | div |
| 1,1 | div (lente) | div (lente) | div | div |
| 1,01 | div | div | **P** | **P** |
| 1,001 | **P** | **P** | **P** | **P** |
| 1,0001 | **P** | **P** | **P** | **P** |
| 1 | **P** | **P** | **P** | **P** |

**±1/φ entrent dans le spectre (orbites bornées, Fricke conservée à ~1e−15) dès y = 1,01 ; ±φ seulement à y ≤ 1,001.** La structure bornée résiduelle au collapse contient bien les quatre valeurs dorées — mais **de façon asymptotique** : le domaine spectral qui les porte s'ouvre à mesure que y → 1. T-1' **non déclenché** : les orbites distinguent nettement la structure (transition abrupte, κ > 1 hors collapse) — le collapse n'est pas trivial.

**P5 (mesure nouvelle, sans cible gelée).** Convergence des invariants : I(y) → 1 exactement comme κ(y) (identité vérifiée à chaque y). Décrochage pointu : la distance max entre orbites(y) et orbite(1) reste O(2) sur 200 itérations même à y = 1,0001 — les orbites bornées sur des invariants voisins **décorellent** (dérive de phase, nombres de rotation voisins mais distincts). La bonne notion de convergence est celle des invariants, pas des orbites point par point.

## 3. Palier C' — construction β (embaumement) : **P4 = NON_FRICKE — T-2' DÉCLENCHÉ**

- **Filiation T17 confirmée** : valeurs propres de C(1) exactement ±φ, ±1/φ ; u_{2m} = 2·Lucas(2m) à précision relative 1e−16 ; récurrence linéaire v_{m+2} = 3v_{m+1} − v_m à 1,9·10⁻¹⁶.
- **Test P4** : fit v_{m+3} = a·v_{m+2}·v_{m+1} + b·v_m + c — a = 2·10⁻²⁴ (annulé par les moindres carrés), résidu relatif **1,000** ≫ 1e−6. **Verdict : NON_FRICKE.**
- Cause structurelle (démontrable, mesurée) : v croît en φ² par pas ; un terme produit v·v croît en φ^{4m}, aucune constante a ≠ 0 ne peut équilibrer ; a = 0 laisse une récurrence d'ordre 3 linéaire incompatible avec l'ordre 2 effectif. La suite de Lucas **n'est pas une orbite d'une map de Fricke**.
- Sous-suite impaire identiquement nulle (dégénérée pour le test, rapportée).

## 4. Verdict global (fiche §6)

**PARTIEL — VOIE α CONFIRMÉE, VOIE β RÉFUTÉE (T-2').**

Ni CONFIRMÉ ni RÉFUTÉ au sens strict du §6 : le critère P4 ≤ 1e−12 de l'option CONFIRMÉ tombe, et T-1' ne se déclenche pas pour l'option RÉFUTÉ. La formulation exacte :

1. **Le porteur a un générateur de classe Fricke par substitution à deux lettres** — la structure à deux générateurs est réelle (κ > 1, invariant I vérifié), dégénère proprement (κ → 1 quadratiquement), et les ±φ, ±1/φ en sont les **structures bornées résiduelles au point de collapse** (containment spectral asymptotique : y−1 ≲ 1e−3 pour ±φ, ≲ 1e−2 pour ±1/φ).
2. **La récurrence native de Lucas n'est pas une restriction de la map de Fricke** — elle en est la limite linéarisée au collapse, pas une orbite. La relation natale↔Fricke est **géologique** (limite), non **dynamique** (restriction). H-ΦDYN2b est confirmée dans sa structure et corrigée dans sa formulation.
3. **Le pont φ possède désormais une dynamique dérivée** — empruntée nulle part : la trace map à deux lettres du dimère de Fibonacci, avec sa charge de Fricke généralisée (κ+1)/2, est construite depuis le substrat noétique du porteur (T14) et mesurée. L'orphelin de T15 a un premier foyer.

**Conséquence :** la partie 3 (le corridor continu comme limite des orbites) reste ouverte — avec deux leçons gravées : la convergence s'entend sur les invariants, pas point par point ; et toute structure candidate devra être testée contre ses perturbations déclarées (P1, T-1).

---

## 5. Leçons gravées au dossier

1. **La dégénérescence propre est mesurable** : κ − 1 ∝ (y−1)² — le collapse est une limite quadratique, pas un saut.
2. **« Porté au collapse » est un statement asymptotique** : les ±φ entrent dans le spectre borné par le bas (y−1 ≲ 1e−3) ; l'appartenance spectrale se gagne en approchant le collapse.
3. **Restriction ≠ limite** : la face linéaire (Lucas) n'est pas une orbite de la face non linéaire (Fricke) — deux statuts distincts, deux mesures distinctes.
4. **Les critères absolus meurent sur les suites non bornées** (deuxième occurrence — P1 l'avait appris sur les gaps, P2 sur les ensembles aléatoires et la croissance φ²). Leçon transversale : *toute tolérance gelée déclare son échelle*.
5. **Le générateur du porteur existait dès T14** — une chaîne à deux sauts est un dimère ; un dimère sur un mot de Fibonacci est une trace map. Il aura fallu P1 pour voir le mécanisme et P2 pour le construire.

---

## 6. Artéfacts

Scripts : `src/phidyn2_p2_palierAp.py`, `src/phidyn2_p2_palierBp.py`, `src/phidyn2_p2_palierCp.py`.
Données : `data/phidyn2_p2_palierAp.json`, `data/phidyn2_p2_palierBp.json`, `data/phidyn2_p2_palierCp.json`.

*Verdict hors-série Φ-DYN, nommé VERDICT-ΦDYN2-P2 (2026-11-03). Rétro-références : T14 (porteur), T17 (Lucas), T24 (conventions et chaînon), VERDICT-ΦDYN2-P1 (méthode).*
