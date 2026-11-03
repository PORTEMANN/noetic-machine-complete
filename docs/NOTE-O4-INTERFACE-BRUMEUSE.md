# NOTE O4 — Bilan : φ n'est pas dans la dynamique — l'interface brumeuse comme objet

**Date :** 2026-11-03 · **Auteur :** Kimi (assistant IA), pour Patrice Portemann
**Statut :** note de bilan et d'orientation — clôt l'arc Φ-DYN-5/5b, ouvre l'orientation « interface brumeuse ». Ne modifie aucun verdict.
**Références :** VERDICT-ΦDYN2-P1 (d862875), P2 (62d3bcf), P3 (651330d), ΦDYN5 (261d41e), ΦDYN5B (162fde5), ERRATUM P1 pilier B, NOTE-PHI-DYN-2-SYNTHESE (18a7ab1), T24.

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| Renvois aux verdicts (toutes les valeurs y sont mesurées) · les cinq faits vérifiés de la correspondance (avant sa résolution) | « φ est du dictionnaire, pas de la dynamique » (synthèse des verdicts 5/5b) · « l'espace de phase est l'espace des invariants » (piste méthodologique) | Le programme « cartographier l'espace des couplants » · l'interface brumeuse comme objet d'étude · les implications pour Φ-DYN-4 · l'épaisseur de brume comme observable |

## I. Bilan de campagne — où φ est, où il n'est pas

**Table de vérité de la soirée et de l'arc :**

| Domaine | φ | Verdict |
|---|---|---|
| Dictionnaire d'isomorphismes (T14–T24) | présent, exact | le socle, inchangé |
| Comptes et échelles spectrales (T24, P1-O2, T24-fenêtre) | présent (ratios → φ) | robuste, instrument anneau |
| Blocking de **valeurs** (Φ-DYN-5) | **s'écoule** | accident UV ; l'ancre est le couplage |
| Ratios de gaps du point fixe de décimation (Φ-DYN-5b) | **absent** (2,3 %) | la générité n'est pas dorée |
| Dynamique du corridor GP (P3) | jamais présent | les entiers topologiques, pas φ |
| Algèbre des mots sous phason (P1) | présent mais **fine-structure** | tué au 1er flip |

**La loi qui se dégage : φ est une signature de la couche *dictionnaire* — isomorphisms, comptes, échelles. Dans tout objet de la couche *mécanique* — flot, RG, dynamique — φ disparaît ou devient instable. S'obstiner sur φ pour faire émerger la dynamique, c'est chercher une géométrie dans un écoulement.**

**Ce qui émerge à la place — les quatre objets dynamiques réels de la campagne :**
1. **La charge de Fricke** — conservée le long des orbites à 2,6·10⁻³⁰ : la seule vraie charge dynamique du corpus.
2. **L'ancre Λ²_sel** — couplage qui tourne (+8 → +29 %, saturation) : elle a une dynamique propre, mesurée, propre.
3. **La classification bornée/divergente** — spectre = orbite bornée : la dynamique discrète *classifie* le continu.
4. **Les entiers topologiques du corridor** (Q, Lk, 4 filaments/quantum) — invariants adiabatiques, mortels par singularité.

---

## II. Le pivot — l'interface brumeuse

**La bonne question n'est plus « où est φ dans la dynamique ? » mais « que traverse l'interface entre le discret et le continu, et qu'est-ce qui meurt en le traversant ? »** La brume n'est pas un obstacle à lever, c'est l'objet d'étude — et la doctrine de la frontière en est déjà l'instrument : l'interface a une épaisseur, mesurable comme la distance entre les seuils de mort de deux canaux (ce soir : algèbre des mots à 1 flip, statistiques de gaps stables à ρ = 0,01 — *deux canaux, deux seuils*).

**Comment faire émerger la dynamique de la machine — la piste :**
- **L'espace de phase n'est pas l'espace des états, c'est l'espace des invariants.** Φ-DYN-5 l'a montré : le couplant écoule proprement là où la valeur se déchire. La machine ne doit pas simuler des trajectoires (empruntées) mais des **écoulements d'invariants** (dérivés).
- **Programme : cartographier l'espace des couplants.** Ancres multi-paramètres (y, ρ, échelles de blocking) sous RG déclarées : flots, points fixes, exposants. Chercher les points fixes LÀ — pas φ : les candidats sont la charge de Fricke (κ-surface), les entiers topologiques (si une RG corridor-adaptée peut être déclarée), le quantum de paroi.
- **L'interface brumeuse comme observable à part entière** : épaisseur = écart de seuils entre canaux ; direction = sens de la hiérarchie de morts ; tout chantier futur doit déclarer son canal (leçon 5b).

