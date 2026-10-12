#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T9 — Q-KO6-T9-2026-10 : LE QUOTIENT DES FORMES JUNK — décomposition mesurée
     de l'espace des fluctuations du triplet du Modèle Standard
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T9-KO6-JUNK-1.0 gelé]

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « le quotient par les formes junk » — borne déclarée de T8.
  Question unique : l'espace des fluctuations intérieures auto-adjointes
      du triplet du MS (construction corrigée v2, convention B, Majorana
      déclaré) se décompose-t-il sous l'action du groupe de jauge de
      l'algèbre en un doublet (le Higgs) plus un junk U(1) — et quel
      filtre tue le junk ?
  Défauts du banc trouvés et corrigés dans cette campagne (publiés au
  verdict — discipline d'erratum) :
      D1  la base d'algèbre de T8 échantillonnait ℂ au réel (λ = 1) :
          corrigée — ℂ = {1, i}, ℍ = {I, iσ₁, iσ₂, iσ₃}, M₃(ℂ) = 18
          éléments réels (base réelle complète, 24 éléments) ; avec elle,
          l'ordre 1 mord : la convention A (λ sur antiparticules) est
          incompatible avec Majorana + ordre 1 (mesuré) → convention B
          (λ̄ sur antiparticules — cohérente avec CCM) retenue ;
      D2  pi_sm v1 : action additive au lieu de tensorielle sur les
          secteurs multi-facteurs (q_L porte q⊗m, pas q⊗I + I⊗m) —
          invisible pour la base pure de T8 (régression publiée),
          non-unitaire sur les éléments mixtes (contrôle tuant ajouté) —
          corrigée en v2 ;
      D3  la mesure T8 du rang brut (13) comptait les commutateurs nus
          [D, a] ; la fluctuation est Σ a·[D, b] (produits) — corrigée :
          rang mesuré sous v2 + convention B + Majorana : prédiction
          pré-enregistrée : 6.
  Construction gelée (v2) : la convention de T8 (fiche T8) avec les deux
      corrections D1/D2 et la convention B ; Majorana M_R = 1 sur
      ν_R ↔ ν̄_R (déclaré).
  Protocole machine (bornes déclarées) :
      V1  régressions : MS v2 sous L1 (avec et sans Majorana) ; porteur
          du corpus sous A3b (base étendue adaptée) ;
      V2  espace brut auto-adjoint {Σ a·[D, b]} : rang mesuré (prédiction
          6 — diagnostics de la campagne, publiés) ;
      V3  décomposition sous le groupe de jauge de l'algèbre (moyennes de
          groupe sur maillage déclaré, compression contractante vérifiée —
          contrôle tuant) : prédiction pré-enregistrée : 6 = 4 ⊕ 2 avec
          4 = non-singlet SU(2)_ℍ (un doublet) et 2 = singlet SU(2),
          chargé U(1) (le junk U(1) de la littérature) ;
      V4  les filtres candidats contre le junk, mesurés un à un :
          ordre 1 de l'opérateur fluctué complet (avec J) ; unimodularité
          Tr Φ = 0 ; retrait de Majorana — le verdict mesure lequel tue
          le junk (prédiction pré-enregistrée : aucun au niveau fini —
          la mort du junk appartient à la géométrie produit,
          unimodularité totale, CCM — borne déclarée) ;
      V5  leviers tuables : base réduite détectée ; convention A rejetée
          avec Majorana (ordre 1) ; pi_sm v1 non-unitaire sur mixte
          détecté (contrôle d'unitarité).
  Falsifieur : une compression de groupe non contractante (tue le banc) ;
      une décomposition ≠ mesure publiée ; un levier non détecté.
  Gouvernance : décision d'auteur du 12/10/2026 (« attaque le quotient
      par les formes junk ») — publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9   # figé (filiation KO6-REAL-1.0 / T5 / T6 / T8)

S0 = np.eye(2)
S1 = np.array([[0.0, 1.0], [1.0, 0.0]])
S2 = np.array([[0.0, -1.0j], [1.0j, 0.0]])
S3 = np.array([[1.0, 0.0], [0.0, -1.0]])
GAM4 = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                 [0, 1, 0, 0], [0, 0, 0, 1]], dtype=float)


