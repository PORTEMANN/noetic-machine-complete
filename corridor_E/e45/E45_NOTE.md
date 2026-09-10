# Campagne E45 — capture de l'enlacement nucléé (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « capture de l'enlacement nucléé dans la trempe GP »
- **Question unique** : la coupure de l'amortissement à t=20 (mécanisme
  déclaré) conserve-t-elle l'enlacement nucléé au-delà de l'ère des
  reconnexions ?
- **Contexte** : E44 a observé la nucléation spontanée d'une paire de Hopf
  (run A/440103, t=12, Lk ≃ −1, robuste à trois estimations) et son
  évaporation avant t=20. Frontière reformulée par E44 : le maillon manquant
  n'est plus la naissance du lien mais sa **conservation**. E45 teste le
  premier mécanisme de capture.
- **Conventions citées** : protocole E44 v1 (`42c65a0c…`), amendement v2
  (`bc977f17…`), détecteur `e44_core.py` byte-identique
  (`604c2232…60ae1ac7`, copie jointe) ; discipline d'aveugle (hachage avant
  calcul).
- **Protocole** : `e45_protocole.json` (E45-CAPTURE-1.0, haché
  `c05f8724…3250d3`, convention d'auto-référence exclue déclarée) ;
  harnais `src/e45_run.py` (`11bc7369…1e2b4b92`, validé en mode --smoke
  hors campagne le 09/09/2026).
- **Structure gelée** : 24 runs de nucléation (graines 440101–440106 =
  filiation E44, 440107–440124 = extension déclarée), snapshots
  t=8,12,16,20 ; tout run nucléant ≥1 paire liée est branché depuis t=20 en
  deux copies : OFF (γ=0,3 maintenu) et ON (γ=0,0 coupé) jusqu'à t=90
  (snapshots t=45,90). Persistance = ≥1 paire liée au snapshot (niveau
  population — identité de paire non suivie, déclaré).
- **Mécanisme testé** : coupure de l'amortissement. Justification : E44 v1
  attribue l'évaporation à « tension et amortissement ». E37 (cœur
  incompressible) et E43 (figeage par rotation) = bras ultérieurs déclarés,
  non lancés par ce protocole.
- **Prédictions pré-enregistrées** :
  - P0 (filiation) : le run 440103 reproduit la paire liée à t=12 — sinon
    B3-FAIL **technique** (harnais réparé avant toute statistique) ;
  - P1 : persistance ON > OFF (directionnel) ;
  - P2 : cohérence — snapshots t≤20 identiques ON/OFF par construction ;
  - P3 : observationnel — distribution des Lk persistants.
- **Règle de verdict gelée** : SUCCÈS si P0 et P1 ; PARTIEL si P0 et moins
  de 3 runs branchés (puissance insuffisante, mesurée et publiée) ;
  B3-FAIL si P0 et absence de différence ON/OFF.
- **Falsifieur global** : aucune différence de persistance ON/OFF → le
  mécanisme est réfuté, publié au même niveau, critère non déplacé.

## Lecture machine-réel (carnet → à déclarer dans la note de verdict)

E45 est la version dynamique de la question de l'interface : la naissance de
l'invariant (Lk ∈ ℤ) est un événement continu (reconnexion) ; sa conservation
exige que la dynamique respecte la structure discrète. La coupure de
l'amortissement teste exactement cela : sans dissipation, la tension seule
suffit-elle à détruire le lien ? Réponse mesurée, pas conjecturée.

## Artefacts (staging local)

- `e45_protocole.json` — gelé, haché `c05f8724…3250d3`
- `src/e45_run.py` — `11bc7369…1e2b4b92`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Incident de harnais — 09/09/2026 (B3-FAIL technique, réparé avant statistique)

Premier lancement : les 24 runs de nucléation et les branches ont été calculés,
mais l'agrégation a planté (`KeyError` : clés de snapshots flottantes lues comme
chaînes) et le verdict n'a pas été écrit — données perdues. Réparation :
clés flottantes + **écriture incrémentale par run** (plus aucune perte possible).
Protocole E45-CAPTURE-1.0 **inchangé** (paramètres, prédictions, règle de
verdict) ; seul le harnais est corrigé, comme prévu par la règle
B3-FAIL-technique du protocole. Harnais réparé : `7f3194ef…f7dfed98`.

## Verdict — 09/09/2026 (exécution locale, harnais réparé)

**B3-FAIL** au sens de la règle gelée — la capture par coupure de
l'amortissement est **réfutée**.

- P0 (filiation) : **PASS** — le run 440103 reproduit sa paire liée à t=12 ;
  harnais validé. Bonus de reproductibilité : les comptes de boucles du
  relancement sont à l'identique du premier lancement (harnais déterministe).
- Nucléation : **5/24 runs** (440102 t=16 ; 440103 t=12 ; 440109 t=8 ;
  440110 t=12 ; 440117 t=8) — taux ≈ 21 %, cohérent avec le 1/6 d'E44.
- Persistance à t=45/90 : **0/5 en OFF, 0/5 en ON** — P1 réfutée.

Lecture physique (déclarée) : l'évaporation se produit **aussi sans
amortissement** (γ=0) — la tension seule suffit à détruire le lien. La
conservation n'est donc pas un problème de dissipation mais de dynamique
intrinsèque : les bras structuraux déclarés (E37 cœur incompressible, E43
figeage par rotation) deviennent les candidats, et toute campagne suivante
devra geler un mécanisme qui change la *cinématique* de la reconnexion, pas
seulement la dissipation.

Incident de harnais (B3-FAIL technique du premier lancement) documenté
ci-dessus ; protocole inchangé ; campagne réparée-relancée mesurée ici.
