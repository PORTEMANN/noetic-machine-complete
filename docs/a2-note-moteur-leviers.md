# A2 — Moteur automatique de leviers : la carte de constitutivité du monopole

**Chantier A2 du programme de prospection — axe 1 (méthode).**
Artefacts : `a2_moteur_leviers.py` · `a2_moteur_leviers_verdict.json` · protocole gelé **LEV-ENG-1.0**.

## 1. Le problème

La discipline des leviers — *chaque mécanisme doit survivre à sa propre suppression* — était jusqu'ici appliquée **à la main** : l'expérimentateur choisit ses leviers, donc choisit partiellement ses résultats. A2 transforme la discipline en **moteur** : les composants de la structure candidate sont énumérés, chacun est ablaté binairement (cᵢ ∈ {0,1}), et la machine publie la carte complète de constitutivité — y compris contre l'intuition de l'expérimentateur.

## 2. Cible et protocole

Première cible : la fonctionnelle radiale du monopole SU(2) Georgi–Glashow (banc P0 du corpus) :

$$ C(\rho) = \int d\xi\; \Big[ c_1 K'^2 + c_2 \frac{(K^2-1)^2}{2\xi^2} + c_3 \frac{(\xi H' - H)^2}{2\xi^2} + c_4 K^2H^2 + c_5 \frac{\rho(H^2-1)^2}{4} \Big] $$

Chaque ablation repart du **même germe** (BPS approché) et du **même solveur** (L-BFGS-B, gradient discret exact) que P0 — zéro recalibration. Critères d'existence gelés : énergie finie, asymptotique correcte (|K|<0.05, |H−1|<0.05 au bord), cœur non effondré. **Contrôle tueur intégré** : à ρ = 0, ablater c₅ doit être strictement invisible (le terme est nul par construction) — sinon le moteur est bugué.

## 3. La carte mesurée (ρ = 1, C nominal = 1.30981 ✓ corpus)

| terme supprimé | C | monopole ? | classe |
|---|---|---|---|
| — (nominal) | 1.30981 | oui (cœur ξ=1.35) | — |
| c₁ cinétique de jauge | 0.96569 | oui | constitutif de valeur (ΔC = 26 %) |
| c₂ flux magnétique | 0.92848 | oui | constitutif de valeur (ΔC = 29 %) |
| c₃ cinétique covariante | 1.15742 | oui | constitutif de valeur (ΔC = 12 %) |
| c₄ couplage jauge–Higgs | 0.51371 | **non** | **CONSTITUTIF D'EXISTENCE** |
| c₅ potentiel de Higgs | 0.04853 | **non** | **CONSTITUTIF D'EXISTENCE** |

**Lecture structurelle** : la carte sépare nettement les **termes de masse** (c₄, c₅) des **termes de gradient/flux** (c₁, c₂, c₃). Sans c₄, le champ de jauge est sans masse : queue algébrique, l'asymptotique n'est plus atteinte. Sans c₅, le Higgs est sans masse : délocalisation complète, l'énergie s'effondre. *L'existence du monopole comme objet localisé repose sur les masses qu'il génère.* Les termes de gradient ne fixent que la valeur de C.

**Stabilité (intégration A1)** : les deux verdicts d'existence survivent au doublement de la boîte (XMAX 30 → 60 : non-existence stable — l'inexistence est structurelle, pas numérique) ; le verdict nominal et l'ablation c₂ sont stables sous raffinement DX 0.02 → 0.04.

## 4. Les trois prédictions de l'expérimentateur : 0/3 — publié

Trois prédictions avaient été pré-enregistrées avant exécution :

| prédiction | verdict | leçon |
|---|---|---|
| P1 — c₂ (flux magnétique) constitutif d'existence | **INFIRMÉE** | sans c₂, le couplage Higgs suffit à faire décroître K de 1 à 0 : le monopole survit (C = 0.928) |
| P2 — c₅ constitutif de valeur, pas d'existence | **INFIRMÉE** | c₅ est constitutif d'existence : c'est le terme de *localisation* |
| P3 — viriel stationnaire à 5 % sur les solutions | **INFIRMÉE** | la relation de Derrick exacte implique le secteur de jauge ; le « viriel » naïf E_h + 3E_pot n'est pas la bonne observable |

C'est le résultat central d'A2 : **le moteur corrige l'expérimentateur**. L'intuition humaine avait désigné le mauvais terme comme pilier d'existence (le flux magnétique, spectaculaire) et raté le vrai (la masse, discrète). Une discipline de leviers choisie à la main aurait confirmé l'intuition ; l'énumération systématique la tue. La pré-registration rend l'échec publiable au lieu d'être réécrit après coup.

## 5. Frontière mesurée : le point BPS n'est pas atteignable par relaxation

Le contrôle tueur a révélé une frontière du protocole P0 lui-même : **C(ρ=0) = 0.0485 ≠ 1**. À masse de Higgs nulle, l'infimum d'énergie n'est pas atteint sur boîte finie — le cœur glisse au bord (ξ = 30.0). Le point BPS est un **point d'invariance d'échelle** (mode zéro), non générique : la valeur C = 1 est exacte analytiquement mais la relaxation numérique ne l'atteint pas. Conséquence pour le corpus : tout verdict de P0–P4 à ρ = 0 obtenu par relaxation est à étiqueter *(verdict, sensible à la boîte)* — exactement le type d'entrée prévu pour le registre A4.

## 6. Ce que A2 change pour le corpus

- Toute structure candidate à ≥ 2 composants reçoit désormais sa **carte de constitutivité complète** (5 minimisations ici — coût marginal nul contre une intuition fausse).
- Les classes sont ternaires et publiées : *existence / valeur / invisible* — toute ablation « invisible » hors contrôle est une anomalie publiée.
- Le contrôle tueur (ablation structurellement nulle) est **constitutif** du moteur : il a immédiatement servi (frontière BPS).
- Prochaines cibles naturelles : la loi spectrale KO-6 (ablation des axiomes), le tube de flux P3, les familles Jastrow de P31–P33 (jonction avec A3).

**Falsifieur** : toute solution régulière à énergie finie exhibée pour les ablations c₄ ou c₅ tue la carte ; un contrôle ρ = 0 non invisible tue le moteur.

---

*A2 — LEV-ENG-1.0 · SHA-256 du script dans `a2_moteur_leviers_verdict.json` · zéro paramètre ajusté, germe et solveur de P0, prédictions pré-enregistrées.*
