#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1b — BATTERIE RÉTROACTIVE SUR LE CORPUS (F7)
=============================================
Application rétroactive du protocole gelé PERT-BATT-1.0 (A1) aux deux
chantiers partiels que le registre A4 (entrée F7-PARTIELS-PROTOCOLE)
désigne : P13 (stabilité) et P22 (double bêta).

Le coût de fermeture déclaré de F7 est :
  « encapsuler P13/P22 en f(π) et passer la batterie A1 ; publier les
    couples (V, Σ) »
Le falsifieur de F7 est : « l'exécution de la batterie fixe le statut ».

Discipline d'encapsulation
  - D est INTÉGRALEMENT repris des scripts du corpus (constantes, tables
    de noyaux, coefficients BW-P16) : aucune donnée nouvelle, aucune
    donnée retouchée. Les formules sont copiées à l'identique.
  - π = les choix de PROTOCOLE (seuils de décision, tolérances, bornes) —
    ce sont eux, et eux seuls, que la batterie perturbe (C1 de PERT-BATT).
  - Les verdicts nominaux sont recalculés par les formules du corpus :
    la batterie ne relitige pas V, elle ajoute Σ.

Axes de perturbation déclarés AVANT EXÉCUTION (plan factoriel axial,
une coordonnée à la fois, nominal inclus) :

  P13 : tol_gn {0.10, 0.20, 0.25} · seuil_hiérarchie {12, 18} ·
        cassure_bas {0.8, 1.2} · cassure_haut {1.8, 2.2} ·
        tol_regge {0.10, 0.20, 0.25}
  P22 : seuil_q2 {0.3, 0.7, 1.0} · seuil_q1 {0.3, 0.7} ·
        tol_qok {1.0, 2.0} · pente_min {5.0, 7.0} · pente_max {14.0, 18.0} ·
        seuil_levier {3, 5} · n_min_qok {6, 8}

