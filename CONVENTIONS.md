# CONVENTIONS.md — registre des conventions datées

> Règle d'usage (permanente) : **un mot = un objet**. Toute convention utilisée par un
> script, un verdict ou une note DOIT être nommée ici, datée et citée par son identifiant
> (ex. « table C-KO6-A3b »). Ajouts en addendum seulement — aucune convention n'est
> réécrite silencieusement (politique « conserver les versions »).

## C-KO6 — Tables de signes KO-dimension 6

| ID | J² | JD | Jγ | Statut | Attestée dans |
|----|----|----|----|--------|----------------|
| **C-KO6-L1** (2026-08, papier L1) | +1 | JD = +DJ | Jγ = −γJ | Table dite « usuelle » (géométrie finie du Modèle standard) | `spectral-triple-minimality/src/utils.py` (docstring), `paper/main.tex` |
| **C-KO6-A3b** (2026-08-31, gelée) | +1 | JD = −DJ | Jγ = +γJ | **Table de travail du vérificateur matriciel** | `src/a3b_ko6_verificateur.py`, `data/a3b_ko6_verificateur_verdict.json` |
| « (J_F γ_F)² = −1 » (texte F4 gelé) | — | — | — | **Coquille publiée** : incompatible avec J² = +1 et Jγ = +γJ (alors (Jγ)² = +1). Conservée comme artefact daté, non comme convention. | texte gelé du registre F4 ; incompatibilité mesurée par A3b |

**Conséquence mesurée.** Le lemme de parité (Jγ = −γJ, J inversible ⇒ J échange H⁺ et H⁻
⇒ dim H paire) n'est valable que sous **C-KO6-L1**. Sous **C-KO6-A3b**, J préserve les
secteurs de chiralité et une dimension impaire n'est pas exclue par ce lemme.
**Le statut de tout candidat de dimension impaire (ex. dim H = 7) dépend donc de la table
choisie — et la table doit être dite.** Changer Jγ décide à lui seul du statut du 7.

⚠️ **Point de décision ouvert (2026-09-06)** : C-KO6-L1 et C-KO6-A3b diffèrent sur les
deux signes JD et Jγ. La table canonique du corpus reste à choisir explicitement ; en
attendant, tout verdict cite sa table par ID. Toute prétention de minimalité doit en outre
être vérifiable matrice par matrice (voir `AXIOMES.md`, test unique).

## C-R — Définition de l'entier R

- **Usage historique** (T1, papier L1) : « dim H_F ≥ 2R+1 » avec R = 3 ⇒ 7. Aucune formule
  machine R(γ, J, m) n'est fournie dans L1 : l'inégalité est **non évaluable** par le banc.
- **Définition proposée** (note de lecture sept. 2026, à valider) : **R = rang du bloc
  Yukawa P₊ D P₋**.
- **Statut : OUVERT.** Tant que C-R n'est pas gelée, aucune borne « 2R+1 » ne peut être
  signée par la machine.

## C-BORNES — Fenêtres d'énumération

- **C12.1 / amendement Krajewski** : m_ij ≤ 3, k ≤ 3, dim H_F ≤ 24 (attesté dans L1, A3, A3b).
- **Fenêtre F4** : k = 2, dim = 5 → 60/256 matrices retenues (verdict F4, 3/3).
- **Coût restant** : k = 3 → 4 723 712 matrices (espace mesuré par A3b).
- **Règle** : les bornes sont des **paramètres de classe** — elles fabriquent l'espace
  compté. Un compte n'est présenté comme invariant que si sa fenêtre est citée avec lui.

## C-COMPTE — Invariants de comptage

Trois proxys de « bandes » attestés (tamis A3), donnant des comptes différents sous la
même cible « 7 » :

| Proxy | Définition | Max atteignable | Compte sous cible 7 |
|---|---|---|---|
| `bands_lignes` | lignes non vides de m | 3 | 0 |
| `bands_paires` | paires de lignes | 6 | 0 |
| `bands_entrees` | entrées non nulles | 9 | 7 200 |

**Aucun de ces proxys n'est le spectre de D.** Règle : le nom du proxy accompagne toujours
le nombre ; un invariant ne dépend pas d'un identifiant de variable.

---

## C-MACHINES — Les deux classes de machines (daté 07/09/2026)

La classe d'architecture et l'opérateur de verdict, articulés :

- **MDU (Machine Dynamique Unifiée)** — la classe d'architecture (définie le 12/01/2026,
  art. « Systèmes complexes II ») : elle **produit et classe** les structures candidates
  (7 plans, adaptateurs par échelle, invariants bornés). Dépôt : `noetic-mdu`.
- **La machine à éprouver** (« sixième classe », l'opérateur de verdict) : elle **statue**
  sur les structures que la MDU achemine — protocole figé, levier discriminant, artefacts
  hashés. Dépôt : `noetic-machine-complete` (principal).

Règle : la MDU alimente, la machine à éprouver statue ; aucune fiche ne sort de la MDU
sans falsifieur, aucun verdict sans levier. (Articulation proposée lors de la création de
noetic-mdu ; enregistrée ici le 07/09/2026.)


*Registre ouvert le 2026-09-06, en réponse à la note de lecture « Incohérences internes du
corpus Portemann » (sept. 2026). Addenda seulement.*