# A1 — Batterie de perturbation de protocole : le verdict devient un couple (V, Σ)

**Chantier A1 du programme de prospection de la Machine Noétique — axe 1 (méthode).**
Artefacts : `a1_batterie_perturbation.py` · `a1_batterie_verdict.json` · protocole gelé **PERT-BATT-1.0**.

## 1. Le problème

Un verdict de la machine n'est jamais meilleur que le protocole gelé qui l'a produit.
P35 l'a démontré *par l'accident* : trois erreurs de protocole ont failli produire trois faux verdicts —

1. **C1 testé loin du seuil** (I = 10 vs 20) : la sigmoïde saturée paraissait *meilleure* que le neurone biologique ;
2. **bruit injecté** (1e-9·randn) puis normalisé : un spectre blanc fantôme (Rtop = 1503) ;
3. **résidu flottant normalisé** (~1e-17 amplifié) : des pics spectraux fantômes (Rtop = 5) sur un signal rigoureusement constant.

Ces accidents ont été attrapés à la main. A1 les rend **impossibles à cacher** : le protocole devient un objet perturbable déclaré, et la machine publie la stabilité avec le verdict.

## 2. La méthode — PERT-BATT-1.0 (gelé)

$$ \hat{M}(D, S, L, \pi) \;\longrightarrow\; (V,\ \Sigma) $$

- chaque chantier est réécrit en **fonction pure** `f(π) → (verdicts booléens, mesures)` — D et S restent figés, seul π bouge ;
- chaque paramètre de π est un **axe de perturbation déclaré avant exécution** (plan factoriel axial : une coordonnée à la fois) ;
- **Σ** = fraction des protocoles (nominal inclus) qui préservent le verdict nominal. Σ = 1 : stable. Σ < 1 : **fragile → publié comme B3-FAIL de protocole**, avec l'axe responsable ;
- les **mesures** ne sont pas des verdicts : on publie leur dispersion (min/max), qui mesure la sensibilité de la *mesure* sans affecter le *verdict*.

## 3. Résultats

### P34 — neurone formel vs 16 fonctions booléennes (11 protocoles)

Axes : marge LP {0.5, 2, 10}, graine/pas/budget du témoin backprop.

| composante | Σ |
|---|---|
| compte 12/14, XOR et XNOR inséparables | 1.00 |
| biais constitutif pour 12 fonctions | 1.00 |
| XOR fermé à coût +1 couche | 1.00 |
| témoin backprop concordant | 1.00 |

**Stabilité totale, et elle est comprise** : la faisabilité LP est invariante d'échelle — toute marge > 0 est équivalente par rescaling de (w, b). Le verdict *exact* ne dépend d'**aucun** choix de protocole. La dispersion des mesures le confirme : n_séparables = 12 partout ; seule la MSE du témoin statistique bouge (×9), sans conséquence.

### P35 — neurone formel σ vs Hodgkin–Huxley (17 protocoles)

Axes : dt {0.01, 0.04}, discard {25, 100 ms}, points de test C1 alternatifs, tolérances ±50 % et ×2, grille f–I, règle ASH-lite, seuil de pics.

**Les 8 composantes, dont le verdict global « σ réfutée », sont stables : Σ = 1.00 partout.**
Les mesures bougent — rate10 : 68–70 Hz, saut f–I : 60–64 Hz, spikes Izhikevich : 5–7, Rc : ±25 % — **sans qu'aucun verdict ne bascule**. La distinction verdict/mesure n'est pas décorative : elle est ce qui permet au verdict de survivre au protocole.

### Prédictions pré-enregistrées : 3/3 confirmées

(i) P34 stable à 100 % par construction ; (ii) le verdict global de P35 survit à toute perturbation déclarée ; (iii) des mesures de P35 sont sensibles au protocole sans effet sur le verdict.

## 4. Certification par mutation : la batterie elle-même éprouvée

Un PASS qui ne peut pas passer au rouge ne vaut rien. Les trois accidents historiques de P35 ont été réintroduits comme **protocoles mutés** :

| mutation | verdict attendu | résultat |
|---|---|---|
| M1 — C1 loin du seuil (10/15/20) | bascule détectée | ✅ C1_bio, C1_S **et verdict global** basculent — σ « réhabilitée » sous protocole muté, donc détectée |
| M2 — bruit 1e-9 injecté | bascule détectée | ✅ C5 bascule (spectre fantôme) |
| M3 — résidu flottant normalisé | bascule détectée | ✅ C5 bascule |

**M3 a d'abord échoué** : à 1e-17, le bruit est absorbé par l'arrondi flottant (ε ≈ 2.2e-16 à magnitude ~1), la mutation passait inaperçue — la batterie était aveugle. **B3-FAIL d'A1, publié et fermé** : garde `std == 0` ajoutée à ASH-lite (un signal rigoureusement constant n'a pas de spectre, quel que soit le seuil — sinon 0/0 = NaN, verdict silencieusement faux), mutation réaliste à 1e-15. Certification finale : **PASS, 3/3 accidents détectés**.

## 5. Ce que A1 change pour le corpus

- Tout verdict publié devient un couple **(V, Σ)** — la stabilité fait partie du résultat, pas de la discussion.
- Un verdict fragile n'est pas jeté : il est **étiqueté** avec l'axe responsable. La fragilité est une mesure, pas une honte.
- Application rétroactive au corpus P0–P33 : chaque chantier sera encapsulé en `f(π)` et passé à la batterie ; prédiction du programme — certains partiels (P13, P22) sont sensibles au protocole.
- La certification par mutation est **constitutive** : toute évolution de la batterie devra redétecter M1–M3.

**Falsifieur** : tout protocole perturbé changeant un verdict de P34 tue « P34 stable à 100 % » ; tout protocole perturbé réhabilitant σ sur C1/C2/C3 tue « P35 globalement stable » ; toute mutation M1–M3 non détectée tue la batterie.

---

*A1 — PERT-BATT-1.0 · SHA-256 du script dans `a1_batterie_verdict.json` · zéro paramètre ajusté, axes déclarés avant exécution.*
