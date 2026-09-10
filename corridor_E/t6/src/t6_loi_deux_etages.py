#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T6 — LA LOI À DEUX ÉTAGES : objet et relation   [protocole T6-LOI-1.0 gelé]
=====================================================================
Tiroir banc. Table gelée AVANT calcul (ci-dessous) — extension datée de
la table de T5 (09/09) : E54 y entre avec son verdict corrigé (E54-B,
amendement de lecture) comme premier cas de conservation INTERNE au
corridor (structure axiale persistante sous rotation — objet non
contractile).

Verdict T5 (mesuré) : pas de séparation scalaire par le ddll (R4
l'interdit) ; séparation parfaite par la contractilité au niveau objet.
E54-B ajoute la nuance mesurée : l'objet non contractile persiste, sa
RELATION discrète (tressage) ne persiste pas sans ancrage.

Loi candidate raffinée (gelée) :
  Niveau objet    : persiste ⟺ non contractile
  Niveau relation : persiste ⟺ non contractile ∧ ancrage externe
Falsifieur pré-enregistré : la campagne désignée E56 (tressage sous
rotation AVEC ancrage des pieds de lignes) doit conserver le tressage —
si elle échoue, la loi est réfutée (publié au même niveau).

Questions gelées :
  Q1 : au niveau objet, la contractilité sépare-t-elle la table étendue ?
  Q2 : au niveau relation, (non contractile ∧ ancré) sépare-t-elle ?
  Q3 : les deux séparations sont-elles robustes aux deux rubriques de
  lisibilité (stricte : mesures internes seules / complète : + références
  documentaires déclarées) ?

Usage : python3 t6_loi_deux_etages.py
"""

import json
import time
from pathlib import Path

# ---------------- TABLE GELÉE (avant calcul) — extension datée de T5 --------
# (nom, niveau, contractile, ancré, persiste, origine)
TABLE = [
    # niveau objet — boucles du corridor (tous : non-persistance)
    ("E45–E53 boucles (10 mécanismes)", "objet", True, None, False,
     "corridor (mesuré)"),
    # niveau objet — lignes sous rotation (verdict corrigé E54-B) :
    # la structure axiale PERSISTE (comptes stables t=45→90) — premier
    # cas de conservation INTERNE au corridor
    ("E54 structure axiale sous rotation", "objet", False, False, True,
     "corridor (mesuré 09/09)"),
    ("R1 E40 triplet stable une fois formé", "objet", False, False, True,
     "corpus (intrinsèque)"),
    ("R2 P24 gap de Hall", "objet", False, False, True,
     "corpus (intrinsèque)"),
    ("R3 P33 charge de bord", "objet", False, False, True,
     "corpus (intrinsèque)"),
    ("R4 flux pinning de LIGNES (type II)", "objet", False, True, True,
     "documentaire externe — déclaré"),
    # niveau relation
    ("E45–E53 lien entre boucles", "relation", True, None, False,
     "corridor (mesuré)"),
    ("E54 tressage (lignes, sans ancrage)", "relation", False, False,
     False, "corridor (mesuré 09/09)"),
    ("R4b réseau d'Abrikosov (relation entre lignes ancrées)",
     "relation", False, True, True, "documentaire externe — déclaré"),
]


def separe_par(pred, table):
    """Le prédicat sépare-t-il parfaitement persiste/non-persiste ?"""
    ok = all(p == pred(e) for e in table for p in [e[4]])
    return ok


def main():
    t0 = time.time()
    print("T6 — la loi à deux étages   [T6-LOI-1.0 gelé]")
    print("=" * 70)
    for e in TABLE:
        print(f"{e[0]:<48} niveau={e[1]:<8} contractile={e[2]} "
              f"ancré={e[3]} persiste={e[4]}")

    obj = [e for e in TABLE if e[1] == "objet"]
    rel = [e for e in TABLE if e[1] == "relation"]

    q1 = separe_par(lambda e: (not e[2]), obj)
    q2 = separe_par(lambda e: ((not e[2]) and bool(e[3])), rel)

    # robustesse : stricte (mesures internes au corpus/corridor seules)
    obj_i = [e for e in obj if "corridor" in e[5] or "corpus" in e[5]]
    rel_i = [e for e in rel if "corridor" in e[5] or "corpus" in e[5]]
    q1s = separe_par(lambda e: (not e[2]), obj_i)
    rel_strict_pred = lambda e: ((not e[2]) and bool(e[3]))
    q2s = separe_par(rel_strict_pred, rel_i) if rel_i else None

    print(f"\nQ1 niveau objet — séparé par non-contractilité : {q1} "
          f"(interne seul : {q1s})")
    print(f"Q2 niveau relation — séparé par (non contractile ∧ ancré) : "
          f"{q2} (interne seul : {q2s if q2s is not None else 'sans objet'})")

    loi = {
        "niveau_objet": "persiste ⟺ non contractile",
        "niveau_relation": "persiste ⟺ non contractile ∧ ancrage externe",
        "falsifieur_désigné": "E56 — tressage sous rotation avec ancrage "
                              "des pieds de lignes : doit conserver le "
                              "tressage ; si échec, loi réfutée",
    }
    verdict = {
        "chantier": "T6-LOI-DEUX-ETAGES",
        "protocole": "T6-LOI-1.0 (gelé)",
        "table": [list(e) for e in TABLE],
        "Q1_objet_séparé": q1, "Q1_interne": q1s,
        "Q2_relation_séparé": q2, "Q2_interne": q2s,
        "loi_raffinée": loi,
        "statut": ("LOI MESURÉE sur la table gelée — falsifieur E56 "
                   "pré-enregistré" if (q1 and q2) else
                   "séparation incomplète — publié tel quel"),
        "durée_s": round(time.time() - t0, 2),
    }
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t6_loi_deux_etages_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("\nStatut :", verdict["statut"])
    print("Verdict →", f)


if __name__ == "__main__":
    main()
