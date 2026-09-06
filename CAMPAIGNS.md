# CAMPAIGNS.md — Boucle de régulation du corpus

> Après chaque campagne (chantier P/A/M/F), le verdict n'est complet que lorsque
> les **tables de l'écosystème** reflètent la nouvelle valeur. Une valeur = une source
> unique : le **registre canonique** (index.portemann.eu) fait foi ; tout le reste cite.

Références vivantes :
- Registre canonique : https://index.portemann.eu/index.php?page=registre
- Table des tables : https://index.portemann.eu/index.php?page=tables
- Divergences : https://index.portemann.eu/index.php?page=divergences

## Règles héritées (inchangées)

B3-FAIL (échecs publiés) · C12.1 (protocoles gelés) · *fermer, ne pas ajouter* ·
*conserver les versions* (addenda datés seulement) · *motivation, pas postulat*.

## La boucle (7 points)

1. **Artefacts figés** — script + JSON + figure produits, empreintes ajoutées à `SHASUMS.txt`.
2. **Verdict publié** — `data/<chantier>_verdict.json` + note dans `docs/` ; l'échec est
   publié avec le même soin que le succès.
3. **Registre canonique** — si une valeur canonique change (ou apparaît) : entrée créée ou
   mise à jour dans `data/registre.csv` de l'index, avec statut ◆ établi / ◇ modèle /
   ◈ conjecture / ✗ réfuté, date de valeur, source, alias historiques conservés.
4. **Divergences** — toute valeur contradictoire ailleurs dans l'écosystème est marquée
   `resolue` (datée, pointant vers le registre) — jamais effacée.
5. **Table des tables** — si la campagne produit une nouvelle table/registre structuré :
   ligne ajoutée à `data/tables.csv` (nature : calculé / mesuré / documentaire / analogique).
6. **Manifests** — `manifest.json` de chaque vhost touché incrémenté (discipline Cockpit :
   version datée à chaque déploiement).
7. **Checklist « verdict → tables »** — propagation dans l'écosystème (voir ci-dessous).

## Point 7 — Checklist « verdict → tables »

À cocher après chaque verdict modifiant une valeur canonique :

- [ ] Valeur entrée au registre canonique (ou mention « inchangée » dans la note de campagne)
- [ ] Statut épistémique choisi et cohérent avec la charte ◆/◇/◈/✗
- [ ] Articles WordPress citant l'ancienne valeur : **addendum daté** en tête
      (corps conservé tel qu'écrit), lien vers le registre
- [ ] Atlas machine-noetique : titre/compteurs alignés (ou relevé figé explicité)
- [ ] Chronologie : prédiction concernée mise à jour (valeur + date)
- [ ] Techniques : page concernée citant le registre (ex. Z_max dans `anu.php`)
- [ ] SPA (portemann.eu, noeticindustries.com) : compteurs et cartes alignés,
      cache-buster incrémenté
- [ ] `tables.csv` : ligne ajoutée ou contenu rafraîchi
- [ ] Relevé daté dans les pieds de page si la valeur canonique affichée change
- [ ] Vérification live de chaque propriété touchée (HTTP 200 + chaîne attendue)

## Traçabilité

Chaque passage de boucle laisse : un commit SHA (ici), une version de manifest (par vhost),
un relevé daté (footers), et le cas échéant un addendum daté (WordPress). Le registre des
divergences conserve la mémoire des valeurs réfutées — la trace de l'erreur fait partie de
la démarche.

---

*Fichier créé le 07/09/2026 lors du câblage de l'écosystème (phases 1–6). Le point 7
formalise ce qui a été appliqué pour Z_max = 180, « 63 160 » réfuté, 11 dépôts publics
et le corpus P0–P48.*
