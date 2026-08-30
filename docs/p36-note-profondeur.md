# P36 — La profondeur éprouvée : constitutive dès que la tâche itère

**Patrice Portemann — corpus Machine Noétique, chantier P36**
Protocole gelé PROF-1.0 · poids dérivés, zéro apprentissage · SHA-256
30 août 2026

## Verdict

**SUCCÈS.** La profondeur devient constitutive dès que la tâche
**itère** — et la frontière profondeur-minimale vs structure de la tâche
est mesurée par une loi serrée, à construction exacte, sans un seul poids
appris :

| Structure de la tâche | Profondeur minimale | Coût mesuré |
|---|---|---|
| séparation unique (ET) | 1 (contrôle P34) | — |
| itération finie : parité n bits | 2 | n unités cachées entières dérivées |
| composition d'ordre m : oscillations | m (largeur 2) | 2m unités — contre 2^m en profondeur 2 |

## Mesures

- **C1 — contrôle P34** : ET séparable en profondeur 1, XOR non (LP
  infaisable) — la frontière F1 est reproduite par la machine étendue.
- **C2 — parité** : la profondeur 1 est impossible (LP infaisable,
  n = 2..4 vérifié) ; la profondeur 2 est exacte avec la construction
  dérivée h_i = 1{Σx ≥ i − ½}, sortie alternée Σ(−1)^{i+1}h_i — poids
  entiers, vérifiée sur les 2^n points, n = 2..8.
- **C3 — oscillations (Telgarsky)** : le réseau profond dérivé
  t(x) = 2·relu(x) − 4·relu(x − ½), composé m fois (2 unités par couche),
  reproduit t^m **exactement** sur la grille déclarée de 100 001 points,
  m = 1..8. En profondeur 2, la loi serrée **w_min = 2^m** est mesurée
  par construction exacte (m = 1..5) : les 2^m transitions de
  t^m(x) ≥ ½ aux demi-dyadiques (2j+1)/2^{m+1} exigent un saut par
  transition.
- **C4 — séparation exponentielle** : ratio des coûts 2^m/2m, mesuré à
  16 pour m = 8, doublant par couche ajoutée. La séparation de Telgarsky
  est reproduite **sans apprentissage** : ici elle n'est pas un théorème
  cité, c'est une construction exécutée.

## B3-FAIL du chantier (publiés)

1. **Loi v1 réfutée par la construction** : « 2^m − 1 sauts aux dyadiques
   k/2^m » — faux : les transitions de t^m ≥ ½ sont aux demi-dyadiques
   (2j+1)/2^{m+1}, au nombre exact de 2^m. Loi corrigée et serrée.
2. **Convention de frontière** : le saut descendant inclusif échouait sur
   exactement 1 point de grille (x = 19/32, m = 4) — le point-frontière
   exact appartient au plateau haut (convention ≥ de la tâche). Corrigé :
   saut ascendant inclusif, descendant exclusif.

## Ce que le chantier apprend

La lecture ddll (conjecture A5) : la fermeture paie en degrés de liberté,
avec deux monnaies mesurées — **composition** (m couches × largeur 2 :
réutilisation des coordonnées, coût 2m) ou **copie** (1 couche × largeur
2^m). Le déficit se paie en réutilisation ou en exponentielle. Entrée
registre F12 (partielle — la loi complète reste à cartographier pour les
symétries et périodes non dyadiques) ; A5 inchangé : v2 couvre **8/8**
points du domaine déclaré.

Connexion directe avec P34 (le neurone formel) et prélude à P38
(l'attention : qu'est-ce qui est constitutif dans un bloc minimal ?) et à
M1 (économie de l'information : le script du réseau profond coûte O(m)
symboles là où le réseau peu profond en coûte O(2^m) — la profondeur est
une compression).

**Falsifieur.** Tout réseau de profondeur 2 et largeur < 2^m exact sur la
tâche à m oscillations tue la loi ; toute séparation LP de la parité tue
C2.

## Artefacts

- `p36_profondeur.py` — SHA-256 `ab7b0217086e92f8…`
- `p36_profondeur_verdict.json`
- registre A4 mis à jour (12 entrées, SHA `869dd6fe45222333…`), A5 rejoué
  (v2 : 8/8)
