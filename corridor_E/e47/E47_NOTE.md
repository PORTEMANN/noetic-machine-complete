# Campagne E47 — séparation des composantes du mur (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation de l'enlacement nucléé — gel de Kelvin (pression
  conservative) vs plancher dissipatif (restauration active) »
- **Question unique** : une fois les deux composantes du mur séparées, l'une
  conserve-t-elle l'enlacement nucléé au-delà de l'ère des reconnexions ?
- **Contexte** : E44 (nucléation observée) ; E45 (B3-FAIL : la dissipation
  n'est pas le destructeur) ; E46 (ANOMALIE : succès formel 5/5 vs 0/5 annulé
  par les compteurs gelés du détecteur — le mur +C à γ=0,3 mêle deux
  composantes qui s'affrontent : pression conservative et anti-restauration
  dissipative). E47 les sépare.
- **Conventions citées** : E44 v1/v2 (`42c65a0c…`, `bc977f17…`), détecteur
  `e44_core.py` byte-identique (`604c2232…60ae1ac7`) ; harnais E45/E46
  (écriture incrémentale) ; discipline d'aveugle.
- **Protocole** : `e47_protocole.json` (E47-SEPARATION-1.0, haché
  `96195d9f…689a11cc`) ; harnais `src/e47_run.py` (`0e22d0ae…c5e1ac42`,
  validé en --smoke hors campagne le 09/09/2026).
- **Design gelé — 2×2** sur chaque run branché depuis t=20 :
  - **A** : γ=0,3, sans mur — témoin (doit reproduire E46-OFF : 0) ;
  - **B** : γ=0, mur +C — gel de Kelvin pur (pression conservative) ;
  - **C** : γ=0,3, mur −C — plancher dissipatif (restauration active) ;
  - **D** : γ=0, sans mur — témoin (doit reproduire E45-ON : 0/5).
- **Critère de lisibilité gelé** (issu de l'anomalie E46) : un snapshot ne
  statue que si anom == 0 et amb ≤ 4 (référence : l'événement valide E44
  avait amb=1 ; les snapshots saturés E46-ON avaient amb ≥ 5699).
- **Prédictions pré-enregistrées** : P0 (filiation 440103) ; P0b (témoins A
  et D à 0, sinon harnais suspect) ; P1 (Kelvin : B > A et B > D) ;
  P2 (plancher : C > A) ; P3 observationnel (longueurs, Lk).
- **Règle de verdict gelée** : SUCCÈS si P0, P0b, bras lisibles et (P1 ou
  P2) ; PARTIEL si < 3 runs branchés ; B3-FAIL si lisible et ni P1 ni P2
  (→ frontière : pinning spatial, E37 strict) ; ANOMALIE si un bras illisible
  (réparation datée requise) ; B3-FAIL-TECHNIQUE si P0/P0b échoue.
- **Falsifieur global** : aucune persistance lisible en B ni C au-delà des
  témoins → mécanismes réfutés, publiés au même niveau.

## Artefacts (staging local)

- `e47_protocole.json` — gelé, haché `96195d9f…689a11cc`
- `src/e47_run.py` — `0e22d0ae…c5e1ac42`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale)

**ANOMALIE partielle + B3-FAIL partiel — la séparation a fonctionné, et
chaque bras reçoit un verdict distinct :**

| Bras | Lisibilité | Persistance | Verdict de bras |
|---|---|---|---|
| A (γ=0,3, témoin) | 5/5 | 0/5 | témoin conforme (E46-OFF reproduit) |
| B (γ=0, mur +C, Kelvin) | **0/5** | non mesurable | **ANOMALIE** — non tranché |
| C (γ=0,3, mur −C, plancher dissipatif) | 5/5 | **0/5** | **B3-FAIL propre** — réfuté |
| D (γ=0, témoin) | 5/5 | 0/5 | témoin conforme (E45-ON reproduit) |

- P0 : PASS (440103, paire à t=12) ; P0b : PASS (témoins à 0) ;
- P1 : non satisfaite (B n'a aucune persistance *lisible*) ; P2 : réfutée.

### Lecture physique (déclarée)

- **Bras C (plancher dissipatif)** : dynamique lisible, boucles normales,
  et **aucune conservation** — la restauration active de la densité sous
  damping ne protège pas le lien. Réfutation propre.
- **Bras B (gel de Kelvin)** : le plus intéressant physiquement — sans
  dissipation, le mur fige un **enchevêtrement dense** (400 boucles, au
  plafond du détecteur, à t=45 ET t=90 : la vorticité ne décroît plus).
  Mais cet état est **illisible** par le détecteur gelé (anom 61–101,
  amb 8 370–10 608 par snapshot) : impossible d'y suivre la paire
  d'origine. Le gel de Kelvin produit donc bien un état conservé — la
  question « la paire nucléée y survit-elle *en tant que paire* » excède
  la résolution du détecteur actuel.

### Suites régulées (frontière reformulée, datée)

La conservation de la vorticité par gel conservatif est observée mais
illisible ; la conservation *de l'enlacement identifié* exige un détecteur
renforcé. Candidat E48 (à geler séparément) : bras B avec (i) porte
d'amplitude déclarée (filtrer le bruit de phase des zones rongées),
(ii) suivi des cœurs de la paire nucléée (position à t=12 conservée en
mémoire, coïncidence spatiale mesurée), (iii) éventuellement boîte plus
grande ou mur plus doux (C déclaré) pour diluer l'enchevêtrement. Tant
qu'E48 n'a pas tourné, la capture de l'enlacement reste **ouverte** :
mécanismes réfutés — dissipation (E45), mur mélangé (E46), plancher
dissipatif (E47-C) ; mécanisme non tranché — gel de Kelvin (E47-B,
illisible) ; non testé — pinning spatial (E37).
