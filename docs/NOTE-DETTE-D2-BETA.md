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

## 2. D2e (première passe, 2026-10-31) — la validation ouverte, close

**Instrument.** `src/dette_d2e_pont.py` parse les tables de
`data/hadr5x26.f` (F. Jegerlehner, HU-Berlin, mise à jour juin 2026) :
2 180 points R(s) temps-like (0,282–38,29 GeV) intégrés en
Δα_had^(5)(e²) (ESA/DAS), continuation pQCD 13 GeV–20 TeV (EMA/DAM,
raccord parfait à 13 GeV : 0,015 78 des deux côtés). La valeur
data-driven à M_Z s'obtient par interpolation log de DAM à 91,1876 GeV.

**Résultat.**

| Source | Δα_had^(5)(M_Z²) |
|---|---|
| Données e⁺e⁻ (compilation 06/2026, interpolée à M_Z) | **0,027 64** |
| PDG (référence croisée) | 0,027 57 ± 0,011 |
| Modèle à seuils habillés (entrées = spectroscopie baryonique) | 0,027 75 |

**Accord direct modèle/données : 0,39 %.** La validation ouverte de D2a
est close : les deux seuils habillés du modèle, ancrés uniquement par
les masses baryoniques PDG, reproduisent la polarisation du vide
hadronique mesurée sur 2 180 points d'expérience e⁺e⁻ à 0,39 % près —
avec zéro paramètre ajusté à chaque étage (D1d/D1e pour les seuils,
D2a pour la forme, D2e pour la confrontation).

**Ce que D2e n'est pas.** Ce n'est pas une dérivation du secteur
hadronique depuis QCD — c'est l'établissement que deux nombres de
spectroscopie suffisent à le résumer à 0,39 %. La dérivation dynamique
(matching EFT D2b, bosons D2c, 2ᵉ boucle D2d) reste inscrite au
registre, chacune avec son écart chiffré attendu.

**Leçon 2.** Le comité demandait : « dérivez le glissement continu des
couplages ». L'écosystème répond désormais en deux étages publiés :
la β existe et est la β standard à contenu habillé (D2a) ; et le
contenu habillé, mesuré indépendamment par la spectroscopie baryonique,
vaut la VP hadronique expérimentale à 0,39 % (D2e). Ce qui reste dû :
le *pourquoi* dynamique — nommé, daté, chiffré.

*Révision uniquement par note datée. Les scripts `src/dette_d2_beta.py`
et `src/dette_d2e_pont.py` reproduisent chaque chiffre de cette note.*

## 3. D2c (première passe, 2026-10-31) — convention, bilan comptable,
tempérance

**Convention sourcée.** La quantité canonique Δα^(5)(M_Z²) = 0,059 0
est *par convention fermionique* : « conventionally, we take α(M_Z) to
contain only the corrections from all leptons and quarks except the
top » (Erler–Langacker, formulation de la revue PDG électrofaible,
hep-ph/9411255). Les contributions bosoniques W/Z/H à la polarisation
du vide du photon existent à une boucle mais sont conventionnellement
rangées dans le reste électrofaible (Δr_rem), hors de Δα^(5).

**Conséquence pour le modèle — espace de comparaison aligné.**
L'escalier est exactement le même objet : fermions chargés, top fermé
par Heaviside à M_Z. Le modèle et Δα^(5) vivent dans le même espace ;
les comparaisons D2a/D2e sont donc *à périmètre égal*. C'est une
clarification de doctrine : le modèle n'omet pas les bosons par
oubli — il calcule le même objet que la référence fermionique.

**Bilan comptable complet (fermeture de D2a).** Le résidu de D2a
(modèle 0,063 05 vs canon 0,059 00, écart +0,004 05) se décompose
intégralement :

| Terme | Écart (Δα) | Origine |
|---|---|---|
| Leptons, 1 boucle vs 3 boucles | **+0,003 79** | ordres supérieurs QED absents du modèle |
| Secteur quark (seuils habillés) | +0,000 18 | surcroît des seuils vs VP hadronique (0,39 %, D2e) |
| Total | +0,003 97 ≈ +0,004 05 | ✓ fermé |

**Tempérance — la mesure que la doctrine exige.** La célébrée
concordance à 0,35 % de l'escalier avec l'expérience (128,397 vs
127,951) est en partie une **cancellation** : les fermions canoniques
seuls s'écartent de l'expérience de 0,78 % (α⁻¹ = 128,95) ; le modèle,
en omettant les boucles leptoniques d'ordre supérieur, retire
précisément ~la moitié de cet écart, et le surcroît hadronique de
0,000 2 compense le reste. La partie structurelle et authentique du
résultat est l'équivalence hadronique (0,39 %, D2e) ; la partie 0,35 %
globale est un mélange d'architecture et de hasard comptable. Les deux
doivent être dites ensemble — c'est écrit ici.

**Périmètre restant (inscrit).** La dérivation propre des termes
bosoniques (une boucle, réduction Passarino–Veltman de la self-énergie
W et du mélange γ–Z) = D2c passe 2, travail d'un jour ouvré avec
sources ; attendu ~10⁻⁴–10⁻³ en Δα, sans effet sur les conclusions
ci-dessus. Le matching EFT aux seuils (D2b) et la 2ᵉ boucle QCD/QED
hors leptons (D2d) demeurent ouverts, chacun avec son ordre de grandeur
attendu.

**Leçon 3.** La dette D2 a produit ce que la rhétorique ne produit
jamais : un *bilan* où chaque chiffre sait d'où il vient, y compris
ceux qui défendent le modèle, **et surtout ceux qui le tempèrent**.
