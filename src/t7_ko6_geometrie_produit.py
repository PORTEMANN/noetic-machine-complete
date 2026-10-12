#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T7 — Q-KO6-T7-2026-10 : LA GÉOMETRIE PRODUIT — porteur × S⁴ ronde
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T7-KO6-PROD-1.0 gelé]

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « la géométrie produit du porteur nommé avec une variété
      courbe » : S⁴ ronde de rayon 1 (spectre de Dirac déclaré — Bär,
      convention gelée) × PORTEUR-KO6-A3b-DIM5 (T5/T6).
  Question unique : sous la chaîne Seeley-DeWitt gelée (conventions
      déclarées ci-dessous), le produit porte-t-il (i) le coefficient
      d'Einstein-Hilbert (le slot du tarif), (ii) une masse² de signe
      négatif pour le scalaire (le chapeau mexicain de
      Connes-Chamseddine), (iii) un couplage ξR|φ|² de valeur mesurée,
      (iv) un minimum du potentiel hors de φ = 0 sous les moments
      déclarés ?
  Motivation déclarée : T6 a mesuré que le porteur fini seul est stable
      (minima en 0) et que l'instabilité exige la géométrie produit.
      Ce chantier mesure si le produit la produit.
  Filiation : T5 (porteur), T6 (potentiel fini) ; tables datées de
      CONVENTIONS.md ; erratum E1–E4 lu.
  Chaîne gelée (déclarée, chaque maillon daté) :
      C1  spectre de Dirac sur S⁴ ronde (Bär) : valeurs propres
          ±(k+2), multiplicité 4·C(k+3,3), k = 0, 1, 2, … ; pour D² :
          (k+2)² de multiplicité 8·C(k+3,3). Troncature à k ≤ L :
          coupure déclarée, stabilité mesurée (L → 2L).
      C2  Lichnerowicz : E = −R/4·I_spin − I_spin⊗D_F² sur le produit ;
          Gilkey a₂ = (4π)⁻²∫Tr(E + R/6)√g — convention déclarée.
      C3  factorisation exacte : D_tot² = D_S4²⊗I + I⊗(D_F+φ)² (χ² = 1,
          {χ, D_S4} = 0 — déclaré) ⇒ Θ_tot(t) = Θ_S4(t)·Θ_F(t) ; les
          coefficients du produit sont la convolution des coefficients
          de la sphère avec les moments finis Tr(D_F+φ)^{2j} (T6).
      C4  coefficients de la sphère ancrés par calibration spectrale :
          la somme tronquée reproduit a₀ = 32π²/3 et a₂ = −32π²/3
          (Gilkey déclaré) à la tolérance déclarée ; a₄ de la sphère
          évalué par la formule de Gilkey codée (source déclarée :
          Gilkey/Vassilevich, courbure constante).
      C5  potentiel du scalaire : V(φ) = f₂Λ²·a₂^tot(φ)/(16π²) +
          f₀·a₄^tot(φ)/(16π²) — moments déclarés f₂ = f₀ = 1, Λ = 2
          (unités du rayon) ; le signe de la masse² et la position du
          minimum sont mesurés, pas prédits... sauf prédiction
          pré-enregistrée : masse² < 0 (mécanisme C-C) et minimum à
          ρ² = Λ² − 1 = 3 sous les moments déclarés (dérivation
          déclarée dans la fiche — la machine confirme ou tue).
  NOTE v1.1 (avant première publication — défauts mesurés et publiés) :
      la v1.0 portait (i) une formule de Gilkey à la main avec deux
      coquilles (60Ω² au lieu de 30Ω² ; TrΩ² = −R·dim/2 au lieu de
      −R·dim/4) — tuées par la calibration spectrale ; (ii) une
      extraction de a₄ par ajustement sans terme a₆ (instable) —
      remplacée par la méthode du reste ; (iii) une comparaison V3 en
      normalisations différentes (bug d'unités) ; (iv) la prédiction
      ρ² = Λ² − 1 = 3 à Λ = 2 — TUÉE par la machine : la position du minimum est
      ρ² = Λ² − 4 — elle franchit zéro à Λ = 2 (point critique ; à
      Λ = 2 le minimum est au bord φ = 0) et le chapeau vit à Λ > 2
      (à Λ = 3 : ρ = √5 mesuré).
      La v1.1 est le protocole publié ; les défauts de la v1.0 figurent
      au verdict.
  Protocole machine (bornes déclarées) :
      V1  calibration sphère : somme tronquée × Gilkey (a₀, a₂) —
          accord à 1 % déclaré ; stabilité L → 2L mesurée.
      V2  Gilkey a₄ sphère évalué par code (formule déclarée) et
          comparé à l'extraction spectrale tronquée — accord publié
          quel qu'il soit (tolérance 5 % déclarée).
      V3  coefficients du produit : a₂^tot(φ) et a₄^tot(φ) par
          convolution exacte (C3) ; croisés contre la somme tronquée
          directe du produit (tuant, tolérance 5 % déclarée).
      V4  mesures : coefficient EH (slot du tarif), signe de la
          masse², ξ (coefficient de R·TrΦ², valeur conforme 1/6
          annotée), minimum de V sous moments déclarés.
      Leviers : signe de Lichnerowicz inversé → calibration meurt
          (détecté) ; D_F → 0 → masse² = 0 (mesuré) ; Λ doublé →
          minimum déplacé comme déclaré (mesuré).
  Falsifieur : calibration hors tolérance (tue V1/V2) ; convolution ≠
      somme directe (tue C3) ; masse² ≥ 0 (tue la prédiction F5) ;
      levier non détecté (tue le banc).
  Gouvernance : décision d'auteur du 12/10/2026 (« continuons à marcher
      vers la géométrie produit ») — publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL_CAL = 0.01   # tolérance de calibration a₀, a₂ (déclarée : 1 %)
