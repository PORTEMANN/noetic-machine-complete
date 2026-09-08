# Campagne T1 — Q-KO6-2026-09

**Statut : exécutée en local le 09/09/2026 ; publiée le 09/09/2026
(pause de tri, décision d'auteur).**

## Question

Sous la table C-KO6-A3b (datée : J²=+1, Jγ=+γJ, JD=−DJ), existe-t-il (D, J, γ)
de taille n impaire vérifiant l'ordre 1 avec un scalaire complexe unique (A = ℂ) ?

## Réponse : OUI — existence dès n = 3

Exemple minimal (vérifié matrice par matrice, tolérance figée 1e-9) :

- γ = diag(1, 1, −1)
- J = J₀∘K, J₀ = diag(−1, 1, 1)
- D réel symétrique, D₁₃ = D₃₁ = 1, autres entrées nulles

Les 7 axiomes d'AXIOMES.md passent. Exemple n = 7 exhibé de même
(γ = diag(1,1,−1,−1,−1,−1,−1), même J₀ étendu, D₁₃ = 1).

## Comptes exacts (espace figé : J₀ permutations signées par blocs, J₀²=+1 ;
D réel symétrique hors-chiral à entrées {0,±1}, D≠0)

| n | (p,q) | J₀ | couples (J₀,D) |
|---|-------|-----|----------------|
| 1 | (0,1),(1,0) | 0 | **0 — n=1 exclu** ({D,γ}=0 avec γ=±I force D=0) |
| 3 | (1,2),(2,1) | 12+12 | 32+32 = **64** |
| 5 | tous blocs | 664 | **13 696** |
| 7 | tous blocs | 13 120 | **8 384 512** |

Contrôles gelés : recoupement par énumération brute exhaustif à n=3 et n=5
(6/6 blocs conformes) ; exemplaires d'orbites vérifiés 20/20 (n=3), 536/536
(n=5), 12 308/12 308 (n=7) ; batterie de leviers : 4/4 axiomes tués détectés.

## Lecture honnête (déclarée dans la fiche avant le run)

Avec A = ℂ, l'ordre 1 est **vacuous** (π(λ)=λI ⇒ [D,π(λ)]=0 — mesuré
numériquement). La substance de la question gelée vivait dans la **taille
impaire** sous la table A3b — tranchée : le lemme de parité ne s'applique pas,
et l'existence est effective dès n=3. La question plus forte (taille impaire
avec ordre 1 **non vacuous**, algèbre plus riche — ex. A = ℂ⊕ℂ avec somme de
dimensions impaire) est une **nouvelle fiche gelée** (candidate T2), pas un
critère déplacé.

Conséquence sur le registre : la « question ouverte honnête » d'AXIOMES.md
reçoit sa réponse datée ; publication décidée à la pause de tri du
09/09/2026 : fiche CAMPAIGNS.md + matrices, conformément à « Si oui, on
publie les trois matrices. »

## Artefacts

- `src/t1_ko6_taille_impaire.py`
- `data/t1_ko6_taille_impaire_verdict.json`
- empreintes complètes (octets du dépôt) : `data/t1_t2_t4_shasums.txt`

Incident de comptage documenté dans le verdict (premier run : sous-comptage
des orbites, détecté par le recoupement brut gelé, corrigé avant verdict —
protocole inchangé).
