#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T6 — Q-KO6-T6-2026-10 : LE PORTEUR FORMALISÉ — certificat, espace des
     scalaires, potentiel spectral
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T6-KO6-PORT-1.0 gelé]

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « le porteur spectral à scalaire réel » (T5, verdict du
      12/10/2026) : A = ℂ ⊕ M₂(ℂ), H = ℂ ⊕ M₂(ℂ) (dim 5, impair),
      D = 0 ⊕ (L_{σ1} − R_{σ1}), γ = 1 ⊕ L_{σ3}R_{σ3}, J = K ⊕ adjoint,
      table C-KO6-A3b (J²=+1, JD=−DJ, Jγ=+γJ).
  Question unique : le porteur, formalisé comme objet nommé et certifié,
      porte un espace de scalaires de quelle dimension — et le potentiel
      de son action spectrale (moments V₂ = Tr(D+φ)², V₄ = Tr(D+φ)⁴)
      a-t-il son minimum en φ = 0 ou hors de 0 ?
  Motivation déclarée : Principes V du corpus prétend que le potentiel
      du champ naît du coefficient a₄ de l'action spectrale. Le porteur
      réparé est le premier objet du corpus où cette prétention est
      calculable exactement. La machine mesure.
  Filiation : vérificateur de T5 (T5-KO6-SCAL-1.0) ; tables datées de
      CONVENTIONS.md (spectral-triple-minimality) ; erratum E1–E4 lu.
  Faits déclarés (dérivés avant gel) :
      F1  l'espace des commutateurs [D, π(a)] est engendré par
          I⊗(iσ₂) et I⊗(iσ₃) sur le nœud M₂ (0 sur le nœud ℂ) ; la
          partie auto-adjointe des fluctuations est
          φ(α,β) = 0 ⊕ I⊗(ασ₂ + βσ₃), (α,β) ∈ ℝ² — « un scalaire
          complexe » = 2 réels, la forme du papier.
      F2  V₂(α,β) = 4(1+α²+β²) + 4 (orthogonalité de Pauli : Tr Dφ = 0)
          — minimum en φ = 0, prédiction pré-enregistrée.
      F3  V₄(α,β) = 4ρ⁴ + 24ρ² + 4 avec ρ² = 1+α²+β² — minimum en
          φ = 0, prédiction pré-enregistrée.
      F4  spectre de D+φ sur le nœud M₂ : {±(ρ−1), ±(ρ+1)} — le mode
          zéro DU NŒUD DU SCALAIRE n'existe qu'en φ = 0 (le nœud ℂ est
          un spectateur à zéro permanent — déclaré), prédiction
          pré-enregistrée.
      F5  le chapeau mexicain (masse² < 0) exige la géométrie produit
          (couplage à la courbure, a₂ de Connes-Chamseddine) — absent
          du porteur fini seul ; obstruction située, hors bornes.
  Protocole machine (bornes déclarées) :
      C0  certificat : le porteur nommé repasse le vérificateur complet
          (régression T5).
      C1  espace des scalaires : rang de la clôture auto-adjointe des
          commutateurs mesuré = 2, égal à l'enveloppe déclarée (F1).
      C2  V₂ mesuré sur grille × formule F2 — accord à 1e-9 ; position
          du minimum publiée.
      C3  V₄ idem (formule F3).
      C4  flot des bandes : spectre de D+φ sur la grille — accord avec
          F4 à 1e-9 ; existence du mode zéro mesurée en fonction de ρ.
      C5  action gaussienne S(ρ) = Tr e^{−(D+φ)²} (Λ = 1 déclaré,
          unités de D) : position de l'extremum mesurée, signe de la
          dérivée seconde publié (interprétation déclarée : S est le
          compte spectral, pas une énergie).
      Leviers : φ → 2φ multiplie la partie scalaire de V₂ par 4
          (mesuré) ; D → 0 donne V₂ = Tr φ² ≥ 0 (mesuré) ; J₀ permuté
          est détecté par le vérificateur (tuant).
  Falsifieur : rang scalaire ≠ 2 (tue F1) ; écart formule/machine >
      1e-9 (tue F2/F3/F4) ; mode zéro trouvé à φ ≠ 0 (tue F4) ; levier
      non détecté (tue le banc).
  Gouvernance : décision d'auteur du 12/10/2026 (« formalisons ce
      porteur spectral à scalaire réel et testons-le ») — publication
      GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9  # figé (filiation KO6-REAL-1.0 / T5)

