# Campagne T2 — Q-KO6-T2-2026-09

**Statut : exécutée en local le 09/09/2026 ; publiée le 09/09/2026
(pause de tri, décision d'auteur).**

## Question

Sous la table C-KO6-A3b (datée : J²=+1, Jγ=+γJ, JD=−DJ), existe-t-il
(D, J, γ) de taille n **impaire** avec A = ℂ⊕ℂ (deux scalaires) et
**ordre 1 non vacuous** — et dans quelle classe d'action de J sur les
secteurs ?

Suite déclarée de T1 (qui a tranché la taille impaire à UN scalaire :
existence dès n=3, ordre 1 vacuous). Nouvelle fiche gelée, pas un
critère déplacé.

## Réponse mesurée

**OUI en préservation et en mélange de secteurs ; NON en échange.**

| n | classe | combos (P,J₀) | avec D≠0 | D total |
|---|--------|---------------|----------|---------|
| 3 | préservation | 112 | 32 | 64 |
| 3 | échange | **0** | 0 | 0 |
| 3 | mélange | 32 | 32 | 64 |
| 5 | préservation | 8 896 | 6 496 | 36 608 |
| 5 | échange | **0** | 0 | 0 |
| 5 | mélange | 7 424 | 7 424 | 87 040 |
| 7 | préservation | 566 720 | 506 400 | 18 143 232 |
| 7 | échange | **0** | 0 | 0 |
| 7 | mélange | 985 600 | 985 600 | 114 993 152 |

Morsure de l'ordre 1 (mesurée) : à n=7, 6 749 568 orbites libres sans
filtre → 4 416 896 avec ordre 1 (≈ 35 % tuées). L'ordre 1 n'est donc
pas vacuous à deux scalaires — et l'impair survit.

## Lemmes pré-enregistrés — les deux confirmés

- **Lemme A (échange ⇒ n pair)** : J₀ P J₀ = Q avec Jγ=+γJ impose des
  rangs de secteurs égaux dans chaque chiralité, donc a et b pairs,
  donc n pair. Mesuré : **0 combo échangeant** sur ~1,6 M combos à
  n=3,5,7. *Un triplet KO-6 impair à deux scalaires ne peut pas avoir
  J échangeant les scalaires.*
- **Lemme B (préservation)** : un secteur bi-chiral suffit — existence
  constructive dès n=3, confirmée.

## Contrôles gelés

- Recoupement par énumération brute à n=3 (toutes P, tous J₀, tous D,
  vérificateur matriciel complet) : **3/3 classes conformes**
  (64 / 0 / 64) ;
- exemplaires exhibés vérifiés matrice par matrice (vérificateur A3b
  étendu, tolérance figée 1e-9) : **112/112** ;
- méthode des orbites filiative de T1, filtre ordre 1 dérivé et déclaré
  (Q′ = J₀QJ₀ reste diagonale ; condition par orbite
  (P_x=P_y) ∨ (P_{σx}=P_{σy})).

## Conséquence mesurée pour « 2+2+3 = 7 » (AXIOMES.md)

La matrice de multiplicités m = [[0,2],[2,3]] a des auto-multiplicités
asymétriques (0 ≠ 3) : **aucun J échangeant les secteurs ne peut
s'y adapter** (cohérent avec le lemme A — l'échange exigerait en outre
n pair). Aux rangs (2,5) et n=7, la machine trouve des triplets
**préservant ou mélangeant** les secteurs, dans les 12 découpages de
chiralité, tous vérifiés. Donc : le « 7 » n'est **pas exclu** comme
triplet KO-6 par la parité — mais toute version à structure réelle
échangeant les scalaires (type modèle standard fini, où J échange
particules/antiparticules) est **exclue en taille impaire**, lemme à
l'appui. Le statut de « 7 » dépend donc entièrement de la structure
réelle choisie — et ce choix doit désormais être déclaré dans toute
fiche qui l'invoque.

## Régularité mesurée (carnet → devenue T4)

100 % des combos mélange à n=5 et n=7 admettent un D≠0
(7 424/7 424 ; 985 600/985 600). Régularité mesurée ici, **prouvée en
T4** (lemme de mélange, note et verdict T4 publiés le 09/09/2026).

## Artefacts

- `src/t2_ko6_ordre1_impair.py`
- `data/t2_ko6_ordre1_impair_verdict.json`
- empreintes complètes (octets du dépôt) : `data/t1_t2_t4_shasums.txt`
