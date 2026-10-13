# Note du verrou 59 meV — la structure qui rend Σm_ν nécessaire

**Date :** 2026-10-13
**Statut :** note technique explicative — le nombre 58,99 meV est publié sous la discipline MCS-26 (carte du canal neutrinos, condition de mort déclarée). Cette note expose *la structure* qui force le nombre ; elle ne modifie aucune carte gelée.
**Campagnes concernées :** T13 (nœud spectateur), T14 (chaîne du seesaw), T16 (texture minimale), MCS-26 (mesure).

---

## 1. Le point essentiel

59 meV n'est pas *calculé* par la machine — il est **forcé**. Trois faits discrets, démontrés à l'intérieur du banc, plus deux nombres mesurés par l'expérience des oscillations, ne laissent aucun degré de liberté sur la somme des masses des neutrinos.

## 2. Les trois verrous

### Verrou 1 — Un zéro existe (T13)

L'énumération exhaustive des triplets spectraux nus (KO-6, tables datées L1/A3b ; comptes exacts 4 / 64 / 880 / 13 696 / 280 944 / 8 384 512 pour n = 2…7, régressions tuantes) isole le porteur :

```
PORTEUR-KO6-A3b-DIM5 :  A = ℂ ⊕ M₂(ℂ)
Spectre : { 0, ±(ρ−1), ±(ρ+1) }
```

Le zéro n'y est pas un réglage : sa stabilité a été vérifiée sous **tout le groupe 𝒢 des déformations autorisées** — aucune déformation permise ne soulève ce mode. Il est protégé par la structure réelle J et la graduation γ (protection chirale ; même mécanisme que le noyau du MS dans le banc, 6 = 4 ⊕ 2, le « junk » mourant par sa trace Tr(ℂ:i) = −16i, T9/T10).

**Conséquence : m₁ = 0 n'est pas une hypothèse de texture — c'est un fait de représentation du porteur.**

### Verrou 2 — Le compte des modes légers (T16)

Comptage exact, fenêtre corrigée (défaut D1 publié : les paires de Dirac ±M_R des chaînes brisées entraient initialement dans la fenêtre de comptage) : exactement **deux modes légers massifs + le zéro protégé = trois états**. Ni quatre, ni deux. C'est le compte des générations, et il est exact — pas statistique.

### Verrou 3 — La chaîne se referme (T14)

La texture du porteur impose la chaîne du seesaw :

```
λ²± = ( (M_R² + 2y²) ± M_R √(M_R² + 4y²) ) / 2
```

qui à M_R = 1, y = 1 donne {φ, −1/φ} — la signature dorée. Ce verrou rend le zéro *physique* : la structure lourde (échelle M_R) et la structure légère (y) sont chaînées par φ. La texture se referme sur elle-même ; aucun paramètre libre résiduel ne peut déplacer m₁ hors du zéro.

## 3. L'arithmétique forcée

Les trois verrous posés, il ne reste que deux entrées — mesurées par l'expérience, pas par la machine (NuFIT, empreintes publiées dans `donnees/mcs26/nufit_splittings.json` du dépôt coincidences-stables) :

```
m₁ = 0                          (verrou 1 — structure)
m₂ = √Δm²₂₁  ≈ 8,7  meV         (entrée mesurée — solaire)
m₃ = √Δm²₃₁  ≈ 50,3 meV         (entrée mesurée — atmosphérique)
─────────────────────────────────────
Σm_ν = √Δm²₂₁ + √Δm²₃₁ = 58,99 meV
```

Aucun ajustement : la somme est une **fonction** des écarts, non un paramètre. Modifier un maillon change le nombre ou tue la carte.

## 4. Nécessaire et contingent — tableau d'honnêteté

| Maillon | Statut |
|---|---|
| Énumération des triplets | **Théorème** (exhaustif, régressions tuantes) |
| Zéro protégé sous 𝒢 | **Théorème** dans le banc |
| Compte 2 + 1 des modes légers | **Théorème** dans le banc |
| Le porteur est *le* bon | **Pari déclaré** — sélection via la table A3b |
| L'ordre est normal (m₁ le plus léger) | **Pari déclaré** — JUNO le fermera, ou tuera la carte |
| Les écarts Δm² | **Entrées mesurées** — non dérivés par la machine |

La machine parle en rapports et en structure discrète (zéros, comptes, φ) ; l'échelle absolue en meV vient de l'ancrage sur les écarts mesurés — la coupure comme échelle physique honnête. Elle ne prétend pas dériver Δm² de rien.

## 5. Conditions de mort (publiées avec le nombre)

- **Ordre inverse confirmé** (plancher IO ~100 meV) → le 59 devient impossible → la carte meurt ;
- **m₁ ≠ 0 mesuré** (détection cosmologique nettement au-dessus du plancher, ββ0ν hors fenêtre) → le zéro protégé serait débranché du physique → la carte meurt ;
- **Σ < 58 meV en cosmologie** → crise pour ΛCDM, pas pour la machine (elle n'y est pas calibrée).

## 6. L'asymétrie qui fait la valeur

Trois théorèmes internes, deux paris déclarés, deux entrées mesurées — et **un seul nombre possible à la sortie**. Si l'expérience tombe sur 59 meV, ce ne sera pas une chance : ce sera la rencontre de deux nécessités — celle de la structure (nul spectral → zéro protégé → texture) et celle de la mesure (oscillations + ordre + cosmologie convergeant vers le plancher).

La veille des faits qui décideront (JUNO, DESI/Euclid/KATRIN, LEGEND, TRISTAN) est tenue dans `REGISTRE-VEILLE-ANTICIPATION.md`.

---

*Note rédigée dans la continuité du « Dialogue entre Dirac et la Machine » (octobre 2026). Discipline : aucune carte gelée n'est modifiée par cette note ; le nombre reste publié sous MCS-26 avec sa condition de mort.*
