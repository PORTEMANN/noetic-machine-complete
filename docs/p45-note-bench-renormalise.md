# Note P45 — Benchmarks EEG renormalisés

**Patrice Portemann — Machine Noétique**
31 août 2026 — conséquence obligatoire de F16 (ouverte par P43)

## 1. Objet

La table figée des benchmarks de `noetic-ash` (juin 2026) classait les
signaux par ReN/régime (« EEG intention → Quantique, ReN ≈ 40,4 »). ReN
étant réfuté comme invariant d'échelle (P43-C3 : pente −1, franchissements
de régime à signal inchangé), P45 rejoue les benchmarks sur invariants
**normalisés** (Rtop, Rdyn, E1..E7 — invariants d'amplitude par
construction) et mesure ce qui survit.

Données : les 5 CSV régénérés **bit-à-bit** par les générateurs seedés
(graine 42) et vérifiés contre `benchmarks/SHASUMS.txt` — 4/4 empreintes
figées conformes (`228c6155…`, `d25d65f9…`, `bb20c04d…`, `375d649e…` ;
la sinusoïde n'avait pas d'empreinte figée — déclaré).

## 2. Résultats

### C2 — ReN non portable : confirmé et mécanisé
- Pente −1 **exacte** pour les signaux à entropie non dégénérée (ECG :
  ReN·A = 0,5895 constant à 7 chiffres sur A ∈ [0,01 ; 100]).
- **3/5 signaux franchissent un seuil de régime** à signal inchangé
  (ECG : Cosmologique → Quantique ; moteur défaillant et EEG :
  Quantique → Cosmologique).
- Mécanisme de saturation mesuré sur la sinusoïde (entropie dégénérée
  H ≈ 0) : le double plancher ε de la formule (`Rc·(H+1e-8) + 1e-8`)
  borne ReN à ≈ 10¹⁰ — la pente −1 n'est plus pure. Détail
  d'implémentation publié.
- Invariants normalisés : stables à **1e-9** sur tout le balayage.

### C3 — la classification survit sans amplitude
**10/10 paires de signaux séparées** par au moins un invariant normalisé
à intervalles inter-fenêtres disjoints (souvent 4–7 invariants
disponibles). Le classement des 5 signaux du benchmark **ne dépend pas de
ReN** — c'est le résultat central : la valeur du benchmark tient, son
étiquette de régime tombe.

### C4 — EEG intention : deux mesures
- **Grille figée (4 octaves, max 15,1 Hz)** : ma prédiction « bouffée β
  strictement invisible » est RÉFUTÉE — la fuite des lobes de Welch élève
  les notes hautes : l'intention est visible par un **canal parasite**
  (Rdyn bascule, écart max = 1,00). Publié.
- **Grille étendue (n_octaves=5, déclaré)** : la bouffée β devient
  lisible en propre — plan E5 ×3,66 pendant [4,7] s, pic dominant à la
  note 52 (20,2 Hz) dans 3/4 fenêtres (la fenêtre [6,8] s ne couvre
  l'intention qu'à moitié — justification déclarée).

### C1 — B3-FAIL de reproductibilité de l'archive
La table figée de juin 2026 n'est reproduite à tolérance par **aucun**
des deux pipelines publiés (fenêtre classe 1–2 s ; fenêtre 256 éch./hop
128), sauf *moteur_sain* (fenêtre classe ✓ : 1,099 vs 1,107 figé). Les
valeurs de juin 2026 proviennent d'une pipeline non figée. Publié comme
B3-FAIL d'archive — entrée **F18** au registre (hygiène, ouverte ;
coût de fermeture : re-figer la table avec le pipeline v1.0.0 déclaré).

## 3. Conséquences pour `noetic-ash`

1. Retirer ReN/régime des classifications publiées (ou fermer F16 par un
   ReN normalisé en amplitude, validé sur la batterie P43) ;
2. La classification par invariants normalisés tient (10/10) — elle peut
   être promue comme la classification officielle du benchmark ;
3. Étendre la grille EEG à 5 octaves si la bande β est visée (la grille
   figée à 4 octaves ne la voit pas en direct) ;
4. Re-figer la table de juin 2026 (F18).

**Verdict P45 : PARTIEL 3/4** — C1 publié comme échec de reproductibilité
de l'archive ; C2, C3, C4 tenus.

## Artefacts

`p45_bench_renormalise.py` (sha `99eb7870…`) ·
`p45_bench_renormalise_verdict.json` · CSV régénérés (empreintes dans le
verdict, conformes au SHASUMS de noetic-ash).