---

## III. Enjeux du chantier ouvert — la correspondance trace map ↔ Jacobi

**L'état vérifié ce soir (mpmath 60 chiffres, main, récurrences croisées) :**

1. **L'anneau réel est auto-cohérent** : ses 233 eigenvalues exactes satisfont la condition de Bloch de sa propre monodromie (|Tr/2| ≤ 1 + 1e−11, vérifié en produit exact). Objet sain.
2. **Les graines de T24 ne sont pas les traces du modèle à sauts uniformes** : écart exact de 0,5 sur la graine 2 (x₂_T24 = 0,5t²−0,5t−0,5 vs Tr(AB)/2 = 0,5t²−0,5t−1) ; à t = 0,7 : −0,605 vs −1,105. P1-A n'a validé que l'**identité de mot** (valable pour toute paire unimodulaire), jamais les graines — c'est ainsi que l'écart a traversé T24 → P1 → ce soir.
3. **La récurrence de T24 est un instrument spectral sain pour *quelque* modèle** : ses comptes (19/30/48/78/126/202) respectent le degré du polynôme (19 ≤ 34 ✓) et la récursion Fibonacci — à la différence des graines « du vrai modèle », qui aliasent dès le niveau 9 (55 > degré 34, impossible). **T24 mesure un spectre réel, mais lequel ?**
4. **L'anneau réel et le discriminant T24 ne coïncident pas** : 41–45 % des eigenvalues exactes de l'anneau ont |x_N(λ)| > 1 (à 60 chiffres, indépendant de toute grille).
5. **Hypothèse à phase (π/3) : blessée, pas tuée proprement.** Les graines 1–3 correspondent *exactement* (algèbre vérifiée mot à mot) à un modèle onsite {0,1} + saut e^{iπ/3} sur les maillons B ; pourtant l'anneau à phases construit numériquement ne satisfait pas la condition de Bloch au discriminant T24 (44 % hors). Contradiction non résolue — la construction de l'anneau à phases (gauge, bouclage, ordre des lettres) doit être auditée avant tout verdict sur l'hypothèse.

**Pourquoi c'est l'enjeu correct, et son échelle :**

- **Interprétation physique.** Si le discriminant de T24 est celui d'un quasicristal à flux (phase π/3), toute la physique lue depuis T24 — bandes, gaps, « chaînon optique » — appartient à un modèle magnétique : le « chaînon SL(2,ℝ) » devient un chaînon *magnétique*, et la filiation au seesaw/Penrose doit être relue (le déterminant 1 avec phases ≠ déterminant 1 réel). Si au contraire les graines T24 sont une jauge innocente d'un modèle réel, le mystère est un artefact de paramétrage et le corpus physique tient.
- **Intégrité du corpus.** P1-A (classification 80/80, O2) et la chaîne T24 utilisent la récurrence T24 comme instrument gelé — *internalement valide* (identité prouvée, comptes sains), mais *physiquement non rattaché* à un Hamiltonien identifié. Aucun verdict ne tombe ; leur **interprétation** est suspendue à ce chantier.
- **Coût et risque.** Faible et borné : l'audit est algébrique (identifier la paire de matrices exacte derrière les graines — problème inverse fini) plus numérique (anneau à phases correctement construit). Risque maximal : si le modèle T24 est exotique, une passe de re-validation des comptes T24/P1 avec l'instrument anneau (déjà disponible) suffit à re-sceller les verdicts concernés.
- **Fenêtre.** Le problème inverse « quelle paire unimodulaire produit les graines (t/2, 0,5(t²−t−1), 0,5(t³−t²−2t+1)) ? » est fini et déterminé : trois équations de traces pour huit paramètres (modulo jauge). Il est attaquable en une session.

---

*La brume n'est pas une défaillance de la machine — c'est sa matière. φ vivait dans le dictionnaire ; la dynamique vit dans les couplants ; l'interface entre les deux est le prochain instrument.*
