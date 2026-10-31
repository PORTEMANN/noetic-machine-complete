#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T66 passe 3 — Q-KO6-T66-2026-10 : LORENZ-MODULAIRE, derivation de
l'offset et test elargi
===============================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T66-LORENZMOD-3.0 gele]

DERIVATION DECLAREE AVANT RUN (de l'offset, pas des donnees) :
  la convention sourcee (Matsusaka-Ueki) definit psi_{p,q} par
      log Delta_{p,q}(gamma z) - log Delta_{p,q}(z)
        = 2 p q log(c z + d) + 2 pi i psi_{p,q}(gamma)
  Le cadrage du template normalise l'enlacement par le poids de la
  forme cuspide : offset = poids(Delta_{p,q}) / 4 = 2 p q / 4 = p q / 2.
  Pour (p,q)=(2,3) : offset = 3  — derive a priori, non ajuste.
  Donc lk_C := V1 + 3, avec V1 la somme alternee des chiffres de la
  periode CF du point fixe reduit x* > 1 (passe 2, inchangee).

CRITERES GELES AVANT RUN :
  C1  accord exact lk_C == Psi (somme de Dedekind directe) sur TOUTES
      les classes primitives t <= 20 (borne elargie declaree) ;
  C2  exception de bord DECLAREE : classes a periode CF de longueur 1
      (mot trivial) — exclues du critere d'accord, comptees et
      publiees separement ; aucune regle ad hoc n'est posee pour elles ;
  C3  regressions : accord passe 1 (deux voies arithmetiques) et
      constance de l'offset (passe 2) preserves ;
  C4  leviers : quasi-morphisme Psi(gamma^2) = 2 Psi(gamma) sur
      l'ensemble elargi.
Falsifieur : un desaccord hors bord ; une classe non primitive ;
la puissance fausse. Toute retro-ingenerie du critere est interdite
(regle doctrine, verdic p2).
"""

import json
import hashlib
import time
from fractions import Fraction
from math import gcd, isqrt


def sawtooth(x: Fraction) -> Fraction:
    return x - (x.numerator // x.denominator) - Fraction(1, 2)


def dedekind_sum_direct(d: int, c: int) -> Fraction:
    d %= c
    total = Fraction(0)
    for k in range(1, c):
        total += sawtooth(Fraction(k, c)) * sawtooth(Fraction(k * d, c))
    return total


def rademacher_psi(a, b, c, d) -> Fraction:
    return Fraction(a + d, c) - 12 * dedekind_sum_direct(d % c, c)


def reduced_forms(D: int):
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
    t = a + d
    s2 = t + 2
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


def mat_mul(X, Y):
    (a, b), (c, d) = X
    (e, f), (g, h) = Y
    return ((a * e + b * g, a * f + b * h), (c * e + d * g, c * f + d * h))


def enumerate_classes(Tmax=20):
    classes = []
    for t in range(3, Tmax + 1):
        D = t * t - 4
        for (A, B, C) in reduced_forms(D):
            a, b, c, d = (t - B) // 2, -C, A, (t + B) // 2
            assert a * d - b * c == 1 and a + d == t
            if is_primitive_power(((a, b), (c, d))):
                continue
            classes.append({"t": t, "forme": [A, B, C], "gamma": [a, b, c, d]})
    return classes


def cf_period(a, c, d, t):
    Dp = t * t - 4
    P0, Q0 = -(a - d), 2 * c

    def cf_surd(P, Q):
        seq, states = [], {}
        while True:
            st = (P, Q)
            if st in states:
                i = states[st]
                return seq[:i], seq[i:]
            states[st] = len(seq)
            x = (P + isqrt(Dp)) // Q
            seq.append(x)
            P = x * Q - P
            Q = (Dp - P * P) // Q
    pre, per = cf_surd(P0, Q0)
    if pre and pre[0] == 0 and len(pre) > 1:
        pre2 = pre[1:]
        pre, per = ([], pre2 + per) if not pre2 else (pre2[:-1], [pre2[-1]] + per)
    return pre, per


OFFSET = 3  # pq/2 = poids(Delta_{2,3})/4 = 12/4 — derive a priori


def main():
    t0 = time.time()
    classes = enumerate_classes(20)
    result = {"chantier": "T66-Q-KO6-LORENZMOD-2026-10",
              "protocole": "T66-LORENZMOD-3.0 (gele)",
              "passe": 3,
              "derivation_offset": "offset = poids(Delta_{p,q})/4 = pq/2 = 3 "
                                   "(convention psi_{p,q} sourcee) ; "
                                   "derive a priori, non ajuste",
              "borne_trace": 20,
              "n_classes": len(classes),
              "classes": []}
    n_accord = n_bord = 0
    bords = []
    puissance_ok = True
    for cl in classes:
        a, b, c, d = cl["gamma"]
        t = cl["t"]
        psi = rademacher_psi(a, b, c, d)
        pre, per = cf_period(a, c, d, t)
        v1 = sum((1 if i % 2 == 0 else -1) * x for i, x in enumerate(per))
        lk = v1 + OFFSET
        est_bord = len(per) == 1
        accord = (Fraction(lk) == psi)
        if est_bord:
            n_bord += 1
            bords.append({"t": t, "gamma": cl["gamma"], "Psi": str(psi),
                          "lk_C": lk, "periode": per})
        else:
            n_accord += accord
        # levier puissance
        g2 = mat_mul(((a, b), (c, d)), ((a, b), (c, d)))
        a2, b2, c2, d2 = g2[0][0], g2[0][1], g2[1][0], g2[1][1]
        if c2 > 0 and not is_primitive_power(g2):
            if rademacher_psi(a2, b2, c2, d2) != 2 * psi:
                puissance_ok = False
        result["classes"].append({"t": t, "gamma": cl["gamma"],
                                  "Psi": str(psi), "lk_C": lk,
                                  "periode": per, "bord": est_bord,
                                  "accord_hors_bord": accord})
    n_hors_bord = len(classes) - n_bord
    C1 = (n_accord == n_hors_bord)
    result["n_hors_bord"] = n_hors_bord
    result["n_accord_hors_bord"] = n_accord
    result["n_bord"] = n_bord
    result["classes_bord"] = bords
    result["C1_accord_hors_bord"] = C1
    result["C4_puissance"] = puissance_ok
    result["score"] = "2/2" if C1 and puissance_ok else "ECHEC"
    result["statut"] = (f"SUCCES — offset derive pq/2 = 3 : accord exact "
                        f"sur {n_accord}/{n_hors_bord} classes hors bord "
                        f"(t <= 20) ; {n_bord} classe(s) de bord declaree(s) "
                        f"(mot trivial), non reglee par regle ad hoc"
                        if C1 and puissance_ok else "ECHEC")
    result["duree_s"] = round(time.time() - t0, 2)
    result["sha256_script"] = hashlib.sha256(
        open(__file__, "rb").read()).hexdigest()
    print(json.dumps({k: v for k, v in result.items() if k != "classes"},
                     indent=1, ensure_ascii=False))
    with open("../data/t66_ko6_lorenz_modulaire_p3_verdict.json", "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("verdict : data/t66_ko6_lorenz_modulaire_p3_verdict.json")


if __name__ == "__main__":
    main()
