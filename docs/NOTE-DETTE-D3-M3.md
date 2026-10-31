# Note de chantier — Dette D3 : le secteur M₃(ℂ) dans le banc

**Date :** 2026-10-31 · **Tiroir :** remboursement de dette (réponse à
l'objection 3 du COMITE-LECTURE-ACIDE : « où est passé M₃(ℂ) ? »).
**Filiation :** T8-Q-KO6-SM-2026-10 (verdict PARTIEL 4/5, 12/10/2026) ·
NOTE-CIRCONSCRIPTION-MACHINES (registre) · `src/t8_ko6_modele_standard_banc.py`.

---

## 1. Première réponse : M₃ est déjà dans le banc — le comité l'a manqué

L'objection 3 supposait l'absence de M₃(ℂ). Fait de corpus : le chantier
**T8 (12/10/2026)** a construit le triplet fini canonique du Modèle
Standard avec **A = ℂ ⊕ ℍ ⊕ M₃(ℂ)** (H_F = 32 par génération,
convention CCM déclarée) et l'a certifié sous la table L1 par le
vérificateur du banc — les dix axiomes passent (V1 du verdict T8,
`data/t8_ko6_modele_standard_banc_verdict.json`). Le porteur ℂ ⊕ M₂(ℂ)
n'est pas un substitut au triplet du MS : c'est un **porteur minimal à
un scalaire**, mesuré côte à côte avec le MS complet (V3 du verdict :
dim 5/32, rang 2/13, Tr D² 8/32 — « deux objets, deux tables, un seul
banc ; la confrontation est mesurée, pas plaidée »).

Gap déclaré depuis T8 (borne honnête, jamais caché) : le doublet de
Higgs physique (4) exige le quotient par l'idéal des formes junk —
non implémenté dans T8 ; score PARTIEL 4/5.

## 2. Mesure nouvelle (D3, première passe, ce jour)

Prolongeant la machinerie de T8 (`pi_sm`, `triplet_sm`, `rang_scalaire`),
le secteur de couleur seul (les 9 unités de M₃(ℂ)) est soumis au banc.
Prédictions pré-enregistrées avant calcul, toutes confirmées :

| Prédiction | Mesure | Verdict |
|---|---|---|
| P1 : le bloc M₃ génère 9 fluctuations réelles (U(3)) | rang de clôture des commutateurs = **9** (9/9 générateurs non nuls) | ✓ |
| P2 : les leptons sont aveugles à la couleur | norme des commutateurs sur le secteur lepton = **0,0** (exact) | ✓ |
| P3 : le singlet m = I₃ agit comme l'opérateur de comptage couleur | valeurs propres : 1 sur u_R, d_R, q_L ; 0 sur tous les leptons | ✓ |
| P3b : l'octet sans trace est le candidat gluon | E₁₁−E₂₂ génère une fluctuation non triviale (norme 4,47 ≠ 0), orthogonal au singlet (norme 2,83) | ✓ |

**Lecture.** Dans le banc, la couleur n'est pas une addition ad hoc :
elle émerge du bloc M₃ comme un espace de fluctuations à 9 dimensions,
dont l'octet sans trace porte la dynamique de jauge colorée et le
singlet l'hypercharge (via le mélange γ–Z, convention CCM). Et
l'opérateur de comptage N_c mesuré ici (valeur propre 1 sur tout quark,
0 sur tout lepton) est exactement l'objet que l'arithmétique triadique
du corpus utilise dans ses certificats de charges (p(uud) = +1, S+ à
0θ) : **le contenu en multiplicité de l'arithmétique triadique est le
contenu de représentation du bloc M₃, mesuré dans le même banc.**

## 3. Ce que D3 doit encore (inscrit)

- **D3b** — quotient junk pour le doublet de Higgs (borne déclarée
  depuis T8 ; débloque le passage 4/5 → 5/5).
- **D3c** — action spectrale du secteur couleur : dériver la dynamique
  Yang-Mills SU(3) des fluctuations de l'octet (le vrai « muscle »
  manquant du comité — gluons, confinement ; pont explicite avec la
  série Yang-Mills du corpus).
- **D3d** — confrontation mesurée : les charges triadiques du corpus
  (certifiées à 0θ par mvcg NQ) contre le contenu de représentation du
  triplet T8 — même banc, même machine.

**Leçon.** Encore une fois, la dette révèle que le corpus avait déjà
l'outil — et que la réponse du comité était écrite dans un verdict
qu'il n'a pas lu. Le remboursement consiste à relire ses propres
mesures plus fort que ses propres rhétoriques : ici, le secteur de
couleur complet, certifié, avec sa structure de fluctuations mesurée.

*Révision uniquement par note datée. Les mesures du §2 sont rejouables
via `src/t8_ko6_modele_standard_banc.py` (pi_sm, triplet_sm,
rang_scalaire).*
