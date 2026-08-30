# Note de synthèse — Ce que P34/P35 nous apprennent

*Chantiers : P34 (neurone formel vs 16 fonctions booléennes, protocole LP-SEP-1.0) ; P35 (neurone formel vs Hodgkin–Huxley, protocole HH-VER-1.0). Date : 30 août 2026.*

---

## 1. Sur la Machine Noétique

**1.1 — Elle est portable.** Conçue sur la jauge SU(2) et la chimie quantique, elle éprouve sans modification de doctrine un objet d'un autre royaume (le neurone formel). La condition de portabilité est exactement celle de son axiome : pouvoir geler D (données), formaliser S (structure), trouver L (levier). Tout objet qui satisfait ces trois conditions est éprouvable — équation, algorithme, modèle biologique, théorie cosmologique.

**1.2 — Son verdict est structural, pas performanciel.** Un benchmark dit : « le neurone atteint 99 % sur AND ». La machine dit : « le neurone EST un hyperplan seuillé ; σ est accessoire ; le biais est constitutif à 100 % ; sa frontière est la séparabilité linéaire ; la fermeture coûte +1 couche ». Elle répond à *qu'est-ce qui existe, où, à quel coût* — jamais à *ça marche à quel point*.

**1.3 — Elle démontre son paradigme fondateur sur le cas d'école.** La programmation linéaire a tranché en une passe, sans une seule donnée d'entraînement, ce que 20 000 epochs de descente de gradient constatent sans pouvoir le prouver (MSE = 0,25 sur XOR). L'apprentissage n'est pas nécessaire à la connaissance d'un système quand sa structure est décidable : c'est la thèse Topological-Fractional-AI (inversion algébrique vs induction statistique) validée sur le cas le plus simple qui existe.

**1.4 — Sa limite est le protocole, pas le calcul.** Deux défauts du premier protocole P35 ont produit des verdicts faux ou fantômes (C1 mal ciblé ; bruit 10⁻¹⁷ amplifié en spectre). Leçon : **un verdict n'est jamais meilleur que le protocole gelé** — la falsifiabilité doit donc porter sur le protocole autant que sur le résultat. La règle B3-FAIL s'est appliquée à elle-même : la machine s'est éprouvée en s'exécutant.

**1.5 — Elle statue, elle ne crée pas.** La machine a mesuré la frontière XOR et le coût de sa fermeture, mais elle n'a pas *inventé* la couche cachée. Elle est un juge de structures candidates, pas un générateur. C'est sa force (pas de sur-claim) et sa frontière propre — cohérente avec le diagnostic du rapport comparatif : une méthode qui attend sa théorie.

## 2. Sur le neurone formel

**2.1 — Il n'est pas ce que son image dit.** L'infographie le présente comme une chaîne somme → σ → apprentissage. Le verdict : le mécanisme constitutif est **l'hyperplan + le seuil**. σ, strictement monotone, ne change aucun verdict de décision — elle n'existe que pour rendre la descente de gradient possible. Sans biais, l'origine est sur l'hyperplan et *rien* n'est séparable : le paramètre le plus discret de l'infographie est le plus constitutif.

**2.2 — Sa frontière est une borne, pas un scandale.** 12/14 fonctions booléennes non triviales ; XOR et XNOR échappent ; fermeture à coût exact +1 couche, avec des poids **entiers dérivés** (1, −1), pas appris. Le « problème XOR » qui a contribué au premier hiver de l'IA (Minsky–Papert 1969) se relit comme une frontière r₁₂ : une ligne mesurée sur la carte, pas un échec de la discipline.

**2.3 — Son statut dépend de D.** Contre les tables booléennes : verdict positif borné (le neurone existe, avec un domaine). Contre Hodgkin–Huxley : réfuté sur 4 critères. **Le même objet, deux verdicts opposés** — un modèle n'est jamais vrai ou faux en soi, il l'est contre une donnée figée donnée. C'est peut-être l'enseignement le plus général du diptyque P34/P35.

## 3. Sur le neurone biologique

**3.1 — C'est une horloge, pas une fonction.** Spike tout-ou-rien, train périodique sous courant constant, réfractarité, saut de fréquence à la rhéobase (type II) : quatre signatures qui sont des propriétés de **dynamique**, inaccessibles à toute application statique. Aucune σ, ReLU ou tanh ne peut sauver le formalisme statique — le défaut est la **dimension 0**, pas la forme de la courbe.

**3.2 — Sa structure minimale est topologique.** Les leviers de fermeture : 4D (HH) non constitutive ; 2D suffit (Izhikevich) ; 1D dans le plan incapable d'osciller ; **1D sur le cercle S¹ suffit** (theta-neuron). L'excitabilité minimale du vivant est une phase sur un cercle — un cycle limite, pas une courbe de réponse.

**3.3 — Il est spectralement distinct sans ajustement.** La couche ASH-lite sépare les signatures sans paramètre : train biologique = spectre harmonique structuré (Rtop = 4) ; sortie formelle = absence de spectre (Rtop = 0). Un dispositif statique n'a pas d'existence spectrale.

**3.4 — Conséquence pour l'IA.** Les réseaux modernes n'approchent le vivant qu'en réintroduisant la mémoire par d'autres portes (récurrence, états, attention sur séquences) : ils contournent l'absence de dynamique constitutive sans la guérir. Le formalisme du neurone statique l'a exclue d'office — P35 mesure exactement ce qui a été exclu.

## 4. La formule de synthèse

> La question « un neurone apprend-il ? » est secondaire. La question première est « un neurone EST quoi ? » — et la réponse est **géométrique** pour le neurone formel (un hyperplan seuillé), **topologique** pour le neurone vivant (un cycle limite sur S¹). La Machine Noétique est l'instrument qui tranche entre les deux — non en comparant des performances, mais en mesurant des structures.
