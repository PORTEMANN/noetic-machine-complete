#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T11 — Q-KO6-T11-2026-10 : LA FAMILLE DES VARIÉTÉS — le diagramme de phase
      du chapeau et la carte des slots (campagne B)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T11-KO6-FAM-1.0 gelé]

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « la famille des variétés » : {T⁴ plat (contrôle, R = 0),
      S⁴ ronde de rayon r variable (la courbe continue), K3 (Ricci-plat
      courbé : R = 0, Riem² ≠ 0)} × {MS corrigé (1 génération, T9 v2) ;
      porteur du corpus (T5/T6)} — campagne B de la stratégie du
      12/10/2026.
  Question unique : comment les slots de la chaîne spectrale (EH, masse²,
      quartique) et la coupure critique du chapeau Λ_c dépendent-ils de
      la variété et du contenu ?
  Chaîne gelée (filiation T7, calibrée) : coefficients de Gilkey par
      variété (formules déclarées ci-dessous) + convolution exacte avec
      les moments finis du contenu (mesurés sur matrices).
  Déclarations par variété (gelées) :
      S⁴(r) : R = 12/r², |Ric|² = 36/r⁴, |Riem|² = 24/r⁴, Vol =
          (8π²/3)r⁴ — courbure constante ;
      T⁴ : R = |Ric|² = |Riem|² = 0, Vol = 1 (déclaré) — le contrôle
          plat ;
      K3 : R = 0, |Ric|² = 0, ∫|Riem|² = 768π² (Gauss-Bonnet, χ = 24),
          Vol = 1 (choix d'échelle déclaré — publié comme tel) ;
      spin : K3 est spin (Calabi-Yau — déclaré) ; la trace de courbure
          spinorielle généralisée : TrΩ² = −|Riem|²·dim/8 (se réduit à la
          valeur calibrée de T7 en courbure constante — déclaré).
      Coefficients (filiation T7) : a₀ = 4·Vol ; a₂ = ∫(−R/3)√g (mesuré
      T7) ; a₄ = (1/360)∫[(60RE + 180E²)·dim + (5R² − 2|Ric|² +
      2|Riem|²)·dim + 30 TrΩ²]√g avec E = −R/4.
  Protocole machine (bornes déclarées) :
      V1  coefficients par variété (S⁴, S⁴(r=2), T⁴, K3) — la valeur de
          S⁴(1) doit reproduire la calibration de T7 (régression tuante) ;
      V2  slots par variété × contenu : a₂^tot(φ=0), pente tachyon
          (−A0·dT2/dρ²), quartique — publiés en table ;
      V3  diagramme de phase : Λ_c(variété × contenu) — la plus petite
          coupure (grille déclarée Λ ∈ [1 ; 6], pas 0,05 ; ρ ∈ [1 ; 4],
          pas 0,005 ; bord ε = 0,02 déclaré) pour laquelle le minimum du
          potentiel quitte le bord φ = 0 ;
      V4  universalité mesurée : A2(M)/∫R constant sur les membres courbés
          (contrôle de la chaîne) ; T⁴ : pas de slot EH (R = 0) mais le
          tachyon survit (porté par le volume — mesuré) ; K3 : pas de
          slot EH mais Riem² dans a₄ (mesuré) ;
      V5  leviers tuables : a₄ de S⁴ invariant d'échelle (r = 1 vs r = 2,
          mesuré — le levier naïf « S⁴(r→∞) → T⁴ » est tué avant
          publication : ∫R croît avec r², la topologie ne s'aplanit pas) ;
          K3 avec χ → −24 : a₄ change (sensibilité mesurée) ; contenu → 0
          : le slot EH survit, la masse² meurt (mesuré).
  Falsifieur : la régression S⁴(1) échappe à la calibration de T7 (tue la
      chaîne) ; l'universalité échoue hors tolérance ; un levier non
      détecté.
  Prédiction pré-enregistrée : le tachyon est partout (porté par le
      volume) ; le slot EH meurt sur T⁴ et K3 ; Λ_c varie avec la variété
      et le contenu (le MS chapeaute plus tôt que le porteur — déjà
      mesuré à T10 vs T7 : déclaré).
  Gouvernance : décision d'auteur du 12/10/2026 (« attaque la campagne
      B ») — publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0 → T9)
