# Campagne E54-C — lignes tressées sous rotation, protocole corrigé (LOCALE, 09/09/2026)

**Verdict : PARTIEL_NUCLÉE_SEUL** — sous un protocole unique et corrigé
d'emblée (pas de chaîne d'amendements).

- P0 (compte axial dans la fenêtre publiée [9,19]) : **PASS** — médiane
  13,0, étendue 9–18 ;
- Contrôle de reproductibilité pré-enregistré : les compteurs d'E54-C sont
  **identiques à ceux d'E54-A** (vérifié champ par champ après
  normalisation des types ; le `false` initial du contrôle en ligne était
  un artefact de types tuple/liste dans le contrôle lui-même, documenté —
  les données concordent à l'identique) ;
- P1 (tressage nucléé) : **VRAI** ;
- P2 (persistance) : **FAUX** — la règle v1 prononce PARTIEL_NUCLÉE_SEUL.

Mesure : sous rotation, la structure axiale persiste, le tressage nuclée
mais ne persiste pas. L'objet non contractile persiste ; la relation
discrète entre objets ne persiste pas sans ancrage.

Protocole : `e54c_protocole.json` (`45376513…ba23f6e`) ; harnais
`src/e54c_run.py` (`d5a8dc88…98845ce027`) = E54-A sauf en-tête et
agrégation (déclaré) ; détecteur : filiation E44 byte-level.
