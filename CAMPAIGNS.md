# CAMPAIGNS.md — registre des campagnes et régulation post-campagne

Une **campagne** = un cycle de la machine portant **une** question (réponse : oui / non /
indécidable). Ce registre est le journal officiel des campagnes du corpus.

**Règle des trois tiroirs** — un seul par phrase :

| Tiroir | Signature | Exemple |
|---|---|---|
| **Carnet** | « j'explore » | analogies, correspondances ANU/E₈, pistes E1–E7 |
| **Banc** | « je calcule, voici le test » | scripts P0–P48, séries A/M, verdicts JSON |
| **Thèse** | « je prétends que » | énoncés de théorèmes, prédictions physiques |

Ce registre ne signe que le **banc**. Le site et les essais peuvent tout dire ; GitHub ne
signe que le test.

Références vivantes de l'écosystème :
- Registre canonique : https://index.portemann.eu/index.php?page=registre
- Table des tables : https://index.portemann.eu/index.php?page=tables
- Divergences : https://index.portemann.eu/index.php?page=divergences

---

## Modèle de fiche (à remplir AVANT chaque run)

```
### Campagne <ID> — <date>
- **Tiroir** : banc
- **Objet** : <structure candidate nommée — un mot = un objet>
- **Question unique** : <formulée pour une réponse oui / non / indécidable>
- **Conventions citées** : <IDs de CONVENTIONS.md>
- **Protocole** : <script, bornes, fenêtre — écrit AVANT le run>
- **Falsifieur** : <ce qui, s'il est observé, réfute>
- **Prédiction pré-enregistrée** : <valeur attendue, fixée avant le run>
- **Verdict** : <succès / partiel / B3-FAIL — publié au même niveau de titre>
- **Artefacts** : <chemins + empreintes SHA-256 (SHASUMS.txt)>
- **Registre des frontières** : <entrée F-…, statut>
```

---

## Boucle de régulation post-campagne (obligatoire)

Après **chaque** campagne, dans l'ordre :

1. **Parité des titres** — le verdict, succès OU échec, est publié au même niveau de titre
   que les succès précédents (README, notes, profil).
2. **Conventions** — toutes les conventions utilisées sont citées par ID dans
   `CONVENTIONS.md` ; toute convention nouvelle y est gelée et datée **avant** publication
   du verdict.
3. **Un mot = un objet** — relecture de la fiche : aucun terme ne sert à la fois de
   définition, de cible et de conclusion (« 7 », « bande », « machine », « théorème »…).
4. **Frontières** — le registre REG-FR-1.0 est mis à jour : fermée / ouverte / partielle,
   avec coût de fermeture déclaré et falsifieurs exécutables.
5. **Hash** — `SHASUMS.txt` est régénéré ; les artefacts morts (proxys, cibles abandonnées)
   sont marqués comme tels. Le hash atteste l'octet, pas l'axiome.
6. **Pas de critère déplacé** — si un critère change après un échec : clôture datée de
   l'ancienne question ET ouverture datée de la nouvelle. Jamais de déplacement silencieux.
7. **Alignement externe — « verdict → tables »** — les surfaces publiques sont alignées
   sur le verdict, y compris pour un B3-FAIL. Une valeur = une source unique : le
   **registre canonique** (index.portemann.eu) fait foi, tout le reste cite.

### Point 7 détaillé — checklist « verdict → tables »

À cocher après chaque verdict modifiant une valeur canonique :

- [ ] Valeur entrée au registre canonique (`data/registre.csv` de l'index), ou mention
      « inchangée » dans la note de campagne — avec statut ◆ établi / ◇ modèle /
      ◈ conjecture / ✗ réfuté, date de valeur, source, alias historiques conservés
- [ ] Statut épistémique cohérent avec la charte ◆/◇/◈/✗ du site
- [ ] Articles WordPress citant l'ancienne valeur : **addendum daté** en tête
      (corps conservé tel qu'écrit), lien vers le registre
- [ ] Page Divergences de l'index : écart marqué `resolue` (daté, pointant vers le
      registre) — jamais effacé
- [ ] Atlas machine-noetique : titre/compteurs alignés (ou relevé figé explicité)
- [ ] Chronologie : prédiction concernée mise à jour (valeur + date)
- [ ] Techniques : page concernée citant le registre (ex. Z_max dans `anu.php`)
- [ ] SPA (portemann.eu, noeticindustries.com) : compteurs et cartes alignés,
      cache-buster incrémenté
- [ ] `data/tables.csv` de l'index : ligne ajoutée ou contenu rafraîchi (nature de lien :
      calculé / mesuré / documentaire / analogique)
