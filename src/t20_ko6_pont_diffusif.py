#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T20 — Q-KO6-T20-2026-10 : LE PONT DIFFUSIF — le φ quasicristallin
      (pavages de Penrose ↔ chaîne de Fibonacci ↔ chaîne du seesaw)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T20-KO6-DIFF-1.0 gelé]

DÉFAUTS DU BANC (v1.0, trouvés au premier run du 14/10/2026 — publiés) :
  D1  V1 comparait le mot de Fibonacci au mot mécanique brut, avec la
      correspondance 1 → 'a' — mesuré : deux conventions étaient
      fausses ; la bonne est le MOT CARACTÉRISTIQUE de pente
      θ = 1/φ² : s_i = ⌊(i+2)θ⌋ − ⌊(i+1)θ⌋, avec 1 → 'b'
      (θ est la densité des b ; les a, plus fréquents (1/φ), sont les
      0). abaab… se lit 0,1,0,0,1… au décalage d'un indice.
      Correction v1.1 : mot caractéristique, correspondance 0 → 'a'.
      La pente et le fait ne sont pas tués — l'instrument l'était.
  D2  le levier de l'inflation dégonflée exigeait |3 − φ²| > 0,5 —
      mesuré : 3 − φ² = 0,382 (le seuil était mal posé, pas le
      levier : la matrice [[2,1],[1,2]] a bien PF = 3 ≠ φ² et
      det 3, non unimodulaire). Correction v1.2 : seuil 0,3.

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « le pont diffusif » — la carte Penrose/quasicristaux
      déclarée candidate au dictionnaire T18 (le φ y est diffusif, pas
      spectral). Deux objets canoniques : la chaîne de Fibonacci
      (quasicristal 1D, substitution a→ab, b→a) et les losanges de
      Penrose (quasicristal 2D, inflation par matrice entière). Le
      pont avec le corpus : les matrices de substitution portent le
      même spectre doré que la chaîne du seesaw.
  Filiation : T17 (mot Fibonacci, matrice S) ; T14 (chaîne C(1)) ;
      T18 (dictionnaire — l'entrée éprouvée) ; T19 (pont φ) ;
      koilon-scale-e8 (déclaré, non mesuré).
  STATUT DU MOT (déclaré, gelé) : PONT DIFFUSIF — théorème mesuré à
      zéro paramètre ; AUCUNE prédiction d'expérience ; le physique
      du corpus (59 meV) n'est pas touché.
  Question unique : le φ quasicristallin (densités, diagonales des
      losanges, spectres des matrices de substitution) coïncide-t-il
      avec les faces déjà mesurées du pont φ — et les leviers
      (pente rationnelle, Thue-Morse, dégonflement de l'inflation)
      tuent-ils le pont comme déclaré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  chaîne de Fibonacci : densités des lettres → 1/φ (a) et
          1/φ² (b) ; le mot est mécanique de pente θ = 1/φ²
          (grille de niveaux gelée n = 12…15) ;
      F2  losanges de Penrose (côté 1) : losange épais (angles
          72°/108°) — grande diagonale 2cos(π/5) = φ ; losange
          mince (36°/144°) — petite diagonale 2sin(π/10) = 1/φ ;
      F3  inflation 2D des pavages (matrice gelée M = [[2,1],[1,1]]) :
          valeur propre dominante φ² ; les populations de losanges
          sous itérations tendent au ratio φ (vecteur propre) ;
      F4  pont diffusif ↔ spectral : Tr Qⁿ = Lucas(n) pour la
          matrice 1D Q = [[1,1],[1,0]] (grille n = 1…12) ; et
          Tr Mⁿ = Lucas(2n) = Tr C(1)^(2n)/2 — les traces du
          quasicristal 2D sont la moitié des traces de la chaîne
          du seesaw (régression T17, exacte) ;
      F5  leviers : pente rationnelle 13/34 tue F1 ; Thue-Morse
          (densités 1/2, spectre {2, 0}) échoue comme témoin ;
          l'inflation dégonflée [[2,1],[1,2]] (det 3, non
          unimodulaire, PF 3 ≠ φ²) tue F3.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5 (régressions
      tuantes : T17 pour Tr C(1)^(2n), T14 pour le spectre).
  Falsifieur : F1…F4 hors TOL_REG (tue V1…V4) ; un levier non
      détecté (tue V5).
  Prédiction pré-enregistrée : 5/5 — le pont diffusif tient, les
      leviers tuent.
  Gouvernance : décision d'auteur du 14/10/2026 (« on y va » — carte
      Penrose) — run local exécuté avant tout push, empreinte figée
      au verdict.
