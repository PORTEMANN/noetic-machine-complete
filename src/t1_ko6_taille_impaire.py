#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T1 — Q-KO6-2026-09 : TAILLE IMPAIRE SOUS C-KO6-A3b, SCALAIRE UNIQUE
====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T1-KO6-IMP-1.0 gelé]

FICHE (gelée avant le run — 09/09/2026, campagne LOCALE, staging)
  Tiroir   : banc
  Objet    : « triplet spectral fini de taille impaire sous C-KO6-A3b »
  Question unique (Q-KO6-2026-09, CAMPAIGNS.md) :
      Sous la table C-KO6-A3b (datée), existe-t-il (D, J, γ) de taille
      n impaire vérifiant l'ordre 1 avec un scalaire complexe unique ?
  Conventions citées : C-KO6-A3b (J²=+1, Jγ=+γJ, JD=−DJ) ; AXIOMES.md
      gelé 2026-09-06 : 1. parité {D,γ}=0 ; 4. ordre 1
      [[D,π(a)], Jπ(b)*J⁻¹]=0 ; 6. un scalaire complexe unique (A=ℂ) ;
      7. non-trivialité D≠0. Lemme de parité : inapplicable sous
      C-KO6-A3b (Jγ=+γJ → J préserve les chiralités).
  Protocole : ce script. Espace figé (bornes déclarées) :
      n ∈ {1, 3, 5, 7} (impair) ; γ = diag(+1×p, −1×q), p+q=n ;
      J = J₀∘K (K conjugaison), J₀ ∈ {permutations signées préservant
      les blocs de chirality, J₀²=+1} — comptées exactement ;
      D ∈ {réelles symétriques hors-chirales à entrées 0,±1}, D≠0.
      Comptage exact par méthode des orbites (la condition JD=−DJ est
      une contrainte linéaire orbite par orbite — déclarée), recoupé
      par énumération brute à n=3. Ordre 1 avec A=ℂ : π(λ)=λI →
      [D,π(λ)]=0 identiquement — la condition est VACUOUS pour un
      scalaire unique : ce fait est mesuré numériquement (scalaires
      aléatoires) et déclaré, pas caché.
  Falsifieur : lemme ou énumération exhaustive montrant l'inexistence
      (aucun (J₀,D), D≠0, à toutes les tailles impaires des bornes).
  Prédiction pré-enregistrée : EXISTENCE dès n=3 (argument constructif
      déclaré : σ=id, une seule signature −1 dans H⁺, une entrée
      D_{p,p+1}=1 — orbite de longueur 1 libre) ; n=1 exclu
      ({D,γ}=0 avec γ=±I force D=0).
  Verdict : existencia (oui/non) + comptes exacts + matrices explicites.
  Gouvernance : campagne LOCALE (pause de tri du 08/09/2026) — aucun
      push GitHub sans décision d'auteur datée.

