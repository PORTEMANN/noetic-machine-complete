# VERDICT-ΦDYN5B — φ sous la RG de décimation : point fixe existant, stable, non-φ-signé

**Date :** 2026-11-03 · **Chantier :** Φ-DYN-5b · **Fiche :** FICHE-PHI-DYN-5B-POINT-FIXE **v1.3 SCELLÉE** (f95512f → 3de8d75 → v1.3 ; parcours : v1.0 critère sourd au bruit → v1.1 bande déclarée → v1.2 instrument anneau imposé par l'erratum VERDICT-ΦDYN2-P1 → v1.3 contrôle interne après diagnostic de non-correspondance des modèles)
**Références :** VERDICT-ΦDYN5 (261d41e), ERRATUM VERDICT-ΦDYN2-P1 pilier B (ce soir), VERDICT-ΦDYN2-P1 (d862875), T24.
**Statut du mot :** hors-série Φ-DYN (précédent P1–P3, 5).

---

## Registre épistémique (apposé le 2026-11-03 — audit à trois étages)

| Mesuré | Interprété | Spéculé |
|---|---|---|
| D(12,13)=0,022 → D(13,14)=0,018 (anneau exact) · permutation gelée p = 1,0000 · fraction φ des ratios 2,3 % · F3 : 17/20 (ρ=0,001) et 13/20 (ρ=0,01) · anneau auto-cohérent (exactitude interne PASS) · profils phason reproductibles niveau 14 | « Point fixe de décimation existant, non φ-signé dans les gaps » · « deux canaux, deux seuils : une frontière déclare son canal » · « stable dans ce canal observable » | La généralité « structurelle (comptes, échelles), pas valueurale ni locale » · l'échelle de robustesse comme hiérarchie universelle de la matière |

## Synthèse en une phrase

**La RG de décimation par substitution possède bien un point fixe dans les statistiques de gaps — convergence strictement monotone (D : 0,022 → 0,018), distributions finales indistinguables (p = 1,0000) — mais ce point fixe n'est PAS φ-signé dans les ratios de gaps (2,3 %), et il est STABLE sous désordre phason (17/20 à ρ = 0,001) : la générité de la convergence existe sans être dorée ni fragile, et la prédiction d'instabilité est réfutée pour ce canal observable.**

---

## 1. Palier A — instrument anneau : **PASS (exactitude interne)**

Anneaux périodiques de Jacobi W₁₂/W₁₃/W₁₄ (144/233/377 sites, `eigvalsh` exact) : réalité, N = L, trace = somme des onsites (55/89/144 exactes) — **PASS aux trois niveaux**. Le croisement anneau/trace map est déclaré **NON APPLICABLE** : la récurrence de T24 et le Jacobi à sauts uniformes ne correspondent pas modèle pour modèle (41–45 % d'eigenvalues exactes hors du discriminant de la récurrence, mesuré à 60 chiffres — les graines de la récurrence ne sont pas les traces du modèle à sauts uniformes). Correspondance exacte des modèles : **ouverte**.

## 2. Palier B — mesures (mot pur puis grille phason)

**F1 — convergence : D(12,13) = 0,0223 → D(13,14) = 0,0181 — strictement décroissante.** La convergence vers une distribution fixe est nette et monotone (le palier observé en B1 avec l'instrument trace map était un artefact de grille — confirmé : l'instrument anneau ne le montre pas).

**F2 — distribution fixe :** permutation gelée (1 000, graine 20261103) : **p = 1,0000** — les distributions de ratios des niveaux 13 et 14 sont statistiquement indistinguables. Le point fixe de décimation **existe**.

**F2 nuance — non-φ-signé :** fraction des ratios de gaps dans {1/φ, 1/φ²} ± 0,02 : **2,3 %**. La distribution fixe n'est pas dorée dans cet observable. La signature φ vit dans les **échelles et les comptes** (fenêtre T24 des ratios de comptes TENUE : 1,6154 / 1,6032 — protocole P1-O2 verbatim), non dans les ratios de gaps consécutifs. H-ΦDYN5b corrigée : *φ fixe dans les comptes, pas dans les gaps.*

**F3 — stabilité sous phason (prédiction réfutée pour ce canal) :** F1 tenu dans **17/20** réalisations à ρ = 0,001 et **13/20** à ρ = 0,01 (critère gelé d'instabilité : échec dans ≥ 15/20 — **NON TENU**). Les statistiques locales de gaps convergent encore sous désordre là où l'algèbre des mots meurt au premier flip (P1). **Deux canaux de dommage, deux seuils.**

## 3. Verdict global (fiche §6)

**NUANCÉ — ni CONFIRMÉ ni RÉFUTÉ au sens strict des trois jambes gelées :**
1. **Point fixe de décimation : CONFIRMÉ** (F1 strict, F2 p = 1,0000) — la réponse à la question de la NOTE v2 est *oui* : il existe une RG déclarée (la décimation par substitution) dont les statistiques spectrales convergent vers une distribution fixe.
2. **« φ-signé » : RÉFUTÉ dans l'observable choisi** — 2,3 % ; la signature dorée du point fixe se porte par les comptes/échelles (T24), pas par les ratios de gaps.
3. **« Instable au phason » : RÉFUTÉ dans ce canal** — la stabilité dépend de l'observable : l'algèbre des mots est fine (1 flip, P1), les statistiques de gaps sont robustes (ρ = 0,01).

**Le tableau des quatre verdicts RG se referme ainsi :**
- Φ-DYN-5 (blocking de *valeurs*) : φ s'écoule — accident UV.
- Φ-DYN-5b (décimation de *structure*) : convergence fixe existante, non dorée dans les gaps, stable au phason dans ce canal.
- La générité cherchée existe — elle est **structurelle** (comptes, échelles), pas valueurale ni locale.

## 4. Leçons gravées au dossier

1. **Une frontière n'existe que relativement à un observable** — deux canaux (algèbre des mots / statistiques de gaps), deux seuils de dommage (1 flip / ρ = 0,01+). La doctrine de la frontière gagne sa réserve fondatrice : *toute frontière déclare son canal.*
2. **Trois instruments, trois pièges** (produits grid-wide : explosion d'entrées ; trace map grille : palier de résolution et modèle de correspondance ouverte ; anneau : exact mais à contrôler en exactitude interne). *Aucun instrument ne se croise avant d'avoir été compris.*
3. **Un palier statistique n'est jamais une preuve de structure sans instrument indépendant** (le palier F1 de B1 était un artefact de grille ; l'anneau l'a dissipé).
4. **La nuit a coûté quatre erratums de fiches et un erratum de verdict** — et chacun a rendu le corpus plus honnête, pas plus faible. C'est le prix de la classe (iii).

---

## 5. Artéfacts

Scripts : `src/phidyn5b_palierAB1.py` (trace map, instrument supplanté — conservé pour la trace), `src/phidyn5b_F3.py` (chemin produit, supplanté — conservé), `src/phidyn5b_v12_anneau.py` (**instrument de référence**).
Données : `data/phidyn5b_palierAB1.json`, `data/phidyn5b_v12_paliersAB.json`.
Erratum associé : `docs/NOTE-ERRATUM-PHIDYN2-P1-PILIERB.md` (pilier B de P1 : produits grid-wide aliasés).

*Verdict hors-série Φ-DYN, nommé VERDICT-ΦDYN5B (2026-11-03).*
