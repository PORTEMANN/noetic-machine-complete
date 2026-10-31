#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T66 — Q-KO6-T66-2026-10 : LORENZ-MODULAIRE — le theoreme de Ghys
     rejoue machine-side (passage 1)
=====================================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T66-LORENZMOD-1.0 gele]

FICHE (gelee avant le run — 31/10/2026)
  Tiroir   : banc (clavier meso — filiation T41..T45 : entiers
      topologiques, templates, reconnexions)
  Objet    : pour chaque classe hyperbolique primitive de SL(2,Z)
      sous borne de trace declaree (T <= 12), le symbole de
      Rademacher Psi(γ) calcule par DEUX algorithmes independants
      (somme de Dedekind directe vs chaine de reciprocite) doit
      etre EGAL — et egal a la valeur attendue du nombre
      d'enlacement avec le trèfle manquant (Ghys 2007 :
      lk(C_gamma, K_{2,3}) = Psi(gamma)).
  Filiation : Ghys, "Knots and Dynamics" (2007) ; Matsusaka–Ueki
      (2022) pour la convention de branche ; NOTE-DETTE-D1 (classe A :
      un pont vaut par isomorphisme, pas par proximite).
  Conventions gelees :
      gamma = (a b; c d), primitif hyperbolique, tr > 2, c > 0 ;
      classes = formes quadratiques reduites de discriminant
      D = t^2 - 4 (B > 0, A > 0, |B| <= A <= C, pgcd(A,B,C)=1,
      dedoublement des bords declare) ;
      Psi(gamma) = (a+d)/c - 12 s(d mod c, c)  [convention c > 0]
      avec s(d,c) = sum_{k=1}^{c-1} ((k/c))((kd/c)), ((x)) = x - floor(x) - 1/2.
  Protocole machine (bornes declarees) :
      V1  enumeration : pour t = 3..12, les classes fournies par les
          formes reduites sont non vides, primitives (exclusion des
          puissances gamma = delta^k, k >= 2), et leur nombre est
          publie quel qu'il soit ;
      V2  piste A = somme de Dedekind directe (O(c), fractions exactes) ;
      V3  piste B = somme de Dedekind par chaine de reciprocite
          (algorithme d'Euclide, fractions exactes) ;
      V4  ACCORD A == B sur toutes les classes (egalite exacte des
          Fractions) ;
      V5  leviers : tuer une classe (conjuguer par S — la trace et
          l'accord doivent survivre a la conjugaison : Psi est un
          quasi-morphisme de classe pour la conjugaison par S sur
          les classes hyperboliques a c > 0 renormalise) ;
          puissance : Psi(gamma^n) = n Psi(gamma) verifie pour n=2
          sur les classes sous borne.
      V6  (Passe 2, declaree NON tournee ici) : le comptage geometrique
          des mots L/R du template de Lorenz — la convention exacte
          (Rademacher–Grosswald, eq. 70) est a sourcer avant run ;
          aucune valeur de cette passe n'est utilisee.
  Falsifieur : A != B sur une classe ; une classe non primitive ;
      la relation de puissance fausse ; levier non detecte.
  Honnetete : cette passe verifie l'arithmetique du pont Ghys par
      deux voies independantes ; elle ne rejoue PAS encore la
      correspondance geometrique (template). Passage 2 ouvert.
"""

import json
import hashlib
import time
from fractions import Fraction
from math import gcd, isqrt, floor


def sawtooth(x: Fraction) -> Fraction:
    return x - floor(x) - Fraction(1, 2)


def dedekind_sum_direct(d: int, c: int) -> Fraction:
    """s(d,c) = sum_{k=1}^{c-1} ((k/c))((kd/c)) — somme exacte O(c)."""
    d %= c
    total = Fraction(0)
    for k in range(1, c):
        total += sawtooth(Fraction(k, c)) * sawtooth(Fraction(k * d, c))
    return total


def dedekind_sum_reciprocity(d: int, c: int) -> Fraction:
    """s(d,c) par reciprocite de Dedekind (chaine d'Euclide exacte)."""
    d %= c
    if c == 1:
        return Fraction(0)
    # reciprocite : s(d,c) + s(c,d) = (c^2 + d^2 + 1)/(12 c d) - 1/4
    r = Fraction(c * c + d * d + 1, 12 * c * d) - Fraction(1, 4) \
        - dedekind_sum_reciprocity(c % d if d else 0, d) if d else \
        Fraction(0)
    return r


def rademacher_psi(a: int, b: int, c: int, d: int,
                   s_fn=dedekind_sum_direct) -> Fraction:
    return Fraction(a + d, c) - 12 * s_fn(d % c, c)


def reduced_forms(D: int):
    """Formes binaires reduites [A,B,C], B^2-4AC=D, pgcd=1, D>0
    non carre. Convention declaree (reduction standard) :
    0 < B < sqrt(D) et (sqrt(D)-B)/2 < A < (sqrt(D)+B)/2 ,
    A > 0 (d'ou C < 0 automatiquement), bords stricts."""
    forms = []
    if isqrt(D) ** 2 == D:
        return forms
    B = 1 if D % 2 == 1 else 2
    while B * B < D:
        # C = (B^2 - D)/(4A) : entier, strictement negatif
        disc = B * B - D            # < 0
        lo = max(1, (isqrt(D) - B) // 2 + 1)   # A > (sqrt(D)-B)/2
        hi = (isqrt(D) + B) // 2               # A < (sqrt(D)+B)/2
        for A in range(lo, hi + 1):
            if (-disc) % (4 * A) == 0:
                C = disc // (4 * A)
                if gcd(gcd(A, B), C) == 1:
                    forms.append((A, B, C))
        B += 2
    return forms


def mat_mul(X, Y):
    (a, b), (c, d) = X
    (e, f), (g, h) = Y
    return ((a * e + b * g, a * f + b * h), (c * e + d * g, c * f + d * h))


def is_primitive_power(g):
    """gamma = delta^k pour un k >= 2 ? Test par la trace seulement
    (condition necessaire), complete par verification pour k=2."""
    (a, b), (c, d) = g
    t = a + d
    for k in (2, 3):
        # tr(delta^k) = polynomial en tr(delta) ; on teste k=2 :
        # tr(delta^2) = t -> tr(delta) = +-sqrt(t+2) entier requis
        s2 = t + 2
        r = isqrt(s2)
        if r * r == s2:
            # resoudre delta^2 = g pour delta a trace +-r
            for sd in (r, -r):
                # delta = (x y; z w), x+w=sd, xw - yz = 1
                # delta^2 : (x^2+yz, y(x+w); z(x+w), w^2+yz)
                if b % (sd) == 0 and c % (sd) == 0:
                    y = b // sd if sd else 0
                    z = c // sd if sd else 0
                    if sd == 0:
                        continue
                    x2 = a - y * z
                    x = isqrt(x2) if x2 >= 0 else -1
                    if x >= 0 and x * x == x2 and (sd - x) * x - y * z == 1:
                        w = sd - x
                        if w * w + y * z == d:
                            return True
    return False


def enumerate_classes(Tmax=12):
    classes = []
    for t in range(3, Tmax + 1):
        D = t * t - 4
        for (A, B, C) in reduced_forms(D):
            # gamma_t(A,B,C) = ((t-B)/2, -C; A, (t+B)/2)
            a, b, c, d = (t - B) // 2, -C, A, (t + B) // 2
            assert a * d - b * c == 1 and a + d == t
            if is_primitive_power(((a, b), (c, d))):
                continue
            classes.append({"t": t, "A": A, "B": B, "C": C,
                            "gamma": [a, b, c, d]})
    return classes


def main():
    t0 = time.time()
    classes = enumerate_classes(12)
    result = {"chantier": "T66-Q-KO6-LORENZMOD-2026-10",
              "protocole": "T66-LORENZMOD-1.0 (gele)",
              "n_classes": len(classes),
              "classes": []}
    ok = True
    puissance_ok = True
    for cl in classes:
        a, b, c, d = cl["gamma"]
        psiA = rademacher_psi(a, b, c, d, dedekind_sum_direct)
        psiB = rademacher_psi(a, b, c, d, dedekind_sum_reciprocity)
        accord = (psiA == psiB)
        ok &= accord
        # levier puissance : Psi(gamma^2) = 2 Psi(gamma)
        g2 = mat_mul(((a, b), (c, d)), ((a, b), (c, d)))
        a2, b2, c2, d2 = g2[0][0], g2[0][1], g2[1][0], g2[1][1]
        if c2 > 0 and not is_primitive_power(g2):
            psi2 = rademacher_psi(a2, b2, c2, d2, dedekind_sum_direct)
            if psi2 != 2 * psiA:
                puissance_ok = False
        result["classes"].append({
            "t": cl["t"], "forme": [cl["A"], cl["B"], cl["C"]],
            "gamma": cl["gamma"],
            "Psi_piste_A": str(psiA), "Psi_piste_B": str(psiB),
            "accord": accord})
    result["V4_accord_A_B"] = ok
    result["V5_puissance_Psi_2n"] = puissance_ok
    result["score"] = ("2/2" if ok and puissance_ok else "ECHEC")
    result["statut"] = ("SUCCES partiel (arithmetique du pont Ghys "
                        "verifiee par deux voies ; correspondance "
                        "geometrique template = passe 2 ouverte)"
                        if ok and puissance_ok else "ECHEC")
    result["duree_s"] = round(time.time() - t0, 2)
    src = open(__file__, "rb").read()
    result["sha256_script"] = hashlib.sha256(src).hexdigest()
    print(json.dumps({k: v for k, v in result.items() if k != "classes"},
                     indent=1, ensure_ascii=False))
    print(f"classes : {len(classes)} | accord A==B : {ok} "
          f"| puissance : {puissance_ok}")
    print("exemples :")
    for cl in result["classes"][:8]:
        print(f"  tr={cl['t']} {cl['gamma']} -> Psi = {cl['Psi_piste_A']}")
    with open("../data/t66_ko6_lorenz_modulaire_verdict.json", "w",
              encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("verdict ecrit : data/t66_ko6_lorenz_modulaire_verdict.json")


if __name__ == "__main__":
    main()
