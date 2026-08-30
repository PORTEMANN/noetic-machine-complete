# Note M2 — Métrologie de la liberté : le registre devient une proto-algèbre

**Patrice Portemann — Machine Noétique, série M (méta-chantiers)**
31 août 2026 — travail local (publication GitHub différée, décision explicite)

## 1. Objet

Le registre des frontières (A4, 18 entrées) porte depuis sa création un
comptage ddll par entrée (déficit / équilibre / mode non contraint) —
mais comme *étiquette*, non comme *structure*. M2 extrait la structure
algébrique que ces coûts mesurés portent réellement, avec des lois
candidates pré-enregistrées et tuables. Protocole MÉT-LIB-1.0 gelé.

## 2. La structure extraite

**La mesure d'abord.** Chaque frontière reçoit un coût de fermeture
d ∈ ℕ̄ = ℕ ∪ {∞}, ou ∅ (hors-domaine — la mesure ne s'applique pas ;
**∅ n'est pas 0** : la clôture d'hygiène F18 ne coûte pas « zéro degré de
liberté », elle est *hors mesure*). Extraction par table figée, déclarée
entrée par entrée avec la phrase de justification du registre — jamais
parsée.

**Les classes.** Équilibre (d = 0 : rien n'est payé — F7 mesure de
protocole, F14 théorème de structure pure) · déficit (0 < d < ∞) ·
mode non contraint (d = ∞ : F5, surplus indéterminé) · et la surprise
mesurée : les **familles paramétrées** (F12 : d(m) = 2m ; F13 : d(n) = n)
— le non-borné existe aussi en régime fini croissant.

**La structure.** Monoïde des coûts (ℕ̄, +, 0) avec ∞ absorbant ;
composition ⊕ = conjonction de chantiers indépendants ; ordre ⊏ =
dépendance de fermeture.

## 3. Les lois mesurées (verdict : SUCCÈS 5/5)

| Loi | Énoncé | Résultat |
|---|---|---|
| **L1** | Cohérence de la mesure : table figée vs verdicts ddll publiés | **TENUE — 18/18** : le comptage publié est déterministe et total sur le domaine |
| **L2a** | Toute fermeture ponctuelle mesurée a d ≤ 1 | **TENUE** — image mesurée = {0, 1} (7 fermetures ponctuelles) : *le corpus n'a jamais payé 2* |
| **L2b** | Il existe des familles à coût non borné | **TENUE** — F12 (d=2m), F13 (d=n) : la liberté croît avec la tâche |
| **L3** | Additivité sur les conjonctions déclarées | **TENUE — 3/3** (P13 = α⊕confinement : 0+0 ; F7 = P13⊕P22 : 0+0 ; F14 = pont⊕quiver⊕Molien : 0+0+0) |
| **L4** | L'ordre de fermeture ⊏ est un ordre partiel | **TENUE** — acyclique ; 4 dépendances déclarées, chaîne maximale 1 (mesurée, publiée telle quelle) |
| **L5** | A5 algébrisée (prospective) | **en vigueur** — voir §4 |

## 4. Ce que l'algèbre change pour A5

La conjecture v1 (« toute frontière = déficit »), réfutée par F5/F7/F14,
se reformule proprement dans la structure :

> **L5 (loi prospective, falsifieur exécutable)** : sur le domaine mesuré,
> toute frontière *physique* nouvelle tombe en déficit ou en mode non
> contraint ; l'équilibre n'advient que par théorème de structure pure ou
> mesure de protocole.
> **Falsifieur** : la prochaine entrée physique mesurée en équilibre
> d'origine prédictive tue L5.

Répartition mesurée qui la fonde : 6 déficits ponctuels + 2 familles +
2 déficits déclarés non mesurés + 1 mode non contraint + 2 équilibres +
5 hors-domaine.

## 5. Limites honnêtes

- C'est une **proto-algèbre** : le monoïde (ℕ̄, +) est commutatif et
  trivial en soi ; la valeur est dans la *mesure* d (extraite du corpus,
  cohérente à 18/18) et dans les lois tuables, pas dans la richesse de
  la structure.
