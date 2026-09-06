# AXIOMES.md — page minimale (gelée, sans le nombre 7)

Cette page gèle les axiomes de travail du programme « triplets spectraux finis ».
Elle ne contient volontairement **aucune cible numérique** — en particulier pas le nombre 7.
Une cible est une hypothèse de campagne, déclarée dans `CAMPAIGNS.md` ; jamais un axiome.

## Axiomes gelés

1. **Parité** : {D, γ} = 0 (triplet pair).
2. **Réalité KO-6** : table de signes **datée**, citée par son ID de `CONVENTIONS.md`
   (C-KO6-L1 ou C-KO6-A3b à ce jour).
3. **Structure réelle** : condition de réalité de Connes pour J.
4. **Ordre 1** : [[D, π(a)], J π(b)* J⁻¹] = 0 pour tous a, b ∈ A.
5. **Krajewski** : les diagrammes de Krajewski (matrice de multiplicités m_ij) classent
   les représentations ; ils ne remplacent pas D.
6. **Un scalaire complexe** : un secteur scalaire complexe unique.
7. **Non-trivialité** : D ≠ 0.

## Lemme de parité (conditionnel)

Sous une table avec **Jγ = −γJ** et J inversible : J échange H⁺ et H⁻, donc dim H est paire.

- Sous **C-KO6-L1** : tout candidat de dimension impaire est exclu par ce lemme.
- Sous **C-KO6-A3b** : le lemme ne s'applique pas ; une dimension impaire est concevable.

Changer de table change le statut d'un candidat — et doit être dit.

## Champion explicite (étalon 4×4)

Triplet minimal **opérationnel**, déjà construit et vérifié matriciellement (A3b, 4/4) :

- A_F = ℂ ⊕ ℂ, H_F = ℂ⁴ ;
- γ = diag(1, 1, −1, −1) ;
- J₀ réelle, J₀² = +1 ;
- D réel symétrique anticommutant avec γ ;
- espace mesuré : 36 J₀ × 80 D.

Tout nouvel énoncé de minimalité se mesure **d'abord** contre cet étalon — le plus petit
exemple qui marche avant toute énumération à dim ≤ 24.

## Test unique d'un candidat (D, J, γ)

Un candidat n'est déclaré « triplet » que s'il passe, **matrice par matrice** :

1. J² (selon la table citée) ;
2. JD (selon la table citée) ;
3. Jγ (selon la table citée) ;
4. {D, γ} = 0 ;
5. ordre 1 : [[D, π(a)], J π(b)* J⁻¹] = 0 ;
6. sous C-KO6-L1 : parité de dim H.

## État résiduel honnête (2026-09-06)

Sous cette page, ce qui tient sans ambiguïté est maigre et daté :

- **k ≥ 2** pour un triplet fini réel irréductible de KO-dimension 6 (obstruction mesurée) ;
- **2 + 2 + 3 = 7** est vrai — comme fait d'arithmétique des multiplicités
  (m = [[0,2],[2,3]]), **pas** comme théorème de géométrie spectrale ;
- le minimum opérationnel construit est **C4** (A3b), puis une fenêtre de 60 matrices en
  dimension 5 (F4) ;
- la question ouverte honnête : *sous une table de signes datée, existe-t-il (D, J, γ) de
  taille impaire vérifiant l'ordre 1 avec un scalaire ?* Si oui, on publie les trois
  matrices. Si non, le 7 sort du tiroir thèse.

---

*Page gelée le 2026-09-06, en réponse à la note de lecture « Incohérences internes du
corpus Portemann » (sept. 2026). Addenda seulement.*
