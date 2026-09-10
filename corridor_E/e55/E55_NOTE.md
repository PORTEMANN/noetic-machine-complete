# Campagne E55 — naissance protégée (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 (`fe5c4846…fb26dd8`) —
aucune donnée de campagne n'existe. Staging local.**

- **Objet** : « trempe confinée dans deux canaux toriques enlacés » —
  changement d'ère désigné par le corridor : faire naître DANS la
  structure protectrice ;
- **Question unique** : le confinement produit-il un lien de tubes — et
  persiste-t-il ?
- **Filiation** : détecteur E44 byte-identique ; géométrie des canaux
  d'E53 identique ; 6 graines déclarées 555001–555006 ; bras A (boîte
  libre, témoin) / B (canaux dès t=0) ; attribution d'une boucle à un tube
  (médiane < 3 mailles, figé) ; lien de tubes = paire inter-tubes liée ;
- **Prédictions** : P0 (A : aucun lien de tubes) ; P1 (B : ≥1 lien nucléé
  à t≤20) ; P2 (le lien né protégé persiste à t=45/90) ;
- **Verdicts** : SUCCÈS (P0+P1+P2 lisible : le corridor se referme par une
  construction) ; PARTIEL_NUCLÉE_SEUL ; B3-FAIL (le confinement n'écrit
  pas le lien) ; B3-FAIL-TECHNIQUE.
- Harnais : `src/e55_run.py` (`f4696768…8ffc03f1`), validé en --smoke.

## Verdict — 09/09/2026 (exécution locale) : B3-FAIL

**P0 PASS (témoin A : aucun lien de tubes, cohérent) ; P1 FAUX — la règle
gelée prononce B3-FAIL : le confinement n'écrit pas le lien.**

Mesure fine : la trempe confinée produit des boucles (jusqu'à 38 à t=8,
davantage qu'en boîte libre à grains comparables — le confinement modifie
la nucléation quantitativement, observationnel) mais elles sont petites et
internes à la section des tubes (attribution : aucune boucle ne suit le
cercle d'un tube, médiane > 3 mailles) ; une seule paire liée intra-tube
(555001, t=12), aucune paire inter-tubes jamais. Lisibilité : 27/30
snapshots lisibles.

Lecture (déclarée) : confiner la phase aléatoire dans un tube produit des
boucles locales, pas des anneaux de tube — la géométrie du canal n'imprime
pas sa topologie au champ. La voie « changer l'ère » est réfutée dans
cette implémentation.

## État du corridor (daté 09/09/2026)

Conservation a posteriori : close (E45–E53). Naissance protégée par
confinement : réfutée (E55). Tressage de lignes : non testé, harnais en
réparation (E54, B3-FAIL-technique, amendement déclaré). La loi de T5
(non-contractilité) reste sans test interne.
