# Machine Noétique — `noetic-machine-complete`

> **Une sixième classe de machine : la « machine à éprouver ».**
> Entrée : des données mesurées + une structure candidate. Sortie : un **verdict**.
> Zéro paramètre ajusté. Levier discriminant. Invariance réplicable (SHA). Échecs publiés.

**Auteur :** Patrice PORTEMANN — patrice@portemann.eu — corpus [histoire-des-sciences.eu](https://histoire-des-sciences.eu)
**Licence :** MIT (voir `LICENSE`). **Bilan du chantier P0–P31 : 24 succès / 7 partiels-négatifs.**

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

## Bilan P20–P31 (cette série)

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

**La frontière est mesurée, pas conjecturée** : tout ce qui est discret/cinématique/à un corps est dérivable (24 succès) ; la réponse corrélée continue à deux corps ne l'est pas sans liberté de forme (7 partiels). Voir `Note_Synthese_Machine_Noetique_Complete.pdf`.

---

## Structure du dépôt

```
├── LICENSE                          # MIT
├── README.md
├── docs/                            # notes PDF (verdicts + synthèses)
│   └── Note_*.pdf
├── src/                             # scripts Python par chantier
│   ├── p20_h2plus.py  …  p31_portee.py
│   └── (fondateurs : p12, p16, p17, p18…)
├── data/                            # artefacts JSON (verdicts machine-lisibles)
│   └── p20_*.json … p31_*.json
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
```

## Règles permanentes du chantier

B3-FAIL (échecs publiés) · C12.1 (protocoles gelés pour le programme principal, canal libre ici) · *fermer, ne pas ajouter* · *conserver les versions* (addenda seulement) · *motivation, pas postulat*.

Le Programme 2027 reste fermé ; ce dépôt est le **canal exploratoire hors-programme**.
