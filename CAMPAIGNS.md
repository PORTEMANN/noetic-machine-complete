# CAMPAIGNS.md — registre des campagnes et régulation post-campagne

Une **campagne** = un cycle de la machine portant **une** question (réponse : oui / non /
indécidable). Ce registre est le journal officiel des campagnes du corpus.

**Règle des trois tiroirs** — un seul par phrase :

| Tiroir | Signature | Exemple |
|---|---|---|
| **Carnet** | « j'explore » | analogies, correspondances ANU/E₈, pistes E1–E7 |
| **Banc** | « je calcule, voici le test » | scripts P0–P48, séries A/M, verdicts JSON |
| **Thèse** | « je prétends que » | énoncés de théorèmes, prédictions physiques |

Ce registre ne signe que le **banc**. Le site et les essais peuvent tout dire ; GitHub ne
signe que le test.

Références vivantes de l'écosystème :
- Registre canonique : https://index.portemann.eu/index.php?page=registre
- Table des tables : https://index.portemann.eu/index.php?page=tables
- Divergences : https://index.portemann.eu/index.php?page=divergences

---

## Modèle de fiche (à remplir AVANT chaque run)

```
### Campagne <ID> — <date>
- **Tiroir** : banc
- **Objet** : <structure candidate nommée — un mot = un objet>
- **Question unique** : <formulée pour une réponse oui / non / indécidable>
- **Conventions citées** : <IDs de CONVENTIONS.md>
- **Protocole** : <script, bornes, fenêtre — écrit AVANT le run>
- **Falsifieur** : <ce qui, s'il est observé, réfute>
- **Prédiction pré-enregistrée** : <valeur attendue, fixée avant le run>
- **Verdict** : <succès / partiel / B3-FAIL — publié au même niveau de titre>
- **Artefacts** : <chemins + empreintes SHA-256 (SHASUMS.txt)>
- **Registre des frontières** : <entrée F-…, statut>
```

---

## Boucle de régulation post-campagne (obligatoire)

Après **chaque** campagne, dans l'ordre :

1. **Parité des titres** — le verdict, succès OU échec, est publié au même niveau de titre
   que les succès précédents (README, notes, profil).
2. **Conventions** — toutes les conventions utilisées sont citées par ID dans
   `CONVENTIONS.md` ; toute convention nouvelle y est gelée et datée **avant** publication
   du verdict.
3. **Un mot = un objet** — relecture de la fiche : aucun terme ne sert à la fois de
   définition, de cible et de conclusion (« 7 », « bande », « machine », « théorème »…).
4. **Frontières** — le registre REG-FR-1.0 est mis à jour : fermée / ouverte / partielle,
   avec coût de fermeture déclaré et falsifieurs exécutables.
5. **Hash** — `SHASUMS.txt` est régénéré ; les artefacts morts (proxys, cibles abandonnées)
   sont marqués comme tels. Le hash atteste l'octet, pas l'axiome.
6. **Pas de critère déplacé** — si un critère change après un échec : clôture datée de
   l'ancienne question ET ouverture datée de la nouvelle. Jamais de déplacement silencieux.
7. **Alignement externe — « verdict → tables »** — les surfaces publiques sont alignées
   sur le verdict, y compris pour un B3-FAIL. Une valeur = une source unique : le
   **registre canonique** (index.portemann.eu) fait foi, tout le reste cite.

### Point 7 détaillé — checklist « verdict → tables »

À cocher après chaque verdict modifiant une valeur canonique :

- [ ] Valeur entrée au registre canonique (`data/registre.csv` de l'index), ou mention
      « inchangée » dans la note de campagne — avec statut ◆ établi / ◇ modèle /
      ◈ conjecture / ✗ réfuté, date de valeur, source, alias historiques conservés
- [ ] Statut épistémique cohérent avec la charte ◆/◇/◈/✗ du site
- [ ] Articles WordPress citant l'ancienne valeur : **addendum daté** en tête
      (corps conservé tel qu'écrit), lien vers le registre
- [ ] Page Divergences de l'index : écart marqué `resolue` (daté, pointant vers le
      registre) — jamais effacé
- [ ] Atlas machine-noetique : titre/compteurs alignés (ou relevé figé explicité)
- [ ] Chronologie : prédiction concernée mise à jour (valeur + date)
- [ ] Techniques : page concernée citant le registre (ex. Z_max dans `anu.php`)
- [ ] SPA (portemann.eu, noeticindustries.com) : compteurs et cartes alignés,
      cache-buster incrémenté
- [ ] `data/tables.csv` de l'index : ligne ajoutée ou contenu rafraîchi (nature de lien :
      calculé / mesuré / documentaire / analogique)
