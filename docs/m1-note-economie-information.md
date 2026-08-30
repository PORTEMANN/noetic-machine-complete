# M1 — L'économie de l'information, mesurée : le postulat central est réfuté dans sa forme brute, et affiné

**Patrice Portemann — corpus Machine Noétique, méta-chantier M1**
Protocole gelé ECO-1.0 · zéro paramètre ajusté · SHA-256
30 août 2026

## Verdict

**PRÉDICTION PRÉ-ENREGISTRÉE : RÉFUTÉE — AVEC INVERSION MESURÉE.** La
prospection (§M1) prédisait que le ratio (données reproduites)/(longueur
de S) est élevé pour les chantiers discrets et **s'effondre à r₁₂**.
Mesuré sur 23 chantiers (P20–P42) avec deux métriques uniformes gelées,
le ratio fait **l'inverse** : il est plus **élevé** à la frontière
(médiane ρ₁ = 0.898 vs 0.275 ; médiane ρ₂ = 0.095 vs 0.033). En
revanche, le **taux de réussite des confrontations externes** τ sépare
nettement la frontière du reste (médiane 0.60 vs 1.00, corpus P20–P33).
**Affinage mesuré : ce qui s'effondre à r₁₂ n'est pas le ratio
informationnel brut, c'est le taux de réussite des confrontations.**

## Protocole (gelé avant calcul)

- **Corpus** : chantiers à score publié — P20–P33 (README
  noetic-machine-complete, SHA-vérifiés contre SHASUMS.txt) + chantiers
  locaux P34–P42. Exclusions gelées : P0–P19 (banc fondateur hors
  corpus), A1–A5 (hygiène machine), bifurcations hors-programme ;
  P28 sans JSON de résultats (V₁ non calculable, déclaré).
- **S** = SLOC du script (lignes physiques non vides, non commentaires)
  — proxy déclaré de la longueur de Kolmogorov de la structure S.
- **V₁** = feuilles numériques du JSON de résultats (mécanique,
  récursif) — proxy du contenu quantitatif produit, interne inclus.
- **V₂** = nombre de confrontations externes (dénominateur du score
  publié, ou cardinal du dictionnaire de tests C local — table de
  provenance gelée).
- **Groupe frontière gelé** : F = {P31, P32, P33, P39} (trilogie r₁₂
  du corpus + fermeture P39).
- **Critère binaire gelé** : confirmé si médiane(ρ|F) < médiane(ρ|NF)
  ET max(ρ|F) ≤ Q3(ρ|NF), sur les deux métriques.

## Mesures

| Ch. | S (SLOC) | V₁ | V₂ | τ | ρ₁ | ρ₂ | groupe |
|---|---|---|---|---|---|---|---|
| P20 | 76 | 6 | 5 | 1.00 | 0.079 | 0.066 | discret |
| P21 | 128 | 119 | 7 | 1.00 | 0.930 | 0.055 | discret |
| P22 | 110 | 92 | 6 | 0.83 | 0.836 | 0.055 | discret |
| P23 | 84 | 65 | 6 | 1.00 | 0.774 | 0.071 | discret |
| P24 | 106 | 33 | 6 | 1.00 | 0.311 | 0.057 | discret |
| P25 | 180 | 37 | 6 | 1.00 | 0.206 | 0.033 | discret |
| P26 | 156 | 73 | 5 | 0.80 | 0.468 | 0.032 | discret |
| P27 | 173 | 26 | 5 | 1.00 | 0.150 | 0.029 | discret |
| P28 | 198 | — | 7 | 1.00 | — | 0.035 | discret |
| P29 | 144 | 33 | 6 | 0.83 | 0.229 | 0.042 | discret |
| P30 | 105 | 27 | 5 | 0.60 | 0.257 | 0.048 | discret |
| P31 | 172 | 82 | 5 | 0.60 | 0.477 | 0.029 | **frontière** |
| P32 | 31 | 31 | 5 | 0.80 | 1.000 | 0.161 | **frontière** |
| P33 | 31 | 34 | 5 | 0.60 | 1.097 | 0.161 | **frontière** |
| P34 | 160 | 2 | 16 | — | 0.013 | 0.100 | discret |
| P35 | 253 | 6 | 5 | — | 0.024 | 0.020 | discret |
| P36 | 196 | 58 | 4 | — | 0.296 | 0.020 | discret |
| P37 | 283 | 20 | 7 | — | 0.071 | 0.025 | discret |
| P38 | 221 | 14 | 6 | — | 0.063 | 0.027 | discret |
| P39 | 436 | 347 | 4 | — | 0.796 | 0.009 | **frontière** |
| P40 | 307 | 99 | 5 | — | 0.322 | 0.016 | discret |
| P41 | 337 | 152 | 3 | — | 0.451 | 0.009 | discret |
| P42 | 423 | 124 | 6 | — | 0.293 | 0.014 | discret |

