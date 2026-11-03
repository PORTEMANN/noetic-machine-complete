# Fiche chantier Φ-DYN-2 partie 1 — Le générateur reconnu (Fricke comme charge conservée)

**Date :** 2026-11-03 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **PRÊTE À GELER — non scellée.** Aucune mesure n'a été lancée depuis cette fiche. Toute exécution exige le scellement de la section 3 (objets déclarés) et la signature de la section 8.
**Références :** NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE.md (v2, commit 4d657fb), T24, T41–T47, T55, NOTE-VINEN-T47-T51.md, NOTE-CREATION-MORT-T52-T54.md.
**Portée :** partie 1 seulement (reconnaissance de la trace map comme générateur + sous-test d'invariance adiabatique). La partie 2 (construction de la trace map du porteur seesaw) fait l'objet d'une fiche distincte, ultérieure.

---

## 1. Contexte et hypothèse

**Le diagnostic (NOTE v2, § I.2).** Le pont φ a une dynamique empruntée, pas dérivée : l'Acte IV mesure *dans* un flot GP déclaré. Le mot orphelin du lexique (T15) est le générateur.

**Le fait déclencheur (T24).** La trace map de Kohmoto — livrée par le pont φ lui-même — est un système dynamique discret à trois dimensions, à préservation du volume, unimodulaire SL(2,ℝ), dont l'invariant de Fricke est constant à 2e−16 le long des orbites. Une dynamique discrète avec une charge conservée est *déjà* en main ; elle n'a pas encore été reconnue comme générateur ni soumise au protocole de la maison.

**Hypothèse H-ΦDYN2a.** *La phénoménologie continue mesurée par l'Acte IV (structure de Cantor, arêtes de bandes à ratio φ, sauts de Lk) est la signature, à la limite, d'orbites de la trace map — non la propriété d'un flot imposé.* Et corollaire : l'invariant de Fricke est la première **charge conservée** de la machine au sens où la maison peut le tenir : non pas une charge de Noether (il n'y a pas de lagrangien — voir NOTE v2, § II.2, absorption de l'ex-D7), mais une charge *vérifiée le long des orbites* d'un générateur déclaré.

---

## 2. Question et sens charter

**Question :** la trace map, seule — sans équation de Schrödinger imposée, sans flot GP — reproduit-elle les signatures continues mesurées T41–T47 ?

**Sens charter :** classe (iii) — dériver le flot depuis les structures. La dynamique est produite par la machine, non empruntée.

**Discipline :** zéro paramètre ajusté, gel avant mesure, levier discriminant, échec publié. Cette fiche ne modifie aucun verdict existant.

---

## 3. Objets déclarés (à sceller avant tout run)

### 3.1 Le générateur

La trace map de T24, reprise **telle quelle** depuis la note T24 (convention d'invariant incluse — la forme vérifiée à 2e−16 est la référence canonique ; cette fiche ne la redéfinit pas, elle la cite). Le générateur est la map elle-même ; l'énergie E est son paramètre ; les orbites sont calculées en précision 64 bits, double reprise en 80 bits étendue sur 5 orbites de contrôle pour la signature numérique.

### 3.2 Grille de seeds (gelée)

- **S1** — orbites amorcées depuis les énergies des **arêtes de bandes** de T24 (N = 8 premières bandes, valeurs telle quelles depuis la note).
- **S2** — orbites amorcées depuis les **milieux de gaps** (même source).
- **S3** — orbites amorcées depuis un échantillonnage déclaré de l'intervalle spectral, pas constant ΔE déclaré = (E_max − E_min)/64, sans regard sur le résultat.
- Chaque seed produit une orbite de longueur L = 10⁴ itérations (déclaré).

### 3.3 Grille de déformations phason (gelée)

La chaîne Fibonacci est déformée par retournements de phason (flips locaux du mot) à densité déclarée ρ ∈ {0 (contrôle), 0.001, 0.01, 0.05, 0.15} — cinq valeurs, gelées, motivées par la littérature des quasicristaux désordonnés, aucune choisie après coup. Pour chaque ρ : 20 réalisations du désordre avec la graine de générateur aléatoire gelée **20261103**.

### 3.4 Observables (gelées)

| # | Observable | Définition | Source de comparaison |
|---|---|---|---|
| O1 | Conservation de Fricke | écart max de l'invariant le long de chaque orbite | T24 (2e−16) |
| O2 | Ratio d'arêtes | c_{N+1}/c_N sur les 8 premières bandes | T24 (→ φ) |
| O3 | Topologie d'orbite | bornée (spectre) vs divergente (gap) — taux de classification correct vs carte de bandes connue | T24 |
| O4 | Nombre de rotation | IDOS sur l'orbite, comparé à la densité d'états intégrée du banc | T24 |
| O5 | Entropie d'orbite | taux de Kolmogorov-Sinai estimé (pas de Bernoulli sur symboles d'itération) | pas de référence — mesure nouvelle |
| O6 | Robustesse phason | O2 et O3 vs ρ ∈ grille §3.3 | levier principal |

### 3.5 Sous-test d'invariance adiabatique (absorbé de l'ex-D7)

Pour les invariants de l'Acte IV mesurés dans le corridor — Q (T41), quantum de paroi 4 filaments (T47) — la question honnête est l'invariance sous **déformation lente des flots déclarés**, non une charge de Noether (pas de lagrangien). Protocole gelé :

- reprendre les runs corridor existants (données T41–T47, aucun nouveau run GP) ;
- appliquer une déformation lente et déclarée des paramètres du flot (rampe γ : γ₀ → γ₁ sur l'intervalle du run, loi linéaire, amplitudes Δγ ∈ {0.1, 0.5} gelées) aux séries temporelles d'invariants **déjà produites** par re-échelle paramétrique déclarée — pas de nouvelle simulation à ce stade ;
- critère pré-enregistré : si Q et le quantum de paroi sont constants (à la tolérance de T42, ±0.005) sous Δγ = 0.1 et Δγ = 0.5 → invariants adiabatiques du flot déclaré ; si une brisure apparaît sans singularité → non adiabatiques, écart publié.

**Limite honnête :** ce sous-test est une analyse à posteriori sur données existantes ; il n'a pas la force d'un run gelé avant mesure. Il sera rapporté comme tel, jamais au même titre qu'un verdict de classe (iii).

### 3.6 Tolérances (gelées)

- O1 : écart ≤ 1e−12 (double précision) attendu ; toute orbite à écart > 1e−9 est comptée comme **orbite non portée** (signature du gap, pas échec numérique — à distinguer explicitement dans le rapport).
- O2 : conforme si |c_{N+1}/c_N − φ| ≤ 0.02 sur les 6 dernières bandes.
- O3 : taux de classification ≥ 99 % exigé.
- Le seuil de réussite global est **pré-enregistré ici** : la partie 1 est tenue si O1 tient sur ≥ 95 % des orbites S1–S3, O2 conforme, O3 ≥ 99 %, et O6 fournit une réponse nette (robuste OU tué proprement — voir tueurs).

---

## 4. Programme en quatre paliers

**Pilier A — Re-vérification du générateur.** Recalculer les orbites T24 depuis la note (seeds S1–S3), vérifier O1–O4. Sortie : reproductibilité de T24 à la tolérance 3.6. **Effort : quelques minutes.**

**Pilier B — Phason (le levier principal).** Grille ρ §3.3, observables O1–O4 par ρ, 20 réalisations. Question : la structure à ratio φ survit-elle au désordre déclaré, et jusqu'à quel ρ ? **Effort : < 1 h.**

**Pilier C — Signature continue.** À partir des seules orbites (matrices SL(2,ℝ) que la map encode), reconstruire l'IDOS et comparer la hiérarchie d'échelles à celle mesurée dans le corridor T41–T47 (structure de Cantor, sauts). Critère : la carte d'échelles de l'orbite coïncide-t-elle avec la carte d'échelles du corridor dans les deux sens (orbite → corridor, corridor → orbite) ? **Effort : quelques heures.**

**Pilier D — Sous-test adiabatique (§3.5).** Analyse a posteriori des séries T41–T47. **Effort : < 1 h.**

---

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict si déclenché |
|---|---|---|
| T-1 Fine-structure | O2 conforme à ρ = 0 mais tué à ρ = 0.001 → φ est du réglage fin, pas du régime | H-ΦDYN2a **réfutée en partie** : le pont est un dictionnaire sensible aux perturbations — publié |
| T-2 Non-robustesse de blocking | O2 dépend du seuil/du mode de comptage des bandes (déclaration check interne) | calibration de fiche documentée, fiche corrigée, run gelé à nouveau |
| T-3 Orbites sourdes | O3 < 99 % : la map ne classe pas spectre/gap | réfutation propre du générateur — publié |
| T-4 Sélection a posteriori | tout critère modifié après observation des résultats | B3-FAIL de fiche, mort datée |
| Levier L-1 | densité phason ρ | axe principal de robustesse |
| Levier L-2 | longueur d'orbite L = 10⁴ vs 10⁵ (sur-échantillon de contrôle, 3 seeds) | convergence numérique |

**Leçon gravée applicable (T42) :** « on ne tue pas un entier en le frottant » — ici, tuer = montrer que les orbites n'ont pas les entiers comme attracteur. La grille phason est le frottement déclaré ; si les entiers meurent sous ρ = 0.001, ils étaient décorés, pas portés.

---

## 6. Verdicts possibles et consignation

1. **CONFIRMÉ (partie 1)** : critères §3.6 tenus, y compris une réponse nette en O6 → la trace map est promue générateur reconnu ; Fricke = première charge conservée vérifiée de la machine ; la partie 2 (trace map du porteur seesaw) est débloquée et mérite sa fiche.
2. **RÉFUTÉ** : T-1 ou T-3 déclenché → le pont φ reste un dictionnaire, et la maison sait *précisément pourquoi* — publié au même titre qu'un succès.
3. **CALIBRATION** : T-2 ou T-4 → erratum de fiche, version +0.1, scellement repoussé.

Consignation : NOTE-PHI-DYN-2-P1.md dans docs/, données brutes (orbites, CSV O1–O6) dans data/, verdict daté, leviers réglés en annexe.

---

## 7. Calendrier et coût

Exécution numérique pure (Python/NumPy, pas de donnée externe, pas de simulation GP nouvelle) : **une session**. Aucun téléchargement, aucune dépendance au-delà de l'existant. La partie 1 est le chantier le moins cher de la feuille Φ-DYN — c'est pourquoi il est premier.

---

## 8. Points de décision d'auteur (à trancher avant scellement)

1. **Graine phason 20261103** — valide ou à remplacer par une autre valeur déclarée ?
2. **Seuil de réussite §3.6 (95 % / 0,02 / 99 %)** — valide ou à resserrer/relâcher *avant* run ?
3. **Sous-test D (adiabatique, §3.5)** — le maintenir dans cette fiche ou le sortir en note autonome de moindre force épistémique ?
4. **Densités phason {0.001, 0.01, 0.05, 0.15}** — la grille est-elle la bonne échelle, ou faut-il une décade supplémentaire (ρ = 0.3) pour forcer la mort propre ?
5. **Nom de scellement** : Φ-DYN-2-P1 est le sigle de travail ; le verdict publié portera-t-il un numéro T (T70 ?) ou restera-t-il hors série Φ-DYN ?

---

*Cette fiche ne modifie aucun verdict, aucune carte gelée, aucune dette. Elle est la première pierre de la classe (iii).*
