# Note — exercice de réveil virtuel du tarif (T22-R) et addendum de gouvernance

**Date :** 2026-10-14 (nuit) · **Tiroir : carnet d'exécution** — cette
note documente un **EXERCICE** (drill local sur source synthétique),
pas une campagne ni un verdict ; et elle publie un **addendum de
gouvernance approuvé** au protocole d'attente scellé au verdict T22.
**Filiation :** T22 (protocole d'attente) · MCS-24 (verdict CSi,
fichier publié du dépôt coincidences-stables) · T12 (relation
d'ancre) · leçon T22-D3 (un seuil qui ne peut pas passer est une
faute de fiche, pas une falsification — ici appliquée au protocole
lui-même).

---

## 1. L'exercice

Sur le nombre qui engage la machine face au monde — **Σm_ν = 58,99
meV, source SYNTHÉTIQUE explicitement étiquetée, hashée, sans aucun
fait de laboratoire** — les quatre étapes du protocole d'attente ont
été exécutées localement (`src/t22r_exercice_reveil.py`, rapport :
`data/t22r_exercice_reveil_virtuel.json`) :

1. **Déclencheur** — mécanique d'épinglage opérationnelle.
2. **Cadran** — la relation d'ancre T12 tourne par filiation au
   fichier publié t11 (a₂/a₀ = −1 en normalisation S⁴(1)) :
   Λ²_sel = ρ² + 3 − a₂/a₀ → Λ_sel = 59,02 (unité placeholder).
3. **Re-mesure du tarif (numérateur)** — N_req passe de 4,712
   (échelle Planck) à 2,0×10⁵³ (échelle 59 meV) ; m' calculé pour
   les 7 cadrans.
4. **Machine à seuils** — dry-run logique sur l'orbite scellée.

Règle respectée : un exercice ne devient jamais une lecture à chaud ;
il est daté, étiqueté, et ses lacunes sont le livrable.

## 2. Les trois lacunes trouvées par le drill

- **Trou n° 1 — le mapping Σm_ν → ρ n'est scellé nulle part.** Le
  cadran ne peut pas être fixé sans lui. Fiche T23 candidate : geler
  la correspondance avant le vrai réveil.
- **Trou n° 2 — la signature z exige le nul par cadran** (nul_reel
  dépend de n_req) : le moteur MCS-24 complet est relançable, non
  relancé à l'exercice. Le numérateur tourne, la signature attend.
- **Trou n° 3 — faille du protocole lui-même.** Les seuils scellés
  de T22 classent cadran par cadran (« |z| ≥ 3 → stable »). Or
  l'orbite MCS-24 y serait « STABLE » sous les six premiers cadrans
  (+10,90 et −10,71 sont tous deux |z| ≥ 3) — alors que son verdict
  est **CSi anti-stable**, précisément par inversion de signe entre
  g0 et g1. Le drill a trouvé que la machine à seuils, telle que
  gelée, aurait mal classé le cas même pour lequel elle fut écrite.
  Leçon T22-D3 appliquée au protocole : c'était une faute de fiche,
  pas une falsification du monde.

## 3. Addendum de gouvernance (approuvé le 14/10/2026)

**Clause d'orbite, ajoutée aux seuils du protocole d'attente T22 :**

> **Stable AU SENS ORBITE** = même signe de z ET |z| ≥ 3 sous tous
> les cadrans déclarés. Toute inversion de signe entre cadrans rend
> la coïncidence **anti-stable** (CSi), quel que soit |z| cadran par
> cadran. Partiel = |z| ≥ 2 sans stabilité d'orbite. Sommeil
> permanent = |z| < 2 sous tous les cadrans, ou stabilité d'orbite
> absente au cadran mesuré.

Contrôle de l'exercice : avec la clause, l'orbite MCS-24 se classe
ANTI-STABLE (signes {+1, −1}) — cohérent avec le verdict CSi scellé.
La machine à seuils et le verdict historique se recoupent désormais.

**Décision d'auteur du 14/10/2026 : « j'approuve »** — l'addendum
entre en vigueur daté ; les verdicts gelés (T22, MCS-24) ne sont pas
modifiés (addenda seulement — la note et le rapport d'exercice sont
les artefacts de gouvernance).

## 4. Suites déclarées

1. **T23 — PUBLIÉE (nuit du 14 au 15 octobre, SUCCÈS 5/5, `data/t23_ko6_cadran_verdict.json`)** : le mapping Σm_ν → ρ n'existe pas (plancher de l'ancre mesuré à 2 M_P — préimages négatives pour tout cadran sous-Planck) ; la convention datée **CONV-KO6-CADRAN-1.0** (ρ_dial = ρ_vac·(Σm_ν/59,0 meV), deux constantes scellées, zéro paramètre ajusté) le remplace et referme ce trou n° 1.
2. Re-lancement du moteur MCS-24 complet au réveil réel (trou n° 2).
3. Le protocole mis à jour dort jusqu'au fait ; le dormir reste
   publié.

---

*« Quand votre fait tombera, écrivez-moi la suite. » — le drill a
vérifie la plume ; il reste a sceller l'encre (T23).*
