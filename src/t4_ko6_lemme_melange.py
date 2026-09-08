#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T4 — Q-KO6-T4-2026-09 : LEMME DE MÉLANGE + CLASSIFICATION COMPLÈTE
===================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T4-KO6-MEL-1.0 gelé]

FICHE (gelée avant le run — 09/09/2026, campagne LOCALE, staging)
  Tiroir   : banc (preuve analytique + vérification machine)
  Objet    : « classification d'existence des triplets (D,J,γ) à deux
      scalaires sous C-KO6-A3b »
  Question unique : la régularité mesurée en T2 (100 % des combos
      mélange admettent D≠0 à n=5,7) est-elle un THÉORÈME — et quelle
      est la classification complète (préservation / échange / mélange)
      de l'existence, à n pair comme impair ?
  Conventions citées : C-KO6-A3b ; AXIOMES.md ; filiation T1 (orbites)
      et T2 (filtre ordre 1) — machines reprises avec leurs bornes.
  Faits élémentaires déclarés (dérivés avant gel) :
      F1  J₀²=+1 ⟹ s_i = s_{σ(i)} sur les 2-cycles ⟹ le signe est
          automatique sur les orbites de longueur 2 ; il ne mord que
          sur les orbites de longueur 1 (x, y fixes : s_x s_y = −1).
      F2  mélange ⟺ ∃ 2-cycle croisant les secteurs dans une chiralité
          (points fixes et 2-cycles mono-secteur préservent S_P).
      F3  ordre 1 sur l'orbite {(x,y),(x',y')} : (P_x=P_y) ∨
          (P_{x'}=P_{y'}) ; sur orbite de longueur 1 : P_x=P_y.
      F4  échange (σ(S_P)=S_Q) ⟹ rangs égaux par chiralité ⟹ a, b
          pairs (lemme A de T2, confirmé) ; en échange, P_{σi}=1−P_i,
          donc l'ordre 1 se réduit à P_x=P_y comme en préservation.
  Théorème candidat (pré-enregistré) :
      T-MÉLANGE : mélange ⟹ existence, pour TOUT n (pair ou impair).
          Preuve par cas (dans T4_NOTE.md) : un 2-cycle croisant
          (x,x') dans H⁺ ; si H⁻ a un point fixe y, l'orbite
          {(x,y),(x',y)} passe l'ordre 1 (disjonction binaire couverte
          par P_x≠P_{x'}) ; sinon (b pair), un 2-cycle de H⁻ croisant
          donne deux orbites dont l'une passe, et des 2-cycles
          mono-secteur rendent la condition automatique. Symétrie H⁻.
      T-CLASSIFICATION : existence ⟺ mélange ∨ [secteur bi-chiral ∧
          (paire même-secteur inter-chiralités en orbite de longueur 2
          ou à signes opposés)]. En préservation comme en échange,
          l'ordre 1 se réduit à la condition même-secteur (F3/F4).
  Protocole machine (bornes déclarées) :
      V1  T-MÉLANGE vérifié exhaustivement à n ∈ {2,…,9} — signes
          COLLAPSÉS (déclaré : la preuve n'utilise que des orbites de
          longueur 2, sans signe ; la vérification machine du lemme
          n'en a donc pas besoin) ; méthode des orbites indépendante
          de la preuve (filiation T2).
      V2  T-CLASSIFICATION vérifiée à n ∈ {2,…,7} avec signes :
          pour chaque (a,b,P,σ,s), l'existence par orbites doit
          coïncider EXACTEMENT avec la formule du théorème.
      V3  échange possible ⟺ a, b pairs — mesuré à n ∈ {2,…,9}.
      V4  recoupement brut n=3 et n=4 : énumération de TOUS les
          D ∈ {0,±1} avec le vérificateur matriciel complet (A3b
          étendu) — les comptes par classe doivent coïncider.
  Falsifieur : un seul combo mélange sans D (tue T-MÉLANGE) ; un seul
      écart formule/orbites (tue T-CLASSIFICATION) ; un combo échange
      à a ou b impair (tue F4) ; un mismatch brut (tue la machine).
  Prédiction pré-enregistrée : 0 contre-exemple à T-MÉLANGE (n=2..9) ;
      coïncidence parfaite de la classification (n=2..7) ; échange
      seulement à a,b pairs ; brut conforme.
  Gouvernance : campagne LOCALE — aucun push sans décision d'auteur.
"""

import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9  # figé


# ------------------------------------------------------------------ bases
def J_agit(M, J0_):
    return J0_ @ np.conj(M) @ J0_


def verifie(D_, J0_, gamma, P_):
    """Vérificateur A3b étendu (filiation T2, inchangée)."""
    n = D_.shape[0]
    Q_ = np.eye(n) - P_
    r = {}
    r["parite_{D,g}=0"] = bool(np.allclose(D_ @ gamma + gamma @ D_, 0, atol=TOL))
    r["J2_+1"] = bool(np.allclose(J_agit(J_agit(np.eye(n), J0_), J0_),
                                    np.eye(n), atol=TOL))
    r["Jgamma_+"] = bool(np.allclose(J_agit(gamma, J0_), gamma, atol=TOL))
    r["JD_-DJ"] = bool(np.allclose(J_agit(D_, J0_), -D_, atol=TOL))
    comm_p = D_ @ P_ - P_ @ D_
    comm_q = D_ @ Q_ - Q_ @ D_
    r["ordre_un"] = bool(
        np.allclose(comm_p @ J_agit(Q_, J0_), J_agit(Q_, J0_) @ comm_p, atol=TOL)
        and np.allclose(comm_q @ J_agit(P_, J0_), J_agit(P_, J0_) @ comm_q, atol=TOL))
    r["D_non_nul"] = bool(np.any(np.abs(D_) > TOL))
    r["TOUS"] = all(r.values())
    return r


def involutions_signees(a, b):
    """Machine de T1 (filiation déclarée, inchangée)."""
    n = a + b
    res = []
    for perm_a in itertools.permutations(range(a)):
        for perm_b in itertools.permutations(range(a, n)):
            sigma = perm_a + perm_b
            if any(sigma[sigma[i]] != i for i in range(n)):
                continue
            libres = [i for i in range(n) if i <= sigma[i]]
            for bits in itertools.product([1, -1], repeat=len(libres)):
                s = [0] * n
                for i, bt in zip(libres, bits):
                    s[i] = bt
                    s[sigma[i]] = bt
                res.append((sigma, s))
    return res


def involutions_seules(a, b):
    """Sans signes (V1 — lemme de mélange, orbites de longueur 2)."""
    n = a + b
    res = []
    for perm_a in itertools.permutations(range(a)):
        for perm_b in itertools.permutations(range(a, n)):
            sigma = perm_a + perm_b
            if all(sigma[sigma[i]] == i for i in range(n)):
                res.append(sigma)
    return res


def D_de_B(B, a, b):
    D = np.zeros((a + b, a + b))
    D[:a, a:] = B
    D[a:, :a] = B.T
    return D


# ------------------------------------------------------------------ orbites
def classe_de(sigma, Pset, n):
    SP = set(Pset)
    image = {sigma[i] for i in SP}
    if image == SP:
        return "preserve"
    if image == set(range(n)) - SP:
        return "echange"
    return "melange"


def orbites_liste(sigma, a, n):
    """Orbites de σ×σ sur H⁺×H⁻ : liste de paires ((x,y),(x',y'))."""
    vu = set()
    out = []
    for x in range(a):
        for y in range(a, n):
            if (x, y) not in vu:
                x2, y2 = sigma[x], sigma[y]
                vu.add((x, y))
                vu.add((x2, y2))
                out.append(((x, y), (x2, y2)))
    return out


def existe_orbites(sigma, s, a, b, Pset):
    """Existence par la méthode des orbites (filiation T2) — machine de
    référence, indépendante de la formule du théorème."""
    n = a + b

    def P_(i):
        return 1 if i in Pset else 0

    for (x, y), (x2, y2) in orbites_liste(sigma, a, n):
        if (x2, y2) == (x, y):
            if s[x] * s[y] == -1 and P_(x) == P_(y):
                return True
        else:
            signe_ok = (s[x] * s[y] * s[x2] * s[y2] == +1)
            ordre1_ok = (P_(x) == P_(y)) or (P_(x2) == P_(y2))
            if signe_ok and ordre1_ok:
                return True
    return False


def formule_theoreme(sigma, s, a, b, Pset):
    """La formule du théorème candidat (T-CLASSIFICATION) — chemin
    indépendant : mélange ⟹ vrai ; sinon condition même-secteur
    (paire inter-chiralités en 2-cycle ou à signes opposés)."""
    n = a + b
    if classe_de(sigma, Pset, n) == "melange":
        return True
    for x in range(a):
        for y in range(a, n):
            if (x in Pset) != (y in Pset):
                continue
            if sigma[x] != x or sigma[y] != y or s[x] * s[y] == -1:
                return True
    return False


def existe_melange_sans_signe(sigma, a, b, Pset):
    """V1 : existence par orbites de longueur 2 uniquement (la preuve
    n'utilise que celles-là — déclaré)."""
    n = a + b

    def P_(i):
        return 1 if i in Pset else 0

    for (x, y), (x2, y2) in orbites_liste(sigma, a, n):
        if (x2, y2) != (x, y):
            if (P_(x) == P_(y)) or (P_(x2) == P_(y2)):
                return True
    return False


# ------------------------------------------------------------------ V1/V2/V3
def V1_melange(n):
    """T-MÉLANGE à n donné : tout combo mélange a un D≠0 (orbites
    longueur 2, signes collapsés). Retourne (combos mélange, échecs)."""
    total, echecs = 0, 0
    for a in range(1, n):
        b = n - a
        for sigma in involutions_seules(a, b):
            for r in range(1, n):
                for Pset in itertools.combinations(range(n), r):
                    if classe_de(sigma, Pset, n) != "melange":
                        continue
                    total += 1
                    if not existe_melange_sans_signe(sigma, a, b, Pset):
                        echecs += 1
    return total, echecs


def V2_classification(n):
    """T-CLASSIFICATION à n donné (signes inclus) : formule == orbites,
    combo par combo. Retourne (combos, écarts)."""
    total, ecarts = 0, 0
    for a in range(1, n):
        b = n - a
        for sigma, s in involutions_signees(a, b):
            for r in range(1, n):
                for Pset in itertools.combinations(range(n), r):
                    total += 1
                    if existe_orbites(sigma, s, a, b, Pset) != \
                            formule_theoreme(sigma, s, a, b, Pset):
                        ecarts += 1
    return total, ecarts


def V3_echange(n):
    """Échange possible ⟺ a, b pairs : comptes par parité de (a,b)."""
    pair, impair = 0, 0
    for a in range(1, n):
        b = n - a
        for sigma in involutions_seules(a, b):
            for r in range(1, n):
                for Pset in itertools.combinations(range(n), r):
                    if classe_de(sigma, Pset, n) == "echange":
                        if a % 2 == 0 and b % 2 == 0:
                            pair += 1
                        else:
                            impair += 1
    return pair, impair


# ------------------------------------------------------------------ V4 brut
def brut(n):
    """Comptes par classe avec le vérificateur matriciel complet sur
    TOUS les D ∈ {0,±1} hors-chiraux (recoupement de la machine)."""
    comptes = {"preserve": 0, "echange": 0, "melange": 0}
    for a in range(1, n):
        b = n - a
        gamma = np.diag([1.0] * a + [-1.0] * b)
        for r in range(1, n):
            for Pset in itertools.combinations(range(n), r):
                Pm = np.zeros((n, n))
                for i in Pset:
                    Pm[i, i] = 1.0
                for sigma, s in involutions_signees(a, b):
                    cl = classe_de(sigma, Pset, n)
                    J0_ = np.zeros((n, n))
                    for j in range(n):
                        J0_[sigma[j], j] = s[j]
                    for mask in itertools.product([0, 1, -1], repeat=a * b):
                        B = np.array(mask, dtype=float).reshape(a, b)
                        if np.any(B) and verifie(D_de_B(B, a, b), J0_,
                                                 gamma, Pm)["TOUS"]:
                            comptes[cl] += 1
    return comptes


def comptes_orbites(n):
    """Comptes par classe via la méthode des orbites (3^k − 1)."""
    comptes = {"preserve": 0, "echange": 0, "melange": 0}
    for a in range(1, n):
        b = n - a

        def P_(i, Pset):
            return 1 if i in Pset else 0

        for sigma, s in involutions_signees(a, b):
            orbs = orbites_liste(sigma, a, n)
            for r in range(1, n):
                for Pset in itertools.combinations(range(n), r):
                    k = 0
                    for (x, y), (x2, y2) in orbs:
                        if (x2, y2) == (x, y):
                            if s[x] * s[y] == -1 and \
                                    P_(x, Pset) == P_(y, Pset):
                                k += 1
                        else:
                            if s[x] * s[y] * s[x2] * s[y2] == +1 and \
                                    (P_(x, Pset) == P_(y, Pset) or
                                     P_(x2, Pset) == P_(y2, Pset)):
                                k += 1
                    if k:
                        comptes[classe_de(sigma, Pset, n)] += 3 ** k - 1
    return comptes


def main():
    t0 = time.time()
    print("T4 — lemme de mélange + classification   [T4-KO6-MEL-1.0 gelé]")
    print("=" * 76)

    print("\nV1 — T-MÉLANGE (mélange ⟹ existence), exhaustif, signes collapsés :")
    v1 = {}
    for n in range(2, 10):
        tot, ech = V1_melange(n)
        v1[n] = {"combos_melange": tot, "sans_D": ech}
        print(f"  n={n} : {tot:>9} combos mélange · sans D : {ech}")
    v1_ok = all(v["sans_D"] == 0 for v in v1.values())

    print("\nV2 — T-CLASSIFICATION (formule == orbites), avec signes :")
    v2 = {}
    for n in range(2, 8):
        tot, ec = V2_classification(n)
        v2[n] = {"combos": tot, "ecarts": ec}
        print(f"  n={n} : {tot:>8} combos · écarts : {ec}")
    v2_ok = all(v["ecarts"] == 0 for v in v2.values())

    print("\nV3 — échange possible ⟺ a,b pairs :")
    v3 = {}
    for n in range(2, 10):
        pair, impair = V3_echange(n)
        v3[n] = {"echange_a_b_pairs": pair, "echange_autre": impair}
        print(f"  n={n} : échange (a,b pairs) = {pair:>6} · "
              f"échange (autre parité) = {impair}")
    v3_ok = all(v["echange_autre"] == 0 for v in v3.values())

    print("\nV4 — recoupement brut (vérificateur complet) :")
    v4 = {}
    for n in (3, 4):
        cb = brut(n)
        co = comptes_orbites(n)
        v4[n] = {"brut": cb, "orbites": co,
                 "conforme": cb == co}
        print(f"  n={n} : brut={cb} orbites={co} → "
              f"{'OK' if cb == co else 'MISMATCH'}")
    v4_ok = all(v["conforme"] for v in v4.values())

    verdict = {
        "chantier": "T4-Q-KO6-T4-2026-09",
        "protocole": "T4-KO6-MEL-1.0 (gelé, local)",
        "table": "C-KO6-A3b — datée",
        "theoreme_melange": {
            "énoncé": "mélange ⟹ existence (D≠0), pour tout n",
            "preuve": "T4_NOTE.md (cas élémentaires, faits F1–F3)",
            "V1": v1, "confirmé_machine": v1_ok},
        "theoreme_classification": {
            "énoncé": "existence ⟺ mélange ∨ [secteur bi-chiral ∧ "
                      "(paire même-secteur inter-chiralités en orbite de "
                      "longueur 2 ou à signes opposés)]",
            "V2": v2, "confirmé_machine": v2_ok},
        "fait_F4_echange": {"énoncé": "échange possible ⟺ a,b pairs",
                            "V3": v3, "confirmé_machine": v3_ok},
        "recoupement_brut_V4": v4,
        "controle_global": bool(v1_ok and v2_ok and v3_ok and v4_ok),
        "falsifieur_statut": "non déclenché" if (v1_ok and v2_ok and v3_ok
                             and v4_ok) else "DÉCLENCHÉ — voir détails",
        "prédiction_pré_enregistrée": "0 contre-exemple ; coïncidence "
                                      "parfaite ; échange à a,b pairs ; "
                                      "brut conforme",
        "gouvernance": "campagne LOCALE — staging, pause de tri avant "
                       "toute publication",
        "durée_s": round(time.time() - t0, 2),
    }
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t4_ko6_lemme_melange_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("\n" + "=" * 76)
    print("CONTRÔLE GLOBAL :", "PASS" if verdict["controle_global"] else "FAIL")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
