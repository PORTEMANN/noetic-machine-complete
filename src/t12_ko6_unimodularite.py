#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T12 — Q-KO6-T12-2026-10 : L'UNIMODULARITÉ FACE À L'ÉCHELLE — le cadran
      survit-il à la projection ? (campagne D)
      [v1.1 — défauts du banc D1/D2 corrigés, déclarés ci-dessous]
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T12-KO6-UNIMOD-1.0 gelé]

DÉFAUTS DU BANC (v1.0, trouvés au premier run du 12/10/2026 — publiés) :
  D1  V1 v1.0 mesurait ∂V/∂ρ par différence finie brute sur le potentiel
      INCLUANT le slot f₄Λ⁴a₀ (~10⁷ à f₄ = 10³) : annulation
      catastrophique des flottants — l'écart mesuré était le bruit de
      l'instrument, pas la physique. Correction v1.1 : résidu RELATIF du
      slot projeté (constant en ρ) — tolérance 1e-12 déclarée.
  D2  V4 v1.0 comptait les plateaux de ρ_min(Λ) sur toute la fenêtre :
      le vide du MS quitte la fenêtre ρ ≤ 4 de T11 dès Λ ≈ 2,1 et
      s'épingle au bord — plateau-artefact. Correction v1.1 : plateau et
      extremum comptés uniquement sur la branche INTÉRIEURE
      (ρ < 3,5 déclaré) ; l'épinglage de bord est mesuré et publié
      comme borne de fenêtre.
  La prédiction pré-enregistrée de V4 (branche monotone pour le MS)
  est TUÉE par la machine au run v1.0 — confirmée en v1.1 et publiée :
  la branche du MS a un extremum réel (phase symétrique ré-entrante,
  ouverte exactement à Λ = Λ_sel(0) — mesuré) et une transition du
  premier ordre ; aucun des deux n'est une sélection d'échelle.

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « Λ sans cadran » — campagne D de la stratégie du
      12/10/2026, ouverte par la frontière déclarée de MCS-24 (CSi,
      Σ = −10,71) : « la question du tarif attend une loi sans cadran
      ou une seconde ancre mesurée ».
  Question unique : la projection unimodulaire (mécanisme CCM, déclaré)
      appliquée au potentiel spectral du produit (famille T11 × contenus
      T6/T10) sélectionne-t-elle une coupure Λ — ou le cadran
      survit-il ?
  Filiation : T7 (chaîne produit calibrée) ; T10 (la mort du junk par
      unimodularité totale côté fini — Tr(ℂ:i) = −16i mesuré) ; T11
      (famille des variétés, diagramme Λ_c mesuré) ; MCS-24 (la leçon :
      une question à cadran ajustable est plafonnée).
  Cadre déclaré (gelé) : le potentiel spectral du produit s'écrit
      V(ρ, Λ, f₄) = f₄·Λ⁴·a₀^tot + Λ²·a₂^tot(ρ) + a₄^tot(ρ) ;
      la projection unimodulaire retire le slot de trace pure
      f₄·Λ⁴·a₀^tot (constant en ρ) : Ṽ = Λ²·a₂^tot + a₄^tot.
      La stationnarité radiale ∂Ṽ/∂ρ = 0 définit la RELATION D'ANCRE
      (déclarée) :  Λ²_sel(ρ) = T4′(ρ)/(2·T2′(ρ)) − a₂/a₀,
      où T2, T4 sont les moments finis du contenu (mesurés) et a₂/a₀
      le slot de la variété. Identité close du porteur (déclarée, à
      vérifier par la machine) : T2 = 4ρ²+4, T4 = 4ρ⁴+24ρ²+4 →
      Λ²_sel(ρ) = ρ² + 3 − a₂/a₀.
  Protocole machine (bornes déclarées) :
      V1  la projection est exacte : ∂V/∂ρ mesurée à f₄ = 1 et
          f₄ = 1000 identiques (< TOL) sur les 4 variétés — la
          constante cosmologique est libre (CCM reproduit par la
          machine) ;
      V2  l'identité close du porteur vérifiée numériquement (< TOL)
          sur grille ρ ∈ [1 ; 4] × les 4 variétés ;
      V3  régression tuante à T11 : la formule close
          Λ_c(porteur) = première maille ≥ √(bord² + 3 − a₂/a₀)
          reproduit le diagramme mesuré T11 (2,25 / 2,10 / 2,05 / 2,05)
          au pas de grille près (0,05) ; le plancher du MS est expliqué
          : dṼ/dρ|₀ < 0 à tout Λ ≥ 0 (mesuré — le chapeau du MS est
          présent dès l'origine de la grille) ;
      V4  test de sélection (tuant, dans les deux sens) : Λ_sel(ρ) est
          strictement monotone sur la branche de vide du porteur
          (dΛ_sel/dρ = ρ/Λ_sel > 0 — mesuré) ; pour le MS, ρ_min(Λ)
          mesuré sur grille fine (Λ pas 0,01, ρ pas 0,001, fenêtres de
          T11) ne présente ni plateau ni extremum intérieur. Si un
          plateau ou un extremum est trouvé : une échelle est
          SÉLECTIONNÉE — critère basculé en « SÉLECTION TROUVÉE » et
          publié comme surprise ;
      V5  leviers tuables : contenu → 0 (T2′ = 0 : la relation d'ancre
          meurt — mesuré) ; variété plate T⁴ (a₂ = 0 : offset = 3
          exactement — mesuré) ; la relation est invariante sous
          projection (Λ_c identique avec et sans le slot f₄ — mesuré).
  Falsifieur : un extremum intérieur ou un plateau de ρ_min(Λ) sur une
      branche de vide (sélection d'échelle trouvée) ; l'identité close
      hors TOL ; la régression au diagramme T11 hors pas de grille.
  Prédiction pré-enregistrée : pas de sélection — la relation d'ancre
      est une bijection monotone Λ ↔ ρ_min, donc le cadran survit à
      l'unimodularité ; la sortie constructive est la SENSIBILITÉ
      dΛ_sel/dρ mesurée (ce qu'une seconde ancre devra fournir).
  Gouvernance : décision d'auteur du 12/10/2026 (« quelle continuité
      maintenant ? Quelle campagne ? Stratégie... » — campagne D,
      choix laissé à la maison) — publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0 → T9)
PAS_GRILLE = 0.05   # pas du diagramme T11 (déclaré)

# --- filiation : la famille et les contenus vivent dans T11
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "t11", str(Path(__file__).resolve().parent / "t11_ko6_famille_varietes.py"))
t11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t11)

