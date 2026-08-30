# P41 — Neurones réels : les interneurones sont-ils type II comme Hodgkin-Huxley ?

**Patrice Portemann — corpus Machine Noétique, chantier P41**
Protocole gelé REEL-1.0 · zéro paramètre ajusté · SHA-256
30 août 2026

## Verdict

**RÉPONSE MESURÉE : NON.** Sur 32 cellules réelles (Allen Cell Types,
current-clamp Long Square), les interneurones (aspiny) ne sont **pas**
type II comme HH : **1/8** interneurones de souris et **0/8**
interneurones humains présentent une fréquence d'onset f₀ ≥ 20 Hz
(seuil gelé hérité de P35) ; les pyramidales (spiny) : **0/8** souris,
**0/8** humain. Le neurone cortical réel est massivement **type I**
(f₀ d'onset 1–10 Hz), alors que le modèle Hodgkin-Huxley est type II
(f₀ = 60 Hz à la rhéobase). HH n'est pas représentatif de l'onset
cortical réel — Izhikevich (RS), lui, l'est.

## Protocole (gelé avant mesure)

- **Sélection sans choix humain** : 4 classes (Mus musculus / Homo
  Sapiens × spiny / aspiny) × 8 cellules, par specimen__id croissant,
  éligibilité = fichier NWB existant (erwkf__id) + seuil Long Square
  mesuré (ef__threshold_i_long_square non nul). 1781 cellules au
  catalogue, 32 sélectionnées.
- **Classification** : type II si et seulement si la fréquence d'onset
  f₀ ≥ **20 Hz** — seuil hérité gelé de P35_NOMINAL (c3_saut_min),
  jamais ré-ajusté sur les données de ce chantier.
- **f₀ table** : premier sweep Long Square (amplitude croissante,
  durée ≥ 0.5 s) avec ≥ 1 spike ; f₀ = n_spikes / durée (table
  EphysSweep de l'API Allen).
- **Contrôles obligatoires avant verdict** : C0 instrument, C2 brut.

## Mesures

- **C0 — contrôle instrument : PASS.** Aux paramètres gelés P35, HH
  donne f₀ = 60 Hz → type II ; Izhikevich (RS) donne f₀ = 8 Hz →
  type I. L'instrument discrimine les deux classes de excitabilité
  avant de toucher au réel.
- **C1 — population (table Allen)** :

  | Classe | type II | f₀ mesurés (Hz) |
  |---|---|---|
  | Souris spiny (pyramidales) | 0/8 | 2, 1, 1, 4, 10, 4, 1, 2 |
  | Souris aspiny (interneurones) | **1/8** | **26**, 1, 1, 1, 9, 2, 1, 1 |
  | Humain spiny | 0/8 | 2, 1, 2, 5, 1, 1, 2, 1 |
  | Humain aspiny (interneurones) | 0/8 | 2, 2, 1, 1, 1, 1, 1, 1 |

  La seule cellule type II de l'échantillon est l'interneurone de
  souris 313861411 (f₀ = 26 Hz) — une minorité (1/16 interneurones),
  pas la règle.
- **C2 — contrôle sur signaux bruts (2 cellules gelées, NWB complets)** :
  le sweep de rhéobase est identifié par la table API gelée
  (sweep_number), puis f₀ est **re-dérivé du signal brut** (croisements
  ascendants à −20 mV dans la fenêtre du pallier de courant) :
  - spiny 313860745 : f₀ brut **1.98 Hz** vs table 2.0 Hz —
    recoupement ±2 Hz ✓ ; ASH-lite à la rhéobase : Rc = 0.518,
    Rtop = 1.0, Rdyn = 0.0 ;
  - aspiny 313861411 : f₀ brut **26.0 Hz** vs table 26.0 Hz —
    recoupement ✓ ; ASH-lite : Rc = 0.497, Rtop = 1.0, Rdyn = 0.0.
  La table Allen et le signal brut racontent la même histoire ; la
  cellule type II est confirmée type II au brut, et la cellule type I
  confirmée type I au brut.

## Lecture

- Le postulat implicite de P35 (« HH comme neurone de référence ») est
  **mesuré comme non représentatif** de l'onset cortical : HH démarre à
  60 Hz, le cortex démarre à 1–10 Hz. Le bon modèle minimal de l'onset
  cortical est de type I (Izhikevich RS), pas HH.
- La frontière type I / type II existe bien dans le réel (une
  interneurone sur seize ici) — elle est **rare**, pas absente.
- ddll : **déficit** — le seuil de classement (20 Hz) est payé une fois
  (hérité gelé de P35, non ré-ajusté) : la classification du réel
  achète sa frontière.

## B3-FAIL (publiés)

- **Chantier v1** : C2 cherchait le nom du stimulus dans les attributs
  des sweeps NWB v1 — absents (ils sont dans /stimulus/templates) ;
  zéro sweep Long Square trouvé. Corrigé : identification par la table
  API gelée. Attrapé par l'absence de recoupement avant gel.
- **Téléchargement** : deux NWB de contrôle corrompus par reprise curl
  pendant une coupure du montage de sortie (signature HDF5 invalide) ;
  re-téléchargés en une passe, intégrité vérifiée (48/92 sweeps
  lisibles).

## Artefacts

- `p41_neurones_reels.py` — SHA-256 `eb1b903ffb615e02…`
- `p41_neurones_reels_verdict.json`
- Données figées : `p41_data_catalog_allen.json` (1781 cellules),
  `p41_data_sweeps.json` (32 cellules), NWB de contrôle
  `p41_data_controle_spiny_313860745.nwb`,
  `p41_data_controle_aspiny_313861411.nwb`
- Source externe : Allen Cell Types (celltypes.brain-map.org),
  specimens mus musculus / homo sapiens, current-clamp Long Square.

**Falsifieur (gelé)** : C0 (HH type II / Izhikevich type I au seuil
gelé) échoue → l'instrument tombe ; le recoupement brut/table ±2 Hz
échoue → la mesure tombe.