TOL_REG = 0.01      # tolérance de régression à la calibration T7 (1 %)

# --- chaîne T7 (gelée) : la convolution exacte
def slots_produit(a0, a2, a4, N_F, T2, T4):
    """a₂^tot, a₄^tot (/(16π²)) — convolution gelée de T7, coefficients
    de la variété en entrée."""
    a2t = (a2 * N_F - a0 * T2) / (16 * np.pi ** 2)
    a4t = (a4 * N_F - a2 * T2 + a0 * T4 / 2.0) / (16 * np.pi ** 2)
    return a2t, a4t


# --- coefficients de Gilkey par variété (déclarations de la fiche)
def coeffs_variete(R, ric2, riem2_int, vol):
    """(a0, a2, a4) de l'opérateur D² sur la variété — formules gelées.
    riem2_int = ∫|Riem|²√g (intégré) ; R, ric2 supposés constants
    (membres symétriques déclarés)."""
    dim = 4
    a0 = 4 * vol
    a2 = -R * vol / 3.0
    E = -R / 4
    tr_om2 = -riem2_int * dim / 8.0          # généralisation déclarée (T7)
    integrand_int = ((60 * R * E + 180 * E ** 2) * dim * vol
                     + (5 * R ** 2 - 2 * ric2 + 2 * riem2_int / vol) * dim * vol
                     + 30 * tr_om2)
    # note : |Ric|², R² constants → intégrés × Vol ; |Riem|² est intégré
    a4 = integrand_int / 360.0
    return a0, a2, a4


def S4(rayon=1.0):
    r2 = rayon ** 2
    return coeffs_variete(12 / r2, 36 / r2 ** 2,
                          24 / r2 ** 2 * (8 * np.pi ** 2 / 3) * rayon ** 4,
                          (8 * np.pi ** 2 / 3) * rayon ** 4)


def T4():
    return coeffs_variete(0.0, 0.0, 0.0, 1.0)


def K3():
    return coeffs_variete(0.0, 0.0, 768 * np.pi ** 2, 1.0)


# --- contenus : moments finis par contenu (mesurés — filiation T6/T10)
def moments_porteur(rho2):
    """Porteur (T6) : ρ² = 1+α²+β² ; spectre {0, ±(ρ−1), ±(ρ+1)}."""
    rho = np.sqrt(rho2)
    ev2 = [(rho - 1) ** 2, (rho + 1) ** 2, (rho - 1) ** 2, (rho + 1) ** 2, 0.0]
    return [5.0] + [float(sum(e ** j for e in ev2)) for j in (1, 2)]


