# Campagne E53 — guides toriques (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 — aucune donnée de campagne
n'existe. Staging local ; lancement et publication soumis à décision d'auteur
(pause de tri).**

## Fiche (modèle du registre)

- **Tiroir** : banc
- **Objet** : « conservation du lien par canaux toriques continus »
- **Question unique** : un canal torique continu apparié aux cœurs
  conserve-t-il le lien sous trempe amortie — là où les puits ponctuels
  (E51) et l'absence de structure (E50) échouent ?
- **Contexte** : E51 (B3-FAIL lisible) a mesuré que les puits ponctuels
  n'empêchent pas la contraction radiale de l'anneau (tension de ligne) ;
  E52 (PARTIEL) que les puits écartent la nucléation. La réparation
  désignée par les données : une structure étendue — le canal torique
  (précédent : courants persistants en canal torique), force de rappel
  continue contre la contraction.
- **Conventions citées** : E44 v1/v2 ; détecteur `e44_core.py`
  byte-identique (`604c2232…60ae1ac7`) ; construction d'E50 identique ;
  suivi d'E48→E51 inchangé.
- **Protocole** : `e53_protocole.json` (E53-GUIDES-1.0, haché
  `4e0ab205…660653`) ; harnais `src/e53_run.py`
  (`824d1d5d…0e1ff6`, validé en --smoke hors campagne le
  09/09/2026 : lien lu Lk=0,963, canaux construits).
- **Design gelé** : campagne déterministe (existence) ; trois bras depuis
  t=5 : A (témoin sans guide), B (canaux appariés : V = −U_g·exp(−d²/2σ²)
  sur la distance au cercle de chaque anneau, U_g=2, σ=1,5), C (canaux
  décalés de +3 mailles en rayon — témoin de spécificité).
- **Prédictions pré-enregistrées** : P0 (|Lk| ∈ [0,9 ; 1,1] à t=5) ;
  P0b (A : 0) ; P1 (B conserve, lisiblement — le canal retient l'anneau
  contre sa tension de ligne) ; P2 (C ne conserve pas) ; P3
  observationnel (contraction mesurée par les distances de suivi).
- **Règle de verdict gelée** : SUCCÈS si P0+P0b+P1+P2, bras lisibles ;
  PARTIEL si C conserve aussi ; **B3-FAIL si lisible et P1 faux — la
  classe « ancrage spatial » est close ENTIÈREMENT** (puits ponctuels
  E51/E52, canaux continus E53) et la frontière passe à « changer l'ère »
  ou hors-GP ; ANOMALIE si un bras illisible ; B3-FAIL-TECHNIQUE si P0
  échoue.
- **Note honnête de profondeur** : U_g=2 est filiative (E51) ; si le canal
  est trop peu profond contre la tension de ligne, le verdict le mesurera
  — toute variation de profondeur relève d'un amendement haché ou d'une
  nouvelle fiche, jamais d'un ajustement post-échec.
- **Falsifieur global** : aucune conservation lisible en B → réfuté,
  publié au même niveau.

## Artefacts (staging local)

- `e53_protocole.json` — gelé, haché `4e0ab205…660653`
- `src/e53_run.py` — `824d1d5d…0e1ff6`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : B3-FAIL — la classe « ancrage spatial » est close

**P0 PASS (Lk=0,976, lisible) ; P0b PASS ; P1 FAUX ; P2 PASS ; tous bras
lisibles → B3-FAIL au sens de la règle gelée.**

Dans les trois bras, les anneaux ont disparu dès t=45 (0 boucle, anom=0,
amb=0 — lecture la plus propre du corridor avec E51). Le canal torique
continu n'a pas retenu l'anneau : à U_g=2 (filiative), la force de rappel
du canal n'a pas suffi contre la tension de ligne sous trempe amortie —
comme la note honnête du protocole l'anticipait (la profondeur est un
paramètre mesuré, non ajusté ; toute variation relèverait d'un amendement
haché).

### Statut régulé — la classe est close entièrement (daté 09/09/2026)

« Ancrage spatial » : puits ponctuels appariés (E51), paysage fixe
(E52), canaux toriques continus (E53) — trois implémentations, trois
verdicts lisibles, zéro conservation. Combiné à la fermeture de la
famille « mur de densité » (E46→E50) et de la dissipation (E45) :
**aucune conservation de l'enlacement n'a été trouvée dans la dynamique
de trempe GP, par aucune classe de mécanisme testée**.

### Frontière (datée)

Il ne reste que deux voies déclarées : (i) **changer l'ère** — faire
naître le lien dans un environnement déjà protégé (tension mesurée : la
nucléation connue exige l'ère des reconnexions) ; (ii) **hors-GP** —
dynamique modifiée déclarée (clamps actifs : projection d'amplitude sans
rotation de phase). La question « capture de l'enlacement » est close
pour la conservation ; elle vit désormais comme question de naissance
protégée.
