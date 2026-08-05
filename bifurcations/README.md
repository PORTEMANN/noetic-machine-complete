# Bifurcations classificatoires — chantier hors-programme

Série de chantiers éprouvant les **bifurcations de classement** du tableau périodique par discriminant dérivé à zéro paramètre ajusté. Logique de verdict binaire (C12.1, B3-FAIL), adossée à l'instrumentation P30–P33 (frontière r₁₂).

**Distinction de statut.** Contrairement au noyau P0–P33 (verdicts physiques sur observables), ces chantiers éprouvent des **questions de classement**. La *loi des bifurcations* qui en émerge est une **conjecture (catégorie II candidate)**, clairement étiquetée — elle n'a pas le statut de théorème.

## Verdicts

| Chantier | Question | Score | Verdict |
|---|---|---|---|
| **P-He** | He : H / Be / gaz noble ? | **5/5** | **tranchée** — He est gaz-noble-like (convergence 4/5, marge 0,602). Le « ns² » de He est une sous-couche *pleine*, pas une parenté avec Be. |
| **P-LaLr** | Bloc f : ouvrir La/Ac ou fermer Lu/Lr ? | **2/5** | **B3-FAIL** — aucun discriminant dérivé ne valide le levier ; frontière d/f = zone de liberté **constitutive** (conventionnelle). |
| **P-CrCu** | Anomalies d⁵/d¹⁰ : loi ou bruit ? | **3/5** | **partiel** — règle d⁵/d¹⁰ exacte en 3d (loi), percée en 4d/5d (liberté). |
| **P-F3** | Indice de complexité dérivé ? | **3/5** | **partiel-négatif** — aucun indice scalaire monotone n'ordonne les bifurcations ; révèle l'axe *conventionnalité*. |

## La loi des bifurcations (v2) — conjecture

Voir `Loi_des_Bifurcations.md`. Forme v2 (affinement issu de l'échec P-F3) :

> Pour une bifurcation **physique** (instabilité de configuration), la dérivabilité **décroît avec la complexité** (Z, corrélation, relativité, dégénérescence) : tranchable à bas Z, zone de liberté à haut Z. Une bifurcation **conventionnelle** (choix de frontière de classement) est zone de liberté **quelle que soit la complexité**. La décroissance ne régit que l'axe physique.

C'est la **formulation classificatoire de la frontière r₁₂** (P32) : même décroissance de la dérivabilité quand la complexité monte.

**Résultat transverse** : la machine discrimine les bifurcations *résolubles* (He) des bifurcations *constitutives* (bloc f) — elle cartographie où le réel cesse d'être classifiable, et distingue deux sortes de zones de liberté (physique par complexité / conventionnelle).

## Fichiers

- `phe_protocole_fige.json`, `phe_verdict.json` — bifurcation He (5/5)
- `plalr_protocole_fige.json`, `plalr_verdict.json` — bloc f (2/5, B3-FAIL)
- `pcrcu_protocole_fige.json`, `pcrcu_verdict.json` — remplissage d⁵/d¹⁰ (3/5)
- `pf3_protocole_fige.json`, `pf3_verdict.json` — indice de complexité (3/5, B3-FAIL)
- `Loi_des_Bifurcations.md` — formalisation v1 + addendum v2 (conjecture)

**Prédictions falsifiables gelées** : P-F1, P-F2 (bifurcations physiques) ; P-F4 (conventionnelles = liberté quel que soit Z).

*Méthode : C12.1 (protocoles figés avant calcul, SHA consignés), B3-FAIL (P-LaLr et P-F3 publiés comme échecs), zéro paramètre ajusté, « fermer ne pas ajouter ». Aucun verdict du noyau P0–P33 n'est modifié.*
