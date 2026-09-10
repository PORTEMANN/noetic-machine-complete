# Campagne E52 — pinning non apparié sous trempe (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « régions de naissance protégée dans un paysage de pinning
  fixe »
- **Question unique** : un paysage de puits fixe (régulier, indépendant des
  configurations à naître) crée-t-il des régions où l'enlacement naît ET
  persiste ?
- **Classe de mécanisme** : ancrage spatial (E37), version non appariée —
  rien n'est ajusté aux configurations ; c'est la forme statistiquement
  propre de « la naissance protégée ».
- **Conventions citées** : E44 v1/v2 ; détecteur `e44_core.py` byte-identique
  (`604c2232…60ae1ac7`) ; trempe d'E44/E45 (mêmes 24 graines) ; branchement
  à la nucléation et suivi d'E48/E49 ; témoin de taux sans puits = E45
  (5/24 — filiation déclarée, pas de recalcul).
- **Protocole** : `e52_protocole.json` (E52-PAYSAGE-1.0, haché
  `991cab4b…b7af9c40`) ; harnais `src/e52_run.py` (`d720f4fc…8e592e63`,
  validé en --smoke hors campagne le 09/09/2026).
- **Design gelé** : puits gaussiens (U0=2, σ=1,5) sur grille cubique ℓ=8,
  origine décalée de 4 mailles, présents dès t=0 (filiation aux runs E44
  volontairement rompue, déclarée) ; 24 graines ; branchement au premier
  snapshot nucléant ; continuation avec les mêmes puits jusqu'à t=90 ;
  split observationnel gelé : paire « proche-puits » si les deux boucles
  ont une distance médiane au puits le plus proche < 4 mailles à t_n.
- **Prédictions pré-enregistrées** : P0 (cohérence du détecteur —
  lisibilité ≥ 90 % en phase 1) ; P1 (persistance proche-puits >
  persistance loin-puits — directionnel) ; P2 observationnel (taux de
  nucléation avec puits vs 5/24) ; P3 observationnel.
- **Règle de verdict gelée** : SUCCÈS si P0 + lisibilité + P1 ; B3-FAIL si
  P1 faux (le pinning non apparié ne protège pas) ; PARTIEL si < 3 paires
  dans une classe du split ; B3-FAIL-TECHNIQUE si P0 échoue.
- **Falsifieur global** : aucune différence proche/loin → le paysage ne
  crée pas de régions protégées ; réfuté, publié au même niveau.

## Artefacts (staging local)

- `e52_protocole.json` — gelé, haché `991cab4b…b7af9c40`
- `src/e52_run.py` — `d720f4fc…8e592e63`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : PARTIEL (puissance insuffisante mesurée)

**Lisibilité : parfaite (toutes suites lisibles). Taux de nucléation avec
puits : 3/24 (témoin E45 sans puits : 5/24) — légère baisse,
observationnelle. Mais 0 paire proche-puits sur 3 nucléations : P1 non
testable (split déséquilibré mesuré : 0 proche / 3 loin) → PARTIEL au
sens de la règle gelée.**

Mesures : les trois nucléations (440112 : Lk=1,34 ; 440119 : Lk=−0,938 ;
440122 : Lk=−1,005 — deux |Lk|≈1 nets) ont toutes lieu à distance ~4,1–4,3
mailles des puits — au milieu des mailles du réseau (la borne figée était
4,0) ; aucune paire ne naît AU puits. Lecture (déclarée) : les puits,
zones favorables en densité, résistent à la déplétion — ils suppriment
localement la nucléation de vortex plutôt qu'ils ne l'ancrent. Aucune
persistance (0/3, toutes loin-puits) — cohérent avec E45–E49.

Suite régulée : le paysage de puits ponctuels ne crée pas de sites de
naissance protégée ; il les écarte. Même direction restante qu'E51 :
structures étendues (canaux), pas puits ponctuels.
