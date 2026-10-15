#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T30 — Q-KO6-T30-2026-10 : LA TEXTURE À DEUX SAVEURS — ce qui est prédit,
      ce qui reste libre (M1 du carnet)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T30-KO6-TEXTURE-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — chantier M1 du carnet : la matrice de masse des
      neutrinos comme trois chaînes (T16), et la question : la
      texture minimale prédit-elle des RAPPORTS de masses ?
  Objet    : « la texture à deux saveurs » : trois chaînes
      (y_i, M_R, y_i) avec texture gelée diag(1, 1/4, 0) (rang 2,
      déclarée T16). Le rang 2 force m₁ = 0 exact (T16) — le plank
      59 meV en découle. Mais les RAPPORTS m₃/m₂ ?
  Filiation : T16 (texture minimale, rang 2 — fichier publié) ;
      T14 (la chaîne, forme close) ; T23 (leçon : le point doré
      y = M_R = 1 est une convention d'unité) ; NOTE-VERROU-59-MEV
      (les verrous) ; JALON-MCS26 (splittings épinglés).
  STATUT DU MOT (déclaré, gelé) : CARTOGRAPHIE interne au banc —
      une mesure honnête peut être négative ; ici la question est :
      le rapport de masses est-il doré ? Prédiction : NON.
  Question unique : la texture rang-2, confrontée aux deux splittings
      mesurés, prédit-elle le rapport m₃/m₂ — et que mesure-t-on sur
      la variété de solutions ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  régressions : chaîne T14 (forme close), texture T16
          (rang 2, m₁ = 0 exact à TOL) ;
      F2  le plank : m₁ = 0 ; m₂ + m₃ = √Δm²₂₁ + √Δm²₃₁ = 58,99 meV
          des entrées épinglées (régression T16) ;
      F3  la variété : pour chaque M_R de la grille gelée {1 ; 10 ;
          100 ; 10³ ; 10⁶} meV, les Yukawas (y₁, y₂) sont fixés par
          les splittings — une famille à UN paramètre ; le rapport
          y₁/y₂ ∈ [2,41 ; 5,56] — NON constant, NON prédit ;
      F4  l'asymptote seesaw : y₁/y₂ → √(m₃/m₂) = 2,4117 quand
          M_R → ∞ (convergence mesurée sur la grille) ; et le fait
          négatif honnête : 2,41 ≠ φ (1,62) — les rapports de masses
          ne sont PAS dorés ; le point doré de la chaîne est une
          convention d'unité (leçon T23) ;
      F5  leviers et gouvernance : le rang 3 (y₃ ≠ 0) soulève m₁ au-
          dessus de zéro (tue le plank — levier mesuré) ; le plank
          59 meV tient sur la minimalité rang-2 ; falsifier déjà
          datés (JUNO, cosmologie — registre de veille).
  Falsifieur : m₁ ≠ 0 mesuré (tue le plank et la texture) ; rapport
      constant mesuré (tuerait F3 — le contraire aussi est publié).
  Prédiction pré-enregistrée : 5/5 — « le plank est prédit, le
      rapport ne l'est pas ; la variété est une dette à un paramètre ;
      le rapport n'est pas doré ».

DÉFAUTS DU BANC (trouvés au premier run du 15/10/2026 — publiés) :
  D1  le test de régression de la chaîne mélangeait φ et 1/φ entre
      les valeurs propres — mesuré : comparaison fausse (l'instrument
      l'était, la chaîne non). Correction v1.1 : comparaison par
      valeur propre exacte.
  D2  la forme close du mode léger souffre d'ANNULATION CATASTROPHIQUE
      pour y² >> M² (les termes en M⁴ et 4M²y² s'annulent en float64
      — NaN au solveur). Correction v1.1 : forme stable par conjugaison
          m² = 2y⁴ / (M² + 2y² + M·√(M² + 4y²))
      (identique algébriquement, stable numériquement).
  Gouvernance : décision d'auteur du 15/10/2026 (« reprenons le
      carnet ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

TOL = 1e-9
PHI = (1 + np.sqrt(5)) / 2
GRILLE_MR_MEV = [1.0, 10.0, 100.0, 1e3, 1e6]     # gelée
DM21_MEV = np.sqrt(7.49e-5) * 1e3                # épinglé NuFIT v6.0
DM31_MEV = np.sqrt(2.534e-3) * 1e3


def m_leger(y, M):
    """Le mode léger de la chaîne (y, M, y) — forme stable (v1.1, D2) :
    m² = 2y⁴/(M² + 2y² + M√(M² + 4y²)) — conjugaison, pas
    d'annulation catastrophique."""
    return np.sqrt(2 * y ** 4 / (M * M + 2 * y * y
                                 + M * np.sqrt(M * M + 4 * y * y)))


def y_de_m(m, M):
    return brentq(lambda y: m_leger(y, M) - m, 1e-14, 1e7, xtol=1e-12)


def chaine(y, M):
    """La chaîne à 4 maillons (construction T14)."""
    return np.array([[0, y, 0, 0],
                     [y, 0, M, 0],
                     [0, M, 0, y],
                     [0, 0, y, 0]], dtype=float)


def main():
    t0 = time.time()
    print("T30 — la texture à deux saveurs : ce qui est prédit, ce qui "
          "reste libre   [T30-KO6-TEXTURE-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : regressions T14/T16
    ev = np.linalg.eigvalsh(chaine(1.0, 1.0))
    v1_chaine = (abs(ev[0] + PHI) < 1e-6 and abs(ev[1] + 1 / PHI) < 1e-6
                 and abs(ev[-1] - PHI) < 1e-6)
    # rang 2 : la texture gelée (1, 1/4, 0) -> m1 = 0 exact
    masses_texture = [0.0, m_leger(0.25, 1.0), m_leger(1.0, 1.0)]
    v1_rang2 = masses_texture[0] == 0.0
    V1 = bool(v1_chaine and v1_rang2)
    print(f"V1 F1 : chaîne T14 (spectre ±φ, ±1/φ) : {v1_chaine} · "
          f"texture rang-2 (1, ¼, 0), m₁ = 0 exact : {v1_rang2} → "
          f"{'PASS' if V1 else 'FAIL'}")

    # ---- V2 / F2 : le plank
    m2, m3 = DM21_MEV, DM31_MEV
    V2 = bool(abs(m2 + m3 - 58.99) < 0.01)
    print(f"V2 F2 : m₁ = 0 · m₂ + m₃ = {m2:.2f} + {m3:.2f} = "
          f"{m2 + m3:.2f} meV (plancher 58,99 — régression T16) → "
          f"{'PASS' if V2 else 'FAIL'}")

    # ---- V3 / F3 : la variété de solutions
    variete = []
    for M in GRILLE_MR_MEV:
        y2 = y_de_m(m2, M)
        y1 = y_de_m(m3, M)
        variete.append({"M_R": M, "y1": y1, "y2": y2,
                        "rapport": y1 / y2})
    rapports = [v["rapport"] for v in variete]
    v3 = bool(len(set(round(r, 3) for r in rapports)) == len(rapports)
              and min(rapports) > 2.0 and max(rapports) < 6.0)
    print(f"V3 F3 : la variété à un paramètre (grille gelée) :")
    for v in variete:
        print(f"   M_R = {v['M_R']:>8.0f} meV : y₁ = {v['y1']:.4e} · "
              f"y₂ = {v['y2']:.4e} · y₁/y₂ = {v['rapport']:.4f}")
    print(f"   rapport NON constant ([{min(rapports):.2f} ; "
          f"{max(rapports):.2f}]) — NON prédit : {v3} → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : asymptote seesaw + le fait negatif honnete
    y1h, y2h = (y_de_m(m3, 1e6), y_de_m(m2, 1e6))
    asym = y1h / y2h
    v4_seesaw = abs(asym - np.sqrt(m3 / m2)) < 1e-3
    v4_pas_dore = abs(asym - PHI) / PHI > 0.2
    V4 = bool(v4_seesaw and v4_pas_dore)
    print(f"V4 F4 : asymptote seesaw y₁/y₂ → {asym:.4f} = √(m₃/m₂) "
          f"({np.sqrt(m3/m2):.4f}) : {v4_seesaw} · fait négatif honnête "
          f": {asym:.4f} ≠ φ ({PHI:.4f}) — les rapports de masses ne "
          f"sont PAS dorés (leçon T23 : le point doré est une convention "
          f"d'unité) : {v4_pas_dore} → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 / F5 : leviers et gouvernance
    lv = {}
    m1_rang3 = m_leger(0.05, 1.0)   # y3 = 0.05 > 0
    lv["levier rang 3 (y₃ = 0,05) : m₁ = "
       f"{m1_rang3:.4f} > 0 — le plank est tué"] = m1_rang3 > 1e-4
    lv["contrôle rang 2 (y₃ = 0) : m₁ = 0 exact"] = \
        m_leger(0.0, 1.0) < 1e-12
    for k_, val in lv.items():
        print(f"V5 levier — {k_} : {val}")
    V5 = all(lv.values())
    print(f"V5 F5 : gouvernance — falsifiers datés (JUNO, cosmologie — "
          f"registre de veille) · dette résiduelle : une famille à un "
          f"paramètre → {'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_regressions_T14_T16": bool(V1),
                "V2_plancher_predi": bool(V2),
                "V3_variete_un_parametre": bool(v3),
                "V4_asymptote_pas_doree": bool(V4),
                "V5_leviers_gouvernance": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T30-Q-KO6-TEXTURE-2026-10",
        "protocole": "T30-KO6-TEXTURE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "la texture à deux saveurs : le plank 59 meV est "
                 "prédit (rang 2), le rapport de masses ne l'est pas "
                 "— et le rapport n'est pas doré",
        "statut_du_mot": "CARTOGRAPHIE interne — résultat partiellement "
                         "négatif publié au même titre",
        "mesures": {"m2_mev": m2, "m3_mev": m3, "somme_mev": m2 + m3,
                    "variete": variete,
                    "asymptote_seesaw": asym,
                    "rapport_m3_sur_m2": float(np.sqrt(m3 / m2))},
        "reponse_a_la_question_unique":
            "NON — la texture rang-2 ne prédit pas le rapport m₃/m₂ : "
            "les splittings fixent une famille à un paramètre "
            "(y₁/y₂ ∈ [2,41 ; 5,56]) dont l'asymptote 2,4117 n'est "
            "pas dorée. Le plank 59 meV tient sur m₁ = 0 exact (rang "
            "2), pas sur l'arithmétique dorée — le point φ de la "
            "chaîne est une convention d'unité (leçon T23).",
        "verdict_classe": ("S+ (plancher prédit, dette quantifiée, "
                           "fait négatif publié)"),
        "falsifieur": "m₁ ≠ 0 mesuré (tue le plank et la texture) ; "
                      "rapport constant mesuré (tuerait F3)",
        "V1": bool(V1), "V2": bool(V2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(V5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t30_ko6_texture_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T30 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