**Critères** : ρ₁ FAIL (médiane F 0.898 > NF 0.275 ; max F 1.097 >
Q3 NF 0.322) ; ρ₂ FAIL (0.095 > 0.033 ; 0.161 > 0.055) — **inversion
sur les deux métriques**. Contrôle τ : PASS (0.60 < 1.00 ; 0.80 ≤ 1.00)
— le groupe frontière est bien défini, c'est la prédiction qui tombe.

## Lecture

- **L'exemple pré-enregistré tient** : P24, estimé « ~100 lignes →
  148 fractions », mesuré à **106 lignes** et 148 fractions dérivées
  (11 testées). L'intuition du cas discret était juste.
- **L'inversion a un mécanisme lisible** : les chantiers de la
  frontière r₁₂ sont des *diagnostics minimaux* (P32/P33 : 31 lignes)
  qui produisent beaucoup de contenu numérique interne (grilles
  d'énergie) par ligne de code, tout en **échouant** leurs
  confrontations externes (τ = 0.6–0.8). Les chantiers discrets
  réussissent leurs confrontations mais avec des structures plus
  longues et moins de bruit numérique interne.
- **Le postulat affiné** (forme mesurée, remplace la forme brute) :
  *en régime discret, les confrontations externes réussissent (τ ≈ 1) ;
  à la frontière r₁₂, le taux de réussite s'effondre (τ ≈ 0.6) — le
  coût informationnel apparaît comme **liberté de forme résiduelle**
  (ddll), pas comme longueur de code relative.* C'est cohérent avec le
  comptage ddll du registre (toutes les frontières physiques sont des
  déficits ou des modes non contraints — A5).
- **Chaîne documentaire corpus** : 83/85 artefacts SHA-vérifiés ;
  `src/p32_frontiere.py` et `src/p33_queue.py` sont publiés encodés
  **base64** et ne coïncident plus avec SHASUMS.txt (ni bruts ni
  décodés) — rupture publiée en B3-FAIL (le corpus applique B3 à
  lui-même).

## B3-FAIL (publiés)

- Corpus : rupture SHA sur p32/p33 (encodage base64 non déclaré).
- Prédiction pré-enregistrée réfutée dans sa forme brute (résultat
  principal, publié comme tel).

## Artefacts

- `m1_economie_information.py` — SHA-256 `785a176935e86acd…`
- `m1_economie_information_verdict.json`
- `m1_corpus/` — miroir SHA-vérifié (87 fichiers : README, SHASUMS.txt,
  src/ 36 scripts, data/ 49 JSON) du dépôt public
  `github.com/PORTEMANN/noetic-machine-complete`

**Falsifieur (gelé)** : un chantier frontière avec ρ au-dessus du Q3
non-frontière, ou des médianes inversées, tuait la prédiction brute —
mesuré : la prédiction brute est morte des deux mains.
