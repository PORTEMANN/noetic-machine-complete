# Campagne T4 — Q-KO6-T4-2026-09 (LOCALE, 09/09/2026)

**Statut : staging local — non publiée (pause de tri du 08/09/2026).**

## Objet

Transformer la régularité mesurée en T2 (100 % des combos « mélange »
admettent D≠0 à n=5,7) en **théorème prouvé**, et établir la
**classification complète** de l'existence des triplets (D, J, γ) à
deux scalaires (A = ℂ⊕ℂ) sous la table C-KO6-A3b, à n pair **et**
impair.

## Cadre (conventions citées)

Table C-KO6-A3b (datée) : J²=+1, Jγ=+γJ, JD=−DJ ; parité {D,γ}=0 ;
ordre 1 [[D,π(a)], Jπ(b)*J⁻¹]=0 ; D≠0. Espace : γ = diag(+1×a, −1×b) ;
P projecteur diagonal (secteurs ℂ⊕ℂ), Q = I−P ; J = J₀∘K, J₀ permutation
signée préservant les blocs de chiralité, J₀²=+1 ; D réel symétrique
hors-chiral.

## Faits élémentaires (dérivés)

**F1 — le signe ne mord que sur les points fixes.** J₀²=+1 impose
s_i·s_{σ(i)} = +1, donc s_i = s_{σ(i)} sur tout 2-cycle. Pour une
orbite {(x,y),(x′,y′)} de D (x′=σ(x), y′=σ(y)), la condition de signe
JD=−DJ se réduit à s_x s_y s_{x′} s_{y′} = +1 — **automatique** dès que
l'orbite est de longueur 2. Seule une orbite de longueur 1 (x et y
fixes) exige s_x s_y = −1.

**F2 — mélange ⟺ 2-cycle croisant les secteurs.** Points fixes et
2-cycles mono-secteur préservent S_P ; donc J₀ mélange (σ(S_P) ∉
{S_P, S_Q}) si et seulement s'il existe un 2-cycle (u,u′) dans un bloc
de chiralité avec P_u ≠ P_{u′}.

**F3 — ordre 1 par orbite.** Q′ = J₀QJ₀ reste diagonale
(Q′_αα = Q_{σ(α)}), et [[D,P],Q′]=0 se réduit, entrée par entrée, à
D_xy·(P_y−P_x)(P_{σ(x)}−P_{σ(y)}) = 0. Sur une orbite {(x,y),(x′,y′)}
(les deux entrées sont liées par JD=−DJ), la condition s'écrit :

    (P_x = P_y) ∨ (P_{x′} = P_{y′})        (∗)

**F4 — échange ⟹ a, b pairs** (lemme A de T2, confirmé machine) ; et en
échange P_{σ(i)} = 1−P_i, donc (∗) se réduit à P_x = P_y — la même
condition qu'en préservation.

## Théorème T-MÉLANGE — mélange ⟹ existence, pour tout n

**Preuve.** Par F2, soit (x,x′) un 2-cycle croisant dans H⁺
(P_x ≠ P_{x′}) — le cas H⁻ est symétrique.

*Cas 1 : H⁻ contient un point fixe y.* L'orbite {(x,y),(x′,y)} est de
longueur 2 (signe automatique, F1) et (∗) vaut (P_x=P_y) ∨ (P_{x′}=P_y)
— vrai, car P_x et P_{x′} couvrent les deux valeurs binaires. ∎

*Cas 2 : H⁻ sans point fixe (b pair, tout en 2-cycles).*
- *2a : un 2-cycle (y,y′) de H⁻ croise les secteurs.* Les deux orbites
  reliant {x,x′} à {y,y′} sont {(x,y),(x′,y′)} et {(x,y′),(x′,y)} ;
  leurs conditions sont (P_x=P_y)∨(P_{x′}=P_{y′}) et
  (P_x=P_{y′})∨(P_{x′}=P_y). Comme {P_y, P_{y′}} = {0,1} couvre les
  deux valeurs, l'une des deux orbites passe (∗). ∎
