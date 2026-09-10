# Campagne E51 — pinning apparié (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation du lien par ancrage spatial apparié »
- **Question unique** : un réseau de puits apparié aux cœurs du lien imprimé
  conserve-t-il le lien sous trempe amortie — là où sans puits il s'évapore ?
- **Classe de mécanisme** : ancrage spatial (E37) — seule classe non testée
  du corridor ; précédent physique : flux pinning des supraconducteurs
  de type II.
- **Conventions citées** : E44 v1/v2 ; détecteur `e44_core.py` byte-identique
  (`604c2232…60ae1ac7`) ; construction d'E50 reprise ; suivi d'E48→E50
  inchangé.
- **Protocole** : `e51_protocole.json` (E51-PINNING-1.0, haché
  `c35c3138…ede5143`) ; harnais `src/e51_run.py` (`266177a8…1576c6c4a8`,
  validé en --smoke hors campagne : lien lu Lk=0,963 ; puits 16+13).
- **Design gelé** : campagne déterministe (existence) ; relaxation sans
  puits (entrée identique à E50) ; trois bras depuis t=5 : A (témoin sans
  puits), B (puits appariés : 16+13 puits gaussiens U0=2, σ=1,5 le long des
  cœurs, ~4 mailles d'espacement), C (puits décalés d'un demi-pas angulaire
  — témoin de non-appariement).
- **Prédictions pré-enregistrées** : P0 (|Lk| ∈ [0,9 ; 1,1] à t=5) ;
  P0b (A : 0) ; P1 (B conserve, lisiblement) ; P2 (C ne conserve pas —
  l'appariement est nécessaire).
- **Règle de verdict gelée** : SUCCÈS si P0+P0b+P1+P2, bras lisibles —
  première conservation mesurée du corridor ; PARTIEL si C conserve aussi
  (ancrage réel mais non spécifique) ; B3-FAIL si lisible et P1 faux ;
  ANOMALIE si un bras illisible ; B3-FAIL-TECHNIQUE si P0 échoue.
- **Falsifieur global** : aucune conservation lisible en B → réfuté, publié
  au même niveau.

## Artefacts (staging local)

- `e51_protocole.json` — gelé, haché `c35c3138…ede5143`
- `src/e51_run.py` — `266177a8…1576c6c4a8`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : B3-FAIL propre

**P0 PASS (Lk=0,976 à l'entrée, lisible) ; P0b PASS (A : évaporé) ;
P1 FAUX ; P2 PASS (C ne conserve pas) ; tous bras lisibles → B3-FAIL.**

Le pinning apparié ne conserve pas le lien — et la mesure est plus forte
que la prédiction : dans les TROIS bras, les anneaux ont entièrement
disparu dès t=45 (0 boucle). Lecture mécaniste (déclarée) : un anneau de
vortex rétrécit sous sa tension de ligne ; des puits posés sur le cercle
initial du cœur n'empêchent pas la contraction radiale — l'anneau quitte
les puits en se contractant. Le pinning de position fonctionne pour des
lignes droites (réseau d'Abrikosov), pas pour des boucles contractiles.
C'est la réfutation la plus lisible du corridor (anom=0, amb=0 partout).

Suite régulée (déclarée) : la classe E37 n'est close que pour les puits
ponctuels. Le candidat restant dans la classe : des GUIDES étendus
(canal torique de rayon fixe — le précédent physique est le courant
persistant en canal torique) qui interdisent la contraction elle-même.
