# P39 — Fermeture de la frontière r₁₂ : la portée se dérive

**Patrice Portemann — corpus Machine Noétique, chantier P39**
Protocole gelé R12-FERM-1.0 · zéro paramètre ajusté · artefacts SHA-256
30 août 2026

## Verdict

**FRONTIÈRE FERMÉE** — par son propre falsifieur, pré-enregistré dans le
registre A4 : « tout couple (famille, règle) à zéro paramètre passant le
tamis en tout Z dans le domaine variationnel ferme la frontière ». À
l'intégrateur d'espérance complet reconstruit, **quatre couples passent en
tout Z = 2..6** : F1×R3 (la règle de densité historique du corpus,
β = 0.42ζ₀), F2×R1, F2×R2, F2×R3. F1×R3 passe aussi en Z = 7..10, dans
H⁻ et dans Ps⁻. La portée du facteur à deux corps **se dérive sans
paramètre**.

## La découverte en cours de route (B3-FAIL corpus, publié)

Le chantier devait commencer par porter l'intégrateur complet de P31. Le
contrôle préalable a réfuté l'outil lui-même : l'intégrande cinétique de
P31 **mélange deux formes d'intégration par parties** — le terme u′² (forme
|∇Ψ|²) y coexiste avec −(u″+2u′/U) (forme laplacienne) et un terme croisé
u′cosθ₁₂(a+b) sans facteur géométrique. Mesures à Z = 2 (même grille) :

- distorsion jusqu'à **+0.13 Ha** à β = 0.5 (portée physique) ;
- optimum apparent déplacé vers les courtes portées (β ≥ 3) ;
- gain maximal écrasé : **4.9 mHa (P31) contre 26.4 mHa (forme correcte)**.

Conséquence publiée : le verdict P31 « la portée n'est pas dérivable à
Z = 2 à l'intégrateur complet » était un **artefact d'intégrande**. Et la
« loi P32 » (R3 ne gagne qu'en Z = 2), confirmée par le tamis A3 à
l'intégrateur delta, était la **signature du domaine de validité de
l'intégrateur delta** — pas de la physique. L'intégrateur delta de C12.1
n'est pas en faute : il est construit différemment (1-corps analytique) ;
mais ses verdicts de perte en corrélation forte ne disaient rien de la
physique — ils mesuraient sa propre frontière.

## Résultats mesurés

**Volet A — les 50 cellules du tamis rejugées à l'intégrateur complet**
(forme |∇Ψ|², grille corpus 300×192, règles figées en ζ₀ résolues dans le
même intégrateur, porte variationnelle 5e-3) :

| couple | Z=2..6 | gains (mHa) |
|---|---|---|
| **F1×R3** (densité) | **+ + + + +** | 18.5 → 19.4 (constant) |
| **F2×R1** (échelle) | **+ + + + +** | 23.0 → … |
| **F2×R2** (orthogonalité) | **+ + + + +** | 43.2 → 40.5 |
| **F2×R3** (densité) | **+ + + + +** | 38.1 → … |
| F1×R2 | − + + + + | perd à Z=2 |
| F4×R2 | − + + + + | perd à Z=2 |
| F1×R1, F3×R3, F4×R1, F4×R3 | − − − − − | — |

**Volet B — extension de la loi** : H⁻ (Z=1) : F1×R3 +17.2 mHa, F2×R3
+33.7 mHa ; Ps⁻ (levier masse M=1, polarisation de masse IBP, contrôle
MP(c=0) = 0 exact) : F1×R3 +3.7 mHa. F2×R3 sur Ps⁻ : HORS DOMAINE — la
boîte de 12 a₀ tronque la densité diffuse de Ps⁻ (biais de grille négatif
mesuré : −3.1 mHa) ; limitation publiée.

**Volet C — série étendue** (données figées, Z = 7..10) : F1×R3 passe
partout, gain constant ≈ 19.3 mHa.

**Loi Z assemblée** — résiduel relatif de la référence split-ζ :

| H⁻ | Ps⁻ | Z=2 | Z=3 | Z=4 | Z=6 | Z=10 |
|---|---|---|---|---|---|---|
| 10.7 % | 8.6 % | 2.08 % | 0.91 % | 0.54 % | 0.28 % | 0.15 % |

La corrélation pèse ~46 mHa constants quand l'énergie croît en Z² — et le
facteur de Jastrow à portée dérivée en récupère une part constante (~19 mHa
pour F1×R3, ~43 mHa pour F2×R2), en tout point de la série, y compris aux
extrêmes de charge et de masse.

## B3-FAIL du chantier

1. **Critère T1 v1** (« l'intégrande P31 dégrade l'énergie pour tout β ») :
   réfuté par la mesure — la forme P31 gagne ~5 mHa à β ≥ 3. Critère
   corrigé sur la distorsion (+0.13 Ha) et le ratio de gains (×5.4).
2. **Corpus P31** : intégrande défectueux (ci-dessus) — republication
   requise, registre F9 étendu.
3. **Ps⁻ × F2×R3** : hors domaine de la boîte (densité diffuse tronquée) —
   limite mesurée de l'intégrateur complet, publiée.

## Ce que le chantier apprend

- La frontière r₁₂ — le résultat phare du corpus — se fermait par son
  propre falsifieur, avec la règle de portée **déjà présente dans le
  corpus** (densité, P31/P28). Ce qui manquait n'était pas un principe
  physique : c'était un intégrateur correct.
- Le registre A4 : **F3 fermée** (3 frontières fermées sur 11), comptage
  ddll « déficit confirmé et fermé » — le degré de liberté 2-corps, une
  fois ajouté, se laisse dériver sans paramètre, comme la conjecture v2
  le prédit (A5 inchangé : 7/7).
- Coût de fermeture mesuré : volet A 1444 s (0.7 s/évaluation, grille
  300×192) — à comparer au « ×10 » déclaré en F3.

**Falsifieur (réouverture).** Toute exécution de R12-FERM-1.0 donnant
F1×R3 perdante en un Z du domaine variationnel rouvre la frontière.

## Artefacts

- `p39_fermeture_r12.py` — SHA-256 `c8478fd81cd513a6…`
- `p39_fermeture_r12_verdict.json` (+ fragments T1/A/A2/B/C)
- `p39_fermeture_r12.png`
- registre A4 mis à jour (SHA `36778295eee3b2d5…`), A5 rejoué (inchangé)

*Données externes figées : énergies exactes non relativistes de la série
He (Frankowski–Pekeris ; Thakkar–Koga ; Drake), H⁻ (Pekeris
−0.5277510165 Ha), Ps⁻ (−0.2620050702 Ha, Bhatia–Drachman/Korobov).*
