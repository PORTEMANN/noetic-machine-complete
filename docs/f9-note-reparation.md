# Note F9 — Réparation du corpus : p31, p32, p33

**Patrice Portemann — Machine Noétique, hygiène de publication**
30 août 2026 — ferme l'entrée **F9-HYGIENE-P32-P33** du registre A4

## 1. Le défaut

Trois sources du corpus n'étaient pas conformes à la chaîne SHA-256 :

1. **p32_frontiere.py** et **p33_queue.py** avaient été commitées en
   base64 ré-emballé **corrompu** (caractères perdus aux frontières de
   lignes : `T<=R1+R2`, `_ckk]`, `_c[[]`, argument `c` manquant) — ni les
   fichiers bruts ni leurs décodages ne reproduisaient les SHA du
   registre. Détecté par l'audit A3, confirmé indépendamment par M1
   (rupture de chaîne SHA sur 2/85 fichiers du miroir).
2. **p31_portee.py** contenait un intégrande cinétique défectueux,
   découvert en voie d'exécution de P39 : mélange de deux formes IBP
   (le terme u′² de la forme |∇Ψ|² coexistant avec −(u″+2u′/u) de la
   forme laplacienne) et terme croisé sans facteur géométrique
   périmétrique (r̂ᵢ·Û).

## 2. La réparation

| Fichier | Réparation | Validation |
|---|---|---|
| `p32_frontiere.py` | 6 corruptions corrigées ; **npts=80** retrouvé par scan systématique | les **30 valeurs figées** des JSON p32/p33 reproduites à 5 décimales, à tout Z |
| `p33_queue.py` | masque `U==`→`U<=`, `_c[[]`, argument `c` restitué | Eref/R3/queue/A conformes aux JSON figés |
| `p31_portee.py` | intégrande remplacé par la forme \|∇Ψ\|² portée **à l'identique** de P39 (R12-FERM-1.0) ; protocole, grilles, règles R1/R2/R3 et critères C0–C4 **inchangés** | contrôle T1 mesurant les deux formes (ci-dessous) |

SHA réparés : p32 `cc94ef3e…`, p33 `29505862…` — conformes et rejoués.

## 3. T1 — mesure publiée du défaut p31 (les deux formes, même protocole)

La signature du défaut sur le protocole de P31 (cusp obligatoire
u′(0)=½, Φ=HF, c=0.5) :

- l'écart entre les deux formes atteint **0,14 Ha** (à β=0.25) et
  **change de signe** entre β=2.5 et β=3 — le terme cinétique fantôme
  n'est pas un biais monotone, il dépend du régime de portée ;
- à grand β (Jastrow réduit à son cusp court, qui doit *coûter* de
  l'énergie), la forme corrigée charge ce coût (E > E_ref) tandis que la
  forme corpus **plonge sous E_ref** (−2,8417 < −2,8351 à β=4) —
  variationnellement impossible pour un Jastrow qui s'éteint.

*Correction de la note de filiation : la formulation « la forme corpus
dégrade E ∀β » valait pour le protocole de P39 (fenêtre ζ hydrogénoïde,
familles F1–F4) ; sur le protocole de P31 la signature est la
sous-estimation systématique + l'anomalie à grand β. Les deux
formulations sont publiées, chacune sur son protocole.*

## 4. Conséquence mesurée : le verdict historique de P31 bascule

Avec l'intégrande corrigée, critères C0–C4 gelés inchangés :

| | initial (corpus) | corrigé (F9) |
|---|---|---|
| C1 une règle bat split-ζ | ✗ | ✓ (R3 densité, β=0,7146) |
| C2 gain ≥ 20 % du résiduel | ✗ | ✓ (0,020 Ha = 29 %) |
| score | **3/5 — frontière constitutive** | **5/5 — portée dérivable** |

La « frontière r₁₂ constitutive » déclarée par P31 était donc **un
artefact de l'intégrande défectueux**. C'est cohérent avec P39, qui a
fermé la frontière (F3) dans le domaine variationnel avec l'intégrateur
reconstruit. Le verdict initial reste dans l'historique git (addenda
seulement) ; le JSON corrigé porte la note F9.

## 5. Chaîne documentaire

`SHASUMS.txt` régénéré sur l'arbre complet du dépôt (343 fichiers +
4 assets de release). Registre A4 : F9 → **fermée** ; le comptage passe
à 6 fermées / 4 ouvertes / 5 partielles. A5 réévaluée (F9 est
hors-domaine ddll — pas d'effet sur la conjecture).

*Réparation publiée comme B3-FAIL d'hygiène : le défaut, sa mesure et sa
réparation sont dans le dépôt, pas dans une corbeille.*
