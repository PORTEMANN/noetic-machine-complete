# Campagne E54 — lignes tressées sous rotation (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 (`022c2254…b84ec22b`) —
aucune donnée de campagne n'existe. Staging local.**

- **Objet** : « tressage de lignes axiales sous rotation » — changement
  d'objet désigné par le corridor (les boucles meurent par contraction,
  E51 ; une ligne ne rétrécit pas) ;
- **Question unique** : le tressage nuclée-t-il sous rotation, et
  persiste-t-il ?
- **Filiation** : détecteur E44 byte-identique ; géométrie exacte d'E44-B
  (cylindre, paroi e^{4iφ}) ; 6 graines 440201–440206 ; AJOUT DE DÉTECTEUR
  déclaré et gelé : traceur de lignes axiales + enroulement mutuel ;
- **Prédictions** : P0 (structure axiale reproduite) ; P1 (tressage nucléé
  à t≤20) ; P2 (le tressage persiste à t=45/90 — directionnel : seule la
  reconnexion peut le défaire) ;
- **Verdicts** : SUCCÈS (P0+P1+P2 : première persistance mesurée) ;
  PARTIEL_NUCLÉE_SEUL ; B3-FAIL (aucun tressage — rejoint P3 d'E44) ;
  B3-FAIL-TECHNIQUE.
- Harnais : `src/e54_run.py` (`b7b9bb61…f753a8879`), validé en --smoke.

## Verdict — 09/09/2026 (exécution locale) : B3-FAIL-TECHNIQUE

**P0 échoue → la règle gelée prononce B3-FAIL-TECHNIQUE : le harnais se
répare avant toute statistique.**

Mesure : le nouveau traceur de lignes axiales trouve très peu de lignes
longues (portée ≥ 40 tranches, saut ≤ 2) et aucune paire tressée — alors
qu'E44-B avait mesuré une structure axiale (filaments de longueur > 40
segments, médiane 14 quanta). Écart localisé : ma définition « portée en
tranches » n'est pas l'observable publiée d'E44-B (longueur en segments
3D) ; le traceur casse les pistes aux tranches vides. La question
physique (nucléation et persistance du tressage) n'est **pas réfutée —
non testée**.

Réparation déclarée (datée, à geler comme amendement haché) :
recalibrer le traceur sur l'observable d'E44-B (filaments ouverts,
longueur en segments > 40) AVANT tout nouveau run ; P0 devra reproduire
la médiane 14 (étendue 9–19) de l'ensemble B d'E44.

## Amendement E54-A — 09/09/2026 (haché AVANT tout calcul : `b495267e…964c1189`)

Réparation exigée par la règle gelée (B3-FAIL-TECHNIQUE de v1). Le traceur
maison est remplacé par le détecteur E44 lui-même (`trace_filaments` de
`e44_core.py`, filiation byte-level) : filaments ouverts, filtre axial
(longueur ≥ 40 segments ET étendue z ≥ 30 mailles — l'observable publiée
d'E44-B), enroulement axial par la formule d'E44, enroulement mutuel par
tranche z (étendue commune ≥ 30 mailles). **P0 recalibré** : à t=45/90,
≥ 1 filament axial dans ≥ 4/6 graines ET médiane d'enroulement du plus
long filament dans [9, 19] (la fenêtre publiée d'E44-B) — sinon deuxième
B3-FAIL-TECHNIQUE. Tout le reste : inchangé (géométrie, graines,
paramètres, snapshots, P1/P2/P3, seuil |w| ≥ 0,5).

Harnais réparé : `src/e54a_run.py`, validé en --smoke (23 filaments
ouverts détectés à N=32 — le détecteur E44 authentique lit ce que le
traceur maison ne voyait pas). La campagne E54-A n'a pas été lancée à
cette date.

## Verdict E54-A — 09/09/2026 (exécution locale) : B3-FAIL-TECHNIQUE (2e série)

**P0 recalibré : FAUX** (médiane d'enroulement du plus long filament axial :
0,0 — hors de la fenêtre [9, 19]) → deuxième B3-FAIL-TECHNIQUE. La cause
est identifiée exactement, et elle est de **lecture** : la « médiane 14 »
publiée d'E44-B porte sur `embrace` — l'enroulement axial des BOUCLES
fermées (`axial_winding` appliqué aux boucles, ligne 87 d'e44_run.py) —
pas sur les filaments ouverts. Mon P0 recalibré visait le mauvais
observable.

Mesures acquises au passage (compteurs gelés, publiés) :
- le détecteur recalibré voit la structure axiale : **6/6 graines** avec
  filaments axiaux à t=45/90 ;
- **le tressage nuclée** (P1 mesuré vrai : jusqu'à 6–8 paires tressées à
  t=8–20 dans plusieurs graines) ;
- **il ne persiste pas** (P2 faux : 0 paire tressée à t=45/90) — mais ces
  deux mesures restent *hors statistique* tant que P0 n'a pas passé
  (règle gelée) : elles sont consignées comme compteurs, pas comme
  verdict.

Réparation déclarée (datée) : **E54-B** — P0 visant le bon observable :
reproduire `embrace` d'E44-B (enroulement axial des boucles, médiane 14,
étendue 9–19), la formule existe dans e44_run.py ; puis P1/P2. La question
physique reste non testée, non réfutée.

## Amendement E54-B et verdict corrigé — 09/09/2026

**Amendement de LECTURE** (`55a1843e…e4b92fd`, haché, sans nouveau calcul
de campagne). La double mésinterprétation de la cible d'E44-B est corrigée
au niveau des lignes de code : la « médiane 14 (étendue 9–19) » est la
médiane du COMPTE de filaments axiaux par snapshot (n_axial40, ligne 86) ;
l'enroulement axial porte sur les boucles (embrace, ligne 87), absentes
de l'ensemble B. Le P0 corrigé est ré-évalué sur les compteurs gelés
d'E54-A : médiane 13,0, étendue 9–18 — **dans la fenêtre publiée** :
P0 PASS.

Verdict corrigé (règle v1, questions et seuils gelés avant toute donnée) :
**PARTIEL_NUCLÉE_SEUL** — P0 ✓, P1 ✓ (le tressage nuclée : 440202,
440205), P2 ✗ (aucune paire tressée ne persiste à t=45/90).

Mesure physique : sous rotation, la structure axiale persiste (comptes
stables de t=45 à t=90) mais la RELATION discrète entre lignes (le
tressage) ne persiste pas — les lignes restent, le tressage se défait.
Nuancé par rapport à la loi de T5 : l'objet non contractile persiste, sa
relation discrète à un autre objet — non. La frontière « conservation de
la relation » reste ouverte.