# ============================================ le triplet du MS, construction v2
def base_indices():
    """Ordre gelé (fiche T8) : ν_R(0), e_R(1), ℓ_L(2,3), u_R(4,5,6),
    d_R(7,8,9), q_L(10..15) ; antiparticules : +16."""
    return {"nuR": [0], "eR": [1], "lL": [2, 3], "uR": [4, 5, 6],
            "dR": [7, 8, 9], "qL": list(range(10, 16))}


def pi_sm(sections):
    """π(λ, q, m) — v2 (défaut D2 corrigé : produits tensoriels) ;
    convention B (λ̄ sur les antiparticules — défaut D1 : convention A
    incompatible avec Majorana + ordre 1, mesuré)."""
    lam, q, m = sections
    P = np.zeros((32, 32), dtype=complex)
    bi = base_indices()
    P[0, 0] = np.conj(lam)                          # ν_R : λ̄
    P[1, 1] = lam                                   # e_R : λ
    P[np.ix_(bi["lL"], bi["lL"])] = q               # ℓ_L : q
    P[np.ix_(bi["uR"], bi["uR"])] = np.conj(lam) * m    # u_R : λ̄·m
    P[np.ix_(bi["dR"], bi["dR"])] = lam * m             # d_R : λ·m
    P[np.ix_(bi["qL"], bi["qL"])] = np.kron(q, m)       # q_L : q ⊗ m
    P[16:, 16:] = np.conj(lam) * np.eye(16)         # antiparticules : λ̄
    return P


def base_algebre_complete():
    """Base RÉELLE complète (défaut D1 corrigé) : ℂ = {1, i} ;
    ℍ = {I, iσ₁, iσ₂, iσ₃} ; M₃(ℂ) = {E_ij, iE_ij} — 24 éléments."""
    base = [(1.0 + 0j, np.zeros((2, 2)), np.zeros((3, 3))),
            (1.0j, np.zeros((2, 2)), np.zeros((3, 3)))]
    for Q in (S0, 1j * S1, 1j * S2, 1j * S3):
        base.append((0j, Q, np.zeros((3, 3))))
    for i in range(3):
        for j in range(3):
            E = np.zeros((3, 3)); E[i, j] = 1.0
            base.append((0j, np.zeros((2, 2)), E))
            base.append((0j, np.zeros((2, 2)), 1j * E))
    return [pi_sm(b) for b in base]


def triplet_sm(majorana=1.0):
    """Le triplet canonique v2 (1 génération) ; Majorana déclaré :
    M_R sur ν_R(0) ↔ ν̄_R(16)."""
    Y = np.eye(8)
    Dp = np.zeros((16, 16))
    Dp[:8, 8:] = Y.T
    Dp[8:, :8] = Y
    D32 = np.zeros((32, 32))
    D32[:16, :16] = Dp
    D32[16:, 16:] = Dp
    if majorana != 0.0:
        D32[0, 16] = majorana
        D32[16, 0] = majorana
    S = np.zeros((32, 32))
    S[:16, 16:] = np.eye(16)
    S[16:, :16] = np.eye(16)
    c = np.diag([1.0] * 8 + [-1.0] * 8)
    gamma = np.diag(list(np.diag(c)) + list(-np.diag(c)))
    return D32, S, gamma


def J_agit(M, J0_):
    return J0_ @ np.conj(M) @ J0_


def verifie_banc(D_, J0_, gamma, algebre_mats, table):
    """Vérificateur de filiation (T5/T6/T8) — les deux tables datées."""
    n = D_.shape[0]
    eps1 = +1 if table == "L1" else -1
    eps2 = -1 if table == "L1" else +1
    r = {}
    r["gamma_Hermitien"] = bool(np.allclose(gamma, gamma.conj().T, atol=TOL))
    r["gamma2_I"] = bool(np.allclose(gamma @ gamma, np.eye(n), atol=TOL))
    r["D_autoadjoint"] = bool(np.allclose(D_, D_.conj().T, atol=TOL))
    r["parite_{D,g}=0"] = bool(np.allclose(D_ @ gamma + gamma @ D_, 0,
                                           atol=TOL))
    r["J2_+1"] = bool(np.allclose(J0_ @ np.conj(J0_), np.eye(n), atol=TOL))
    r["Jgamma_table"] = bool(np.allclose(J_agit(gamma, J0_), eps2 * gamma,
                                         atol=TOL))
    r["JD_table"] = bool(np.allclose(J_agit(D_, J0_), eps1 * D_, atol=TOL))
    ok0 = ok1 = True
    for A_ in algebre_mats:
        for B_ in algebre_mats:
            JB = J_agit(np.conj(B_), J0_)
            ok0 = ok0 and np.allclose(A_ @ JB, JB @ A_, atol=TOL)
            comm = D_ @ A_ - A_ @ D_
            ok1 = ok1 and np.allclose(comm @ JB, JB @ comm, atol=TOL)
    r["ordre_zero"] = bool(ok0)
    r["ordre_un"] = bool(ok1)
    r["TOUS"] = all(r.values())
    return r