- [ ] Manifests des vhosts touchés incrémentés (version datée à chaque déploiement) ;
      relevé daté dans les pieds de page si la valeur canonique affichée change
- [ ] Vérification live de chaque propriété touchée (HTTP 200 + chaîne attendue)

---

## Historique (extrait régulé — à compléter à chaque campagne)

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **A3** | 2026-08 | Le compte « 63 160 » est-il reproductible sous la logique publiée ? | **B3-FAIL** — 0 solution ; plafond codé en dur, axiomes proxys, certification vide → artefact | Frontière KO-6 **ouverte** ; erratum déposé sur `spectral-triple-minimality` (branche `gouvernance-corpus`) |
| **A3b** | 2026-08-31 | Un triplet minimal explicite passe-t-il les vrais axiomes (table C-KO6-A3b) ? | **SUCCÈS 4/4** — champion C4 (H_F = ℂ⁴) | Coquille F4 publiée ; étalon 4×4 vers `AXIOMES.md` |
| **F4** | 2026-08 | Combien de matrices sous vrais axiomes, k=2, dim=5 ? | **SUCCÈS 3/3** — 60/256 | ⚠️ Vigilance : le test d'existence ne dépend pas de m au-delà des filtres symétrie/bloc-vide — à documenter dans le verdict |
| **M1/M1b** | 2026-08 | Le postulat « discret bon marché » prédit-il un surplus d'information à r₁₂ ? | **RÉFUTÉ avec inversion** (Spearman 0,980) | Le slogan ne doit plus servir d'enseigne sans sa mesure (τ : 0,60 vs 1,00) |
| **P42** | 2026-08 | \|2I\| = racines⁺(E₈) = 120 et quiver de McKay ? | **SUCCÈS** (arithmétique) | Pont documentaire ≠ dérivation : l'identification physique du « 12 » reste hypothèse déclarée (F14 partielle) |
| **P44–P45** | 2026-08 | Les règles ReN zéro paramètre tiennent-elles sur EEG réel ? | **B3-FAIL** (règles réfutées) | Critère non déplacé : F17/F18 ouvertes et datées ; poursuite « sans ReN » explicitée |

---

## Corridor de falsification (fiches pré-enregistrées, non lancées — daté 07/09/2026)

Sept tests pré-enregistrés, chacun avec son falsifieur ; aucun n'est lancé à la date de
dépôt. Chaque lancement futur devient une campagne au sens du présent registre.

| Fiche | Test | Prédiction pré-enregistrée | Falsifieur |
|---|---|---|---|
| COR-BELL | Bell noétique, d = 1 m | S = 3,23 ± 0,05 (au-delà de 2√2) | S < 2,83 |
| COR-RMN | résonance ANU k = 3 | ΔB = 0,5 mT | pas de pic à B_res |
| COR-PATCH | patch-clamp sous champ focalisé | ΔV_m = −5 mV | \|ΔV_m\| < 1 mV |
| COR-FEXP | loi harmonique δ^n hors calibrage | F_exp ∈ [0,97 ; 1,03] sur particules non calibrées | hors corridor |
| COR-FISSION | pics secondaires de fission | A = 63, 110, 126, 173 | spectre lisse |
| COR-RNU | neutrinos, cible cristalline vs amorphe | R_ν ∝ e^(−β₄ΔS₄) | pas de contraste |
| COR-HZ | H(z) filtré par F₄ sans ajuster Ω_Λ | variation > 3–5 % sur H(z) | ajustement nécessaire |

Ces fiches sont pré-enregistrées lors du câblage du 07/09/2026 (entrée noetic-mdu) ;
leur lancement relève d'une décision d'auteur datée.

---

### Verdicts locaux et réparations du corridor (07/09/2026)

Calculs locaux (arithmétique interne des fiches) — aucune campagne physique lancée :

- **COR-RMN** — *réparée* : la forme publiée (c_éth = 10⁹c) donne ΔB ≈ 4×10³² T (hors cible
  ~10³⁵). Réparation par la fréquence phare du corpus (ω_res = 7,83 Hz) : **B_res = m_e c·ω/ge
  ≈ 42 mT** — mesurable au laboratoire ordinaire. Variante déclarée : la cible 0,5 mT
  correspond à ω = 0,093 Hz. La forme choisie sera datée.
- **COR-BELL** — *clôture proposée* : le « +0,4 » n'a pas de source dans les paramètres
  publiés (calculé : ΔS ≈ 4×10⁻³⁹). Réparer exigerait à la fois le signe de l'exposant et
  l'échelle (ξ_eff ≈ 1,1 cm vs 10⁸ m) — critère déplacé : point 6 de la boucle → clôture
  datée + nouvelle fiche si une forme réparée est posée. Jamais de déplacement silencieux.
