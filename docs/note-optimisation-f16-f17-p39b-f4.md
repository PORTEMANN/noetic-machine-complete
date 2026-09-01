# Note — Chantiers d'optimisation enchaînés (F16, F17, P39b, F4, F11, F10)

**Patrice Portemann — Machine Noétique, 31 août 2026**

Enchaînement des six chantiers d'optimisation déclarés, tous mesurés :

## F16 — ReN normalisé : FERMÉE (P46, REN-NORM-1.0)

Réparation mesurée : **ReN_a = (Rdyn+ε)(Rtop·D)/(H+ε)·100** (pression
entropique pure — Rc, seul porteur d'amplitude, supprimé). Fuite
d'amplitude réduite de ×100 à **≤ 1,13e-7** (4/5 signaux à 1e-15 ;
réserve publiée : cas d'entropie dégénérée H≈0, la sinusoïde).
Séparation des 5 signaux du benchmark préservée. ReN_b (pression par
note active) éliminé par mesure ; ReN_c (orientation physique) rejeté par
principe et mesuré pour publication. L'ordre des deux candidats diffère
(C4 publié). Verdict : PARTIEL 2/4 sur mes critères trop stricts — la
normalisation tient, le seuil 1e-9 que j'avais figé était excessif pour
le cas dégénéré.

## F17 — EEG single-trial : voie (i) MESURÉE INSUFFISANTE (P47, B3-FAIL)

Vote majoritaire sur blocs de N ∈ {1..12} essais : moyenne max **0,5926
< 0,60** (seuil figé de P44). Le sujet fort A03 atteint 1,0 à N=12 ; les
sujets faibles restent au hasard. Écarts à la montée binomiale publiés —
les essais ne sont pas indépendants. Restent les voies (ii) baseline
figée et (iii) filtrage spatial dérivé. Publié, pas effacé.

## P39b — Atomes 2D : PARTIEL 3/4, coût de fermeture mesuré

Ma convention 3D (orbitale e^{−Zr}) était fausse en 2D — **B3-FAIL
publié** : la 1s 2D est e^{−2Zr} (exposant doublé), cusp −2Z mesuré
exact. L'intégrale 1/r₁₂ en 2D a une **divergence logarithmique en θ à
r₁=r₂** (u ≈ Rθ) : le trapèze uniforme la surestime systématiquement
(mesuré : E_sp 2534 → 1260 Ha quand la grille radiale double). La
fermeture de l'intégrateur 2D exige la **fonction elliptique complète
K(m)** — coût mesuré, publié.

## F4 — KO-6 : vérificateur réel certifié (A3b, 4/4)

Les vrais axiomes KO-6 sont maintenant **exécutables** au niveau
matriciel (J²=+1, Jγ=+γJ, JD=−DJ, ordre un) : un triplet compatible est
trouvé par énumération déclarée (36 J₀ × 80 D), les trois axiomes et
l'ordre un tués un à un sont tous détectés (dont deux leviers v1 erronés
publiés en B3-FAIL). **Coquille mesurée** dans l'énoncé figé du registre
(« (J_F γ_F)² = −1 » incompatible avec la table de Connes). Espace
d'énumération sous bornes mesuré : 4 723 712 matrices. L'énumération
complète reste à exécuter — coût restant publié.

## F11 — Mémoire fractionnaire : le manque est publié

Les données Allen figées sont des trains de spikes, pas des traces de
facilitation/dépression synaptique — la voie exige un dataset
d'adaptation (déclaré, non disponible localement). F11 reste ouverte.

## F10 — Topological-Fractional-AI : reste ouverte par définition

Le script n'existe pas localement — rien à publier.

---

*Registre A4 : 20 entrées, 10 fermées / 5 ouvertes / 5 partielles
(SHA c56654f1…). Tous les scripts et verdicts sont figés SHA-256.*