- L'ordre ⊏ est encore pauvre (4 arêtes, chaîne maximale 1) — il
  s'enrichit à chaque fermeture future ; sa profondeur est une métrique
  de maturité du corpus.
- Les coûts paramétrés (F12, F13) sont déclarés depuis les justifications
  du registre, pas recalculés : L2b tient sur la parole du corpus — le
  recalcul de d(m) en exécutant P36 à m variable est la suite déclarée.

## 6. Suites déclarées

1. **M2b** : recalculer d(m) en exécutant P36 à m variable — promouvoir
   F12 de « famille déclarée » à « famille mesurée » ;
2. Enrichir ⊏ à chaque fermeture (F4, F5, F11, F16, F17 ouvertes) ;
3. L5 est prospective : chaque nouvelle entrée du registre la confronte.

**Verdict M2 : SUCCÈS 5/5** — la structure est extraite, les lois
tiennent sur le corpus figé, le falsifieur prospectif est armé.

## Artefacts (locaux, publication différée)

`m2_metrologie_liberte.py` (sha `52582c7d…`) ·
`m2_metrologie_liberte_verdict.json` · registre lu et vérifié
(SHA `28a486b0…`).

---

## Addendum M2b (même jour) — la famille F12 est mesurée, et l'homomorphisme avec

Exécution de la famille d'oscillations de P36 (tente de Telgarsky,
grille figée 100 001 points, constructions dérivées à zéro
apprentissage) — protocole MÉT-LIB-1.1 gelé, verdict `6dfef08f…`,
**SUCCÈS 4/4** :

| Loi mesurée | Contenu | Statut |
|---|---|---|
| d_profondeur(m) = 2m | construction exacte pour m = 1..8 | 8/8 |
| d_profondeur-2(m) = 2^m | minimalité **certifiée par comptage** (w Heaviside ≤ w sauts ; 2^m seuils demi-dyadiques mesurés) | 8/8 |
| **Homomorphisme** | d(t^m ∘ t^k) = d(m) + d(k) — la composition des tâches s'envoie sur l'addition des coûts | **26/26 compositions exactes** |
| **Conversion** | d_2couches(m) = 2^(d_prof(m)/2) — la même liberté coûte linéairement en profondeur, exponentiellement en largeur | 8/8 |

F12 passe de « famille déclarée » à **famille mesurée**. Le point fort :
la mesure de coût n'est pas une étiquette par chantier mais un
**homomorphisme** de la composition des tâches vers (ℕ, +) — vérifié
exécutablement — et le choix de réalisation (profondeur vs largeur) est
régi par une loi de conversion exacte (log₂). C'est le premier contenu
algébrique non trivial de la métrologie de la liberté, mesuré et non
postulé.

---

## Addendum M2c (même jour) — enrichissement de ⊏, confrontation de L5

Protocole MÉT-LIB-1.1…1.2, verdict `4e996ea8…`, **SUCCÈS 4/4** :

- **A — famille parité mesurée (F19)** : d(n) = n — constructions
  dérivées profondeur-2 exactes sur les 2^n points (n = 2..8), LP
  profondeur-1 infaisable (n = 2..6). Nouvelle entrée au registre
  (physique, fermée sur la famille déclarée ; minimalité en profondeur 2
  déclarée non prouvée).
- **B — L3 promue** : l'additivité n'est plus seulement déclarée, elle
  est **mesurée sur familles** — parité_n ⊗ oscillation_m : d = n + 2m,
  9/9 couples exacts.
- **C — ⊏ enrichi** : 7 arêtes (3 nouvelles, chacune justifiée publiée :
  F1⊏F13 harnais LP hérité, F16⊏F17 ReN proscrit, F14⊏F8 racine
  arithmétique commune), ordre toujours acyclique, profondeur max 1
  (mesurée).
- **D — L5 confrontée** : F19 est la première frontière mesurée après
  l'armement de L5 ; classe mesurée : **déficit** (famille paramétrée) →
  **L5 tient**. Le falsifieur reste armé pour la suivante.

