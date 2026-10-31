#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T67 passe 3 — Q-KO6-T67-2026-10 : RESIDUS vs RESOLUTION (elargissement
du spectre de longueurs)
=====================================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T67-SPECTRAL-3.0 gele]

CHOIX METHODOLOGIQUE DECLARE AVANT RUN : la passe 3 ne soustrait PAS
de fond continu (methode molle, non reproductible en l'etat) — elle
ELARGIT le spectre de longueurs. Hypothese gellee : si les decalages
residuels des 4 raies (passe 2 : 0.005, 0.166, 0.322, 0.472) sont des
artefacts de resolution lies a la troncature, ils decroissent
systematiquement quand le cut-off de trace monte ; s'ils ne decroissent
pas, ils sont physiques (poids/scattering) et cette conclusion sera
publiee telle quelle.

CRITERES GELES AVANT RUN :
  C1  pour chaque raie r_j, le maximum local de S le plus proche de
      r_j dans la fenetre +-0.5 est localise a chaque palier
      t_cut in {25, 35, 45, 60} (meme grille pas 0.005, fenetre [8,15]) ;
  C2  chaque residu a t_cut = 60 est <= max(residu_passe2 / 2, 0.05)
      (table des seuils gelee ici : r1: 0.083, r2: 0.161, r3: 0.05,
      r4: 0.236) ;
  C3  la table de convergence (4 paliers x 4 raies) est publiee ;
  C4  leviers : regression orbites identiques a la passe 2 en t=25
      (memes positions a la grille pres) ; enumeration T66, primitives.
Produit publie : la table de convergence complete, la conclusion
(resolution ou physique) — les deux issues sont des SUCCES informatifs.
Falsifieur : residu non decroissant au palier 60 ; maximum introuvable.
"""

import json
import hashlib
import time
import math
from math import gcd, isqrt


def reduced_forms(D):
    forms = []
    if isqrt(D) ** 2 == D:
        return forms
    B = 1 if D % 2 == 1 else 2
    while B * B < D:
        disc = B * B - D
        lo = max(1, (isqrt(D) - B) // 2 + 1)
        hi = (isqrt(D) + B) // 2
        for A in range(lo, hi + 1):
            if (-disc) % (4 * A) == 0:
                C = disc // (4 * A)
                if gcd(gcd(A, B), C) == 1:
                    forms.append((A, B, C))
        B += 2
    return forms


def is_primitive_power(g):
    (a, b), (c, d) = g
    s2 = a + d + 2
    r = isqrt(s2)
    if r * r == s2:
        for sd in (r, -r):
            if sd and b % sd == 0 and c % sd == 0:
                y, z = b // sd, c // sd
                x2 = a - y * z
                if x2 >= 0:
                    x = isqrt(x2)
                    if x * x == x2 and x * (sd - x) - y * z == 1 \
                            and (sd - x) ** 2 + y * z == d:
                        return True
    return False


def enumerate_orbits(Tmax):
    orbits = []
    for t in range(3, Tmax + 1):
        D = t * t - 4
        for (A, B, C) in reduced_forms(D):
            a, b, c, d = (t - B) // 2, -C, A, (t + B) // 2
            if is_primitive_power(((a, b), (c, d))):
                continue
            ell = 2 * math.acosh(t / 2)
            amp = ell / math.sqrt(t * t - 4)
            orbits.append((t, ell, amp))
    return orbits


SOURCES = [("r1", 9.5337), ("r2", 12.1730), ("r3", 13.7798), ("r4", 14.3585)]
SEUILS = {"r1": 0.083, "r2": 0.161, "r3": 0.05, "r4": 0.236}
PALIERS = [25, 35, 45, 60]


def S_of(orbits, r):
    return sum(a * math.cos(r * l) for _, l, a in orbits)


def nearest_max(orbits, rj, grid):
    vals = [S_of(orbits, r) for r in grid]
    best, bestv = None, None
    for i in range(1, len(grid) - 1):
        if abs(grid[i] - rj) <= 0.5 and vals[i] > vals[i - 1] \
                and vals[i] >= vals[i + 1]:
            if best is None or vals[i] > bestv:
                best, bestv = grid[i], vals[i]
    return best, bestv


def main():
    t0 = time.time()
    grid = [8 + 0.005 * i for i in range(int((15 - 8) / 0.005) + 1)]
    orbits = {tc: enumerate_orbits(tc) for tc in PALIERS}
    table = {nom: {} for nom, _ in SOURCES}
    for tc in PALIERS:
        for nom, rj in SOURCES:
            loc, h = nearest_max(orbits[tc], rj, grid)
            table[nom][str(tc)] = {"maximum": loc,
                                   "residu": round(abs(loc - rj), 4)
                                   if loc else None}
    C2 = all(table[nom]["60"]["residu"] is not None
             and table[nom]["60"]["residu"] <= SEUILS[nom] for nom, _ in SOURCES)
    C1 = all(table[nom][str(tc)]["maximum"] is not None
             for nom, _ in SOURCES for tc in PALIERS)
    C4 = (len(orbits[25]) == 107)
    conclusion = ("RESOLUTION : les residus decroissent avec le cut-off "
                  "-> les decalages de la passe 2 etaient des artefacts "
                  "de troncature" if C2 else
                  "PHYSIQUE : au moins un residu persiste au palier 60 "
                  "-> decalage structurel (poids/scattering), a "
                  "documenter comme fait")
    result = {"chantier": "T67-Q-KO6-SPECTRAL-2026-10",
              "protocole": "T67-SPECTRAL-3.0 (gele)",
              "passe": 3,
              "n_orbites": {str(tc): len(orbits[tc]) for tc in PALIERS},
              "choix_methodologique": "elargissement du spectre de "
                  "longueurs, pas de soustraction de fond",
              "table_convergence": table,
              "seuils_geles": SEUILS,
              "C1_maxima_localises": C1,
              "C2_residus_au_palier_60": C2,
              "C4_regression_107": C4,
              "conclusion": conclusion,
              "score": f"{int(C1)+int(C2)+int(C4)}/3",
              "statut": ("SUCCES — " + conclusion) if C1 and C4 else "ECHEC",
              "duree_s": round(time.time() - t0, 2)}
    result["sha256_script"] = hashlib.sha256(
        open(__file__, "rb").read()).hexdigest()
    print(json.dumps(result, indent=1, ensure_ascii=False))
    with open("../data/t67_ko6_spectral_p3_verdict.json", "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("verdict : data/t67_ko6_spectral_p3_verdict.json")


if __name__ == "__main__":
    main()
