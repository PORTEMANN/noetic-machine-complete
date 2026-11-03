# Fiche chantier Φ-DYN-2 partie 1 — Le générateur reconnu (Fricke comme charge conservée)

**Date :** 2026-11-03 · **Version :** 1.1 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.1** (erratum de la v1.0 après le run 1 : verdict CALIBRATION, trois défauts de rédaction documentés — voir §6.3 et §8 v1.1). Les corrections portent sur les **références d'implémentation** et la **fenêtre O2** (retour au protocole canonique T24) ; aucune tolérance numérique ne change de valeur. Toute exécution doit suivre cette version à la lettre ; tout écart la tue (T-4). Toute modification ultérieure exige une version +0.1 et une note de changement datée.
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

La chaîne Fibonacci est déformée par retournements de phason (flips locaux du mot) à densité déclarée ρ ∈ {0 (contrôle), 0.001, 0.01, 0.05, 0.15, 0.3} — **six valeurs, gelées** (la valeur 0.3 ajoutée au scellement, point 4 de la section 8), motivées par la littérature des quasicristaux désordonnés, aucune choisie après coup. Pour chaque ρ : 20 réalisations du désordre avec la graine de générateur aléatoire gelée **20261103**.

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

### 3.6 Tolérances (gelées — v1.0, références v1.1)

