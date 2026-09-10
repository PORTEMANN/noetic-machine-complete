# Campagne E58 — réseau imprimé (LOCALE, 09/09/2026)

## Verdict v1 : B3-FAIL-TECHNIQUE (cause identifiée et mesurée)

**P0 échoue → la règle gelée prononce B3-FAIL-TECHNIQUE.**

- Validation d'instrument (--smoke64, sans évolution) : la construction
  est exacte — 27/27 lignes lues, ψ6=1,0 à l'écriture ;
- Mais la relaxation gelée (100 pas, γ=0,3, paroi commensurable au quantum
  27) a dégradé l'état avant le départ : **44 lignes à l'entrée (contre 27
  écrites) et ψ6 1,0 → 0,26**. Cause mesurée : la paroi à circulation 27
  injecte des vortex (forte torsion de phase dans un anneau mince) et la
  relaxation dissipe l'ordre ;
- Bras B (témoin brassé) : ψ6 monte 0,07 → 0,43 à t=90 (ordre partiel
  spontané, sous le seuil — observationnel).

La question physique (l'ordre écrit persiste-t-il ?) est NON TESTÉE —
non réfutée. Réparation déclarée : **E58-A** — relaxation SANS paroi
(boîte libre), paroi commensurable enclenchée à t=5 (entrée) ; haché
avant calcul.

## Verdict E58-A — 09/09/2026 : B3-FAIL-TECHNIQUE (2e série, cause identifiée)

**Le P0 gelé (compte 27 ± 3 ET ψ6 ≥ 0,7 à l'entrée) échoue sur la clause
de compte : 11 lignes à l'entrée.** La relaxation réparée (sans paroi) n'a
plus injecté de vortex — mais elle a drainé 16 des 27 lignes (les
périphériques, sans paroi pour les retenir) avant le départ. Ce n'est ni
l'instrument (27/27 lues à l'écriture, ψ6=1,0) ni la paroi (absente) :
c'est la préparation elle-même — la relaxation libre est une étape de
persistance hostile aux lignes périphériques.

### Compteurs consignés (hors verdict, règle gelée)

- Entrée : 11 lignes survivantes, ordre intact parmi elles (ψ6 = 0,93) ;
- Puis : ψ6 0,93 → 0,31 (t=45) → 0,05 (t=90) ; compte 11 → 18 → 20 ;
- Bras B (brassé) : ψ6 0,92 (entrée, sous-ensemble) → 0,30 → 0,43.

La trajectoire est visible dans les compteurs — l'ordre écrit ne persiste
pas sous rotation — mais le P0 gelé n'ayant pas passé, la campagne ne
statue pas. **J'arrête la chaîne de réparation ici** : la troisième
réparation (relaxation sous paroi faible, quantum ~4, pour retenir les
périphériques sans injecter) est une décision d'auteur, pas un réflexe —
deux B3-FAIL-techniques consécutifs disent que la famille « écrire puis
persister » exige une préparation qui est elle-même un mécanisme de
persistance. La frontière reste où T6/E56-x l'ont laissée.