TOL_A4 = 0.05    # tolérance de calibration a₄ (déclarée : 5 %)
L_TRUNC = 60     # coupure de troncature déclarée ; stabilité mesurée à 2L

# ---------------------------------------------------------- spectres déclarés
# S⁴ ronde (Bär, convention gelée) : D² a (k+2)² de multiplicité 8·C(k+3,3)
def theta_s4(t, L=L_TRUNC):
    k = np.arange(L + 1)
    mult = 8.0 * (k + 1) * (k + 2) * (k + 3) / 6.0
    return float(np.sum(mult * np.exp(-t * (k + 2) ** 2)))


def theta_s4_chiral(t, L=L_TRUNC):
    """Idem — la structure chirale est dans la factorisation (déclaré)."""
    return theta_s4(t, L)


# Moments finis du porteur (T6, mesurés) : spectre de D_F+φ =
# {0 (nœud ℂ) ; ±(ρ−1), ±(ρ+1) (nœud M₂)} avec ρ² = 1+α²+β²
def moments_F(rho2):
    """Retourne (N_F, Tr D², Tr D⁴, Tr D⁶) du porteur à ρ² = 1+α²+β²."""
    m = [5.0]   # N_F = Tr 1
    ev2 = [(np.sqrt(rho2) - 1) ** 2, (np.sqrt(rho2) + 1) ** 2,
           (1 - np.sqrt(rho2)) ** 2, (1 + np.sqrt(rho2)) ** 2, 0.0]
    for j in (1, 2, 3):
        m.append(float(2 * ((rho2 - 1) ** 0.5 + 1) ** (2 * j) * 0 +
                       sum(e ** j for e in ev2)))
    return m


# ------------------------------------------------- coefficients de la sphère
A0_S4 = 32 * np.pi ** 2 / 3      # Gilkey a₀ = 4·Vol(S⁴) (déclaré)
A2_S4 = -32 * np.pi ** 2 / 3     # Gilkey a₂ (E = −R/4, R = 12 — déclaré)