- **COR-FEXP** — *migrée* : δ^n à référence unique : 0/10 au corridor (bases implicites par
  ligne : 1,0 à 77 954 MeV — circularité mesurée). La forme est close, datée. La fiche vit
  migrée vers les ratios à constantes déclarées (m_Z = 137,036·m_p/√2 : 0,3 % ; m_μ :
  0,6 % ; m_t : 0,8 % ; m_u : 1,2 % — recalculés le 07/09) : **COR-FEXP v2** : ces ratios sur
  quantités hors construction ; falsifieur : écart > 3 % systématique hors calibrage.
- **COR-FISSION** — *close* : réfutée sur JEFF-3.1.1 (verdict existant, koilon-scale-e8) ;
  renvoi daté.

---

## Prochaine campagne candidate (tiroir banc)

**Q-KO6-2026-09** — *exécutée* : campagne T1 (09/09/2026, réponse OUI dès n=3 — voir la
série T1–T2–T4 en fin de registre).
Prochaine candidate : **E45 — capture de l'enlacement nucléé** (reformulation de frontière
d'E44 : la nucléation est observée, la conservation est le maillon manquant ; mécanismes
candidats E37/E43). Protocole à geler avant tout run.

---

*Registre ouvert le 2026-09-06, en réponse à la note de lecture « Incohérences internes du
corpus Portemann » (sept. 2026). Addenda seulement. Point 7 détaillé ajouté le 07/09/2026
lors du câblage de l'écosystème — il formalise la propagation appliquée pour Z_max = 180,
« 63 160 » réfuté, 11 dépôts publics et le corpus P0–P48.*

---

## Campagnes P49–P51 — données réelles (déposé et exécuté le 08/09/2026)

Note de traçabilité préalable. Le package initial P49–P51 (dépôt du 08/09/2026) contenait
des verdicts de démonstration sur données **synthétiques** non reproductibles par les scripts
livrés (P50 : aucun calcul de verdict dans le script, TODO ligne 78 ; P51 : champs
`accuracy_globale`, `accuracy_avec_ReN_brut`, `levier_discriminant` non produits ; P49 :
falsifieurs F1/F2 non produits), un fichier `CAMPAIGNS_P49_P50_P51.md` annoncé mais absent,
et un `SHASUMS.txt` auto-référent (ligne de sa propre empreinte, invalide par construction).
Le fichier `CAMPAIGNS_P49_P50_P51.md` n'ayant jamais été reçu, les critères repris ci-dessous
sont ceux **codés dans les scripts gelés** (seuils de verdict), cités comme tels. Les
correctifs v1.1 sont documentés par campagne ; aucune règle de prédiction gelée n'a été
modifiée (P49), et les corrections de P51 (features dégénérées) sont listées ci-dessous —
elles dégradent le score par rapport à la démo synthétique, ce qui confirme que le critère
n'a pas été déplacé pour sauver le résultat.

### Campagne P49 — 08/09/2026
- **Tiroir** : banc
- **Objet** : structure candidate « règle sqf des îlots super-lourds » (A ∈ 18k + M_sqf,
  k ≤ 9 ; parité N ≡ sqf(Z) mod 2 ; Z ≤ 180 ; M_sqf = {n < 200 : sqf(n) impair ≤ 7})
- **Question unique** : la règle sqf reproduit-elle la stabilité (T1/2 > 1 s) des états
  fondamentaux Z ≥ 104 de NUBASE2020 avec un score ≥ 80 % ?
- **Conventions citées** : seuils de verdict du script gelé (succès ≥ 0,80 ; partiel ≥ 0,60 ;
  sinon B3-FAIL) ; seuil de stabilité gelé T1/2 > 1 s
- **Protocole** : `src/p49_sqf_islands.py` v1.1 (règle gelée inchangée ; ajout des
  falsifieurs F1/F2 et de la matrice de confusion, absents de la v1.0) ;
  données `data/p49_data_nubase2020_z104.csv` (188 états fondamentaux Z ≥ 104,
  NUBASE2020 — Kondev et al., Chin. Phys. C45, 030001 (2021) ; 84 noyaux à T1/2 > 1 s)
- **Falsifieur** : F1 — un noyau prédit stable avec T1/2 < 1 ms ; F2 — un noyau hors zone
  prédite stable avec T1/2 > 1 s ; effondrement du levier (sans coupure k ≤ 9 : plus du
  double de stables prédits)
