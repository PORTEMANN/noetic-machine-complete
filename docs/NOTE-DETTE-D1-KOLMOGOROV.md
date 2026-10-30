# Note de chantier — Dette D1 : la comptabilité de Kolmogorov

**Date :** 2026-10-30 · **Tiroir :** remboursement de dette (convention de
mesure + instrument + reclassement ; aucune carte gelée modifiée).
**Filiation :** COMITE-LECTURE-ACIDE (objection 1) ·
NOTE-CIRCONSCRIPTION-MACHINES (registre des dettes) ·
`src/kolmogorov_density.py` (instrument versionné).

---

## 1. La dette

Le comité soutient que le « zéro paramètre ajusté » est vulnérable à
l'accusation de sélection *a posteriori* tant que l'écosystème ne
pénalise pas la complexité de description du choix d'opérateur, et que
le réseau {φ, π, e, √2, √3, 2^(1/12), Fibonacci/Lucas, dimensions de
Lie} forme une bibliothèque dense sur ℝ rendant toute « coincidence à
θ % » sans valeur probante.

## 2. La mesure (instrument : src/kolmogorov_density.py)

Générateur déclaré (bornes explicites : |a|,|b|,|c| ≤ 3, d ∈ [−12,12],
p,q ∈ {0,1}, n ∈ Fibonacci/Lucas ≤ 1000), valeurs dans [1, 2000] :

- **356 928 valeurs distinctes** ; densité moyenne ≈ 32 549 valeurs
  par octave ; espacement médian relatif **8 × 10⁻⁶** (0,0008 %).
- Une cible aléatoire possède en moyenne **921 voisins** du réseau à
  θ = 1 % (4 572 à θ = 5 %).
- Cibles du corpus (137,036 ; 128,397 ; 83,8 ; 312,757 ; 105,946 ;
  1,2) : 570 à 1 107 hits chacune dans la fenêtre ±1 %.

**Conclusion de mesure : à θ = 1–5 %, aucune proximité à un nombre
« spécial » ne porte de poids probant contre cette bibliothèque.**
Le comité a raison sur ce point, chiffres à l'appui.

## 3. Convention de comptabilité v0.1 (figée)

Toute affirmation numérique du corpus est classée :

- **Classe A — dérivation ou identité exacte.** Le nombre est produit
  par une structure de coût descriptif publié (graphe, contrainte,
  formule du canon), ou est une identité exacte (entier, comptage), ou
  une précision sous l'espacement de la bibliothèque. Exigence :
  coût descriptif en bits, publié avec la carte.
- **Classe B — proximité de bibliothèque.** Le nombre rejoint une
  constante du réseau à θ % près, sans dérivation jointe.
  Exigence : θ relatif ≲ 10⁻⁵ (sous l'espacement médian mesuré),
  sinon **auto-CSi** — la carte se juge elle-même morte par densité.

La règle s'applique rétroactivement au corpus et à sa rhétorique
(lettre ouverte incluse), et prospectivement à toute carte future :
c'est un organe, pas une circonstance atténuante.

## 4. Reclassement des affirmations (premier passage)

**Classe A (conservées comme monnaie) :** seesaw ±φ (dérivé du P4 à
M_R = 1 — coût : spécification du graphe) ; Tr = −16i (entier exact
sous unimodularité) ; charges p(uud) = +1 à 0θ (exact) ;
quasicristaux 147/147 (comptage entier) ; identité de Fricke à
10⁻¹⁶ (dix ordres sous l'espacement) ; escalier α⁻¹(M_Z) à 0,35 %
(formule du canon + seuils mesurés — coût : règle d'inclusion des
fermions connus) ; Σm_ν = 59 meV (forcé par la structure, NOTE-VERROU).

**Classe B (reclassées, non réfutées) :** toute formulation du type « la
constante X rejoint le nombre spécial Y à θ % » sans dérivation jointe —
proportion corticales φ⁻¹/φ⁻² à trois chiffres, le 137 comme nombre
(isolé de son banc spectral). Statut : évidentiellement vides seules ;
redevables d'une Classe A ou muettes.

## 5. Ouvert

La dette est partiellement remboursée : la densité est mesurée, la
règle est figée, le reclassement est commencé. Reste : chiffrer en bits
le coût descriptif de chaque opérateur du banc (porteur ℂ ⊕ M₂(ℂ),
KO-dim 6, partition AAL-116, escalier à 9 seuils) — chantier D1b, à
ouvrir quand le banc lui-même sera l'objet.
