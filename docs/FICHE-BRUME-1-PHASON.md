# Fiche chantier BRUME-1 — La brume sous phason : premier test brume = f(perturbation)

**Date :** 2026-11-03 · **Version :** 1.0 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** **SCELLÉE le 2026-11-03 — v1.0.** Les cinq points de décision d'auteur (section 7) sont tranchés et inscrits ci-dessous. Toute exécution suit cette version à la lettre ; tout écart la tue (T-3⁗). Toute modification exige une version +0.1 et une note de changement datée.
**Références :** NOTE-CORRESPONDANCE-RÉSOLUE (fbabe54), NOTE O4 (dad3b46), VERDICT-ΦDYN2-P1 (grille phason gelée), NOTE-PHI-DYN-2-SYNTHESE (doctrine de la frontière), Brume_noetic.pdf.

---

## 1. Contexte et question

**Ce qui est établi.** La correspondance résolue (fbabe54) : le chaînon spectral de T24 est une chaîne de Fibonacci **non-Hermitienne** (Hatano-Nelson, c = e^{2iπ/3} sur les sites B). Son spectre d'anneau est complexe avec un profil imaginaire **universel et stable** : |Im| médian ≈ 0,626, maximum 0,880, ~97 % des modes au-dessus de 0,05 — identique aux niveaux 12/13/14. La partie imaginaire de l'énergie est la constante d'évanescence du formalisme de la brume : **la brume a une signature spectrale mesurable.**

**La question.** La brume est-elle un objet de régime ? Autrement dit : sous perturbation déclarée (phason), le profil imaginaire **s'épaissit-il, s'amincit-il, ou meurt-il** — et selon quelle frontière ? C'est le premier test « brume = f(perturbation) » de l'histoire de la maison, et il applique la doctrine de la frontière à l'objet brume : perturbation gelée, hiérarchie d'observables, mort nette ou molle.

**Hypothèse H-BRUME.** *Le profil imaginaire est un invariant grossier du modèle (comme la loi de Vinen dans P3) : il survit au phason faible et meurt nettement au-delà d'une frontière ρ\* — la brume a une épaisseur de régime, pas seulement une épaisseur spectrale.*

## 2. Sens charter

Classe (ii) — la machine simule le rôle d'une dynamique (réponse à une perturbation déclarée). Zéro paramètre ajusté, gel avant mesure, échec publié. Numérique pure : anneaux M-pair (eig exact), instrument validé hier soir (0,0000 % hors discriminant).

---

## 3. Objets déclarés (à sceller)

### 3.1 Instrument

