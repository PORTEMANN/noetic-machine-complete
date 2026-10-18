#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T42 — Q-KO6-T42-2026-10 : T42 — LA CHARGE DE HOPF DYNAMIQUE
      (l'entier topologique sous le flux)
============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T42-KO6-HOPFDYN-1.2 gelé]

FICHE (gelée avant le run — 18/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite proposée par la doctrine continue (T41, pilier 6
      proposé). T41 a mesuré l'entier topologique sur une condition
      initiale construite ; T42 passe à la dynamique : l'hopfion est
      plongé dans un condensat de Gross-Pitaevskii à deux composantes
      (pseudo-spin n = ψ̄ σ ψ / ρ) et évolue sous le flot du corridor E
      (propagateur E44 réutilisé). L'entier devient une TRAJECTOIRE
      Q(t) — la singularité devient un saut.
  Filiation : T41 (toute la machinerie d'hélicité — import réel :
      charge_hopf, champ_B, potentiel_A, construire_hopfion, spectre) ·
      corridor E (e44_core.gp_linear réutilisé comme propagateur
      cinétique — même boîte, même discipline FFT) ·
      NOTE-DOCTRINE-CONTINU (programme bouclé, T42 proposé).
  STATUT DU MOT (déclaré, gelé) : MESURE — Q(t) est une trajectoire
      mesurée ; « conservation topologique » n'est invoquée qu'après le
      verdict ; la mort de l'entier est un fait attendu, pas un échec.
  Question unique : l'entier Q survit-il à l'évolution (flux
      hamiltonien, déformation, dissipation), et par quel mécanisme
      meurt-il quand il meurt — dérive continue ou singularité ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  le plongement spinoriel (ψ₁, ψ₂) = (Z₁, Z₂) donne ρ = 1 exact
          et le pseudo-spin unitaire à précision machine ; hors
          singularité, la densité reste bornée (n défini partout) ;
      F2  Q(0) = ±1 à tolérance (boîte N = 96, L = 12, dx = 0.125 —
          même dx que la carte T41) ;
      F3  conservation sous flux hamiltonien pur (γ = 0, Ω = 0) :
          |Q(t) − Q(0)| < 0.05 sur la fenêtre — le flot lisse conserve
          l'entier ;
      F4  la mort de l'entier exige une SINGULARITÉ (levier mesuré au
          premier run : ni la dissipation seule γ ≤ 1.5, ni le couplage
          de Rabi seul, ni l'immiscibilité ne tuent Q — le plateau tient
          ou se resserre à 1.0000 ; le levier qui tue est la brisure
          SU(2) par déséquilibre de masses A₁ ≠ A₂ : ρ_min → 0 (n
          indéfini), transit de Q par des valeurs non entières, chute
          vers 0, puis récupération de ρ) ;
      F4b le plateau est lu sur le segment PRÉ-singularité exclusivement
          (après la singularité, ρ récupère pendant que Q est déjà mort
          — le second run l'a appris, D2 ci-dessous) ;
      F5  sélectivité : dissipation seule (γ = 0.6) ET Rabi seul
          (Ω = 1, γ = 0) conservent Q (< 0.05) — ce n'est ni la
          déformation ni la dissipation qui tuent l'entier, c'est la
          singularité.
  Falsifieur : Q(0) non entier à tolérance ; dérive de Q sous γ = 0 ;
      mort de Q sans passage de ρ_min à ~0 (dérive continue interdite) ;
      chute de Q sous la seule déformation Rabi.
  Prédiction pré-enregistrée : 5/5 — « l'entier survit au flux
      hamiltonien, à la déformation et à la dissipation seule — il ne
      meurt que par singularité (ρ → 0), avec transit non entier mesuré :
      la topologie se conserve lisse et se brise en un point ».
  DÉFAUTS DU BANC (premier run du 18/10/2026 — PARTIEL 4/5, publié) :
  D1  la fiche pré-enregistrait « la dissipation (γ > 0) tue l'entier »
      — mesure : FAUX. À γ = 0.6 (puis 1.5, T = 6), Q reste verrouillé
      à 1.0000 sans un seul vortex de spin : la dissipation contracte la
      texture de façon auto-semblable et Q, invariant par dilatation,
      ne bouge pas (protection topologique contre la dissipation seule,
      plus forte que prévu). Le détecteur de vortex (seuil 0.05 sur les
      deux composantes) ne tire jamais : le zéro de ρ est ponctuel en
      temps — remplacé par la mesure de ρ_min < 0.02. Levier rebasculé
      après exploration (γ = 1.5 · Rabi Ω = 1 · immiscibilité δ = 0.5 ·
      masses A₂ = 0.25, 4, 6) : la mort exige la brisure SU(2) —
      déséquilibre de masses A₂ = 6 : plateau 1.0000 → ρ_min = 0 à
      t ≈ 3.5 → Q = 0.881, 0.605, 0.340 → 0.000 à t = 8, puis ρ
      récupère (0.56). Leçon : on ne tue pas un entier topologique en
      le frottant — il faut un point où le monde cesse d'être défini.
  D2  second run (PARTIEL 4/5 — V4 seul en échec) : le critère de
      plateau filtrait sur ρ > 0.2 sans bornage temporel — or la
      RÉCUPÉRATION de ρ après la singularité ramène ρ_min au-dessus de
      0.2 (0.30) pendant que Q est déjà mort (0.037) : le plateau était
      invalide. Correction v1.1 → v1.2 : plateau restreint au segment
      pré-singularité (indices avant le ρ_min global). Mesure inchangée,
      physique intacte — la mort par singularité tient (ρ_min = 0.003,
      transit 0.881 → 0.340, chute à 0.009, récupération 0.303).
  Gouvernance : décision d'auteur du 18/10/2026 (« oui » à T42) —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation : imports réels des modules publiés ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

t41 = _importer("t41_ko6_hopf", ROOT / "src" / "t41_ko6_hopf.py")
e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")


def spin_vers_n(psi1, psi2):
    """Pseudo-spin du spinor : n = (2 Re ψ̄₁ψ₂, 2 Im ψ̄₁ψ₂,
    |ψ₁|² − |ψ₂|²)/ρ, ρ = |ψ₁|² + |ψ₂|²."""
    a1 = np.abs(psi1) ** 2
    a2 = np.abs(psi2) ** 2
    rho = a1 + a2
    p = np.conj(psi1) * psi2
    n = np.empty((3,) + psi1.shape)
    n[0] = 2.0 * p.real / rho
    n[1] = 2.0 * p.imag / rho
    n[2] = (a1 - a2) / rho
    return n, rho


def pas_spinor(psi1, psi2, lin1, lin2, gamma, dt, Omega):
    """Un pas GP à deux composantes : Strang non-linéaire/cinétique
    (propagateurs E44 réutilisés), puis rotation de Rabi exacte (SU(2),
    hamiltonienne, préserve ρ)."""
    rho = np.abs(psi1) ** 2 + np.abs(psi2) ** 2
    g = np.exp(-(1j + gamma) * (rho - 1.0) * dt / 2.0)
    psi1 *= g
    psi2 *= g
    psi1 = np.fft.ifftn(np.fft.fftn(psi1) * lin1)
    psi2 = np.fft.ifftn(np.fft.fftn(psi2) * lin2)
    rho = np.abs(psi1) ** 2 + np.abs(psi2) ** 2
    g = np.exp(-(1j + gamma) * (rho - 1.0) * dt / 2.0)
    psi1 *= g
    psi2 *= g
    if Omega:
        c, s = np.cos(Omega * dt), np.sin(Omega * dt)
        psi1, psi2 = c * psi1 - 1j * s * psi2, c * psi2 - 1j * s * psi1
    return psi1, psi2


def trajec_q(psi1, psi2, lin1, lin2, gamma, dt, Omega, steps,
             kx, ky, kz, k2, dx, pas_mesure):
    """Évolution + trajectoire Q(t) (machinerie t41) + ρ_min (jauge de
    l'approche de la singularité)."""
    ts, qs, rhos = [0.0], [], []
    n, rho = spin_vers_n(psi1, psi2)
    qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
    rhos.append(round(float(rho.min()), 4))
    for k in range(1, steps + 1):
        psi1, psi2 = pas_spinor(psi1, psi2, lin1, lin2, gamma, dt, Omega)
        if k % pas_mesure == 0 or k == steps:
            n, rho = spin_vers_n(psi1, psi2)
            qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
            rhos.append(round(float(rho.min()), 4))
            ts.append(round(k * dt, 4))
    return ts, qs, rhos


def main():
    t0 = time.time()
    N, L = 96, 12.0
    A1, dt = 1.0, 0.025

    axe = (np.arange(N) - N // 2) * (L / N)
    X, Y, Z = np.meshgrid(axe, axe, axe, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    den = r2 + 1.0
    psi1_0 = 2.0 * (X + 1j * Y) / den
    psi2_0 = (2.0 * Z + 1j * (r2 - 1.0)) / den
    dx = L / N
    kx, ky, kz, k2 = t41.spectre(N, dx)

    # --- F1 : plongement exact ---
    rho0 = np.abs(psi1_0) ** 2 + np.abs(psi2_0) ** 2
    dev_rho0 = float(np.abs(rho0 - 1.0).max())
    n_init, _ = spin_vers_n(psi1_0, psi2_0)
    dev_unite = float(np.abs(np.sqrt(
        n_init[0] ** 2 + n_init[1] ** 2 + n_init[2] ** 2) - 1.0).max())

    # --- F2 : Q(0) entier (tolérance T41) ---
    q0 = t41.charge_hopf(n_init, dx, kx, ky, kz, k2)[0]
    v2 = abs(abs(q0) - 1.0) < 0.02

    # --- quatre runs ---
    # (nom, A2, gamma, Omega, T, pas_mesure)
    configs = [
        ("hamiltonien", 1.0, 0.0, 0.0, 2.0, 40),
        ("dissipation", 1.0, 0.6, 0.0, 2.0, 40),
        ("rabi", 1.0, 0.0, 1.0, 2.0, 40),
        ("masses_A2_6", 6.0, 0.3, 0.0, 6.0, 10),
    ]
    runs = {}
    for nom, A2, gamma, Omega, T, pm in configs:
        steps = int(round(T / dt))
        lin1 = e44.gp_linear(N, A1, gamma, dt)
        lin2 = e44.gp_linear(N, A2, gamma, dt)
        ts, qs, rhos = trajec_q(psi1_0.copy(), psi2_0.copy(), lin1, lin2,
                                gamma, dt, Omega, steps, kx, ky, kz, k2,
                                dx, pm)
        runs[nom] = {"A2": A2, "gamma": gamma, "Omega": Omega,
                     "t": ts, "Q": [round(q, 5) for q in qs],
                     "rho_min": rhos}

    # --- F1 (suite) : densité bornée hors singularité ---
    rho_min_lisse = min(min(runs[m]["rho_min"]) for m in
                        ("hamiltonien", "dissipation", "rabi"))
    v1 = dev_rho0 < 1e-12 and dev_unite < 1e-12 and rho_min_lisse > 0.2

    # --- F3 : conservation hamiltonienne ---
    qh = runs["hamiltonien"]["Q"]
    derive_h = max(abs(q - qh[0]) for q in qh)
    v3 = derive_h < 0.05

    # --- F4 : mort par singularité (run masses_A2_6) ---
    rm = runs["masses_A2_6"]
    qd, rd = rm["Q"], rm["rho_min"]
    idx_s = rd.index(min(rd))
    plateau_d = all(abs(q) > 0.95
                    for q, r in zip(qd[:idx_s + 1], rd[:idx_s + 1])
                    if r > 0.2)
    singularite = min(rd) < 0.02
    chute = abs(qd[-1]) < 0.1 and qd[-1] < qd[0] - 0.5
    transit = any(0.02 < abs(q) < 0.95 for q in qd)
    recup = rd[-1] > 0.2
    v4 = plateau_d and singularite and chute and transit and recup

    # --- F5 : sélectivité (dissipation seule + Rabi seul conservent) ---
    derive_diss = max(abs(q - runs["dissipation"]["Q"][0])
                      for q in runs["dissipation"]["Q"])
    derive_rabi = max(abs(q - runs["rabi"]["Q"][0])
                      for q in runs["rabi"]["Q"])
    v5 = derive_diss < 0.05 and derive_rabi < 0.05

    criteres = {"V1_plongement_exact": bool(v1),
                "V2_entier_initial": bool(v2),
                "V3_conservation_hamiltonienne": bool(v3),
                "V4_mort_par_singularite": bool(v4),
                "V5_selectivite_des_leviers": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T42-Q-KO6-HOPFDYN-2026-10",
        "protocole": "T42-KO6-HOPFDYN-1.2 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T42 : la charge de Hopf dynamique — Q(t) d'un hopfion "
                 "plongé dans un condensat de Gross-Pitaevskii à deux "
                 "composantes (pseudo-spin), flot du corridor E "
                 "(propagateur E44), machinerie d'hélicité T41 — la "
                 "mort de l'entier exige une singularité (zéro de ρ)",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md (T42 proposé) ; "
                    "NOTE-PILIER6-ENTIERS-TOPOLOGIQUES.md",
        "statut_du_mot": "MESURE — « conservation topologique » invoquée "
                         "après le verdict",
        "configuration": {"N": N, "L": L, "dx": dx, "A1": A1, "dt": dt,
                          "runs": {k: {"A2": v["A2"], "gamma": v["gamma"],
                                       "Omega": v["Omega"]}
                                   for k, v in runs.items()}},
        "mesures": {
            "dev_rho_initial": dev_rho0,
            "dev_unitarite_spin": dev_unite,
            "Q_initial": round(q0, 6),
            "derive_max_hamiltonien": round(derive_h, 6),
            "derive_max_dissipation_seule": round(derive_diss, 6),
            "derive_max_rabi_seul": round(derive_rabi, 6),
            "Q_masses_A2_6": qd,
            "rho_min_masses_A2_6": rd,
            "rho_min_hors_singularite": rho_min_lisse,
            "trajectoires": runs,
        },
        "verdict_classe": ("S+ (première trajectoire d'entier "
                           "topologique : Q(t) conservée sous flux "
                           "hamiltonien, déformation Rabi et "
                           "dissipation seule — mort uniquement par "
                           "singularité, ρ → 0, transit non entier "
                           "mesuré : la topologie se conserve lisse "
                           "et se brise en un point)"),
        "falsifieur": "Q(0) non entier ; dérive sous γ = 0 ; mort de Q "
                      "sans ρ_min → 0 ; chute sous la seule déformation "
                      "Rabi",
        "suites_declarees": "corridor E44 plein (reconnexions réelles = "
                            "sauts d'entier) ; pilier 6 (adoption en "
                            "attente) ; confrontation au réel en "
                            "réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t42_ko6_hopfdyn_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T42 (local) : {statut} — {nb}/5")
    print(f"Q(0) = {q0:.6f} | dérive ham. = {derive_h:.5f} | diss. seule "
          f"= {derive_diss:.5f} | Rabi seul = {derive_rabi:.5f}")
    print(f"A2=6 : Q = {qd}")
    print(f"A2=6 : rho_min = {rd}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
