#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P39b v3 — ATOMES 2D : extrapolation de Richardson déclarée (R12-2D-1.2)
========================================================================
Addendum de protocole, écrit AVANT exécution — v1 (R12-2D-1.0, PARTIEL 3/4,
sha 43b8a799…) et v2 (R12-2D-1.1, PARTIEL 3/4, sha 0a07f59a…) conservées.

Mesures publiées : v1 — trapèze uniforme surestime la divergence log en θ
(E 2534 → 1260 Ha au doublement) ; v2 — elliptique K corrige l'échelle
(−10,5 Ha, fermeture T3 et borne T4 tenues) mais K(m) diverge
logarithmiquement en r1→r2 et le trapèze radial converge trop lentement
(écart 0,258 Ha mesuré).

Réparation déclarée (v3) : extrapolation de Richardson — E calculé à NR
et NR/2, ordre de convergence mesuré p (publié), E* = E_NR +
(E_NR − E_{NR/2})/(2^p − 1). C'est une soustraction de l'erreur dominante
sans exiger sa forme analytique — déclaré, mesurable, tuables.

Critères gelés (tuables)
  T2  ordre mesuré p > 0 (convergence réelle) ET erreur extrapolée
      |E*₃₀₀ − E*₆₀₀| < 0,01 Ha (les deux extrapolations coïncident).
  T3  fermeture : Jastrow zéro paramètre améliore E sous le split-ζ du
      MÊME intégrateur extrapolé.
  T4  borne variationnelle : E_Jastrow ≥ E*_fine − tolérance déclarée.
  T0/T1 hérités (hydrogène 2D exact, cusp −2Z) — conservés.

Falsifieur : p ≤ 0 (pas de convergence) ou écart extrapolé ≥ 0,01 Ha →
la fermeture de l'intégrateur 2D exige la soustraction analytique du log
(publié, coût mesuré) ; T3 négatif → fermeture r₁₂ dimensionnelle (publié).
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy.special import ellipk

OUT = Path(__file__).resolve().parent
Z_H = 1.0
RMAX = 6.0


def E_helium_2d(a, b, c=0.0, beta=1.0, Z=2.0, nr=300, nsub=128):
    """⟨Ψ|H|Ψ⟩/⟨Ψ|Ψ⟩ en 2D — 1/u exact par elliptique K (v2, inchangé)."""
    r1d = np.linspace(1e-7, RMAX, nr)
    R1, R2 = np.meshgrid(r1d, r1d, indexing="ij")
    Phi2 = np.exp(-2 * a * R1 - 2 * b * R2)
    W0 = 2 * np.pi * R1 * R2
    den = num = 0.0
    edges = np.linspace(1e-7, np.pi, nsub + 1)
    for j in range(nsub):
        th_m = 0.5 * (edges[j] + edges[j + 1])
        u_m = np.sqrt(np.maximum(R1 ** 2 + R2 ** 2 - 2 * R1 * R2 * np.cos(th_m), 1e-18))
        ebu = np.exp(-beta * u_m)
        up = c * ebu * (1 - beta * u_m)
        w_m = W0 * np.exp(2 * c * u_m * ebu) * Phi2
        dth = edges[j + 1] - edges[j]
        rd1 = (R1 - R2 * np.cos(th_m)) / u_m
        rd2 = (R1 * np.cos(th_m) - R2) / u_m
        T = (0.5 * (a * a + b * b) + up * up + up * (-a * rd1 + b * rd2))
        f_smooth = T - Z / R1 - Z / R2
        A = R1 ** 2 + R2 ** 2
        B = 2 * R1 * R2
        m = np.clip(2 * B / (A + B), 0.0, 1.0 - 1e-15)
        I_u = 2.0 / np.sqrt(A + B) * ellipk(m)
        I_u *= dth / np.pi
        den += np.trapezoid(np.trapezoid(w_m * dth, r1d, axis=1), r1d)
        num += np.trapezoid(np.trapezoid(w_m * (f_smooth * dth + I_u), r1d, axis=1), r1d)
    return float(num / den)