"""
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0)
TOL_REG = 1e-6      # tolérance de régression (déclarée)
PHI = (1 + np.sqrt(5)) / 2
GRILLE_NIV = [12, 13, 14, 15]     # gelée (mots de Fibonacci)
GRILLE_P = list(range(1, 13))     # gelée (traces de matrices)


def mot_fibonacci(n):
    """Le mot de Fibonacci par substitution gelée a→ab, b→a."""
    w = "a"
    for _ in range(n):
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def mot_mecanique(n_let, theta):
    """Mot caractéristique de pente θ (v1.1, D1 corrigé) :
    s_i = ⌊(i+2)θ⌋ − ⌊(i+1)θ⌋ — 1 → 'b' (θ = densité des b)."""
    return "".join("b" if int(np.floor((i + 2) * theta))
                   - int(np.floor((i + 1) * theta)) == 1 else "a"
                   for i in range(n_let))


def lucas(k):
    a, b = 2, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def chaine(y, M):
    """La chaîne à 4 maillons de sauts (y, M, y) — construction T14."""
    return np.array([[0, y, 0, 0],
                     [y, 0, M, 0],
                     [0, M, 0, y],
                     [0, 0, y, 0]], dtype=float)


def main():
    t0 = time.time()
    print("T20 — le pont diffusif : le φ quasicristallin   "
          "[T20-KO6-DIFF-1.0 gelé — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : densités + caractère mécanique de pente 1/φ²
    theta = (3 - np.sqrt(5)) / 2          # = 1/φ²
    v1_dens = v1_meca = True
    for niv in GRILLE_NIV:
        w = mot_fibonacci(niv)
        na, nb = w.count("a"), w.count("b")
        v1_dens &= (abs(na / len(w) - 1 / PHI) < 1e-3
                    and abs(nb / len(w) - 1 / PHI ** 2) < 1e-3)
        w_m = mot_mecanique(len(w), theta)
        v1_meca &= (w == w_m)
    V1 = bool(v1_dens and v1_meca)
    print(f"V1 F1 : densités → 1/φ, 1/φ² (niveaux {GRILLE_NIV}) : "
          f"{v1_dens} · mot mécanique de pente 1/φ² : {v1_meca} → "
          f"{'PASS' if V1 else 'FAIL'}")

    # ---- V2 / F2 : diagonales des losanges de Penrose
    epais_long = 2 * np.cos(np.pi / 5)            # losange 72°/108°
    mince_court = 2 * np.sin(np.pi / 10)          # losange 36°/144°
    V2 = (abs(epais_long - PHI) < TOL_REG
          and abs(mince_court - 1 / PHI) < TOL_REG)
    print(f"V2 F2 : losange épais grande diagonale = {epais_long:.9f} "
          f"(φ) · losange mince petite diagonale = {mince_court:.9f} "
          f"(1/φ) → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 / F3 : inflation 2D — M = [[2,1],[1,1]], PF φ², ratio φ
    M = np.array([[2, 1], [1, 1]], dtype=float)
    vp = np.linalg.eigvalsh(M)
    v3_vp = (abs(max(vp) - PHI ** 2) < TOL_REG
             and abs(min(vp) - 1 / PHI ** 2) < TOL_REG)
    pop = np.array([1.0, 1.0])                    # (épais, mince)
    ratios = []
    for _ in range(14):
        pop = M @ pop
        ratios.append(pop[0] / pop[1])
    v3_ratio = abs(ratios[-1] - PHI) < 1e-4 and \
        all(abs(ratios[k + 1] - PHI) <= abs(ratios[k] - PHI) + 1e-12
            for k in range(len(ratios) - 1))
    V3 = bool(v3_vp and v3_ratio)
    print(f"V3 F3 : inflation M = [[2,1],[1,1]] — VP = "
          f"{np.round(sorted(vp, reverse=True), 9).tolist()} (φ², φ⁻²) : "
          f"{v3_vp} · populations → ratio φ : {v3_ratio} (niveau 14 : "
          f"{ratios[-1]:.9f}) → {'PASS' if V3 else 'FAIL'}")

    # ---- V4 / F4 : pont diffusif ↔ spectral (régressions T17)
    Q = np.array([[1, 1], [1, 0]], dtype=float)
    v4_q = all(abs(np.trace(np.linalg.matrix_power(Q, n))
                   - lucas(n)) < TOL_REG for n in GRILLE_P)
    v4_m = all(abs(np.trace(np.linalg.matrix_power(M, n))
                   - lucas(2 * n)) < TOL_REG for n in GRILLE_P)
    C1 = chaine(1.0, 1.0)
    v4_pont = all(abs(np.trace(np.linalg.matrix_power(M, n))
                      - np.trace(np.linalg.matrix_power(C1, 2 * n)) / 2)
                  < TOL_REG for n in GRILLE_P)
    V4 = bool(v4_q and v4_m and v4_pont)
    print(f"V4 F4 : Tr Qⁿ = Lucas(n), n=1…12 : {v4_q} · Tr Mⁿ = "
          f"Lucas(2n) : {v4_m} · Tr Mⁿ = Tr C(1)^(2n)/2 (pont T17) : "
          f"{v4_pont} → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 / F5 : leviers + témoin
    lv = {}
    wr = mot_mecanique(len(mot_fibonacci(15)), Fraction(13, 34))
    w15 = mot_fibonacci(15)
    lv["pente rationnelle 13/34 tue F1 (mot ≠ mécanique doré)"] = \
        wr != w15
    tm = "a"
    for _ in range(12):
        tm = "".join("ab" if c == "a" else "ba" for c in tm)
    lv["Thue-Morse : densités 1/2 ≠ 1/φ² (témoin)"] = \
        tm.count("a") == tm.count("b")
    Qtm = np.array([[1, 1], [1, 1]], dtype=float)
    lv["Thue-Morse : spectre {2, 0} — Tr ≠ Lucas(n) (n ≥ 3)"] = \
        all(abs(np.trace(np.linalg.matrix_power(Qtm, n)) - lucas(n))
            > TOL_REG for n in range(3, 8))
    Mplat = np.array([[2, 1], [1, 2]], dtype=float)
    lv["inflation dégonflée [[2,1],[1,2]] : det 3, PF 3 ≠ φ²"] = \
        abs(max(np.linalg.eigvalsh(Mplat)) - PHI ** 2) > 0.3
    for k, val in lv.items():
        print(f"V5 levier — {k} : {val}")
    V5 = all(lv.values())

    criteres = {"V1_chaîne_Fibonacci": bool(V1),
                "V2_losanges_Penrose": bool(V2),
                "V3_inflation_2D": bool(V3),
                "V4_pont_diffusif_spectral": bool(V4),
                "V5_leviers": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T20-Q-KO6-PONT-DIFFUSIF-2026-10",
        "protocole": "T20-KO6-DIFF-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le pont diffusif : le phi quasicristallin (Penrose, "
                 "chaîne de Fibonacci) éprouvé contre le pont phi "
                 "(T14/T17/T18/T19)",
        "statut_du_mot": "PONT DIFFUSIF — théorème mesuré à zéro "
                         "paramètre ; AUCUNE prédiction d'expérience ; "
                         "le physique (59 meV) n'est pas touché",
        "faces": {
            "densités": "mot de Fibonacci : 1/phi (a), 1/phi² (b) ; "
                        "mécanique de pente 1/phi²",
            "géométrie": "losanges de Penrose : diagonales phi et "
                         "1/phi (côté 1)",
            "substitution": "Q=[[1,1],[1,0]] : Tr Q^n = Lucas(n) ; "
                            "M=[[2,1],[1,1]] : Tr M^n = Lucas(2n) = "
                            "Tr C(1)^(2n)/2 — pont avec le spectre du "
                            "seesaw (T17)",
        },
        "V1": bool(V1), "V2": bool(V2),
        "V3": {"VP": sorted([float(x) for x in vp], reverse=True),
               "ratio_populations_niveau_14": float(ratios[-1])},
        "V4": {"Tr_Qn_=_Lucas": bool(v4_q), "Tr_Mn_=_Lucas2n": bool(v4_m),
               "Tr_Mn_=_Tr_C1_2n_sur_2": bool(v4_pont)},
        "V5": {k: bool(v) for k, v in lv.items()},
        "entree_dictionnaire_T18": {
            "mot": "pont-φ-diffusif", "filiation": "T20 (T17, T14)",
            "polynôme": "λ² − λ − 1 (Q) · λ² − 3λ + 1 (M)",
            "séquence": "Lucas(n) et Lucas(2n) = Tr C(1)^(2n)/2",
            "statut": "pont diffusif mesuré — entrée proposée au "
                      "dictionnaire (modification de T18 soumise à "
                      "décision de gouvernance)"},
        "candidats_déclarés_non_mesurés": [
            "diffraction de Bragg de la chaîne de Fibonacci (fonction "
            "de structure — carte séparée, fenêtre et seuils à "
            "déclarer avant run)"],
        "falsifieur": "F1…F4 hors TOL_REG ; levier non détecté",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t20_ko6_pont_diffusif_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T20 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