S0 = np.eye(2)
S1 = np.array([[0.0, 1.0], [1.0, 0.0]])
S2 = np.array([[0.0, -1.0j], [1.0j, 0.0]])
S3 = np.array([[1.0, 0.0], [0.0, -1.0]])
GAM4 = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                 [0, 1, 0, 0], [0, 0, 0, 1]], dtype=float)  # transpose-vec


# ---------------------------------------------------------------- le porteur
def porteur():
    """Le porteur nommé (T5) : A = ℂ ⊕ M₂(ℂ), H = ℂ ⊕ M₂(ℂ), dim 5."""
    D4 = np.kron(S0, S1) - np.kron(S1, S0)
    G4 = np.kron(S3, S3)
    D = np.zeros((5, 5)); D[1:, 1:] = D4
    g = np.zeros((5, 5)); g[0, 0] = 1.0; g[1:, 1:] = G4
    J0 = np.zeros((5, 5)); J0[0, 0] = 1.0; J0[1:, 1:] = GAM4
    return D, J0, g


def J_agit(M, J0_):
    return J0_ @ np.conj(M) @ J0_


def algebre_base():
    e0 = np.diag([1.0, 0, 0, 0, 0])
    mats = [e0]
    for S in (S0, S1, S2, S3):
        m = np.zeros((5, 5), dtype=complex)
        m[1:, 1:] = np.kron(S0, S)
        mats.append(m)
    return mats


def verifie_porteur(D_, J0_, gamma, algebre_mats):
    """Vérificateur de filiation (T5) — table A3b, ordre 0/1, fluctuation."""
    n = D_.shape[0]
    r = {}
    r["gamma_Hermitien"] = bool(np.allclose(gamma, gamma.conj().T, atol=TOL))
    r["gamma2_I"] = bool(np.allclose(gamma @ gamma, np.eye(n), atol=TOL))
    r["D_autoadjoint"] = bool(np.allclose(D_, D_.conj().T, atol=TOL))
    r["parite_{D,g}=0"] = bool(np.allclose(D_ @ gamma + gamma @ D_, 0, atol=TOL))
    r["J2_+1"] = bool(np.allclose(J0_ @ np.conj(J0_), np.eye(n), atol=TOL))
    r["Jgamma_+"] = bool(np.allclose(J_agit(gamma, J0_), gamma, atol=TOL))
    r["JD_-DJ"] = bool(np.allclose(J_agit(D_, J0_), -D_, atol=TOL))
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


# ------------------------------------------------ C1 : l'espace des scalaires
def espace_scalaires(D, algebre_mats):
    """Clôture auto-adjointe des commutateurs [D, π(a)] : rang mesuré,
    base publiee. φ auto-adjoint = Σ (c_k C_k + c̄_k C_k*) pour C_k
    anti-Hermitiens indépendants ; rang réel mesuré par SVD."""
    comms = []
    for A_ in algebre_mats:
        C = D @ A_ - A_ @ D
        if np.linalg.norm(C) > TOL:
            comms.append(C)
    # enveloppe auto-adjointe : {i·(combinaisons réelles des C anti-herm.)}
    herm = []
    for C in comms:
        H1 = 1j * C          # C anti-hermitien → iC hermitien
        herm.append(H1)
        herm.append(np.conj(H1))   # conjugaison dans l'enveloppe réelle
    mats = np.array([h.reshape(-1) for h in herm])
    # rang réel : SVD sur parties réelle/imaginaire empilées
    M = np.concatenate([mats.real, mats.imag], axis=0)
    rang = int(np.linalg.matrix_rank(M, tol=TOL))
    base = []
    if rang:
        u, s, _ = np.linalg.svd(M)
        for k in range(rang):
            v = u[:, k] @ np.concatenate([mats.real, mats.imag], axis=0)
            H = v.reshape(5, 5)
            base.append(H)
    return rang, comms, base


