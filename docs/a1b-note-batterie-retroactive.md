# Note A1b — Batterie rétroactive sur le corpus : P13 et P22

**Patrice Portemann — Machine Noétique, série A (méthode)**
30 août 2026 — ferme l'entrée **F7-PARTIELS-PROTOCOLE** du registre A4

## 1. Objet

Le registre des frontières (A4, protocole REG-FR-1.0) portait une entrée
ouverte de type *méthode* : **F7** — « P13 (stabilité) et P22 (double bêta)
sont partiels ; le programme A1 prédit une sensibilité au protocole non
encore mesurée ». Coût de fermeture déclaré : encapsuler P13/P22 en
fonctions pures f(π) et leur passer la batterie A1 (PERT-BATT-1.0, gelé) ;
falsifieur : « l'exécution de la batterie fixe le statut ».

A1b paye ce coût. Les deux chantiers du corpus sont encapsulés **sans
retouche de D** : constantes, tables de noyaux, coefficients
Bethe-Weizsäcker P16 et formules sont repris à l'identique de
`p13_stabilite.py` et `p22_doublebeta.py`. Seuls les choix de protocole π
(seuils de décision, tolérances, bornes) deviennent des axes de
perturbation déclarés **avant exécution**, une coordonnée à la fois
(plan factoriel axial, nominal inclus).

## 2. Axes perturbés

| Chantier | Axes (valeurs perturbées) | Protocoles |
|---|---|---|
| P13 | tol_gn {0.10, 0.20, 0.25} ; seuil_hiérarchie {12, 18} ; cassure_bas {0.8, 1.2} ; cassure_haut {1.8, 2.2} ; tol_regge {0.10, 0.20, 0.25} | 13 |
| P22 | seuil_q2 {0.3, 0.7, 1.0} ; seuil_q1 {0.3, 0.7} ; tol_qok {1.0, 2.0} ; pente_min {5, 7} ; pente_max {14, 18} ; seuil_levier {3, 5} ; n_min_qok {6, 8} | 16 |

## 3. Prédictions pré-enregistrées et résultats

Deux prédictions écrites **avant la première exécution** :

- **P-A1b-1** : P13 est intégralement stable (Σ = 1 sur les 4 composantes).
  → **CONFIRMÉE.** Geiger-Nuttall, hiérarchie (~25 ordres), cassure de
  corde (1,70 fm), pente de Regge (écart relatif 0,018) : toutes les
  marges nominales sont larges devant les tolérances perturbées.
- **P-A1b-2** : P22 garde Σ = 1 sur ses composantes *structurelles*
  (mécanisme d'appariement, signes Qbb 9/9) ; toute fragilité est
  confinée aux composantes *à seuil*.
  → **CONFIRMÉE.** Une seule fragilité, publiée en B3-FAIL de protocole :
  `faux_positifs_localisés_magiques_P16` bascule sous `seuil_q1 = 0.7`
  (Σ = 0,94) — un témoin supplémentaire passe la sélection quand le
  critère de blocage du β simple est relâché.

**C0 (reproductibilité) : PASS** — deux exécutions complètes de la
batterie donnent des couples (V, Σ) identiques sur les deux chantiers
(fonctions pures, aucune graine cachée).

## 4. Couples (V, Σ) publiés

| Chantier | V nominal | Σ_min | Lecture |
|---|---|---|---|
| P13 | 4/4 | 1,00 | le verdict ne dépend d'aucun choix de protocole testé |
| P22 | 5/6 (inchangé) | 0,94 | le partiel P22 n'est pas un artefact de protocole : la magnitude Qbb (composante fausse au nominal) est un échec *documenté* de BW lisse (frontière coquille P29), pas une fragilité de seuil ; la seule fragilité touche la localisation des faux positifs |

## 5. Conséquence sur le registre et la conjecture A5

F7 passe de **ouverte** à **fermée** (ddll : *équilibre* — la fermeture
n'ajoute ni ne retire de degré de liberté physique : les axes existaient,
ils sont désormais déclarés et mesurés). Le registre compte désormais
**5 fermées / 5 ouvertes / 5 partielles** (SHA global
`45dc0619d66f2850…`).

Effet de bord mesuré, non anticipé dans la note A4-A5 : F7 fermée rejoint
les points *équilibre* du domaine — la conjecture v1 « toute frontière =
déficit de ddll » gagne un **troisième réfuteur** (F5, F7, F14 ; 10/13
conformes) et la couverture de v2 passe à 11/13. Fermer une entrée de
méthode a *renforcé* la réfutation de la v1 : le registre ne distingue
pas les frontières physiques des frontières de méthode dans son comptage
— c'est désormais mesuré, pas discuté.

## 6. Artefacts

| Artefact | SHA-256 (tronqué) |
|---|---|
| `a1b_batterie_retroactive.py` | `950ba05c3d90d39a…` |
| `a1b_batterie_retroactive_verdict.json` | chaîne SHASUMS.txt |
| registre A4 mis à jour (15 entrées, 5/5/5) | `45dc0619d66f2850…` |
| verdict A5 régénéré (v1 : 3 réfuteurs ; v2 : 11/13) | `cbc6df7fb52beef3…` (script) |

*Protocole PERT-BATT-1.0 gelé (hérité d'A1) — zéro paramètre ajusté, D
intact, fragilités publiées (C2), falsifieur de F7 exécuté.*
