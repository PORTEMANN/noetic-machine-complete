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

**Q-KO6-2026-09** — *Sous la table C-KO6-A3b (datée), existe-t-il (D, J, γ) de taille n
impaire vérifiant l'ordre 1 avec un scalaire complexe unique ?*
Falsifieur : lemme ou énumération exhaustive montrant l'inexistence. Si oui : publication
des trois matrices, pas du récit. Si non : toute prétention de dimension impaire sort du
tiroir thèse.

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
  `data/p49_data_nubase2020_z104.csv` (1b4c6f5d…04c959),
  `data/p49_verdict.json` (56389d43…943ce4) — empreintes complètes dans
  `data/p49_p51_shasums.txt`
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
  `data/p51_verdict.json` (9ae7a189…1c64) — empreintes complètes dans
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
(fichier non auto-empreinté). La régénération du `SHASUMS.txt` racine reste à faire avec
l'outillage local du dépôt (le présent dépôt a été poussé via API, sans clone local).