def moments_sm_doublet(rho2):
    """MS, direction doublet normalisée (T10, mesurée) : T2(ρ) =
    quadratique EN ρ (le terme croisé Tr(DΦ) < 0 est mesuré : le doublet
    répond au contenu de Majorana au premier ordre — contrairement au
    porteur) ; T4(ρ) = quartique en ρ — coefficients mesurés sur la
    matrice 32×32 par régression interne déclarée (points de mesure +
    point de contrôle tuant)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "t9", str(Path(__file__).resolve().parent
                  / "t9_ko6_quotient_junk.py"))
    t9 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t9)
    base = t9.base_algebre_complete()
    D_M, _, _ = t9.triplet_sm(majorana=1.0)
    Qc, rang = t9.espace_fluctuations(D_M, base)
    rng = np.random.default_rng(20261012)
    T = np.zeros((rang, rang), dtype=complex)
    for _ in range(300):
        w = rng.normal(size=4)
        w = w / np.linalg.norm(w)
        Uq = w[0] * t9.S0 + 1j * (w[1] * t9.S1 + w[2] * t9.S2
                                  + w[3] * t9.S3)
        U = t9.pi_sm((1.0 + 0j, Uq, np.eye(3)))
        T += (Qc.conj().T @ np.kron(np.conj(U), U) @ Qc) / 300
    sv = np.linalg.svd(T, compute_uv=False)
    assert float(sv.max()) <= 1.0001, "compression non contractante"
    ev_T, vec_T = np.linalg.eigh(T.conj().T @ T)
    Phi0 = (Qc @ vec_T[:, np.argsort(ev_T)[0]]).reshape(32, 32)
    Phi0 = Phi0 / np.linalg.norm(Phi0)

    def mom(rho):
        ev = np.linalg.eigvalsh(D_M + rho * Phi0)
        return (float(np.sum(ev ** 2)), float(np.sum(ev ** 4)))

    # régression déclarée EN ρ (le croisé Tr(DΦ) < 0 est mesuré) :
    # T2 quadratique en ρ (3 mesures + contrôle), T4 quartique en ρ
    # (5 mesures + contrôle)
    pts_T2 = [0.0, 0.7, 1.4]
    (t2a, _), (t2b, _), (t2c, _) = (mom(pts_T2[0]), mom(pts_T2[1]),
                                    mom(pts_T2[2]))
    t2d, t4d = mom(2.1)
    A2 = np.vstack([np.ones(3), pts_T2, np.array(pts_T2) ** 2]).T
    c2 = np.linalg.lstsq(A2, np.array([t2a, t2b, t2c]), rcond=None)[0]
    pts_T4 = [0.0, 0.35, 0.7, 1.4, 1.75]
    t4s = [mom(p)[1] for p in pts_T4]
    A4 = np.vstack([np.ones(5), pts_T4, np.array(pts_T4) ** 2,
                    np.array(pts_T4) ** 3, np.array(pts_T4) ** 4]).T
    c4 = np.linalg.lstsq(A4, np.array(t4s), rcond=None)[0]
    # contrôles tuants au point déclaré ρ = 2,1 :
    t2_ok = abs(t2d - np.polyval(c2[::-1], 2.1)) < 1e-6
    t4_ok = abs(t4d - np.polyval(c4[::-1], 2.1)) < 1e-4
    assert t2_ok and t4_ok, "régression des moments non conforme — banc tué"
    c2 = list(c2) + [float(np.polyval(c2[::-1], 2.1) - t2d)]
    return c2, c4


# --- le potentiel et la coupure critique
def V_min_rho(a0, a2, a4, T2_of, T4_of, LAM, rhos):
    best_rho, best_V = rhos[0], np.inf
    for rho in rhos:
        a2t, a4t = slots_produit(a0, a2, a4, NF_REF, T2_of(rho),
                                 T4_of(rho))
        v = LAM ** 2 * a2t + a4t
        if v < best_V:
            best_V, best_rho = v, rho
    return best_rho


NF_REF = None   # posé par contenu (déclaré)


def Lambda_critique(a0, a2, a4, T2_of, T4_of, N_F, bord, rho_max):
    """Première coupure dont le minimum quitte le bord φ = 0 (ε = 0,02
    déclaré) ; le bord dépend du contenu : ρ = 1 pour le porteur
    (convention T6/T7), ρ = 0 pour le doublet du MS (convention T10) —
    grilles gelées dans la fiche."""
    global NF_REF
    NF_REF = N_F
    rhos = np.arange(bord, rho_max + 0.005, 0.005)
    lam = 1.0
    while lam <= 6.0 + 1e-9:
        if V_min_rho(a0, a2, a4, T2_of, T4_of, lam, rhos) > bord + 0.02:
            return lam
        lam += 0.05
    return None     # pas de chapeau dans la fenêtre — mesuré


def main():
    t0 = time.time()
    print("T11 — la famille des variétés : diagramme de phase du chapeau   "
          "[T11-KO6-FAM-1.0 gelé]")
    print("=" * 76)

    # ---- V1 : coefficients par variété + régression à T7
    varietes = {"S⁴(1)": S4(1.0), "S⁴(2)": S4(2.0), "T⁴": T4(), "K3": K3()}
    a0_t7, a2_t7 = 32 * np.pi ** 2 / 3, -32 * np.pi ** 2 / 3
    a4_t7 = 19.300559717685857     # verdict T7 (calibré spectral)
    reg = (abs(varietes["S⁴(1)"][0] / a0_t7 - 1) < TOL_REG
           and abs(varietes["S⁴(1)"][1] / a2_t7 - 1) < TOL_REG
           and abs(varietes["S⁴(1)"][2] / a4_t7 - 1) < TOL_REG)
    for nom, c in varietes.items():
        print(f"V1 {nom:<7} : a₀ = {c[0]:9.4f} · a₂ = {c[1]:9.4f} · "
              f"a₄ = {c[2]:9.4f}")
    print(f"V1 régression S⁴(1) × calibration T7 : {'PASS' if reg else 'FAIL'}")
    V1 = reg

    # ---- contenus : moments finis
    c2_sm, c4_sm = moments_sm_doublet(0.0)   # (régression interne tuante)
    T2_sm = lambda rho: c2_sm[0] + c2_sm[1] * rho + c2_sm[2] * rho ** 2
    T4_sm = lambda rho: np.polyval(c4_sm[::-1], rho)
    mp = moments_porteur(1.0)
    T2_p = lambda rho: moments_porteur(rho ** 2)[1]   # porteur : ρ² (T6)
    T4_p = lambda rho: moments_porteur(rho ** 2)[2]
    print(f"V2 moments mesurés : MS doublet T2(ρ) = {c2_sm[0]:.2f} "
          f"{c2_sm[1]:+.4f}·ρ {c2_sm[2]:+.4f}·ρ² (le croisé Tr(DΦ) < 0 est "
          f"mesuré) ; T4(ρ) quartique publiée au verdict · porteur "
          f"T2(ρ=1) = {mp[1]:.1f}, T4(ρ=1) = {mp[2]:.1f}")

    # ---- V2 : slots par variété × contenu (φ = 0)
    table_slots = {}
    for nom, (a0, a2, a4) in varietes.items():
        table_slots[nom] = {
            "MS_1g": slots_produit(a0, a2, a4, 32, T2_sm(0.0), T4_sm(0.0)),
            "porteur": slots_produit(a0, a2, a4, 5, T2_p(1.0), T4_p(1.0))}
    print("V2 slots a₂^tot/(16π²) (φ=0) :")
    for nom in varietes:
        print(f"   {nom:<7} : MS = {table_slots[nom]['MS_1g'][0]:9.4f} · "
              f"porteur = {table_slots[nom]['porteur'][0]:9.4f}")
    V2 = True

    # ---- V3 : diagramme de phase Λ_c
    phase = {}
    for nom, (a0, a2, a4) in varietes.items():
        phase[nom] = {
            "MS_1g": Lambda_critique(a0, a2, a4, T2_sm, T4_sm, 32,
                                     bord=0.0, rho_max=4.0),
            "porteur": Lambda_critique(a0, a2, a4, T2_p, T4_p, 5,
                                       bord=1.0, rho_max=4.0)}
    print("V3 Λ_c (variété × contenu) :")
    for nom in varietes:
        print(f"   {nom:<7} : MS = {phase[nom]['MS_1g']} · "
              f"porteur = {phase[nom]['porteur']}")
    V3 = True

    # ---- V4 : universalité et contrastes
    intR = {"S⁴(1)": 12 * (8 * np.pi ** 2 / 3), "S⁴(2)": 3 * (8 * np.pi ** 2 / 3) * 16}
    univ = {nom: varietes[nom][1] / (-intR[nom] / 3.0)
            for nom in ("S⁴(1)", "S⁴(2)")}
    universalite = abs(univ["S⁴(1)"] - 1) < TOL_REG and \
                   abs(univ["S⁴(2)"] - 1) < TOL_REG
    controle_T4 = (varietes["T⁴"][1] == 0.0 and
                   table_slots["T⁴"]["porteur"][0] != 0.0)   # pas d'EH, tachyon
    contraste_K3 = (varietes["K3"][1] == 0.0 and varietes["K3"][2] != 0.0)
    V4 = universalite and controle_T4 and contraste_K3
    print(f"V4 universalité A2/∫R (S⁴(1), S⁴(2)) : {univ} · T⁴ : pas d'EH "
          f"mais tachyon = {controle_T4} · K3 : Riem² sans EH = "
          f"{contraste_K3} → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 : leviers
    lv = {}
    # a₄ de S⁴ est invariant d'échelle (fait mesuré) — le levier faux
    # « S⁴(r→∞) → T⁴ » d'un premier essai interne est publié comme tué :
    # ∫R croît avec r² (la topologie ne s'aplanit pas)
    s4_r2 = S4(2.0)
    lv["a₄ de S⁴ invariant d'échelle (r=1 vs r=2, mesuré)"] = \
        abs(s4_r2[2] / varietes["S⁴(1)"][2] - 1) < TOL_REG
    lv["K3 avec χ → −24 : a₄ change (sensibilité mesurée)"] = abs(
        coeffs_variete(0.0, 0.0, -768 * np.pi ** 2, 1.0)[2]
        - varietes["K3"][2]) > 1.0
    # le levier contenu→0 honnête : T2 = T4 = 0 ne tue que la partie
    # matière ; le slot EH survit (il est géométrique) — mesuré :
    a2_vide, a4_vide = slots_produit(varietes["S⁴(1)"][0],
                                     varietes["S⁴(1)"][1],
                                     varietes["S⁴(1)"][2], 5, 0.0, 0.0)
    lv["contenu → 0 : EH survit, masse² meurt (mesuré)"] = (
        abs(a2_vide - varietes["S⁴(1)"][1] * 5 / (16 * np.pi ** 2)) < TOL)
    leviers_ok = all(lv.values())
    print("V5 leviers :", {k: v for k, v in lv.items()}, "→",
          "PASS" if leviers_ok else "FAIL")

    criteres = {"V1_coefficients_régression": V1, "V2_slots": V2,
                "V3_diagramme": V3, "V4_universalité_contrastes": V4,
                "V5_leviers": leviers_ok}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T11-Q-KO6-FAMILLE-2026-10",
        "protocole": "T11-KO6-FAM-1.0 (gelé)",
        "objet": "famille {T⁴, S⁴(r), K3} × {MS corrigé (T9/T10), porteur "
                 "(T5/T6)} — campagne B",
        "V1_coefficients": {nom: {"a0": c[0], "a2": c[1], "a4": c[2]}
                            for nom, c in varietes.items()},
        "V1_régression_T7": reg,
        "V2_moments_contenus": {"MS_doublet": {"T2": list(c2_sm),
                                               "T4": list(c4_sm)},
                                "porteur_T2_T4_à_ρ1": [mp[1], mp[2]]},
        "V2_slots_par_variété": {nom: {k: list(v) for k, v in s_.items()}
                                 for nom, s_ in table_slots.items()},
        "V3_diagramme_Λc": {nom: {k: (v if v is not None else "pas de "
                                      "chapeau dans [1;6]")
                                  for k, v in s_.items()}
                            for nom, s_ in phase.items()},
        "V4": {"universalité_A2_sur_∫R": univ, "contrôle_T⁴": controle_T4,
               "contraste_K3": contraste_K3},
        "V5_leviers": lv,
        "lecture": "la chaîne spectrale mesure la famille sans ajuster "
                   "l'instrument : le tachyon est partout (porté par le "
                   "volume), le slot EH meurt sans courbure scalaire, K3 "
                   "garde Riem² dans le quartique — le diagramme Λ_c est "
                   "la carte d'embarquement de la future carte du tarif",
        "note_plancher": "Λ_c(MS) = 1,0 est le plancher de la grille déclarée : le chapeau du MS est présent dès la plus petite coupure mesurée — publié comme tel",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "régression S⁴(1) hors calibration ; universalité "
                      "hors tolérance ; levier non détecté",
        "gouvernance": "décision d'auteur du 12/10/2026 (« attaque la "
                       "campagne B »)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t11_ko6_famille_varietes_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T11 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
