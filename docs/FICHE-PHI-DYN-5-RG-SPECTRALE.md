# Fiche chantier Φ-DYN-5 — La RG spectrale (φ comme point fixe de la renormalisation déclarée)

**Date :** 2026-11-03 · **Version :** 1.1 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.1** (erratum de la v1.0 après le run du palier A : un contrôle physiquement invalide et une clarification d'indexation — voir §6). Toute exécution doit suivre cette version à la lettre ; tout écart la tue (T-4). Toute modification ultérieure exige une version +0.1 et une note de changement datée.
**Références :** NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (4d657fb, § II.5 — protocole de blocking déclaré), NOTE-PHI-DYN-2-SYNTHESE (18a7ab1 — doctrine de la frontière : la RG spectrale est une machine à frontière), VERDICT-ΦDYN2-P1/P2/P3, T24 (chaînon SL(2,ℝ)), T30 (rapport y₁/y₂ et plancher 59 meV — texture, non re-mesurée ici).

---

## 1. Contexte et question

**La question de la NOTE v2 (§ II.5).** Les structures φ sont-elles un **point fixe**, un **attracteur**, ou une **direction irrélevante** d'une renormalisation déclarée ? « Le monde discret signe φ » deviendrait précis : φ = point fixe du flot déclaré — la traduction exacte du concept académique d'*universalité*. Si φ s'écoule (direction irrélevante) : le pont est un accident infrarouge — B3-FAIL publié, avancée de la même taille qu'un succès.

**La lecture doctrine (SYNTHESE §4).** Le blocking δ = 1/φ² est une machine à frontière au sens de P3 : perturbation déclarée, hiérarchie d'observables (fins/grossiers), mort attendue fine-d'abord. La question relevance/irrelevance de la RG n'est donc pas une métaphore : c'est la question « quelles structures meurent sous le blocking, et dans quel ordre ? » — et la réponse est une frontière mesurable.

**Hypothèse H-ΦDYN5.** *Les moments spectraux (grossiers) sont des invariants du blocking déclaré ; la structure fine des gaps φ est une direction du flot dont le caractère (fixe ou irrélevant) est mesurable par la trajectoire de la relation d'ancre sous itérations.*

---

## 2. Sens charter

Classe (ii) — la machine simule la *générité* d'une dynamique sans en connaître les équations. Zéro paramètre ajusté, gel avant mesure, échec publié. Numérique pure : spectre d'approximants périodiques du quasicristal de Kohmoto (le banc spectral le plus riche dont la maison dispose — filiation directe T24/P1).

---

## 3. Objets déclarés (à sceller)

### 3.1 Banc spectral

- **Banc principal :** approximant périodique du quasicristal de Kohmoto au **niveau 13** : matrice de Jacobi 233×233, sauts suivant le mot W₁₃ (A → 1, B → y), diagonale nulle. Spectre par `eigvalsh` (233 valeurs propres réelles).
- **Paramètre y déclaré : 1,5** (hors collapse y = 1 — leçon P2 : le collapse est une autre frontière, pas le sujet ici).
- **Contrôles :** (a) à y = 1, le spectre coïncide avec la chaîne uniforme 2·cos(k) à 1e−12 ; (b) le spectre est symétrique (chapiteau bipartite) à 1e−12 ; (c) niveau 14 (377) en re-run de contrôle uniquement.

### 3.2 Règle de blocking gelée (reprise verbatim de la NOTE v2 § II.5)

Fusionner toute paire d'eigenvalues adjacentes dont l'écart relatif |λ_{i+1} − λ_i| / max(|λ_i|, ε) est inférieur au seuil déclaré **δ = 1/φ²** (≈ 0,382) ; valeurs fusionnées par leur moyenne ; **itérer jusqu'à stabilité** (plus aucune fusion). Le seuil est déclaré d'avance, motivé par le module d'or — aucun ajustement post-run.

**Grille de robustesse gelée (tueur de la NOTE v2) :** δ′ ∈ {1/φ, 1/φ³, 1/φ⁴} — **trois valeurs pré-enregistrées** (1/φ⁴ ajouté au scellement, point 4 de la section 7 : leçon P2/P3 — une grille qui n'atteint pas la mort rend la frontière muette) ; si le verdict qualitatif diffère entre δ, δ′, la RG dépend du choix de blocking → B3-FAIL publié.

### 3.3 Transport (relation d'ancre — lecture opérationnelle gelée)

La relation d'ancre de la NOTE v2, **Λ²_sel = ρ² + 3 − a₂/a₀**, n'a pas de définition plus ancienne dans le corpus : elle est déclarée ici opérationnellement pour la première fois, et ce choix fait partie du gel :

- ρ = rayon spectral = max|λ_i| ;
- a₀ = Σλ_i⁰ = N (nombre de valeurs) ; a₂ = Σλ_i² (moment spectral) ;
- la combinaison a₂/a₀ = moyenne des carrés.

Cette lecture est **validée au palier A** (dimensions, comportement aux contrôles) ; elle n'est jamais modifiée après.

### 3.4 Observables (gelés — hiérarchie pré-enregistrée, doctrine §2 condition 2)

| # | Observable | Classe | Définition | Attendu doctrine |
|---|---|---|---|---|
| R1 | nombre de clusters | fin | N après blocking à fixpoint, par itération | meurt (fusion) |
| R2 | signature φ des gaps | fin | ratios des 8 plus grands gaps consécutifs vs φ (fenêtre ±0,02, standard maison) | **la question du point fixe** |
| R3 | relation d'ancre Λ²_sel | grossier | transportée par 3.3 à chaque itération | survit (invariant de flot ?) |
| R4 | trajectoire et exposant | mixte | dérive de R3 sous itérations ; exposant apparent (pente log-log sur les itérations 1..n*) | fixe / irrélevant / non monotone |

Critère de stabilité de fixpoint : itération jusqu'à N stable (ΔN = 0) ou 50 itérations maximum (plafond gelé).

### 3.5 Graines et tolérances

Graine gelée **20261103**. Double 64 bits. Critères relatifs partout où les objets ne sont pas bornés (leçon P1/P2, troisième génération). Aucune tolérance modifiable après le premier run (T-4).

---

## 4. Programme

**Palier A — instrument et algèbre.** Construction W₁₃/Jacobi — **clarification gelée v1.1 : W₁₃ = mot de Fibonacci de longueur F₁₃ = 233, c'est-à-dire `mot_fibonacci(11)` dans la convention T24 (mot_fibonacci(n) a longueur F_{n+2})** — piège d'indexation identique à P1-B, mort une fois, pas deux. Contrôles : (a) à y = 1, le spectre coïncide avec la chaîne uniforme 2cos(k) à 1e−12 ; (b) **v1.1 : spectre réel, N = L = 233, trace nulle à 1e−12** — le contrôle v1.0 « symétrie spectrale » était physiquement invalide : une chaîne annulaire de longueur impaire (233 est impair) contient un cycle impair et n'est pas bipartite, son spectre n'est pas symétrique (mesuré 1,0·10⁻², conforme à la théorie des graphes) ; (c) blocking idempotent ; (d) validation de la lecture 3.3 : valeur de contrôle **v1.1 : Λ²_sel calculée sur le vrai spectre uniforme à y = 1** (ρ = 2, a₂/a₀ = moyenne des λ² = 2, donc Λ²_sel = 4 + 3 − 2 = 5 — la v1.0 testait un spectre jouet de 2 points où a₂/a₀ = 4, arithmétique de contrôle fautive). Effort : minutes. Échec → la fiche retourne en rédaction, rien d'autre ne tourne.

**Run du 03/11/2026 (v1.0 → v1.1) — verdict : CALIBRATION au palier A (contrôle bipartite invalide pour L impair + indexation du mot + arithmétique du contrôle ancre), puis exécution v1.1.**

**Palier B — mesure.** Blocking δ = 1/φ², trajectoires R1–R4 ; re-run δ′ ∈ {1/φ, 1/φ³} ; contrôle niveau 14. Effort : < 1 h.

---

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict si déclenché |
|---|---|---|
| T-1''′ Robustesse | verdict qualitatif (fixe/irrélevant) différent entre δ, δ′ = 1/φ, δ′ = 1/φ³ | **B3-FAIL publié** : la RG spectrale dépend du blocking choisi — « φ point fixe » n'est pas robuste |
| T-2''′ Mort molle | ni fixe ni irrélevant : trajectoire non monotone de R3 sans structure | map mal déclarée → calibration documentée |
| T-3''′ Palier A en échec | contrôles 3.1 ou idempotence ou valeur de contrôle manuelle non reproduite | la fiche retourne en rédaction (T-4) |
| T-4''′ | sélection a posteriori | B3-FAIL de fiche, mort datée |

**Levier discriminant :** δ (seuil de blocking) — l'analogue du ρ phason (P1) et du w boxcar (P3) : le troisième visage de la frontière.

---

## 6. Verdicts possibles

1. **φ = POINT FIXE :** R2 tient à la fenêtre ±0,02 après blocking à fixpoint, R3 invariant (variation relative ≤ 1e−3), robuste aux δ′ → « le monde discret signe φ » devient une statement de universalité mesurée. Bloque la porte de Φ-DYN-4 (Vinen externe) avec un concept exportable.
2. **φ = DIRECTION IRRÉLÉVANTE :** R2 s'écoule monotone, exposant mesuré (R4) → B3-FAIL publié : le pont φ est un accident infrarouge — avancée de la même taille qu'un succès (NOTE v2, verbatim).
3. **CALIBRATION :** T-2''′/T-3''′/T-4''′ → erratum +0.1.

---

## 7. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **y = 1,5 — VALIDÉ** : point de travail déclaré, hors collapse (leçon P2 : y = 1 est une autre frontière) et hors régime divergent (P2 : à y = 2 les orbites divergent partout) ; structure spectrale présente à 1,5.
2. **Niveau 13 principal — VALIDÉ** : 233 eigenvalues suffisent pour la hiérarchie de gaps ; niveau 14 (377) en contrôle de reproductibilité, pas en run principal (économie de protocole, pas de données).
3. **Lecture opérationnelle de l'ancre — VALIDÉE** : ρ = rayon spectral, a₀ = N, a₂ = moment spectral ; valeur de contrôle manuelle au palier A (y = 1 → Λ²_sel = 5) — jamais modifiée après.
4. **Grille δ′ — ÉTENDUE à trois valeurs :** {1/φ, 1/φ³, 1/φ⁴}. Motif (leçon P2/P3) : si le verdict ne change qu'au-delà de la grille, la grille était muette ; 1/φ⁴ ≈ 0,146 force le régime de fusion large.
5. **Nom — CONFIRMÉ :** verdict publié comme **VERDICT-ΦDYN5 (daté)**, hors-série Φ-DYN, même précédent que P1–P3.

---

*Cette fiche ne modifie aucun verdict ni carte gelée. Elle est la machine à frontière tournée vers la question d'universalité — le quatrième visage de la même doctrine.*