- [ ] Manifests des vhosts touchés incrémentés (version datée à chaque déploiement) ;
      relevé daté dans les pieds de page si la valeur canonique affichée change
- [ ] Vérification live de chaque propriété touchée (HTTP 200 + chaîne attendue)

---

## Historique (extrait régulé — à compléter à chaque campagne)

| Campagne | Date | Question unique | Verdict | Suites régulées |
|---|---|---|---|---|
| **A3** | 2026-08 | Le compte « 63 160 » est-il reproductible sous la logique publiée ? | **B3-FAIL** — 0 solution ; plafond codé en dur, axiomes proxys, certification vide → artefact | Frontière KO-6 **ouverte** ; erratum déposé sur `spectral-triple-minimality` (branche `gouvernance-corpus`) |
| **A3b** | 2026-08-31 | Un triplet minimal explicite passe-t-il les vrais axiomes (table C-KO6-A3b) ? | **SUCCÈS 4/4** — champion C4 (H_F = ℂ⁴) | Coquille F4 publiée ; étalon 4×4 vers `AXIOMES.md` |
| **F4** | 2026-08 | Combien de matrices sous vrais axiomes, k=2, dim=5 ? | **SUCCÈS 3/3** — 60/256 | ⚠️ Vigilance : le test d'existence ne dépend pas de m au-delà des filtres symétrie/bloc-vide — à documenter dans le verdict |
| **M1/M1b** | 2026-08 | Le postulat « discret bon marché » prédit-il un surplus d'information à r₁₂ ? | **RÉFUTÉ avec inversion** (Spearman 0,980) | Le slogan ne doit plus servir d'enseigne sans sa mesure (τ : 0,60 vs 1,00) |
| **P42** | 2026-08 | \|2I\| = racines⁺(E₈) = 120 et quiver de McKay ? | **SUCCÈS** (arithmétique) | Pont documentaire ≠ dérivation : l'identification physique du « 12 » reste hypothèse déclarée (F14 partielle) |
| **P44–P45** | 2026-08 | Les règles ReN zéro paramètre tiennent-elles sur EEG réel ? | **B3-FAIL** (règles réfutées) | Critère non déplacé : F17/F18 ouvertes et datées ; poursuite « sans ReN » explicitée |

---

## Corridor de falsification (fiches pré-enregistrées, non lancées — daté 07/09/2026)

Sept tests pré-enregistrés, chacun avec son falsifieur ; aucun n'est lancé à la date de
dépôt. Chaque lancement futur devient une campagne au sens du présent registre.

| Fiche | Test | Prédiction pré-enregistrée | Falsifieur |
|---|---|---|---|
| COR-BELL | Bell noétique, d = 1 m | S = 3,23 ± 0,05 (au-delà de 2√2) | S < 2,83 |
| COR-RMN | résonance ANU k = 3 | ΔB = 0,5 mT | pas de pic à B_res |
| COR-PATCH | patch-clamp sous champ focalisé | ΔV_m = −5 mV | \|ΔV_m\| < 1 mV |
| COR-FEXP | loi harmonique δ^n hors calibrage | F_exp ∈ [0,97 ; 1,03] sur particules non calibrées | hors corridor |
| COR-FISSION | pics secondaires de fission | A = 63, 110, 126, 173 | spectre lisse |
| COR-RNU | neutrinos, cible cristalline vs amorphe | R_ν ∝ e^(−β₄ΔS₄) | pas de contraste |
| COR-HZ | H(z) filtré par F₄ sans ajuster Ω_Λ | variation > 3–5 % sur H(z) | ajustement nécessaire |

Ces fiches sont pré-enregistrées lors du câblage du 07/09/2026 (entrée noetic-mdu) ;
leur lancement relève d'une décision d'auteur datée.

---

## Prochaine campagne candidate (tiroir banc)

**Q-KO6-2026-09** — *Sous la table C-KO6-A3b (datée), existe-t-il (D, J, γ) de taille n
impaire vérifiant l'ordre 1 avec un scalaire complexe unique ?*
Falsifieur : lemme ou énumération exhaustive montrant l'inexistence. Si oui : publication
des trois matrices, pas du récit. Si non : toute prétention de dimension impaire sort du
tiroir thèse.

---

*Registre ouvert le 2026-09-06, en réponse à la note de lecture « Incohérences internes du
corpus Portemann » (sept. 2026). Addenda seulement. Point 7 détaillé ajouté le 07/09/2026
lors du câblage de l'écosystème — il formalise la propagation appliquée pour Z_max = 180,
« 63 160 » réfuté, 11 dépôts publics et le corpus P0–P48.*