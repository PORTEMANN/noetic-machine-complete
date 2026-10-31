# Note de chantier — Dettes cosmologiques : transitions Noether (C1) et
CMB/BBN/lentille (C2)

**Date :** 2026-10-31 · **Tiroir :** remboursement de dette (réponses à
l'objection 5 du COMITE-LECTURE-ACIDE).
**Filiation :** NOTE-CIRCONSCRIPTION-MACHINES (registre ; les trois
cercles) · T48-D1 (axiome d'extinction) · verdict RAR × SPARC (CS+).

---

## 1. C1 — la transition hors-régime et Noether : localisation du conflit

**Le conflit n'est pas là où le comité le met.** La mesure RAR × SPARC
(CS+) est une loi **lisse** : g_obs = g_bar + g†·f(g_bar/g†) avec f
interpolante régulière (fonction « simple » f(x) = x/(1+x) et
consœurs). Aucune marche de Heaviside n'existe dans les données ni
dans le fit. La discontinuité vit dans l'*axiome* T48-D1 — « hors de
son régime, un coefficient cesse d'être » — lu comme fonction marche.
Le conflit avec Noether est donc un conflit entre l'interprétation
(marche) et la loi mesurée (lisse), pas une propriété de la loi.

**Résolution par mur de domaine (mécanisme vérifié ce jour).**
Toute marche est la limite mince d'un profil lisse : le « mort du
coefficient » se réinterprète comme une paroi de domaine d'un champ
effectif. Vérification symbolique (potentiel φ⁴ déclaré, illustratif —
pas une physique choisie) :

- équation du mouvement satisfaite identiquement : φ'' − dV/dφ = 0 ;
- **conservation exacte** : dT_xx/dx = φ'·(EOM) = 0 — ∇_μT^{μν} = 0
  sur toute la paroi, pas seulement en dehors ;
- le « saut » vit dans l'équation d'état (T_xx change de signe), pas
  dans la conservation ; viriel ∫T_xx = 0 mesuré ;
- tension de surface σ = 2√2·m³/(3λ) — **le prix de la transition,
  nouvel objet phénoménologique**.

T48-D1 se relit : limite mince (Δr → 0) d'une paroi de largeur Δr.
La doctrine gagne un falsifiable : la **largeur de transition** dans
les courbes de rotation doit être finie si l'interprétation paroi est
correcte. Données requises : SPARC (inscription) — besoin déclaré,
chantier ouvert, rien mesuré d'ici.

**Reste dû (C1b).** Dériver la paroi depuis un potentiel fondamental
(et non déclaré) ; articulation avec les actions connues du type
MOND (AQUAL, TeVeS — voies sourcées de la littérature, non re-dérivées
ici).

## 2. C2 — CMB, BBN, lentille : la carte des régimes

La doctrine T48-D1 coupe l'espace des observations en régimes. Carte
honnête :

| Régime | Observations | Statut de la machine |
|---|---|---|
| Disques spiraux, g_bar ∈ [10⁻¹², 10⁻⁸] m/s² | courbes de rotation SPARC | **mesuré — CS+ (seul verdict scellé)** |
| Amas de galaxies (lentille + rayons X) | Bullet Cluster et consœurs | **extrapolation non scellée** — tension connue du type RAR à l'échelle amas ; aucun verdict de la machine ; la critique du comité touche ici juste |
| Univers primordial (CMB, BBN) | pic acoustique 3, hélium | **silencieux** — la machine ne prétend pas (Cercle 3, NOTE-CIRCONSCRIPTION) |

**Deux points gravés.** (1) Le silence n'est pas une contradiction :
T48-D1 dit précisément que le coefficient RAR « cesse d'être » hors de
son régime — le CMB est hors régime par construction. L'exigence du
comité (« votre alternative doit tout expliquer ») est un changement de
sujet que la doctrine refuse. (2) **Mais** l'amas Bullet est dans la
classe de régime des extrapolations, et la tension y est réelle et
connue : la machine ne peut pas se cacher derrière le silence. Statut
honête : verdict non tourné, données (lentille faible, cartes de
convergence) requises — besoin déclaré.

**Crochets falsifiables scellables.** (a) Universalité de g† : si le
seuil g† ≈ 1,2·10⁻¹⁰ m/s² gouverne aussi la classe amas, la position
des pics de masse doit corréler au franchissement du seuil local ;
(b) largeur de transition (C1). Les deux sont des veilles datées, en
attente de données.

## 3. Leçon

Ces deux dettes se rétrécissent au même geste : la machine ne fabule
pas là où elle n'a pas pesé, et elle transforme l'absence de verdict en
carte nommée — régimes, données requises, crochets falsifiables. Le
comité avait raison sur la lettre (pas de dérivation Noether-compatible,
pas de mot sur le CMB) ; la réponse est la doctrine appliquée : localiser,
scoper, dater, déclarer les besoins. Ce qui reste dû est un programme à
deux volets (C1b : potentiel de paroi fondamental ; C2b : verdict amas
quand les données arrivent) — plus des inscriptions à faire par
l'atelier humain (SPARC, lentille).

*Révision uniquement par note datée. La vérification symbolique du §1
est rejouable (sympy, kink φ⁴ déclaré).*
