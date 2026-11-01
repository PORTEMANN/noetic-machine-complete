# Note — Premier axe clinique réel : schizophrénie (UCLA LA5C, pilote)

**Date :** 2026-11-01 · **Tiroir :** cognition (MCS-28, axe SZ) · **Statut :**
pilote provisoire, non scellé.
**Filiation :** NOTE-MCS-28 (§9–§12 : dry-run, axe SZ gelé le plus fragile)
· NOTE-DETTE-COSMO · infrastructure `preprocessing/ants_pipeline.py` v0.1.

---

## 1. Contexte

COBRE inaccessible (NITRC en maintenance mondiale au moment du chantier).
Bascule sur **UCLA LA5C (OpenNeuro ds000030)** : 272 sujets, 50 SCHZ /
130 CONTROL avec rest, téléchargement direct S3 public, zéro inscription.
Pré-traitement : chaîne B-light validée (SyNRA, nuisance, AAL-116),
**zéro échec** sur 24 sujets, FD tous < 0,7 mm.

## 2. Résultats du pilote (12 SCHZ vs 11 CONTROL, nuls d'étiquettes
N = 10 000, graine 20261028)

| Invariant | SCHZ | CTRL | Z | p |
|---|---|---|---|---|
| Γ (spécialisation) | 0,263 | 0,226 | **+2,35** | **0,0004** |
| S_ent (entropie spectrale) | 0,166 | 0,103 | **+2,39** | **0,0010** |
| d_eff (dimension effective) | 1,065 | 1,035 | **+2,56** | **0,0015** |
| C_26 | 0,765 | 0,773 | −0,09 | 0,85 |
| M_34 | 0,714 | 0,781 | −0,98 | 0,054 |

## 3. Lecture doctrine — trois faits, trois tempérances

1. **S_ent↑ confirmé dans la direction gelée de 2025.** C'est la première
   confirmation expérimentale d'un axe de Cognition_2. Mais Γ va **en sens
   inverse** du gelé (Γ↓ attendu, Γ↑ mesuré) — et ce n'est pas une
   surprise : le dry-run (§9) avait mesuré que Γ et S_ent sont
   positivement couplés, rendant la combinaison « S_ent↑ Γ↓ »
   mathématiquement fragile. La réalité tranche comme le dry-run l'a
   prédit : les deux montent ensemble. **L'axe gelé SZ demande révision :
   S_ent↑ tient, Γ↓ tombe.**

2. **Les effets sont anormalement forts pour n = 23.** p ~ 10⁻³ à cette
   taille est possible mais inhabituel ; jusqu'à la cohorte complète
   (50 SZ / 127 CTRL), statut = **piste forte, non verdict**. La règle 1.2
   s'applique à soi : la démonstration de puissance n'est pas faite sur
   cet échantillon.

3. **Le mouvement n'explique pas le signal, mais le surveille.** FD moyen
   SZ 0,241 vs CTRL 0,166 (t = 1,36, n.s.) ; corr(FD, Γ) = −0,02,
   corr(FD, S_ent) = +0,27 (n = 12). Le pilote n'est pas un artefact de
   mouvement à première vue — mais la différence de tendance FD SZ > CTRL
   est classique de la littérature et **impose une analyse appariée FD**
   (régression ou matching) sur la cohorte complète.

## 4. Programme

1. Cohorte complète LA5C (50 SZ / 127 CTRL restants ≈ 4 h de calcul).
2. Analyse FD-appariée + nul symétrique G/D (déclaré, non encore tourné
   sur ce jeu).
3. COBRE en réplication dès le réveil de NITRC (cohorte indépendante —
   le vrai test de robustesse).
4. Seulement alors : verdict de l'axe SZ, scellement ou révision datée.

*Données : `data/ucla-cnp/` (raw OpenNeuro, invariants.csv, out/ par
sujet). Script pilote : `preprocess_ucla.py`. Aucune donnée publiée —
invariants agrégés uniquement, conforme DUA OpenNeuro.*
