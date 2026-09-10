# Alignement du registre canonique — boucle point 7 (verdict → tables)
**Relevé proposé au 09/09/2026** — à insérer dans le registre canonique
(index.portemann.eu/index.php?page=registre), au format des entrées
existantes (statut ◆ établi / ◇ modèle / ◈ conjecture / ✗ réfuté —
« valeur du <date> », source, valeurs historiques obsolètes).

---

## 1. Entrées EXISTANTES à mettre à jour

### ◇ T1 — « dimension 7 » de la classe minimale
**Résolu partiellement** : existence dès n=3 sous C-KO6-A3b (établi) ;
exclu sous C-KO6-L1 (établi, lemme de parité)
modèle | | valeur du 2026-09-09
Source : campagne T1 — noetic-machine-complete (64 couples (J₀,D) à n=3,
13 696 à n=5, 8 384 512 à n=7 ; recoupement brut 6/6 ; lemme de parité
inapplicable sous Jγ=+γJ — campagnes T2/T4 pour la classification complète)
Valeurs historiques (obsolètes) : « dimension 7 établie / démontrée »
(portemann.eu, art. 12407, jusqu'au 2026-09-06) ; « exclu sous la table
usuelle KO-6 » (ERRATUM E4, jusqu'au 2026-09-08)
Note : la « question ouverte honnête » d'AXIOMES.md est close (datée).

### ◆ Registre des frontières (A4)
établi | | valeur du 2026-09-09
Source : A4 / REG-FR-1.0 — noetic-machine-complete + CAMPAIGNS.md
Mises à jour datées : frontière « règle sqf des îlots super-lourds »
FERMÉE le 08/09/2026 (P49 B3-FAIL + modèle nul p = 0,099) ; sous-frontière
F4 « classification matricielle à deux scalaires » FERMÉE le 09/09/2026
(théorème T4 — voir entrée série T) ; F4 générale (énumération k ≤ 3,
dim ≤ 24) reste OUVERTE à coût déclaré (4 723 712 matrices).

---

## 2. Nouvelles entrées

### ✗ P49 — règle sqf des îlots super-lourds
score 107/188 = 0,569 < seuil gelé 0,80
réfuté | | valeur du 2026-09-08
Source : campagne P49 — noetic-machine-complete (NUBASE2020, Kondev et
al., Chin. Phys. C45, 030001 (2021) ; sensibilité 34,5 %, spécificité
75,0 % ; falsifieurs F1 ×4, F2 ×55 ; modèle nul par permutations p = 0,099
(staging local T3) — frontière fermée datée 08/09/2026)

### ◇ P50 — quantification de Hall entière par invariants ASH
modèle | | valeur du 2026-09-08
reportée, non lancée — données réelles (Klitzing 1980, datasets GaAs/AlGaAs)
indisponibles sous forme exploitable à la date du dépôt ; script déposé
non exécuté ; critère à geler avant tout run réel (point 6 de la boucle).
Source : noetic-machine-complete

### ✗ P51 — séparabilité des stades de sommeil par invariants ASH
0/10 paires séparées à > 70 %, accuracy globale 0,319
réfuté | | valeur du 2026-09-08
Source : campagne P51 — noetic-machine-complete (Sleep-EDFx 1.0.0
PhysioNet, 2575 segments équilibrés ; levier discriminant effondré ;
baseline Welch-PSD 0,627 la domine au même protocole — campagne I1,
staging local. Quatrième échec EEG mesuré de la famille après P44–P45)

### ◆ I3 — CI de reproductibilité du corpus
REPRODUCTIBLE 5/5
établi | | valeur du 2026-09-08
Source : campagne I3 — noetic-machine-complete (7/7 empreintes conformes,
re-runs P49/P40/P51 identiques ; la CI est le contrôle d'entrée de toute
publication future)

### ◆ Série T1–T4 — classification KO-6 à deux scalaires
théorème prouvé + vérification machine (1 774 080 combos, 0 sans D)
établi | | valeur du 2026-09-09
Source : noetic-machine-complete (campagnes T1–T4 : existence dès n=3 à
un scalaire ; classification à deux scalaires : existence ⟺ mélange ∨
[secteur bi-chiral ∧ condition de signe/cycle] ; lemme A : échange ⟹ n
pair ; sous-frontière F4 « classification à deux scalaires » fermée datée)

### ◆ Corridor E — relations discrètes dans le continu (E44–E68 + T5/T6)
29 campagnes et amendements — cartographie complète
établi | | valeur du 2026-09-09
Source : noetic-machine-complete, corridor_E/ (registre :
corridor_E/README.md, empreintes : corridor_E/SHASUMS.txt)
Contenu : fermeture de la famille GP (relation topologique toujours
réécrivable, plafond τ ≤ 15 — E59) ; loi à deux étages (T6 : objet ⟺
non contractile, relation ⟺ non contractile ∧ ancrage externe) ;
équilibre souffle/pression de la cavité ANU mesuré (E61) ; fenêtre du
couronnement κ ∈ ]0,075 ; 0,125[ (E64-A — parking avant la barrière
énergétique R ≈ 16) ; signature énergétique à n = 18 (E65) ; dents de
scie E/n et ovoïdes 3/12/63 reproduits (E66) ; paysages par n (E67 :
n=18 a le plus grand bassin 16→22) ; fenêtre non universelle par n (E68 :
14 tient sur toute la grille, 18 en un point, 24 nulle part — prédiction
de largeur de bassin réfutée, publiée).

---

## 3. Ajouts à la table des tables (nature de lien)

| Table | Nature | Source | Statut registre |
|---|---|---|---|
| Corridor E (E44–E68) : 29 campagnes, protocoles gelés, verdicts, SHASUMS | calculé (zéro paramètre ajusté) + mesuré (NUBASE2020, Sleep-EDFx, AME2020, JEFF-3.1.1) | github.com/PORTEMANN/noetic-machine-complete/tree/main/corridor_E | ◆ établi — entrée CORRIDOR-E |
| Série T1–T4 (classification KO-6 à deux scalaires) | calculé | github.com/PORTEMANN/noetic-machine-complete | ◆ établi — entrée SERIE-T-KO6 |

## 4. Page Divergences — addendum

Aucune nouvelle divergence introduite par ces relevés (Z_max reste 180 ;
le « 63 160 » reste réfuté). Mise à jour de statut : la question de la
« dimension 7 » de la classe minimale (entrée registre T1) n'est plus une
question ouverte — résolue partiellement le 09/09/2026 (existence dès n=3
sous C-KO6-A3b) — voir Registre, entrée T1-DIMENSION-7.

---

## 5. Protocole de vérification post-insertion (point 7, checklist)

- [ ] Chaque nouvelle entrée porte : statut (◆/◇/◈/✗), « valeur du
      2026-09-08/09 », source unique, alias historiques conservés
- [ ] Statuts épistémiques cohérents avec la charte ◆/◇/◈/✗ du site
- [ ] Page Divergences : entrée T1-DIMENSION-7 marquée `resolue` (datée
      09/09/2026) — jamais effacée
- [ ] tables.csv : deux lignes ajoutées (corridor_E, série T) avec nature
      de lien (calculé / calculé+mesuré)
- [ ] Vérification live : HTTP 200 + chaînes attendues sur
      index.php?page=registre (« P49 », « Série T1–T4 », « Corridor E »),
      index.php?page=tables (« corridor_E »), index.php?page=divergences
      (« dimension 7 » → resolue)

*Alignement préparé le 09/09/2026 — verdicts figés, sources uniques,
empreintes vérifiables dans le dépôt (corridor_E/SHASUMS.txt et
SHASUMS.txt racine).*
