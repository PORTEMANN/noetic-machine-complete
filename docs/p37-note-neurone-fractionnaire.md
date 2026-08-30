# P37 — Le neurone fractionnaire éprouvé : la mémoire n'est pas l'excitabilité

**Patrice Portemann — corpus Machine Noétique, chantier P37**
Protocole gelé FRAC-NEU-1.0 · zéro paramètre ajusté · artefacts SHA-256
30 août 2026

## Verdict

**PARTIEL.** Le neurone fractionnaire (intégrateur fuyard d'ordre α,
Atangana–Baleanu–Caputo : D^α V = −V + I) est **réfuté comme modèle du
spike** — mais pour une raison nouvelle dans le corpus : non pas la
staticité (σ, 0 degré de liberté), mais la **linéarité**. Il possède un
état — une mémoire distribuée de dimension infinie — et pourtant aucun
seuil, aucun tout-ou-rien, aucun train. Simultanément, il est **éprouvé
comme modèle de la mémoire** : la queue algébrique t^{−α} est mesurée,
constitutive, et sa fermeture de rang fini coûte cher.

## D, S, L

- **D** : le neurone biologique de référence (Hodgkin–Huxley figé, repris
  de P35) + la définition exacte de la dynamique fractionnaire
  (Mittag-Leffler E_α(−t^α), représentation spectrale de Pollard).
- **S** : le neurone fractionnaire — la signature propre de l'auteur
  (Topological-Fractional-AI), ici pour la **première fois exécutable**
  dans le corpus, rejouable, zéro paramètre ajusté.
- **L** : quatre leviers discriminants — α → 1 (contrôle), suppression du
  noyau (queue algébrique constitutive ?), excitabilité (P35 rejoué sur
  un candidat qui a un état), fermeture (coût de rang fini de la mémoire).

## Résultats mesurés

| Critère | Mesure | Verdict |
|---|---|---|
| T0 | Mittag-Leffler exacte : err 0.00e+00 (α=1 vs e^{−t}), 2.64e-16 (α=½ vs e^t erfc(√t)) | PASS |
| C1 | levier α → 1 : réduction exacte à l'exponentielle | PASS |
| C2 | pentes log-log de la relaxation sur [20, 200] ms : −0.253 / −0.493 / −0.837 pour α = 0.3 / 0.5 / 0.8 (attendu −α) ; exponentielle morte à t = 20 ms | PASS |
| C3 | superposition exacte (écart 0.0), relaxation monotone, **0 spike** sous tout courant constant | réfutée comme spike |
| C4 | 100 ms après une impulsion de 10 ms : queue fractionnaire 2.59e-3 (mesurable), queue exponentielle 3.7e-44 (morte) | PASS |
| C5 | ASH-lite : σ = (0, 0, 0) · fractionnaire = (Rc 0.53, Rtop 1, 0) · HH = (0.31, 4, 0.39) — trois signatures disjointes | PASS |
| C6 | meilleur double-exponentiel (grille déclarée τ ∈ {1,3,10,30,100}, w ∈ {0.2,…,0.8}) contre le noyau α = ½ : erreur max **0.152** — rang 2 refusé | PASS |

## B3-FAIL — échecs publiés

**Candidat.** Le neurone fractionnaire comme modèle du spike : réfuté par
la linéarité mesurée (superposition exacte). Le motif est publié
précisément : ce n'est pas l'absence d'état (F2) mais l'absence de seuil.

**Internes (la Machine s'est éprouvée elle-même, quatre fois).**

1. *E_α v1* (série + asymptotique, jonction z = 2) perdait 7e-3 :
   l'asymptotique de E_1(−t) est identiquement nulle alors que
   e^{−5} = 6.7e-3. Corrigé par la représentation de Pollard.
2. *Pollard v2* rappelée avec le mauvais exposant (e^{−r·t^α} au lieu de
   e^{−r·t}) : exacte par coïncidence en t = 1, réfutée par les contrôles
   T0 hors de ce point. Corrigée (paire de Laplace s^{α−1}/(s^α+1)).
3. *Critère C4 v1* (rétention > 20 % à Δ = 100 ms) : réfuté par la
   mesure (la queue t^{−1/2} retombe à 0.3 % de la fin d'impulsion) —
   remplacé par la mesure absolue des queues.
4. *Critère C5 v1* (Rtop = 0 exigé pour le fractionnaire) : réfuté — un
   spectre 1/f monotone produit un pic local en bord de bande. Critère
   corrigé sur le triplet complet (Rc, Rtop, Rdyn).

## Ce que le chantier apprend

**Le neurone a deux axes orthogonaux, désormais mesurés séparément.**

| Axe | Objet minimal | Dimension | Chantier |
|---|---|---|---|
| Excitabilité (seuil, tout-ou-rien, horloge) | phase sur S¹ | 1D (θ-neuron) | P35 |
| Mémoire (adaptation, longue portée) | noyau Mittag-Leffler | ∞D exact, rang fini approché | P37 |

Le comptage des degrés de liberté s'enrichit d'une case nouvelle :
σ = 0D · θ = 1D(S¹) · Izhikevich = 2D · HH = 4D · fractionnaire = **∞D**
(noyau distribué). La mémoire exacte est infiniment coûteuse — c'est
pourquoi le vivant ne l'implémente pas : il empile des canaux lents, une
approximation de rang fini du noyau, dont P37 mesure le coût (rang 2
insuffisant : 0.152 d'erreur sur grille déclarée).

La conjecture des frontières v2 (« défaut de comptage des ddll — déficit
ou mode non contraint ») couvre désormais **7/7 points** du domaine
déclaré, F11 entrant dans la case « déficit » : le fractionnaire possède
la mémoire mais pas l'excitabilité (il manque la phase S¹), et sa
version biologique exige l'ajout de variables lentes.

**Falsifieur.** Toute trajectoire fractionnaire linéaire exhibant un
spike tout-ou-rien ou un train périodique sous courant constant tue le
verdict.

## Artefacts

- `p37_neurone_fractionnaire.py` — SHA-256 `248fabdea7655f0b…`
- `p37_neurone_fractionnaire_verdict.json`
- `p37_neurone_fractionnaire.png` (4 panneaux : noyaux, échelons,
  mémoire d'impulsion, ASH-lite)
- registre A4 mis à jour (11 entrées, SHA `41f16cfbea6e745a…`), A5 rejoué
  (SHA `cbc6df7fb52beef3…`)

*Effet de bord sur F10 : P37 fournit la première dynamique fractionnaire
exécutable du corpus. L'entrée F10 reste ouverte — le script du modèle
Topological-Fractional-AI (84.1 % AUC) reste à publier.*
