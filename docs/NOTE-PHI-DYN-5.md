# VERDICT-ΦDYN5 — φ sous la RG spectrale déclarée : direction qui s'écoule

**Date :** 2026-11-03 · **Chantier :** Φ-DYN-5 · **Fiche :** FICHE-PHI-DYN-5-RG-SPECTRALE **v1.1 SCELLÉE** (0ef9289 ; v1.0 → CALIBRATION au palier A : contrôle bipartite invalide pour L impair, indexation W₁₃, arithmétique du contrôle ancre — documentées §6 de la fiche)
**Références :** NOTE-PONT-PHI-CHANTIERS-DYNAMIQUE v2 (§ II.5), NOTE-PHI-DYN-2-SYNTHESE (18a7ab1), T24, VERDICT-ΦDYN2-P1/P2/P3.
**Statut du mot :** hors-série Φ-DYN (précédent P1–P3).

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| 0 ratio φ dans la fenêtre à tous les δ de la grille gelée · ancre +8→+29 % avec saturation · trajectoires par itération (montée + chute terminale documentée) · robustesse : verdict unique sur {1/φ, 1/φ², 1/φ³, 1/φ⁴} · palier A 4/4 | « φ = direction qui s'écoule sous blocking de valeurs » · « l'ancre est un couplage qui tourne » (le vocabulaire « running coupling » est une identification) | « Accident UV, pas universalité infrarouge » comme statement sur la nature · « la générité n'est pas φ — c'est l'ancre » · le programme « une RG où φ est fixe » |

## Synthèse en une phrase

**φ n'est pas un point fixe de la renormalisation spectrale déclarée : sous le blocking δ = 1/φ², la signature dorée des gaps s'écoule immédiatement (0 ratio dans la fenêtre à tous les δ testés), tandis que la relation d'ancre — se comportant exactement comme un couplage qui tourne — dérive de +8 % à +29 % selon l'échelle de blocking : pour cette RG, le pont φ est une structure UV qui s'intègre au cours du flot, pas une universalité infrarouge — B3-FAIL publié, avancée de la même taille qu'un succès.**

---

## 1. Palier A — instrument et algèbre : **PASS 4/4**

| Contrôle | Résultat | Verdict |
|---|---|---|
| A1 y = 1 = chaîne uniforme 2cos(k), 233 sites | écart max 3,4·10⁻¹⁵ | PASS |
| A2 spectre réel, N = 233, trace nulle | exact | PASS (v1.1) |
| A3 idempotence du blocking | fixpoint stable | PASS |
| A4 ancre sur spectre uniforme | Λ²_sel = 5,000000 (valeur de main) | PASS |

## 2. Palier B — mesure (banc Kohmoto W₁₃, y = 1,5, 233 eigenvalues)

**R1 — clusters :** 233 → fixpoint en 5–7 itérations selon δ (8 clusters à δ = 1/φ, 15 à 1/φ², 19 à 1/φ³, 25 à 1/φ⁴). Le blocking a une dynamique propre, pas une effondrement instantané.

**R2 — signature φ des gaps (la question du point fixe) :** après blocking à fixpoint, **0 ratio dans la fenêtre ±0,02 à tous les δ** — 0/6 (1/φ), 0/6 (1/φ²), 0/5 (1/φ³), 0/6 (1/φ⁴). La structure dorée des gaps ne survit à aucune échelle de la RG déclarée. **φ n'est pas un point fixe.**

**R3 — relation d'ancre Λ²_sel (le couplage) :**

| δ | Λ²_sel au fixpoint | dérive relative |
|---|---|---|
| brut | 5,816 | — |
| 1/φ | 6,295 | +8,2 % |
| **1/φ² (principal)** | **6,968** | **+19,8 %** |
| 1/φ³ | 7,511 | +29,1 % |
| 1/φ⁴ | 7,498 | +28,9 % (saturation) |

L'ancre varie **lisse et monotone en l'échelle de blocking**, avec saturation au-delà de 1/φ³ — le comportement exact d'un **couplage qui tourne** au sens de la RG : bien défini à chaque échelle, jamais invariant. La hiérarchie doctrine se vérifie à l'envers du cas P1/P3 : ici c'est l'observable *grossier* (l'ancre) qui coule, parce que le blocking déclaré est une vraie RG et non une simple perturbation.

**R4 — trajectoires par itération :** montée continue 5,82 → 7,2–7,5 ; monotone stricte à δ = 1/φ³ ; à δ = 1/φ et 1/φ², une **chute en toute dernière itération** (7,24 → 6,97 et 7,13 → 6,30) brise la monotone. Diagnostic : la dernière grande fusion discrète rogne le bord spectral et fait chuter ρ² — artefact de finite size de la map de blocking, pas une structure sans loi (le flux est monotone sur toute la partie non terminale). Rapporté comme annexe, non reclassé.

**Robustesse (tueur T-1''′) :** verdict qualitatif unique — « φ écoulé » — sur les quatre valeurs de δ. La conclusion ne dépend pas du blocking choisi. **Robuste.**

**Contrôle niveau 14 (377 sites) :** N fixpoint = 15, identique au niveau 13 → reproductible.

## 3. Verdict global (fiche §6, option 2)

**φ = DIRECTION QUI S'ÉCOULE — B3-FAIL PUBLIÉ** (au sens de la fiche : « le pont φ est, pour cette RG déclarée, un accident UV, pas une universalité infrarouge — avancée de la même taille qu'un succès »).

Les trois énoncés exacts :
1. La signature φ des gaps n'est un point fixe d'aucun blocking de la grille gelée (R2 nul partout, robuste).
2. La relation d'ancre est un couplage qui tourne (+8 → +29 %, saturation), bien défini à chaque échelle — l'objet naturel de la description RG n'est pas φ mais l'ancre.
3. La hiérarchie fine/grossier doctrine se lit ici comme : **structures UV (φ) = décor qui s'intègre au flot ; couplage (ancre) = ce qui porte la physique à toutes les échelles.**

**Conséquence pour la maison :** « le monde discret signe φ » reste vrai spectralement (P1, T24), mais **la générité n'est pas φ** — c'est l'ancre qui tourne. La question d'universalité se reformule : existe-t-il une RG déclarée pour laquelle φ EST fixe ? (une blocking rule sur les *gaps* plutôt que sur les valeurs, par exemple — chantier distinct, non ouvert ce soir). Φ-DYN-4 (Vinen externe) n'est pas affecté : sa cible est une loi phénoménologique, pas une universalité.

## 4. Leçons gravées au dossier

1. **Troisième visage de la frontière :** flip phason (discret, P1) · boxcar temporel (série, P3) · blocking spectral (RG, ce soir) — trois perturbations, trois frontières nettes, une doctrine.
2. **Un couplage qui tourne est la bonne réponse à une mauvaise question** : demander si φ est fixe, c'était demander si un objet UV est IR ; la RG déclarée répond en exhibant ce qui, elle, coule proprement (l'ancre).
3. **La dernière itération d'une map discrète est un événement, pas une asymptote** — la monotone doit être lue hors fusion terminale, et cette règle doit être déclarée dans les fiches futures qui itèrent des maps de fusion.
4. **Un B3-FAIL mesuré proprement vaut une confirmation** (4ᵉ génération de la leçon).

---

## 5. Artéfacts

Script : `src/phidyn5_paliersAB.py`. Données : `data/phidyn5_paliersAB.json`.

*Verdict hors-série Φ-DYN, nommé VERDICT-ΦDYN5 (2026-11-03).*
