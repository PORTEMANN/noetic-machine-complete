# Corridor E — du lien nucléé à la signature du 18
### Publication groupée du 09/09/2026 — série E44 → E65 + T5/T6

Cette série est la cartographie mesurée de la relation discrète dans le
continu : de la nucléation du lien (E44) à la signature énergétique du 18
(E65), en passant par la fermeture complète de la famille GP (E45–E59) et
le passage au vide hyperfluide (E60–E65).

**Gouvernance** : chaque campagne a été exécutée en local d'abord, avec
protocole gelé et haché avant tout calcul (champ `sha256_protocole`
calculé sur le fichier avec le champ vide — auto-référence exclue
déclarée), puis publiée après pause de tri (décision d'auteur du
09/09/2026). Les verdicts sont figés tels qu'exécutés ; les incidents de
harnais (B3-FAIL-TECHNIQUE) sont documentés dans les notes de chaque
campagne, avec leurs réparations hachées avant calcul. Le détecteur E44
(`e44_core.py`, filiation byte-level) est l'instrument de toute la série
E44→E59 ; la série E60+ est la dynamique de filaments de Biot–Savart
(harnais validé par T0 pré-enregistré : anneau isolé vs valeur
analytique).

---

## I. La nucléation — E44 (document fondateur)

**E44 — nucléation spontanée de l'enlacement** (`e44/`, note d'audit dans
`docs/`) : trempe Gross-Pitaevskii amortie (64³, A=2, γ=0,3) ; une paire
de Hopf nucléée spontanément dans l'ère des reconnexions (run A/440103,
t=12, Lk ≃ −1, robuste à trois estimations) — mais évaporée avant t=20.
Protocoles v1 (`42c65a0c…`) et amendement v2 (`bc977f17…`, hachés avant
calcul). Verdict : DÉRIVÉ partiel fort — « le maillon manquant n'est plus
la naissance du lien mais sa conservation. »

## II. La fermeture de la famille GP — E45 → E59

| Camp. | Question | Verdict |
|---|---|---|
| E45 | coupure de l'amortissement | **B3-FAIL** — 0/5 OFF, 0/5 ON : la tension seule détruit le lien |
| E46 | mur de densité mélangé | **ANOMALIE** — succès formel annulé par les compteurs gelés du détecteur (saturation) |
| E47 | séparation des composantes du mur | bras C : **B3-FAIL propre** ; bras B (Kelvin) : enchevêtrement figé illisible |
| E48 | gel à la nucléation + suivi | **B3-FAIL propre** — le gel fige les positions, le lien meurt (Lk_suivi = 0) |
| E49 | nettoyage puis gel | **B3-FAIL_FENETRE** — le lien meurt en < 5 unités, par reconnexion, pendant que les boucles vivent (mesure lisible) |
| E50 | lien imprimé + gel | **ANOMALIE** — le gel régénère l'enchevêtrement même depuis un état propre |
| E51 | pinning ponctuel apparié | **B3-FAIL lisible** — les puits n'empêchent pas la contraction (tension de ligne) |
| E52 | paysage de puits fixe | **PARTIEL** — les puits écartent la nucléation au lieu d'ancrer |
| E53 | canaux toriques continus | **B3-FAIL lisible** — la classe « ancrage spatial » close |
| E54(+A,B,C) | tressage de lignes sous rotation | **PARTIEL_NUCLÉE_SEUL** — l'objet persiste, la relation non (3 réparations de harnais documentées) |
| E55 | naissance dans des canaux enlacés | **B3-FAIL** — le confinement n'écrit pas le lien |
| E56 | tressage + ancrage des pieds | **SUCCÈS formel + note de marge** (loi T6 corroborée faiblement) |
| E56-x | robustesse (24 graines) | **CONFIRMÉ_FAIBLE** — persistance au plancher 1/24, B = A ; nucléation abondante (18–22/24) |
| E57 | cristallisation sous rotation forte | **B3-FAIL** — pas de réseau ordonné (ψ6 ≤ ~0,43 ; surnucléation mesurée) |
| E58(+A) | réseau imprimé | 2× **B3-FAIL-TECHNIQUE** (injection par la paroi ; drainage des périphériques) — la préparation est elle-même un problème de persistance |
| E59 | τ(A, γ) | **PARTIEL — la fonction de frontière** : τ décroît avec la non-idéalité, plafond τ_max = 15 au bord de résolution |

**Mesure centrale du corridor GP** : dans la famille GP résoluble, la
relation topologique est toujours réécrivable (obstruction : le cœur
déplétable) — plafond mesuré τ ≤ 15 unités (E59).

## III. Les lois — T5, T6

- **T5** (`t5/`) : le coût scalaire (ddll) est réfuté sous deux rubriques
  ; séparation parfaite par la contractilité de l'objet.
- **T6** (`t6/`) : **la loi à deux étages, mesurée sur table gelée** —
  objet ⟺ non contractile ; relation ⟺ non contractile ∧ ancrage externe.
  Falsifieur pré-enregistré : E56 (corroboré faiblement).

## IV. Le vide hyperfluide — E60 → E65

| Camp. | Question | Verdict |
|---|---|---|
| E60 | Biot–Savart libre | **B3-FAIL** — composites cohérents de forme mais non liés en position (l'espace libre n'a pas de pression du vide) |
| E61 | + pression du vide (κ=0,05) | **SUCCÈS** — l'équilibre souffle/pression tient la cage ANU (note de marge : bornes presque saturées à t=90) |
| E62 | fenêtre longue (t=180) | **B3-FAIL** — fuite lente : noyau stable, peau qui fuit |
| E63 | balayage du nombre n | **SUCCÈS** — toutes les cages n=12..24 tiennent à t=90 ; spectre de stabilité mesuré ; optimum de marge n=14 |
| E64 | τ_fuite(κ) | **FENETRE** — l'équilibre a un domaine : κ ≈ 0,1 tient à t=180 avec rms saturé |
| E65 | énergie des cages | **la signature du 18** : énergie par anneau minimale à n = 18 (5,27 — creux net) |

**La structure mesurée entre discret et continu** : la cavité tenue par
les filaments (objet continu, Kelvin exact), son équilibre
souffle/pression (mesuré), son domaine de pression (E64), son spectre
(E63), sa signature énergétique à n = 18 (E65), et sa mortalité (E62).

---

## Intégrité

- Protocoles gelés hachés avant calcul dans chaque dossier de campagne
  (`*_protocole.json`, amendements hachés le cas échéant) ;
- Empreintes par campagne : `SHASUMS_local.txt` dans chaque dossier ;
- Empreinte globale de la série : `corridor_E/SHASUMS.txt` (calculée sur
  les octets du dépôt — GitHub = source de vérité) ;
- Détecteur E44 commun : `e44_core.py` (sha256
  604c22322370eaa8707ddb6e7529b29539ec125c121b7e5368e2287b60ae1ac7) —
  copie byte-identique dans chaque campagne de la série GP ;
- Verdicts d'honneur du banc : 3 B3-FAIL-TECHNIQUE documentés (E45
  agrégation, E54 v1, E54-A, E58 v1) avec réparations hachées avant
  calcul — le protocole refuse de statuer tant que l'instrument n'est
  pas prouvé.

*Série exécutée en local le 09/09/2026, publiée groupée le 09/09/2026
(décision d'auteur). Auteur : Patrice Portemann — ORCID 0009-0009-4016-8389.*
