# Note de chantier — D5 (mouvement) : première passe, et révision datée
du verdict UCLA

**Date :** 2026-11-02 · **Tiroir :** instrument (déformation D5 déclarée le
01/11 dans NOTE-UCLA-SZ-PILOTE §5).
**Filiation :** NOTE-UCLA-SZ-PILOTE (le verdict révisé ici) · la règle
gelée : une déformation tuée ne tue pas la carte, elle impose la passe
correspondante avant tout nouveau verdict.

---

## 1. Ce que la première passe a trouvé (107 sujets, invariants complets)

**Appariement exact FD (glouton 1:1, caliper 0,05 mm) → 36 paires, FD
moyens 0,167 (SZ) vs 0,180 (CTRL) — équilibre parfait :**

| Invariant | Z apparié | p (nul sign-flip N = 10 000) |
|---|---|---|
| Γ | +2,92 | 0,0022 |
| S_ent | +2,32 | 0,0214 |
| d_eff | +2,71 | 0,0069 |
| C_26 | **−3,46** | **0,0004** |
| M_34 | +0,17 | 0,87 |

**La corrélation FD↔invariants a des signes opposés selon le groupe**
(Spearman) : SZ ρ(FD, Γ) = +0,23, ρ(FD, S_ent) = +0,37 (p = 0,007),
ρ(FD, d_eff) = +0,37 (p = 0,008) ; CTRL : **−0,32** (p = 0,016),
−0,26 (p = 0,050), −0,25 (p = 0,061).

## 2. Révision datée du verdict du 01/11

Le verdict « rien ne survit à l'appariement mouvement » reposait sur une
**régression linéaire poolée** — qui suppose une pente commune FD→invariant.
La passe D5 mesure que les pentes **diffèrent de signe entre les groupes**
(Simpson) : la régression poolée sur-corrigeait et a tué un signal que
l'appariement exact laisse vivant. **Verdict révisé : l'axe SZ, mort par
mauvaise méthode le 01/11, ressuscite en CSp sous appariement exact** —
Γ/S_ent/d_eff plus hauts, **C_26 plus bas** chez les schizophrènes
(p = 0,0004, dans le sens du gelé 2025 pour une fois).

**Deux lectures honnêtes, non tranchées :** (a) différence de groupe
réelle, visible quand le mouvement est égalisé ; (b) interaction
mouvement × diagnostic (le mouvement affecte différemment les deux
groupes — phénomène connu de la littérature, qui serait *elle-même* un
signal clinique). Les deux sont des signaux ; aucun n'est encore un
verdict de carte.

## 3. Ce qui reste à D5 (passe 2, gelée à l'avance)

1. **Scrubling temporel** : censure des volumes à FD élevé *avant* la
   corrélation — exige de relancer le pré-traitement sur les séries
   (~5 h de calcul) ; c'est la version forte du contrôle.
2. **Appariement étendu** : avec les 127 contrôles complets (la sélection
   n'en a retenu que 57 ici — l'intégralité élargira le nombre de paires
   et la puissance).
3. **Vérité plantée de l'appariement** : vérifier (style règle 1.2) que
   l'appariement FD ne crée pas de faux positifs sur des données sans
   effet.
4. **Réplication COBRE** (NITRC) — l'arbitre extérieur, FD-apparié.

## 4. Leçon de méthode (gravée)

Une déformation ne condamne jamais un résultat *définitivement* : elle
condamne la **méthode qui l'a mesuré**. D5 a tué la régression poolée ;
elle a rendu l'appariement exact ; et elle a révélé une structure
(Simpson) que la régression ne pouvait pas voir. La leçon rejoint le
corpus : *chaque déformation tuée est une méthode révisée, pas un cercueil.*

*Révision uniquement par note datée. Données : invariants complets UCLA
(déjà publiés), graine 20261028.*