Anneau M-pair (NOTE-CORRESPONDANCE-RÉSOLUE §1) aux niveaux 12/13/14 (W₁₂/W₁₃/W₁₄ = 144/233/377 sites). Spectre par `numpy.linalg.eig` (non-Hermitien ; vérification d'exactitude : résidu ‖Jψ − λψ‖ ≤ 1e−8 sur échantillon, et Tr(J) = n_B).

### 3.2 Perturbation déclarée

Flips phason Bernoulli par position (graine 20261103 instanciée une fois par ρ, reprise gelée P1/5b) : **un flip échange A ↔ B, donc onsite 0 ↔ 1 ET structure complexe 1 ↔ c simultanément** (le mot gouverne les deux — c'est le modèle). Grille ρ ∈ {0 (contrôle), 0.001, 0.01, 0.05, 0.15, 0.3} — six valeurs gelées (grille complète de la maison, atteint la mort, leçon P2/P3). 20 réalisations par ρ.

### 3.3 Observables (gelés — hiérarchie pré-enregistrée)

| # | Observable | Classe | Définition |
|---|---|---|---|
| B1 | médiane \|Im\| | **grossier** (le δ de la brume) | médiane des parties imaginaires en valeur absolue |
| B2 | max \|Im\| | fin | maximum |
| B3 | fraction Im > 0,05 | grossier | part des modes évanescents |
| B4 | fraction hors discriminant | **fin** (structure) | \|x_N(Re λ)\| > 1 — l'appartenance au chaînon |
| B5 | Re-étendue | grossier | [min Re, max Re] |

Hiérarchie doctrine attendue : B4 (structure fine) meure d'abord ; B1/B3 (la brume) survivent ou meurent à leur propre frontière ρ\*.

### 3.4 Critères pré-enregistrés

- **Frontière nette** : B1 ou B3 hors tolérance déclarée (±20 % de la valeur ρ = 0, gelée) à un ρ fini, monotone ;
- **Robuste** : B1 et B3 varient peu (≤ 20 %) jusqu'à ρ = 0,3 → la brume est un invariant de régime (H-BRUME tenue) ;
- **Mort nette** : B1 ou B3 → 0 au-delà d'un ρ\* → la brume meure (H-BRUME tenue dans sa forme frontière) ;
- **Molle** : dégradation sans seuil → H-BRUME réfutée dans cette forme.

## 4. Programme

**Palier A — instrument.** Contrôle exactitude (résidu, trace) au niveau 13 pur. Minutes.
**Palier B — mesure.** Grille ρ complète, 20 réalisations, B1–B5. Effort : < 30 min (eig 377×377 complexe ~ms).

## 5. Tueurs et leviers

| Tueur | Mécanisme | Verdict |
|---|---|---|
| T-1⁗ Instrument | résidu > 1e−8 ou trace fausse | retour rédaction |
| T-2⁗ Dépendance taille | B1 varie > 20 % entre niveaux 13 et 14 à ρ = 0 | la médiane n'est pas encore convergée en taille finie — rapporté, critères lus au niveau 14 |
| T-3⁗ | sélection a posteriori | B3-FAIL de fiche |

**Levier discriminant :** ρ (phason) — le quatrième visage de la frontière, cette fois sur le spectre imaginaire.

## 6. Annexe A — l'ancre contre δ = √(2η / ωµ_eff)

**Ce qui est testable ce soir.** L'ansatz du document a trois paramètres pour deux observables — il est sous-déterminé tel quel. Ce qui peut être mesuré proprement : **la co-évolution de l'ancre spectrale et du δ de brume sous la même perturbation**. Ancre déclarée sur le spectre complexe : Λ²_cplx = ρ²_λ + 3 − ⟨|λ|²⟩ (rayon spectral et moment sur |λ|). Mesure : trajectoire (Λ²_cplx, B1) par ρ — si δ ∝ (µ_eff)^{−1/2} avec µ_eff ∝ ancre, la trajectoire suit une loi de puissance d'exposant −1/2 dans le plan (ancre, δ). Rapportée comme test de cohérence, jamais comme validation de l'ansatz complet (η et ω non identifiables séparément ce soir — déclaré).

## 7. Décisions d'auteur tranchées au scellement (2026-11-03, v1.0)

1. **Grille ρ complète — VALIDÉE telle quelle** : {0, 0.001, 0.01, 0.05, 0.15, 0.3} — atteint la mort (leçon P2/P3 des grilles muettes), comparabilité directe avec P1.
2. **Tolérance ±20 % — VALIDÉE** : la nuit a démontré quatre fois que les critères trop stricts meurent au bruit ; 20 % est la bande de régime, pas de la rigueur.
3. **Flip double canal — VALIDÉ** : un flip échange A↔B, donc onsite 0↔1 ET structure complexe 1↔c simultanément — c'est le modèle. La variante à canal séparé (flips onsite seuls, structure fixe) est un chantier futur distinct, à ouvrir seulement si BRUME-1 révèle un comportement ambigu.
4. **Niveau 13 principal, 14 en contrôle, 12 en reproductibilité — VALIDÉ.**
5. **Nom — CONFIRMÉ :** verdict publié comme **VERDICT-BRUME-1 (daté)** — première campagne de la série BRUME, hors Φ-DYN.

---

*La brume a un spectre depuis hier soir ; ce soir, on apprend si elle a une épaisseur de régime.*
