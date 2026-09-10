# Campagne E50 — conservation pure (lien imprimé) (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation pure d'un lien de Hopf né protégé »
- **Question unique** : un lien imprimé, relaxé puis gelé immédiatement
  (gel de Kelvin) survit-il jusqu'à t=90 — lisiblement ?
- **Contexte** : le corridor E44–E49 a clos la conservation a posteriori
  (le lien meurt en < 5 unités, par reconnexion, avant toute intervention).
  E40 rappelle que le triplet est stable une fois formé. E50 isole la
  conservation pure de la question de la naissance : si le gel conserve un
  lien né protégé, la frontière se réduit à la naissance protégée ; sinon,
  la conservation par gel est close.
- **Construction gelée** : anneau 1 (plan xy, centre (31,5;31,5;31,5),
  R=10) ; anneau 2 (plan xz, centre (41,5;31,5;31,5), r=8) — centre de 2
  sur 1, r < R → enlacement exactement 1, distance inter-cœurs constante
  8 mailles ; ψ = tanh(d1/δ)·tanh(d2/δ)·exp(i(φ1+φ2)), δ=1,5 ; relaxation
  100 pas à γ=0,3 (filiation E44-T0 : Lk=+0,994).
- **Nature déclarée** : campagne **déterministe** (condition initiale figée,
  pas de graine) — test d'existence, pas de statistique.
- **Conventions citées** : E44 v1/v2 ; détecteur `e44_core.py`
  byte-identique (`604c2232…60ae1ac7`) ; suivi d'E48/E49 inchangé.
- **Protocole** : `e50_protocole.json` (E50-IMPRIME-1.0, haché
  `bc716376…6579ab`) ; harnais `src/e50_run.py`
  (`af242328…dbd8d2`, validé en --smoke hors campagne
  le 09/09/2026 : paire lue Lk=0,963, anom=0, amb=0).
- **Prédictions pré-enregistrées** : P0 (|Lk| ∈ [0,9 ; 1,1] à t=5) ;
  P0b (témoin A : 0 persistance) ; P1 (B conserve la paire à t=45 ET t=90) ;
  P2 (B lisible partout — l'état initial est propre, sans enchevêtrement) ;
  P3 observationnel (rayons effectifs, rétrécissement sous tension).
- **Règle de verdict gelée** : SUCCÈS si P0+P0b+P1+P2 ; B3-FAIL si lisible
  et P1 faux (la conservation par gel est close ; frontière → E37 pinning
  ou mécanisme actif) ; ANOMALIE si B illisible ; B3-FAIL-TECHNIQUE si P0
  échoue.
- **Falsifieur global** : paire non conservée en B malgré lisibilité →
  réfuté, publié au même niveau.

## Artefacts (staging local)

- `e50_protocole.json` — gelé, haché `bc716376…6579ab`
- `src/e50_run.py` — `af242328…dbd8d2`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : ANOMALIE + mesure systématique

**P0 PASS (Lk=0,975 à l'entrée, lisible) ; P0b PASS (témoin A : évaporé,
0 boucle à t=45/90) ; P1 FAUX ; P2 FAUX (B illisible) → la règle gelée
prononce ANOMALIE. Mais E50 apporte la mesure qui manquait au corridor.**

### Mesures

- Entrée du gel (t=5) : paire imprimée relaxée lue à **Lk = 0,975**,
  parfaitement lisible (anom=0, amb=0) — la construction et la filiation
  T0 sont validées ;
- Bras A (témoin) : évaporation complète sous trempe amortie (0 boucle dès
  t=45) — conforme à toute la série ;
- Bras B (gel immédiat sur état propre) : les boucles suivies restent **en
  place** (1,3–1,8 maille, stables t=45→90) mais Lk_suivi = 0, et surtout :
  **400 boucles, amb 5 768 → 8 000** — partant d'un état à 4 boucles.

### La mesure systématique (déclarée)

Le gel n'est pas un congélateur passif : **il regénère l'enchevêtrement,
même depuis un état propre**. Le mur +C sous dynamique conservative crée
un potentiel chimique ~24 dans les zones appauvries → rotation de phase
rapide et différentielle aux défauts → gradients violents → nucléation de
nouveaux vortex. E49 l'avait montré après nettoyage (re-saturation à
t=45) ; E50 le montre depuis un état initial à 4 boucles. La classe
« mur de densité sous GP conservateur » est ainsi entièrement mesurée :
pression au cœur (E47-B conserve les positions) MAIS génération de
turbulence de phase (E49, E50) — illisible et non conservative pour le
lien.

### Statut régulé

Verdict : **ANOMALIE** (règle gelée) ; la conservation par gel de Kelvin
est close *dans cette implémentation* (mur de densité + GP). Il reste dans
la famille déclarée : le pinning spatial (E37 — mécanisme physique, hors
mur de densité) et, hors GP, les clamps actifs (projection d'amplitude
sans rotation de phase — à déclarer comme dynamique modifiée si un jour
gelée). Le corridor de conservation est clos avec sa carte complète :
naître protégé ou ne pas naître durable — et même « né protégé », le gel
de densité ne suffit pas.