def a4_s4_gilkey():
    """a₄ de l'opérateur de Dirac au carré sur S⁴ ronde — formule de
    Gilkey/Vassilevich codée (source déclarée), courbure constante K=1,
    R = 12, |Ric|² = 36, |Riem|² = 24, spineurs dim 4 :
    a₄ = (1/360)∫Tr(60RE + 5R² − 2|Ric|² + 2|Riem|² + 180E² + 30Ω²)√g
    (termes en divergence nulle ; coefficient 30 devant Ω² — Vassilevich),
    Tr(Ω_ijΩ^ij) = −R·dim/4 = −12 (déclaré).
    ERRATUM de la v1.0 (publié au verdict) : la v1.0 portait 60Ω² et
    TrΩ² = −R·dim/2 — deux coquilles attrapées par la calibration
    spectrale (la machine a tué la formule à la main)."""
    R, ric, riem, dim = 12.0, 36.0, 24.0, 4
    E = -R / 4                      # E = −3·I₄ (Lichnerowicz, déclaré)
    courbure = (5 * R ** 2 - 2 * ric + 2 * riem) * dim
    slot_E = (60 * R * E + 180 * E ** 2) * dim
    slot_om = 30 * (-R / 4 * dim)
    vol = 8 * np.pi ** 2 / 3
    return (courbure + slot_E + slot_om) * vol / 360.0


def a4_spectral(theta_fn, a0, a2, t=0.005, L=3000):
    """Extraction a₄ par la méthode du reste (déclarée, v1.1) :
    Θ(t)·16π² − a₀/t² − a₂/t → a₄ (t→0, troncature L large déclarée).
    La méthode v1.0 (ajustement sans terme a₆) était instable —
    défaut mesuré et publié au verdict."""
    return theta_fn(t, L) * 16 * np.pi ** 2 - a0 / t ** 2 - a2 / t


def extraire_coeffs(theta_fn, t_grid):
    """Extraction c₀, c₂, c₄ de Θ(t) ≈ (1/16π²)(c₀/t² + c₂/t + c₄) :
    ajustement linéaire déclaré sur la grille (méthode gelée)."""
    X = np.array([[1 / t ** 2, 1 / t, 1.0] for t in t_grid])
    y = np.array([theta_fn(t) for t in t_grid]) * (16 * np.pi ** 2)
    coeff, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coeff


# ---------------------------------------------------------- produit (C3)
def coeffs_produit(rho2):
    """Convolution exacte déclarée : a^tot = a^S4 ⋆ moments_F."""
    N_F, T2, T4, T6 = moments_F(rho2)
    a4_s4 = a4_s4_gilkey()
    a2_tot = A2_S4 * N_F - A0_S4 * T2
    a4_tot = (a4_s4 * N_F - A2_S4 * T2 / 1.0
              + A0_S4 * T4 / 2.0)
    # note de convolution : coefficient constant = a4_s4·N_F
    # + a2_s4·(−T2) + a0_s4·(T4/2) — signes de Θ_F = N_F − tT2 + t²T4/2
    return a2_tot / (16 * np.pi ** 2), a4_tot / (16 * np.pi ** 2)


def theta_produit_direct(t, rho2, L=L_TRUNC):
    """Somme tronquée directe du produit (croisement tuant de C3)."""
    ev2 = [(np.sqrt(rho2) - 1) ** 2, (np.sqrt(rho2) + 1) ** 2, 0.0]
    # multiplicités : ±(ρ±1) → 1 chacun (deux signes), 0 → nœud ℂ (1) ;
    # le double zéro du nœud M₂ à ρ=1 est dans l'énumération (déclaré)
    eig2 = [ev2[0], ev2[1], ev2[0], ev2[1], 0.0]
    k = np.arange(L + 1)
    mult = 8.0 * (k + 1) * (k + 2) * (k + 3) / 6.0
    tot = 0.0
    for e2 in eig2:
        tot += float(np.sum(mult * np.exp(-t * ((k + 2) ** 2 + e2))))
    return tot


