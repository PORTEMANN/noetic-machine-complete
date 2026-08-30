# P38 — L'attention éprouvée : carte constitutive du bloc minimal

**Patrice Portemann — corpus Machine Noétique, chantier P38**
Protocole gelé ATTN-1.0 · poids dérivés, zéro apprentissage, exhaustivité déclarée · SHA-256
30 août 2026

## Verdict

**SUCCÈS.** Le bloc d'attention minimal est éprouvé sur quatre tâches
gelées à vérification exhaustive, poids entièrement dérivés, zéro
apprentissage. Le verdict n'est pas « l'attention marche » ni
« l'attention est universelle » : c'est une **carte constitutive** —
quel degré de liberté est constitutif de quelle tâche, et quel constitutif
manque pour laquelle.

| Degré de liberté | Statut | Mesure |
|---|---|---|
| position (one-hot dérivé) | **CONSTITUTIVE** de tout ce qui n'est pas symétrique | copie : 8/262144 sans, 262144/262144 avec |
| softmax | **NON constitutif** | linéaire exact ; softmax à coût d'échelle dérivé β ≥ ln((n−1)/ε)/Δ |
| profondeur | **CONSTITUTIVE** pour la parité (cohérence P36/F12) | 1 couche : meilleure exactitude 0.6367 ; 2 couches : exact |
| comparaison | **CONSTITUTIF MANQUANT** du tri | les candidats bilinéaires dérivés échouent (3/27) |
| multi-tête | **CONSTITUTIF uniquement** pour relations incompatibles simultanées | mono-tête : 8/256 ; 2 têtes dérivées : 256/256 |

## Mesures

- **C1 — sans position** : la copie par scores uniformes est exacte sur
  8/262144 séquences (les constantes seules) ; le comptage, lui, est
  exact — la position n'est pas constitutive du sac de symboles.
- **C2 — avec position one-hot dérivée** : copie exacte sur
  **262144/262144** séquences de V=8 symboles et longueur N=6. La
  position est constitutive de la copie — prédiction pré-enregistrée
  **confirmée**.
- **C3 — softmax** : l'erreur d'argmax approché est bornée par
  (n−1)·e^{−βΔ} ; le coût d'échelle dérivé β ≥ ln((n−1)/ε)/Δ est
  vérifié à ε = 10⁻³, 10⁻⁶, 10⁻⁹ (erreur mesurée égale à la borne aux
  chiffres affichés). Le softmax n'est qu'une argmax molle à coût
  mesuré — il n'ajoute aucun degré de liberté constitutif.
- **C4 — parité** : une couche + seuil atteint au mieux 0.6367
  (exhaustif 2^8) ; deux couches dérivées sont exactes. Cohérence
  mesurée avec P36 : la profondeur est constitutive dès que la tâche
  itère, dans le bloc d'attention comme dans le réseau feedforward.
- **C5 — tri** : les scores bilinéaires dérivés candidats (x_i·x_j,
  x_i, x_j) échouent tous sur l'exhaustif 3^3 = 27 triplets (3/27
  chacun). La comparaison x_i > x_j n'est pas bilinéaire en les valeurs :
  le constitutif manquant est identifié par échec publié — le tri exige
  une non-linéarité de comparaison que le bloc minimal ne possède pas.
- **C6 — double-relation** : la tâche demande simultanément le maximum
  (tête argmax dérivée) et le comptage (tête uniforme dérivée) — deux
  relations incompatibles pour une seule distribution d'attention.
  Mono-tête : 8/256 (les constantes) ; deux têtes dérivées : **256/256**.
  Le multi-tête est constitutif **uniquement** pour relations
  incompatibles simultanées — raffinement mesuré de la prédiction
  pré-enregistrée (« multi-tête non constitutif » : confirmée pour tâches
  à une relation, réfutée pour relations incompatibles simultanées ;
  raffinement publié).

## B3-FAIL du chantier (publiés)

1. **S = bloc d'attention minimal comme trieur** : réfutée — la
   comparaison n'est pas bilinéaire, les échecs sont publiés tels quels.
2. **Comptage C1 v1** (bug interne de la machine, corrigé avant gel) :
   comparaison au niveau du jeu de données sur une forme incompatible —
   remplacée par une comparaison par séquence contre la somme exacte.
3. **C6 v1** (bug interne, corrigé avant gel) : la tête 2 recevait des
   uns comme valeurs (comptait N, pas Σb) — valeurs remplacées par les
   bits eux-mêmes, la tête uniforme dérivée calcule la somme exacte.

## Ce que le chantier apprend

La lecture ddll (conjecture A5) : chaque constitutif identifié est un
degré de liberté ajouté — la coordonnée de position (n dimensions), la
tête supplémentaire (une distribution), la non-linéarité de comparaison
(absente, à payer). Verdict ddll : **déficit** — l'attention minimale
ferme ses tâches en ajoutant des coordonnées, exactement comme P33–P39
fermaient les leviers physiques. Entrée registre F13 ajoutée ; A5 v2
étendu à **9/9** points du domaine déclaré.

Connexion directe : P36 (profondeur, F12) fournit C4 ; P34 (le neurone
formel, F1) fournit le seuil ; la structure de la carte — position /
échelle / profondeur / comparaison / multiplicité — est la transposition
aux architectures de la lecture par leviers L du corpus physique.

## Artefacts

- `p38_attention.py` — SHA-256 d2c857893439901c… (script gelé ATTN-1.0)
- `p38_attention_verdict.json` — mesures, verdicts, falsifieur
- Falsifieur pré-enregistré : copie exacte sans position ; tri exact à
  scores bilinéaires ; double-relation exacte en mono-tête. Aucun n'est
  survenu.
