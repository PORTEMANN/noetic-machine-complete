#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T67 — Q-KO6-T67-2026-10 : LONGUEURS MODULAIRES vs SPECTRE DE MAASS
     (le pont spectral du pont de Ghys, tronque machine-side)
=====================================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T67-SPECTRAL-1.0 gele]

FICHE (gelee avant le run — 31/10/2026)
  Tiroir   : banc (clavier meso) · filiation T66 (meme enumeration de
      classes, trace elargie declaree).
  Objet    : cote geometrique de la formule des traces de Selberg :
      S(r) = Somme_{classes primitives, tr <= 25} A_gamma cos(r l_gamma),
      A_gamma = l_gamma / sqrt(t^2 - 4), l_gamma = 2 arcosh(t/2)
      (identite exacte : 2 sinh(l/2) = sqrt(t^2 - 4)).
      Le cote spectral (formes de Maass cuspidales de la surface
      modulaire, sources) exige des pics de S en r_j :
          r1 = 9.5337 (lambda1 = 91.14...) , r2 = 12.1730 (148.43...)
      (Booker–Strombergsson–Venkatesh, verifies a 100 decimales ;
      valeurs rapporchees ici a 1e-4, source : revue et prepublication).
  Caveats declares (non voiles) :
      - spectre CONTINU (Eisenstein) non soustrait : le test est une
        detection de pics robuste, pas une inversion complete ;
      - troncature tr <= 25 : resolution limite d r ~ 2 pi / l_max
        ~ 0.97 ; tolerances declarees en consequence ;
      - S est reelle, paire ; seule la fenetre r in [8, 14] est testee.
  Protocole machine (bornes declarees) :
      C1  les deux maxima locaux les plus hauts de S sur la grille
          r in [8, 14] (pas 0.005) sont a +- 0.5 de r1 et r2 sources ;
      C2  controle anti-pic : S((r1+r2)/2) < 0.5 * max S ;
      C3  levier : retirer l'orbite la plus longue (moitie de la
          resolution) — les maxima doivent bouger de > 0.15 ou la
          tolerance effective doit se degrader (levier detecte) ;
      C4  regression : re-utilisation de l'enumeration T66, trace
          elargie 25, classes primitives uniquement.
  Falsifieur : maximum manquant hors tolerance ; pic au controle ;
  levier non detecte.
"""

import json
import hashlib
import time
import math
from fractions import Fraction
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


def enumerate_orbits(Tmax=25):
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


R1, R2 = 9.5337, 12.1730   # sources (BSV, 100 decimales)


def S_of(orbits, r):
    return sum(a * math.cos(r * l) for _, l, a in orbits)


def local_maxima(grid, vals):
    out = []
    for i in range(1, len(vals) - 1):
        if vals[i] > vals[i - 1] and vals[i] >= vals[i + 1]:
            out.append((grid[i], vals[i]))
    return sorted(out, key=lambda x: -x[1])


def main():
    t0 = time.time()
    orbits = enumerate_orbits(25)
    grid = [8 + 0.005 * i for i in range(int((14 - 8) / 0.005) + 1)]
    vals = [S_of(orbits, r) for r in grid]
    maxima = local_maxima(grid, vals)
    top2 = maxima[:2]
    top2_sorted = sorted(top2, key=lambda x: x[0])
    locs = [m[0] for m in top2_sorted]
    C1 = (abs(locs[0] - R1) <= 0.5 and abs(locs[1] - R2) <= 0.5)
    mid = (R1 + R2) / 2
    C2 = S_of(orbits, mid) < 0.5 * vals[vals.index(max(vals))]
    # levier : retirer l'orbite la plus longue
    orbits_sans = [o for o in orbits if o[1] < max(o[1] for o in orbits)]
    vals2 = [S_of(orbits_sans, r) for r in grid]
    maxima2 = local_maxima(grid, vals2)
    locs2 = sorted([m[0] for m in maxima2[:2]])
    C3 = (len(locs2) < 2 or abs(locs2[0] - locs[0]) > 0.15
          or abs(locs2[1] - locs[1]) > 0.15)
    result = {"chantier": "T67-Q-KO6-SPECTRAL-2026-10",
              "protocole": "T67-SPECTRAL-1.0 (gele)",
              "n_orbites": len(orbites) if (orbites := orbits) else 0,
              "sources_spectrales": "Booker–Strombergsson–Venkatesh "
                  "(verifiees 100 dec.) : r1=9.5337, r2=12.1730",
              "caveats": "spectre continu non soustrait ; troncature "
                  "tr<=25 (resolution ~0.97)",
              "maxima": [[round(l, 4), round(v, 4)] for l, v in top2],
              "C1_maxima_a_r1_r2": C1,
              "C2_controle_anti_pic": C2,
              "C3_levier_troncature": C3,
              "score": f"{int(C1)+int(C2)+int(C3)}/3",
              "statut": ("SUCCES — le cote geometrique (orbites modulaires "
                         "de T66) dessine les deux premiers pics du spectre "
                         "de Maass dans les tolerances declarees"
                         if C1 and C2 and C3 else "ECHEC"),
              "duree_s": round(time.time() - t0, 2)}
    result["sha256_script"] = hashlib.sha256(
        open(__file__, "rb").read()).hexdigest()
    print(json.dumps(result, indent=1, ensure_ascii=False))
    with open("../data/t67_ko6_spectral_verdict.json", "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("verdict : data/t67_ko6_spectral_verdict.json")


if __name__ == "__main__":
    main()