Lecture honnête déclarée AVANT le run : avec A=ℂ, l'ordre 1 est
vacuous ; la substance de la question vit dans la TAILLE impaire sous
la table A3b, pas dans l'ordre 1. Si l'auteur veut une question plus
forte (ordre 1 non vacuous en taille impaire, A plus riche), c'est une
NOUVELLE fiche gelée (point 6 de la boucle : pas de critère déplacé).
"""

import hashlib
import itertools
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9  # figé (même tolérance que KO6-REAL-1.0)


# ------------------------------------------------------------------ structures
def gamma_de(p, q):
    return np.diag([1.0] * p + [-1.0] * q)


def J_agit(M, J0_):
    """J M J⁻¹ = J₀ M* J₀ (anti-linéaire, J₀ réelle involutive)."""
    return J0_ @ np.conj(M) @ J0_


def verifie(D_, J0_, gamma):
    """Les 7 axiomes d'AXIOMES.md, matrice par matrice, tolérance figée.
    A = ℂ : π(λ) = λI — ordre 1 testé numériquement sur scalaires
    aléatoires (déclaré vacuous analytiquement)."""
    n = D_.shape[0]
    r = {}
    r["parite_{D,g}=0"] = bool(np.allclose(D_ @ gamma + gamma @ D_, 0, atol=TOL))
    r["J2_+1"] = bool(np.allclose(J_agit(J_agit(np.eye(n), J0_), J0_), np.eye(n), atol=TOL))
    r["Jgamma_+"] = bool(np.allclose(J_agit(gamma, J0_), gamma, atol=TOL))
    r["JD_-DJ"] = bool(np.allclose(J_agit(D_, J0_), -D_, atol=TOL))
    # ordre 1, A = ℂ : [[D, λI], J(μI)*J⁻¹] = 0 — mesuré sur scalaires aléatoires
    rng = np.random.default_rng(0)
    ok = True
    for _ in range(8):
        lam, mu = rng.standard_normal() + 1j * rng.standard_normal(), \
                  rng.standard_normal() + 1j * rng.standard_normal()
        comm = D_ @ (lam * np.eye(n)) - (lam * np.eye(n)) @ D_
        bopp = J_agit(np.conj(mu) * np.eye(n), J0_)
        ok = ok and np.allclose(comm @ bopp, bopp @ comm, atol=TOL)
    r["ordre_un_A=C"] = bool(ok)
    r["D_non_nul"] = bool(np.any(np.abs(D_) > TOL))
    r["TOUS"] = all(r.values())
    return r


# ------------------------------------------------- énumération exacte (orbites)
def involutions_signees(p, q):
    """J₀ = permutations signées préservant les blocs (p, q), J₀² = +1.
    Rend (sigma, s) avec sigma involution de S_n par blocs, s_i s_{σ(i)}=+1."""
    n = p + q
    res = []
    for perm_p in itertools.permutations(range(p)):
        for perm_q in itertools.permutations(range(p, n)):
            sigma = perm_p + perm_q
            if any(sigma[sigma[i]] != i for i in range(n)):
                continue  # σ involution
            # signes : s_i s_{σ(i)} = 1 → sur les 2-cycles (i,σ(i)) : s_i = s_{σ(i)}
            libres = [i for i in range(n) if i <= sigma[i]]
            for bits in itertools.product([1, -1], repeat=len(libres)):
                s = [0] * n
                for i, b in zip(libres, bits):
                    s[i] = b
                    s[sigma[i]] = b
                res.append((sigma, s))
    return res


def compte_D_orbites(sigma, s, p, q):
    """Espace des D réels sym. hors-chiraux avec J₀ D J₀ = −D, entrées {0,±1}.
    Contrainte orbite par orbite sur le bloc B (H⁺×H⁻) :
      B_{σ(i),σ(j)} = −s_i s_j B_ij.
    Orbite longueur 1 : libre si s_i s_j = −1, sinon nulle.
    Orbite longueur 2 : libre si s_i s_j s_{i'} s_{j'} = +1, sinon nulle.
    k orbites libres → 3^k − 1 matrices D non nulles (entrées {0,±1}).
    Retourne (nb_D_non_nuls, exemple_B_ou_None)."""
    n = p + q
    vu = set()
    k_libres = 0
    exemple = np.zeros((p, q))
    a_un = False
    for i in range(p):
        for j in range(p, n):
            if (i, j) in vu:
                continue
            i2, j2 = sigma[i], sigma[j]
            if (i2, j2) == (i, j):
                vu.add((i, j))
                if s[i] * s[j] == -1:
                    k_libres += 1
                    if not a_un:
                        exemple[i, j - p] = 1.0
                        a_un = True
            else:
                vu.add((i, j))
                vu.add((i2, j2))
                if s[i] * s[j] * s[i2] * s[j2] == +1:
                    k_libres += 1
                    if not a_un:
                        exemple[i, j - p] = 1.0
                        exemple[i2, j2 - p] = -s[i] * s[j] * 1.0
                        a_un = True
    nb = (3 ** k_libres - 1) if k_libres else 0
    return nb, (exemple if a_un else None)


def enumeration_exacte(n):
    """Pour chaque (p,q) avec p+q=n : compte exact des (J₀, D), D≠0,
    dans l'espace figé {0,±1}, par la méthode des orbites."""
    out = []
    for p in range(0, n + 1):
        q = n - p
        if p == 0 or q == 0:
            out.append({"p": p, "q": q, "n_J0": 0, "n_couples_D_non_nul": 0,
                        "note": "{D,γ}=0 avec γ=±I force D=0 — exclu"})
            continue
        n_J0 = 0
        total = 0
        exemple = None
        for sigma, s in involutions_signees(p, q):
            n_J0 += 1
            nb, ex = compte_D_orbites(sigma, s, p, q)
            total += nb
            if exemple is None and ex is not None:
                exemple = (sigma, s, ex)
        out.append({"p": p, "q": q, "n_J0": n_J0,
                    "n_couples_D_non_nul": total,
                    "exemple_trouve": exemple is not None})
    return out


def D_de_B(B, p, q):
    D = np.zeros((p + q, p + q))
    D[:p, p:] = B
    D[p:, :p] = B.T
    return D


