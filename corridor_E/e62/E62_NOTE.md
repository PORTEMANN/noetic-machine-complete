# Campagne E62 — fenêtre longue (LOCALE, exécutée le 09/09/2026)

**Protocole E62-FENETRE-1.0 (gelé, haché `3d66da70…6651000`).**

## Verdict : B3-FAIL — l'équilibre fuit lentement ; la marge d'E61 était bien un signe

- T0 : PASS (instrument, seuils d'E60/E61 inchangés) ;
- Bras A (témoin libre) : gonflement continu — rms 12,0 → 21,47 (t=180),
  échappement 44,97 — reproduction étendue d'E60 ;
- Bras B (confiné) : la clause de rms tient **jusqu'à t=180** (17,085 ≤
  18, figé) MAIS l'échappement franchit la borne entre t=90 (22,83) et
  t=135 → échappement max 30,75 > 24 → **P1 FAUX → B3-FAIL** au sens de
  la règle gelée.

## Lecture (déclarée)

L'équilibre souffle/pression n'est pas une fenêtre de passage mais n'est
pas non plus l'éternité : **le cœur de la cage tient (rms dans sa clause
à t=180), la périphérie fuit** (l'anneau le plus externe franchit la
borne d'échappement entre t=90 et t=135). La note de marge d'E61 (bornes
à 82 % et 95 % à t=90) était le signe d'une dérive lente, mesurée et
publiée au même niveau. La structure est **métastable à κ=0,05** : noyau
stable, peau qui fuit. Toute variation de κ relève d'un amendement haché
ou d'une nouvelle fiche — jamais d'ajustement post-échec.
