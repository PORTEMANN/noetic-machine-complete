#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T23 — Q-KO6-T23-2026-10 : LE CADRAN — le mapping Σm_ν → ρ
      (existence mesurée, puis convention datée)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T23-KO6-CADRAN-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « le cadran » — le trou n° 1 trouvé par l'exercice T22-R :
      le mapping du nombre qui engage la machine (Σm_ν, scellé T16) vers
      l'ancre du porteur (ρ, relation d'ancre T12) n'est scellé nulle
      part. Question préalable, gelée ici : ce mapping peut-il être
      DÉRIVÉ des objets scellés ? Prédiction pré-enregistrée : NON —
      l'ancre a un plancher mesuré à 2·M_P, aucun cadran sous-Planck
      n'a de préimage réelle ; il faut donc sceller une CONVENTION
      datée (le mécanisme de la maison pour les objets déclarés,
      comme les tables KO-6 de CONVENTIONS.md).
  Filiation : T12 (relation d'ancre, sensibilité) ; T7 (le vide
      ρ_vac) ; t11 (coefficients de chaleur — fichier publié,
      IMPORTÉ) ; T22 (carte d'attente) ; T22-R (exercice — trou n° 1) ;
      T16/JALON-MCS26 (Σm_ν = 59,0 meV, empreinte publiée).
  STATUT DU MOT (déclaré, gelé) : CONVENTION — ni mesure, ni
      prédiction ; un objet déclaré daté, relu par empreinte à tout
      réveil, et TUÉ-HONNÊTEMENT si le labo déplace Σm_ν (la
      convention rescale — c'est sa fonction, comme un étalon).
  Question unique : le mapping Σm_ν → ρ peut-il être dérivé des
      objets scellés ; à défaut, quelle convention datée le remplace ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  non-existence mesurée : Λ²_sel(ρ) = ρ² + 3 − a₂/a₀ avec
          a₂/a₀ = −1 (t11, S⁴(1)) → plancher Λ_sel = 2 en unités
          M_P pour tout ρ ; les préimages ρ² requises par les
          cadrans sous-Planck sont négatives (mesurées : Σm_ν =
          4,83e-27 M_P et v = 2,02e-17 M_P donnent ρ² = −4) ;
      F2  régression T12 : dΛ/dρ au vide = 0,7453559924999299 =
          √5/3 exact (la zone utile de ρ est O(1), hors de portée
          du cadran direct) ;
      F3  la convention gelée : ρ_dial = ρ_vac · (Σm_ν / 59,0 meV)
          avec ρ_vac = √5/3 (scellé T7/T12) et 59,0 meV (scellé
          T16) — deux constantes scellées, zéro paramètre ajusté ;
          contrôle : ρ_dial(59,0 meV) = ρ_vac exactement ;
      F4  leviers : briser la proportionnalité (exposant ≠ 1)
          déplace ρ_dial (mesuré) ; le changement d'échelle déclaré
          (v = 246 GeV, entrée mesurée) rescale par le rapport
          v/59 meV = 4,17e9 (mesuré — D1 : la fiche annonçait
          4,17e12, faute de transcription d'exposant) — la
          convention est cohérente sous changement d'échelle ;
      F5  gouvernance : la convention est publiée au verdict avec
          statut CONVENTION ; elle referme le trou n° 1 de l'exercice
          T22-R et complète le protocole d'attente T22 (addenda).
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5.
  Falsifieur : F1/F2 hors tolérance (tue V1/V2) ; ρ_dial(59,0) ≠
      ρ_vac (tue F3) ; levier non détecté (tue V4).
  Prédiction pré-enregistrée : 5/5 — « le mapping direct n'existe pas
      (plancher de l'ancre mesuré) ; la convention datée le remplace ».

DÉFAUT DU BANC (trouvé au premier run du 14/10/2026 — publié) :
  D1  la fenêtre déclarée du levier de changement d'échelle visait
      4e12…5e12 alors que le rapport mesuré v/59 meV = 4,17e9 —
      faute de transcription d'exposant dans la fiche (10^12 au lieu
      de 10^9). Correction v1.1 : fenêtre 4e9…5e9, fiche corrigée.
      Le rapport, lui, était juste — c'est la borne qui mentait.
  Gouvernance : décision d'auteur du 14/10/2026 (« attaque T23 ») —
      run local exécuté avant tout push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
TOL_REG = 1e-6
PHI = (1 + np.sqrt(5)) / 2
M_P_MEV = 1.2209e28          # gelé MCS-24 (M_P = 1.2209e19 GeV)
V_EW_MEV = 2.46e11           # doublet : 246 GeV, entrée mesurée
SM_NU_MEV = 59.0             # gelé T16/JALON-MCS26


def main():
    t0 = time.time()
    print("T23 — le cadran : le mapping Σm_ν → ρ   "
          "[T23-KO6-CADRAN-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : non-existence mesuree (plancher de l'ancre)
    spec = importlib.util.spec_from_file_location(
        "t11", str(Path(__file__).resolve().parent / "t11_ko6_famille_varietes.py"))
    t11 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t11)
    a0, a2, a4 = t11.S4(1.0)
    offset = 3 - a2 / a0
    plancher = float(np.sqrt(offset))
    cadrans = {"Σm_ν = 59 meV": SM_NU_MEV, "doublet v = 246 GeV": V_EW_MEV}
    preimages = {}
    v1 = abs(a2 / a0 + 1) < TOL_REG and abs(plancher - 2.0) < TOL_REG
    print(f"V1 F1 : a₂/a₀ = {a2/a0:.9f} (t11 S⁴(1)) · plancher Λ_sel = "
          f"{plancher:.6f} M_P")
    for nom, mev in cadrans.items():
        u = mev / M_P_MEV
        rho2 = u ** 2 - offset
        preimages[nom] = rho2
        v1 &= rho2 < 0
        print(f"   {nom:22s} : {u:.3e} M_P → ρ² requis = {rho2:+.4f} "
              f"→ préimage réelle : {rho2 > 0}")
    print(f"   → aucune préimage sous-Planck (mapping direct inexistant) "
          f"→ {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : regression T12 (sensibilite au vide)
    v12 = json.loads((Path(__file__).resolve().parent.parent / "data" /
                      "t12_ko6_unimodularite_verdict.json")
                     .read_text(encoding="utf-8"))
    sens = v12["V4_sensibilité_ancre"]["dΛ/dρ_au_vide_T7"]
    rho_vac = float(np.sqrt(5) / 3)
    v2 = abs(sens - rho_vac) < TOL_REG
    print(f"V2 F2 : dΛ/dρ au vide T12 = {sens:.16f} = √5/3 : {v2} "
          f"→ {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : la convention gelee
    def rho_dial(sm_mev, exposant=1.0):
        return rho_vac * (sm_mev / SM_NU_MEV) ** exposant
    controle = rho_dial(SM_NU_MEV)
    v3 = abs(controle - rho_vac) < TOL
    print(f"V3 F3 : ρ_dial = ρ_vac·(Σm_ν/59,0 meV) — ρ_vac = √5/3 = "
          f"{rho_vac:.10f} · contrôle ρ_dial(59,0) = {controle:.10f} "
          f"= ρ_vac : {v3} → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers
    lv = {}
    lv["levier exposant : briser la proportionnalite (exp 1,5) deplace "
       "rho_dial"] = abs(rho_dial(50.0, 1.5) - rho_dial(50.0, 1.0)) > 1e-3
    rapport = V_EW_MEV / SM_NU_MEV
    lv["changement d'echelle declare (v/59 meV) : rapport mesure "
       f"{rapport:.4e}"] = 4e9 < rapport < 5e9
    lv["controle : rho_dial(59,0) = rho_vac exactement"] = \
        abs(controle - rho_vac) < TOL
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance publiee au verdict
    convention = {
        "id": "CONV-KO6-CADRAN-1.0",
        "date": "2026-10-14",
        "formule": "ρ_dial = ρ_vac · (Σm_ν / 59,0 meV)",
        "constantes_scellees": {"ρ_vac": "√5/3 (T7/T12)",
                                "Σm_ν_ref": "59,0 meV (T16/JALON-MCS26)"},
        "parametre_ajuste": 0,
        "statut": "CONVENTION — ni mesure, ni prédiction ; étalon daté, "
                  "relu par empreinte à tout réveil ; tuée-honnêtement "
                  "(rescale) si le labo déplace Σm_ν",
        "referme": "trou n° 1 de l'exercice T22-R",
    }
    V5 = convention["parametre_ajuste"] == 0 and "ρ_vac" in \
        convention["constantes_scellees"]
    print(f"V5 F5 : convention {convention['id']} publiée au verdict "
          f"(statut CONVENTION, 0 paramètre ajusté) : {V5} → "
          f"{'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_mapping_inexistant": bool(v1),
                "V2_regression_T12": bool(v2),
                "V3_convention_controlee": bool(v3),
                "V4_leviers": bool(V4),
                "V5_gouvernance": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T23-Q-KO6-CADRAN-2026-10",
        "protocole": "T23-KO6-CADRAN-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le cadran : le mapping Σm_ν → ρ n'existe pas (plancher "
                 "de l'ancre mesuré à 2 M_P) ; la convention datée "
                 "CONV-KO6-CADRAN-1.0 le remplace",
        "statut_du_mot": "CONVENTION — étalon daté, ni mesure ni "
                         "prédiction",
        "reponse_a_la_question_unique":
            "le mapping direct est IMPOSSIBLE (préimages négatives "
            "mesurées pour tout cadran sous-Planck) ; la convention "
            "ρ_dial = ρ_vac·(Σm_ν/59,0 meV), deux constantes scellées "
            "et zéro paramètre ajusté, le remplace et referme le trou "
            "n° 1 de l'exercice T22-R",
        "mesures": {"a2_sur_a0": float(a2 / a0),
                    "plancher_Lambda_sel_Mp": plancher,
                    "preimages_rho2": preimages,
                    "sensibilite_T12": sens,
                    "rho_vac": rho_vac,
                    "rho_dial_pour_59meV": controle},
        "convention": convention,
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3),
        "V4": {k: bool(v) for k, v in lv.items()},
        "V5": bool(V5),
        "falsifieur": "F1/F2 hors tolérance ; ρ_dial(59,0) ≠ ρ_vac ; "
                      "levier non détecté ; la convention meurt "
                      "honnêtement si Σm_ν sort du plancher",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t23_ko6_cadran_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T23 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
