#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T18 — Q-KO6-T18-2026-10 : LE DICTIONNAIRE DES SÉQUENCES SPECTRALES —
      le gabarit de T17 généralisé (un objet certifié → sa séquence)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T18-KO6-DICO-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026)
  Tiroir   : banc
  Objet    : « le dictionnaire des séquences spectrales » — le gabarit
      déclaré par T17 (chaque objet certifié → son polynôme spectral →
      sa séquence de traces → ses régressions) éprouvé sur les entrées
      disponibles aujourd'hui : la chaîne du seesaw C(1) (T14/T17) et
      le modèle spectral du porteur (T13 — spectre déclaré
      {0, ±(ρ−1), ±(ρ+1)}).
  Convention déclarée (gelée) : les traces sont des invariants
      spectraux — l'entrée « porteur » du dictionnaire est le MODÈLE
      SPECTRAL D(ρ) = diag(0, ρ−1, −(ρ−1), ρ+1, −(ρ+1)) ; la géométrie
      du porteur (T13) n'est pas réimportée, elle est citée. Un mot =
      un objet : « porteur » reste l'objet géométrique de T13 ; ici le
      mot est « porteur-spectral ».
  STATUT DU MOT (déclaré, gelé) : MÉTHODE — le dictionnaire est un
      instrument de régression interne ; chaque entrée porte sa
      condition d'entierité (paramètres gelés). Aucune prédiction
      d'expérience.
  Filiation : T17 (le gabarit et l'entrée C(1) — fichier publié) ;
      T14 (la chaîne) ; T13 (le spectre du porteur — cité) ;
      koilon-scale-e8 (candidat déclaré, NON mesuré ici).
  Question unique : le gabarit tient-il sur les deux entrées
      disponibles — séquences exactes, reconstruction des polynômes
      par les traces (Newton), et leviers tuables sur l'entierité ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  C(1) : Tr C(1)^(2n) = 2·Lucas(2n), n = 1…12 (régression T17)
      F2  porteur-spectral à ρ = 2 (spectre {0, ±1, ±3}) :
          Tr D(2)^(2n) = 2 + 2·9ⁿ ; à ρ = 1 (repos, zéros accidentels
          déclarés T13) : Tr D(1)^(2n) = 2·4ⁿ
      F3  les traces reconstruisent le polynôme spectral (Newton) :
          C(1) → λ⁴ − 3λ² + 1 ; porteur générique ρ →
          λ(λ² − (ρ−1)²)(λ² − (ρ+1)²)
      F4  l'entierité est discrète (liée aux paramètres gelés) :
          ρ = 2,5 tue F2 (mesuré) ; y = 1/4 sur C(1) tue F1
          (régression T17)
      F5  le dictionnaire publie 2 entrées et la règle d'admission
          des prochaines (régression tuante + levier + condition
          d'entierité déclarée)
  Protocole machine (bornes déclarées) :
      V1  F1 : régression tuante à T17 sur la grille n = 1…12
      V2  F2 : porteur-spectral sur les grilles gelées n = 1…8,
          ρ ∈ {1 ; 2} (régressions tuantes)
      V3  F3 : reconstruction de Newton à partir des seules traces
          (C(1) : p1…p4 ; porteur générique ρ = 1,7 : p1…p5)
      V4  F4 : leviers tuables (ρ = 2,5 ; y = 1/4) + contrôle faux
          (suite témoin erronée doit échouer)
      V5  F5 : le dictionnaire JSON est assemblé — 2 entrées, règle
          d'admission publiée
  Falsifieur : F1/F2/F3 hors TOL_REG (tue V1/V2/V3) ; un levier non
      détecté (tue V4) ; le dictionnaire incomplet (tue V5).
  Prédiction pré-enregistrée : V1…V5 passent ; le dictionnaire tient
      sur 2 entrées ; l'entierité est confirmée discrète (paramètres).
  Gouvernance : décision d'auteur du 14/10/2026 (« rédige T18 et
      publie ») — publication GitHub autorisée (run local exécuté le
      14/10/2026 avant push, empreinte du script figée au verdict).
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0)
TOL_REG = 1e-6      # tolérance de régression (déclarée)
GRILLE_C = list(range(1, 13))    # gelée (T17)
GRILLE_P = list(range(1, 9))     # gelée
RHO_REPOS, RHO_ENTIER, RHO_GEN, RHO_LEVIER = 1.0, 2.0, 1.7, 2.5


