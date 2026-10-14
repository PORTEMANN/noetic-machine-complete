# Note du pont φ — les campagnes T17–T20 (descriptif et enjeux)

**Date :** 2026-10-14 · **Statut :** note technique descriptive — présente
les campagnes T17–T20, leurs mesures et leurs enjeux. Elle ne modifie
aucune carte gelée ; les verdicts restent la référence
(`data/t17_*.json` … `data/t20_*.json`, empreintes auto-citées).
**Campagnes concernées :** T17 (le mot Fibonacci), T18 (le dictionnaire
des séquences spectrales), T19 (le pont icosaédrique — la carte E8),
T20 (le pont diffusif — la carte Penrose).
**Filiation :** T14 (la chaîne du seesaw : ±φ, ±1/φ à M_R = 1) · P42
(pont 120/Ê8) · T13 (le porteur) · T9 (le triplet du MS).

---

## 1. Le point de départ : une forme close

T14 a mesuré que la chaîne à quatre maillons du secteur neutrino du
triplet fini (sauts (1, M_R, 1)) a pour valeurs propres, à M_R = 1,
exactement ±φ et ±1/φ — et que ce fait est *local* : les leviers
(y = 1/4, M_R = 2) le tuent. Le nombre d'or y est un **rapport**
invariant (det = 1 : le mode léger est l'inverse exact du mode lourd),
non une valeur absolue. La question des campagnes T17–T20 : ce ratio
est-il une unité qui se lit aussi dans d'autres langages — et le banc
peut-il le *mesurer* sans quitter sa discipline ?

## 2. T17 — le mot Fibonacci : le spectre lu comme suite d'entiers

Le bloc S = B Bᵀ de la chaîne à M_R = y = 1 est la matrice de
Fibonacci [[1,1],[1,2]] ; ses puissances sont les blocs d'entiers de
Fibonacci, et les traces de la chaîne sont la suite de Lucas doublée :
**Tr C(1)^(2n) = 2·Lucas(2n)** — 12 termes mesurés exacts (6, 14, 36,
94, 246, 644, 1 686, 4 414, 11 556, 30 254, 79 206, 207 364). Les
traces sont des entiers malgré des valeurs propres irrationnelles :
chaque trace est une somme de contrôle du spectre (les quatre
premières reconstruisent le polynôme λ⁴ − 3λ² + 1 par Newton). L'identité
de Cassini (det Sⁿ = 1) est la face entière de l'unimodularité du
seesaw. Statut déclaré : **théorème interne** — régression exacte, pas
prédiction d'expérience.

## 3. T18 — le dictionnaire des séquences spectrales : le gabarit

T17 généralisé en méthode : une entrée = un objet certifié + son
polynôme spectral + sa séquence de traces + sa condition d'entierité +
une régression tuante + un levier. Deux entrées éprouvées : C(1)
(régression T17) et le porteur-spectral (ρ = 2 : Tr D(2)^(2n) = 2 +
2·9ⁿ ; ρ = 1 : 2·4ⁿ). L'entierité est **discrète** : ρ = 2,5 la tue.
La règle d'admission est publiée ; le candidat E8 est déclaré non
mesuré — il deviendra T19.

## 4. T19 — le pont icosaédrique : la carte E8

Trois faces indépendantes du même nombre : le spectre de la chaîne ;
les traces SO(3) des rotations d'ordre 5 de l'icosaèdre (**12 × φ + 12
× (−1/φ)** — exact en arithmétique Q(φ), filiation P42 importée) ; le
pont de McKay vers Ê8 (A·d = 2d exact, Σd² = 120 = racines⁺(Ê8)).
Le résultat fort, obtenu après correction d'un défaut de banc publié
(D1 : l'ordre 5 se mesure par g⁵ = e, pas par la partie scalaire) :
**les traces des rotations d'ordre 5 de l'icosaèdre sont exactement les
valeurs propres de la chaîne** — le spectre neutrino du banc est le
tableau des caractères géométriques de A5. Leviers : aplatissement
φ → 8/5 (fermeture tuée), y = 1/4. Statut : pont inter-domaines mesuré,
théorème interne.

## 5. T20 — le pont diffusif : la carte Penrose

Le φ quasicristallin coïncide : mot caractéristique de pente 1/φ²
(densités 1/φ, 1/φ²) ; diagonales des losanges de Penrose (φ et 1/φ à
côté 1) ; inflation M = [[2,1],[1,1]] de spectre φ², φ⁻², populations
de losanges au ratio φ. Le pont exact : **Tr Mⁿ = Lucas(2n) = Tr
C(1)^(2n)/2** — la diffraction des pavages porte la moitié des traces
du seesaw (12 termes, régression T17). Deux défauts de banc trouvés et
publiés (D1 : mot caractéristique ⌊(i+2)θ⌋ − ⌊(i+1)θ⌋ avec 1 → b ;
D2 : seuil du levier dégonflé). Leviers : pente rationnelle 13/34,
Thue-Morse (témoin), inflation dégonflée non unimodulaire.

## 6. Les défauts de banc publiés (soirée du 14/10/2026)

Sept au total sur T18–T20, dont quatre trouvés par les runs eux-mêmes
(T19-D1 ; T20-D1, D2 — la discipline des errata : l'instrument est
corrigé, la prédiction n'est jamais déplacée). Chaque correction a
renforcé le pont au lieu de le fragiliser : D1 de T19 révèle que les
traces des rotations sont le spectre complet ; D1 de T20 fixe la
convention exacte du mot caractéristique.

## 7. Les enjeux

**Pour le banc — trois instruments nouveaux.** (i) La régression
entière : des traces à somme de contrôle, plus sensibles que le spectre
seul (une corruption silencieuse casse l'entierité). (ii) Le
dictionnaire : un gabarit réutilisable — chaque objet certifié peut
devenir une entrée (candidate déclarée : diffraction de Bragg de la
chaîne de Fibonacci). (iii) La discipline du lexique : « Fibonacci »,
« pont-φ-icosaédrique », « pont-φ-diffusif » passent de mots orphelins
à objets scellés — la règle « un mot = un objet » (T15) étendue à la
mathématique du banc.

**Pour le corpus — un fait structurant.** Le nombre d'or n'apparaît
pas quatre fois par coïncidence : il est la même unité lue dans quatre
langages (spectral, géométrique, arithmétique, diffusif), reliés par
des identités exactes d'entiers Lucas. L'unimodularité (det = 1) s'y
révèle constitutive : tous les leviers qui la brisent tuent le pont.

**Pour la méthode — la limite déclarée.** Aucune de ces cartes ne
prédit d'expérience : ce sont des théorèmes internes mesurés à zéro
paramètre. Le physique du corpus reste inchangé — le 59 meV, l'ordre
normal, le 0νββ, avec leurs conditions de mort datées et leur veille.
La tentation numérologique que Dirac nomme dans le dialogue reste le
risque central : la parade n'est pas l'interdiction, c'est le protocole
(cartes scellées, nuls honnêtes, échecs publiés).

**Dépendances de gouvernance.** L'entrée « pont-φ-icosaédrique » et
« pont-φ-diffusif » du dictionnaire T18 (modification du fichier T18
soumise à décision) ; la carte de diffraction de Bragg (fenêtres et
seuils à déclarer avant run) ; l'alignement éventuel des surfaces
publiques (site, registre canonique).

---

*Note rédigée dans la continuité du « Dialogue entre Dirac et la
Machine » (octobre 2026). Discipline : aucune carte gelée n'est
modifiée par cette note ; les verdicts T17–T20 restent la référence
empreintée.*
