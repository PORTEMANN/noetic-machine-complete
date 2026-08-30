# A3 — Le juge devient tamis : frontière r₁₂ et ré-énumération KO-6

**Chantier A3 du programme de prospection — axe 1 (méthode).**
Artefacts : `a3_tamis_jastrow.py` · `a3_tamis_jastrow_verdict.json` · `a3_ko6_reenumeration.py` · `a3_ko6_reenumeration_verdict.json` · protocoles gelés **TAMIS-J12-2.0** et **TAMIS-KO6-1.0**.

## 1. Le problème

Un juge qui choisit ses candidats choisit partiellement ses verdicts. P31–P33 testaient trois règles de portée pour une seule famille de Jastrow ; l'énumération KO-6 annonçait 63 160 réalisations « certifiées ». A3 remplace le choix par l'énumération : **toute** famille déclarée × **toute** règle déclarée × **tout** Z, et pour KO-6, l'énumération complète **plafond supprimé**.

## 2. Volet 1 — Tamis de Jastrow sur la frontière r₁₂ (Z = 2..6)

### Le tamis a d'abord failli — B3-FAIL d'A3, publié et fermé

La première version a produit des « victoires » avec des gains de **225 % à 4 377 % du résiduel** : des énergies *sous* l'exact, donc non variationnelles. Deux défauts détectés par le tamis lui-même :

1. **Déviation de protocole** : la règle de portée β doit être figée en ζ₀ = Z−5/16 puis ζ balayé (protocole corpus) — coupler β au ζ courant en dévie ;
2. **Absence de porte variationnelle** : l'intégrateur delta de C12.1 n'est valide qu'en corrélation faible (|u| ≪ 1). Hors de ce domaine, il produit des énergies non variationnelles — que le tamis v1 comptait comme des succès.

Fermeture : protocole TAMIS-J12-2.0 — règles figées en ζ₀ + **porte variationnelle** (E < E_exact − 5e-3 ⇒ cellule HORS DOMAINE, publiée, exclue des passants).

### La table finale (N = 96, stabilité 64/128)

| couple | Z=2 | Z=3 | Z=4 | Z=5 | Z=6 | stabilité |
|---|---|---|---|---|---|---|
| F1×R1 (corpus) | − | − | − | − | − | STABLE |
| F1×R2 | HD | HD | HD | HD | HD | FRAGILE |
| F1×R3 (corpus) | **+** | − | − | − | − | FRAGILE |
| F2×R1, F2×R2, F2×R3 | HD | HD | HD | HD | HD | STABLE |
| F4×R1, F4×R3 | − | − | − | − | − | STABLE |
| F4×R2 | HD | HD | HD | HD | HD | STABLE |
| F3×R3 (queue exacte P33) | − | − | − | − | − | STABLE |

(− : perd contre la référence split-ζ ; HD : hors domaine variationnel ; + : passe.)

**Verdicts mesurés** :

- **0/10** couple ne bat la référence en tout Z dans le domaine — la frontière r₁₂ est **confirmée** au niveau du tamis déclaré ;
- **25/50 cellules sont hors domaine** : la moitié de l'espace déclaré échappe à l'intégrateur delta. *Frontière d'intégrateur mesurée* — coût de fermeture exact : l'intégrateur d'espérance complet type P31 (×10), chantier déclaré (jonction avec P39) ;
- **Loi P32 affûtée** : la règle de densité R3 ne gagne clairement qu'en Z = 2. La « victoire » de P32 en Z = 3 (+3.5×10⁻³ Ha) est *sous la résolution de l'intégrateur* — à convergence (N96/N128) la cellule est perdante (−2.4×10⁻³). La loi Z-dépendante de la frontière est confirmée et durcie ;
- **La queue exacte dégrade en tout Z** (P33 reproduit, stable) : imposer l'asymptotique exacte coûte de l'énergie partout — résultat contre-intuitif du corpus, désormais vérifié sur trois grilles ;
- Contrôles : levier c = 0 exact (T0 PASS, trois grilles) ; croisement corpus T1 3/3.

## 3. Volet 2 — Ré-énumération KO-6 propre

Audit du moteur publié (`spectral-triple-minimality`), trois défauts :

| défaut | constat |
|---|---|
| D1 — plafond codé en dur | `if len(solutions) >= 63160: break` — le nombre annoncé est une **entrée** du script |
| D2 — axiomes proxys | `order_one` = symétrie matricielle ; `ko6` = k pair et dim ≥ 2k+1 — aucune structure J_F, γ_F, D_F |
| D3 — certification vide | `certify()` retourne `True` **inconditionnellement** |

**Ré-énumération fidèle, plafond supprimé** — prédiction pré-enregistrée confirmée : la cible « 7 bandes » avec la définition commitée (lignes non vides ≤ k ≤ 3) est **inatteignable → 0 solution**. Le moteur publié ne peut produire *aucune* des 63 160 réalisations qu'il annonce.

**Tamis de définitions** — le compte n'est pas un objet mathématique, c'est un artefact de définition :

| définition de « bande » | cible 7 | max atteignable | sans cible |
|---|---|---|---|
| lignes non vides (commitée) | 0 | 3 | 29 017 |
| entrées non nulles | 7 200 | 9 | 29 017 |
| paires non nulles | 0 | 6 | 29 017 |

**Verdict : le « 63 160 » est RÉFUTÉ comme publié (B3-FAIL du corpus)** — ni sortie du code, ni invariant de définition. Contrôle : la loi de multiplicité sqf (T4) passe ses propres tests — c'est le moteur d'énumération, pas les théorèmes, qui est en cause. **Coût de fermeture exact** : implémenter les vrais axiomes KO-6 au niveau des représentations (J_F² = +1, J_FD_F = D_FJ_F, (J_Fγ_F)² = −1, ordre un sur les blocs de D_F), ré-énumérer sous bornes déclarées, publier le compte quel qu'il soit.

## 4. Ce que A3 change pour le corpus

- Tout test de candidats devient une **énumération déclarée** : familles × règles × cas, table complète publiée.
- La **porte variationnelle** est désormais constitutive de tout tamis variationnel : une énergie sous l'exact est un diagnostic d'intégrateur, jamais un succès.
- Le tamis s'éprouve lui-même : B3-FAIL d'A3 (v1 sous-variationnelle) détecté, publié, fermé — comme A1 (mutation M3) et A2 (prédictions de l'expérimentateur 0/3).
- Deux frontières alimentent le registre A4 : r₁₂ (ouverte, double coût mesuré) et KO-6 (ouverte, nombre réfuté, axiomes réels à implémenter).

---

*A3 — TAMIS-J12-2.0 / TAMIS-KO6-1.0 · SHA-256 des scripts dans les JSON de verdict · zéro paramètre ajusté, grilles 64/96/128, porte variationnelle 5×10⁻³ Ha.*
