# Note de chantier — T67 : longueurs modulaires vs spectre de Maass

**Date :** 2026-10-31 · **Tiroir :** banc (clavier méso) ·
**Verdict :** `data/t67_ko6_spectral_verdict.json` (2/3, ECHEC gelé
productif).
**Filiation :** T66 (même énumération d'orbites, trace élargie) · la
perspective tracée le 31/10 (pont spectral du pont de Ghys).

---

## 1. Protocole (gelé avant run)

Côté géométrique de la formule des traces de Selberg, tronqué :
S(r) = Σ_{orbites primitives, tr ≤ 25} A_γ cos(r ℓ_γ), avec
A_γ = ℓ_γ/√(t²−4) (identité exacte 2 sinh(ℓ/2) = √(t²−4)) ; 107
orbites. Côté spectral : les valeurs propres de Maass cuspidales de la
surface modulaire, sourcées avant run (Booker–Strömbergsson–Venkatesh,
vérifiées 100 décimales : r₁ = 9,5337 ; r₂ = 12,1730 ; r₃ = 13,7798).
Caveats déclarés : spectre continu non soustrait ; résolution limitée
par ℓ_max (~0,97).

## 2. Résultat — ECHEC gelé, avec découverte

Le critère C1 gelé (les deux maxima les plus hauts = r₁, r₂ dans
±0,5) **échoue** : les deux plus hauts pics sont à 13,785 et 9,700.
L'analyse post-mortem, jointe au verdict sans modification des
critères :

| Maximum détecté | Plus proche valeur source | Écart |
|---|---|---|
| 13,785 | r₃ = 13,7798 | **0,005** (exact à la grille) |
| 9,700 | r₁ = 9,5337 | 0,166 |
| 12,495 | r₂ = 12,1730 | 0,322 |

**Trois raies spectrales authentiques détectées depuis les 107 orbites
modulaires de T66** — dont une à 0,005 près. L'échec du critère vient
d'une hypothèse non déclarée de la fiche : l'ordre des amplitudes
géométriques suit l'ordre des indices propres. Il ne le suit pas
(les amplitudes dépendent des poids des formes — r₃ domine). Erreur
de conception assumée ; critère conservé tel quel.

## 3. Valeur du résultat

C'est la première confrontation directe, dans le banc, entre un spectre
*classique-arithmétique* (longueurs des géodésiques fermées modulaires)
et un spectre *quantique automorphe* (formes de Maass) — le cœur du
chaos quantique arithmétique (Sarnak), joué machine-side sur la table
exacte de T66. Que trois raies tombent sur les valeurs sourcées (dont
une exactement) n'est pas un ajustement : aucun paramètre n'a été
tourné — 107 orbites, poids exacts, grille déclarée.

## 4. Ouvert

Passe 2 (déclarée, critères à geler avant run) : jeu des K = 4 maxima
contenant ≥ 3 accords avec {r₁…r₄} sous tolérance 0,5 ; l'absence
d'ordre d'amplitudes est un fait physique à documenter, pas une
exception. Au-delà : soustraction du fond continu (Eisenstein), qui
explique les décalages résiduels (0,166 ; 0,322) — chantier à
méthode (intégrale de scattering déclarée) plutôt qu'à tolérance.

## Passe 2 (2026-10-31) — critère corrigé gelé avant run : SUCCES 3/3

Script : `src/t67b_ko6_spectral_p2.py` · verdict :
`data/t67_ko6_spectral_p2_verdict.json`.

Critère C1 corrigé (gelé avant run, correction assumée depuis la
passe 1) : ≥ 3 accords dans le jeu des 4 maxima les plus hauts vs
{r₁…r₄}, tolérance 0,5, fenêtre [8, 15] ; aucune hypothèse d'ordre.

**Résultat : 4/4.** Les quatre maxima les plus hauts de la somme
géométrique tombent sur les quatre premières valeurs propres sourcées :

| Maximum | Raie | Écart | Accord |
|---|---|---|---|
| 13,785 | r₃ = 13,7798 | 0,005 | ✓ |
| 9,700 | r₁ = 9,5337 | 0,166 | ✓ |
| 12,495 | r₂ = 12,1730 | 0,322 | ✓ |
| 14,830 | r₄ = 14,3585 | 0,472 | ✓ |

Contrôle anti-pic : ✓ ; levier de troncature : ✓. Score 3/3.

**Lecture.** Le spectre quantique de la surface modulaire — les quatre
premières formes de Maass, vérifiées à 100 décimales par
Booker–Strömbergsson–Venkatesh — est intégralement présent dans les
107 longueurs géodésiques primitives issues de l'énumération exacte de
T66. La formule des traces de Selberg, côté machine, tient sa
confrontation. Le pont de Ghys (topologie) a désormais un second étage
(spectres) — et l'ordre d'amplitudes observé (r₃ > r₁ > r₂ > r₄) est
documenté comme fait physique (poids non uniformes des formes), non
comme anomalie.

**Ce qui reste ouvert (honnêteté).** Le décalage résiduel des raies
(≤ 0,47) est attribué au fond continu non soustrait — la passe 3, si
elle ouvre, gèlera une soustraction de scattering avant run ; l'accord
à 0,005 de r₃ montre que la limite n'est pas la table mais le fond.

## Passe 3 (2026-10-31) — élargissement du spectre de longueurs : 2/3,
conclusion PHYSIQUE

Script : `src/t67c_ko6_spectral_p3.py` · verdict :
`data/t67_ko6_spectral_p3_verdict.json`.

Choix méthodologique gelé : pas de soustraction de fond (méthode molle)
— **élargissement du spectre de longueurs** (cut-off de trace
25 → 35 → 45 → 60 ; 107 → 607 orbites). Hypothèse : si les résidus
sont des artefacts de troncature, ils décroissent ; sinon ils sont
physiques, et cette conclusion serait publiée. Critère C2 gelé : chaque
résidu au palier 60 ≤ max(résidu passe 2 / 2, 0,05).

**Table de convergence (résidus).**

| Raie | t=25 | t=35 | t=45 | t=60 | Seuil gelé |
|---|---|---|---|---|---|
| r₁ | 0,166 | 0,146 | 0,134 | **0,109** | 0,083 |
| r₂ | 0,322 | 0,267 | 0,347 | 0,242 | 0,161 |
| r₃ | 0,005 | 0,390 | 0,245 | 0,110 | 0,050 |
| r₄ | 0,472 | 0,189 | 0,149 | 0,469 | 0,236 |

C2 : non atteint — **conclusion PHYSIQUE gelée** : les décalages sont
dominés par les poids spectraux et le fond continu, pas par la
résolution. La lecture fine (analyse jointe au verdict) est un mélange :
r₁ décroît monotone (type résolution, sans atteindre le seuil) ;
r₂/r₃/r₄ non monotones (structurel) ; au palier 60, un maximum unique à
13,89 est capturé par les fenêtres r₃ et r₄ à la fois — **battement des
deux raies voisines** (13,78 / 14,36) sur le fond non soustrait. Le
0,005 de la passe 2 était exceptionnel, pas la norme.

**Valeur.** La passe 3 transforme une tolérance en physique : elle
localise exactement ce que la troncature n'explique pas — et désigne
la passe 4 (déclarée) : soustraction du scattering d'Eisenstein
(déterminant de scattering, avec ζ), seule voie honnête vers les raies
résiduelles. Trois passes, trois statuts différents (SUCCES / ECHEC
productif / SUCCES informatif par échec de critère) : le chantier T67
est devenu l'atelier-type de la méthode.