- **Prédiction pré-enregistrée** : succès (score ≥ 0,80) — seuil du script gelé du
  08/09/2026, faute de fiche externe reçue
- **Verdict** : **B3-FAIL** — score 107/188 = 0,569. Matrice de confusion :
  TP = 29, FP = 26, FN = 55, TN = 78 (sensibilité 29/84 = 34,5 % ; spécificité 78/104 =
  75,0 %). F1 violé 4 fois, F2 violé 55 fois. Levier discriminant : pas d'effondrement
  (55 stables prédits avec coupure k ≤ 9 ; 89 sans coupure ; ratio 1,62 < 2)
- **Artefacts** : `src/p49_sqf_islands.py` (49fcdc63…ee3906),
  `data/p49_data_nubase2020_z104.csv` (e9e8e870…ab6d1e),
  `data/p49_verdict.json` (34d55606…22ae27) — empreintes complètes dans
  `data/p49_p51_shasums.txt` (calculées sur les octets du dépôt)
- **Suites régulées** : la règle sqf ne doit plus être citée comme prédiction des îlots
  super-lourds sans réparation datée ; la spécificité correcte (75 %) mais la sensibilité
  faible (34,5 %) localisent la réparation éventuelle du côté de la condition
  « A ∈ 18k + M_sqf » (80 rejets) et de la parité (53 rejets), non de la coupure k ≤ 9.

### Campagne P50 — 08/09/2026 — REPORTÉE
- **Tiroir** : banc
- **Objet** : structure candidate « quantification de Hall entière par invariants ASH »
- **Question unique** : les invariants ASH (Rc, Rtop, Rdyn) extraits des courbes V_Hall(B)
  repèrent-ils les plateaux entiers ν = 1, 2, 3, 4, 6 et échouent-ils sur ν = 1/3
  (B3-FAIL attendu sur les fractions) ?
- **Statut** : **reportée, non lancée** — les données réelles (Klitzing 1980 ; datasets
  publics GaAs/AlGaAs) ne sont pas disponibles sous forme exploitable à la date du dépôt.
  Le script `src/p50_hall_ash.py` v1.0 est déposé **non exécuté** ; il contient un TODO
  (ligne 78 : corrélation avec ν mesurée) et ne produit pas de verdict. Le critère de succès
  n'étant gelé nulle part en code, il devra être gelé **avant** tout run réel (point 6 de la
  boucle : pas de critère déplacé). Le « succès 6/15 » du package initial était un résultat
  de démo synthétique non reproductible par le script livré — il ne fait pas foi.
- **Artefacts** : `src/p50_hall_ash.py` (db63ac52…858db6, v1.0 inchangé) — empreinte
  complète dans `data/p49_p51_shasums.txt`

### Campagne P51 — 08/09/2026
- **Tiroir** : banc
- **Objet** : structure candidate « séparabilité des régimes de sommeil par invariants ASH »
- **Question unique** : les invariants ASH (Rtop, Rdyn ; grille harmonique f0 = 0,5 Hz,
  5 octaves) séparent-ils au moins 7/10 paires de stades de sommeil (Wake, N1, N2, N3, REM)
  avec une accuracy > 70 %, sur Sleep-EDFx, EEG Fpz-Cz, segments de 30 s ?
- **Conventions citées** : seuils de verdict du script gelé (succès ≥ 7/10 ; partiel ≥ 4/10 ;
  sinon B3-FAIL) ; classifieur centroïde euclidien, split 70/30 par classe
- **Protocole** : `src/p51_prepare_sleep_edf.py` v1.0 (script de préparation **absent** de
  la v1.0 — ajouté ; 8 nuits sleep-cassette SC4001–SC4112, Sleep-EDFx 1.0.0 PhysioNet ;
  2575 segments équilibrés, 515 par classe, graine 0) puis `src/p51_sleep_ash.py` v1.1
- **Correctifs v1.1 (CHANGELOG)** : B1 — `Rtop_norm` de la v1.0 valait toujours 1,0
  (feature dégénérée) → remplacé par Rtop / N_grille ; B2 — `Rdyn_norm` mélangeait deux
  échelles → Rdyn brut (ratio sans dimension) ; B3 — split ordonné → tirage stratifié
  graine fixe 0 ; B4 — ajout d'`accuracy_globale` et du levier discriminant (annoncés dans
  le JSON de démo mais non calculés). Le champ `accuracy_avec_ReN_brut` du JSON de démo
  n'est reproduit par aucun script livré : retiré du schéma.
- **Falsifieur** : accuracy globale < 0,40 (effondrement du levier)
- **Prédiction pré-enregistrée** : succès (≥ 7/10 paires) — seuil du script gelé du
  08/09/2026, faute de fiche externe reçue
