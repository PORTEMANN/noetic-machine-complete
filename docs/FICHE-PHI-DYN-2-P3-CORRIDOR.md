# Fiche chantier Φ-DYN-2 partie 3 — Le corridor comme limite : convergence sur les invariants

**Date :** 2026-11-03 · **Version :** 1.0 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.0.** Les cinq points de décision d'auteur (section 7) sont tranchés et inscrits ci-dessous (grille w étendue à sept valeurs). Toute exécution doit suivre cette version à la lettre ; tout écart la tue (T-4). Toute modification exige une version +0.1 et une note de changement datée.
**Références :** VERDICT-ΦDYN2-P1 (d862875), VERDICT-ΦDYN2-P2 (62d3bcf), T41–T47 (données corridor archivées), T55, FICHES Φ-DYN-2 P1 v1.1 / P2 v1.1, NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (§ II.2 point 2 : « le continuum du corridor est-il la limite de ses orbites ? »).

---

## 1. Contexte et hypothèse

**Ce que P1 et P2 ont établi.** Le pont φ a deux dynamiques dérivées : la trace map de Kohmoto (générateur reconnu, Fricke conservée à 2,6·10⁻³⁰, structure φ fine — tuée par 1 flip phason) et la trace map du porteur (voie α confirmée : κ(y) → 1 quadratiquement, ±φ portés comme structures bornées résiduelles au collapse ; voie β réfutée : la récurrence de Lucas n'est pas une restriction de Fricke). Leçon transversale des deux verdicts : **la convergence s'entend sur les invariants, jamais point par point** (P5 de P2 : orbites décorrellées, invariants convergents).

**La question de la NOTE v2 restant ouverte.** Le continuum du corridor est-il la limite des orbites du porteur ?

**Reformulation opérationnelle (leçons P1–P2 appliquées).** La question « continuum = limite des orbites » est mal posée point par point (P5 l'a tuée pour les orbites elles-mêmes). Elle devient mesurable sous la forme symétrique suivante :

> **H-ΦDYN2c.** Le corridor et les orbites du porteur convergent *de la même manière* : par les invariants, avec une **frontière de perturbation déclarée** — le corridor aussi a son « flip phason » : une échelle de blocking au-delà de laquelle sa loi (Vinen) se brise, exactement comme φ se brise au premier flip.

P1 a mesuré la frontière discrète (1–4 flips tuent φ). P3 mesure la frontière continue (quel blocking tue la loi du corridor ?). Si les deux mondes ont une structure de frontière analogue — loi robuste en dessous, mort nette au-delà — alors le corridor et le porteur appartiennent à la même *classe de convergence*, et « la limite » a un sens commun : **l'invariant est la limite, et la frontière est sa mesure**.

---

## 2. Sens charter

Classe (iii) — dériver, pas emprunter. Zéro paramètre ajusté, gel avant mesure, échec publié. Analyse sur **données archivées uniquement** (T41–T47, T55) — aucune nouvelle simulation GP : le corridor de l'Acte IV est terminé et scellé ; la question porte sur sa *structure de limite*, pas sur de nouvelles données.

---

## 3. Objets déclarés (à sceller)

### 3.1 Voie γ — la frontière de blocking du corridor (mesure principale)

- **Données :** séries archivées Λ(t) du corridor (T47 `historiques`, runs 440201 n=2/4/8, 440203 n=4) — densités de lignes de vortex par pas de temps. Séries Lk/Q (T42–T44) en annexe.
- **Blocking déclaré :** moyenne glissante boxcar de largeur w (déclarée, non ajustée), w ∈ {1, 2, 4, 8, 16, 32, 64} — **sept valeurs gelées** (64 ajoutée au scellement, point 2 de la section 7 : forcer la mort propre si w\* = 32, leçon P2 de la grille qui n'atteint pas la mort), grille par facteur 2 (même esprit que la grille phason de P1).
- **Observables recomputés sur chaque série bloquée :**
  - G1 — loi de Vinen : R² du fit 1/Λ vs t à n = 8 (run 440201), seuil de survie **R² ≥ 0,90** (standard déclaré repris de T47, où le fit tient à 0,930 sur données brutes) ;
  - G2 — plateaux de paroi : valeurs aux plateaux (9,8 / 15,9 / 31,4 bruts) déviations relatives ≤ 5 % (tolérance gelée) ;
  - G3 — comptage d'événements : sauts unitaires détectés (détecteur gelé : |ΔΛ| > 0,5·échelle-type local, fenêtre 5 pas) — compte à ±1 de la série brute ;
  - G4 — échelle φ : ratios des plateaux 15,9/9,8 et 31,4/15,9, test |ratio − φ| ≤ 0,02 (standard maison O2 de P1, pré-enregistré — rapportés quoi qu'il arrive, sans refonte).
- **Critère de frontière :** w\* = plus grand w tel que G1 **et** G2 tiennent ; la frontière est rapportée avec le premier w mort (mort nette attendue, à la manière de P1).

### 3.2 Voie δ — la table des échelles comparée (annexe descriptive)

- Côté corridor (archive) : plateaux {9,8, 15,9, 31,4} à n = {2, 4, 8} ; sauts datés t = 3,50/3,55 (T44) ; drainage ÷43 (T46) ; durées de vie KM/Little ≈ 0,5 (T55).
- Côté porteur (P1/P2) : échelle de bande médiane ≈ 0,52/niveau (P1-C) ; κ − 1 ∝ (y−1)² (P2) ; frontière 1–4 flips (P1-B).
- Pas de critère de coïncidence gelé (les objets ne sont pas commensurables) : table descriptive, écarts explicites, aucune claim au-delà.

### 3.3 Graines et tolérances

Graine gelée **20261103**. Précision double 64 bits. Aucune tolérance modifiable après le premier run (clause T-4, troisième génération).

---

## 4. Programme

**Palier A'' — inventaire d'archives.** Vérifier la présence et l'intégrité des séries T47 (longueurs, pas, plateaux bruts reproduits à 1e−3) ; sans archive saine, le chantier s'arrête là (données, pas fiche). Effort : minutes.

**Palier B'' — voie γ.** Blocking + G1–G4 sur les six largeurs ; frontière w\* mesurée. Effort : < 1 h.

**Palier C'' — voie δ.** Table des échelles consolidée. Effort : minutes.

---

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict si déclenché |
|---|---|---|
| T-1'' Archives absentes | séries T47 indisponibles ou non reproductibles | chantier reporté (données) — pas un échec de H-ΦDYN2c |
| T-2'' Mort molle | la loi de Vinen se dégrade progressivement sans frontière nette (R² décroît sans saut) | H-ΦDYN2c **réfutée** : le corridor n'a pas de structure de frontière analogue au flip — la convergence n'est pas de la même classe — publié |
| T-3'' Mort immédiate | R² < 0,90 dès w = 2 | le corridor est fragile au blocking ; la frontière existe mais est étroite — mesure rapportée, H-ΦDYN2c tenue avec réserve |
| T-4'' | sélection a posteriori (changement de w grid, de kernel, de tolérance après observation) | B3-FAIL de fiche, mort datée |

**Levier discriminant :** w (largeur de blocking) — l'analogue exact du ρ phason de P1.

---

## 6. Verdicts possibles

1. **CONFIRMÉ :** frontière nette w\* mesurée (loi vivante à w\*, morte à 2w\*) → le corridor et le porteur ont la même classe de convergence (invariant-first, frontière nette) — « le continuum est la limite des orbites » acquiert un sens mesurable commun : **les deux mondes vivent sur leurs invariants et meurent sur leurs perturbations déclarées**. La partie 4 (synthèse Φ-DYN-2) est débloquée.
2. **RÉFUTÉ :** T-2'' → pas de structure de frontière ; le corridor se comporte comme un objet à convergence molle — classes distinctes — publié.
3. **CALIBRATION :** T-4'' → erratum +0.1.

---

## 7. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **Kernel — BOXCAR validé** : standard spectral, comparabilité avec les conventions du corridor ; la médiane glissante serait une variante de robustesse — à proposer en fiche distincte si la mort s'avère ambiguë, jamais en cours de run.
2. **Grille w — ÉTENDUE à sept valeurs :** {1, 2, 4, 8, 16, 32, 64}. Motif (leçon P2) : une grille qui n'atteint pas la mort rend la frontière muette ; 64 forces la mort propre.
3. **Seuil G1 — GELÉ à 0,90** : standard repris de T47, volontairement en dessous de la valeur brute archivée (0,930) pour laisser vivre le w = 1 et mesurer la dégradation ; resserrer à 0,92 tuerait la dynamique de mesure.
4. **Voie δ — MAINTENUE en annexe descriptive**, sans critère de coïncidence : les objets (échelles corridor, échelles porteur) ne sont pas commensurables ; doter la table d'un critère fabriquerait une comparabilité. Les écarts sont explicités, aucune claim au-delà.
5. **Nom — CONFIRMÉ :** verdict publié comme **VERDICT-ΦDYN2-P3 (daté)**, hors-série Φ-DYN, même précédent que P1/P2.

---

*Cette fiche ne modifie aucun verdict ni carte gelée. Elle est la troisième pierre de la classe (iii) — celle qui demande si les deux dynamiques dérivées parlent le même langage de limite.*