- *2b : tous les 2-cycles de H⁻ sont mono-secteur.* Alors
  P_{y′}=P_y pour tout y, et (∗) vaut (P_x=P_y) ∨ (P_{x′}=P_y) —
  couvert par P_x≠P_{x′}. ∎

(Le cas où le croisement n'existe que dans H⁻ se traite de même en
échangeant les rôles : point fixe de H⁺ (cas 1′), ou 2-cycle croisant
de H⁺ (cas 2a′), ou mono-secteur partout dans H⁺ (cas 2b′).)

**Remarque.** La parité de n ne joue aucun rôle : le théorème vaut à
n pair comme impair. L'asymétrie pair/impair vit uniquement dans la
classe échange (F4).

## Théorème T-CLASSIFICATION

Sous les bornes déclarées, l'existence de D≠0 équivaut à :

    mélange
    ∨ [ ∃ (x∈H⁺, y∈H⁻) même secteur avec
        (x ou y en 2-cycle)  ∨  (s_x·s_y = −1) ]

En préservation et en échange, l'ordre 1 se réduit à la condition
même-secteur (F3/F4) ; la condition de signe/cycle est F1. La classe
échange n'existe que si a et b sont pairs (F4).

## Vérification machine (protocole T4-KO6-MEL-1.0 gelé)

- **V1** : T-MÉLANGE vérifié exhaustivement à n ∈ {2,…,9} (signes
  collapsés, déclaré — la preuve n'utilise que des orbites de
  longueur 2) par la méthode des orbites, indépendante de la preuve ;
- **V2** : T-CLASSIFICATION vérifiée combo par combo à n ∈ {2,…,7}
  avec signes (formule du théorème == méthode des orbites) ;
- **V3** : échange ⟺ a,b pairs mesuré à n ∈ {2,…,9} ;
- **V4** : recoupement brutal à n=3 et n=4 — tous les D ∈ {0,±1}
  passés au vérificateur matriciel complet (A3b étendu), comptes par
  classe confrontés à la méthode des orbites.

Falsifieurs : un combo mélange sans D ; un écart formule/orbites ; un
échange à a ou b impair ; un mismatch brut.

## Verdict — CONTRÔLE GLOBAL PASS (09/09/2026)

- **V1** : T-MÉLANGE confirmé — 1 774 080 combos mélange à n=2…9, dont
  1 524 480 à n=9, **0 sans D** ;
- **V2** : T-CLASSIFICATION confirmée — 1 729 136 combos à n=2…7,
  **0 écart** entre la formule du théorème et la méthode des orbites ;
- **V3** : échange ⟺ a,b pairs confirmé — combos échange à n=4 (4),
  n=6 (48), n=8 (624) ; **0** à parité autre sur n=2…9 ;
- **V4** : recoupement brut conforme — n=3 (64/0/64) et n=4
  (1760/32/2624) identiques entre vérificateur complet et orbites ;
  noter : la classe échange **existe et porte des D** à n=4 (32 D),
  conformément au théorème (n pair, secteur bi-chiral).

Prédiction pré-enregistrée : confirmée en tous points.

## Conséquence pour le corpus

La classification des triplets KO-6 à deux scalaires est désormais
**close au niveau matriciel** : existence entièrement décidée par la
classe d'action de J sur les secteurs ; l'impair n'est exclu que pour
l'échange. La « question KO-6 » du corpus (frontière F4, partielle)
passe de « énumération coûteuse sous bornes » à « théorème de
classification prouvé + vérifié machine » — ce qui est exactement la
forme qu'une frontière fermée doit avoir dans ce programme.

## Artefacts

- `src/t4_ko6_lemme_melange.py`
- `data/t4_ko6_lemme_melange_verdict.json`
- empreintes complètes (octets du dépôt) : `data/t1_t2_t4_shasums.txt`
