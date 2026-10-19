# Note de consolidation — l'arc Vinen (T47–T51)

**Date :** 2026-10-19 · **Tiroir :** carnet — note de consolidation
(n'ajuste aucune carte gelée ; les verdicts restent la référence
`data/tNN_*.json`, empreintes auto-citées).
**Campagnes consolidées :** T47 (la loi), T48 (le coefficient), T49 (le
pont chiffré), T50 (la production), T51 (la loi d'échelle).
**Filiation :** corridor E (protocole B, graines officielles) · T41–T46
(les entiers topologiques, de l'hopfion au tangle) · Vinen (1957) comme
prédiction ancêtre — citée, jamais invoquée avant le verdict.

---

## 1. Ce qui est mesuré

L'équation de Vinen côté corridor, terme par terme, sans paramètre
ajusté dans l'arc :

| Pièce | Campagne | Mesure |
|---|---|---|
| Existence de la loi | T47 | décroissance algébrique 1/Λ affine (R² = 0.930 à n = 8) — **fait de régime** |
| Le coefficient | T48 | β̂ ≈ 1.4e-5 unités corridor, constant en n, reproductible à 27 % à n = 8 |
| Dissipation | T49 | β̂Λ² prédit la décroissance : rapport médian 1.3 (n = 8, deux graines) ; 12.4 à n = 2 (pont mort) |
| Production | T50 | injection murale I mesurée : I/β̂Λ∞² = 1.0–1.5, **même pendant le remplissage** |
| Équilibre | T51 | Λ∞(n) = √(I(n)/β̂) tombe sur les plateaux à **0.8–22 %** (1143 vs 1133 à n = 8/440201) |

La loi d'échelle complète : production monotone en n (6.4 < 9.5 < 18.9),
plateaux monotone (466 < 750 < 1133), prédiction et mesure dans le même
ordre, à deux graines.

## 2. La frontière — la leçon répétée trois fois

Trois campagnes ont testé la loi là où elle devait se taire, et trois
fois la mesure a tenu le même langage :

> **Hors de son régime, la loi ne devient pas faible — elle cesse
> d'être.**

- T47 : R²(1/Λ) = 0.007 à n = 2 (contre 0.930 à n = 8) — la signature
  algébrique disparaît sous l'épinglage mural ;
- T48 : β̂ « négatif » à n = 2 avec R² ≈ 0 — pas une dissipation
  négative, une absence de drainage ; à n = 4, une graine draine et
  l'autre non (régime mixte) ;
- T49 : le pont chiffré s'effondre à n = 2 (rapport 12.4) — exactement
  à la frontière tracée par T48.

Corollaire pratique gravé (T48-D1, T50-D2) : la balance
|I − D|/(I + D) est un critère **d'atteinte du plateau**, non une
condition de la loi — la production obéit à β̂Λ∞² avant l'équilibre.

## 3. L'équation, écrite avec les nombres du corridor

```
dΛ/dt = I(mur)  −  β̂·Λ²        (β̂ = 1.1–1.8e-5 selon graine, n = 8)

au plateau :  Λ∞ = √(I/β̂)      (vérifié à 0.8–22 % sur 3 runs valides)
```

Le mur parle le quantum (production ∝ forçage, T47 : 4 filaments par
quantum), la dissipation garde le silence (β̂ constant en n, T48), et
l'équilibre des deux fixe la densité (T51). C'est la mécanique
statistique du désordre contraint, mesurée pièce par pièce.

## 4. Questions ouvertes (honnêteté de la consolidation)

1. **La production α(v).** I est mesuré phénoménologiquement (sauts de
   Λ). L'origine microscopique — le taux de nucléation au mur en
   fonction du quantum — n'est pas encore décomposée. La fenêtre est
   ouverte (comptage des nucléations vs croissances).
2. **La dissipation inter-graines à n = 8** diverge dans la fenêtre
   (facteur 5.6, T50-D2) — sensibilité transitoire du remplissage ; à
   refaire à t > 90 si un jour la fenêtre s'allonge.
3. **Le drainage lent de n = 2** (balance 0.18, dissipation qui dépasse
   légèrement l'injection) mérite une fenêtre plus longue : le régime
   épinglé a peut-être sa propre loi, plus discrète.

## 5. Gouvernance

Cette note consolide, elle ne scelle rien : les verdicts T47–T51
restent la référence. Adoption proposée : mention « arc Vinen clos »
dans la doctrine continue (déjà consignée le 19/10/2026) et renvoi
depuis la carte du pont φ. La confrontation au réel (turbulence
superfluide, données de tangles) reste en réserve sous la règle T25 —
jamais « vrai », toujours « S+ (compatible, avec réserve) » quand elle
viendra.

**Leçon de l'arc, pour les campagnes futures :** une loi ne se
mesure pas seulement où elle parle — elle se mesure surtout où elle se
tait. Trois tests de frontière valent un ajustement.