- **Verdict** : **B3-FAIL** — 0/10 paires séparées à > 70 % ; accuracy globale 0,319 ;
  levier effondré. Meilleure paire : N3/REM à 0,590 ; pires : N1/N2 à 0,087 et Wake/N1 à
  0,148. Les invariants ASH tels que gelés ne séparent pas les stades de sommeil.
- **Artefacts** : `src/p51_sleep_ash.py` (61bb58ea…0cd8b78),
  `src/p51_prepare_sleep_edf.py` (dcc44ea3…323a22),
  `data/p51_verdict.json` (217a61be…296d374) — empreintes complètes dans
  `data/p49_p51_shasums.txt`. Le NPZ (62 Mo) n'est pas déposé ;
  régénération : `python3 src/p51_prepare_sleep_edf.py <dossier_edf> data/sleep_edf_segments.npz`
  sur les fichiers Sleep-EDFx 1.0.0 (PhysioNet, accès public).
- **Suites régulées** : cohérent avec P44–P45 (B3-FAIL EEG) — la famille « invariants
  spectraux sans apprentissage » cumule trois échecs mesurés sur EEG réel ; toute nouvelle
  campagne EEG devra déclarer une réparation datée avant lancement.

### Historique — lignes ajoutées le 08/09/2026

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **P49** | 2026-09-08 | La règle sqf prédit-elle les îlots super-lourds (NUBASE2020, Z ≥ 104) à ≥ 80 % ? | **B3-FAIL** — 107/188 = 0,569 ; sensibilité 34,5 % | Règle sqf réfutée comme prédicteur des îlots ; réparation à dater avant toute réutilisation |
| **P50** | 2026-09-08 | Hall entier par ASH | **REPORTÉE** — données réelles indisponibles ; critère à geler avant run | Script v1.0 déposé non exécuté ; le « succès » synthétique initial ne fait pas foi |
| **P51** | 2026-09-08 | ASH sépare-t-il ≥ 7/10 paires de stades de sommeil (Sleep-EDF) à > 70 % ? | **B3-FAIL** — 0/10 paires ; accuracy 0,319 ; levier effondré | Troisième échec EEG mesuré (après P44–P45) ; réparation datée exigée avant nouvelle campagne EEG |

### Hash — boucle point 5 (08/09/2026)

Les empreintes des artefacts P49–P51 sont déposées dans `data/p49_p51_shasums.txt`
(fichier non auto-empreinté, calculées sur les octets du dépôt — GitHub = source de
vérité). La régénération du `SHASUMS.txt` racine reste à faire avec l'outillage local
du dépôt (le présent dépôt a été poussé via API, sans clone local).

---

## Campagne I3 — 08/09/2026 (publiée après pause de tri)

### Campagne I3 — 08/09/2026
- **Tiroir** : banc
- **Objet** : « CI de reproductibilité » du corpus
- **Question unique** : les verdicts publiés dotés de données se ré-exécutent-ils à
  l'identique, et les artefacts du dépôt passent-ils le contrôle SHA-256 ?
- **Conventions citées** : boucle point 5 (hash) ; « GitHub = source de vérité »
- **Protocole** : `src/ci_verdicts.py` v1.0 (gelé avant run) — contrôle des 7 empreintes
  P49–P51, re-run P49 (NUBASE2020), re-run P40 (legacy AME2020 + JEFF-3.1.1, empreintes
  de données embarquées vérifiées), re-run P51 (NPZ régénéré à l'identique par
  `src/p51_prepare_sleep_edf.py` : 2575 segments, 515/classe)
- **Falsifieur** : un seul écart d'empreinte ou de verdict ré-exécuté
- **Prédiction pré-enregistrée** : REPRODUCTIBLE (le corpus se revendique reproductible ;
  la campagne le mesure)
- **Verdict** : **REPRODUCTIBLE — 5/5 contrôles** : 7/7 empreintes conformes ; P49
  ré-exécuté identique (107/188, B3-FAIL) ; P40 ré-exécuté identique (verdict complet
  conforme, données embarquées conformes) ; P51 ré-exécuté identique (0,319, B3-FAIL)
- **Artefacts** : `src/ci_verdicts.py` (451d3bad…a36a7c),
  `data/i3_ci_verdicts.json` (685a4e1c…16f92) — empreintes complètes dans
  `data/p49_p51_shasums.txt`
- **Suites régulées** : la CI devient le contrôle d'entrée de toute future publication ;
  elle aurait détecté les ruptures de traçabilité du package initial P49–P51.

### Staging local — campagnes non publiées (décision d'auteur, pause de tri du 08/09/2026)