Registre local : **19 entrées** — 8 fermées / 5 ouvertes / 6 partielles,
SHA `b5cbd5cd…` ; A5 réévaluée mécaniquement : v2 couvre 12/14 (F19,
déficit, est couverte), v1 toujours réfutée par F5/F7/F14.
Publication GitHub toujours différée.

---

## Addendum M2d (même jour) — la surface de coût : la liberté a une géométrie

M2b avait mesuré deux réalisations pures (profondeur m → 2m ; largeur →
2^m). M2d (protocole MÉT-LIB-1.3, verdict `8b6802ec…`, **SUCCÈS 4/4**)
mesure la surface complète : à k couches, la couche i réalise t^{j_i}
d'un coup (2^{j_i} unités ReLU à poids entiers dérivés, breakpoints
dyadiques), et t^m = t^{j_1} ∘ … ∘ t^{j_k} pour toute composition.

| Loi | Contenu mesuré | Statut |
|---|---|---|
| Surface | d(m, k) = Σ_i 2^{j_i} sur split équilibré | **36/36 cellules exactes** |
| Bornes | d(m, 1) = 2^m et d(m, m) = 2m (M2b récupéré comme cas extrêmes) | 8/8 |
| Optimum | **d*(m) = 2m** pour m = 1..8 — la profondeur n'est jamais battue ; plateau d'optimalité mesuré (m = 8 : tout k ∈ [4, 8] donne 16) | table publiée |
| Cohérence | homomorphisme M2b vérifié le long des chemins profonds | 6/6 |

**Lecture.** Le coût de la liberté dépend du *chemin* de fermeture, avec
une loi exacte et un optimum mesuré : d*(m) = 2m. Le plateau de
m=8 — quatre chemins minimaux distincts de même coût — fait écho à T4
(non-unicité de la classe minimale) sans l'égaler : c'est une remarque
mesurée, pas un théorème. La métrologie de la liberté dispose désormais
d'une **géométrie des coûts** : monoïde (M2), homomorphisme (M2b),
ordre enrichi et loi prospective confrontée (M2c), surface et optimum
(M2d).

**Série M2 complète (local)** : M2 5/5 · M2b 4/4 · M2c 4/4 · M2d 4/4 —
prête pour la publication groupée.

---

## Addendum M2e (même jour) — copie certifiée minimale, tri mesuré, L5 ×2

Protocole MÉT-LIB-1.4, verdict `aa518fbf…`, **SUCCÈS 3/3** :

- **Copie (F13 promue)** : d_copie(n) = n non seulement mesuré
  (exhaustif V=8, n=2..6) mais **certifié minimal** — la validité sous le
  readout du corpus exige la dominance diagonale stricte (nécessité
  mesurée) ; Lévy–Desplanques (cité) donne rang n ; les scores
  bilinéaires de rang ≤ r imposent r ≥ n ; one-hot atteint r = n.
  Le chemin candidat bon marché (scores quadratiques rang 3) est
  **réfuté par exécution** sur les séquences à doublons (M2e-A2,
  B3-FAIL interne publié) — le registre porte l'addendum.
- **Tri (F20, famille neuve)** : réseau de Batcher dérivé, exactitude
  exhaustive (V=4 n≤5, permutations et binaire n≤8) ; coûts mesurés
  1, 3, 5, 9, 12, 16, 19 — **exactement à la borne ⌈log₂ n!⌉ jusqu'à
  n=4**, ratio ≤ 1,19 ensuite. Classe : déficit → **L5 survit à sa
  seconde confrontation**.
- Registre local : **20 entrées** (9 fermées / 5 ouvertes / 6
  partielles), SHA `bd592a8a…` ; A5 réévaluée : v2 couvre 13/15 (F19 et
  F20, déficits, couvertes), v1 toujours réfutée par F5/F7/F14.

La métrologie dispose maintenant d'un **certificat de minimalité** (le
premier : la copie, via un théorème d'algèbre linéaire) — le coût n'est
plus seulement mesuré, il est prouvé incompressible sur sa classe de
réalisation.