def brut_n(n, couples):
    """Énumération BRUTE (tous J₀ signés permutations J₀²=I préservant γ,
    tous D ∈ {0,±1} hors-chiraux) pour les (p,q) listés : recoupe le
    comptage par orbites et vérifie les 7 axiomes matrice par matrice."""
    res = {}
    for p, q in couples:
        nn = p + q
        gamma = gamma_de(p, q)
        nb_ok = 0
        premier = None
        for sigma, s in involutions_signees(p, q):
            J0_ = np.zeros((nn, nn))
            for j in range(nn):
                J0_[sigma[j], j] = s[j]
            for mask in itertools.product([0, 1, -1], repeat=p * q):
                B = np.array(mask, dtype=float).reshape(p, q)
                if not np.any(B):
                    continue
                D_ = D_de_B(B, p, q)
                if verifie(D_, J0_, gamma)["TOUS"]:
                    nb_ok += 1
                    if premier is None:
                        premier = (D_, J0_)
        res[f"p{p}q{q}"] = {"couples_ok_brut": nb_ok, "premier": premier}
    return res


def exemplaires_orbites_verifies(n):
    """Pour CHAQUE (p,q) et CHAQUE J₀ à orbites libres : l'exemplaire B
    construit par la méthode des orbites passe le vérificateur (7 axiomes).
    Contrôle que le comptage ne porte que sur de vrais triplets."""
    total, ok = 0, 0
    for p in range(1, n):
        q = n - p
        gamma = gamma_de(p, q)
        for sigma, s in involutions_signees(p, q):
            nb, B = compte_D_orbites(sigma, s, p, q)
            if B is None:
                continue
            J0_ = np.zeros((n, n))
            for j in range(n):
                J0_[sigma[j], j] = s[j]
            D_ = D_de_B(B, p, q)
            total += 1
            ok += verifie(D_, J0_, gamma)["TOUS"]
    return ok, total


# ----------------------------------------------------------------------- leviers
def leviers_n3(D_, J0_, gamma):
    """Batterie tuante (même discipline qu'A3b-C1) : chaque axiome tué
    séparément doit être détecté par le vérificateur."""
    n = D_.shape[0]
    J0_swap = np.zeros((n, n))  # J₀ échange les chiralités → Jγ=−γJ
    J0_swap[0, 2] = J0_swap[2, 0] = 1.0
    J0_swap[1, 1] = 1.0
    return {
        "parité tuée (D→γ)": verifie(gamma.copy(), J0_, gamma),
        "J² → −1": verifie(D_, 1j * J0_, gamma),
        "Jγ → −γJ (swap chiralités)": verifie(D_, J0_swap, gamma),
        "JD → +DJ (D_alt avec J₀DJ₀=+D)": None,  # construit ci-dessous
    }


