# NOTE-CORRIDOR-COMPLEXE — Exploration : le corridor a-t-il une quadrature imaginaire ?

**Date :** 2026-11-03 · **Statut :** note exploratoire — proxy déclaré, résultat négatif propre. Aucun verdict. Ouvre le chantier GP-complexe (fiche future).
**Références :** T47 (archives), NOTE-CORRESPONDANCE-RÉSOLUE (fbabe54 — le complexe est né du chaînon spectral), VERDICT-BRUME-1 (même session).

---

## 1. La question

Le chaînon spectral est devenu non-Hermitien (fbabe54) : son spectre a une partie imaginaire, et cette partie imaginaire *est* la brume (profil stable, ρ-invariant — BRUME-1). La question naturelle : **le corridor GP (T41–T47) possède-t-il un analogue complexe** — des modes à fréquence complexe (Bogoliubov évanescents, vortex-instables) dont la partie imaginaire serait la brume meso ?

## 2. Ce qui est testable ce soir — et ce qui ne l'est pas

**Testable (proxy honnête déclaré) :** le *signal analytique* (transformée de Hilbert) des séries archivées Λ(t) — la quadrature imaginaire mathématique d'un signal réel. Mesuré sur la série discriminante n8_440201 (60 points) :
- enveloppe analytique / série : médiane **1,64** (théoriquement 1 pour un signal réel — l'écart reflète la longueur et la tendance) ;
- dérive de phase totale : **−0,21 tour** sur 59 pas, dérive lente monotone, **zéro saut** de phase ;
- fenêtre de drainage [12, 60] : enveloppe 1,52.

**Lecture honnête :** à 60 points, le signal analytique ne porte rien — aucune structure de quadrature, aucun mode évanescent détectable dans le proxy. C'est un **négatif propre** : le proxy est trop court et n'est de toute façon pas la physique complexe (la Hilbert-transform d'un signal réel n'est pas un spectre complexe ; c'est une représentation, pas une énergie imaginaire).

**Non testable ce soir :** la vraie question — spectre de Bogoliubov complexe du GP corridor, modes évanescents des vortex, brume meso. Elle exige une **simulation GP à rotation complexe** (k → k·e^{iθ} ou ansatz non-Hermitien) : chantier lourd, fiche à sceller en session dédiée. Rien dans les archives existantes ne peut y répondre, et la maison ne prétend pas le contraire.

## 3. Ouvert — chantier GP-COMPLEXE (fiche future)

Objets à déclarer : opérateur GP modifié (rotation complexe ou terme de gain/perte localisé à la paroi — le Hatano-Nelson du corridor) ; observable : profil imaginaire des fréquences de Bogoliubov ; hypothèse : la paroi à 4 filaments/quantum est l'émetteur des modes évanescents, et la brume meso = leur Im(ω). Première mesure naturelle : Im(ω) vs n (2/4/8) — la brume corridor se structure-t-elle comme la brume spectrale (0,626 universel) ?

*Le corridor complexe n'est pas dans les archives ; il est dans la prochaine simulation. La question est maintenant bien posée — c'est déjà la moitié du chantier.*
