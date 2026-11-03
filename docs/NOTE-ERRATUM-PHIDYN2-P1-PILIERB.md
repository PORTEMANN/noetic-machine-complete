# ERRATUM — VERDICT-ΦDYN2-P1, pilier B (instrument de comptage défectueux)

**Date :** 2026-11-03 · **Statut :** erratum daté — corrige VERDICT-ΦDYN2-P1 (d862875), pilier B uniquement. Piliers A, C, D et le sous-test adiabatique ne sont pas touchés.

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| Le défaut d'instrument (comptes = longueurs de mots, archives 233/377 vs 126/202) · ce qui tient (résidus d'identité) et ce qui tombe (frontière en comptes) · les leçons (produits grid-wide interdits) | « Un contrôle à valeur unique ne valide jamais un instrument » (la coïncidence 377/233 = φ comme piège numérique) | — (note procédurale : pas de couche spéculée) |

## Le défaut

Le comptage de bandes par produit de matrices de transfert sur grille 2¹⁸ (`compte_bandes_mot`, src/phidyn2_p1_pilierB.py) est **numériquement instable** : aux niveaux 11–14, les entrées du produit explosent hors bande et la précision flottante s'effondre, produisant des croisements fantômes de |Tr/2| = 1. Mesuré ce soir : le comptage retourne la **longueur du mot** (89/144/233/377) — valeur aliasée, non spectrale. Les archives le confirment : comptes ρ = 0 = 233/377, alors que T24 donne 126/202.

**Pourquoi le contrôle d'alors n'a pas attrapé le défaut.** Le contrôle « ratio c₁₄/c₁₃ → φ » est passé spurious : 377/233 = φ par coïncidence des nombres de Fibonacci. Un contrôle à valeur unique ne valide jamais un instrument.

## Ce qui tombe

- La **frontière en espace des comptes** de P1-B : « 0 flip → ratio = φ exact (1,6180, 20/20) » et les colonnes « ratio médian » et « dans φ ± 0,02 » du tableau phason. Ces nombres mesuraient des longueurs de mots aliasées.
- Toute conclusion quantitative de P1-B fondée sur les comptes grid-wide.

## Ce qui tient

- Les **résidus d'identité de trace** : calculés par produits de préfixes courts à énergie fixe (t = 0,7, en bande — pas d'explosion), ils sont exacts : 0 flip → 2,2·10⁻¹⁵ (epsilon machine) ; 1 flip → résidu 0,7–16 (map brisée) ; ≥ 4 flips → mort. **La hiérarchie de dommages par flip (exact → dégradé → mort) est maintenue.**
- Le verdict de P1 dans son ensemble (générateur reconnu, Fricke à 2,6·10⁻³⁰, classification 80/80, T-1 fine-structure) repose sur les piliers A, C, D — **inchangé**.

## La leçon gravée au registre

1. **Produits de matrices de transfert grid-wide : interdits** pour le comptage spectral. Instrument de référence : spectre de l'anneau périodique (Jacobi L×L, `eigvalsh`) — stable, exact, valable pour les mots déformés, croisé avec le trace map (voir VERDICT-ΦDYN5B).
2. **Un contrôle à valeur unique ne valide jamais un instrument** — 377/233 = φ était un piège numérique, pas une signature. Tout instrument se contrôle par un canal indépendant.
3. **La doctrine des frontières s'applique aux instruments** : le produit grid-wide est mort dès le niveau 11 ; l'anneau est vivant partout.

*Frontière en comptes sous phason : ouverte, à re-mesurer par l'instrument anneau si un chantier l'exige.*