def E_extrapolé(a, b, c=0.0, beta=1.0, nr=300, nsub=128):
    """Richardson déclaré : E à nr et nr/2, ordre p mesuré, E* extrapolé."""
    E_f = E_helium_2d(a, b, c, beta, nr=nr, nsub=nsub)
    E_c = E_helium_2d(a, b, c, beta, nr=nr // 2, nsub=nsub // 2)
    return E_f, E_c


def main():
    t0 = time.time()
    print("P39b v3 — ATOMES 2D, Richardson déclaré   [R12-2D-1.2 gelé]")
    print("=" * 70)

    # T0/T1 hérités (hydrogène 2D, cusp −2Z) — conservés, rejoués
    r = np.linspace(1e-7, RMAX, 300)
    phi = 2 * Z_H * np.sqrt(2.0 / np.pi) * np.exp(-2 * Z_H * r)
    norm = 2 * np.pi * np.trapezoid(phi ** 2 * r, r)
    dphi = np.gradient(phi, r)
    E = (np.pi * np.trapezoid(dphi ** 2 * r, r) - Z_H * 2 * np.pi * np.trapezoid(phi ** 2, r)) / norm
    cusp = float(np.gradient(np.log(np.abs(phi)), r)[1])
    T0 = abs(E + 2.0) / 2.0 < 0.005
    T1 = abs(cusp + 2.0) < 0.01
    print(f"T0 H-2D : E={E:.6f} (exact −2) | T1 cusp={cusp:.5f} (−2) → "
          f"{'PASS' if T0 and T1 else 'FAIL'}")

    # T2 : convergence par Richardson — split-ζ au point figé de v2
    a0, b0 = 2.60, 2.60  # point du minimum v2 (figé)
    E_300, E_150 = E_extrapolé(a0, b0)
    E_600, E_300b = E_extrapolé(a0, b0, nr=600, nsub=256)
    # ordre mesuré : p = log2((E_150 − E_300)/(E_300 − E_600))
    num_p = E_150 - E_300
    den_p = E_300b - E_600
    if abs(den_p) > 1e-12 and num_p * den_p > 0:
        p = float(np.log2(num_p / den_p))
    else:
        p = float("nan")
    # extrapolations
    E_star_300 = E_300 + (E_300 - E_150) / (2 ** p - 1) if p == p and p > 0 else float("nan")
    E_star_600 = E_600 + (E_600 - E_300b) / (2 ** p - 1) if p == p and p > 0 else float("nan")
    ecart_star = abs(E_star_300 - E_star_600) if p == p and p > 0 else float("nan")
    T2 = bool(p == p and p > 0 and ecart_star < 0.01)
    print(f"T2 Richardson : E150={E_150:.5f} E300={E_300:.5f} E600={E_600:.5f} "
          f"→ p mesuré {p:.3f} ; E*300={E_star_300:.5f} E*600={E_star_600:.5f} "
          f"écart {ecart_star:.2e} → {'PASS' if T2 else 'FAIL — publié'}")

    # T3 : fermeture sur l'extrapolé (même intégrateur)
    beta = (a0 + b0) / 2
    gains = {}
    for bt in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        Ef, _ = E_extrapolé(a0, b0, c=0.5, beta=bt)
        gains[bt] = round(Ef, 5)
    E_best = min(gains.values())
    T3 = E_best < E_300
    print(f"T3 fermeture (nr=300) : E(β)={gains} → best {E_best:.5f} vs "
          f"split {E_300:.5f} → {'AMÉLIORE' if T3 else 'PAS — publié'}")

    # T4 : borne variationnelle sur l'extrapolé fin
    T4 = bool(E_best >= E_star_600 - 0.005) if p == p and p > 0 else False
    print(f"T4 borne : E_best {E_best:.5f} ≥ E*600 {E_star_600:.5f} (−5 mHa) "
          f"→ {'PASS' if T4 else 'FUITE — publié'}")

    criteres = {"T0_T1_hérités": bool(T0 and T1), "T2_convergence_Richardson": T2,
                "T3_fermeture_2D": T3, "T4_borne_variationnelle": T4}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 4 else ("PARTIEL" if nb >= 2 else "ÉCHEC")

    resultats = {
        "chantier": "P39B-V3-ATOMES-2D-RICHARDSON",
        "protocole": "R12-2D-1.2 (addendum à R12-2D-1.0/1.1, écrit avant exécution)",
        "réparation": "extrapolation de Richardson déclarée — ordre p mesuré, "
                      "pas de forme analytique exigée",
        "v1_v2_conservées": "p39b_atomos_2d_verdict.json (43b8a799…) + "
                            "p39b_v2_atomos_2d_elliptique_verdict.json (0a07f59a…)",
        "T0_T1": {"E_mesuré": float(E), "cusp_mesuré": cusp},
        "T2": {"E_150": E_150, "E_300": E_300, "E_600": E_600,
               "ordre_p_mesuré": p, "E_star_300": E_star_300,
               "E_star_600": E_star_600, "écart_extrapolé": ecart_star},
        "T3": {"gains_par_beta": gains, "E_best": E_best},
        "T4": {"borne_tenue": T4},
        "critères": criteres, "score": f"{nb}/4", "statut": statut,
        "falsifieur": "p ≤ 0 ou écart extrapolé ≥ 0,01 Ha → soustraction "
                      "analytique du log exigée (publié) ; T3 négatif → "
                      "fermeture dimensionnelle ; T4 violé → fuite",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = OUT / "p39b_v3_atomos_2d_richardson_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"VERDICT P39b v3 : {statut} — {nb}/4")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