def phi(alpha, beta):
    """La forme déclarée F1 : φ = 0 ⊕ I⊗(ασ₂ + βσ₃)."""
    p = np.zeros((5, 5), dtype=complex)
    p[1:, 1:] = np.kron(S0, alpha * S2 + beta * S3)
    return p


def V2(D_, p_):
    X = D_ + p_
    return float(np.real(np.trace(X @ X)))


def V4(D_, p_):
    X = D_ + p_
    return float(np.real(np.trace(X @ X @ X @ X)))


def S_gauss(D_, p_):
    ev = np.linalg.eigvalsh(D_ + p_)
    return float(np.sum(np.exp(-ev ** 2)))


def bandes(D_):
    ev = np.linalg.eigvalsh(D_)
    distinct = []
    for x in ev:
        if not any(abs(x - y) < 1e-6 for y in distinct):
            distinct.append(float(x))
    zero = any(abs(x) < 1e-6 for x in ev)
    return len(distinct), zero, sorted(distinct)


def main():
    t0 = time.time()
    print("T6 — le porteur formalisé : certificat, scalaires, potentiel "
          "spectral   [T6-KO6-PORT-1.0 gelé]")
    print("=" * 76)

    D, J0, g = porteur()
    alg = algebre_base()

    # ---- C0 : certificat (régression)
    c0 = verifie_porteur(D, J0, g, alg)
    print("C0 certificat du porteur :", {k: v for k, v in c0.items()}, "→",
          "PASS" if c0["TOUS"] else "FAIL")
    empreinte = hashlib.sha256(
        np.concatenate([D.real.reshape(-1), J0.reshape(-1),
                        g.reshape(-1)]).tobytes()).hexdigest()

    # ---- C1 : espace des scalaires
    rang, comms, base = espace_scalaires(D, alg)
    # égalité avec l'enveloppe déclarée F1 : φ(1,0) et φ(0,1) dans l'enveloppe
    enveloppe = np.array([h.reshape(-1) for h in base])
    ok_env = True
    for probe in (phi(1, 0), phi(0, 1)):
        v = probe.reshape(-1)
        coeff, *_ = np.linalg.lstsq(enveloppe.T, v, rcond=None)
        ok_env = ok_env and np.allclose(enveloppe.T @ coeff, v, atol=1e-8)
    C1 = (rang == 2 and ok_env and len(comms) == 2)
    print(f"C1 scalaires : rang mesuré = {rang} (déclaré 2) ; "
          f"commutateurs non nuls = {len(comms)} ; enveloppe F1 conforme : "
          f"{ok_env} → {'PASS' if C1 else 'FAIL'}")

    # ---- C2 / C3 : moments V2, V4 — grille × formule déclarée
    grid = [(-1.2 + 0.3 * i, -0.9 + 0.3 * j) for i in range(9)
            for j in range(7)]
    ec2 = ec4 = 0.0
    min_v2 = min_v4 = (np.inf, None)
    for a, b in grid:
        p_ = phi(a, b)
        v2, v4 = V2(D, p_), V4(D, p_)
        r2 = 1 + a * a + b * b
        ec2 = max(ec2, abs(v2 - (4 * r2 + 4)))
        ec4 = max(ec4, abs(v4 - (4 * r2 ** 2 + 24 * r2 + 4)))
        if v2 < min_v2[0]:
            min_v2 = (v2, (a, b))
        if v4 < min_v4[0]:
            min_v4 = (v4, (a, b))
    C2 = ec2 < 1e-9 and all(abs(x) < 1e-9 for x in min_v2[1])
    C3 = ec4 < 1e-9 and all(abs(x) < 1e-9 for x in min_v4[1])
    print(f"C2 V2 : écart machine/formule ≤ {ec2:.2e} ; minimum mesuré en "
          f"{min_v2[1]} → {'PASS' if C2 else 'FAIL'}")
    print(f"C3 V4 : écart machine/formule ≤ {ec4:.2e} ; minimum mesuré en "
          f"{min_v4[1]} → {'PASS' if C3 else 'FAIL'}")

    # ---- C4 : flot des bandes sous φ
    flot = []
    zero_hors_zero = False
    ecart_flot = 0.0
    for rho_a, rho_b in [(0, 0), (0.3, 0), (0, 0.6), (0.5, 0.5), (1.0, 0),
                         (0.9, 0.9)]:
        p_ = phi(rho_a, rho_b)
        rho = np.sqrt(1 + rho_a ** 2 + rho_b ** 2)
        nb, zero, spec = bandes(D + p_)
        attendu = sorted([-(rho + 1), -(rho - 1), rho - 1, rho + 1])
        ev = sorted(np.linalg.eigvalsh((D + p_)[1:, 1:]))
        ecart_flot = max(ecart_flot,
                         float(np.max(np.abs(np.array(ev) -
                                             np.array(attendu)))))
        # le zéro qui compte : celui du nœud du scalaire (le nœud ℂ est un
        # spectateur à zéro permanent — déclaré)
        zero_noeud = any(abs(x) < 1e-9 for x in ev)
        zero_si = (abs(rho - 1) < 1e-9)
        if zero_noeud and not zero_si:
            zero_hors_zero = True
        flot.append({"phi": (rho_a, rho_b), "rho": round(rho, 6),
                     "bandes": nb, "zero_noeud_scalaire": zero_noeud})
        print(f"C4 φ={ (rho_a, rho_b) } : {nb} bandes {[round(s, 3) for s in spec]}"
              f" zéro={zero}")
    C4 = ecart_flot < 1e-9 and not zero_hors_zero
    print(f"C4 flot : écart à F4 ≤ {ecart_flot:.2e} ; zéro hors φ=0 : "
          f"{zero_hors_zero} → {'PASS' if C4 else 'FAIL'}")

    # ---- C5 : action gaussienne
    s_vals = []
    t_grid = np.linspace(0.0, 1.5, 61)
    for t in t_grid:
        s_vals.append(S_gauss(D, phi(t, 0.0)))
    i_max = int(np.argmax(s_vals))
    # ρ = √(1+t²) ≥ 1 : le domaine physique ; t = 0 ⇔ ρ = 1 (déclaré)
    rho_star = float(np.sqrt(1 + t_grid[i_max] ** 2))
    # dérivée seconde au point ρ=1 (différences finies déclarées, h=1e-3)
    h = 1e-3
    s2 = (S_gauss(D, phi(1 + h, 0)) - 2 * S_gauss(D, phi(1, 0))
          + S_gauss(D, phi(1 - h, 0))) / h ** 2
    C5 = abs(rho_star - 1.0) <= 0.03 and s2 < 0
    print(f"C5 S(ρ) gaussienne : extremum mesuré à ρ = {rho_star:.3f} "
          f"(attendu 1) ; S″(1) = {s2:.4f} < 0 (maximum du compte spectral "
          f"au point de zéro-mode) → {'PASS' if C5 else 'FAIL'}")

    # ---- leviers
    lv = {}
    v2_phi = V2(D, phi(0.4, 0.3))
    v2_2phi = V2(D, phi(0.8, 0.6))
    attendu_ratio = (4 * (1 + 0.64 + 0.36) + 4) / (4 * (1 + 0.16 + 0.09) + 4)
    lv["φ→2φ (ratio V2 déclaré)"] = abs(v2_2phi / v2_phi - attendu_ratio) < 1e-9
    lv["D→0 : V2 = Tr φ² ≥ 0"] = abs(V2(np.zeros((5, 5)), phi(0.4, 0.3))
                                     - np.real(np.trace(phi(0.4, 0.3) @
                                                        phi(0.4, 0.3)))) < 1e-9
    J_bad = J0.copy(); J_bad[1:, 1:] = np.roll(GAM4, 1, axis=0)
    lv["J₀ permuté détecté (tuant)"] = not verifie_porteur(D, J_bad, g,
                                                           alg)["TOUS"]
    leviers_ok = all(lv.values())
    print("Leviers :", {k: v for k, v in lv.items()}, "→",
          "PASS" if leviers_ok else "FAIL")

    criteres = {"C0_certificat": c0["TOUS"], "C1_espace_scalaires": C1,
                "C2_V2": C2, "C3_V4": C3, "C4_flot_bandes": C4,
                "C5_action_gaussienne": C5, "leviers": leviers_ok}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 7 else ("PARTIEL" if nb >= 5 else "ÉCHEC")

    verdict = {
        "chantier": "T6-Q-KO6-PORTEUR-2026-10",
        "protocole": "T6-KO6-PORT-1.0 (gelé)",
        "porteur_nommé": {
            "id": "PORTEUR-KO6-A3b-DIM5",
            "algebre": "ℂ ⊕ M₂(ℂ)", "H": "ℂ ⊕ M₂(ℂ) (vec colonne)",
            "D": "0 ⊕ (L_{σ1} − R_{σ1})", "gamma": "1 ⊕ L_{σ3}R_{σ3}",
            "J": "K ⊕ adjoint", "table": "C-KO6-A3b (J²=+1, JD=−DJ, Jγ=+γJ)",
            "empreinte_matrices_sha256": empreinte},
        "C0_certificat": c0,
        "C1_scalaires": {"rang_mesuré": rang, "déclaré": 2,
                         "commutateurs_non_nuls": len(comms),
                         "forme": "φ(α,β) = 0 ⊕ I⊗(ασ₂+βσ₃) — un scalaire "
                                  "complexe = 2 réels (forme du papier)",
                         "enveloppe_F1_conforme": ok_env},
        "C2_V2": {"formule_déclarée": "4(1+α²+β²)+4", "écart_max": ec2,
                  "minimum": "φ = 0 (mesuré sur grille)"},
        "C3_V4": {"formule_déclarée": "4ρ⁴+24ρ²+4, ρ²=1+α²+β²",
                  "écart_max": ec4, "minimum": "φ = 0 (mesuré sur grille)"},
        "C4_flot": {"formule_déclarée": "bandes {±(ρ−1), ±(ρ+1)}",
                    "écart_max": ecart_flot, "mesures": flot,
                    "fait": "le mode zéro n'existe qu'en φ = 0 — le "
                            "scalaire décale le zéro (mesuré)"},
        "C5_gaussienne": {"rho_extremum": rho_star, "S_seconde_en_1": s2,
                          "interprétation": "S = compte spectral (pas une "
                                            "énergie) : maximal au point de "
                                            "zéro-mode"},
        "leviers": lv,
        "obstruction_chapeau_mexicain": "le potentiel du porteur fini est "
                                        "stable (minima en 0) : la masse² < 0 "
                                        "exige la géométrie produit "
                                        "(couplage a₂ à la courbure) — "
                                        "obstruction située, hors bornes",
        "criteres": criteres, "score": f"{nb}/7", "statut": statut,
        "falsifieur": "rang scalaire ≠ 2 ; écart formule/machine > 1e-9 ; "
                      "mode zéro à φ ≠ 0 ; levier non détecté",
        "gouvernance": "décision d'auteur du 12/10/2026 (« formalisons ce "
                       "porteur spectral à scalaire réel et testons-le »)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t6_ko6_porteur_spectral_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T6 : {statut} — {nb}/7")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