- O1 : écart ≤ 1e−12 (double précision) attendu ; toute orbite à écart > 1e−9 est comptée comme **orbite non portée** (signature du gap, pas échec numérique — à distinguer explicitement dans le rapport). **Référence v1.1 : l'échantillonnage aveugle de [−2,5 ; 2,5] touche majoritairement des gaps (le spectre de Cantor y est de mesure nulle) — le taux de portées s'entend donc *parmi les seeds classées bandes par la référence exacte (O3)*, seuil ≥ 95 % des seeds de bandes.**
- O2 : **conforme si les 3 derniers ratios (niveaux 12, 13, 14 — fenêtre canonique reprise verbatim de T24) sont dans φ ± 0,02 ET que la récursion des comptes c_N ≈ c_{N−1}+c_{N−2} tient à ±4** (les deux critères validés de T24 ; la fenêtre 7–14 de la v1.0 était un défaut de rédaction — la convergence c_{N+1}/c_N → φ est lente et les premiers niveaux en dévient).
- O3 : **référence exacte v1.1 : seed classé « bande » ssi limsup_{N ≤ 120} |x_N(t)| ≤ 1, calculé en arithmétique directe au seed** (le test grille par interpolation de |x₂₀| est invalide : x_N est un polynôme de degré F_N en t — pente locale jusqu'à 3e4 par cellule de grille à 2^18, démontré au run 1 sur 5 seeds). taux d'accord ≥ 99 % exigé.
- Le seuil de réussite global est **pré-enregistré ici** : la partie 1 est tenue si O1 tient sur ≥ 95 % des seeds **de bandes** (référence exacte O3), O2 conforme (fenêtre T24), O3 ≥ 99 %, et O6 fournit une réponse nette (robuste OU tué proprement — voir tueurs).

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

**Run 1 du 03/11/2026 (v1.0) — verdict : CALIBRATION, 0/3 critères, trois défauts de rédaction documentés, aucun physique :**
- O3 = 93,75 % : la référence grille (interpolation de |x₂₀|, 2^18) est sous-résolue — démontré en arithmétique exacte sur les 5 désaccords (tous gaps : |x_N| dépasse 1 à N = 20–23). La classification Fricke était juste sur 80/80 avec la référence exacte.
- O1 = 48,75 % : seuil appliqué sur l'ensemble des seeds, gaps inclus — physique mal posée (spectre de Cantor de mesure nulle dans [−2,5 ; 2,5]).
- O2 : fenêtre 7–14 non conforme au protocole T24 ; les ratios des niveaux 7–9 dévient de > 0,02 (convergence lente connue).
- O4 : non conclusif (relation rotation/IDOS non spécifiée) — reporté en note, hors critères.
- Mesures nouvelles conservées : Lyapunov en bande ≈ 0,38–0,44 ; ≈ 11 près d'arête.
Corrections en v1.1 (feu vert de l'auteur du 03/11/2026) : références exactes pour O1/O3, fenêtre O2 = protocole T24 verbatim, O4 reporté, contrôle 30 chiffres sur seeds de bandes.

Consignation : NOTE-PHI-DYN-2-P1.md dans docs/, données brutes (orbites, CSV O1–O6) dans data/, verdict daté, leviers réglés en annexe.

---

## 7. Calendrier et coût

Exécution numérique pure (Python/NumPy, pas de donnée externe, pas de simulation GP nouvelle) : **une session**. Aucun téléchargement, aucune dépendance au-delà de l'existant. La partie 1 est le chantier le moins cher de la feuille Φ-DYN — c'est pourquoi il est premier.

---

## 8. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **Graine phason 20261103 — VALIDÉE telle quelle.** Une graine n'a de valeur que dans sa déclaration préalable ; la remplacer après coup n'ajouterait que du churn. Toute graine arbitraire déclarée avant run est équivalente ; celle-ci est la gelée.
2. **Seuils §3.6 (95 % / 0,02 / 99 %) — VALIDÉS.** Justification : 95 % sur O1 est honnête car la grille S3 échantillonne l'intervalle spectral à l'aveugle, sans présélection bande/gap — les orbites de gap ont le droit de ne pas porter Fricke, et le rapport les comptera explicitement comme « non portées », pas comme échecs. 0,02 sur O2 avec 8 bandes seulement est la tolérance naturelle d'une suite convergente dont les premiers termes oscillent. 99 % sur O3 est tenable car T24 a déjà prouvé la conjugaison de la map — la classification est sa fonction élémentaire. Clause ajoutée : **aucune tolérance de cette fiche n'est modifiable après le premier run** (T-4 s'applique).
3. **Sous-test D (adiabatique) — MAINTENU dans la fiche**, en annexe de force réduite. Une note autonome pour un sous-test d'une heure serait de la bureaucratie ; la fiche le porte explicitement comme analyse a posteriori, jamais au titre d'un verdict de classe (iii). La frontière épistémique est inscrite au §3.5.
4. **Décade ρ = 0.3 — AJOUTÉE** (grille §3.3 = six valeurs). Motif : si la structure à ratio φ survit à ρ = 0.15 mais meurt à 0.3, la maison mesure une **frontière de phase** au lieu d'un oui/non ; si elle survit à 0.3, la claim est plus forte encore. Coût marginal négligeable, information maximale.
5. **Nom de scellement — HORS-SÉRIE Φ-DYN.** Le verdict sera publié comme **VERDICT-ΦDYN2-P1 (daté)**, non comme T70. Motif : la série T est le registre des campagnes de mesure du pont φ ; Φ-DYN est un namespacing dédié (NOTE v2, changelog 1) et mélanger les deux retirerait au scellement son rôle de garde-fou anti-collision. Rétro-référence T24 inscrite dans le registre canonique au moment de la publication du verdict.

## 8 bis. Changelog v1.1 (scellé le 2026-11-03 après run 1, feu vert auteur)

| Point | v1.0 | v1.1 | Motif |
|---|---|---|---|
| Référence O3 | test grille \|x₂₀\| ≤ 1 par interpolation | limsup exact N ≤ 120 au seed | sous-résolution démontrée (degré F_N du polynôme) |
| Périmètre O1 | taux de portées sur toutes les seeds | taux de portées **parmi seeds de bandes** (réf. O3) | échantillonnage aveugle majoritairement en gaps — physique mal posée |
| Fenêtre O2 | niveaux 7–14, 6 derniers ratios | niveaux 9–14, **3 derniers ratios ± 0,02 + récursion comptes ± 4 (protocole T24 verbatim)** | retour au précédent canonique gelé ; convergence lente des premiers niveaux |
| O4 | observable des critères annexes | **reporté en note** (spécification à rédiger), hors critères | relation rotation/IDOS non spécifiée ; deux implémentations divergent — pas de troisième tentative d'implémentation (pas de calibration à l'aveugle) |
| Contrôle 30 chiffres | 5 premières seeds S3 | 5 seeds S3 **de bandes** | les 5 premières seeds S3 étaient toutes dans le gap du bas (spectre ≥ −1,4916) — contrôle sans objet |

---

*Cette fiche ne modifie aucun verdict, aucune carte gelée, aucune dette. Elle est la première pierre de la classe (iii).*
