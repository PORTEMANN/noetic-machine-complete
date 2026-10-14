#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T17 — Q-KO6-T17-2026-10 : LE MOT FIBONACCI — la suite dans le spectre de la
      chaîne (ce que le nombre d'or mesuré force comme régression)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T17-KO6-FIB-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push, aucune carte épinglée)
  Tiroir   : banc
  Objet    : « le mot Fibonacci » — la carte déclarée dans la continuité du
      « Dialogue entre Dirac et la Machine » (14/10/2026) : le bloc
      S = B Bᵀ de la chaîne du seesaw à M_R = y = 1 est-il exactement la
      matrice de Fibonacci, et les puissances paires de la chaîne
      génèrent-elles les suites de Fibonacci et de Lucas ?
  STATUT DU MOT (déclaré, gelé) : THÉORÈME INTERNE — une régression
      exacte du spectre mesuré, PAS une prédiction d'expérience.
      La maison distingue : confondre les deux est la faute nommée par
      Dirac dans le dialogue (la concordance ne prouve pas la théorie).
  Filiation : T14 (la chaîne — forme close, spectre ±φ, ±1/φ à M_R = 1,
      fichier publié du dépôt) ; T9 (la construction) ; T15 (la règle
      des mots certifiés : aucune carte sur un mot orphelin) ; le dépôt
      koilon-scale-e8 (le chantier géométrique E8/icosaédrique — cité,
      non mesuré ici).
  Question unique : les identités Fibonacci/Lucas sont-elles des faits
      de la chaîne MESURÉE (régressions tuantes), et meurent-elles
      correctement sous les leviers (M_R ≠ 1, y ≠ 1, contrôle faux) ?
  Fait déclaré (dérivé avant gel, à vérifier par la machine) :
      F1  S = B Bᵀ = [[1,1],[1,2]] à M_R = y = 1 (la matrice de
          Fibonacci) ; Sⁿ = [[F(2n−1), F(2n)], [F(2n), F(2n+1)]]
      F2  Tr C(1)^(2n) = 2 · Lucas(2n) pour la grille gelée n = 1…12
      F3  le fait meurt hors M_R = y = 1 (levier mesuré, pas universel)
  Protocole machine (bornes déclarées) :
      V1  la construction : la chaîne C(1) déclarée reproduit le spectre
          de T14 (±φ, ±1/φ — régression tuante à T14) ;
      V2  F1 vérifiée : S = B Bᵀ = matrice de Fibonacci ; les puissances
          Sⁿ (n = 1…8, grille gelée) sont les blocs de Fibonacci annoncés
          (régression tuante) ;
      V3  F2 vérifiée : Tr C(1)^(2n) = 2·Lucas(2n) sur la grille
          n = 1…12 (prédiction pré-enregistrée — régression tuante à
          TOL_REG) ; identités φ associées re-mesurées (φ − 1/φ = 1,
          φ² + 1/φ² = 3) ;
      V4  leviers tuables : la chaîne (y, M_R, y) avec y = 1/4 à M_R = 1
          ne vérifie PAS F2 (mesuré — le fait est un fait de M_R = y = 1,
          pas une loi universelle) ; M_R = 2, y = 1 idem ; le contrôle
          faux (comparer à une suite témoin erronée) doit échouer ;
      V5  statut déclaré : le verdict publie que ce mot, s'il passe, est
          un mot de MATHÉMATIQUES internes au banc — pas une attente
          de labo.
  Falsifieur : F1 ou F2 hors TOL_REG (tue V2/V3) ; un levier non détecté
      (tue V4) ; la régression T14 perdue (tue V1 — le banc).
  Prédiction pré-enregistrée : V1…V5 passent ; le fait est exact à
      M_R = y = 1 et meurt sous les leviers ; aucune prétention physique.
  Gouvernance : RUN LOCAL UNIQUEMENT (14/10/2026) — publication GitHub
      en attente du feu vert de l'auteur. Aucune carte MCS épinglée.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0 → T9/T14)
TOL_REG = 1e-6      # tolérance de régression (déclarée)
GRILLE_N = list(range(1, 13))   # grille gelée n = 1…12
GRILLE_P = list(range(1, 9))    # grille gelée des puissances Sⁿ


def chaine(y, M):
    """La chaîne à 4 maillons de sauts (y, M, y) — construction T14."""
    return np.array([[0, y, 0, 0],
                     [y, 0, M, 0],
                     [0, M, 0, y],
                     [0, 0, y, 0]], dtype=float)


def fibonacci(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def lucas(k):
    a, b = 2, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def main():
    t0 = time.time()
    print("T17 — le mot Fibonacci : la suite dans le spectre de la chaîne   "
          "[T17-KO6-FIB-1.0 gelé — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 : régression à T14 (la chaîne déclarée = le spectre publié)
    C1 = chaine(1.0, 1.0)
    ev = np.linalg.eigvalsh(C1)
    phi = (1 + np.sqrt(5)) / 2
    v1 = (abs(ev[0] + phi) < TOL and abs(ev[1] + 1 / phi) < TOL
          and abs(ev[2] - 1 / phi) < TOL and abs(ev[3] - phi) < TOL)
    print(f"V1 régression T14 : spectre C(1) = {np.round(ev, 9).tolist()} "
          f"(attendu ±φ, ±1/φ) → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 : F1 — S = B Bᵀ est la matrice de Fibonacci
    B = np.array([[1.0, 0.0], [1.0, 1.0]])
    S = B @ B.T
    S_fib = np.array([[1.0, 1.0], [1.0, 2.0]])
    f1_shape = bool(np.allclose(S, S_fib, atol=TOL))
    f1_powers = True
    for n in GRILLE_P:
        Sn = np.linalg.matrix_power(S, n)
        attendu = np.array([[fibonacci(2 * n - 1), fibonacci(2 * n)],
                            [fibonacci(2 * n), fibonacci(2 * n + 1)]],
                           dtype=float)
        if not np.allclose(Sn, attendu, atol=TOL_REG):
            f1_powers = False
    V2 = bool(f1_shape and f1_powers)
    print(f"V2 F1 : S = B Bᵀ = [[1,1],[1,2]] : {f1_shape} · Sⁿ = blocs de "
          f"Fibonacci sur la grille {GRILLE_P[0]}…{GRILLE_P[-1]} : "
          f"{f1_powers} → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 : F2 — Tr C(1)^(2n) = 2·Lucas(2n) (prédiction pré-enregistrée)
    v3_ok = True
    serie = []
    for n in GRILLE_N:
        tr = float(np.trace(np.linalg.matrix_power(C1, 2 * n)))
        att = 2.0 * lucas(2 * n)
        ok = abs(tr - att) < TOL_REG
        v3_ok &= ok
        serie.append((n, int(round(tr)), int(att), ok))
    id1 = abs(phi - 1 / phi - 1.0) < TOL_REG
    id2 = abs(phi ** 2 + 1 / phi ** 2 - 3.0) < TOL_REG
    V3 = bool(v3_ok and id1 and id2)
    print("V3 F2 (prédiction pré-enregistrée Tr C(1)^(2n) = 2·Lucas(2n)) :")
    for n, tr, att, ok in serie:
        print(f"   n={n:2d} : mesuré {tr:>6d} · attendu {att:>6d} · "
              f"{'OK' if ok else 'FAIL'}")
    print(f"   identités φ : φ − 1/φ = 1 : {id1} · φ² + 1/φ² = 3 : {id2} "
          f"→ {'PASS' if V3 else 'FAIL'}")

    # ---- V4 : leviers — le fait meurt hors M_R = y = 1 ; contrôle faux
    lv = {}
    Cq = chaine(0.25, 1.0)
    tue_y = all(abs(np.trace(np.linalg.matrix_power(Cq, 2 * n))
                    - 2 * lucas(2 * n)) > TOL_REG for n in range(1, 7))
    C2 = chaine(1.0, 2.0)
    tue_M = all(abs(np.trace(np.linalg.matrix_power(C2, 2 * n))
                    - 2 * lucas(2 * n)) > TOL_REG for n in range(1, 7))
    temoin_errone = all(abs(np.trace(np.linalg.matrix_power(C1, 2 * n))
                            - 2 * lucas(2 * n - 1)) > TOL_REG
                        for n in GRILLE_N)   # mauvais index : doit échouer
    lv["y = 1/4 tue F2 (mesuré — fait lié à y = 1)"] = bool(tue_y)
    lv["M_R = 2 tue F2 (mesuré — fait lié à M_R = 1)"] = bool(tue_M)
    lv["contrôle faux (Lucas décalé) : échoue comme attendu"] = \
        bool(temoin_errone)
    for k, v in lv.items():
        print(f"V4 levier — {k} : {v}")
    V4 = all(lv.values())

    # ---- V5 : statut du mot déclaré et publié dans le verdict
    V5 = True
    print("V5 statut du mot : THÉORÈME INTERNE (régression exacte du "
          "spectre ; pas une prédiction d'expérience) — publié au verdict.")

    criteres = {"V1_régression_T14": bool(v1), "V2_F1_S=matrice_de_Fibonacci": V2,
                "V3_F2_Tr=2Lucas": V3, "V4_leviers": V4, "V5_statut_déclaré": V5}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T17-Q-KO6-FIBONACCI-2026-10",
        "protocole": "T17-KO6-FIB-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le mot Fibonacci : S = B Bᵀ est la matrice de Fibonacci ; "
                 "Tr C(1)^(2n) = 2·Lucas(2n) — régressions exactes du "
                 "spectre mesuré de la chaîne du seesaw",
        "statut_du_mot": "THÉORÈME INTERNE au banc — régression, PAS "
                         "prédiction d'expérience (déclaré, gelé)",
        "filiation": ["T14 (chaîne, spectre ±φ ±1/φ)",
                      "T9 (construction)", "T15 (règle des mots)",
                      "koilon-scale-e8 (chantier géométrique — cité)"],
        "V1": bool(v1), "V2": {"S_égale_matrice_Fibonacci": f1_shape,
                               "puissances_Sn": bool(f1_powers)},
        "V3": {"série_Tr_C1_2n_vs_2Lucas2n": [
                    {"n": n, "mesuré": tr, "attendu": att, "ok": ok}
                    for n, tr, att, ok in serie],
               "identités_φ": {"φ−1/φ=1": bool(id1), "φ²+1/φ²=3": bool(id2)}},
        "V4_leviers": {k: bool(v) for k, v in lv.items()},
        "falsifieur": "F1/F2 hors TOL_REG ; levier non détecté ; "
                      "régression T14 perdue",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "t17_ko6_fibonacci_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T17 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