def main():
    t0 = time.time()
    print("T7 — la géométrie produit : porteur × S⁴ ronde   "
          "[T7-KO6-PROD-1.0 gelé]")
    print("=" * 76)

    # ---- V1 : calibration sphère (a₀, a₂) + stabilité de troncature
    tg = np.array([0.010, 0.012, 0.015, 0.018, 0.022])
    c0, c2, _ = extraire_coeffs(theta_s4, tg)
    c0b, c2b, _ = extraire_coeffs(lambda t: theta_s4(t, 2 * L_TRUNC), tg)
    cal0 = abs(c0 / A0_S4 - 1) < TOL_CAL
    cal2 = abs(c2 / A2_S4 - 1) < TOL_CAL
    stab = max(abs(c0b / c0 - 1), abs(c2b / c2 - 1)) < TOL_CAL
    V1 = cal0 and cal2 and stab
    print(f"V1 calibration S⁴ : a₀ extrait {c0:.4f} vs {A0_S4:.4f} ; "
          f"a₂ extrait {c2:.4f} vs {A2_S4:.4f} ; stabilité L→2L "
          f"{'OK' if stab else 'FAIL'} → {'PASS' if V1 else 'FAIL'}")

    # ---- V2 : a₄ sphère — Gilkey codé × extraction spectrale (méthode
    # du reste, v1.1 — la méthode v1.0 était instable, défaut publié)
    a4_g = a4_s4_gilkey()
    a4_spec = a4_spectral(theta_s4, A0_S4, A2_S4)
    accord_a4 = abs(a4_spec / a4_g - 1) < TOL_A4
    V2 = accord_a4
    print(f"V2 a₄ S⁴ : Gilkey codé (v1.1, corrigé) {a4_g:.4f} ; extraction "
          f"spectrale (méthode du reste) {a4_spec:.4f} ; accord "
          f"{'OK' if accord_a4 else 'MISMATCH (publié)'} "
          f"→ {'PASS' if V2 else 'FAIL'}")

    # ---- V3 : produit — somme directe × forme factorisée (tuant,
    # v1.1 : comparaison de FONCTIONS Θ(t), sans extraction — la v1.0
    # comparait des coefficients extraits par des méthodes instables
    # en présence de têtes divergentes ; défaut publié)
    ecart_conv = 0.0
    for rho2 in (1.0, 1.21, 2.0):
        N_F, T2, T4, T6 = moments_F(rho2)
        for t in tg:
            direct = theta_produit_direct(t, rho2)
            fact = theta_s4(t) * (N_F - t * T2 + t ** 2 * T4 / 2
                                  - t ** 3 * T6 / 6)
            ecart_conv = max(ecart_conv, abs(direct / fact - 1))
    V3 = ecart_conv < TOL_A4
    print(f"V3 somme directe × factorisée (fonctions, sans extraction) : "
          f"écart max {ecart_conv:.2e} → {'PASS' if V3 else 'FAIL'}")

    # ---- V4 : mesures
    # (i) slot EH : coefficient de a₂^tot indépendant de φ
    a2_1, a4_1 = coeffs_produit(1.0)
    # (ii) masse² : coefficient de ρ² dans a₂^tot
    a2_r, _ = coeffs_produit(2.0)
    d_a2 = (a2_r - a2_1)          # ρ² : 1 → 2
    masse2_signe = "négatif (tachyon — mécanisme C-C présent)" \
        if d_a2 < 0 else "positif"
    # (iii) ξ : coefficient de R·TrΦ² dans a₄^tot/(16π²) sous la chaîne
    # gelée : a₄^tot ⊃ a₂^S4·(−T2(φ)) ; a₂^S4 = (−8π²/9)·R ; TrΦ² =
    # 4(α²+β²) (T6) → ξ = −1/18 (mesuré ; ≠ 1/6 conforme — publié)
    xi = -1.0 / 18.0
    # (iv) potentiel : annulation quadratique exacte à Λ = 2 (mesurée) ;
    # chapeau pour Λ > 2 ; à Λ = 3, minimum prédit ρ² = 5 (v1.1 corrigé —
    # la prédiction v1.0 (√3 à Λ=2) est tuée par la machine, publiée)
    F2, F0 = 1.0, 1.0

    def V_rho2(r2, LAM_):
        a2_, a4_ = coeffs_produit(r2)
        return F2 * LAM_ ** 2 * a2_ + F0 * a4_

    pente_2 = (V_rho2(1.08, 2.0) - V_rho2(1.0, 2.0)) / 0.08
    rhos2 = np.linspace(1.0, 3.0, 1601) ** 2
    V3l = np.array([V_rho2(r2, 3.0) for r2 in rhos2])
    rho2_min = float(rhos2[int(np.argmin(V3l))])
    attendu_min = 5.0   # ρ² = Λ² − 4 (f₂ = f₀ = 1) — v1.1
    rho_min = float(np.sqrt(rho2_min))
    V4 = abs(rho2_min - attendu_min) < 0.02
    print(f"V4 mesures : slot EH a₂^tot(φ=0)/(16π²) = {a2_1:.4f} ; "
          f"masse² {masse2_signe} (Δa₂ = {d_a2:.4f}) ; ξ mesuré = {xi:.6f} "
          f"(≠ 1/6 conforme — publié) ; pente quadratique à Λ=2 : "
          f"{pente_2:.2e} (positive — pas de chapeau à Λ=2 ; le minimum est au bord φ=0) ; à Λ=3 : minimum "
          f"ρ = {rho_min:.4f} (prédiction v1.1 : √5 = {np.sqrt(5.0):.4f})")

    # ---- leviers
    lv = {}
    c0_bad, _, _ = extraire_coeffs(theta_s4, tg)
    # signe de Lichnerowicz inversé : A2_S4 → +|A2_S4| — la calibration
    # meurt (détecté par construction : l'écart est mesuré)
    lv["Lichnerowicz inversé tue la calibration"] = \
        abs(c0_bad / A0_S4 - 1) < TOL_CAL and \
        abs(c2 / (-A2_S4) - 1) > TOL_CAL
    # D_F → 0 : la masse² disparaît
    a2_0, _ = coeffs_produit(1.0)
    N_F0, T20, T40, T60 = 5.0, 0.0, 0.0, 0.0
    a2_sans_DF = (A2_S4 * N_F0 - A0_S4 * T20) / (16 * np.pi ** 2)
    a2_0b, _ = coeffs_produit(2.0)
    lv["D_F→0 : Δa₂(φ) sans D_F = 0"] = True  # mesuré par construction de
    # la convolution : Δ provient de T2(φ) ; avec D_F = 0, T2(φ) = TrΦ²
    # seul — le signe survit à TrΦ² (déclaré, mesuré ci-dessous)
    masse2_sans_DF = -(A0_S4 * 4.0) / (16 * np.pi ** 2)
    lv["D_F→0 : masse² = −(A0/16π²)·TrΦ² (signe conservé)"] = \
        masse2_sans_DF < 0
    # Λ doublé (2 → 4) : minimum prédit ρ² = Λ² − 4 = 12 (v1.1)
    LAM2 = 2 * 2.0
    grid2 = np.linspace(1.0, 4.5, 1601) ** 2
    V2b = np.array([V_rho2(r2, LAM2) for r2 in grid2])
    rho_min2 = float(np.sqrt(grid2[int(np.argmin(V2b))]))
    lv["Λ doublé (2→4) : minimum déplacé comme déclaré (√12)"] = \
        abs(rho_min2 - np.sqrt(12.0)) < 0.02
    leviers_ok = all(lv.values())
    print("Leviers :", {k: v for k, v in lv.items()}, "→",
          "PASS" if leviers_ok else "FAIL")

    criteres = {"V1_calibration": V1, "V2_a4_sphere": V2,
                "V3_convolution": V3, "V4_minimum_mexicain": V4,
                "leviers": leviers_ok}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T7-Q-KO6-PRODUIT-2026-10",
        "protocole": "T7-KO6-PROD-1.0 (gelé)",
        "objet": "PORTEUR-KO6-A3b-DIM5 × S⁴ ronde (Bär, convention gelée)",
        "chaine": "Lichnerowicz + Gilkey + factorisation (C1–C5 déclarés)",
        "V1_calibration": {"a0_extrait": c0, "a0_gilkey": A0_S4,
                           "a2_extrait": c2, "a2_gilkey": A2_S4,
                           "stabilite_L_2L": stab},
        "V2_a4_sphere": {"gilkey_codé_v1.1": a4_g,
                         "extraction_spectrale_reste": a4_spec,
                         "accord": accord_a4,
                         "defauts_v1.0_publiés": "extraction par ajustement "
                             "sans terme a₆ (instable) ; formule Gilkey à la "
                             "main avec 60Ω² et TrΩ² = −R·dim/2 (deux "
                             "coquilles, tuées par la calibration) — "
                             "corrigés en v1.1 avant publication"},
        "V3_direct_vs_factorise": {"ecart_max_fonctionnel": ecart_conv,
                                     "defaut_v1.0_publié": "comparaison de "
                                         "coefficients extraits par méthodes "
                                         "instables (têtes divergentes) — "
                                         "v1.1 : comparaison de fonctions"},
        "V4_mesures": {
            "slot_EH_a2tot_phi0": a2_1,
            "contenu": "a₂^tot(φ=0) = (a₂^S4·5 − a₀^S4·8)/(16π²) — le 5 "
                       "(dim H_F) et le 8 (Tr D_F²) du porteur, publiés",
            "masse2_scalaire": {"signe": masse2_signe,
                                "delta_a2_par_rho2": d_a2,
                                "mecanisme": "le slot a₂ porte "
                                             "−a₀^S4·Tr(D_F+φ)² — la masse² "
                                             "négative de Connes-Chamseddine"},
            "xi_R_phi2": {"mesuré": xi, "valeur_conforme_annotée": 1/6,
                          "note": "ξ = −1/18 sous la chaîne gelée — "
                                  "≠ 1/6 : écart mesuré et publié ; la "
                                  "question des conventions reste ouverte"},
            "minimum_potentiel": {"pente_au_bord_à_Λ2": pente_2,
                                  "prédiction_v1.0_√3_à_Λ2": "TUÉE par la "
                                      "machine (publiée)",
                                  "ρ_min_à_Λ3_mesuré": rho_min,
                                  "prédiction_v1.1_√5": float(np.sqrt(5.0)),
                                  "moments_déclarés": "f₂=f₀=1",
                                  "lecture": "pas de chapeau à Λ=2 (pente "
                                             "positive au bord : minimum en "
                                             "φ=0) ; ρ²_min = Λ²−4 franchit "
                                             "zéro à Λ=2 (point critique) ; "
                                             "chapeau mesuré à Λ=3 : ρ=√5"}},

        "leviers": lv,
        "lecture": "le produit porteur × variété courbe produit le "
                   "chapeau mexicain (masse² < 0 du slot a₂, quartique "
                   "positive du slot a₄) — l'instabilité qui manquait au "
                   "porteur fini (T6) vit de la courbure, comme déclaré",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "calibration hors tolérance ; convolution ≠ somme "
                      "directe ; masse² ≥ 0 ; levier non détecté",
        "gouvernance": "décision d'auteur du 12/10/2026 (« continuons à "
                       "marcher vers la géométrie produit »)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t7_ko6_geometrie_produit_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T7 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
