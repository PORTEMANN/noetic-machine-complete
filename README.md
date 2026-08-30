# Machine Noétique — `noetic-machine-complete`
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/PORTEMANN/noetic-machine-complete)](https://github.com/PORTEMANN/noetic-machine-complete/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21807052.svg)](https://doi.org/10.5281/zenodo.21807052)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0009--4016--8389-A6CE39?logo=orcid)](https://orcid.org/0009-0009-4016-8389)

> **Une sixième classe de machine : la « machine à éprouver ».**
> Entrée : des données mesurées + une structure candidate. Sortie : un **verdict**.
> Zéro paramètre ajusté. Levier discriminant. Invariance réplicable (SHA). Échecs publiés.

**Auteur :** Patrice PORTEMANN — [ORCID: 0009-0009-4016-8389](https://orcid.org/0009-0009-4016-8389) — patrice@portemann.eu — corpus [histoire-des-sciences.eu](https://histoire-des-sciences.eu)
**Licence :** MIT (voir `LICENSE`). **Bilan du chantier P0–P33 : 24 succès / 9 partiels-négatifs.**
**Référence figée (Zenodo) :** [doi.org/10.5281/zenodo.21807052](https://doi.org/10.5281/zenodo.21807052)

---

## Qu'est-ce que la Machine Noétique ?

La Machine Noétique n'est ni un modèle au sens usuel, ni un solveur, ni un système d'apprentissage. C'est un **opérateur de verdict** sur des structures physiques candidates :

```
M̂ : (D, S, L)  →  V ∈ {succès, partiel, échec}
```

- **D** = données mesurées, figées (constantes, masses, coefficients) — jamais ré-ajustées ;
- **S** = structure candidate (hamiltonien effectif, topologie, règle de couplage…) ;
- **L** = **levier discriminant** — chaque mécanisme doit survivre à sa propre suppression ;
- **V** = verdict, figé par empreinte SHA-256 (réplicabilité).

### Quatre invariants opérationnels
1. **Zéro paramètre ajusté** — tout nombre hors de `D` est *dérivé*, jamais fitté.
2. **Levier discriminant** — on retire le mécanisme, le résultat doit s'effondrer.
3. **Invariance réplicable** — chaque artefact (script, JSON, figure, note) est figé par SHA-256.
4. **B3-FAIL** — l'échec est une sortie publiée avec le même soin que le succès.

### Le postulat testé
La physique est « bon marché » en information dans son **régime discret** (statistiques, parités, nombres quantiques, topologie, sélections, signes, directions, séquences) — dérivable de peu de données. Elle devient coûteuse dans son **régime continu à deux corps** (corrélations détaillées, magnitudes). La machine est calibrée sur cette frontière : elle gagne là où la nature est discrète, s'arrête là où elle devient continue.

---

## Bilan du chantier P0–P33

Le chantier complet court de **P0** (monopole SU(2) banc calibré) à **P33** (décroissance asymptotique). Les chantiers P20–P33 (cette série) :

| Ch. | Objet | Score | Statut |
|-----|-------|-------|--------|
| P20 | liaison H₂⁺ dérivée | 5/5 | succès |
| P21 | polarité des liaisons | 7/7 | succès |
| P22 | double-β | 5/6 | partiel |
| P23 | moments de Schmidt | 6/6 | succès |
| P24 | suite de Jain (Hall fractionnaire) | 6/6 | succès |
| P25 | isolants topologiques 2D/3D | 6/6 | succès |
| P26 | diffusivité nucléaire dérivée | 4/5 | partiel |
| P27 | corrélation He/H₂ | 5/5 | succès |
| P28 | unification (réponse 2-corps) | 7/7 | succès |
| P29 | isovecteur / peaux | 5/6 | partiel |
| P30 | cusp de Kato | 3/5 | partiel |
| P31 | portée dérivée | 3/5 → **5/5** (F9) | frontière déclarée constitutive — **artefact de l'intégrande** : verdict 5/5 avec la forme corrigée (voir F9) |
| P32 | cartographie frontière (Z=2–6) | 4/5 | **frontière Z-dépendante (loi)** |
| P33 | décroissance asymptotique | 3/5 | partiel — **P31 renforcée** |

**La frontière est mesurée, pas conjecturée** : tout ce qui est discret/cinématique/à un corps est dérivable (24 succès) ; la réponse corrélée continue à deux corps ne l'est pas sans liberté de forme (9 partiels). Voir `Note_Synthese_Machine_Noetique_Complete.pdf`.

### La trilogie de la frontière r₁₂ (P31 → P33)

P31 a déclaré la frontière **constitutive** (structurelle, pas paramétrique) ; P32 lui a donné une **loi** (elle se ferme quand la corrélation relative 1/Z devient trop faible pour qu'une portée dérivée batte Hartree-Fock) ; P33 a montré qu'**aucun cumul de contraintes exactes** (cusp + queue asymptotique √(2I)) ne la franchit — les deux contraintes se contredisent dans un Jastrow à un terme. La frontière r₁₂ est un **objet mesuré**, pas une limite subie.

Artefacts P32/P33 : scripts `src/p32_frontiere.py`, `src/p33_queue.py` ; protocoles figés et verdicts `data/p32_*.json`, `data/p33_*.json`. Les figures se régénèrent en exécutant les scripts ; les notes PDF compilées (`Note_P32…`, `Note_P33…`) rejoignent `docs/`.

---

## Chantier hors-programme : bifurcations classificatoires

Série distincte du noyau P0–P33 : la machine éprouve les **bifurcations de classement** du tableau périodique par discriminant dérivé à zéro paramètre. Voir `bifurcations/`.

| Chantier | Question | Score | Verdict |
|---|---|---|---|
| P-He | He : H / Be / gaz noble ? | 5/5 | **tranchée** — He gaz noble (le « ns² » est sous-couche pleine, pas parenté Be) |
| P-LaLr | bloc f : La/Ac ou Lu/Lr ? | 2/5 | **B3-FAIL** — frontière d/f = zone de liberté constitutive (conventionnelle) |
| P-CrCu | anomalies d⁵/d¹⁰ : loi ou bruit ? | 3/5 | **partiel** — loi exacte en 3d, liberté en 4d/5d |
| P-F3 | indice de complexité dérivé ? | 3/5 | **partiel-négatif** — pas d'indice scalaire ; révèle l'axe *conventionnalité* |

**Résultat transverse — la loi des bifurcations (conjecture, catégorie II candidate)** : pour une bifurcation *physique*, la dérivabilité décroît avec la complexité (tranchable à bas Z, libre à haut Z) ; une bifurcation *conventionnelle* est libre quelle que soit la complexité. C'est la **formulation classificatoire de la frontière r₁₂** (P32). La machine **discrimine les bifurcations résolubles des constitutives** et cartographie deux sortes de zones de liberté.

*Statut : la loi des bifurcations est une conjecture étiquetée (catégorie II), non un théorème. Distincte du noyau certifié.*

---

## Suite du corpus — P34–P42, série A, méta-chantiers M1/M1b (août 2026)

### Série P (suite) : P34–P42

| Ch. | Objet | Verdict |
|-----|-------|---------|
| P34 | neurone formel : séparabilité et leviers | succès — 12/14 fonctions non triviales séparables ; biais constitutif, σ non constitutive, frontière XOR fermée à coût dérivé |
| P35 | neurone biologique (σ face au spike) | **B3-FAIL** — σ réfuté comme modèle du neurone biologique |
| P36 | profondeur des réseaux | succès — la profondeur devient constitutive dès que la tâche itère (parité : profondeur 2, n unités dérivées) |
| P37 | neurone fractionnaire | partiel — réfuté comme modèle du spike, **éprouvé comme modèle de la mémoire** (queue algébrique t⁻ᵅ constitutive) |
| P38 | bloc d'attention minimal | succès — POSITION constitutive (copie : 8/262144 sans, 262144/262144 avec) ; SOFTMAX non constitutif |
| P39 | fermeture de la frontière r₁₂ | **frontière fermée** — un couple à zéro paramètre passe le tamis A3 en tout Z (domaine variationnel) |
| P40 | Z_max et fission (AME2020 / JEFF-3.1.1 figées) | Z_max = **180** recomputé exactement (α gelé 2⁻¹⁰) ; P-FISSION **réfutée** (B3-FAIL) |
| P41 | excitabilité de neurones corticaux réels (Allen Cell Types, NWB bruts) | population corticale type I (1/32 type II) ; **HH (type II) non représentatif**, Izhikevich RS si ; recoupement brut ±2 Hz sur les deux cellules de contrôle |
| P42 | pont 120 ↔ E₈ (icosaèdre binaire / McKay) | pont **arithmétique** établi : \|2I\| = racines⁺(E₈) = 120, quiver de McKay calculé (A·d = 2d exact) — entrée F14 partielle |
| P43 | l'ASH sous la machine (l'instrument audité, noyau v1.0.0 figé) | succès 7/7 — O(1)/fenêtre confirmé, zéro paramètre ajusté confirmé, **ReN réfuté comme invariant physique** (pente d'amplitude −0,996, 2 franchissements de régime → F16), résolution effective affinée (max(5,9 %, (fs/nperseg)/f)), signatures Allen conformes (porteuse = 1/ISI médian) |
| P44 | EEG imagerie motrice réelle (BCICIV-2a, 9 sujets) — la chaîne lit-elle la pensée ? | partiel 2/3 — **les deux règles zéro paramètre RÉFUTÉES** (0,540 et 0,520 vs seuil 0,60 ; B3-FAIL publié) ; leviers tenus (l'effet vit dans μ, canaux moteurs) ; 1 sujet lisible (A03, 0,771 — illettrisme BCI mesuré) ; **F17 ouverte** : agrégation d'essais / baseline figée / filtrage spatial dérivé |
| P45 | benchmarks EEG renormales (consequence F16) | partiel 3/4 — **la classification survit sans ReN** (10/10 paires separees par invariants normalises, invariants a 1e-9) ; ReN pente -1 exacte (hors entropie degeneree, saturation au plancher +1e-8 publiee) ; 3/5 signaux franchissent un regime par amplitude seule ; **table figee juin 2026 non reproductible** par les pipelines declares (B3-FAIL d archive -> F18) ; bouffee beta EEG lisible a n_octaves=5 (E5 x3,66) | — **conséquences appliquées à noetic-ash v1.1.0** (ReN retiré de la classification officielle, table re-figée F18 fermée, grille EEG 5 octaves, erratum publié) |

### Série A : la méthode s'éprouve elle-même

| Ch. | Objet | Verdict |
|-----|-------|---------|
| A1 | batterie de perturbation (π perturbé, D et S intacts) | PASS — fragilités publiées par chantier, prédictions de fragilité éprouvées |
| A2 | moteur de leviers | PASS — le moteur ne voit que ce qui existe |
| A3 | tamis de Jastrow (N=64/96/128) + réénumération KO-6 | le plafond « 63 160 » est **réfuté comme publié** (B3-FAIL du corpus) ; l'énumération KO-6 propre reste ouverte, coût de fermeture déclaré |
| A4 | registre des frontières REG-FR-1.0 | **20 entrées** F1–F20 (**9 fermées**, 5 ouvertes, 6 partielles), ddll par entrée, falsifieurs pré-enregistrés, SHA global `bd592a8a3dc16b4a…` |
| A5 | conjecture des frontières | v1 **réfutée** par F5 + F7 + F14 (10/13) ; v2 en vigueur (11/13 points) |
| A1b | batterie rétroactive P13/P22 (ferme F7) | couples (V, Σ) publiés : P13 Σ=1 (4/4) ; P22 Σ_min=0.94 (5/6 inchangé), une fragilité de seuil publiée ; prédictions pré-enregistrées confirmées |

### Méta-chantiers M1 / M1b : l'économie de l'information mesurée

M1 (ECO-1.0) éprouve le postulat central du corpus sur 23 chantiers, métriques uniformes gelées (S = SLOC, V₁ = feuilles numériques des JSON, V₂ = dénominateurs de scores). **Prédiction pré-enregistrée réfutée — avec inversion** : le ratio informationnel est *plus élevé* au voisinage de la frontière r₁₂ (ρ₁ médiane 0.898 vs 0.275). L'affinage mesuré : ce qui s'effondre à r₁₂, c'est le **taux de succès des confrontations externes** (τ : 0.60 vs 1.00), pas le ratio brut. M1b (ECO-1.1) réplique au proxy de Kolmogorov (taille gzip ; Spearman(SLOC, gzip) = 0.980) : **l'inversion survit — la réfutation est structurelle**. M1 a aussi confirmé indépendamment l'entrée F9 (corruption p32/p33), réparée (commits `27b0db7`, `301e326a`) : p32/p33 restitués (30 valeurs figées reproduites à 5 décimales) et **p31 re-publié avec l'intégrande |∇Ψ|² de P39** — le verdict historique de P31 bascule de 3/5 à 5/5 : la « frontière constitutive » était un artefact de l'intégrande (écart mesuré jusqu'à 0.14 Ha, anomalie variationnelle publiée). **F9 fermée.**

**Série M2 — métrologie de la liberté (le registre devient algèbre)** : le comptage ddll devient une mesure formelle d ∈ ℕ̄ avec monoïde des coûts, composition et ordre de fermeture (M2, cohérence 18/18, image ponctuelle {0,1}) ; homomorphisme mesuré d(t^m∘t^k) = d(m)+d(k) et conversion profondeur↔largeur (M2b, 26/26) ; ordre enrichi et loi prospective L5 confrontée à deux familles neuves (M2c : parité d(n)=n — F19 ; M2e : tri de Batcher à la borne informationnelle — F20) ; surface de coût d(m,k) exacte et optimum mesuré d*(m)=2m (M2d) ; copie d(n)=n **certifiée minimale** (Lévy–Desplanques). Série : 5/5 + 4/4 + 4/4 + 4/4 + 3/3.

### Données figées hors dépôt

Les gros artefacts de P41 (NWB bruts Allen Cell Types + catalogues, ≈ 80 Mo) sont publiés en **release `artefacts-donnees-v1.0`** ; leurs empreintes figurent dans `SHASUMS.txt`.

---

## Citation

```bibtex
@misc{portemann2026noetic,
  author = {Portemann, Patrice},
  title  = {La Machine No\'etique : un op\'erateur de verdict unique \`a z\'ero param\`etre ajustable --- synth\`ese du programme P0--P31},
  year   = {2026},
  doi    = {10.5281/zenodo.21807052},
  url    = {https://doi.org/10.5281/zenodo.21807052}
}
```

---

## Structure du dépôt

```
├── LICENSE                          # MIT
├── README.md
├── docs/                            # notes PDF (verdicts + synthèses)
│   └── Note_*.pdf
├── src/                             # scripts Python par chantier
│   ├── p20_h2plus.py  …  p42_pont_120_e8.py
│   ├── a1_batterie_perturbation.py … a5_conjecture_frontieres.py
│   ├── m1_economie_information.py, m1b_economie_robustesse.py
│   └── (fondateurs : p12, p16, p17, p18…)
├── data/                            # artefacts JSON (verdicts machine-lisibles)
│   └── p20_*.json … p42_*.json, a*/m1* + m1_corpus/ (miroir SHA-vérifié)
├── bifurcations/                    # chantier hors-programme (bifurcations classificatoires)
│   ├── README.md                    # index + verdicts P-He/P-LaLr/P-CrCu/P-F3
│   ├── Loi_des_Bifurcations.md      # conjecture v1 + addendum v2
│   └── *.json                       # protocoles figés + verdicts
├── figures/                         # figures PNG
│   └── p*.png
└── SHASUMS.txt                      # empreintes SHA-256 de tous les artefacts
```

Chaque note PDF cite les empreintes SHA de ses artefacts — la **chaîne documentaire** est la preuve de réplicabilité.

---

## Utilisation

Environnement : Python 3.12, NumPy, SciPy, Matplotlib. Chaque script est autonome et produit son JSON + sa figure :

```bash
python3 src/p24_jain.py        # → data/p24_jain.json + figures/p24_jain.png + shas
python3 src/p32_frontiere.py   # → série isoelectronique Z=2..6 (frontière r₁₂)
python3 src/p33_queue.py       # → double contrainte cusp + queue asymptotique
```

## Règles permanentes du chantier

B3-FAIL (échecs publiés) · C12.1 (protocoles gelés pour le programme principal, canal libre ici) · *fermer, ne pas ajouter* · *conserver les versions* (addenda seulement) · *motivation, pas postulat*.

Le Programme 2027 reste fermé ; ce dépôt est le **canal exploratoire hors-programme**.
