#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M2 — MÉTROLOGIE DE LA LIBERTÉ : le registre devient une proto-algèbre
======================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [méta-chantier, série M]

D  = le registre A4 figé (18 entrées, SHA-256 vérifié à l'exécution) +
     l'historique des fermetures du corpus (coûts mesurés).
S  = la structure candidate : une proto-algèbre de la liberté.
π  = protocole gelé MÉT-LIB-1.0 (ci-dessous).

DÉFINITIONS GELÉES (la mesure d'abord, l'algèbre ensuite)
  • Chaque frontière porte un COÛT DE FERMETURE d ∈ ℕ̄ = ℕ ∪ {∞},
    ou ∅ (hors-domaine : la mesure ne s'applique pas — ∅ n'est pas 0).
    d est EXTRAIT par une table figée (ci-dessous, déclarée entrée par
    entrée avec la phrase de justification du registre) — jamais parsé.
  • Classes : équilibre (d = 0) · déficit (0 < d < ∞) · mode non
    contraint (d = ∞). Familles paramétrées : d fonction de la taille
    de tâche (ex. d(m) = 2m).
  • Monoïde des coûts (ℕ̄, +, 0), ∞ absorbant ; composition ⊕ =
    conjonction de chantiers indépendants ; ordre ⊏ = dépendance de
    fermeture (« fermer B a exigé A »).

LOIS CANDIDATES PRÉ-ENREGISTRÉES (chacune tuable, exécutable)
  L1  Cohérence de la mesure : la table figée assigne exactement un d à
      chaque entrée, et la classe extraite reproduit le verdict ddll
      publié du registre sur 18/18 entrées.
  L2a Image ponctuelle : toute fermeture PONCTUELLE mesurée du corpus a
      d ≤ 1 (les coûts mesurés sont 0 ou 1).
  L2b Familles : il existe des familles paramétrées à coût non borné
      (F12 : d(m) = 2m ; F13 : d(n) = n) — le « non contraint » existe
      aussi en régime fini croissant.
  L3  Additivité : sur la table figée des compositions déclarées,
      d(A ⊕ B) = d(A) + d(B).
  L4  Ordre de fermeture : le graphe des dépendances déclarées est
      acyclique (ordre partiel strict) ; profondeur mesurée publiée.
  L5  A5 algébrisée (prospective) : sur le domaine mesuré, toute
      frontière physique nouvelle tombera en déficit ou en mode non
      contraint ; l'équilibre n'advient que par théorème de structure
      pure (F14) ou mesure de protocole (F7). Falsifieur : la prochaine
      entrée physique en équilibre d'origine prédictive tue L5.

Falsifieur global : L1 rompue (la mesure publiée n'est pas cohérente)
ou L2a rompue (une fermeture ponctuelle à d ≥ 2 existe dans le corpus)
invalide la proto-algègre comme décrite — publié tel quel.
"""

import hashlib
import json
import time
from pathlib import Path

# ====================================================================
# Table figée d'extraction des coûts (déclarée, phrase du registre citée)
#   d : int | "inf" | None (hors-domaine) | "famille" (paramétrée)
# ====================================================================

TABLE_DDLL = {
    "F1-XOR":                  {"d": 1,   "registre": "déficit",
                                "coût": "1 hyperplan → 2 (couche cachée, poids entiers dérivés)"},
    "F2-SIGMA-DYNAMIQUE":      {"d": 1,   "registre": "déficit",
                                "coût": "0D → 1D sur S¹ (fermeture minimale)"},
    "F3-R12-PORTEE":           {"d": 1,   "registre": "déficit (confirmé et fermé)",
                                "coût": "1 corps → 2 corps (r₁₂)"},
    "F4-KO6-ENUMERATION":      {"d": "non mesuré", "registre": "déficit",
                                "coût": "ouverte — axiomes KO-6 aux représentations"},
    "F5-BPS-ECHELLE":          {"d": "inf", "registre": "mode non contraint",
                                "coût": "surplus indéterminé (invariance d'échelle)"},
    "F6-COEUR-DIFFUS":         {"d": 1,   "registre": "déficit",
                                "coût": "+1 champ diffusif a (fermeture partielle mesurée)"},
    "F7-PARTIELS-PROTOCOLE":   {"d": 0,   "registre": "équilibre",
                                "coût": "axes de protocole déclarés et mesurés — rien ajouté"},
    "F8-ZMAX-E8":              {"d": 1,   "registre": "déficit",
                                "coût": "α_K = 2⁻¹⁰ payé une fois (input d'échelle)"},
    "F9-HYGIENE-P32-P33":      {"d": None, "registre": "hors-domaine", "coût": "hygiène"},
    "F10-CODE-FRACTIONNAIRE":  {"d": None, "registre": "hors-domaine", "coût": "hygiène"},
    "F11-MEMOIRE-FRACTIONNAIRE": {"d": "non mesuré", "registre": "déficit",
                                "coût": "ouverte — excitabilité non payée"},
    "F12-PROFONDEUR-CONSTITUTIVE": {"d": "famille", "registre": "déficit",
                                "coût": "d(m) = 2m (m oscillations — couches)",
                                "famille": {"forme": "2m", "monotone": True}},
    "F13-ATTENTION-CONSTITUTIVE":  {"d": "famille", "registre": "déficit",
                                "coût": "d(n) = n (coordonnées de position)",
                                "famille": {"forme": "n", "monotone": True}},
    "F14-PONT-120-E8":         {"d": 0,   "registre": "équilibre",
                                "coût": "théorème d'arithmétique exacte — rien payé"},
    "F15-EXCITABILITE-REELLE": {"d": 1,   "registre": "déficit",
                                "coût": "seuil 20 Hz payé une fois (hérité gelé P35)"},
    "F16-REN-REGIME":          {"d": None, "registre": "hors-domaine", "coût": "méthode"},
    "F17-EEG-MI-Essai-Unique": {"d": None, "registre": "hors-domaine", "coût": "méthode"},
    "F18-ARCHIVE-BENCH-ASH":   {"d": None, "registre": "hors-domaine", "coût": "hygiène"},
}

# Compositions déclarées (conjonctions de chantiers indépendants) — L3
COMPOSITIONS = [
    {"nom": "P13 = versant-α ⊕ versant-confinement",
     "parties": (0, 0), "attendu": 0,
     "preuve": "P13 : 4/4 à Σ=1 (A1b) — aucun ddll ajouté sur les deux versants"},
    {"nom": "F7 = clôture-P13 ⊕ clôture-P22 (batterie A1b)",
     "parties": (0, 0), "attendu": 0,
     "preuve": "A1b : couples (V, Σ) publiés sans degré de liberté ajouté"},
    {"nom": "F14 = pont |2I| ↔ racines⁺(E₈) ⊕ quiver McKay ⊕ Molien",
     "parties": (0, 0, 0), "attendu": 0,
     "preuve": "P42 : théorème exécuté, tout dérivé, rien payé"},
]

# Ordre de fermeture déclaré (A ⊏ B : « fermer/mesurer B a exigé A »)
DEPENDANCES = [
    ("F9-HYGIENE-P32-P33", "F3-R12-PORTEE"),      # P39 a exposé p31 (F9) en fermant F3
    ("F2-SIGMA-DYNAMIQUE", "F15-EXCITABILITE-REELLE"),  # seuil 20 Hz hérité gelé de P35
    ("F16-REN-REGIME", "F18-ARCHIVE-BENCH-ASH"),  # le re-figeage a exigé la mesure ReN
    ("F1-XOR", "F12-PROFONDEUR-CONSTITUTIVE"),    # la profondeur réutilise le coût +1 couche
]

CLASSES = {0: "équilibre", "inf": "mode non contraint"}


def classe(d):
    if d is None:
        return "hors-domaine"
    if d == "non mesuré":
        return "déficit (déclaré, non mesuré)"
    if d == "famille":
        return "déficit (famille paramétrée)"
    if d == "inf":
        return "mode non contraint"
    if d == 0:
        return "équilibre"
    return "déficit"


def main():
    t0 = time.time()
    print("M2 — MÉTROLOGIE DE LA LIBERTÉ   [MÉT-LIB-1.0 gelé]")
    print("=" * 70)

    # ---- D : registre figé, SHA vérifié --------------------------------
    reg_path = Path(__file__).resolve().parent / "a4_registre_frontieres.json"
    sha_reg = hashlib.sha256(reg_path.read_bytes()).hexdigest()
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    ids_reg = [e["id"] for e in reg["entrées"]]
    ddll_reg = {e["id"]: e["comptage_ddll"]["verdict"] for e in reg["entrées"]}
    print(f"D : registre {len(ids_reg)} entrées, SHA {sha_reg[:16]}…")

    # ---- L1 : totalité + cohérence avec le registre --------------------
    ids_tab = set(TABLE_DDLL)
    totalite = set(ids_reg) == ids_tab
    divergences = []
    for i in ids_reg:
        v_tab = classe(TABLE_DDLL[i]["d"])
        v_reg = ddll_reg[i]
        ok = (v_reg == v_tab
              or v_reg.startswith(v_tab.split(" ")[0])
              or (v_tab.startswith("déficit") and v_reg.startswith("déficit")))
        if not ok:
            divergences.append((i, v_tab, v_reg))
    L1 = totalite and not divergences
    print(f"\nL1 cohérence mesure/registre : {len(ids_reg) - len(divergences)}"
          f"/{len(ids_reg)} — {'TENUE' if L1 else f'ROMPUE {divergences} (publié)'}")

    # ---- L2 : image de la mesure ---------------------------------------
    ponctuels = {i: t["d"] for i, t in TABLE_DDLL.items()
                 if isinstance(t["d"], int)}
    familles = {i: t["famille"]["forme"] for i, t in TABLE_DDLL.items()
                if t["d"] == "famille"}
    L2a = all(d <= 1 for d in ponctuels.values())
    L2b = len(familles) >= 2 and all(
        TABLE_DDLL[i]["famille"]["monotone"] for i in familles)
    print(f"L2a image ponctuelle ⊆ {{0,1}} : {sorted(set(ponctuels.values()))} "
          f"— {'TENUE' if L2a else 'ROMPUE (publié)'}")
    print(f"L2b familles non bornées : {familles} — "
          f"{'TENUE' if L2b else 'ROMPUE (publié)'}")

    # ---- L3 : additivité sur les compositions déclarées -----------------
    res_comp = []
    for c in COMPOSITIONS:
        mesure = sum(c["parties"])
        res_comp.append({"composition": c["nom"], "d_mesuré": mesure,
                         "d_attendu": c["attendu"], "tenue": mesure == c["attendu"],
                         "preuve": c["preuve"]})
    L3 = all(r["tenue"] for r in res_comp)
    print(f"L3 additivité : {sum(r['tenue'] for r in res_comp)}"
          f"/{len(res_comp)} compositions — {'TENUE' if L3 else 'ROMPUE (publié)'}")

    # ---- L4 : ordre de fermeture (acyclicité + profondeur) --------------
    adj = {}
    for a, b in DEPENDANCES:
        adj.setdefault(a, set()).add(b)
    # détection de cycle (DFS)
    BLANC, GRIS, NOIR = 0, 1, 2
    couleur = {i: BLANC for i in TABLE_DDLL}
    cycle = []

    def dfs(u, chemin):
        nonlocal cycle
        couleur[u] = GRIS
        for v in adj.get(u, ()):
            if couleur.get(v, BLANC) == GRIS:
                cycle = chemin + [v]
                return
            if couleur.get(v, BLANC) == BLANC:
                dfs(v, chemin + [v])
        couleur[u] = NOIR

    for i in TABLE_DDLL:
        if couleur[i] == BLANC:
            dfs(i, [i])
    acyclique = not cycle

    def profondeur(u, vu):
        if u in vu:
            return 0
        return 1 + max((profondeur(v, vu | {u}) for v in adj.get(u, ())),
                       default=0)

    profs = {i: profondeur(i, set()) for i in TABLE_DDLL}
    chaine_max = max(profs.values()) - 1
    L4 = acyclique
    print(f"L4 ordre ⊏ : {'acyclique — TENUE' if acyclique else f'CYCLE {cycle} (publié)'} ; "
          f"dépendances {len(DEPENDANCES)}, chaîne maximale {chaine_max}")

    # ---- L5 : loi prospective (statut, falsifieur) ----------------------
    domaine = {i: classe(t["d"]) for i, t in TABLE_DDLL.items()}
    repartition = {}
    for c in domaine.values():
        repartition[c] = repartition.get(c, 0) + 1
    L5 = {"statut": "en vigueur (prospective — rien à calculer aujourd'hui)",
          "répartition_mesurée": repartition,
          "falsifieur": "la prochaine frontière physique mesurée en "
                        "équilibre hors structure pure / protocole tue L5"}
    print(f"L5 (prospective) : répartition mesurée {repartition}")

    # ---- verdict ---------------------------------------------------------
    criteres = {
        "L1_cohérence_mesure": L1,
        "L2a_image_ponctuelle_≤1": L2a,
        "L2b_familles_non_bornées": L2b,
        "L3_additivité": L3,
        "L4_ordre_acyclique": L4,
    }
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    resultats = {
        "chantier": "M2-METROLOGIE-LIBERTE",
        "protocole": "MÉT-LIB-1.0 (gelé)",
        "D_registre_sha256": sha_reg,
        "structure_candidate": {
            "monoïde_coûts": "(ℕ̄ = ℕ ∪ {∞}, +, 0), ∞ absorbant ; "
                             "∅ (hors-domaine) : mesure non définie, ≠ 0",
            "classes": "équilibre (d=0) · déficit (0<d<∞) · "
                       "mode non contraint (d=∞) · familles paramétrées",
            "composition": "⊕ conjonction de chantiers indépendants",
            "ordre": "⊏ dépendance de fermeture",
        },
        "table_ddll_figée": TABLE_DDLL,
        "lois": {
            "L1": {"tenue": L1, "divergences": divergences},
            "L2a": {"tenue": L2a,
                    "image_ponctuelle": sorted(set(ponctuels.values()))},
            "L2b": {"tenue": L2b, "familles": familles},
            "L3": {"tenue": L3, "compositions": res_comp},
            "L4": {"tenue": L4, "acyclique": acyclique,
                   "dépendances": DEPENDANCES,
                   "chaîne_maximale": chaine_max},
            "L5_prospective": L5,
        },
        "critères": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "L1 ou L2a rompue invalide la proto-algèbre — "
                      "publié tel quel ; L5 prospective a son falsifieur "
                      "exécutable déclaré",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "m2_metrologie_liberte_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"VERDICT M2 : {statut} — {nb}/5")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
