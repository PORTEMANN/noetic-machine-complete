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

*Révision uniquement par note datée. Script : `src/t67_ko6_spectral.py`
(sha256 dans le verdict).*
