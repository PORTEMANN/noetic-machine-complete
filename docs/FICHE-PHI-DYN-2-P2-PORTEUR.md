# Fiche chantier Φ-DYN-2 partie 2 — Le générateur du porteur (trace map du seesaw)

**Date :** 2026-11-03 · **Version :** 1.0 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.0.** Les cinq points de décision d'auteur (section 7) sont tranchés et inscrits ci-dessous (grille y étendue à six valeurs). Toute exécution doit suivre cette version à la lettre ; tout écart la tue (T-4). Toute modification exige une version +0.1 et une note de changement datée.
**Références :** VERDICT-ΦDYN2-P1 (d862875), NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (4d657fb), T14, T17–T18, T24, FICHE-PHI-DYN-2-P1 v1.1 (4ad4875).

---

## 1. Contexte et hypothèse

**Ce que la partie 1 a établi.** La trace map de Kohmoto est un générateur reconnu : Fricke est conservée à 2,6·10⁻³⁰, l'orbite seule classifie le spectre (80/80). Mais l'objet générateur de Φ-DYN-2 P1 est le *quasicristal Fibonacci* — pas le porteur du pont φ. L'orphelin de T15 reste en partie ouvert : **le flot emprunté par l'Acte IV peut-il être dérivé du substrat noétique du pont φ lui-même ?**

**La question exacte de la NOTE v2 (§ II.2, point 2).** La chaîne seesaw à M_R = 1 (T14) a son opérateur à deux sauts ; existe-t-il une trace map dont les orbites portent les ±φ, ±1/φ et les entiers topologiques de l'Acte IV ? Son invariant de Fricke existe-t-il ? Le continuum du corridor est-il la limite de ses orbites ?

**Hypothèse H-ΦDYN2b.** *La dynamique native du porteur (récurrence linéaire de Lucas, T17) est la dégénérescence d'une structure de Fricke à deux générateurs : quand le désordre/dimérisation y tend vers 1, la trace map dégénère en map de puissances, et les points ±φ, ±1/φ sont les structures bornées résiduelles de cette dégénérescence.*

### Faits déclarés (dérivés avant gel — à vérifier numériquement par la machine au palier A', aucun n'est utilisé avant vérification)

- **F1.** La chaîne fermée C(y) (4×4, sauts (1, y, 1)) a pour polynôme caractéristique λ⁴ − (2+y²)λ² + 1 ; à y = 1 : λ² = (3±√5)/2, valeurs propres **exactement ±φ et ±1/φ** (T14).
- **F2.** Tr C(1)ⁿ satisfait la récurrence **linéaire** u_{n+4} = 3u_{n+2} − u_n (du polynôme caractéristique) — classe Lucas (T17 : Tr C(1)^{2n} = 2·Lucas(2n)). La dynamique native du porteur est linéaire, intégrable, d'ordre 4 — *pas* une trace map non linéaire d'ordre 3.
- **F3.** Pour **toute** paire de matrices A, B ∈ SL(2,ℝ), les demi-traces x = Tr A/2, y = Tr B/2, z = Tr AB/2 vivent sur une surface de Fricke généralisée : l'invariant I = x² + y² + z² − 2xyz diffère d'une constante fixée par la demi-trace du commutateur κ = Tr[A,B]/2. **Forme exacte de la relation et conventions : à établir numériquement au palier A'** (identité vérifiée sur matrices aléatoires avant toute mesure — jamais assumée).
- **F4.** Le porteur à y = 1 est le point de dégénérescence : les deux maillons de dimère coïncident (A = B), le commutateur devient trivial (κ = 1), et la structure à deux générateurs s'effondre sur la dynamique de puissances (F2). **±φ vivent exactement à ce point de collapse.**

---

## 2. Question et sens charter

**Question :** le porteur seesaw possède-t-il une dynamique discrète de classe Fricke dont les orbites portent ±φ, ±1/φ — et cette dynamique dégénère-t-elle proprement en la récurrence de Lucas à y = 1 ?