Deux campagnes exécutées en local le 08/09/2026 restent **hors dépôt** par décision de
triage (elles sont citées ici pour la régulation des frontières, artefacts conservés en
local). T1, T2 et T4, exécutées en local le 09/09/2026, sont **publiées** — voir la
série en fin de registre. Les deux campagnes non publiées :

- **T3 — modèle nul de P49** (10 000 permutations des labels, graine 0) : la règle sqf ne
  bat pas le hasard à taux de prédictions positives égal — p = 0,099 ; spécificité 0,75
  dans la distribution nulle (p95 = 0,760). Verdict local : B3-FAIL.
- **I1 — ASH vs baseline Welch-PSD** (même NPZ, même split, même classifieur que P51) :
  baseline 0,627 (2/10 paires) contre ASH 0,319 (0/10). Verdict local : B3-FAIL pour ASH.
  La colonne ASH d'I1 reproduit P51 au centième — contre-preuve de ré-exécutabilité.

### Frontière « règle sqf des îlots super-lourds » — fermeture datée (08/09/2026)

**Fermée.** Motif : P49 B3-FAIL au seuil gelé (0,569 < 0,80) et absence de signal résiduel
au modèle nul local (p = 0,099). Coût de fermeture : toute réparation (ex-T2) doit être une
nouvelle fiche gelée, avec justification indépendante du run P49 — la frontière ne doit
plus être citée comme piste ouverte. Conséquence sur la file : T1 (Q-KO6-2026-09) devient
la campagne théorie prioritaire.

### Historique — ligne ajoutée le 08/09/2026 (pause de tri)

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **I3** | 2026-09-08 | Le corpus publié se ré-exécute-t-il à l'identique ? | **REPRODUCTIBLE 5/5** | CI = contrôle d'entrée de toute publication future ; T3/I1 en staging local (non publiées) ; frontière sqf **fermée** (datée) |

---

## Série T1–T2–T4 — KO-6 : taille impaire et classification à deux scalaires (publiée le 09/09/2026, après pause de tri)

Note de gouvernance. Les trois campagnes ont été exécutées en local le
09/09/2026 (staging) et sont publiées par décision d'auteur du 09/09/2026,
après la pause de tri et lecture du chantier E44 (même discipline : protocole
haché avant calcul, aveugle préservé). Les champs « gouvernance » des verdicts
JSON conservent l'état d'avant publication (artefacts figés, non réécrits).
T3 (modèle nul de P49) et I1 (baseline Welch) restent en staging local.

### Campagne T1 — 09/09/2026
- **Tiroir** : banc
- **Objet** : « triplet spectral fini de taille impaire sous C-KO6-A3b » (A = ℂ)
- **Question unique** (Q-KO6-2026-09) : sous la table C-KO6-A3b (datée),
  existe-t-il (D, J, γ) de taille n impaire vérifiant l'ordre 1 avec un
  scalaire complexe unique ?
- **Conventions citées** : C-KO6-A3b ; AXIOMES.md (gelé 2026-09-06) ;
  tolérance figée 1e-9
- **Protocole** : `src/t1_ko6_taille_impaire.py` (T1-KO6-IMP-1.0 gelé) —
  n ∈ {1,3,5,7} ; J₀ permutations signées par blocs, J₀²=+1 ; D réel sym.
  hors-chiral {0,±1} ; comptage exact par orbites, recoupement brut n=3 et n=5
- **Falsifieur** : lemme ou énumération exhaustive montrant l'inexistence
- **Prédiction pré-enregistrée** : EXISTENCE dès n=3 ; n=1 exclu
- **Verdict** : **OUI — existence dès n=3** — 64 couples (J₀,D) à n=3 ;
  13 696 à n=5 ; 8 384 512 à n=7 ; n=1 exclu ({D,γ}=0 avec γ=±I force D=0).
  Recoupement brut 6/6 blocs conformes ; exemplaires d'orbites vérifiés
  20/20, 536/536, 12 308/12 308 ; batterie de leviers 4/4 détectée. Lecture
  honnête déclarée : avec A=ℂ l'ordre 1 est vacuous (mesuré sur scalaires
  aléatoires) — la substance de la question était la taille impaire. Exemple
  minimal publié : γ=diag(1,1,−1), J₀=diag(−1,1,1), D₁₃=D₃₁=1.
- **Artefacts** : `src/t1_ko6_taille_impaire.py`,
  `data/t1_ko6_taille_impaire_verdict.json`,
  `docs/t1-note-ko6-taille-impaire.md` — empreintes complètes dans
  `data/t1_t2_t4_shasums.txt` (octets du dépôt)
