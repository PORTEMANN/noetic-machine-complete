# Note P44 — EEG-MI-REEL : la chaîne lit-elle l'intention motrice ?

**Patrice Portemann — Machine Noétique**
31 août 2026 — réponse mesurée à la question « drone piloté par la pensée »

## 1. Objet et discipline

Premier test de la chaîne ASH → M̂ sur de l'**EEG réel d'imagerie
motrice** : BCICIV-2a (BCI Competition IV, dataset 2a — la référence
mondiale du domaine), 9 sujets, 250 Hz, 288 essais/sujet (gauche, droite,
pieds, langue), zip figé SHA-256 `65fe93cb…`, sujets figés
individuellement. S = ASH v1.0.0 figée (copie byte-identique). Règle de
décision **zéro paramètre, zéro calibration, zéro apprentissage** :
asymétrie d'occupation de la bande μ (8–13 Hz, notes 36–44 de la grille)
entre C3 et C4 — l'ERD d'imagerie motrice étant controlatérale.
Artefacts non rejetés (déclaré). **ReN non utilisé** (F16 — occupation
relative, invariante d'amplitude par construction).

## 2. Résultat : les deux règles zéro paramètre sont réfutées

| Règle | Précision moyenne (seuil 0,60) | Sujets significatifs (seuil 5/9) | Verdict |
|---|---|---|---|
| v1 — asymétrie absolue A = o_C3/(o_C3+o_C4) | **0,540** | **1/9** (A03 : 0,771) | RÉFUTÉE |
| v2 — ERD relative à la baseline intra-essai | **0,520** | **0/9** | RÉFUTÉE (addendum pré-enregistré avant exécution) |

**Leviers effondrés comme prévu** (P44-2 tenue) : bande θ 0,479 et
paire postérieure P1/P2 0,514 — ce qui reste de signal vit bien dans la
bande μ et les canaux moteurs. La machine mesure donc proprement : il y
a un effet, mais il est trop faible en essai unique sans calibration.

Le sujet A03 (0,771, p < 10⁻⁹) est lisible — cohérent avec la
littérature de la compétition (meilleur sujet du dataset) : **l'«
illettrisme BCI » est mesuré par la chaîne**, pas seulement cité.

## 3. Réponse à la question du drone

**Non, pas aujourd'hui, pas à zéro paramètre en essai unique** — et c'est
désormais un résultat publié avec falsifieur, pas une opinion. La voie de
fermeture est mesurée et déclarée (registre F17) :

1. **Agrégation d'essais** : si le signal existe (A03 le prouve), voter
   sur N essais fait croître la précision en √N — pilotage *lent*
   (une commande par 5–10 s) mais honnête ;
2. **Baseline sujet figée comme D** : la signature de repos du sujet
   devient une donnée de référence déclarée (conforme C12.1 — une
   donnée, pas un paramètre fitté) ;
3. **Filtrage spatial dérivé** : CSP est ajusté sur données — interdit ;
   une variante structurelle (combiner C3/C4/CP3/CP4 par règle d'anatomie
   déclarée) reste à dériver.

Le casque noétique reste pertinent (O(1) embarqué mesuré, verdict (V, Σ)
qui *refuse* de commander quand Σ chute — la sécurité structurelle que
le ML embarqué n'a pas) — mais la lecture fine de l'IM 4-classes
exige la fermeture de F17.

## 4. Effet de bord obligatoire (conséquence de F16)

Le benchmark figé de `noetic-ash` classait « EEG intention → Quantique
(ReN ≈ 41) ». ReN étant réfuté comme invariant d'échelle (P43/F16),
cette classification n'est **pas portable** entre sujets ou gains :
rejouer les benchmarks EEG du dépôt sur invariants normalisés est une
suite déclarée.

## 5. Artefacts

`p44_eeg_mi_reel.py` (sha `c305614e…`) ·
`p44_eeg_mi_reel_verdict.json` · dataset BCICIV-2a (zip SHA
`65fe93cb…`, sujets SHA publiés dans le verdict ; données externes non
commitées — même politique que `noetic-ash/benchmarks`).

**Verdict P44 : PARTIEL 2/3 — P44-1 réfutée (B3-FAIL publié), leviers
tenus, F17 ouverte avec coût de fermeture exact.**
