# Campagne E49 — nettoyage puis gel (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation lisible de la paire nucléée par calendrier à
  trois temps : nucléation libre → nettoyage → gel »
- **Question unique** : après un drain amorti court (5 unités, déclaré) qui
  dilue l'enchevêtrement, le gel de Kelvin conserve-t-il LA paire nucléée,
  lisiblement ?
- **Contexte** : E48 (B3-FAIL propre) a mesuré que le gel fige la
  configuration spatiale (boucles suivies en place à 1,0–3,1 mailles,
  stables t=45→90) mais que le lien lu est nul sous saturation du
  détecteur — deux causes déclarées : (i) le lien meurt entre nucléation et
  immobilisation effective ; (ii) lecture corrompue par la densité de
  l'enchevêtrement figé. E49 les distingue.
- **Conventions citées** : E44 v1/v2 ; détecteur `e44_core.py`
  byte-identique (`604c2232…60ae1ac7`) ; harnais E48 (branchement à la
  nucléation, suivi spatial, écriture incrémentale) repris.
- **Protocole** : `e49_protocole.json` (E49-NETTOIE-GELE-1.0, haché
  `e89ce7b6…7ed753`) ; harnais `src/e49_run.py` (`265c21e4…15e231`, validé
  en --smoke hors campagne le 09/09/2026).
- **Design gelé** : bras A (γ=0,3, témoin — reproduit E48-A) ; bras B2 :
  nettoyage γ=0,3 sans mur de t_n à t_n+5 (100 pas, figé), **snapshot de
  suivi à l'entrée du gel (t_n+5)**, puis gel γ=0 + mur +C jusqu'à t=90
  (snapshots t=45, 90).
- **Prédictions pré-enregistrées** : P0 (filiation 440103, Lk ≃ −1,04) ;
  P0b (témoin A à 0) ; P1 (persistance identifiée B2 > A) ; P2 (B2 lisible
  dans tous les runs branchés — le nettoyage rend l'état lisible) ;
  P3 observationnel (lien à l'entrée du gel, distances, Lk).
- **Règle de verdict gelée** : SUCCÈS si P0+P0b+P1+P2 ; **B3-FAIL** si
  lisible et P1 faux ; **B3-FAIL_FENETRE** si le lien est mort à l'entrée
  du gel dans tous les runs (la fenêtre de vie du lien est plus courte que
  tout mécanisme testé — mesuré, publié) ; ANOMALIE si B2 illisible ;
  B3-FAIL-TECHNIQUE si P0/P0b échoue.
- **Falsifieur global** : aucune persistance identifiée lisible en B2
  au-delà du témoin → mécanisme réfuté, publié au même niveau.

## Artefacts (staging local)

- `e49_protocole.json` — gelé, haché `e89ce7b6…7ed753`
- `src/e49_run.py` — `265c21e4…15e231`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : B3-FAIL_FENETRE

**La fenêtre de vie du lien est plus courte que tout mécanisme testé.
Mesuré, lisible, net.**

### Mesures

- P0 : PASS (440103 nuclée à t=12) ; P0b : PASS (témoin A à 0) ;
- **Le snapshot d'entrée du gel (t_n+5) est lisible dans les 5 runs
  (anom=0, amb ≤ 1) — et il tranche** : les boucles suivies y sont encore
  en place pour 3/5 runs (distances 2,0–2,8 mailles) mais **Lk_suivi ≈
  0,003–0,007** — le lien est mort, les boucles vivent ; pour les 2 autres
  runs, une boucle a déjà dérivé (18,4 ; 9,1 mailles) ;
- Donc : entre t_n et t_n+5, les deux boucles se sont **traversées par
  reconnexion sans se détruire** — la topologie du lien est réécrite en
  moins de 5 unités de temps, dans des snapshots parfaitement lisibles.
  Cause (i) d'E48 confirmée, cause (ii) écartée ;
- Bras B2 après gel : l'état re-sature (400 boucles, amb ~10⁴ à t=45/90) —
  observation déclarée : sans dissipation, le champ de fluctuations
  résiduel repeuple l'enchevêtrement de vortex ; le gel ne garde pas la
  propreté acquise au nettoyage.

### Conclusion physique (déclarée)

Le lien de Hopf est un produit évanescent de l'ère des reconnexions :
**né par la reconnexion, tué par la reconnexion, en moins de ~5 unités de
temps** — plus vite que toute intervention possible après détection. La
conservation *a posteriori* de l'enlacement est close par quatre campagnes
convergentes (E45–E49). La frontière se reformule : la capture doit
précéder ou accompagner la naissance — candidats déclarés : nucléation
*sous* environnement non-reconnectant (changer l'ère — tension mesurée :
la nucléation exige l'ère des reconnexions) ou pinning spatial (E37). Le
corridor E44–E49 est clos pour la conservation a posteriori ; chaque
verdict est propre, lisible et publié au même niveau.
