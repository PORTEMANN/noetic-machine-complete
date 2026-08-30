# M1b — Robustesse de l'inversion : la réfutation de M1 ne dépend pas du compteur

**Patrice Portemann — corpus Machine Noétique, méta-chantier M1b**
Protocole gelé ECO-1.1 · zéro paramètre ajusté · SHA-256
30 août 2026

## Verdict

**PRÉDICTION PRÉ-ENREGISTRÉE : CONFIRMÉE.** L'inversion mesurée en M1
(le ratio V/S est plus *élevé* à la frontière r₁₂, pas plus bas) survit
au remplacement du compteur SLOC par la taille gzip du script — un
proxy de Kolmogorov plus fidèle : ρ₁′ médiane frontière **0.0323** vs
0.0105 ; ρ₂′ médiane frontière **0.0031** vs 0.0016. La réfutation du
postulat brut est **structurelle, pas un artefact du compteur de
longueur**.

## Protocole (gelé avant calcul)

- Identique à ECO-1.0 (même corpus de 23 chantiers, mêmes exclusions,
  mêmes V₁ feuilles et V₂ confrontations, même groupe frontière
  F = {P31, P32, P33, P39}, même critère médiane), **sauf** :
  **S₂ = taille gzip du script** (niveau 9, mtime=0 — déterministe).
- **Contrôle interne gelé** : Spearman(SLOC, gzip) ≥ 0.5, sinon le test
  n'est pas un contrôle de robustesse (verdict suspendu, B3-FAIL
  protocole).
- **Prédiction gelée** (annoncée dans la note M1) : l'inversion survit,
  car son mécanisme — diagnostics minimaux à la frontière — est
  structurel.
- Enrichissement descriptif sans critère (déclaré) : V₃ = littéraux
  numériques distincts embarqués dans la source (tokens NUMBER, 0/1/2
  exclus).

## Mesures

- **Contrôle métrique : PASS** — Spearman(SLOC, gzip) = **0.980** : les
  deux compteurs ordonnent les scripts presque identiquement ; si
  l'inversion avait disparu, ce n'aurait pas été un effet « les deux
  métriques mesurent des choses différentes ».
- **Inversion sur ρ₁′ (feuilles/gzip)** : médiane F 0.0323 > NF 0.0105
  — **survit**.
- **Inversion sur ρ₂′ (confrontations/gzip)** : médiane F 0.0031 > NF
  0.0016 — **survit**.
- Le mécanisme est visible dans le détail : P32/P33 sont les scripts
  les plus **compressibles du corpus** (987–1029 octets gzip, les plus
  petits des 23 chantiers) tout en produisant des grilles de diagnostic
  denses ; P39 (fermeture r₁₂) concentre le plus grand JSON de mesures
  (347 feuilles) du corpus local.

## Lecture

- M1 + M1b ensemble ferment la question « est-ce le compteur ? » :
  SLOC et gzip (ρ_s = 0.98) donnent le même classement et la même
  inversion. Le résultat M1 — *ce qui s'effondre à r₁₂ est le taux de
  réussite τ des confrontations externes, pas le ratio informationnel
  brut* — tient avec deux compteurs de complexité de Kolmogorov
  indépendants dans leur principe (lignes physiques vs contenu
  compressé).
- V₃ (littéraux embarqués) montre un signal secondaire déclaré
  exploratoire : les chantiers discrets à succès embarquent *plus* de
  données dans S (P22 : 71, P21 : 62 littéraux) que les diagnostics de
  frontière (P32/P33 : 21) — cohérent avec le postulat affiné : en
  régime discret, on paie des **données** (D) et la structure dérive ;
  à la frontière, on paie une **forme** (ddll) que les données ne
  suffisent plus à contraindre.

## Artefacts

- `m1b_economie_robustesse.py` — SHA-256 `71ee5733d8b21d43…`
- `m1b_economie_robustesse_verdict.json`
- Mêmes données que M1 : `m1_corpus/` (miroir SHA-vérifié) + verdicts
  locaux P34–P42.

**Falsifieur (gelé)** : l'inversion disparaissant sur l'une des deux
métriques gzip aurait fait tomber la prédiction et requalifié M1 en
« réfutation fragile » — mesuré : elle survit sur les deux.
