# Note de chantier — T66 : Lorenz-modulaire, l'arithmétique du pont
Ghys rejouée machine-side

**Date :** 2026-10-31 · **Tiroir :** banc (clavier méso) ·
**Verdict :** `data/t66_ko6_lorenz_modulaire_verdict.json` (2/2).
**Filiation :** T41–T45 (entiers topologiques, templates, reconnexions)
· Ghys, *Knots and Dynamics* (2007) · NOTE-DETTE-D1 (la Classe A comme
standard) · la lecture du 31/10/2026 (question de l'utilisateur).

---

## 1. Ce que le chantier mesure

Pour chaque classe hyperbolique primitive de SL(2,ℤ) sous borne de
trace déclarée (t ≤ 12), le symbole de Rademacher Ψ(γ) — qui vaut, par
le théorème de Ghys, le nombre d'enlacement du nœud modulaire avec le
trèfle manquant (S³\trèfle ≅ SL(2,ℤ)\SL(2,ℝ)) — est calculé par deux
algorithmes indépendants à arithmétique exacte : somme de Dedekind
directe (O(c), Fractions) et chaîne de réciprocité (Euclide). L'accord
des deux voies est le critère ; la relation de quasi-morphisme
Ψ(γ²) = 2Ψ(γ) est le levier.

## 2. Résultats (verdict 2/2)

- **27 classes primitives** énumérées par les formes quadratiques
  réduites de discriminant t²−4 (convention de réduction déclarée ;
  contrôle croisé : h⁺(12) = 2, h⁺(5) = 1 — accord avec les nombres de
  classes étroits réels connus).
- **Accord exact des deux pistes sur les 27 classes** (égalité des
  Fractions, zéro flottant dans tout le chantier).
- **Ψ(γ²) = 2Ψ(γ) vérifiée** sur toutes les classes sous borne.
- Famille témoin : γ = (1, n; 1, n+2)·(forme) donne Ψ = t — les
  entiers d'enlacement sortent des matrices, pas d'une table.

## 3. Honnêteté de statut

Cette passe rejoue l'**arithmétique** du pont Ghys par deux voies
indépendantes ; elle ne rejoue pas encore la **correspondance
géométrique** (le comptage des mots L/R du template de Lorenz,
Σεᵢ = Ψ, Rademacher–Grosswald eq. 70) — convention à sourcer en
passe 2 avant tout run. Le chantier reste ouvert sur ce volet, comme
déclaré dans la fiche gelée.

## 4. Place dans le corpus

C'est la première fois que la machine rejoue un pont **prouvé
ailleurs** : jusqu'ici elle a scellé ses propres ponts (φ, entiers
topologiques, seuils habillés) ; ici elle vérifie, dans sa discipline
(arithmétique exacte, critères tuables, verdict auto-empreinté), un
isomorphisme du continu vers le discret qu'elle n'a pas conjecturé.
Le clavier méso (T41–T45) y gagne son cousin le plus profond : les
nombres d'enlacement de Lorenz sont des entiers « inusables par
frottement, tués par reconnexion » — exactement la catégorie mesurée en
octobre, ici à la source même où le chaos devient arithmétique.

*Révision uniquement par note datée. Script : `src/t66_ko6_lorenz_modulaire.py`
(sha256 dans le verdict).*

## Passe 2 (2026-10-31) — la voie géométrique : ECHEC productif

Script : `src/t66b_ko6_lorenz_template.py` · verdict :
`data/t66_ko6_lorenz_modulaire_p2_verdict.json` · **ECHEC gelé 2/2→ECHEC
(3e voie), avec découverte**.

La piste C (somme alternée des chiffres de la fraction continue du point
fixe attractant — le comptage template Σεᵢ au sens de Rademacher–
Grosswald eq. 70, convention sourcée avant run) n'accorde pas tel quel
avec Ψ : **écart constant 3 sur 26 des 27 classes** — et 2 sur une
seule, la classe au mot trivial (tr = 3, γ = (1,1,1,2), période CF [1]).

Lecture, non scellée : l'offset 3 est compatible avec **pq/2 = 3 du
nœud manquant T(2,3)** — dérivation possible depuis la convention
sourcée ψ_{p,q} à poids 2pq (= 12 pour SL(2,ℤ), le 12 de notre propre
définition de Ψ). Hypothèse structurelle, à dériver proprement en
passe 3, critère gelé *avant* le run ; l'exception à période [1] reste
déclarée, non ajustée. La règle doctrine est appliquée à la lettre : le
critère figé donnait 27/27 sur une variante non corrigée, il donne
ECHEC, il reste ECHEC dans le verdict — **aucune rétro-ingénierie**.

Valeur de l'échec : la constante 3 est sortie des données entières
elles-mêmes, uniforme sur 26 classes indépendantes — c'est exactement
le genre de signal (offset structurel universal, exception de bord
publiée) qu'un banc honnête doit laisser parler plutôt que le noyer
sous un ajustement. La passe 3 est ouverte avec sa règle : offset pq/2
dérivé, exception de bord déclarée, critères gelés avant exécution.