- **Incident documenté** (dans le verdict) : sous-comptage d'orbites au
  premier run, détecté par le recoupement brut gelé, corrigé avant verdict,
  protocole inchangé.

### Campagne T2 — 09/09/2026
- **Tiroir** : banc
- **Objet** : « triplet de taille impaire à deux scalaires, ordre 1 non
  vacuous » (A = ℂ⊕ℂ)
- **Question unique** : sous C-KO6-A3b, existe-t-il (D, J, γ) de taille n
  impaire avec A = ℂ⊕ℂ et ordre 1 non vacuous — et dans quelle classe
  d'action de J sur les secteurs (préservation / échange / mélange) ?
- **Conventions citées** : C-KO6-A3b ; AXIOMES.md ; vérificateur d'A3b
  (filiation KO6-REAL-1.0) ; méthode des orbites de T1 (filiation déclarée)
- **Protocole** : `src/t2_ko6_ordre1_impair.py` (T2-KO6-O1IMP-1.0 gelé) —
  n ∈ {3,5,7} ; toutes (a,b) ; tous P ; tous J₀ signés involutifs par blocs ;
  D réel hors-chiral {0,±1}, D≠0 ; filtre ordre 1 dérivé et déclaré
  (Q′ = J₀QJ₀ reste diagonale ; condition par orbite (P_x=P_y) ∨
  (P_{σx}=P_{σy}))
- **Falsifieur** : un combo échangeant à n impair (tue le lemme A) ;
  inexistence là où le lemme B prédit l'existence ; mismatch du brut n=3
- **Prédiction pré-enregistrée** : lemme A confirmé (0 échange) ; lemme B
  confirmé (existence dès n=3) ; mélange mesuré sans cible (discipline E1)
- **Verdict** : **OUI en préservation et mélange ; NON en échange** —
  lemme A confirmé (échange ⟹ rangs égaux par chiralité ⟹ n pair : 0 combo
  échangeant sur ~1,6 M à n=3,5,7) ; lemme B confirmé ; morsure de l'ordre 1
  mesurée (n=7 : 6 749 568 orbites libres → 4 416 896 avec ordre 1) ;
  recoupement brut 3/3 classes ; exemplaires 112/112 vérifiés. Cas
  « 2+2+3=7 » (rangs 2/5, n=7) : triplets vérifiés en préservation et en
  mélange, dans les 12 découpages de chiralité.
- **Artefacts** : `src/t2_ko6_ordre1_impair.py`,
  `data/t2_ko6_ordre1_impair_verdict.json`,
  `docs/t2-note-ko6-ordre1-impair.md` — empreintes complètes dans
  `data/t1_t2_t4_shasums.txt`
- **Suites régulées** : le statut de « 2+2+3=7 » devient une décision de
  structure réelle à déclarer — toute structure réelle échangeant les
  scalaires est exclue en taille impaire ; toute fiche invoquant le « 7 »
  doit désormais déclarer sa classe de J.

### Campagne T4 — 09/09/2026
- **Tiroir** : banc (preuve analytique + vérification machine)
- **Objet** : « lemme de mélange et classification d'existence des triplets
  à deux scalaires »
- **Question unique** : la régularité mesurée en T2 (100 % des combos
  mélange avec D≠0 à n=5,7) est-elle un théorème — et quelle est la
  classification complète de l'existence, à n pair comme impair ?
- **Conventions citées** : C-KO6-A3b ; AXIOMES.md ; filiations T1/T2
  (machines reprises avec leurs bornes)
- **Protocole** : preuve analytique (`docs/t4-note-ko6-lemme-melange.md`,
  faits élémentaires F1–F4) + vérification machine
  `src/t4_ko6_lemme_melange.py` (T4-KO6-MEL-1.0 gelé) — V1 : mélange
  exhaustif n ∈ {2,…,9} (signes collapsés, déclaré : la preuve n'utilise que
  des orbites de longueur 2) ; V2 : classification formule == orbites,
  n ∈ {2,…,7} avec signes ; V3 : échange ⟺ a,b pairs ; V4 : recoupement
  brut n=3 et n=4 au vérificateur complet
- **Falsifieur** : un combo mélange sans D ; un écart formule/orbites ; un
  échange à a ou b impair ; un mismatch brut
- **Prédiction pré-enregistrée** : 0 contre-exemple ; coïncidence parfaite ;
  échange seulement à a,b pairs ; brut conforme
