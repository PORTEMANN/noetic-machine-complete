# P42 — Le pont 120/E₈ : les deux 120 ont une racine commune, et c'est un théorème

**Patrice Portemann — corpus Machine Noétique, chantier P42**
Protocole gelé PONT-1.0 · arithmétique exacte Q(φ) · zéro paramètre ajusté · SHA-256
30 août 2026

## Verdict

**SUCCÈS — le pont est établi au niveau arithmétique.** La question
gelée du programme de prospection était : « si les deux 120 ont une
racine commune, c'est un théorème ; sinon, une frontière de plus au
registre. » C'est un théorème — exécuté, pas cité.

## Mesures

- **C1 — |2I| = 120, construit.** Le groupe icosaédrique binaire est
  construit en quaternions exacts dans Q(φ) (arithmétique Fraction, φ² =
  φ + 1) : 8 + 16 + 96 éléments, fermeture vérifiée, **9 classes de
  conjugaison** de tailles {1, 1, 12, 12, 12, 12, 20, 20, 30} — la
  structure exacte connue de 2I, ici calculée.
- **C4 — McKay exécuté.** Les 9 caractères irréductibles sont extraits
  par Gram–Schmidt sur les χ(Symⁿ V₂) (dimensions {1, 2, 2, 3, 3, 4, 4,
  5, 6}, Σd² = 120 ✓). La matrice d'adjacence de McKay A (entière,
  produits tensoriels avec la représentation naturelle) vérifie
  **A·d = 2d exactement** et est **isomorphe au diagramme affine Ẽ₈** —
  la référence Ẽ₈ n'est pas citée mais *construite* (racines simples de
  Bourbaki, det Cartan = 1, racine la plus haute θ = 2α₁+3α₂+4α₃+6α₄+
  5α₅+4α₆+3α₇+2α₈ vérifiée) ; isomorphismes trouvés par retour sur trace
  élagué ; spectres égaux à 1e-12 ({±2, ±φ, ±1, ±1/φ, 0}).
- **C5 — Molien.** La série calculée M(t) = (1/120)Σ_g U_l(cos θ_g)
  égale **exactement** (1+t³⁰)/((1−t¹²)(1−t²⁰)) jusqu'à l'ordre 60 ;
  premier degré invariant **d₁ = 12**.
- **C2 — la distinction publiée.** Sur S³/2I, le laplacien **scalaire**
  n'a de modes que sur les harmoniques 2I-invariants : λ_l = l(l+2)/R²
  aux l où m_l > 0 ; le premier est l = 12 → **λ₁ = 168/R²**
  (multiplicité 13). La « valeur propre 2/R² » n'est donc **pas** la
  première valeur propre scalaire.
- **C3 — d'où vient 2/R².** Le laplacien **tordu** (brut de connexion)
  sur les champs de Killing de S³ vaut 2/R² : Ric = (2/R²)·g vérifié
  symboliquement exact en coordonnées stéréographiques (Weitzenböck :
  ∇*∇X = Ric(X) pour X de Killing). Les deux objets sont distincts et
  les deux valeurs sont exactes — la machine les a distinguées.
- **C6 — la réécriture.** Avec le « 12 » de la formule koilon lu comme
  premier degré de Molien : N = d₁·log₂(1/α) = |2I| ⟺ **α =
  2^(−|2I|/d₁) = 2⁻¹⁰** — et |2I| = racines⁺(E₈) = 120 (240 racines
  comptées). Les deux 120 ont pour racine commune le couple **(d₁ = 12,
  |2I|/d₁ = 10 octaves)**.

## B3-FAIL du chantier (publiés)

1. **v1** : sympy symbolique générique trop lent (deadline) — v2 en
   arithmétique exacte dédiée Q(φ) en fractions rationnelles, même
   protocole.
2. **v2** : erreur de signe dans la partie réelle du produit de
   quaternions (−cg+dh au lieu de −cg−dh) — attrapée par le test de
   fermeture C1 (classes absurdes : 22 au lieu de 9).
3. **v2** : la cible spectrale « exposants de E₈ » codée de mémoire
   était **fausse** — les exposants donnent le spectre de l'adjacence
   du diagramme *fini*, pas affine. Remplacée par la construction
   directe et le test d'isomorphisme. Le graphe de McKay calculé était
   juste ; c'est ma cible qui était fausse.

## Ce que le chantier apprend

La lecture ddll (conjecture A5) : le pont est un théorème arithmétique —
**équilibre**, rien payé, rien ajusté. La frontière qui reste :
l'identification **physique** du « 12 » koilon (les demi-tons de la
gamme) avec d₁(2I) = 12 (le premier degré de Molien) — déclarée, hors
théorème, au registre. Entrée F14 ajoutée.

## Artefacts

- `p42_pont_120_e8.py` — SHA-256 114e28102247efe0… (script gelé PONT-1.0)
- `p42_pont_120_e8_verdict.json` — mesures exactes, verdicts, falsifieur
- Falsifieur pré-enregistré : A·d ≠ 2d ; non-isomorphisme à Ẽ₈ ; Molien
  calculé ≠ série théorique ; Ric ≠ (2/R²)g. Aucun n'est survenu.
