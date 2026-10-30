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

## 6. D1b — le chiffrage des opérateurs du banc (2026-10-30)

**Convention de comptage v0.1 (déclarée, révisable par note seulement).**
On compte les bits nécessaires pour spécifier le choix de l'opérateur
parmi ses alternatives plausibles à l'échelle du banc ; les entrées
*mesurées* (masses PDG, constantes CODATA) coûtent 0 bit ; les formules
du canon (boucle à un fermion, Laplacien D − W) coûtent 0 bit ;
chaque choix discret arbitraire coûte log₂ du nombre d'alternatives.
Fourchettes honnêtes : ce sont des estimations d'ingénierie, pas des
mesures.

**Bilan comptable (premier passage).**

| Opérateur | Spécification | Coût estimé | Classe | Statut de survie |
|---|---|---|---|---|
| Porteur ℂ ⊕ M₂(ℂ) | algèbre semisimple, dim 5, 2 blocs (1,2) | **≈ 6–8 bits** (algèbres de petite dim : peu de candidates) | A | tenu (Tr = −16i exact) |
| KO-dimension 6 | KO-dim ∈ {0..7}, choix physique motivé (ordre un, 4D) | **≈ 3 bits** | A | tenu (condition d'ordre) |
| Unimodularité | contrainte volume-fixe, choix binaire | **≈ 1–2 bits** | A | tenu (secteur 6 = 4 ⊕ 2) |
| Chaîne seesaw P4 à M_R = 1 | graphe chemin sur 4 nœuds (≈ 3 bits parmi les graphes 4n) + échelle naturelle (≈ 2 bits) | **≈ 5 bits** | A | tenu (±φ exact, 0 paramètre) |
| Escalier spectral (9 seuils) | règle « tous les fermions chargés connus » (contenu SM, ≈ 2 bits) + triade m_p/3 (≈ 2 bits parmi {pole, MS̄, m_p/3, constituante}) + **s fixé à 0,500 GeV (≈ 4–6 bits — choix franc dans une incertitude large)** | **≈ 8–10 bits** | A | tenu (0,35 %, S+) |
| Partition AAL-116 → 7 plans | 116 régions assignées, 6 arbitrages documentés (NOTE-MCS-28 §4) — mais assignation *sémantique*, non dérivée | **≈ 30–60 bits** (le plus cher du banc, de loin) | B+ (règles publiées, pas dérivation) | **fragile** : effets CSp après D4, invariance inter-grille modérée |

**Lecture du bilan.**

1. **Le squelette micro est incroyablement bon marché.** Pour ≈ 15–20
   bits au total, le banc achète : Tr = −16i exact, ±φ exact, charges
   à 0θ, running à 0,35 %. À titre de comparaison, *une seule*
   coincidence de Classe B à θ = 1 % coûte log₂(921) ≈ **10 bits et
   n'achète rien**. Le rapport coût/acquisition du banc micro est le
   meilleur argument de l'écosystème — mieux que toute rhétorique.
2. **La partition AAL-116 est le mauvais élève du banc.** Opérateur le
   plus cher en bits (un ordre de grandeur au-dessus du reste), et le
   seul dont le rendement mesuré se dégrade sous déformation (D4) et
   sous changement de grille (MCS-32). La comptabilité D1b **prédit ce
   que la mesure a déjà montré** : un opérateur cher et faiblement
   ancré. Conséquence proposée : toute nouvelle carte cognitive devra
   désormais déclarer son coût descriptif, et le seuil d'acceptation
   sera d'autant plus exigeant que le coût est haut.
3. **Le point faible honnête de l'escalier** : le seuil s à 0,500 GeV
   est un choix non dérivé (~4–6 bits) dans une incertitude de masse
   large. Un audit du seuil s (bornes PDG/MS̄, sensibilité de la
   prédiction) est la suite naturelle du muscle micro.
4. **Statut : D1 soldée v0.1 + D1b première passe.** La convention est
   publiée, le bilan est chiffré, la règle de seuil coût/précision est
   proposée au prochain passage. Révision uniquement par note datée.

## 7. D1c — audit des seuils de l'escalier (2026-10-30)

Instrument : `src/audit_seuil_s.py`. Scénarios déclarés, calcul direct,
projecteur de Heaviside appliqué strictement (seuil ouvert seulement si
m < Λ — le top est fermé à M_Z, ce qui reproduit la base du corpus à
128,3969 exact).

**Correction datée de la lecture 3 du §6.** L'audit mesure l'inverse de
l'inquiétude que j'y avais consignée : le seuil s est *inerte* — sur
toute la fourchette honnête [0,075 ; 0,950] GeV, la prédiction bouge de
128,26 à 128,44 (écart 0,24–0,38 %, S+ partout). Le choix s = 0,500
coûte ses bits descriptifs mais n'achète et ne perd rien. Le vrai point
de charge est ailleurs.

**Résultat central : la triade m_p/3 est l'unique pari structurel du
muscle micro.** Sensibilités : c (pole vs MS) ≤ 0,06 %, b ≤ 0,01 %,
t nul (fermé), s couverte ci-dessus. Mais u/d aux masses MS physiques :
prédiction 126,69 (0,99 %, bord du S+) ; tout-MS̄ : 126,57 → **1,08 %,
downgrade P**. Le muscle tient entier sur le seuil de confinement à
m_p/3 — précisément le pari que le sceau voulait structurel. L'audit le
confirme et le localise chirurgicalement.

**Comparaison canonique, avec réserve déclarée.** La valeur fermionique
canonique du Modèle Standard (3 boucles QED+QCD) vaut ≈ 128,95, écart
0,78 % à l'expérience — plus mauvais que les 0,35 % du modèle à seuils
discrets. Réserve honnête : le canon inclut la polarisation hadronique ;
la formule à seuils ne la contient pas, et la triade à 313 MeV (même
ordre que Λ_QCD ≈ 213 MeV) y fonctionne comme ancre infrarouge
effective. Le muscle est un modèle effectif à seuils dont l'accord bat
le calcul canonique nu — déclaré comme tel, pas vendu pour de la QFT.

**Verdict de l'audit : muscle micro renforcé.** Insensibilité démontrée
à 8 seuils sur 9 ; le neuvième identifié comme le pari unique ; comparaison
canonique favorable. Suite naturelle : chantier sur la triade elle-même
(m_p/3 vs Λ_QCD × coefficient ; lien avec la charge effective IR).

**Leçon de méthode.** Une comptabilité (D1b) avait désigné un faux
coupable (le seuil s) ; une mesure (D1c) a désigné le vrai (la triade).
L'ordre comptabilité → mesure → correction datée est le circuit complet
du remboursement de dette. Répéter.

