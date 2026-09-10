# Campagne E56 — tressage sous rotation avec ancrage des pieds (LOCALE, protocole gelé, NON LANCÉE)

**Statut : protocole gelé et haché le 09/09/2026 (`5760eae7…03cf1f`) —
aucune donnée de campagne n'existe. Staging local.**

- **Objet** : « falsifieur désigné de la loi T6 » — tressage sous rotation
  avec ancrage des pieds de lignes (puits gaussiens U0=2, σ=1,5, grille
  pas 8, aux deux chapeaux, dès t=0) ;
- **Question unique** : l'ancrage des pieds fait-il persister le tressage
  nucléé ? La loi T6 prédit OUI (directionnel pré-enregistré) ;
- **Filiation** : harnais d'E54-C repris, seul ajout gelé : l'ancrage des
  chapeaux ;
- **Règle de verdict** : SUCCÈS si P0+P1+P2 (première conservation de
  RELATION mesurée) ; **B3-FAIL si P2 faux — la loi T6 est réfutée par son
  falsifieur désigné, publiée réfutée au même niveau** ;
- Harnais : `src/e56_run.py` (`7ca13d6b…cabc06`), validé en
  --smoke.

## Verdict — 09/09/2026 (exécution locale) : SUCCÈS formel + note de marge déclarée

**Règle gelée : P0 ✓ (médiane 15,0 ∈ [9,19], structure axiale dans les 6
graines), P1 ✓ (tressage nucléé : 4/6 graines, jusqu'à 42 paires à t=20),
P2 ✓ (une paire tressée à t≤20 et des paires tressées à t=45 dans le même
run — 440204) → SUCCÈS. La loi T6 tient son falsifieur désigné : l'ancrage
des pieds fait persister la relation.**

### Note de marge (déclarée — précédent E46)

L'effet est réel mais fin : la persistance repose sur **un run** (440204) ;
les 5 paires de t=45 partagent toutes le même filament et sont assises
**exactement au seuil** (|w| = 0,5) ; à t=90, plus rien. Sans ancrage
(E54-C) : 0 paire tardive nulle part. Donc : l'ancrage produit un effet
mesuré (0 → 1 run, braises tardives présentes) mais marginal. La
robustesse (plus de graines, marge d'enroulement au-dessus du seuil)
relève d'une campagne d'extension à geler séparément si l'auteur le
décide — jamais d'un re-seuilage.

### Mesures d'ensemble

- Comptes axiaux t=45/90 : [17,15,17,12,12,12,22,15,13,15,18,13] —
  médiane 15,0 (vs 13,0 sans ancrage : l'ancrage ajoute des lignes) ;
- Nucléation du tressage amplifiée par l'ancrage : 440205 passe de 2 à 35
  paires à t=8 ;
- Le contrôle de reproduction d'E54-A est désactivé par déclaration
  (géométrie modifiée par les puits — protocole).

### Statut régulé

La loi T6 (objet ⟺ non contractile ; relation ⟺ non contractile ∧ ancré)
n'est pas réfutée par son falsifieur désigné — elle est corroborée,
faiblement (note de marge). Première conservation de RELATION mesurée
dans le corpus. Si l'auteur veut la robustesse : extension E56-x à geler
(plus de graines, statistique de marge au-dessus du seuil) — sinon la
frontière « conservation de la relation » passe de « ouverte » à
« existante mais marginale sous ancrage de chapeaux ».
