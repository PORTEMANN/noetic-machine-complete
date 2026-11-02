# Note — T69 : la formule explicite sous forme Ei — ECHEC partiel 1/4,
et deux faits mesurés malgré tout

**Date :** 2026-11-02 · **Verdict :** `data/t69_connes_ei_verdict.json`
(1/4) · **Script :** `src/t69_connes_ei.py`.
**Filiation :** NOTE-ANTIK-ANALYSE §3.1 (R-Antik-2) · T67 (outillage ζ).

---

## 1. Ce que la machine a mesuré

| Critère (gelé) | Mesure | Verdict |
|---|---|---|
| V1 Li ≡ Ei∘log à 1e-40 | écart **2,1·10⁻²⁵** (= précision de travail à 25 chiffres) | tenu *en substance* ; le seuil gelé dépassait la précision du run (mismatch de protocole assumé, pas de la formule) |
| V2 π̂(100) dans ±2 de 25 | 28,58 (écart 3,58) | **refusé** |
| V2 π̂(1000) dans ±6 de 168 | 176,7 (écart 8,7) | **refusé** |
| V3 appariement (ρ, ρ̄) vs (ρ, 1−ρ) | écart **0,0000** | tenu — et c'est un résultat, voir §2 |
| V4 levier somme vide | écart 4,4 (< 10) | refusé (seuil gelé, enchaîné à V2) |

## 2. Le fait structural : sur la ligne critique, la « correction » ne
change rien numériquement

V3 mesure que les deux appariements sont **exactement identiques** —
ce qui est mathématiquement évident *une fois vu* : sur la ligne critique,
1 − ρ = ρ̄. La correction Connes–Ei est donc, en valeur, **protectrice
de branche** (elle fixe le prolongement analytique là où la forme Li
classique devient ambiguë hors de la ligne), non modifiante sur les zéros
vérifiés sous RH. C'est la réponse honnête à apporter au document Antik :
la substitution est légitime et sans effet numérique sur Re(s) = 1/2 —
ni confirmation spectaculaire, ni réfutation, une précision de langage.

## 3. Le refus V2 : diagnostic honnête

L'écart systématique (+3,6 / +8,7, croissant comme √x) avec une somme
des zéros mesurée à −0,19 là où la structure de l'énoncé exige +3,4 (π)
ou davantage (Π) indique une **erreur de conventions dans la formule
implémentée**, pas nécessairement dans la forme Ei : candidats identifiés
— (a) la forme de Riemann compte les **puissances premières** (Π), et le
passage à π exige l'inversion de Möbius que le script n'applique pas ;
(b) l'ordonnancement/Cesàro conditionnels de la somme sur ρ pour la
forme li n'est pas celui de la forme ψ, mieux comporte. Aucune
rétro-correction du critère gelé : passe 2 déclarée.

## 4. Passe 2 (gelée à l'avance)

1. Formule en **ψ(x)** (von Mangoldt), somme x^ρ/ρ — objet le mieux
   conditionné numériquement ; vérifier ψ(100) = 94 (valeur exacte
   déclarée) sous tolérance ±4.
2. Puis passage π ← Π par inversion de Möbius, critères redéclarés.
3. N = 1000 zéros, dps = 40 (V1 à son seuil légitime), cache unique.

## 5. Leçon

Le chantier le plus court de l'Antik a tenu sa promesse quand même :
il a **produit un fait** (l'identité des deux formes sur la ligne) et
il a **localisé une erreur** (structure Π/π) — les deux sont des gains
de la doctrine, et le 1/4 est publié comme tel.

## Passe 2 (2026-11-02, soir) — la forme ψ CONFIRMÉE, 3/5 avec deux
erreurs de calibration de fiche documentées

Script `src/t69b_psi.py` (fiche T69-PSI-2.0 gelée), verdict
`data/t69b_psi_verdict.json`. Vérité de référence calculée exactement en
séance (crible des premiers — rien lu de mémoire). 800 zéros mis en cache
(correction de la soirée : cache incrémental par paquets de 100, le cache
en fin de boucle initial perdait tout au timeout).

**Le résultat scientifique central :**

| x | ψ exact | ψ̂ (Cesàro 200, 800 zéros) | écart | tolérance gelée |
|---|---|---|---|---|
| 100 | 94,045 | 93,986 | **0,059** | 1,0 ✓ |
| 500 | 501,652 | 502,097 | **0,445** | 1,5 ✓ |
| 1000 | 996,681 | 997,307 | **0,626** | 2,5 ✓ |

**La formule explicite tient numériquement sous forme ψ** — l'échec de la
passe 1 était bien la structure Π/π, comme diagnostiqué : les mêmes zéros,
la même somme, le bon objet, et la machine reproduit ψ(x) au dixième près
sur trois points, sans aucune valeur importée (ψ exact recalculé par crible).

**Les deux critères refusés sont des erreurs de calibration de la fiche,
pas de la formule** — second et troisième exemple du chantier :
- C5 (levier, seuil gelé 50) : mesuré 4,1 — qui est *exactement* la
  contribution totale des zéros à x = 100 (ψ = x − Σ − log 2π → Σ = 4,12).
  Le levier fonctionne directionnellement et en magnitude exacte ; le seuil
  gelé supposait à tort une contribution « massive ». Seuil mal calibré,
  publié comme tel.
- C6 (identité en dps 40) : **exacte** (0,00e+00) ; C1 (cache, monotone)
  tenu.

**Bilan Antik complet.** Le gisement a livré : un pont vers la dynamique
(T68, 4/4), une confirmation numérique de la formule explicite sous forme ψ
(3/5, cœur tenu), un fait structurel (les deux formes Ei/Li coïncident sur
la ligne critique), et trois leçons de calibration gravées (précision de
dps, seuil de levier, cache incrémental). Le document Connes_Zýta est ainsi
répondu avec la précision de la maison : la correction est légitime, sans
effet numérique sur la ligne, et la formule explicite — son voisin —
reproduit le réel quand on la pèse sur le bon objet.

*Révision uniquement par note datée.*
