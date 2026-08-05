# Machine Noétique — `noetic-machine-complete`
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/PORTEMANN/noetic-machine-complete)](https://github.com/PORTEMANN/noetic-machine-complete/releases)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21807052.svg)](https://doi.org/10.5281/zenodo.21807052)

> **Une sixième classe de machine : la « machine à éprouver ».**
> Entrée : des données mesurées + une structure candidate. Sortie : un **verdict**.
> Zéro paramètre ajusté. Levier discriminant. Invariance réplicable (SHA). Échecs publiés.

**Auteur :** Patrice PORTEMANN — patrice@portemann.eu — corpus [histoire-des-sciences.eu](https://histoire-des-sciences.eu)
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
| P31 | portée dérivée | 3/5 | **frontière r₁₂ constitutive** |
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
│   ├── p20_h2plus.py  …  p33_queue.py
│   └── (fondateurs : p12, p16, p17, p18…)
├── data/                            # artefacts JSON (verdicts machine-lisibles)
│   └── p20_*.json … p33_*.json
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