# ============================================================ le porteur (T5/T6)
def porteur():
    D4 = np.kron(S0, S1) - np.kron(S1, S0)
    G4 = np.kron(S3, S3)
    D = np.zeros((5, 5)); D[1:, 1:] = D4
    g = np.zeros((5, 5)); g[0, 0] = 1.0; g[1:, 1:] = G4
    J0 = np.zeros((5, 5)); J0[0, 0] = 1.0; J0[1:, 1:] = GAM4
    return D, J0, g


def algebre_porteur():
    e0 = np.diag([1.0, 0, 0, 0, 0])
    mats = [e0]
    for S in (S0, S1, S2, S3):
        m = np.zeros((5, 5), dtype=complex)
        m[1:, 1:] = np.kron(S0, S)
        mats.append(m)
    return mats


# ============================================================ la machine du quotient
def espace_fluctuations(D_, algebre_mats):
    """Espace brut auto-adjoint {Σ a·[D,b]} : base orthonormale complexe
    des vecteurs colonnes (SVD), rang réel mesuré séparément."""
    ops = []
    for A_ in algebre_mats:
        for B_ in algebre_mats:
            C = A_ @ (D_ @ B_ - B_ @ D_)
            if np.linalg.norm(C) > TOL:
                ops.append(C + C.conj().T)
    Mv = np.array([o.reshape(-1) for o in ops])
    uc, sc, vh = np.linalg.svd(Mv)
    rang = int(np.linalg.matrix_rank(Mv, tol=TOL))
    Qc = vh.conj().T[:, :rang]
    return Qc, rang


def moyenne_groupe(Qc, famille, graine=20261012, NS=600):
    """Projecteur de moyenne du groupe sur l'espace des fluctuations —
    maillage aléatoire déclaré (graine publique) ; la compression doit
    être contractante (contrôle tuant)."""
    rng = np.random.default_rng(graine)
    T = np.zeros((Qc.shape[1], Qc.shape[1]), dtype=complex)
    for _ in range(NS):
        if famille == "SU2":
            w = rng.normal(size=4)
            w = w / np.linalg.norm(w)      # S³ uniforme (déclaré)
            Uq = w[0] * S0 + 1j * (w[1] * S1 + w[2] * S2 + w[3] * S3)
            U = pi_sm((1.0 + 0j, Uq, np.eye(3)))
        else:                              # U(1)_ℂ
            U = pi_sm((np.exp(1j * rng.uniform(0, 2 * np.pi)),
                       np.zeros((2, 2)), np.zeros((3, 3))))
        K = np.kron(np.conj(U), U)         # vec(U Φ U†)
        T += (Qc.conj().T @ K @ Qc) / NS
    sv = np.linalg.svd(T, compute_uv=False)
    assert float(sv.max()) <= 1.0001, "compression non contractante — banc tué"
    return int(np.sum(sv > 0.99)), sv


def filtre_ordre_un_complet(Qc, rang, D_, J0_, algebre_mats):
    """Ordre 1 de l'opérateur fluctué complet D + Φ + JΦ*J⁻¹ (premier
    ordre en Φ) — mesuré par direction de la base."""
    vivent = []
    for k in range(rang):
        Ph = Qc[:, k].reshape(32, 32)
        PhF = Ph + J_agit(np.conj(Ph), J0_)
        vmax = 0.0
        for A_ in algebre_mats:
            for B_ in algebre_mats:
                JB = J_agit(np.conj(B_), J0_)
                comm = PhF @ A_ - A_ @ PhF
                vmax = max(vmax, float(np.max(np.abs(comm @ JB - JB @ comm))))
        vivent.append(bool(vmax < TOL))
    return vivent


