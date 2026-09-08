#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2 — Q-KO6-T2-2026-09 : TAILLE IMPAIRE, A = ℂ⊕ℂ, ORDRE 1 NON VACUOUS
======================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T2-KO6-O1IMP-1.0 gelé]

FICHE (gelée avant le run — 09/09/2026, campagne LOCALE, staging)
  Tiroir   : banc
  Objet    : « triplet spectral fini de taille impaire à deux scalaires »
  Question unique : sous la table C-KO6-A3b (datée), existe-t-il
      (D, J, γ) de taille n impaire avec A = ℂ ⊕ ℂ (deux scalaires) et
      ordre 1 NON vacuous — et dans quelle classe d'action de J sur les
      secteurs (préservation / échange / mélange) ?
  Motivation déclarée : T1 (verdict local du 09/09/2026) a tranché la
      taille impaire avec UN scalaire (existence dès n=3, ordre 1
      vacuous pour A=ℂ). La présente campagne est la question plus
      forte annoncée dans le verdict T1 — nouvelle fiche gelée, pas un
      critère déplacé (point 6 de la boucle). Enjeu corpus : le statut
      de l'arithmétique de multiplicités « 2+2+3 = 7 » (AXIOMES.md).
  Conventions citées : C-KO6-A3b (J²=+1, Jγ=+γJ, JD=−DJ) ; AXIOMES.md
      gelé 2026-09-06 (parité {D,γ}=0 ; ordre 1 ; non-trivialité D≠0) ;
      vérificateur d'A3b (filiation déclarée — KO6-REAL-1.0) ; méthode
      des orbites de T1 (T1-KO6-IMP-1.0) avec filtre ordre 1 ajouté.
  Protocole : ce script. Espace figé (bornes déclarées) :
      n ∈ {3, 5, 7} (impair) ; γ = diag(+1×a, −1×b), a+b=n, a,b ≥ 1 ;
      P projecteur diagonal non trivial (tous les sous-ensembles,
      1 ≤ rang ≤ n−1), Q = I − P ;
      J = J₀∘K, J₀ ∈ {permutations signées par blocs de chirality,
      J₀²=+1} (énumérées exhaustivement — machine de T1) ;
      D réel symétrique hors-chiral, entrées {0,±1}, D≠0.
      Classement de chaque (P, J₀) : J₀PRÉSERVE (σ(S_P)=S_P) /
      ÉCHANGE (σ(S_P)=S_Q) / MÉLANGE (sinon).
      Condition d'ordre 1 exacte (déclarée, dérivée) : Q' = J₀QJ₀ reste
      diagonale, Q'_αα = Q_{σ(α)} ; pour chaque orbite de σ sur H⁺×H⁻ :
      [[D,P],Q']=0 ⟺ (P_x=P_y) ∨ (P_{σ(x)}=P_{σ(y)}) sur chaque paire
      de l'orbite ; consistence de signe JD=−DJ comme dans T1.
      Comptes exacts par orbites (3^k − 1) ; recoupement par
      énumération brute à n=3 (toutes P, tous J₀, tous D) ; exemplaires
      vérifiés matrice par matrice (vérificateur A3b étendu à n).
  Lemmes pré-enregistrés :
      LEMME A (échange) : J₀ P J₀ = Q avec J₀ préservant la chirality
      (Jγ=+γJ) impose rang(P∩H⁺) = rang(Q∩H⁺) et rang(P∩H⁻)=rang(Q∩H⁻),
      donc a, b pairs, donc n pair. À n impair : ZÉRO (P,J₀) échangeant.
      LEMME B (préservation) : si un secteur enjambe les deux
      chiralités, existence constructive dès n=3 (orbite intra-secteur
      de longueur 1 à signe libre).
      Mesure C (mélange) : publiée quel qu'en soit le résultat
      (discipline E1 de F4 — aucune cible).
  Falsifieur : (i) un seul (P,J₀) échangeant à n impair (tue le
      lemme A) ; (ii) inexistence là où le lemme B prédit l'existence ;
      (iii) mismatch du recoupement brut n=3.
  Prédiction pré-enregistrée : lemme A confirmé (0 échange) ; lemme B
      confirmé (existence dès n=3) ; mélange : existence possible
      (analyse déclarée — la disjonction de l'ordre 1 sauve certaines
      orbites).
  Verdict : comptes par classe et par n + matrices explicites + statut
      mesuré de « 2+2+3=7 » (rangs 2/5 à n=7).
  Gouvernance : campagne LOCALE — aucun push GitHub sans décision
      d'auteur datée (pause de tri du 08/09/2026).
"""

import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9  # figé (filiation KO6-REAL-1.0)


# ------------------------------------------------------------------ structures
def gamma_de(a, b):
    return np.diag([1.0] * a + [-1.0] * b)


def J_agit(M, J0_):
    return J0_ @ np.conj(M) @ J0_


def verifie(D_, J0_, gamma, P_):
    """Vérificateur d'A3b étendu à n et aux projecteurs (P, Q) déclarés —
    filiation KO6-REAL-1.0 : mêmes axiomes, même tolérance."""
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


# --------------------------------------- machine de T1 (filiation déclarée)
def involutions_signees(a, b):
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


def D_de_B(B, a, b):
    D = np.zeros((a + b, a + b))
    D[:a, a:] = B
    D[a:, :a] = B.T
    return D


# --------------------------------------- orbites + filtre ordre 1 (T2)
def orbites_D(sigma, s, a, b, Pset):
    """Compte exact des D ∈ {0,±1} hors-chiraux, D≠0, vérifiant JD=−DJ
    ET l'ordre 1 (filtre T2 déclaré). Classe l'action de J₀ sur les
    secteurs. Retourne (nb, exemple_B, classe, k_orbites_libres,
    k_orbites_sans_ordre1)."""
    n = a + b
    SP = set(Pset)
    SQ = set(range(n)) - SP
    image = {sigma[i] for i in SP}
    if image == SP:
        classe = "preserve"
    elif image == SQ:
        classe = "echange"
    else:
        classe = "melange"

    def P_(i):
        return 1 if i in SP else 0

    vu = set()
    k = 0           # orbites libres avec ordre 1
    k_sans = 0      # orbites libres sans le filtre ordre 1 (mesure de morsure)
    exemple = np.zeros((a, b))
    a_un = False
    for x in range(a):
        for y in range(a, n):
            if (x, y) in vu:
                continue
            x2, y2 = sigma[x], sigma[y]
            if (x2, y2) == (x, y):
                vu.add((x, y))
                signe_ok = (s[x] * s[y] == -1)
                ordre1_ok = (P_(x) == P_(y))
                if signe_ok:
                    k_sans += 1
                    if ordre1_ok:
                        k += 1
                        if not a_un:
                            exemple[x, y - a] = 1.0
                            a_un = True
            else:
                vu.add((x, y))
                vu.add((x2, y2))
                signe_ok = (s[x] * s[y] * s[x2] * s[y2] == +1)
                # ordre 1 sur l'orbite : les deux paires donnent la MÊME
                # condition (P_x=P_y) ∨ (P_{σx}=P_{σy}) — déclaré
                ordre1_ok = (P_(x) == P_(y)) or (P_(x2) == P_(y2))
                if signe_ok:
                    k_sans += 1
                    if ordre1_ok:
                        k += 1
                        if not a_un:
                            exemple[x, y - a] = 1.0
                            exemple[x2, y2 - a] = -s[x] * s[y]
                            a_un = True
    nb = (3 ** k - 1) if k else 0
    return nb, (exemple if a_un else None), classe, k, k_sans


# --------------------------------------- énumération principale
def enumeration(n):
    """Toutes (a,b), tous P, tous J₀ — comptes exacts par classe."""
    classes = ("preserve", "echange", "melange")
    stats = {c: {"combos": 0, "combos_avec_D": 0, "D_total": 0,
                 "k_somme": 0, "k_sans_somme": 0} for c in classes}
    exemples = {}
    rangs_2_5 = None  # le cas « 2+2+3=7 » à n=7
    for a in range(1, n):
        b = n - a
        gamma = gamma_de(a, b)
        J0s = involutions_signees(a, b)
        for r in range(1, n):
            for Pset in itertools.combinations(range(n), r):
                for sigma, s in J0s:
                    nb, ex, classe, k, k_sans = orbites_D(sigma, s, a, b, Pset)
                    st = stats[classe]
                    st["combos"] += 1
                    st["D_total"] += nb
                    st["k_somme"] += k
                    st["k_sans_somme"] += k_sans
                    if nb > 0:
                        st["combos_avec_D"] += 1
                        cle = (classe, a, b, r)
                        if cle not in exemples:
                            J0_ = np.zeros((n, n))
                            for j in range(n):
                                J0_[sigma[j], j] = s[j]
                            D_ = D_de_B(ex, a, b)
                            Pm = np.zeros((n, n))
                            for i in Pset:
                                Pm[i, i] = 1.0
                            v = verifie(D_, J0_, gamma, Pm)
                            exemples[cle] = {
                                "verifie_TOUS": v["TOUS"],
                                "P": sorted(Pset), "J0_diag_ou_perm": str(sigma),
                                "signes": s, "D": D_.tolist()}
    return stats, exemples


# --------------------------------------- recoupement brut n=3
def brut_n3():
    """Énumération BRUTE à n=3 : toutes (a,b), tous P, tous J₀, tous
    D ∈ {0,±1} hors-chiraux — vérifie les comptes par orbites, classe
    par classe, avec le vérificateur matriciel complet."""
    comptes = {"preserve": 0, "echange": 0, "melange": 0}
    for a in (1, 2):
        b = 3 - a
        gamma = gamma_de(a, b)
        for r in (1, 2):
            for Pset in itertools.combinations(range(3), r):
                Pm = np.zeros((3, 3))
                for i in Pset:
                    Pm[i, i] = 1.0
                for sigma, s in involutions_signees(a, b):
                    _, _, classe, _, _ = orbites_D(sigma, s, a, b, Pset)
                    J0_ = np.zeros((3, 3))
                    for j in range(3):
                        J0_[sigma[j], j] = s[j]
                    for mask in itertools.product([0, 1, -1], repeat=a * b):
                        B = np.array(mask, dtype=float).reshape(a, b)
                        if not np.any(B):
                            continue
                        if verifie(D_de_B(B, a, b), J0_, gamma, Pm)["TOUS"]:
                            comptes[classe] += 1
    return comptes


def main():
    t0 = time.time()
    print("T2 — taille impaire, A=ℂ⊕ℂ, ordre 1 non vacuous   [T2-KO6-O1IMP-1.0 gelé]")
    print("=" * 76)

    resultats = {}
    exemples_tous = {}
    for n in (3, 5, 7):
        stats, exemples = enumeration(n)
        resultats[n] = stats
        exemples_tous[n] = exemples
        print(f"\nn={n} :")
        for c in ("preserve", "echange", "melange"):
            st = stats[c]
            print(f"  {c:<9} : {st['combos']:>9} combos (P,J₀) · "
                  f"{st['combos_avec_D']:>8} avec D≠0 · {st['D_total']:>10} D")
        morsure = (sum(st["k_sans_somme"] for st in stats.values()),
                   sum(st["k_somme"] for st in stats.values()))
        print(f"  morsure de l'ordre 1 : {morsure[0]} orbites libres sans "
              f"filtre → {morsure[1]} avec ordre 1")

    # ---- recoupement brut n=3
    brut = brut_n3()
    print(f"\nRecoupement brut n=3 : {brut}")
    ok_brut = all(brut[c] == resultats[3][c]["D_total"]
                  for c in ("preserve", "echange", "melange"))
    print("  →", "OK (3 classes conformes)" if ok_brut else "MISMATCH")

    # ---- exemplaires vérifiés matrice par matrice
    ex_ok = sum(1 for n_ in exemples_tous for e in exemples_tous[n_].values()
                if e["verifie_TOUS"])
    ex_tot = sum(len(exemples_tous[n_]) for n_ in exemples_tous)
    print(f"Exemplaires vérifiés (vérificateur A3b étendu) : {ex_ok}/{ex_tot}")

    # ---- lemme A : zéro échange à n impair ?
    echange_zero = all(resultats[n_]["echange"]["combos"] == 0
                       for n_ in (3, 5, 7))
    print("Lemme A (échange ⇒ n pair) :",
          "CONFIRMÉ — 0 combo échangeant à n=3,5,7" if echange_zero
          else "RÉFUTÉ — un échange existe à n impair")

    # ---- lemme B : existence en préservation dès n=3
    lemmeB = resultats[3]["preserve"]["D_total"] > 0
    print("Lemme B (existence en préservation dès n=3) :",
          "CONFIRMÉ" if lemmeB else "RÉFUTÉ")

    # ---- cas « 2+2+3=7 » : rangs (2,5) à n=7
    cas7 = {}
    for (classe, a, b, r), e in exemples_tous[7].items():
        if r in (2, 5) and e["verifie_TOUS"]:
            cas7.setdefault(f"{classe} (a={a},b={b},rang={r})", True)
    print(f"Cas rangs 2/5 à n=7 avec D≠0 vérifié : {sorted(cas7)}")

    verdict = {
        "chantier": "T2-Q-KO6-T2-2026-09",
        "protocole": "T2-KO6-O1IMP-1.0 (gelé, local)",
        "table": "C-KO6-A3b (J²=+1, Jγ=+γJ, JD=−DJ) — datée",
        "algebre": "A = ℂ ⊕ ℂ (deux scalaires) — ordre 1 non vacuous",
        "question": "existe-t-il (D,J,γ) de taille impaire à deux "
                    "scalaires avec ordre 1 non vacuous, et dans quelle "
                    "classe d'action de J ?",
        "bornes": "n ∈ {3,5,7} ; toutes (a,b) ; tous P ; tous J₀ signés "
                  "involutifs par blocs ; D réel hors-chiral {0,±1}, D≠0",
        "comptes_par_classe": {str(k): v for k, v in resultats.items()},
        "recoupement_brut_n3": {"conforme": ok_brut, "comptes": brut},
        "exemplaires_verifies": f"{ex_ok}/{ex_tot}",
        "lemme_A_echange_implique_n_pair": {
            "énoncé": "J₀ P J₀ = Q avec Jγ=+γJ ⇒ rangs égaux par "
                      "chirality ⇒ a, b pairs ⇒ n pair",
            "mesure": "0 combo échangeant à n=3,5,7",
            "confirmé": echange_zero},
        "lemme_B_existence_preservation": {
            "énoncé": "un secteur bi-chiral ⇒ orbite intra-secteur "
                      "libre ⇒ existence dès n=3",
            "confirmé": lemmeB},
        "mesure_C_melange": {str(n_): resultats[n_]["melange"]
                             for n_ in (3, 5, 7)},
        "cas_2+2+3=7": {"rangs_2_5_n7_avec_D": sorted(cas7)},
        "reponse": None,
        "gouvernance": "campagne LOCALE — staging, pause de tri avant "
                       "toute publication",
        "durée_s": round(time.time() - t0, 2),
    }
    existe_pres = any(resultats[n_]["preserve"]["D_total"] > 0
                      for n_ in (3, 5, 7))
    verdict["reponse"] = (
        "OUI en préservation de secteurs (dès n=3) ; NON en échange "
        "(lemme A : n pair requis) ; mélange mesuré"
        if existe_pres and echange_zero else "VOIR COMPTE RENDU")
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t2_ko6_ordre1_impair_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print("\n" + "=" * 76)
    print("RÉPONSE :", verdict["reponse"])
    print("Verdict →", f)


if __name__ == "__main__":
    main()