- **Verdict** : **THÉORÈME prouvé et confirmé machine (contrôle global
  4/4)** — T-MÉLANGE (mélange ⟹ existence, pour tout n) : 1 774 080 combos
  à n=2…9, 0 sans D ; T-CLASSIFICATION (existence ⟺ mélange ∨ [secteur
  bi-chiral ∧ paire même-secteur inter-chiralités en orbite de longueur 2
  ou à signes opposés]) : 1 729 136 combos à n=2…7, 0 écart ; échange :
  4/48/624 combos à n=4/6/8, 0 à autre parité ; brut conforme (n=3 :
  64/0/64 ; n=4 : 1760/32/2624 — l'échange porte des D à n pair, comme
  prédit).
- **Artefacts** : `src/t4_ko6_lemme_melange.py`,
  `data/t4_ko6_lemme_melange_verdict.json`,
  `docs/t4-note-ko6-lemme-melange.md` — empreintes complètes dans
  `data/t1_t2_t4_shasums.txt`
- **Suites régulées** : la classification matricielle à deux scalaires est
  close ; voir la mise à jour de la frontière F4 ci-dessous.

### Frontière F4-KO6-ENUMERATION — mise à jour datée (09/09/2026)

La sous-frontière « classification matricielle à deux scalaires » est
**fermée** (théorème T4 : preuve analytique + vérification exhaustive
n ≤ 9, falsifieurs non déclenchés). L'énumération générale sous bornes
d'audit (k ≤ 3, dim ≤ 24, espace de 4 723 712 matrices mesuré en A3b-C3)
reste **ouverte** — coût de fermeture déclaré inchangé. Statut de F4 :
partielle, avec une sous-frontière close datée.

### Historique — lignes ajoutées le 09/09/2026 (pause de tri)

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **T1** | 2026-09-09 | Existe-t-il (D,J,γ) de taille impaire sous C-KO6-A3b avec un scalaire unique ? | **OUI — existence dès n=3** (ordre 1 vacuous pour A=ℂ, déclaré) | Question forte (ordre 1 non vacuous) traitée en T2 — fiche séparée, pas de critère déplacé |
| **T2** | 2026-09-09 | Taille impaire à deux scalaires avec ordre 1 non vacuous ? | **OUI en préservation/mélange ; NON en échange** (lemme A : n pair requis) | « 2+2+3=7 » : statut = décision de structure réelle à déclarer |
| **T4** | 2026-09-09 | La régularité de mélange de T2 est-elle un théorème ? | **THÉORÈME prouvé + machine 4/4** (T-MÉLANGE, T-CLASSIFICATION, n pair et impair) | Sous-frontière F4 « classification à deux scalaires » fermée (datée) ; énumération générale toujours ouverte |

---

## Série E — publication groupée du 09/09/2026 (après pause de tri)

Vingt-quatre campagnes et amendements exécutés en local le 09/09/2026 et
publiés groupés dans `corridor_E/` (registre : `corridor_E/README.md`,
empreintes : `corridor_E/SHASUMS.txt`). La série cartographie la relation
discrète dans le continu : de la nucléation du lien (E44) à la signature
énergétique du 18 (E65).

- **Corridor GP (E44–E59)** : la relation topologique est toujours
  réécrivable — plafond mesuré τ ≤ 15 unités (E59) ; obstruction nommée :
  le cœur déplétable. Neuf mécanismes réfutés proprement, un SUCCÈS
  formel avec note de marge (E56), la fonction de frontière τ(A, γ)
  mesurée (E59).
- **Lois (T5/T6)** : coût scalaire réfuté ; loi à deux étages mesurée —
  objet ⟺ non contractile, relation ⟺ non contractile ∧ ancrage externe.
- **Vide hyperfluide (E60–E65)** : la cavité tenue par les filaments —
  équilibre souffle/pression mesuré (E61), domaine de pression (E64 :
  fenêtre κ ≈ 0,1 avec rms saturé), spectre des cages (E63 : optimum de
  marge n=14), signature énergétique à n = 18 (E65), mortalité mesurée
  (E62).

Discipline identique à la série T : protocoles gelés hachés avant calcul
(champ d'auto-référence exclue déclaré), verdicts publiés au même niveau
succès ou échec, 3 B3-FAIL-TECHNIQUE documentés avec réparations hachées
avant calcul.

### Historique — ligne ajoutée le 09/09/2026 (pause de tri)

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **Série E** (E44–E65 + T5/T6) | 2026-09-09 | La relation discrète peut-elle exister dans le continu, et sous quelles lois ? | **Cartographie complète** : fermeture GP (τ ≤ 15), loi à deux étages, équilibre souffle/pression, fenêtre κ ≈ 0,1, signature n = 18 | Publication groupée `corridor_E/` ; alignement du registre canonique (boucle point 7) à la prochaine pause |

