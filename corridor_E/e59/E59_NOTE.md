# Campagne E59 — la fonction de frontière τ(A, γ) (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 (`b2c2a84a…50c2a2`) —
aucune donnée de campagne n'existe. Staging local.**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « durée de vie τ du lien en fonction de la non-idéalité (A, γ) »
- **Question unique** : τ(A, γ) est-elle une loi (position mesurable de la
  frontière) ou une constante robuste de la famille GP ?
- **Conversion déclarée** : du catalogue des mécanismes à la fonction de
  frontière — le corridor a mesuré un seul point (τ < 5 à A=2, γ=0,3) ;
  le point d'appui est Kelvin (idéal : conservation exacte) ; la
  non-idéalité est paramétrée par ξ ∝ √A et γ. Précédent de style : P32.
- **Conventions citées** : construction d'E50 inchangée ; détecteur E44
  byte-identique (`604c2232…60ae1ac7`) ; suivi d'E48→E51 ; seuil |Lk| ≥ 0,5
  inchangé.
- **Protocole** : `e59_protocole.json` (haché `b2c2a84a…50c2a2`) ;
  harnais `src/e59_run.py` (`c6174157…9e7228`, validé en
  --smoke hors campagne).
- **Design gelé** : grille A ∈ {0,5 ; 1 ; 2 ; 4 ; 8} × γ ∈ {0 ; 0,3}
  (A=0,5 au bord de résolution, marqué) ; entrée unique (t=5), copies par
  point ; snapshots denses t = 5,10,15,20,25,30,45,60,90 ; τ = dernier
  snapshot lié.
- **Prédictions pré-enregistrées** : P0 (|Lk| entrée ∈ [0,9 ; 1,1]) ;
  P1 (τ non croissant en A à γ fixé ; τ(γ=0) ≥ τ(γ=0,3) point par point) ;
  P2 (τ(A=0,5, γ=0) ≥ 90 ? — mesuré, publié quel qu'il soit).
- **Règle de verdict gelée** : SUCCÈS_LOI (P0 + monotonies + τ atteint 90
  au bord — la carte devient une courbe) ; CONSTANTE_ROBUSTE (τ ≤ 45
  partout — théorème négatif : la relation est réécrivable en temps
  constant dans toute la famille résoluble ; la frontière est la famille) ;
  PARTIEL (intermédiaire — publié tel quel) ; B3-FAIL-TECHNIQUE si P0
  échoue.

## Artefacts (staging local)

- `e59_protocole.json` — gelé, haché `b2c2a84a…50c2a2`
- `src/e59_run.py` — `c6174157…9e7228`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : PARTIEL — la loi est mesurée, et elle a un plafond

**P0 PASS (entrée Lk=0,975) ; P1 PASS (les deux monotonies tiennent) ;
P2 FAUX (τ n'atteint jamais 90 — plafond à 15) → PARTIEL au sens de la
règle gelée : monotone sans divergence.**

### La fonction de frontière mesurée

| A | γ=0 | γ=0,3 |
|---|---|---|
| 0,5 (bord de résolution) | **15** | 10 |
| 1 | 10 | 5 |
| 2 | 5 | 5 |
| 4 | 5 | 5 |
| 8 | 5 | 5 |

### Lecture (déclarée)

1. **La loi existe** : τ décroît avec la non-idéalité (A : cœur déplétable ;
   γ : dissipation), point par point — la non-idéalité tarife la vie du
   lien, comme pré-enregistré ;
2. **Elle a un plafond** : τ_max = 15 unités, atteint au bord de
   résolution (A=0,5, γ=0) — la durée de vie ne diverge PAS dans le
   domaine résoluble de la famille. Le plafond est à la frontière de la
   famille (lignes idéales singulières, inatteignables sur grille) ;
3. Conséquence mesurée : dans la famille GP résoluble, la relation
   topologique est TOUJOURS réécrivable — au plus lentement en ~15 unités.
   « Pousser la frontière » au sein de la famille est clos : il faut une
   autre dynamique (clamps actifs, hors-GP — déjà déclarés) ou un autre
   continuum. C'est la conversion complète : le corridor est passé d'un
   catalogue d'échecs à une fonction mesurée, monotone, plafonnée — et le
   plafond dit où la famille finit.
