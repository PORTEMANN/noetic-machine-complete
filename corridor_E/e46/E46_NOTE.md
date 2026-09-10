# Campagne E46 — verrouillage du cœur (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation de l'enlacement nucléé par plancher de densité »
- **Question unique** : un mur raide sous un plancher de densité (ρ_min=0,5,
  C=100, figés), actif à partir de t=20, conserve-t-il l'enlacement nucléé
  au-delà de l'ère des reconnexions ?
- **Contexte** : E44 (nucléation observée, évaporation avant t=20) ; E45
  (B3-FAIL : la coupure de l'amortissement ne conserve pas — 0/5 OFF, 0/5 ON —
  la tension seule détruit le lien ; le destructeur est la reconnexion, pas la
  dissipation). E46 teste le mécanisme que la lecture d'E45 désigne :
  supprimer la **condition cinématique** de la reconnexion (déplétion du
  cœur) — version GP du théorème de Kelvin.
- **Hypothèse mécaniste gelée** : la reconnexion exige une densité nulle au
  point de contact ; un plancher raide la rend coûteuse → topologie gelée
  après la nucléation. Calendrier gelé : le mur n'existe qu'à partir de t=20
  (la nucléation exige l'ère des reconnexions — mesuré en E44).
- **Conventions citées** : E44 v1 (`42c65a0c…`), amendement v2 (`bc977f17…`),
  détecteur `e44_core.py` byte-identique (`604c2232…60ae1ac7`) ; harnais E45
  réparé (écriture incrémentale reprise) ; discipline d'aveugle.
- **Protocole** : `e46_protocole.json` (E46-VERROU-1.0, haché
  `d019ee3a…6629d13`, convention d'auto-référence exclue déclarée) ;
  harnais `src/e46_run.py` (`b28aa4bc…c40c73ba`, validé en --smoke hors
  campagne le 09/09/2026).
- **Structure gelée** : identique à E45 — 24 runs (440101–440124), snapshots
  t=8,12,16,20 ; branchement ON/OFF depuis t=20 pour tout run nucléant ;
  snapshots t=45,90. **Facteur unique** : le mur de densité (γ=0,3 dans les
  deux branches — ne pas mélanger avec la coupure d'amortissement, réfutée
  en E45).
- **Prédictions pré-enregistrées** :
  - P0 (filiation) : 440103 reproduit sa paire liée à t=12 — sinon B3-FAIL
    technique ;
  - P1 : persistance ON > OFF (directionnel) ;
  - P2 : les snapshots t≤20 reproduisent E45 à l'identique (contrôle de
    cohérence fort — même phase 1, même harnais) ;
  - P3 : observationnel — longueur totale des boucles, distribution des Lk
    persistants.
- **Règle de verdict gelée** : SUCCÈS si P0 et P1 ; PARTIEL si P0 et moins
  de 3 runs branchés ; B3-FAIL si P0 et absence de différence ON/OFF —
  mécanisme réfuté, critère non déplacé, la frontière passe au pinning
  spatial (E37 strict) ou à la rotation (E43).
- **Falsifieur global** : aucune différence de persistance ON/OFF → réfuté,
  publié au même niveau.

## Artefacts (staging local)

- `e46_protocole.json` — gelé, haché `d019ee3a…6629d13`
- `src/e46_run.py` — `b28aa4bc…c40c73ba`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : ANOMALIE DÉCLARÉE

**La règle gelée est formellement satisfaite, et les compteurs gelés du
détecteur l'annulent. Le mécanisme n'est ni confirmé ni réfuté — il doit
être réparé.**

- P0 (filiation) : **PASS** — 440103 reproduit sa paire liée à t=12 ;
- P2 (cohérence forte) : **PASS** — la phase 1 reproduit E45 à l'identique
  (mêmes 5 runs nucléés : 440102, 440103, 440109, 440110, 440117) ;
- P1 (formel) : persistance 5/5 en ON contre 0/5 en OFF → satisfaite ;
- **MAIS** les compteurs d'anomalies du détecteur (observables gelés) :
  snapshots ON à t=45 saturés — boucles au plafond (400, 4 runs/5),
  anomalies de flux jusqu'à 2880, ambiguïtés jusqu'à 48 125, paires « liées »
  en masse au ras du seuil (128 paires dans 440117, |Lk| ≈ 0,50–0,55) —
  contre **0 anomalie et 0 ambiguïté** dans tous les snapshots OFF, dans
  toute la phase 1, et dans toute l'histoire E44/E45. Puis **effondrement
  total à t=90 en ON** (0 boucle partout).

### Analyse du mécanisme (déclarée)

Le mur gelé V = ρ²−1 + C·max(0, ρ_min−ρ)² a deux composantes qui
**s'affrontent** dans la branche ON (γ=0,3 conservé) : la partie
conservative (i) est bien un plancher de pression (incompressibilité — le
mécanisme visé, type Kelvin) ; la partie dissipative (γ) avec V grand et
positif sous ρ_min *amplifie* la déplétion au lieu de la restaurer
(ρ décroît quand V>0). La zone du cœur est donc à la fois comprimée et
rongée — phase rapide + amplitude erratique → bruit de phase massif au
détecteur → fausses plaquettes → fausses boucles → faux liens. La
« persistance » 5/5 est de la saturation du détecteur, pas de la
conservation ; l'effondrement à t=90 en est la preuve terminale.

### Statut régulé

Verdict publié : **ANOMALIE — succès formel annulé par les compteurs
gelés** (précédent du corpus : P31, artefact de l'intégrande ; E44,
cellules anormales de paroi). E46 ne tranche pas la conservation. La
réparation est déjà lisible dans les données : **E47** devra séparer les
deux composantes du mur — 2×2 gelé : γ ∈ {0 ; 0,3} × mur ∈ {pression
(+C, conservative)} — et tenir le détecteur propre (anom = amb = 0 exigé
comme critère de lisibilité pré-enregistré). Le cas γ=0 + mur de pression
est le test propre du gel de Kelvin.