**Sens charter :** classe (iii) — dériver, pas emprunter. Zéro paramètre ajusté, gel avant mesure, échec publié.

**Nature du chantier :** exploratoire-théorique. Contrairement à P1 (re-vérification d'un objet connu), P2 **construit** l'objet. Le protocole est donc en deux phases : A' (algèbre de vérification, sans physique nouvelle), puis B'/C' (mesure sur les constructions déclarées).

---

## 3. Objets déclarés (à sceller)

### 3.1 Construction α — le porteur par substitution (dimérisation déclarée)

- Maillons de dimère : chaîne de Jacobi infinie à deux sauts alternés : intracellule **1**, intercellule **y** ; matrices de transfert SL(2,ℝ) A(t ; 1) et B(t ; y) déclarées par le gabarit standard de T24 (même convention de transfert — A(t) = [[t,−1],[1,0]] généralisée au saut v : M_v(t) = [[t, −v],[1/v, 0]]... **forme exacte gelée au palier A' après vérification du déterminant 1**).
- Mot : substitution de Fibonacci sur l'alphabet {A, B} (précédent canonique P1).
- Grille y gelée : y ∈ {2, 1.1, 1.01, 1.001, 1.0001, 1} — **six valeurs** (1.0001 ajoutée au scellement, point 3 de la section 7 : forcer l'approche du collapse), dont le point de collapse y = 1 (les deux lettres coïncident : la valeur y = 1 est le contrôle de dégénérescence, pas une mesure Fricke).
- Énergies de mesure : grille déclarée t ∈ [−2,5 ; 2,5], 2¹⁴ points ; les points t = ±φ, ±1/φ sont inscrits comme seeds obligatoires (ils sont dans la bande [−2,2] du chaîne uniforme — leur statut d'orbite est précisément la question).

### 3.2 Construction β — le porteur natif (récurrence de Lucas)

- Matrice C(1) (T14, T17) : orbite u_n = Tr C(1)ⁿ par multiplication matricielle directe, n ≤ 10⁴.
- Test d'embaumement Fricke : existe-t-il une surface I = const et une carte non linéaire de R³ dont la restriction porte la suite de Lucas ? Formulation opérationnelle gelée : **la suite u_n est-elle la trace d'une orbite d'une récurrence non linéaire d'ordre 3 à coefficients constants ?** — testée par identification : chercher (a, b, c) constants tels que u_{n+3} = a·u_{n+2}·u_{n+1} + b·u_n + c tienne sur la grille n (moindres carrés exacts + résidu max) ; puis la même question pour la sous-suite impaire/paire. Critère pré-enregistré : résidu max ≤ 1e−12 → structure Fricke trouvée ; > 1e−6 → la dynamique native n'est pas une restriction de Fricke.

### 3.3 Observables (gelées)

| # | Observable | Définition | Cible |
|---|---|---|---|
| P1 | Identité F3 | relation I–κ vérifiée sur 10⁴ paires aléatoires SL(2,ℝ) | résidu ≤ 1e−12 (condition sine qua non) |
| P2 | κ(y) | demi-trace du commutateur sur la grille y | limite y→1 : κ → 1 (dégénérescence propre) |
| P3 | Statut d'orbite à ±φ, ±1/φ | bornée / divergente, y = 1 + ε | réponse nette requise |
| P4 | Identification Fricke-Lucas (β) | résidu de la récurrence non linéaire | ≤ 1e−12 ou > 1e−6 |
| P5 | Dégénérescence | distance orbite(α, y) → orbite(β) en norme de traces, y → 1 | mesure nouvelle, sans cible gelée |

### 3.4 Graines et tolérances

Graine aléatoire gelée **20261103** (même précédent que P1). Précision : double 64 bits ; contrôle 30 chiffres (mpmath) sur 5 orbites. Aucune tolérance n'est modifiable après le premier run (clause T-4 reprise de P1).

---

## 4. Programme

**Palier A' — vérification d'algèbre (sans physique nouvelle).** F3 sur matrices aléatoires ; déterminant des matrices de transfert du dimère = 1 ; formes exactes gelées. Effort : minutes. Si A' échoue → la fiche retourne en rédaction (T-4), rien d'autre ne tourne.

**Palier B' — construction α.** Orbites de la trace map de Fibonacci sur les paires (A, B)(t ; y), grille y, seeds ±φ/±1/φ. Mesures P2, P3, P5. Effort : < 1 h.

**Palier C' — construction β.** Suite de Lucas, identification non linéaire, mesure P4. Effort : minutes.

---

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict si déclenché |
|---|---|---|
| T-1' Collapse trivial | à y = 1 + ε, κ ≈ 1 et les orbites ne distinguent pas la structure à deux générateurs : ±φ ne sont portés par aucune structure bornée spécifique | H-ΦDYN2b **réfutée** : les ±φ sont des quantification finie, pas un attracteur dynamique — publié (c'est la réponse honnête attendue par la moitié de la doctrine) |
| T-2' Non-existence Fricke-Lucas | P4 > 1e−6 : la récurrence native n'est pas une restriction de Fricke | H-ΦDYN2b réfutée sur la voie β ; seule la voie α reste — publié |
| T-3' κ non convergent | κ(y) n'a pas de limite propre en y → 1 | construction α mal posée → calibration documentée |
| T-4' | sélection a posteriori | B3-FAIL de fiche, mort datée |

**Levier discriminant :** y (dimérisation) — c'est lui qui décide si la structure Fricke existe en dehors du point de collapse.

---

## 6. Verdicts possibles

1. **CONFIRMÉ :** P2 montre κ → 1 proprement, P3 montre ±φ portés comme structures bornées résiduelles à la dégénérescence, P4 ≤ 1e−12 → le porteur a un générateur Fricke, la récurrence de Lucas en est la face linéaire au point de collapse — première **dynamique dérivée du substrat noétique**, et la partie 3 (limite corridor) est débloquée.
2. **RÉFUTÉ :** T-1' ou T-2' → les ±φ sont une quantification de chaîne fermée finie sans dynamique sous-jacente de classe Fricke — le pont φ garde sa dynamique empruntée, publié honnêtement : *la signature n'est pas un mécanisme*.
3. **CALIBRATION :** T-3' ou T-4' → erratum +0.1.

---

## 7. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **Matrices de transfert du dimère — VALIDÉES :** M_v(t) = [[t, −v],[1/v, 0]] (déterminant 1 identiquement, jauge standard du saut v ; la vérification déterminantique est quand même exigée au palier A', sine qua non).
2. **Test P4 — VALIDÉ tel quel :** u_{n+3} = a·u_{n+2}·u_{n+1} + b·u_n + c sur les sous-suites paire et impaire séparément ; la forme épouse la structure de Fricke (produit des deux traces les plus récentes + terme linéaire + constante), avec moindres carrés exacts et résidu max ; critère binaire gelé ≤ 1e−12 / > 1e−6.
3. **Grille y — ÉTENDUE à six valeurs :** {2, 1.1, 1.01, 1.001, 1.0001, 1}. Motif : 1.0001 force l'approche du collapse ; si κ(y) n'a pas de comportement lisible à 1.0001, la limite est une extrapolation, pas une mesure.
4. **Seuil P3 — GELÉ à 1e−12** (identique au standard P1). Toute relaxation serait modifiable après observation ; le seuil dur est le prix de la réponse nette. Les orbites à y éloigné du collapse sont exploratoires et rapportées sans critère.
5. **Nom — CONFIRMÉ :** verdict publié comme **VERDICT-ΦDYN2-P2 (daté)**, hors-série Φ-DYN, même précédent que P1 (fiche P1 §8 point 5).

---

*Cette fiche ne modifie aucun verdict ni carte gelée. Elle est la seconde pierre de la classe (iii) — celle qui construit au lieu de re-vérifier.*