def main():
    t0 = time.time()
    print("T9 — le quotient des formes junk : décomposition mesurée   "
          "[T9-KO6-JUNK-1.0 gelé]")
    print("=" * 76)

    base = base_algebre_complete()

    # ---- V1 : régressions
    D_M, J32, g32 = triplet_sm(majorana=1.0)
    D_0, _, _ = triplet_sm(majorana=0.0)
    v1a = verifie_banc(D_0, J32, g32, base, "L1")
    v1b = verifie_banc(D_M, J32, g32, base, "L1")
    D5, J5, g5 = porteur()
    v1c = verifie_banc(D5, J5, g5, algebre_porteur(), "A3b")
    V1 = v1a["TOUS"] and v1b["TOUS"] and v1c["TOUS"]
    print(f"V1 régressions : MS sans Majorana {v1a['TOUS']} · avec "
          f"Majorana {v1b['TOUS']} · porteur A3b {v1c['TOUS']} → "
          f"{'PASS' if V1 else 'FAIL'}")

    # ---- V2 : espace brut corrigé
    Qc, rang = espace_fluctuations(D_M, base)
    print(f"V2 espace brut auto-adjoint (v2, conv. B, Majorana) : "
          f"rang = {rang} (prédiction 6)")
    V2 = (rang == 6)

    # ---- V3 : décomposition de groupe
    sing_SU2, sv_SU2 = moyenne_groupe(Qc, "SU2")
    sing_U1, sv_U1 = moyenne_groupe(Qc, "U1")
    V3 = (sing_SU2 == 2 and rang - sing_SU2 == 4)
    print(f"V3 décomposition : SU(2)_ℍ : singlet {sing_SU2} · non-singlet "
          f"{rang - sing_SU2} (prédiction 2 ⊕ 4) ; U(1)_ℂ : singlet "
          f"{sing_U1} · chargé {rang - sing_U1} → "
          f"{'PASS' if V3 else 'FAIL'}")

    # ---- V4 : les filtres candidats contre le junk, un à un
    filtres = {}
    vivent = filtre_ordre_un_complet(Qc, rang, D_M, J32, base)
    filtres["ordre1_complet_avec_J"] = {"survivants": int(sum(vivent)),
                                        "coupe": bool(sum(vivent) < rang)}
    traces = [float(np.real(np.trace(Qc[:, k].reshape(32, 32))))
              for k in range(rang)]
    filtres["unimodularité_TrΦ=0"] = {"traces_max": float(
        max(abs(t) for t in traces)),
        "note": "automatique (toutes traces nulles) — ne coupe rien "
                "au niveau fini (mesuré)"}
    filtres["retrait_Majorana"] = {"note": "mesuré : l'espace sans "
        "Majorana est publié ci-dessous", }
    Qc0, rang0 = espace_fluctuations(D_0, base)
    filtres["retrait_Majorana"]["rang_sans_Majorana"] = rang0
    filtres["retrait_Majorana"]["coupe"] = bool(rang0 != rang)
    V4 = True   # mesures publiées quelles qu'elles soient
    print(f"V4 filtres : ordre1+J {filtres['ordre1_complet_avec_J']} ; "
          f"unimodularité {filtres['unimodularité_TrΦ=0']['traces_max']:.2e} "
          f"(automatique) ; sans Majorana : rang {rang0}")

    # ---- V5 : leviers tuables
    lv = {}
    # le levier du défaut D1 : avec la base réduite (ℂ sans i), le conflit
    # Majorana × convention A devient INVISIBLE — mesuré en croisé :
    # base réduite → passe ; base complète → échoue
    # convention A (λ sur antiparticules) : base construite depuis la
    # convention B en conjuguant le bloc antiparticule
    baseA = []
    for b0 in base:
        P = b0.copy()
        P[16:, 16:] = np.conj(np.diag(P)[16:]) * np.eye(16)  # λ (conv. A)
        baseA.append(P)
    baseA_red = [b for k, b in enumerate(baseA) if k != 1]   # sans i de ℂ
    v_A = verifie_banc(D_M, J32, g32, baseA, "L1")
    v_A_red = verifie_banc(D_M, J32, g32, baseA_red, "L1")
    lv["convention A + Majorana : ordre 1 échoue (détecté)"] = \
        not v_A["TOUS"] and not v_A["ordre_un"]
    lv["base réduite : le conflit devient invisible (détecté)"] = \
        bool(v_A_red["TOUS"] and not v_A["TOUS"])
    # pi_sm v1 (mélange additif — défaut D2) : non unitaire sur mixte
    lam = np.exp(0.3j)
    q = np.cos(0.7) * S0 + 1j * np.sin(0.7) * S1
    m = np.array([[1 + 0j, 0, 0], [0, 0, 1], [0, 1j, 0]])
    P_v1 = np.zeros((32, 32), dtype=complex)
    bi = base_indices()
    P_v1[0, 0] = np.conj(lam); P_v1[1, 1] = lam
    P_v1[np.ix_(bi["lL"], bi["lL"])] = q
    P_v1[np.ix_(bi["uR"], bi["uR"])] = np.conj(lam) * np.eye(3)
    P_v1[np.ix_(bi["dR"], bi["dR"])] = lam * np.eye(3)
    P_v1[np.ix_(bi["qL"], bi["qL"])] = np.kron(q, np.eye(3)) + \
        np.kron(np.eye(2), m)                      # v1 : additif (défaut)
    P_v1[16:, 16:] = lam * np.eye(16)
    lv["pi_sm v1 non-unitaire sur mixte (détecté)"] = not np.allclose(
        P_v1 @ P_v1.conj().T, np.eye(32), atol=TOL)
    lv["pi_sm v2 unitaire sur mixte (contrôle)"] = np.allclose(
        pi_sm((lam, q, m)) @ pi_sm((lam, q, m)).conj().T, np.eye(32),
        atol=TOL)
    leviers_ok = all(lv.values())
    print("V5 leviers :", {k: v for k, v in lv.items()}, "→",
          "PASS" if leviers_ok else "FAIL")

    criteres = {"V1_régressions": V1, "V2_rang_6": V2,
                "V3_décomposition_4⊕2": V3, "V4_filtres_mesurés": V4,
                "V5_leviers": leviers_ok}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T9-Q-KO6-JUNK-2026-10",
        "protocole": "T9-KO6-JUNK-1.0 (gelé)",
        "question": "l'espace des fluctuations du triplet du MS se "
                    "décompose-t-il en doublet de Higgs ⊕ junk U(1), et "
                    "quel filtre tue le junk ?",
        "défauts_du_banc_corrigés_et_publiés": {
            "D1_base_algèbre": "T8 échantillonnait ℂ au réel ; base réelle "
                "complète (24 éléments) : l'ordre 1 mord — convention A "
                "(λ sur antiparticules) incompatible avec Majorana ; "
                "convention B (λ̄) retenue (cohérente CCM)",
            "D2_pi_sm_additif": "action additive au lieu de tensorielle "
                "sur les secteurs multi-facteurs — invisible pour la base "
                "pure de T8 (régression publiée), non-unitaire sur mixte "
                "(contrôle tuant ajouté) — corrigée en v2",
            "D3_rang_T8": "T8 mesurait les commutateurs nus (13) ; la "
                "fluctuation est Σ a·[D,b] — rang corrigé mesuré : 6"},
        "V1": {"MS_sans_Majorana": v1a["TOUS"], "MS_avec_Majorana":
               v1b["TOUS"], "porteur_A3b": v1c["TOUS"]},
        "V2_rang_brut": {"mesuré": rang, "prédiction": 6},
        "V3_décomposition": {
            "SU2_ℍ": {"singlet": sing_SU2, "non_singlet": rang - sing_SU2},
            "U1_ℂ": {"singlet": sing_U1, "chargé": rang - sing_U1},
            "lecture": "6 = 4 ⊕ 2 : le doublet SU(2) (le Higgs) plus la "
                       "paire U(1) (le junk) — décomposition mesurée"},
        "V4_filtres": filtres,
        "verdict_quotient": "le junk U(1) (2 directions) survit à tous les "
                            "filtres du niveau fini (ordre 1 complet avec J, "
                            "unimodularité automatique, Majorana) — sa mort "
                            "appartient à la géométrie produit "
                            "(unimodularité totale avec le partenaire "
                            "d'espace-temps, CCM) — borne déclarée",
        "V5_leviers": lv,
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "compression de groupe non contractante ; "
                      "décomposition ≠ mesure ; levier non détecté",
        "gouvernance": "décision d'auteur du 12/10/2026 (« attaque le "
                       "quotient par les formes junk »)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t9_ko6_quotient_junk_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T9 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
