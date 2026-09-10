# Campagne E67 — les paysages par n (LOCALE, exécutée le 09/09/2026)

**Protocole E67-PAYSAGES-1.0 (gelé, haché `18592501…96679a8d`). Incident
d'extraction documenté : la première extraction prenait le maximum global
(bord de grille à R=30, qui dépasse la crête) au lieu du premier maximum
local — réparé et relancé (durée de calcul : 12 s) ; protocole inchangé.**

## Verdict : les paysages de la fenêtre dépendent fortement de n

| n | barrière R | vallée R |
|---|---|---|
| 12 | 8,5 | 9,0 |
| 14 | 15,0 | 17,0 |
| 16 | 14,5 | 15,5 |
| **18** | **16,0** | **22,0** |
| 20 | 18,5 | 24,5 |
| 22 | 17,5 | 27,0 |
| 24 | 13,5 | 14,0 |

n=18 reproduit exactement la référence (16,0 / 22,0 ✓ — cohérence avec le
calcul déclaré d'E64-A).

## Lecture (déclarée)

La barrière et la vallée ne suivent PAS une loi monotone en n : le
paysage est structuré par l'empilement (3 latitudes) — chaque n a sa
géométrie de crête et sa profondeur de vallée. La fenêtre du
couronnement (parking avant la barrière) est donc **par n** : la cage
tenue se gare sous sa propre crête, qui n'est pas universelle. La cage à
18 a la plus grande séparation crête→vallée (16 → 22) — le plus grand
« bassin de fuite » ; la cage à 24 a la structure la plus étroite (13,5 →
14,0). Conséquence : la fenêtre κ devra être mesurée par n (le κ ≈ 0,1
d'E64 vaut pour n=18 ; la fenêtre de la cage à 14 ou 24 sera différente).