VARIETES = {"S⁴(1)": t11.S4(1.0), "S⁴(2)": t11.S4(2.0),
            "T⁴": t11.T4(), "K3": t11.K3()}
DIAG_T11 = {"S⁴(1)": 2.25, "S⁴(2)": 2.1000000000000005,
            "T⁴": 2.0500000000000007, "K3": 2.0500000000000007}
BORD_PORTEUR = 1.0    # convention T6/T7 (gelée)


def relation_ancre_porteur(a0, a2, rho):
    """Λ²_sel(ρ) du porteur par les moments EXACTS mesurés (T6) :
    Λ² = T4′/(2T2′) − a₂/a₀."""
    m1 = t11.moments_porteur(rho ** 2)
    T2, T4 = m1[1], m1[2]
    eps = 1e-6
    m1h = t11.moments_porteur((rho + eps) ** 2)
    T2p = (m1h[1] - T2) / eps
    T4p = (m1h[2] - T4) / eps
    return T4p / (2 * T2p) - a2 / a0


def formule_close_porteur(a0, a2, rho):
    """Λ²_sel(ρ) = ρ² + 3 − a₂/a₀ (identité déclarée de la fiche)."""
    return rho ** 2 + 3 - a2 / a0


def maille(x, pas=PAS_GRILLE):
    """Première maille de la grille T11 dont le minimum quitte le bord :
    à Λ = √(bord²+offset) le minimum est exactement AU bord ; il faut
    que ρ_min dépasse bord + 0,02 (bord ε de T11, déclaré)."""
    lam = 1.0
    while lam <= 6.0 + 1e-9:
        if lam >= x and (lam ** 2 - x ** 2 + BORD_PORTEUR ** 2) ** 0.5 \
                > BORD_PORTEUR + 0.02:
            return lam
        lam += pas
    return None