def main():
    t0 = time.time()
    print("T1 — Q-KO6-2026-09 : taille impaire sous C-KO6-A3b   [T1-KO6-IMP-1.0 gelé]")
    print("=" * 74)

    # ---- comptage exact (orbites), bornes figées n ∈ {1,3,5,7}
    comptes = {}
    for n in (1, 3, 5, 7):
        tab = enumeration_exacte(n)
        comptes[n] = tab
        tot = sum(e["n_couples_D_non_nul"] for e in tab)
        print(f"n={n} : " + " ; ".join(
            f"(p={e['p']},q={e['q']}) J0={e['n_J0']} couples={e['n_couples_D_non_nul']}"
            for e in tab) + f"  → total D≠0 : {tot}")

    # ---- recoupement brut n=3 complet + n=5 (p,q)=(1,4),(2,3),(3,2),(4,1)
    brut = brut_n(3, [(1, 2), (2, 1)])
    brut.update(brut_n(5, [(1, 4), (2, 3), (3, 2), (4, 1)]))
    print("\nRecoupement brut (n=3 complet, n=5 tous blocs) :")
    ok_recoupe = True
    for cle, r in brut.items():
        p, q = int(cle[1]), int(cle[3])
        n = p + q
        attendu = [e["n_couples_D_non_nul"] for e in comptes[n]
                   if e["p"] == p and e["q"] == q][0]
        ok = (r["couples_ok_brut"] == attendu)
        ok_recoupe = ok_recoupe and ok
        print(f"  n={n} {cle} : brut={r['couples_ok_brut']} orbites={attendu} "
              f"→ {'OK' if ok else 'MISMATCH'}")

    # ---- exemplaires d'orbites vérifiés (n=3,5,7)
    ex_ok = {}
    for n in (3, 5, 7):
        o, t = exemplaires_orbites_verifies(n)
        ex_ok[n] = (o, t)
        print(f"  exemplaires d'orbites vérifiés n={n} : {o}/{t}")
    tous_ex_ok = all(o == t for o, t in ex_ok.values())

    # ---- exemples explicites vérifiés matrice par matrice
    exemples = {}
    for n in (3, 7):
        p, q = 2, n - 2  # plus petit p≥1 avec H⁻ plus grand — déclaré
        gamma = gamma_de(p, q)
        # construction déclarée : σ=id, s=(−1,+1,…,+1) → orbite (0,p) libre
        sigma = tuple(range(n))
        s = [-1] + [1] * (n - 1)
        J0_ = np.diag(s).astype(float)
        B = np.zeros((p, q))
        B[0, 0] = 1.0
        D_ = D_de_B(B, p, q)
        v = verifie(D_, J0_, gamma)
        exemples[n] = {"gamma_diag": [1] * p + [-1] * q, "J0_diag": s,
                       "D": D_.tolist(), "verifie": v}
        print(f"\nExemple explicite n={n} (γ=diag({p}+,{q}−), J₀=diag{s}, "
              f"D_{{1,{p+1}}}=1) :")
        print("  ", {k: vv for k, vv in v.items()}, "→",
              "PASS" if v["TOUS"] else "FAIL")

    # ---- leviers (batterie tuante) sur l'exemple n=3
    D3 = np.array(exemples[3]["D"])
    J03 = np.diag(exemples[3]["J0_diag"])
    g3 = gamma_de(2, 1)
    lv = leviers_n3(D3, J03, g3)
    # JD → +DJ : D_alt invariant sous J₀ (au lieu de anti-)
    D_alt = np.zeros((3, 3))
    D_alt[1, 2] = D_alt[2, 1] = 1.0  # orbite (1,2) : s1*s2=+1 → J₀D_altJ₀=+D_alt
    lv["JD → +DJ (D_alt avec J₀DJ₀=+D)"] = verifie(D_alt, J03, g3)
    tous_detectes = all(not v["TOUS"] for v in lv.values())
    print("\nLeviers (chaque axiome tué doit être détecté) :")
    for nom, v in lv.items():
        print(f"  {nom:<38} : détecté = {not v['TOUS']}")
    print("  →", "PASS" if tous_detectes else "FAIL")

    # ---- verdict
    existe = any(e["n_couples_D_non_nul"] > 0 for n_ in (3, 5, 7)
                 for e in comptes[n_])
    n1_exclu = all(e["n_couples_D_non_nul"] == 0 for e in comptes[1])
    verdict = {
        "chantier": "T1-Q-KO6-2026-09",
        "protocole": "T1-KO6-IMP-1.0 (gelé, local)",
        "table": "C-KO6-A3b (J²=+1, Jγ=+γJ, JD=−DJ) — datée",
        "algebre": "A = ℂ (scalaire complexe unique)",
        "question": "existe-t-il (D,J,γ) de taille n impaire vérifiant "
                    "l'ordre 1 avec un scalaire complexe unique ?",
        "ordre_un_vacuous_pour_A=C": True,
        "note_honnete": "avec A=ℂ, l'ordre 1 est vacuous (mesuré sur "
                        "scalaires aléatoires) ; la substance de la question "
                        "est la TAILLE impaire sous la table A3b. Une "
                        "question plus forte (ordre 1 non vacuous, A plus "
                        "riche, taille impaire) = nouvelle fiche gelée.",
        "bornes": "n ∈ {1,3,5,7} ; J₀ permutations signées par blocs, "
                  "J₀²=+1 ; D réel sym. hors-chiral {0,±1} ; tol 1e-9",
        "comptes_exactes": {str(k): v for k, v in comptes.items()},
        "recoupement_brut": ok_recoupe,
        "exemplaires_orbites_verifies": {str(k): f"{o}/{t}"
                                         for k, (o, t) in ex_ok.items()},
        "note_comptage": "premier run : comptage par orbites sous-comptait "
                         "(2 par orbite libre au lieu de 3^k − 1) — détecté "
                         "par le recoupement brut gelé, corrigé avant verdict ; "
                         "protocole (bornes, espace, axiomes) inchangé.",
        "exemples": {str(k): {"gamma": v["gamma_diag"], "J0": v["J0_diag"],
                              "D": v["D"], "axiomes": v["verifie"]}
                     for k, v in exemples.items()},
        "leviers_detectes": tous_detectes,
        "n1_exclu": n1_exclu,
        "reponse": "OUI — existence dès n=3" if existe else
                   "NON — inexistence sous les bornes",
        "falsifieur_statut": "non déclenché (existence)" if existe else
                             "déclenché (inexistence)",
        "prédiction_pré_enregistrée": "EXISTENCE dès n=3 ; n=1 exclu",
        "prédiction_confirmée": bool(existe and n1_exclu),
        "gouvernance": "campagne LOCALE — staging, pause de tri avant "
                       "toute publication (décision d'auteur du 08/09/2026)",
        "durée_s": round(time.time() - t0, 3),
    }
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t1_ko6_taille_impaire_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n" + "=" * 74)
    print("RÉPONSE :", verdict["reponse"])
    print("Recoupement brut :", "OK" if ok_recoupe else "MISMATCH",
          "· exemplaires orbites :",
          "tous vérifiés" if tous_ex_ok else "FAIL",
          "· leviers :", "tous détectés" if tous_detectes else "FAIL")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
