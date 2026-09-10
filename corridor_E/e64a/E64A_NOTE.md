# Campagne E64-A — grille fine de la fenêtre du couronnement (LOCALE, exécutée le 09/09/2026)

**Amendement gelé `43e6f78b…815b5eb9` (haché avant calcul). Incident
d'agrégation documenté : clé de contrôle hors grille fine (0,05 au lieu de
0,1) — réparation sur fichiers incrémentaux, protocole inchangé.**

## Verdict : la fenêtre est étroite — κ ∈ ]0,075 ; 0,125[

| κ | tient à t=180 | τ_fuite | rms(t=180) |
|---|---|---|---|
| 0,06 | non | 135 | 17,20 |
| 0,075 | non | 135 | 16,41 |
| **0,1** | **OUI** | **≥ 180** | **14,18** |
| 0,125 | non | 180 | 17,28 |
| 0,15 | non | 135 | 18,92 |

- Bord bas (échappement) : entre 0,075 et 0,1 (P1 pré-enregistré 0,05–0,075
  — mesuré au-dessus : publié) ;
- Bord haut (disruption) : entre 0,1 et 0,125 (P2 pré-enregistré
  0,125–0,2 — mesuré en dessous : publié) ;
- Contrôle de filiation κ=0,1 : tient à t=180 ✓.

## Lecture (déclarée — cohérente avec le paysage énergétique calculé)

La cage tenue (κ=0,1) se gare à rms = 14,18 — **en dessous de la barrière
énergétique à R ≈ 16** (calculée sur la géométrie gelée d'E65) ; toutes
les cages qui échouent dérivent vers rms 16,4–18,9 : elles **franchissent
la barrière** et courent vers la vallée statique à R ≈ 22 (le bras libre
d'E62 était à 21,47 à t=180, à 0,53 de la vallée, en accélération après
la barrière). La fenêtre du couronnement est donc un **parking avant la
barrière** : le confinement arrête le gonflement par réorganisation avant
la crête ; sous la fenêtre, la cage passe la crête et fuit ; au-dessus,
le confinement force les croisements d'anneaux (disruption rapide).
