# Note d'applications — les machines hors de la physique (proposition de doctrine)

**Date :** 2026-10-20 · **Tiroir :** carnet — **proposition de doctrine,
non adoptée** : adoption = décision d'auteur (un « oui » nomme la
version, un amendement la modifie).
**Origine :** document d'proposition joint (améliorations de la machine,
application en ligne sur histoire-des-sciences.eu) — abstraction de la
mécanique algorithmique (opérateur à tolérance gelée, testeur de
robustesse sous pré-enregistrement) vers cinq domaines d'application.
**Filiation :** [NOTE-BILAN-MACHINES](NOTE-BILAN-MACHINES.md) ·
[NOTE-POSITIONNEMENT-HISTORIQUE](NOTE-POSITIONNEMENT-HISTORIQUE.md) ·
la discipline commune (zéro paramètre ajusté, protocole gelé, dormeurs
publiés, empreintes).

---

## 1. Ce qui est juste dans la proposition

L'abstraction est légitime : la mécanique des machines n'est pas liée à
la physique. L'identification des cinq domaines est correcte et
l'intérieur des machines est bien compris :

1. **Métrologie industrielle, contrôle qualité, spatial/nucléaire** —
   mvcg comme certificats de conformité à tolérance gelée, cartes
   reproductibles à l'octet près.
2. **Crise de la reproductibilité** (biomédical, pharmacologie) — la
   règle de puissance obligatoire (CS0) contre les études
   sous-dimensionnées ; le scellement SHA-256 + OpenTimestamps contre
   le p-hacking.
3. **Finance quantitative** — le test de déformations contre le
   backtest overfitting (l'analogue exact de MCS-24 et de S8).
4. **Audit des modèles d'IA** — mvcg comme garde-fou déterministe
   rejetant les sorties physiquement incohérentes.
5. **Gouvernance des données publiques, fact-checking** — le registre
   de veille généralisé (prédictions scellées, conditions de mort
   datées, rejou automatique).

La formule de synthèse — *l'épistémologie transformée en code
exécutable, des notaires algorithmiques* — est la bonne carte de
visite. Ces machines « pèsent » ; tout domaine où des humains peuvent
tordre des chiffres pour confirmer leurs intuitions est un domaine
d'application honnête.

## 2. Les trois tensions à régler avant tout développement

**Tension 1 — SaaS contre vérifiabilité.** La valeur des machines tient
dans : régénération = mêmes octets, MIT, reproductible par quiconque.
Un service qui cache le calcul derrière une API réintroduit le problème
de confiance que les machines résolvent. Personne ne doit croire le
serveur : il doit pouvoir *rejouer* la pesée. **Forme correcte : les
outils restent MIT sur GitHub (canonique) ; le service héberge ce qui ne
se rejoue pas — scellements, registres publics, horodatages, tableaux de
bord.**

**Tension 2 — pression commerciale contre culture du dormeur.** Un
service qui vend des « stratégies certifiées » fera pression pour que
la machine certifie. Les 52 errata et les dormeurs publiés sont la
source de la crédibilité : tout service dérivé publie ses CSp/CS−/CSi
au même titre que ses CS+. **La discipline voyage, ou rien ne voyage.**

**Tension 3 — contamination du corpus.** La force du dossier physique
(59 meV scellé, veille trimestrielle) vient de son historique.
Les applications vivent sur des registres **séparés et marqués** ; la
trace scientifique reste canonique.

## 3. La forme recommandée (à adopter ou amender)

Non pas un SaaS de calcul, mais : **les vérificateurs MIT et gratuits ;
le service vendu = hébergement de registres, curation, registres
d'entreprise, tableaux de bord — jamais le calcul.**

## 4. Feuille de route proposée (trois phases)

- **Phase 1 — les registres publics scellés** (le moins cher, le plus
  vite) : sur histoire-des-sciences.eu, une page « registre » où l'on
  dépose un hash de protocole, ancré (OpenTimestamps/Git), avec moteur
  de rejou trimestriel — le registre de veille généralisé.
- **Phase 2 — la pesée publique** : démo vivante où l'on colle une
  sortie d'IA (prédiction physique, bilan d'énergie) et où un opérateur
  mvcg-style rend un verdict immédiat — le garde-fou du domaine 4 rendu
  visible et pédagogique.
- **Phase 3 — les pilotes** (filtre anti-overfitting en finance, sceau
  de protocole en recherche) avec publication systématique des dormeurs.

## 5. Gouvernance

Note proposée le 2026-10-20 ; rien n'est scellé. Adoption = décision
d'auteur ; amendements bienvenus (les tensions peuvent être re-pondérées,
la feuille de route réordonnée). Ce qui n'est pas négociable dans
l'esprit de la proposition : la vérifiabilité rejouable, les dormeurs
publiés, les registres séparés.