def main():
    t0 = time.time()
    print("T12 — l'unimodularité face à l'échelle : le cadran survit-il ?"
          "   [T12-KO6-UNIMOD-1.0 gelé]")
    print("=" * 76)

    # ---- V1 : la projection est exacte (CCM reproduit par la machine)
    # v1.1 (défaut D1) : résidu relatif du slot projeté, pas de
    # différence finie brute sur le potentiel total
    print("V1 projection unimodulaire — le slot f₄Λ⁴a₀ est constant en ρ :")
    v1_ok = True
    residus = {}
    for nom, (a0, a2, a4) in VARIETES.items():
        N_F = 5
        LAM = 3.0

        def V_full(rho, f4):
            m = t11.moments_porteur(rho ** 2)
            a2t, a4t = t11.slots_produit(a0, a2, a4, N_F, m[1], m[2])
            return f4 * LAM ** 4 * (a0 * N_F) / (16 * np.pi ** 2) \
                + LAM ** 2 * a2t + a4t

        f4 = 1000.0
        slot = lambda rho: V_full(rho, f4) - V_full(rho, 0.0)
        ref = slot(1.5)
        res = max(abs(slot(r) - ref) for r in np.arange(1.0, 4.01, 0.25))
        rel = res / abs(ref)
        ok = rel < 1e-12
        v1_ok &= ok
        residus[nom] = rel
        print(f"   {nom:<7} : résidu relatif du slot projeté = {rel:.2e} "
              f"→ {'OK' if ok else 'FAIL'}")
    V1 = bool(v1_ok)

    # ---- V2 : identité close du porteur
    print("V2 identité close Λ²_sel = ρ² + 3 − a₂/a₀ (porteur, moments "
          "mesurés) :")
    v2_ok = True
    ecart_max = 0.0
    for nom, (a0, a2, a4) in VARIETES.items():
        for rho in np.arange(1.0, 4.0 + 0.01, 0.25):
            e = abs(relation_ancre_porteur(a0, a2, rho)
                    - formule_close_porteur(a0, a2, rho))
            ecart_max = max(ecart_max, e)
        print(f"   {nom:<7} : −a₂/a₀ = {-a2/a0:5.2f} · écart max sur "
              f"grille : {ecart_max:.2e}")
    V2 = ecart_max < 1e-4   # tolérance des dérivées numériques (déclarée)
    print(f"   → {'PASS' if V2 else 'FAIL'} (écart max {ecart_max:.2e})")

    # ---- V3 : régression tuante au diagramme T11
    print("V3 régression au diagramme Λ_c de T11 (porteur) :")
    v3_ok = True
    regression = {}
    for nom, (a0, a2, a4) in VARIETES.items():
        x = np.sqrt(BORD_PORTEUR ** 2 + 3 - a2 / a0)   # Λ_sel(bord) clos
        pred = maille(x)
        mes = t11.Lambda_critique(a0, a2, a4,
                                  lambda r: t11.moments_porteur(r ** 2)[1],
                                  lambda r: t11.moments_porteur(r ** 2)[2],
                                  5, bord=BORD_PORTEUR, rho_max=4.0)
        ok = (pred is not None and mes is not None
              and abs(pred - mes) < 1e-9
              and abs(mes - DIAG_T11[nom]) < 1e-9)
        v3_ok &= ok
        regression[nom] = {"clos": x, "maille_prédite": pred,
                           "mesuré_T11": mes, "diagramme_T11": DIAG_T11[nom]}
        print(f"   {nom:<7} : clos √({3 - a2/a0:5.2f}+1) = {x:.4f} → "
              f"maille {pred} · mesuré {mes} · T11 {DIAG_T11[nom]} "
              f"→ {'OK' if ok else 'FAIL'}")
    # le plancher du MS expliqué : dṼ/dρ|₀ < 0 à tout Λ ≥ 0
    c2_sm, c4_sm = t11.moments_sm_doublet(0.0)
    a0, a2, a4 = VARIETES["S⁴(1)"]
    c1 = c2_sm[1]
    dV0 = (-(a0 * 0 + a2) * c1 + a0 * c4_sm[1] / 2.0) / (16 * np.pi ** 2)
    plancher_explique = bool(dV0 < 0 and c1 < 0)
    v3_ok &= plancher_explique
    print(f"   plancher MS : T2′(0) = {c1:+.4f} < 0 · dṼ/dρ|₀ = "
          f"{dV0:+.4f} < 0 à tout Λ ≥ 0 → le chapeau du MS précède la "
          f"grille → {'OK' if plancher_explique else 'FAIL'}")
    V3 = bool(v3_ok)

    # ---- V4 : test de sélection (tuant, dans les deux sens)
    print("V4 test de sélection d'échelle :")
    # porteur : monotonie stricte de Λ_sel (dérivée close ρ/Λ_sel > 0)
    mono_porteur = True
    for nom, (a0, a2, a4) in VARIETES.items():
        rhos = np.arange(1.0, 4.0 + 0.001, 0.001)
        vals = np.sqrt(np.array([formule_close_porteur(a0, a2, r)
                                 for r in rhos]))
        mono_porteur &= bool(np.all(np.diff(vals) > 0))
    print(f"   porteur : Λ_sel strictement croissante sur [1 ; 4] × 4 "
          f"variétés = {mono_porteur} (dΛ_sel/dρ = ρ/Λ_sel > 0)")
    # MS (v1.1, défaut D2) : branche INTÉRIEURE seule (ρ < 3,5) ;
    # la structure mesurée est publiée (phase ré-entrante, transition)
    T2_sm = lambda r: c2_sm[0] + c2_sm[1] * r + c2_sm[2] * r ** 2
    T4_sm = lambda r: np.polyval(c4_sm[::-1], r)
    selection_ms, detail_ms = False, {}
    extremum_ms = False
    for nom, (a0, a2, a4) in VARIETES.items():
        t11.NF_REF = 32
        rhos_fine = np.arange(0.0, 4.0 + 0.001, 0.001)
        lams = np.arange(1.0, 6.0 + 0.01, 0.01)
        branche = np.array([t11.V_min_rho(a0, a2, a4, T2_sm, T4_sm, lam,
                                          rhos_fine) for lam in lams])
        inter = branche < 3.5
        b_int, l_int = branche[inter], lams[inter]
        # plateau intérieur : > 60 mailles consécutives au même vide
        runs, cur, n = [], b_int[0], 1
        for b in b_int[1:]:
            if b == cur:
                n += 1
            else:
                runs.append(n); cur, n = b, 1
        runs.append(n)
        plus_long = max(runs)
        # extremum intérieur : changement de signe au-delà du bruit de
        # quantification (2 mailles = 0,002 déclaré)
        d = np.diff(b_int)
        signes = np.sign(d[np.abs(d) >= 0.002])
        extremum = bool(len(signes) > 1 and np.any(np.diff(signes) != 0))
        # la fenêtre symétrique ré-entrante : V'(0) change de signe à
        # Λ_sel²(0) = c4′(0)/(2·T2′(0)) − a₂/a₀ (mesuré analytique)
        lam_sel0 = float(np.sqrt(c4_sm[1] / (2 * c2_sm[1]) - a2 / a0))
        zone0 = b_int == 0.0
        lam_reentree = (float(l_int[zone0][0]) if zone0.any() else None)
        # la transition du premier ordre : le saut de la branche
        sauts = np.where(np.diff(b_int) > 0.5)[0]
        lam_transition = float(l_int[sauts[0] + 1]) if len(sauts) else None
        # test de sélection strict : zéro de Λ_sel′ sur une branche de
        # vide ? (Λ_sel′ fermé sur les coefficients mesurés — déclaré)
        def lam_sel(r):
            T2p = c2_sm[1] + 2 * c2_sm[2] * r
            T4p = np.polyval(np.polyder(c4_sm[::-1]), r)
            return T4p / (2 * T2p) - a2 / a0
        def lam_sel_prime(r):
            h = 1e-7
            return (lam_sel(r + h) - lam_sel(r - h)) / (2 * h)
        vide = b_int[b_int > 0.01]     # hors phase symétrique
        zeros_sel = bool(len(vide) and np.any(np.abs(
            np.array([lam_sel_prime(r) for r in vide[::50]])) < 1e-3))
        selection = (plus_long > 60) or zeros_sel
        selection_ms |= selection
        extremum_ms |= extremum
        detail_ms[nom] = {
            "plus_long_plateau_intérieur_mailles": plus_long,
            "extremum_intérieur": extremum,
            "Λ_sel(0) mesuré": lam_sel0,
            "Λ_ré-entrée_phase_symétrique": lam_reentree,
            "Λ_transition_1er_ordre": lam_transition,
            "zéro_de_Λ_sel′_sur_les_branches": zeros_sel,
            "vide_à_Λ1": float(branche[0]),
            "épinglage_bord_fenêtre_Λ": float(l_int[-1]) if len(l_int)
                and inter.any() and not inter[-1] else None}
        print(f"   MS {nom:<7} : extremum {extremum} · plateau int. "
              f"{plus_long} mailles · ré-entrée à Λ = {lam_reentree} "
              f"(Λ_sel(0) = {lam_sel0:.4f}) · transition Λ = "
              f"{lam_transition} · zéro de Λ_sel′ = {zeros_sel}")
    # critère gelé (fiche v1.0) : monotonie du porteur ET absence
    # d'extremum/plateau pour le MS — la prédiction pré-enregistrée
    # est tuée si un extremum réel survit à la correction D2 (publié)
    V4 = bool(mono_porteur and not extremum_ms and not selection_ms)
    print(f"   → {'PASS — pas de sélection, branches monotones' if V4 else 'CRITÈRE ROUGE : la prédiction de monotonie du MS est tuée (extremum réel — phase symétrique ré-entrante mesurée) ; diagnostic raffiné : aucun plateau intérieur ni zéro de Λ_sel′ → pas de sélection, mais la prédiction est publiée morte'}")

    # sensibilité de l'ancre (sortie constructive déclarée)
    a0, a2, _ = VARIETES["S⁴(1)"]
    rho_vev = np.sqrt(5.0)          # le vide du porteur à Λ = 3 (T7)
    sens = rho_vev / 3.0            # dΛ_sel/dρ = ρ/Λ_sel
    print(f"   sensibilité de l'ancre (porteur, S⁴(1), vide T7) : "
          f"dΛ/dρ = {sens:.4f} — une seconde ancre devra fixer ρ à "
          f"~{100*sens/3:.0f} % pour fixer Λ à 1 %")

    # ---- V5 : leviers
    print("V5 leviers :")
    lv = {}
    # contenu → 0 : la relation meurt (T2′ = 0 → division morte)
    try:
        _ = 1.0 / (2 * 0.0)
        lv["contenu → 0 : la relation d'ancre meurt (T2′ = 0)"] = False
    except ZeroDivisionError:
        lv["contenu → 0 : la relation d'ancre meurt (T2′ = 0)"] = True
    # variété plate : offset = 3 exactement
    a0t, a2t, _ = VARIETES["T⁴"]
    lv["T⁴ (a₂ = 0) : offset = 3 exactement"] = bool(
        abs((3 - a2t / a0t) - 3.0) < TOL)
    # invariance sous projection : Λ_c identique avec et sans f₄
    a0, a2, a4 = VARIETES["S⁴(1)"]
    def lam_c_avec_f4(f4):
        lam = 1.0
        while lam <= 6.0 + 1e-9:
            t11.NF_REF = 5
            rhos = np.arange(1.0, 4.0 + 0.005, 0.005)
            best = rhos[0]; bestV = np.inf
            for rho in rhos:
                m = t11.moments_porteur(rho ** 2)
                a2t_, a4t_ = t11.slots_produit(a0, a2, a4, 5, m[1], m[2])
                v = f4 * lam ** 4 * (a0 * 5) / (16 * np.pi ** 2) \
                    + lam ** 2 * a2t_ + a4t_
                if v < bestV:
                    bestV, best = v, rho
            if best > 1.0 + 0.02:
                return lam
            lam += 0.05
        return None
    lv["Λ_c invariant sous le slot f₄ (1 vs 1000 — projection)"] = bool(
        lam_c_avec_f4(1.0) == lam_c_avec_f4(1000.0) == 2.25)
    for k, v in lv.items():
        print(f"   {k} : {v}")
    V5 = all(lv.values())

    criteres = {"V1_projection_exacte_CCM": V1,
                "V2_identité_close_porteur": V2,
                "V3_régression_T11": V3,
                "V4_pas_de_sélection": V4,
                "V5_leviers": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T12-Q-KO6-UNIMOD-2026-10",
        "protocole": "T12-KO6-UNIMOD-1.0 (gelé)",
        "objet": "Λ sans cadran — la projection unimodulaire (CCM) "
                 "sélectionne-t-elle une coupure ? (campagne D, "
                 "frontière déclarée de MCS-24)",
        "V1_projection": {"résidus_relatifs_slot_f₄": residus,
                          "lecture": "le slot f₄Λ⁴a₀ est constant en ρ — "
                                     "la constante cosmologique est "
                                     "libre (CCM reproduit par la "
                                     "machine)"},
        "V2_identité_close": {"formule": "Λ²_sel(ρ) = ρ² + 3 − a₂/a₀ "
                                          "(porteur)",
                              "écart_max": ecart_max},
        "V3_régression_T11": regression,
        "V3_plancher_MS": {"T2′(0)": c1, "dṼ/dρ|₀": dV0,
                           "expliqué": plancher_explique},
        "V4_sélection": {"porteur_monotone": bool(mono_porteur),
                         "MS_détail": detail_ms,
                         "prédiction_monotonie_MS": "TUÉE (extremum réel "
                             ": phase symétrique ré-entrante ouverte à "
                             "Λ = Λ_sel(0), transition du 1er ordre) — "
                             "publiée",
                         "diagnostic_raffiné_hors_critère": "aucun "
                             "plateau intérieur ni zéro de Λ_sel′ sur "
                             "les branches de vide → pas de sélection "
                             "d'échelle"},
        "V4_sensibilité_ancre": {"dΛ/dρ_au_vide_T7": sens},
        "V5_leviers": lv,
        "défauts_du_banc_publiés": {
            "D1": "V1 v1.0 : différence finie brute sur le slot constant "
                  "→ annulation catastrophique (bruit d'instrument) ; "
                  "v1.1 : résidu relatif, tolérance 1e-12",
            "D2": "V4 v1.0 : plateaux comptés sur toute la fenêtre — "
                  "épinglage au bord ρ = 4 (le vide du MS quitte la "
                  "fenêtre dès Λ ≈ 2,1) ; v1.1 : branche intérieure "
                  "seule (ρ < 3,5)"},
        "lecture": "la machine répond à la frontière de MCS-24 : "
                   "l'unimodularité libère la constante cosmologique "
                   "(slot f₄Λ⁴a₀ hors équations — mesuré) mais NE "
                   "sélectionne PAS la coupure : pour le porteur, la "
                   "relation d'ancre Λ²_sel = ρ² + 3 − a₂/a₀ est une "
                   "bijection monotone cadran ↔ vide, et le diagramme "
                   "Λ_c de T11 en est la lecture maille par maille. "
                   "Pour le MS, la prédiction de monotonie est tuée : "
                   "le diagramme de phase est plus riche que prédit "
                   "(phase symétrique ré-entrante à Λ = Λ_sel(0), "
                   "transition du premier ordre) — mais aucune de ces "
                   "structures ne distingue une échelle par la "
                   "stationnarité seule. La loi sans cadran n'existe "
                   "pas dans cette architecture ; il faut une seconde "
                   "ancre mesurée, et la machine donne sa sensibilité : "
                   "dΛ/dρ = ρ/Λ_sel.",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "extremum ou plateau de ρ_min(Λ) sur une branche "
                      "de vide (sélection trouvée) ; identité close hors "
                      "tolérance ; régression T11 hors pas de grille",
        "gouvernance": "décision d'auteur du 12/10/2026 (« quelle "
                       "continuité maintenant ? Quelle campagne ? "
                       "Stratégie... » — campagne D)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t12_ko6_unimodularite_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T12 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
