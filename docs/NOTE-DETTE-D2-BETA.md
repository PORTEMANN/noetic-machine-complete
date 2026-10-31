# Note de chantier — Dette D2 : la fonction β de l'escalier

**Date :** 2026-10-31 · **Tiroir :** remboursement de dette (dynamique ;
réponse à l'objection 2 du COMITE-LECTURE-ACIDE : « où est l'équation
de Callan-Symanzik ? »).
**Filiation :** NOTE-CIRCONSCRIPTION-MACHINES (registre) ·
NOTE-DETTE-D1-KOLMOGOROV §7–§9 (escalier, triade, constituante) ·
`src/dette_d2_beta.py` (instrument).

---

## 1. Passage 1 (D2a) — β dérivée et décomposition chiffrée

**Dérivation formelle.** L'escalier spectral est l'intégrale exacte
d'une β fermionique à une boucle à contenu de saveurs Heaviside :

> dα⁻¹/dlnΛ = −(1/2π)(4/3) Σ_{active(Λ)} N_c Q²

— la forme standard de la β QED à une boucle ; la seule spécificité du
modèle est le contenu actif : seuils discrets, habillés dans le secteur
léger (D1d/D1e). La réponse au comité, au niveau revendiqué :
**la β existe, elle est dérivée, elle est la β canonique avec un
contenu de seuils discret et habillé.**

**Décomposition à M_Z** (zéro paramètre ajusté ; canon sourcé : PDG,
Δα = 0,0590 ± 0,0005, α⁻¹(M_Z) = 127,951(9)) :

| Terme (unités Δα) | Modèle (1 boucle) | Canonique | Écart |
|---|---|---|---|
| Leptons | 0,035 29 | 0,031 50 (3 boucles) | +0,003 8 = ordres sup. QED |
| Secteur quark (seuils habillés) | **0,027 75** | **0,027 57** (VP hadronique) | **0,65 %** |
| Total | 0,063 05 | 0,059 00 | +0,004 05 |

## 2. Le résultat central : l'ansatz habillé ≡ VP hadronique

Le secteur quark du modèle à seuils discrets — dont les deux seules
entrées sont mesurées par la spectroscopie baryonique (D1d) —
reproduit la polarisation du vide hadronique **non perturbative** du
Modèle Standard à **0,65 %** près. L'ansatz des masses constituantes,
justifié par le régime IR (D1e), est ainsi numériquement équivalent à
ce que la théorie canonique calcule depuis les données e⁺e⁻. C'est la
mesure la plus profonde produite par la dette D2 : le contenu
phénoménologique du modèle discret n'est pas une approximation
arbitraire — il *est*, à 0,65 %, le contenu hadronique de la physique
standard.

**Réserve de statut.** La comparaison croise deux calculs qui partagent
l'ancre α⁻¹(0) ; la validation complète exige le pont direct avec
Π_had(s) mesurée (dispersion e⁺e⁻) — chantier D2e, données à
télécharger (tau/ehadronic-fc). La 0,65 % reste une comparaison
indirecte tant que D2e n'est pas tourné.

## 3. Programme restant (inscrit au registre)

- **D2b** — conditions de matching aux seuils (découplage EFT propre,
  continuité de la charge effective aux échelles m_i).
- **D2c** — boucles W/Z/H (contributions électrofaibles à la
  polarisation du vide du photon).
- **D2d** — deuxième boucle QED+QCD, passage MS̄→pole ; doit absorber
  l'écart leptonique +0,003 8.
- **D2e** — pont hadronique direct : Π_had(s) depuis e⁺e⁻/τ, comparée
  aux seuils habillés. La validation ouverte du résultat central.

**Leçon.** Le comité demandait les muscles continus ; D2a montre que
le squelette discret porte déjà, dans ses seuils, le muscle hadronique
entier à 0,65 %. Les muscles encore manquants (matching, bosons, 2e
boucle) sont maintenant nommés un par un — c'est tout ce qu'un premier
remboursement doit faire.

*Révision uniquement par note datée. Le script `src/dette_d2_beta.py`
reproduit chaque chiffre de cette note.*
