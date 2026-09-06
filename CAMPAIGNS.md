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
7. **Alignement externe** — les surfaces publiques (README des dépôts satellites, profil
   PORTEMANN, index portemann.eu) sont alignées sur le verdict, y compris pour un B3-FAIL.

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

## Prochaine campagne candidate (tiroir banc)

**Q-KO6-2026-09** — *Sous la table C-KO6-A3b (datée), existe-t-il (D, J, γ) de taille n
impaire vérifiant l'ordre 1 avec un scalaire complexe unique ?*
Falsifieur : lemme ou énumération exhaustive montrant l'inexistence. Si oui : publication
des trois matrices, pas du récit. Si non : toute prétention de dimension impaire sort du
tiroir thèse.

---

*Registre ouvert le 2026-09-06, en réponse à la note de lecture « Incohérences internes du
corpus Portemann » (sept. 2026). Addenda seulement.*
