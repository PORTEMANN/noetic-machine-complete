#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T5 — LE ddll DE LA CONSERVATION : la persistance du discret dans le
continu a-t-elle un prix mesurable ?   [protocole T5-DDLL-1.0 gelé]
=====================================================================
Tiroir banc. Table gelée AVANT tout calcul (ci-dessous, TUPLE FROZEN) :
les 10 mécanismes du corridor E45–E53 (tous : non-conservation) + 4
protections de référence qui conservent (3 intrinsèques du corpus :
E40 triplet stable une fois formé, P24 gap de Hall, P33 charge de bord
— et 1 documentaire externe déclarée : flux pinning des LIGNES en
supraconducteur de type II).

Rubrique gelée (deux variantes, déclarées — robustesse exigée) :
  descripteurs par mécanisme : n_scal (paramètres scalaires gelés
  indépendants), n_struct (déclarations structurelles : géométrie,
  calendrier, bord, réseau), n_choix (choix combinatoires libres :
  positions, translations).
  ddll_v1 = n_scal + n_struct + log2(1 + n_choix)
  ddll_v2 = n_scal + 2·n_struct + log2(1 + n_choix)   (poids structurel
  doublé — variante figée)
Axe secondaire gelé : objet contractile (boucles) vs non contractile
(lignes, étendu, intrinsèque).

Questions gelées :
  Q1 : un ddll scalaire sépare-t-il les protections qui conservent des
  mécanismes qui échouent ? (dans quel sens ?)
  Q2 : la séparation est-elle robuste au changement de rubrique (v1→v2) ?
  Q3 : la carte (ddll × contractilité) est-elle séparée ?

Falsifieur : aucune structure de séparation sous aucune rubrique → la
« métrologie du coût de conservation » est réfutée comme scalaire —
publié (précédent P-F3 : pas d'indice scalaire).
Discipline E1 : le compte est publié quel qu'il soit.

Usage : python3 t5_ddll_conservation.py
"""

import json
import math
import os
import time
from pathlib import Path

# ---------------- TABLE GELÉE (avant calcul) — descripteurs déclarés --------
# (nom, n_scal, n_struct, n_choix, contractile, conserve, origine)
TABLE = [
    # corridor E45–E53 — tous : non-conservation (verdicts staging 09/09)
    ("E45 coupure amortissement", 1, 1, 0, True, False, "corridor"),
    ("E46 mur mélangé", 2, 1, 0, True, False, "corridor"),
    ("E47-B gel de Kelvin", 2, 1, 0, True, False, "corridor"),
    ("E47-C plancher dissipatif", 2, 1, 0, True, False, "corridor"),
    ("E48 gel à la nucléation + suivi", 2, 1, 0, True, False, "corridor"),
    ("E49 nettoyage puis gel", 3, 2, 0, True, False, "corridor"),
    ("E50 lien imprimé + gel", 5, 2, 2, True, False, "corridor"),
    ("E51 pinning ponctuel apparié", 3, 1, 29, True, False, "corridor"),
    ("E52 paysage de puits", 4, 1, 512, True, False, "corridor"),
    ("E53 canaux toriques", 5, 2, 2, True, False, "corridor"),
    # protections de référence — conservent (déclarées)
    ("R1 E40 triplet stable une fois formé", 0, 0, 0, False, True,
     "corpus (intrinsèque)"),
    ("R2 P24 gap de Hall (protection par gap)", 0, 0, 0, False, True,
     "corpus (intrinsèque)"),
    ("R3 P33 charge de bord / asymptotique", 0, 0, 0, False, True,
     "corpus (intrinsèque)"),
    ("R4 flux pinning de LIGNES (type II, documentaire)", 2, 1, 512,
     False, True, "documentaire externe — déclaré"),
]

VARIANTES = {
    "v1": lambda s, st, c: s + st + math.log2(1 + c),
    "v2": lambda s, st, c: s + 2 * st + math.log2(1 + c),
}


def separe(vals, flags):
    """Existe-t-il un seuil séparant parfaitement True/False ?
    Rend (séparé, sens, seuil)."""
    t = sorted(zip(vals, flags))
    for k in range(len(t) + 1):
        lo = [f for _, f in t[:k]]
        hi = [f for _, f in t[k:]]
        if all(not f for f in lo) and all(f for f in hi):
            seuil = (t[k - 1][0] if k else None, t[k][0] if k < len(t) else None)
            return True, "conserve = au-dessus", seuil
        if all(f for f in lo) and all(not f for f in hi):
            seuil = (t[k - 1][0] if k else None, t[k][0] if k < len(t) else None)
            return True, "conserve = en-dessous (INVERSION)", seuil
    return False, None, None


def main():
    t0 = time.time()
    print("T5 — le ddll de la conservation   [T5-DDLL-1.0 gelé]")
    print("=" * 70)

    lignes = []
    for nom, s, st, c, contractile, conserve, origine in TABLE:
        d = {v: round(f(s, st, c), 3) for v, f in VARIANTES.items()}
        lignes.append({"mécanisme": nom, "n_scal": s, "n_struct": st,
                       "n_choix": c, "ddll": d, "contractile": contractile,
                       "conserve": conserve, "origine": origine})
        print(f"{nom:<44} ddll v1={d['v1']:>7} v2={d['v2']:>7} "
              f"contractile={contractile} conserve={conserve}")

    resultats = {}
    for v in VARIANTES:
        vals = [l["ddll"][v] for l in lignes]
        flags = [l["conserve"] for l in lignes]
        sep, sens, seuil = separe(vals, flags)
        resultats[v] = {"séparé": sep, "sens": sens, "seuil": seuil}
        print(f"\nQ1 rubrique {v} : séparation par seuil : {sep} {sens or ''} "
              f"seuil={seuil}")

    robuste = (resultats["v1"]["séparé"] and resultats["v2"]["séparé"]
               and resultats["v1"]["sens"] == resultats["v2"]["sens"])
    print(f"Q2 robustesse de rubrique : {robuste}")

    # Q3 : carte ddll × contractilité — séparation par quadrant ?
    quadrants = {}
    for l in lignes:
        key = (l["contractile"], l["conserve"])
        quadrants.setdefault(key, []).append(l["mécanisme"])
    q3 = all(len(v) > 0 for k, v in quadrants.items()) and \
        all(l["conserve"] is False for l in lignes if l["contractile"])
    print(f"\nQ3 carte : quadrants = { {k: len(v) for k, v in quadrants.items()} }")
    print("   tous les contractiles échouent :",
          all(not l["conserve"] for l in lignes if l["contractile"]))
    print("   tous les non-contractiles conservent :",
          all(l["conserve"] for l in lignes if not l["contractile"]))

    verdict = {
        "chantier": "T5-DDLL-CONSERVATION",
        "protocole": "T5-DDLL-1.0 (gelé)",
        "table": lignes,
        "Q1_separation_scalaire": resultats,
        "Q2_robuste": robuste,
        "Q3_carte": {"quadrants": {str(k): v for k, v in quadrants.items()},
                     "contractiles_tous_échouent":
                     all(not l["conserve"] for l in lignes
                         if l["contractile"]),
                     "non_contractiles_tous_conservent":
                     all(l["conserve"] for l in lignes
                         if not l["contractile"])},
        "durée_s": round(time.time() - t0, 2),
    }
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t5_ddll_conservation_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("\nVerdict →", f)


if __name__ == "__main__":
    main()
