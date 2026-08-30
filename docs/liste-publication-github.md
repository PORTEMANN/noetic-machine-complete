# Chantiers à publier sur GitHub — inventaire et affectation par dépôt

**Patrice Portemann — corpus Machine Noétique**
30 août 2026 (rafraîchi après P36–P42 + M1)

> Note d'accès : la page `histoire-des-sciences.eu/cockpit` est protégée
> par connexion (« Cockpit HdS / Connexion ») — son contenu n'est pas
> lisible publiquement. La liste ci-dessous est construite depuis
> l'inventaire complet des artefacts de la session, à rapprocher du
> cockpit lorsque tu l'auras sous les yeux. La publication elle-même
> attend le jeton que tu fourniras.

## 1. Dépôt `noetic-machine-complete` — chantiers P (suite du corpus P0–P33)

| Artefact | Type | Destination proposée |
|---|---|---|
| `p34_neurone.py` + `p34_neurone_verdict.json` | script + verdict | `src/` + `data/` |
| `p35_neurone_biologique.py` + verdict JSON + PNG | script + verdict | `src/` + `data/` |
| `p36_profondeur.py` + `p36_profondeur_verdict.json` | script + verdict | `src/` + `data/` |
| `p37_neurone_fractionnaire.py` + verdict JSON + PNG | script + verdict | `src/` + `data/` |
| `p38_attention.py` + `p38_attention_verdict.json` | script + verdict | `src/` + `data/` |
| `p39_fermeture_r12.py` + `p39_fermeture_r12_verdict.json` | script + verdict | `src/` + `data/` |
| `p40_zmax.py` + `p40_zmax_verdict.json` | script + verdict | `src/` + `data/` |
| `p40_data_ame2020_mas20.txt` + `p40_data_fy235u.csv` + `p40_data_fy239pu.csv` | données figées (AME2020, JEFF-3.1.1) | `data/` |
| `p41_neurones_reels.py` + `p41_neurones_reels_verdict.json` | script + verdict | `src/` + `data/` |
| `p41_data_catalog_allen.json` + `p41_data_sweeps.json` + 2 NWB de contrôle | données figées (Allen Cell Types) | `data/` |
| `p42_pont_120_e8.py` + `p42_pont_120_e8_verdict.json` | script + verdict | `src/` + `data/` |
| notes P34, P35, P36, P37, P38, P39, P40, P41, P42 (md/docx) | documentation | `docs/` |

## 2. Dépôt `noetic-machine-complete` — chantiers A et méta-chantier M1

| Artefact | Type | Destination proposée |
|---|---|---|
| `a1_batterie_perturbation.py` + `a1_batterie_verdict.json` | script + verdict | `src/` + `data/` |
| `a2_moteur_leviers.py` + `a2_moteur_leviers_verdict.json` | script + verdict | `src/` + `data/` |
| `a3_tamis_jastrow.py` + verdicts JSON (N64/N96/N128 + chunks) | script + verdicts | `src/` + `data/` |
| `a3_ko6_reenumeration.py` + verdict JSON | script + verdict | `src/` + `data/` |
| `a4_registre_frontieres.py` + `a4_registre_frontieres.json` | registre (**15 entrées**, SHA `4b82ca3fdbb5ae88…`) | racine ou `data/` |
| `a5_conjecture_frontieres.py` + verdict JSON | script + verdict (v1 réfutée par F5+F14 ; v2 = 11/12) | `src/` + `data/` |
| `m1_economie_information.py` + `m1_economie_information_verdict.json` | méta-chantier (postulat central mesuré : réfuté brut, affiné) | `src/` + `data/` |
| `m1b_economie_robustesse.py` + `m1b_economie_robustesse_verdict.json` | méta-chantier (robustesse : inversion confirmée au proxy gzip, Spearman 0.980) | `src/` + `data/` |
| `m1_corpus/` (miroir SHA-vérifié, 87 fichiers) | réplicabilité du méta-chantier | `data/m1_corpus/` |
| notes A1, A2, A3, A4-A5, M1, M1b (md/docx) | documentation | `docs/` |

*Alternative discutable : un dépôt séparé `noetic-method` pour la série A
(méthode) et M1 en gardant `noetic-machine-complete` pour la série P
(physique). Tranché au moment de la publication.*

## 3. Hygiène du corpus existant (frontières F9 / F10 du registre)

| Chantier | Action exacte |
|---|---|
| **F9 — p32/p33 corrompus** | **confirmé par M1 (mesure indépendante)** : re-publier `p32_frontiere.py` et `p33_queue.py` en Python propre (les fichiers commités sont en base64 : SHA bruts `bbf42182…`/`1a4bb130…` ≠ SHASUMS `60a868bd…`/`286f9888…`, ni bruts ni décodés), régénérer JSON/PNG, **mettre `SHASUMS.txt` à jour** |
| **F10 — Topological-Fractional-AI** | publier le script du modèle 84.1 % AUC / 28 paramètres — P37 fournit déjà la dynamique fractionnaire exécutable (`p37_neurone_fractionnaire.py`, E_α contrôlée à 2.6e-16) mais ne ferme pas l'entrée |

## 4. Discipline de publication (héritée du corpus)

- Chaque script : protocole gelé en en-tête, zéro paramètre ajusté,
  falsifieur déclaré, B3-FAIL publiés (P40 : 1 + P-FISSION réfutée ;
  P41 : 2 ; P42 : 3 internes ; M1 : rupture SHA corpus + prédiction
  pré-enregistrée réfutée — tous documentés dans les JSON).
- Chaque verdict : JSON + SHA-256 du script ; registre A4 : SHA-256 par
  entrée + global (15 entrées : 4 fermées, 6 ouvertes, 5 partielles).
- `SHASUMS.txt` régénéré sur l'ensemble des fichiers publiés.
- Les figures PNG accompagnent les scripts dans `data/` ou `figures/`.

## 5. Ordre de publication suggéré

1. **F9 d'abord** (hygiène : sources p32/p33 propres + SHASUMS) — le
   corpus existant redevient conforme avant d'ajouter du nouveau.
2. Série P : P34 → P42 (continuité P0–P33), données figées incluses.
3. Série A : A1 → A5 + registre (la méthode documente les chantiers).
4. **M1 + M1b** (les méta-chantiers mesurent le corpus : ils se publient après lui).
5. F10 en dernier (script Topological-Fractional-AI, dépôt séparé).

*En attente du jeton GitHub — aucune action sur les dépôts avant.*
