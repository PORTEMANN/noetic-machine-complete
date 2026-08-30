# A4 + A5 — Registre des frontières mesurées et conjecture des frontières

**Chantiers A4 et A5 du programme de prospection — axe 1 (méthode).**
Artefacts : `a4_registre_frontieres.py` · `a4_registre_frontieres.json` · `a5_conjecture_frontieres.py` · `a5_conjecture_frontieres_verdict.json` · protocoles gelés **REG-FR-1.0** et **CONJ-FR-1.0**.

## 1. A4 — la frontière devient un objet de première classe

Jusqu'ici, les frontières du corpus vivaient dispersées dans les verdicts (B3-FAIL, partiels, déclarations). A4 les registre à discipline ash-corpus : schéma déclaré (toute entrée invalide = B3-FAIL du registre), SHA-256 par entrée et global, et une règle dure : **n'entre au registre qu'une frontière mesurée** — verdict d'un chantier exécuté, artefact à l'appui.

### Le registre (10 entrées)

| id | type | statut | comptage de ddll |
|---|---|---|---|
| F1-XOR | physique | fermée (+1 couche, poids entiers dérivés) | déficit (1→2 hyperplans) |
| F2-SIGMA-DYNAMIQUE | physique | fermée (0D→2D plan ou 1D sur S¹) | déficit (0→2 variables d'état) |
| F3-R12-PORTEE | physique | ouverte (double coût mesuré par le tamis A3) | déficit putatif (1→2 corps) |
| F4-KO6-ENUMERATION | méthode | ouverte (« 63 160 » réfuté par A3) | déficit (proxys → représentations) |
| F5-BPS-ECHELLE | physique | ouverte (découverte A2) | **mode non contraint** (mode zéro d'échelle) |
| F6-COEUR-DIFFUS | physique | partielle (corpus P9/P11) | déficit (0→1 champ diffusif) |
| F7-PARTIELS-PROTOCOLE | méthode | ouverte (batterie A1 rétroactive à exécuter) | en attente de mesure |
| F8-ZMAX-E8 | physique | ouverte (chantier P40 à exécuter) | en attente de mesure |
| F9-HYGIENE-P32-P33 | hygiène | ouverte (base64 corrompu, SHA non conformes) | hors domaine |
| F10-CODE-FRACTIONNAIRE | hygiène | ouverte (résultats sans script) | hors domaine |

Deux entrées d'hygiène mesurées au passage par A3 : les scripts `p32/p33` publiés en base64 re-wrapé sont **corrompus** (caractères perdus aux sauts de ligne : `T<=R1+R2`, `_ckk]`) et leurs SHA-256 ne correspondent pas au registre SHASUMS.txt — la discipline de publication du corpus s'applique à elle-même.

## 2. A5 — la méta-loi éprouvée sur le registre

La conjecture du programme de prospection n'est pas discutée, elle est **éprouvée** : le registre A4 est la donnée figée D, la conjecture est la structure candidate S, le levier L est la chasse au contre-exemple. Domaine déclaré avant agrégation : types physique/méthode à comptage tranché → **n = 6 points mesurés**.

### Verdict

**v1 — « toute frontière mesurée est un déficit de dimension/degré de liberté » : RÉFUTÉE, 5/6.**

Le contre-exemple est F5 (découverte A2) : au point BPS, la frontière n'est pas une structure *manquante* mais une **direction sans coût** — le mode zéro d'échelle laisse la relaxation délocaliser le monopole jusqu'au bord de la boîte. Un surplus indéterminé, pas un déficit.

**v2 — raffinée à partir du contre-exemple publié :**

> *Toute frontière mesurée est un défaut de comptage des degrés de liberté — déficit (structure manquante : hyperplan, état, champ, deux-corps, représentations) ou mode non contraint (direction sans coût : échelle au point BPS).*

v2 couvre **6/6** points du domaine. Ce n'est pas une victoire verbale : la réfutation de v1 est *publiée* dans le verdict JSON (b3_fail), et v2 ne vaut que par ses prédictions.

### Prédictions pré-enregistrées de v2

- **F7** (partiels P13/P22) : quand la batterie A1 rétroactive tournera, les fragilités trouvées devront être des défauts de comptage de ddll — sinon v2 tombe ;
- **F8** (Z_max, chantier P40) : sa fermeture devra être un défaut de comptage de ddll — sinon v2 tombe.

**Falsifieur de v2** : toute frontière mesurée dont la fermeture ne change *aucun* comptage de degrés de liberté (ni ajout, ni contrainte, ni fixation de mode).

## 3. Bilan de l'axe 1 : la machine après cinq chantiers de méthode

| chantier | apport constitutif |
|---|---|
| A1 | le verdict est un couple **(V, Σ)** — stabilité publiée, batterie certifiée par mutation |
| A2 | les leviers sont **énumérés** — carte de constitutivité complète, contrôle tueur intégré |
| A3 | le juge est un **tamis** — candidats énumérés, porte variationnelle, intégrateur à domaine mesuré |
| A4 | les frontières sont des **objets registres** — schéma, SHA-256, statuts, coûts exacts |
| A5 | les frontières ont une **méta-loi falsifiable** — v1 réfutée publiée, v2 en vigueur sous prédictions |

Et trois résultats de physique au passage : la carte de constitutivité du monopole (les masses font l'existence), la frontière r₁₂ confirmée et durcie (R3 ne gagne qu'en Z = 2), le « 63 160 » réfuté comme artefact de protocole.

---

*A4/A5 — REG-FR-1.0 / CONJ-FR-1.0 · SHA-256 des scripts dans les JSON · le registre est la seule donnée d'A5, le comptage_ddll n'est jamais réinterprété.*
