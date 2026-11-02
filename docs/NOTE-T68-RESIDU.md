# Note — T68 : le triplet de résidus mesuré sur les triplets certifiés

**Date :** 2026-11-02 · **Verdict :** `data/t68_ko6_residu_verdict.json`
(**4/4 SUCCÈS**) · **Script :** `src/t68_ko6_residu.py`.
**Filiation :** NOTE-ANTIK-ANALYSE §2 (gisement Remizov) · T5/T6 (porteur)
· T8 (triplet MS) · archives Antik (théorème du résidu, janvier 2026).

---

## 1. Ce qui est mesuré

La fiche gelée T68-RESIDU-1.0 transpose le triplet noétique
(Rζ, Rtop, Rdyn) du théorème du résidu en objets exacts pour un triplet
spectral fini à Dirac auto-adjoint :

- **Rζ := Tr(D_F²)** — la zêta spectrale en s = −1, exacte pour spectre
  fini ;
- **Rtop := dim ker(D_F)** — la multiplicité des zéros (les nœuds
  spectateurs de T13) ;
- **Rdyn := max Im(spec(D_F))** — la distance à la Ligne Critique :
  l'auto-adjonction place l'objet *sur* la ligne (Rdyn = 0).

## 2. Résultats (critères gelés, première exécution)

| Objet | Rζ | Rtop | Rdyn | Régression |
|---|---|---|---|---|
| porteur ℂ ⊕ M₂(ℂ) (T5/T6) | **8** | **3** | 0,0 | ✓ exacte (T6/T8) |
| triplet MS, Y = I (T8) | **32** | **0** | 0,0 | ✓ exacte (T8 V3) |

**Leviers (tualbles) :** perturbation non auto-adjointe déclarée
(D + 0,1i·A, A = permutation) → Rdyn = 0,1 détecté sur les deux objets ;
déformation ρ → 1,5 du porteur (T6) → Rtop 3 → 1 (les deux zéros de la
chaîne P4 se soulèvent, le spectateur ℂ survit).

## 3. Lectures

1. **Le théorème du résidu de janvier 2026 a sa première instance
   bancable et banc-certifiée** — les archives Antik ne sont plus seulement
   un gisement : leur invariant fondateur est désormais mesuré par la
   machine sur ses propres objets certifiés.
2. **Rtop distingue proprement les objets** : le porteur minimal porte
   3 zéros (un spectateur + la paire protégée de la chaîne), le MS à
   Yukawa unitaire n'en porte aucun — le « zéro protégé » de T13 est une
   propriété du porteur, pas du MS générique.
3. **Rdyn = 0 partout dans le banc** : l'auto-adjonction du Dirac fini
   *est* la Ligne Critique des archives. Les objets du banc vivent sur la
   ligne — et le levier montre ce que la déformation non hermitienne
   coûte : Rdyn > 0, sortie de la ligne, détectée au centième près.
4. **Pont vers le muscle manquant n°1** : ce n'est pas U(t), mais c'est la
   stabilité dynamique lue dans le spectre — exactement la promesse
   Remizov (diagnostiquer par les pôles, non par la simulation).

## 4. Limites déclarées

La transposition (Rtop := dim ker plutôt que Index de Fredholm, qui
s'annule pour tout opérateur auto-adjoint) est déclarée dans la fiche :
pour les objets hermitiens du banc, le noyau est l'invariant topologique
significant ; un opérateur non hermitien du banc (chantier à part) rendra
l'indice de Fredholm pertinent. Rζ = Tr D² ne porte pas encore la
régularisation −1/12 du document Antik (objet infini — pas de spectre
fini) : la correspondance ζ(−1) reste un pont à construire, daté.

*Révision uniquement par note datée. Fiche gelée embarquée dans le script.*