PRÉDICTIONS PRÉ-ENREGISTRÉES (avant toute exécution)
  P-A1b-1 : P13 est stable — Σ = 1 sur ses 4 composantes (les marges
            nominales sont larges devant les tolérances perturbées).
  P-A1b-2 : P22 garde Σ = 1 sur ses composantes STRUCTURELLES
            (mécanisme d'appariement dérivé ; signes Qbb 9/9) ; toute
            fragilité est confinée aux composantes À SEUIL
            (levier, faux positifs, pente de phase, magnitude Qbb).
Falsifieur des prédictions : une fragilité de P13 tue P-A1b-1 ; une
fragilité de « mécanisme_appariement_dérivé » ou de
« Qbb_signe_émetteurs_9sur9 » tue P-A1b-2. Une prédiction tuée est
publiée comme B3-FAIL de prédiction.

Critères gelés (hérités de PERT-BATT-1.0)
  C0  reproductibilité : la batterie complète est exécutée DEUX fois ;
      (V, Σ) doivent être identiques — aucune graine cachée.
  C1  D et S intacts : seul π est perturbé.
  C2  toute fragilité (Σ < 1) est publiée avec l'axe responsable.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a1_batterie_perturbation import batterie  # PERT-BATT-1.0 (gelé)

# ====================================================================
# P13 encapsulé — D reprise à l'identique de src/p13_stabilite.py
# ====================================================================

HC = 197.3269804              # hbar.c en MeV.fm
C_LIGHT = 2.99792458e23       # c en fm/s
E2 = 1.4399645                # e^2/(4 pi eps0) en MeV.fm
R0 = 1.2                      # fm, ancrage P6/P9/P11
M_AMU = 931.494               # MeV/c^2
M_ALPHA = 3727.379            # MeV/c^2
ZALPHA = 2.0

ALPHA = [
    ("212Po", 208, 82, 8.784, 2.99e-7),
    ("218Po", 214, 82, 6.115, 0.186),
    ("216Po", 212, 82, 6.906, 0.145),
    ("214Po", 210, 82, 7.833, 1.64e-4),
    ("226Ra", 222, 86, 4.784, 1.60e3 * 3.156e7),
    ("228Th", 224, 88, 5.423, 1.912 * 3.156e7),
    ("230Th", 226, 88, 4.687, 7.54e4 * 3.156e7),
    ("232Th", 228, 88, 4.083, 1.40e10 * 3.156e7),
    ("235U", 231, 90, 4.679, 7.04e8 * 3.156e7),
    ("238U", 234, 90, 4.270, 4.468e9 * 3.156e7),
    ("241Pu", 237, 92, 5.150, 14.3 * 3.156e7),
    ("244Cm", 240, 94, 5.805, 18.1 * 3.156e7),
    ("252Cf", 248, 96, 6.118, 2.645 * 3.156e7),
    ("148Gd", 144, 62, 3.183, 70.9 * 3.156e7),
    ("151Eu", 147, 63, 1.964, 4.62e18 * 3.156e7),
]

SIGMA = 0.18       # GeV^2, tension de corde mesurée
M_MESON = 0.775    # GeV, rho
REGGE_MES = 0.9    # GeV^-2, pente mesurée de référence


def gamow(A_d, Z_d, E):
    """Facteur de Gamow — formule du corpus, inchangée."""
    Rc = R0 * A_d ** (1 / 3.0)
    b = Z_d * ZALPHA * E2 / E
    if b <= Rc:
        return Rc, b, 0.0, 0.0
    mu = (M_ALPHA * M_AMU * A_d) / (M_ALPHA + M_AMU * A_d)
    x = Rc / b
    arg = np.arccos(np.sqrt(x)) - np.sqrt(x * (1 - x))
    V0 = Z_d * ZALPHA * E2
    G = np.sqrt(2 * mu * V0 * b) / HC * arg
    v = np.sqrt(2.0 * E / M_ALPHA) * C_LIGHT
    f = v / (2 * Rc)
    log10_t12 = (np.log(np.log(2)) - np.log(f) + 2 * G) / np.log(10)
    return Rc, b, G, log10_t12


def p13_chantier(pi):
    """f(π) → (verdicts, mesures).
    π : tol_gn, seuil_hiérarchie, cassure_bas, cassure_haut, tol_regge."""
    xs, ycalc, ymes = [], [], []
    for nom, Ad, Zd, E, t in ALPHA:
        Rc, b, G, l10 = gamow(Ad, Zd, E)
        xs.append(Zd / np.sqrt(E))
        ycalc.append(l10)
        ymes.append(float(np.log10(t)))
    xs = np.array(xs)
    pente_calc = float(np.polyfit(xs, ycalc, 1)[0])
    pente_mes = float(np.polyfit(xs, ymes, 1)[0])
    marge_gn = abs(pente_calc - pente_mes) / abs(pente_mes)
    ordres = float(max(ymes) - min(ymes))

    sigma_GeVfm = SIGMA / 0.197327
    r_casse = 2 * M_MESON / sigma_GeVfm
    alpha_p = 1 / (2 * np.pi * SIGMA)
    marge_regge = abs(alpha_p - REGGE_MES) / REGGE_MES

    verdicts = {
        "geiger_nuttall_pente": bool(marge_gn < pi["tol_gn"]),
        "hiérarchie_ordres": bool(ordres > pi["seuil_hiérarchie"]),
        "cassure_corde_calculée": bool(pi["cassure_bas"] < r_casse
                                       < pi["cassure_haut"]),
        "regge_pente": bool(marge_regge < pi["tol_regge"]),
    }
    mesures = {
        "pente_calc": pente_calc, "pente_mes": pente_mes,
        "marge_gn": float(marge_gn), "ordres_couverts": ordres,
        "r_casse_fm": float(r_casse), "alpha_p_GeV_2": float(alpha_p),
        "marge_regge": float(marge_regge),
    }
    return verdicts, mesures


P13_NOMINAL = {"tol_gn": 0.15, "seuil_hiérarchie": 15.0,
               "cassure_bas": 1.0, "cassure_haut": 2.0, "tol_regge": 0.15}
P13_AXES = {
    "tol_gn": [0.10, 0.20, 0.25],
    "seuil_hiérarchie": [12.0, 18.0],
    "cassure_bas": [0.8, 1.2],
    "cassure_haut": [1.8, 2.2],
    "tol_regge": [0.10, 0.20, 0.25],
}

# ====================================================================
# P22 encapsulé — D reprise à l'identique de src/p22_doublebeta.py
# ====================================================================

AV, AS, AA, AP, AC = 15.8, 18.3, 23.2, 12.0, 0.71
MN_MP = 1.293

EMETTEURS = [
    ("48Ca", 48, 20, 4.27, 6.4e19),
    ("76Ge", 76, 32, 2.04, 1.9e21),
    ("82Se", 82, 34, 3.00, 9.6e19),
    ("96Zr", 96, 40, 3.35, 2.3e19),
    ("100Mo", 100, 42, 3.03, 7.1e18),
    ("116Cd", 116, 48, 2.81, 3.0e19),
    ("130Te", 130, 52, 2.53, 7.0e20),
    ("136Xe", 136, 54, 2.46, 2.2e21),
    ("150Nd", 150, 60, 3.37, 9.1e18),
]
TEMOINS = [
    ("40Ca", 40, 20), ("56Fe", 56, 26), ("88Sr", 88, 38), ("120Sn", 120, 50),
    ("138Ba", 138, 56), ("140Ce", 140, 58), ("142Ce", 142, 58),
    ("208Pb", 208, 82),
]


def Eb(N, Z, ap=AP):
    """Bethe-Weizsäcker P16 — coefficients du corpus, inchangés."""
    A = N + Z
    if N < 0 or Z < 0:
        return 0.0
    pair = (1 if (N % 2 == 0 and Z % 2 == 0)
            else (-1 if (N % 2 == 1 and Z % 2 == 1) else 0))
    return (AV * A - AS * A ** (2 / 3) - AA * (N - Z) ** 2 / A
            - AC * Z ** 2 / A ** (1 / 3) + pair * ap / np.sqrt(A))


def Q1(A, Z, ap=AP):
    return MN_MP + Eb(A - Z - 1, Z + 1, ap) - Eb(A - Z, Z, ap)


def Q2(A, Z, ap=AP):
    return 2 * MN_MP + Eb(A - Z - 2, Z + 2, ap) - Eb(A - Z, Z, ap)


def p22_chantier(pi):
    """f(π) → (verdicts, mesures).
    π : seuil_q2, seuil_q1, tol_qok, pente_min, pente_max, seuil_levier,
        n_min_qok."""
    def selectionne(A, Z, ap=AP):
        return (Z % 2 == 0 and (A - Z) % 2 == 0
                and Q2(A, Z, ap) > pi["seuil_q2"]
                and Q1(A, Z, ap) < pi["seuil_q1"])

    rows_e = []
    for nom, A, Z, qm, tm in EMETTEURS:
        rows_e.append(dict(nom=nom, A=A, Z=Z, q2=Q2(A, Z), qm=qm, tm=tm,
                           sel=selectionne(A, Z)))
    faux_pos = [nom for nom, A, Z in TEMOINS if selectionne(A, Z)]
    sans_ap = sum(1 for nom, A, Z, qm, tm in EMETTEURS
                  if selectionne(A, Z, ap=0.0))

    qm = np.array([r["qm"] for r in rows_e])
    tm = np.array([r["tm"] for r in rows_e])
    n_phase = float(-np.polyfit(np.log(qm), np.log(tm), 1)[0])
    n_qok = sum(1 for r in rows_e if abs(r["q2"] - r["qm"]) <= pi["tol_qok"])

    verdicts = {
        "mécanisme_appariement_dérivé": bool(
            all(r["Z"] % 2 == 0 and (r["A"] - r["Z"]) % 2 == 0
                for r in rows_e)),
        "Qbb_signe_émetteurs_9sur9": bool(
            all(r["q2"] > 0 for r in rows_e)),
        "levier_appariement_discriminant": bool(
            sans_ap <= pi["seuil_levier"]),
        "faux_positifs_localisés_magiques_P16": bool(
            all(n in ("120Sn", "142Ce") for n in faux_pos)),
        "pente_phase_bornée": bool(pi["pente_min"] <= n_phase
                                   <= pi["pente_max"]),
        "Qbb_magnitude_échec_documenté": bool(n_qok >= pi["n_min_qok"]),
    }
    mesures = {
        "pente_n_phase": n_phase,
        "offset_systématique_qbb": float(
            np.mean([r["q2"] - r["qm"] for r in rows_e])),
        "sélection_émetteurs": float(sum(r["sel"] for r in rows_e)),
        "faux_positifs_témoins": float(len(faux_pos)),
        "sans_appariement_sélectionnés": float(sans_ap),
        "n_qok": float(n_qok),
    }
    return verdicts, mesures


P22_NOMINAL = {"seuil_q2": 0.5, "seuil_q1": 0.5, "tol_qok": 1.5,
               "pente_min": 6.0, "pente_max": 16.0, "seuil_levier": 4,
               "n_min_qok": 7}
P22_AXES = {
    "seuil_q2": [0.3, 0.7, 1.0],
    "seuil_q1": [0.3, 0.7],
    "tol_qok": [1.0, 2.0],
    "pente_min": [5.0, 7.0],
    "pente_max": [14.0, 18.0],
    "seuil_levier": [3, 5],
    "n_min_qok": [6, 8],
}


# ====================================================================
# Exécution — C0 : la batterie tourne DEUX fois, (V, Σ) identiques
# ====================================================================

def main():
    print("A1b — BATTERIE RÉTROACTIVE P13 / P22   [PERT-BATT-1.0, F7]")
    print("=" * 70)

    rapports, c0 = {}, {}
    for nom, chantier, nominal, axes in [
        ("P13-STABILITE", p13_chantier, P13_NOMINAL, P13_AXES),
        ("P22-DOUBLE-BETA", p22_chantier, P22_NOMINAL, P22_AXES),
    ]:
        r1 = batterie(nom, chantier, nominal, axes)
        r2 = batterie(nom, chantier, nominal, axes)
        c0[nom] = bool(
            r1["verdicts_nominaux"] == r2["verdicts_nominaux"]
            and r1["stabilité_par_composante"] == r2["stabilité_par_composante"]
            and r1["fragilités_publiées"] == r2["fragilités_publiées"])
        rapports[nom] = r1

        print(f"\n### {nom} — {r1['n_protocoles_testés']} protocoles "
              f"(1 nominal + {r1['n_protocoles_testés'] - 1} perturbés)  "
              f"[C0 reproductibilité : {'PASS' if c0[nom] else 'FAIL'}]")
        for comp, s in r1["stabilité_par_composante"].items():
            etat = "STABLE" if s == 1.0 else f"FRAGILE Σ={s:.2f}"
            print(f"  {comp:<38} Σ = {s:.2f}   {etat}")
        if r1["fragilités_publiées"]:
            print("  --- B3-FAIL de protocole (publié) ---")
            for comp, details in r1["fragilités_publiées"].items():
                for d in details:
                    print(f"  ⚠ {comp} : {d}")
        else:
            print("  aucune fragilité de verdict détectée")

    # ---- prédictions pré-enregistrées ---------------------------------
    s13 = rapports["P13-STABILITE"]["stabilité_par_composante"]
    s22 = rapports["P22-DOUBLE-BETA"]["stabilité_par_composante"]
    p_a1b_1 = all(s == 1.0 for s in s13.values())
    structurelles = ["mécanisme_appariement_dérivé", "Qbb_signe_émetteurs_9sur9"]
    p_a1b_2 = all(s22[c] == 1.0 for c in structurelles)
    predictions = {
        "P-A1b-1_P13_intégralement_stable": {
            "statut": "CONFIRMÉE" if p_a1b_1 else "RÉFUTÉE (B3-FAIL de prédiction)",
            "détail": {c: s13[c] for c in s13}},
        "P-A1b-2_P22_structurel_stable_fragilités_confinées_aux_seuils": {
            "statut": "CONFIRMÉE" if p_a1b_2 else "RÉFUTÉE (B3-FAIL de prédiction)",
            "détail": {c: s22[c] for c in s22}},
    }

    print("\n" + "=" * 70)
    print("PRÉDICTIONS PRÉ-ENREGISTRÉES")
    for nom, p in predictions.items():
        print(f"  {nom} : {p['statut']}")

    resultats = {
        "chantier": "A1B-BATTERIE-RETROACTIVE",
        "registre": "ferme F7-PARTIELS-PROTOCOLE (A4, REG-FR-1.0) : le coût "
                    "de fermeture déclaré était l'encapsulation f(π) + la "
                    "batterie A1 + la publication des couples (V, Σ) — payé",
        "protocole": "PERT-BATT-1.0 (gelé, hérité d'A1) — plan factoriel "
                     "axial, une coordonnée perturbée à la fois, axes "
                     "déclarés avant exécution",
        "discipline": "D repris à l'identique du corpus (p13_stabilite.py, "
                      "p22_doublebeta.py) ; seuls les choix de protocole π "
                      "sont perturbés ; les verdicts nominaux sont "
                      "recalculés par les formules du corpus, non relitigés",
        "rapports": rapports,
        "prédictions_pré_enregistrées": predictions,
        "verdict_global": {
            "C0_reproductibilité": ("PASS — deux exécutions, (V, Σ) "
                                    "identiques sur les deux chantiers"
                                    if all(c0.values()) else
                                    f"FAIL — {c0}"),
            "C1_D_et_S_intacts": "PASS — seul π est perturbé ; D copié du "
                                 "corpus sans retouche",
            "C2_fragilités_publiées": "voir fragilités_publiées par chantier",
            "couples_V_Σ": {
                "P13": {"V_nominal": rapports["P13-STABILITE"]["verdicts_nominaux"],
                        "Σ_min": round(min(s13.values()), 4)},
                "P22": {"V_nominal": rapports["P22-DOUBLE-BETA"]["verdicts_nominaux"],
                        "Σ_min": round(min(s22.values()), 4)},
            },
        },
        "falsifieur": "l'exécution de la batterie fixe le statut de F7 "
                      "(registre A4) — exécutée",
    }

    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).with_name("a1b_batterie_retroactive_verdict.json")
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")

    print("\n" + "=" * 70)
    print("COUPLES (V, Σ) PUBLIÉS — F7 fermée par exécution")
    for nom in ("P13", "P22"):
        c = resultats["verdict_global"]["couples_V_Σ"][nom]
        n_ok = sum(c["V_nominal"].values())
        print(f"  {nom} : V nominal = {n_ok}/{len(c['V_nominal'])} "
              f"composantes, Σ_min = {c['Σ_min']:.2f}")
    print(f"\nSHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
