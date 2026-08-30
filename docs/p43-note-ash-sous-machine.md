# Note P43 — L'ASH sous la machine

**Patrice Portemann — Machine Noétique**
30 août 2026 — le verdict éprouve son instrument d'acquisition

## 1. Objet et discipline

La machine éprouve l'ASH **telle que publiée** (`noetic-ash`, `ash_core.py`
v1.0.0, blob git `c9dd73c2…`, copie figée `data/p43_ash_core_v100.py`,
sha256 `338dbda7…` — aucune retouche ; contrôle de fidélité C6 : le noyau
π-instrumenté au nominal reproduit *exactement* le noyau figé sur toute la
batterie). Les affirmations publiques du README v1.0.0 deviennent des
prédictions pré-enregistrées avec tests tuables. Protocole ASH-MACH-1.0
gelé ; batterie PERT-BATT-1.0 (héritée d'A1) sur 5 axes de protocole.

Le chantier a exigé **deux addenda** (v2, v2.1/v2.2) — chaque échec
intermédiaire est conservé dans le verdict JSON, pas effacé.

## 2. Verdicts sur les affirmations publiques

| # | Affirmation (README v1.0.0) | Verdict mesuré |
|---|---|---|
| A1 | O(1) par fenêtre | **CONFIRMÉE** — temps/fenêtre ×1,1 et mémoire/fenêtre ×1,0 de 8 s à 128 s de signal (critère déclaré < 2) |
| A2 | Zéro paramètre ajusté | **CONFIRMÉE** (structurelle : f0, n_octaves issus de DEFAULTS ou de π déclaré, jamais des données) |
| A3 | Invariants interprétables | **CONFIRMÉE À RÉSOLUTION SUFFISANTE** — v1 : 6/8 attentes tenues au nominal ; v2 (haute fréquence) : 2/2 |
| A4 | ReN discriminant de régime | **RÉFUTÉE comme invariant physique** (pré-enregistré) : balayage d'amplitude à signal inchangé → **2 franchissements de seuil de régime**, pente log-log ReN∝A mesurée **−0,996** (théorie : −1) |
| A5 | Résolution de grille 2^(1/12) ≈ 5,9 % | **AFFINÉE** — résolution effective = max(5,9 %, (fs/nperseg)/f) : la claim grille seule est réfutée à basse fréquence, confirmée à f ≫ fs/nperseg |
| A6 | Fonctionne sur données réelles | **CONFIRMÉE** sur peigne de spikes (Allen, cellules figées P41) |

## 3. B3-FAIL publiés (la machine ne s'épargne pas)

1. **Prédictions v1 S2/S3 réfutées** : l'accord tempéré basse fréquence
   (4 notes à 41 % d'écart) donne Rtop=3 au lieu de 4 — la résolution
   **Welch (fs/nperseg = 1 Hz) borne la résolution effective**, pas la
   grille. Conséquence mesurée forte : une série harmonique vraie
   (2,4,6,8 Hz) est lue comme sa sous-série d'octaves — **parfaitement
   consonante (Rdyn=0)** — par absorption des harmoniques non résolues.
2. **Levier v1 invalide** (conception) : la paire basse fréquence est
   séparable sans Rdyn — publié ; le levier v2 haute fréquence tient
   (inséparable sans Rdyn, séparable avec — **Rdyn est constitutif** de
   la classe accord/harmonique).
3. **C5 v2.0** : deux défauts d'encodage de ma part (rate native 200 kHz
   lue comme 500 Hz ; décimation d'un peigne creux par sous-échantillonnage
   direct) — publiés.
4. **Limite de lisibilité mesurée** : une paire de spikes n'a pas de
   porteuse spectrale (pic aléatoire). L'ASH exige un train.

## 4. Résultat physique non anticipé

Sur les cellules Allen figées : la porteuse spectrale du peigne de spikes
est l'**inverse de l'ISI médian**, pas le taux moyen n/T — type I : 11,6 Hz
(note 43 lue vs 42,4 attendue) ; type II : 46,9 Hz (note 67 vs 66,6). La
cellule type II a un train d'apparition **non stationnaire** (bursts à
~21 ms entrecoupés de pauses de 155/320 ms) : son taux moyen P41 (26 Hz)
et sa porteuse ISI (48 Hz) diffèrent d'un facteur ~2 — mesuré, publié.

## 5. Stabilité de protocole (PERT-BATT, 11 protocoles)

Σ = 1,00 partout sauf : S1 (Σ=0,91, fragile sous nperseg=128), S4 bruit
(Σ=0,82, fragile sous f0=0,5 et n_octaves=4) — fragilités publiées avec
axes responsables. C0 : deux exécutions, (V, Σ) identiques.

## 6. Conséquence registre

Nouvelle entrée **F16-REN-REGIME** (méthode, partielle) : ReN n'est pas un
discriminant de régime physique sans normalisation d'amplitude déclarée.
Falsifieur : un ReN normalisé, invariant d'échelle, conservant la
séparation des régimes sur la batterie P43 ferme l'entrée.

**Verdict P43 : SUCCÈS 7/7** — l'instrument passe sous le verdict, avec
ses limites mesurées et publiées.

## Artefacts

`p43_ash_sous_machine.py` (sha `a834ff0c…`) ·
`p43_ash_sous_machine_verdict.json` · `p43_ash_core_v100.py` (S figée) ·
NWB Allen : release `artefacts-donnees-v1.0` (empreintes SHASUMS).