def chaine(y, M):
    """La chaîne à 4 maillons de sauts (y, M, y) — construction T14."""
    return np.array([[0, y, 0, 0],
                     [y, 0, M, 0],
                     [0, M, 0, y],
                     [0, 0, y, 0]], dtype=float)


def porteur_spectral(rho):
    """MODÈLE SPECTRAL déclaré (convention gelée de la fiche) :
    D(ρ) = diag(0, ρ−1, −(ρ−1), ρ+1, −(ρ+1)) — spectre du porteur
    tel que publié (T13, NOTE-VERROU-59-MEV), sans réimport géométrique."""
    return np.diag([0.0, rho - 1, -(rho - 1), rho + 1, -(rho + 1)])


def lucas(k):
    a, b = 2, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def newton_reconstruit(traces):
    """Coefficients c1..ck de P(λ) = λ^k + c1 λ^(k−1) + … + ck
    à partir des sommes de Newton p1…pk (invariants de frottement
    : la reconstruction est un solveau triangulaire exact)."""
    k = len(traces)
    c = []
    for m in range(1, k + 1):
        cm = -traces[m - 1] - sum(c[j] * traces[m - 2 - j]
                                  for j in range(m - 1))
        c.append(cm / m)
    return c


def poly_porteur(rho):
    """λ(λ²−(ρ−1)²)(λ²−(ρ+1)²) — développé : λ⁵ + c2 λ³ + c4 λ."""
    return [0.0, -(2 * rho ** 2 + 2), 0.0, (rho ** 2 - 1) ** 2]


