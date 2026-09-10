# Campagne E56-x — extension de robustesse (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 (`7fa7f2c7…d9f07e`) —
aucune donnée de campagne n'existe. Staging local.**

- **Objet** : robustesse du SUCCÈS formel d'E56 (falsifieur de la loi T6) ;
- **Motivation** (note de marge d'E56) : 1 run, enroulements au seuil,
  disparition à t=90 — mesurer la robustesse sans re-seuiller ;
- **Design gelé** : 24 graines nouvelles (550101–550124, déclarées ;
  440204 reste historique) ; bras appariés A (sans ancrage, = E54-C à la
  nouvelle taille) / B (ancrage des chapeaux, = E56 inchangé) ; marge
  d'enroulement (|w|−0,5) enregistrée par paire ; persistance mesurée
  séparément à t=45 et t=90 ;
- **Niveaux de verdict gelés** : ROBUSTE (≥3/24 à t=45 en B et marge
  médiane ≥ 0,1, i.e. |w| ≥ 0,6 — figé avant calcul) ; CONFIRMÉ_FAIBLE
  (≥1/24, en deçà des bornes — statut E56 inchangé) ; RÉFUTÉ (0/24 — la
  corroboration E56 était un épiphénomène ; loi T6 réfutée à 24 graines,
  publiée au même niveau) ;
- Harnais : `src/e56x_run.py` (`a0eb120f…309258`), validé
  en --smoke.

## Artefacts (staging local)

- `e56x_protocole.json` — gelé, haché `7fa7f2c7…d9f07e`
- `src/e56x_run.py` — `a0eb120f…309258`
- `src/e44_core.py` — filiation byte-identique `604c2232…60ae1ac7`
- empreintes complètes : `SHASUMS_local.txt`

## Verdict — 09/09/2026 (exécution locale) : CONFIRMÉ_FAIBLE

**Les niveaux gelés prononcent CONFIRMÉ_FAIBLE** (≥1/24 mais sous les
bornes de robustesse) — et la lecture fine affine : l'effet d'ancrage
mesuré en E56 **ne se réplique pas au-delà du niveau du témoin**.

### Mesures (24 graines nouvelles, bras appariés)

| | A (sans ancrage) | B (ancré) |
|---|---|---|
| Nucléation du tressage | 18/24 | 22/24 |
| Persistance t=45 | 1/24 | 1/24 |
| Persistance t=90 | 1/24 | 0/24 |
| Marge médiane des braises persistantes | — | 0,052 (\|w\| ≈ 0,55) |

- P0 : PASS (médiane du compte axial B = 15,0 ∈ [9,19]) ;
- ROBUSTE : non (il fallait ≥3/24 à t=45 et marge ≥ 0,1) ;
- RÉFUTÉ : non (il fallait 0/24 — le plancher est à 1/24, pas à zéro).

### Lecture (déclarée)

1. **La nucléation de la relation est facile sous rotation** : 18–22/24
   graines produisent des tresses — la rotation organise la naissance de
   la relation discrète (contraste fort avec le lien de Hopf en trempe
   libre : 5/24) ;
2. **La persistance est au plancher (~4 %) et indiscernable entre bras** :
   l'ancrage des chapeaux n'est pas le facteur opérant à cette taille
   d'échantillon — la clause « ∧ ancrage » de la loi T6 n'est pas soutenue
   par cette mesure (B = A = 1/24) ;
3. La loi T6 n'est pas réfutée par son falsifieur (le seuil de réfutation
   gelé était 0/24) — elle reste « corroborée faiblement », et la clause
   d'ancrage est marquée **non soutenue** dans la note.

### Frontière (datée)

La relation discrète naît abondamment sous rotation et persiste au
plancher (~4 %), sans facteur mécanique mesuré à cette échelle. La
conservation robuste de la relation reste ouverte — candidats déclarés :
cristallisation (réseau ordonné, pas seulement ancrage des pieds — le
précédent R4b est un réseau, pas des pieds) ou contrôle actif hors-GP.
