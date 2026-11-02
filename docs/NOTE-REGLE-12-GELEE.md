# Fiche gelée — Règle 1.2 : démonstration de puissance sur HCP contrôles

**Date de gel :** 2026-11-02 · **Statut : GELÉE avant run — aucune donnée
utilisée pour concevoir les critères après cette date.**
**Filiation :** NOTE-MCS-28 §6 (la règle originelle) · dry-run §9 (le plant
sz = dissolution homogène) · inv_HCP (extraction validée croisée) ·
NOTE-UCLA-SZ (la leçon D5 : les déformations tuent, donc on les gèle).

---

## Objet

Vérifier que l'instrument MCS-28 détecte une vérité plantée de magnitude
déclarée dans de vrais connectomes HCP contrôles, à **α = 10⁻⁴**, avec
**puissance ≥ 0,95**, et que la détection **s'effondre quand la vérité est
retirée** (levier tuable).

## Données

HCP Young Adult, paquets **Rest3TRecommended**, sujets contrôles (HCP-YA
est une cohorte saine — tout sujet va). Seuil d'exécution déclaré :
**≥ 15 sujets extraits** (méthode d'extraction validée croisée,
sous-échantillonnage temporel ×2, inf neutralisés — conventions déjà
figées, NOTE 2026-11-01). Les ~93 sujets attendus dépassent le seuil ;
la règle peut tourner à 15, 30 ou 93 sans modification des critères
(les trois tailles seront rapportées).

## Vérité plantée (déclarée, figée)

Le plant **sz-dissolution** du dry-run (§9) : sur le connectome z de
Fisher, réduction de la présence intra-plan (facteur 1 − s) et hausse
homogène de la présence inter-plan (+s·magnitudes) — la perturbation
structurelle qui, dans le monde synthétique, produisait Γ↓, S_ent↑,
d_eff↑ (deux invariants du trio spectral déplacés). Deux magnitudes :
**s = 0,3 (faible) et s = 0,5 (fort)** — la puissance est rapportée pour
chacune ; l'exigence de puissance porte sur **s = 0,3** (le cas dur).

## Design (within-sujet — chaque cerveau est son propre contrôle)

Pour chaque sujet i, à partir de sa matrice W_i (116×116) :
- **20 copies plantées** P_i,k : plant à s appliqué à W_i ;
- **20 copies témoins** C_i,k : W_i bruité à magnitude équivalente sans
  structure (même budget de perturbation, module non planté — le contrôle
  du « bruit qui imiterait le plant »).

## Statistiques (gelées)

- Invariants : Γ, S_ent, d_eff (le trio spectral), canoniques (D4 :
  sans filtre) ; C_26, M_34 rapportés, non critères.
- Score de copie : z du trio dans l'espace du sujet (standardisation sur
  ses 40 copies).
- **Détection** : seuil α = 10⁻⁴ par permutation des étiquettes de copies
  (within-sujet, N = 10 000, graine publique 20261028), test unilatéral
  dans la direction plantée (Γ↓, S_ent↑ — direction gelée AVANT run,
  conforme au plant, §9).
- **C1 (puissance)** : fraction de copies plantées détectées ≥ 0,95,
  rapportée par sujet et poolée (médiane inter-sujets) — pour s = 0,3.
- **C2 (fausse alarme)** : fraction de copies témoins détectées ≤ 10⁻⁴.
- **C3 (levier)** : à s = 0 (plant retiré, bruit conservé), la puissance
  mesurée doit chuter sous 0,05 — sinon la statistique attrape le bruit,
  et c'est la statistique qui est tuée, pas le run qui continue.
- **C4 (levier longueur)** : halver les volumes retenus (×2 → ×4) doit
  dégrader la puissance de faç monotone documentée (pas un critère
  binaire — une mesure publiée).
- **C5 (regression)** : sur au moins un sujet, rejeu complet du script
  depuis les volumes bruts → mêmes nombres au 1e-4.

## Falsifieurs (tuables)

Puissance < 0,95 à s = 0,3 ; fausse alarme > 10⁻⁴ ; levier s = 0 non
détecté ; dégradation non monotone en C4.

## Ce que cette règle n'est pas

Ce n'est pas un test clinique (aucune donnée patient). C'est le banc
d'étalonnage : il certifie que l'instrument *entend* une structure d'amplitude
connue dans du vrai cerveau. Le verdict de la carte MCS-28 sur la cognition
reste suspendu à D5 (mouvement) et aux réplications — la règle 1.2 est
nécessaire, non suffisante.

*Modification de cette fiche uniquement par note datée référençant celle-ci.*