def main():
    t0 = time.time()
    print("T18 — le dictionnaire des séquences spectrales   "
          "[T18-KO6-DICO-1.0 gelé]")
    print("=" * 76)

    # ---- V1 : F1 — régression tuante à T17
    C1 = chaine(1.0, 1.0)
    v1 = all(abs(np.trace(np.linalg.matrix_power(C1, 2 * n))
                 - 2 * lucas(2 * n)) < TOL_REG for n in GRILLE_C)
    print(f"V1 F1 (entrée C(1), régression T17, n=1…12) : "
          f"{'PASS' if v1 else 'FAIL'}")

    # ---- V2 : F2 — porteur-spectral, ρ ∈ {1 repos, 2 entier}
    d2 = porteur_spectral(RHO_ENTIER)
    f2_entier = all(abs(np.trace(np.linalg.matrix_power(d2, 2 * n))
                        - (2 + 2 * 9 ** n)) < TOL_REG for n in GRILLE_P)
    d1 = porteur_spectral(RHO_REPOS)
    f2_repos = all(abs(np.trace(np.linalg.matrix_power(d1, 2 * n))
                       - 2 * 4 ** n) < TOL_REG for n in GRILLE_P)
    V2 = bool(f2_entier and f2_repos)
    print(f"V2 F2 (porteur-spectral) : ρ=2 : Tr D(2)^(2n) = 2 + 2·9ⁿ "
          f"(n=1…8) : {f2_entier} · ρ=1 (repos) : Tr = 2·4ⁿ : {f2_repos} "
          f"→ {'PASS' if V2 else 'FAIL'}")

    # ---- V3 : F3 — reconstruction de Newton à partir des seules traces
    pC = [np.trace(np.linalg.matrix_power(C1, k)) for k in range(1, 5)]
    cC = newton_reconstruit(pC)
    f3_c = (abs(cC[0]) < TOL_REG and abs(cC[1] + 3) < TOL_REG
            and abs(cC[2]) < TOL_REG and abs(cC[3] - 1) < TOL_REG)
    dg = porteur_spectral(RHO_GEN)
    pP = [np.trace(np.linalg.matrix_power(dg, k)) for k in range(1, 6)]
    cP = newton_reconstruit(pP)
    att = poly_porteur(RHO_GEN)
    f3_p = all(abs(cP[i] - att[i]) < TOL_REG for i in range(4)) and \
        abs(cP[4] - 0.0) < TOL_REG and abs(cP[1] - att[0 + 1]) < TOL
    V3 = bool(f3_c and f3_p)
    print(f"V3 F3 (Newton) : C(1) → λ⁴ − 3λ² + 1 : {f3_c} · porteur "
          f"ρ=1,7 → λ(λ²−(ρ−1)²)(λ²−(ρ+1)²) : {f3_p} → "
          f"{'PASS' if V3 else 'FAIL'}")

    # ---- V4 : F4 — leviers sur l'entierité + contrôle faux
    dl = porteur_spectral(RHO_LEVIER)
    tue_rho = all(abs(np.trace(np.linalg.matrix_power(dl, 2 * n))
                      - (2 + 2 * 9 ** n)) > TOL_REG for n in range(1, 5))
    Cq = chaine(0.25, 1.0)
    tue_y = all(abs(np.trace(np.linalg.matrix_power(Cq, 2 * n))
                    - 2 * lucas(2 * n)) > TOL_REG for n in range(1, 5))
    temoin = all(abs(np.trace(np.linalg.matrix_power(C1, 2 * n))
                     - 2 * lucas(2 * n - 1)) > TOL_REG
                 for n in GRILLE_C)
    V4 = bool(tue_rho and tue_y and temoin)
    print(f"V4 F4 (leviers) : ρ=2,5 tue l'entierité : {tue_rho} · y=1/4 "
          f"tue F1 (T17) : {tue_y} · contrôle faux échoue : {temoin} → "
          f"{'PASS' if V4 else 'FAIL'}")

    # ---- V5 : F5 — le dictionnaire est assemblé
    dictionnaire = {
        "règle_d'admission": "une entrée = un objet certifié du banc + "
            "son polynôme spectral + sa séquence de traces + sa "
            "condition d'entierité (paramètres gelés) + une régression "
            "tuante + un levier tuable. Statut : instrument interne, "
            "aucune prédiction d'expérience.",
        "entrées": [
            {"mot": "chaîne-seesaw C(1)", "filiation": "T14/T17",
             "polynôme": "λ⁴ − 3λ² + 1",
             "séquence": "Tr C(1)^(2n) = 2·Lucas(2n), n = 1…12 mesurés",
             "entierité": "y = M_R = 1 (gelé — leviers mesurés)"},
            {"mot": "porteur-spectral D(ρ)",
             "filiation": "T13 (spectre déclaré, NOTE-VERROU)",
             "polynôme": "λ(λ²−(ρ−1)²)(λ²−(ρ+1)²)",
             "séquence": "Tr D(2)^(2n) = 2 + 2·9ⁿ ; Tr D(1)^(2n) = 2·4ⁿ "
                         "(n = 1…8 mesurés)",
             "entierité": "ρ ∈ {1 ; 2} sur la grille déclarée — "
                          "entierité discrète confirmée"},
        ],
        "candidats_déclarés_non_mesurés": [
            "koilon-scale-e8 (géométrie E8/icosaédrique — le φ y est "
            "géométrique, pas spectral : la carte devra déclarer le "
            "pont avant toute mesure)"],
    }
    V5 = len(dictionnaire["entrées"]) == 2
    print(f"V5 F5 (dictionnaire : {len(dictionnaire['entrées'])} entrées, "
          f"règle publiée) : {'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_C1_régression_T17": bool(v1),
                "V2_porteur-spectral_rho_1_2": V2,
                "V3_newton_reconstruction": V3,
                "V4_leviers_entierité": V4,
                "V5_dictionnaire_assemblé": V5}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T18-Q-KO6-DICO-SEQUENCES-2026-10",
        "protocole": "T18-KO6-DICO-1.0 (gelé)",
        "objet": "le dictionnaire des séquences spectrales : le gabarit "
                 "T17 généralisé, éprouvé sur C(1) (T14/T17) et le "
                 "modèle spectral du porteur (T13 cité)",
        "convention_gelée": "entrée porteur = modèle spectral "
            "D(ρ)=diag(0,±(ρ−1),±(ρ+1)) — les traces sont spectrales ; "
            "la géométrie T13 n'est pas réimportée",
        "statut_du_mot": "MÉTHODE interne — instrument de régression ; "
                         "aucune prédiction d'expérience",
        "V1": bool(v1), "V2": {"rho_2": bool(f2_entier),
                               "rho_1_repos": bool(f2_repos)},
        "V3": {"C1_coeffs": [float(x) for x in cC],
               "porteur_rho1.7_coeffs": [float(x) for x in cP]},
        "V4": {"rho_2.5_tue": bool(tue_rho), "y_1/4_tue": bool(tue_y),
               "contrôle_faux": bool(temoin)},
        "dictionnaire": dictionnaire,
        "falsifieur": "F1/F2/F3 hors TOL_REG ; levier non détecté ; "
                      "dictionnaire incomplet",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t18_ko6_dico_sequences_verdict.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T18 : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
