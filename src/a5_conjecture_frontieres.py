#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A5 — CONJECTURE DES FRONTIÈRES : méta-loi éprouvée sur le registre
==================================================================
Conjecture v1 (programme de prospection) :
  « Toute frontière mesurée est un déficit de dimension/degré de liberté. »

La méta-loi n'est pas discutée, elle est ÉPROUVÉE : le registre A4 est la
donnée figée D ; la conjecture est la structure candidate S ; le levier L
est la chasse au contre-exemple. Domaine déclaré (gelé avant agrégation) :
  — entrées de type physique ou méthode (l'hygiène de publication ne relève
    pas d'une loi de structure) ;
  — comptage_ddll tranché (les entrées « en attente de mesure » sont des
    points PRÉ-ENREGISTRÉS, pas des points acquis).

Protocole gelé CONJ-FR-1.0
  1. Agrégation : pour chaque entrée du domaine, le verdict comptage_ddll
     ∈ {déficit, mode non contraint, hors-domaine} — mesuré par le chantier
     source, jamais réinterprété ici.
  2. v1 est CONFIRMÉE si 100 % des points du domaine sont « déficit » ;
     un seul « mode non contraint » la tue.
  3. Si v1 tombe, une v2 raffinée est FORMULÉE À PARTIR du contre-exemple
     publié (pas avant) et ré-éprouvée sur le même domaine.
  4. Prédictions pré-enregistrées de v2 sur les entrées en attente
     (F7 partiels-protocole, F8 Z_max) : leur fermeture devra être un
     défaut de comptage de ddll — sinon v2 tombe à son tour.

Falsifieur
  v2 est tuée par toute frontière mesurée dont la fermeture ne change
  aucun comptage de degrés de liberté (ni ajout, ni contrainte, ni
  fixation de mode).
"""

import hashlib
import json
from pathlib import Path

REGISTRE = Path(__file__).with_name("a4_registre_frontieres.json")


def main():
    reg = json.loads(REGISTRE.read_text(encoding="utf-8"))
    entrees = reg["entrées"]

    domaine = [e for e in entrees
               if e["type"] in ("physique", "méthode")
               and not e["comptage_ddll"]["verdict"].startswith("hors-domaine")]
    attente = [e for e in entrees
               if e["comptage_ddll"]["verdict"].startswith("hors-domaine")
               and e["type"] in ("physique", "méthode")]

    points = {e["id"]: e["comptage_ddll"]["verdict"] for e in domaine}
    n = len(points)
    n_deficit = sum(1 for v in points.values() if v.startswith("déficit"))
    contre_exemples = {k: v for k, v in points.items()
                       if not v.startswith("déficit")}
    v1_confirmee = not contre_exemples

    print("A5 — CONJECTURE DES FRONTIÈRES   [protocole CONJ-FR-1.0 gelé]")
    print("=" * 70)
    print(f"domaine déclaré : {n} points mesurés "
          f"(types physique/méthode, comptage tranché)")
    for k, v in points.items():
        print(f"  {k:<24} {v}")
    print("-" * 70)
    print(f"v1 « toute frontière = déficit de ddll » : "
          f"{n_deficit}/{n} conformes")
    if v1_confirmee:
        v1_statut = "CONFIRMÉE"
        v2 = None
    else:
        v1_statut = f"RÉFUTÉE par {', '.join(contre_exemples)}"
        v2 = ("v2 (raffinée sur le contre-exemple publié) : toute frontière "
              "mesurée est un DÉFAUT DE COMPTAGE des degrés de liberté — "
              "déficit (structure manquante : hyperplan, état, champ, 2-corps, "
              "représentations) ou MODE NON CONTRAINT (direction sans coût : "
              "mode zéro d'échelle au point BPS)")
        couverts = sum(1 for v in points.values()
                       if v.startswith("déficit") or v == "mode non contraint")
        print(f"v2 couvre {couverts}/{n} points du domaine")
    print(f"verdict v1 : {v1_statut}")

    predictions = {e["id"]: "sa fermeture devra être un défaut de comptage "
                            "de ddll (sinon v2 tombe)"
                   for e in attente}

    resultats = {
        "chantier": "A5-CONJECTURE-FRONTIERES",
        "protocole": "CONJ-FR-1.0 (gelé) — registre A4 comme donnée figée, "
                     "domaine déclaré avant agrégation, aucune réinterprétation",
        "donnée": {"registre": reg["registre"],
                   "sha256_registre": reg["sha256_registre"]},
        "points_mesurés": points,
        "n_points": n,
        "conjecture_v1": {
            "énoncé": "toute frontière mesurée est un déficit de dimension/"
                      "degré de liberté",
            "conformes": f"{n_deficit}/{n}",
            "contre_exemples": contre_exemples,
            "statut": v1_statut,
        },
        "conjecture_v2": ({
            "énoncé": v2,
            "couverture_domaine": f"{couverts}/{n}",
            "statut": "en vigueur — éprouvée prospectivement sur les points "
                      "pré-enregistrés",
        } if v2 else None),
        "points_pré_enregistrés_en_attente": predictions,
        "b3_fail": ([f"v1 réfutée par {k} ({v})"
                     for k, v in contre_exemples.items()] if contre_exemples
                    else []),
        "falsifieur": "v2 est tuée par toute frontière mesurée dont la "
                      "fermeture ne change aucun comptage de degrés de "
                      "liberté (ni ajout, ni contrainte, ni fixation de mode)",
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).with_name("a5_conjecture_frontieres_verdict.json")
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\nSHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
