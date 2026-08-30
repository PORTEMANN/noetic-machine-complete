# P40 — Z_max : où finit le tableau périodique ?

**Patrice Portemann — corpus Machine Noétique, chantier P40**
Protocole gelé ZMAX-1.0 · zéro paramètre ajusté · SHA-256
30 août 2026

## Verdict

**CONFRONTATION RÉALISÉE — 2/5 prédictions tranchées.** Le chantier a
confronté les cinq prédictions gelées du corpus koilon-scale-e8
(22 août 2026) aux masses mesurées (AME2020) et aux rendements évalués
(JEFF-3.1.1). Une prédiction est **réfutée**, une est **cohérente sans
contradiction mesurée**, trois restent hors de portée des masses.

## Mesures

- **C1 — recompute exact de la limite causale.** Avec les formules
  gelées c_s(Z) = α_K·c·√(2^(Z/12)·Z^(2/3)), α_K = 2⁻¹⁰ : le plus grand
  Z avec c_s ≤ c est **Z_max = 180** (marge 0.19 %, excès à Z = 181 de
  2.9 %). Le corpus annonçait « ≈ 179 » : le « ≈ » tient, l'exact est
  180. N_modes = 12·log₂(1/α_K) = 120 = racines positives de E₈ ✓.
- **C2 — contrôle instrument (obligatoire).** Sur AME2020 expérimental
  seul, le gap protonique médian g(Z) = med_N δ₂p retrouve **les cinq
  magiques connus {8, 20, 28, 50, 82}** comme maxima locaux —
  l'instrument est validé avant de trancher quoi que ce soit d'autre.
- **C3 — région superlourde.** Z = 100–116 : gaps de 1.3–2.4 MeV,
  essentiellement sur valeurs **estimées** AME (le '#' est distingué) ;
  aucun maximum local mesuré à Z = 114 — la « coquille 114 » n'est pas
  visible dans les masses expérimentales.
- **C4 — frontière « dernière coquille ».** Les modèles publiés (table
  gelée D3 : mac-mic Möller FRLDM → 114 ; RMF Bender et al. → 120 ;
  RCHB Zhang/Meng → 126 ; table étendue Pyykkö → 168) placent la
  dernière coquille fermée dans **[114, 168]**, tous **sous** la limite
  causale koilon 180. La limite causale et la frontière de coquille sont
  deux objets distincts, et ils sont **cohérents**.
- **C5 — P-FISSION : RÉFUTÉE.** Rendements indépendants thermiques
  JEFF-3.1.1 (U-235, Pu-239) : **0/8 pics secondaires** aux positions
  gelées A ∈ {63, 110, 126, 173} (critère : maximum local strict après
  lissage 5 points + proéminence ≥ 1 % du maximum global). A = 63 et 173
  sont hors couverture ou en queue monotone ; A = 110 et 126 montrent des
  proéminences sous le seuil (max 10 % pour Pu-239 à A = 110, mais pas
  de maximum local). La paire complémentaire (63, 173), (110, 126) =
  U-236* n'est pas réalisée dans les rendements évalués.
- **C6 — diagnostic grille 2^(1/12).** Écarts au demi-ton entier pour
  les magiques consécutifs : [0.14, 0.17, 0.04, 0.44] — trois paires
  proches de la grille, la paire 50→82 à 0.44 demi-ton. La gamme koilon
  décrit les ANU de la Chimie Occulte ; sur les **coquilles mesurées**,
  l'accord est partiel.

## B3-FAIL (publiés)

1. **Corpus — P-FISSION réfutée** : les pics secondaires prédits à
   A = 63, 110, 126, 173 n'existent pas dans JEFF-3.1.1 (indépendant
   thermique, critère gelé). Publié tel quel.
2. **Chantier v1** : le contrôle B(²⁰⁸Pb) était codé sur une valeur
   littérature (1636.446 MeV, liaison nucléaire) au lieu de la convention
   atomique du fichier — l'écart de 16 keV est la **liaison électronique**
   totale du plomb. Corrigé avant gel : auto-contrôle interne au fichier
   (B recomputé vs colonne BINDING/A, même convention, tolérance 20 keV).

## Statut des cinq prédictions

| Prédiction | Statut après P40 |
|---|---|
| P-Z-MAX (rien de stable au-delà de Z ≈ 179) | confrontée — cohérente, pas de contradiction mesurée ; exact = 180 |
| P-FISSION (pics à 63, 110, 126, 173) | **réfutée** sur JEFF-3.1.1 |
| P-MASS-EFF (Δm/m ∝ E², indép. de ω) | non confrontable — expérience laser 800/400 nm requise |
| P-ALPHA-VAR (α_T vs redshift) | non confrontable — spectroscopie quasars requise |
| P-KOILON-SON (c_s(0) ≈ 300 km/s) | non confrontable — dispersion des ondes gravitationnelles requise |

## Lecture ddll (A5)

α_K = 2⁻¹⁰ est un input payé — **1 ddll** : la fermeture causale achète
son échelle. Verdict : **déficit**, conforme à A5 v2. Réponse à la
question du programme (« dernière coquille fermée : 126 ? 164 ?
172–179 ? ») : les masses + modèles répondent **[114, 126]** (chimie
étendue : 168) ; la limite causale koilon répond **180** — et ce n'est
pas la même question.

## Artefacts

- `p40_zmax.py` — SHA-256 c6760b9778655f93… (script gelé ZMAX-1.0)
- `p40_zmax_verdict.json` — mesures, verdicts, falsifieurs
- `p40_data_ame2020_mas20.txt` (SHA e8599c6d…), `p40_data_fy235u.csv`
  (SHA 74e0dd81…), `p40_data_fy239pu.csv` (SHA 278ccb0c…)
- Falsifieur pré-enregistré : Z_max recomputé hors {179, 180} tue la
  dérivation ; magiques connus non récupérés tuent l'instrument. Aucun
  n'est survenu.
