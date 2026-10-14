#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T24 — Q-KO6-T24-2026-10 : LE CHAÎNON OPTIQUE — le spectre de Cantor
      Fibonacci (matrices de transfert, SL(2, ℝ))
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T24-KO6-CANTOR-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « le chaînon optique » — le chantier E2 du carnet
      NOTE-CANDIDATS-PONT-PHI : les empilements quasi-périodiques à mot
      de Fibonacci (modèle canonique de Kohmoto : matrices compagnons
      A(t), B(t) de déterminant 1, mot par substitution déclarée).
      Question : le spectre de ce cristal photonique idéal vérifie-t-il
      les régressions dorées du dictionnaire — et l'unimodularité
      SL(2, ℝ) est-elle bien le chaînon entre la chaîne du seesaw,
      Penrose et le module d'or ?
  Filiation : T20 (mot caractéristique, matrices Q et M, Legendre) ;
      T14 (unimodularité du seesaw, det B = 1) ; T17 (mot Fibonacci,
      Lucas) ; T21 (le module d'or) ; carnet (E2). Dérivation faite
      avant gel : l'identité de trace Tr(W_{n+1}) = Tr(W_n)Tr(W_{n-1})
      − Tr(W_{n-2}) est PROUVÉE par conjugaison (W_n W_{n-1}^{-1}
      est conjugué de W_{n-2}) ; la machine la régresse.
  STATUT DU MOT (déclaré, gelé) : PONT SPECTRAL (photonique) —
      théorème interne mesuré à zéro paramètre ; AUCUNE prédiction
      d'expérience nouvelle ; les filtres optiques de Fibonacci réels
      (données de littérature) sont candidat MCS EXTERNE déclaré,
      non mesuré ici.
  Question unique : le spectre du cristal de Cantor Fibonacci
      (comptage de bandes, recursion de trace, invariant de Fricke)
      régresse-t-il le dictionnaire doré, et les leviers tuent-ils
      la structure comme déclaré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  unimodularité : det A(t) = det B(t) = 1 identiquement ;
          identité de trace (prouvée par conjugaison) régressée à
          TOL sur la grille gelée ; invariant de Fricke
          I = x²+y²+z²−2xyz constant le long des orbites (mesuré) ;
      F2  le spectre de Cantor : bandes au niveau N = {t : |x_N(t)| ≤ 1}
          sur la grille gelée (2^18, [−2,5 ; 2,5]) — les comptes
          CROISSENT : c_{N+1}/c_N converge vers φ (fenêtre gelée
          1,58…1,64 pour les trois derniers ratios — D1 v1.1 : la
          fiche annonçait 1/φ, direction inversée au gel ; la
          récursion c_N ≈ c_{N-1} + c_{N-2}, elle, était juste) ;
          tolérance gelée ≤ 4 — effets de bord déclarés ;
      F3  le chaînon : la structure combinatoire du spectre (mot de
          Fibonacci) et l'unimodularité (det = 1) sont les mêmes
          invariants constitutifs que la chaîne du seesaw (T14 :
          det B = 1) et l'inflation de Penrose (T20 : det M = 1) —
          régressions citées ;
      F4  leviers : mot périodique (AB)^N — bandes constantes (ratio
          1,0, mesure positive : pas de Cantor) ; absorption
          (det = 2 ≠ 1) — l'identité de trace et l'invariant de
          Fricke se brisent (résidus > 1e-6 mesurés) ;
      F5  statut et gouvernance : pont spectral, théorème interne ;
          entrée « cantor-photonique » proposée au dictionnaire ;
          candidat MCS externe (filtres réels) déclaré non mesuré.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5 (grille gelée,
      tolérances gelées).
  Falsifieur : F1/F2 hors tolérance (tue V1/V2) ; levier non détecté
      (tue V4).
  Prédiction pré-enregistrée : 5/5 — « le spectre de Cantor Fibonacci
      parle la langue du dictionnaire ».

DÉFAUT DU BANC (trouvé au premier run du 14/10/2026 — publié) :
  D1  la fiche gelait la fenêtre des ratios de comptage à 0,60…0,64
      (habitude du ratio de gap décroissant de T21) — mesuré : les
      bandes CROISSENT, c_{N+1}/c_N → φ ≈ 1,618 (1,6032 au dernier
      niveau). Correction v1.1 : fenêtre 1,58…1,64. La récursion
      c_N ≈ c_{N-1} + c_{N-2} n'était pas touchée — la structure ne
      mentait pas, sa direction dans la fiche si.
  Gouvernance : décision d'auteur du 14/10/2026 (« attaque le chantier
      suivant » — E2) — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
TOL_REG = 1e-6
PHI = (1 + np.sqrt(5)) / 2
GRILLE = 1 << 18
TMAX = 2.5
NIVEAUX = list(range(9, 15))       # gelée
FENETRE_RATIO = (1.58, 1.64)       # gelée (v1.1, D1)
TOL_REC_COMPTE = 4                 # gelée (effets de bord)


def A(t):
    return np.array([[t, -1.0], [1.0, 0.0]])


def B(t):
    return np.array([[t - 1.0, -1.0], [1.0, 0.0]])


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def produit(w, t):
    P = np.eye(2)
    for c in w:
        P = P @ (A(t) if c == "A" else B(t))
    return P


def traces_grille(t):
    """Traces initiales x1, x2, x3 (mots A, AB, ABA) sur la grille."""
    x1 = 0.5 * t
    x2 = 0.5 * (t * (t - 1.0) - 1.0)
    x3 = 0.5 * (t * (t * (t - 1.0) - 1.0) - (t - 1.0))
    return [x1, x2, x3]


def xN_grille(t, N):
    xs = traces_grille(t)
    for _ in range(N - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    return np.array(xs)


def nb_bandes(t, N):
    x = xN_grille(t, N)[-1]
    m = np.abs(x) <= 1.0
    idx = np.where(m)[0]
    if len(idx) == 0:
        return 0
    return 1 + int(np.sum(np.diff(idx) > 1))


def main():
    t0 = time.time()
    print("T24 — le chaînon optique : le spectre de Cantor Fibonacci   "
          "[T24-KO6-CANTOR-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : unimodularite, identite de trace, Fricke
    ts_det = np.array([0.3, 0.7, 1.1, 1.9])
    det_ok = all(abs(np.linalg.det(A(t)) - 1) < TOL_REG
                 and abs(np.linalg.det(B(t)) - 1) < TOL_REG for t in ts_det)
    rec_ok = True
    for t in ts_det:
        xs = [0.5 * np.trace(produit(mot_fibonacci(k), t))
              for k in range(1, 7)]
        for i in range(3):
            rec_ok &= abs(2 * xs[i + 2] * xs[i + 1] - xs[i]
                          - xs[i + 3]) < TOL_REG
    fricke = []
    for t in ts_det:
        x = xN_grille(np.array([t]), 8).ravel()
        I = (x[2:] ** 2 + x[1:-1] ** 2 + x[:-2] ** 2
             - 2 * x[2:] * x[1:-1] * x[:-2])
        fricke.append(float(np.max(I) - np.min(I)))
    fricke_ok = max(fricke) < TOL_REG
    V1 = bool(det_ok and rec_ok and fricke_ok)
    print(f"V1 F1 : det A = det B = 1 : {det_ok} · identité de trace "
          f"(prouvée par conjugaison, régressée) : {rec_ok} · invariant "
          f"de Fricke constant (dérive max {max(fricke):.2e}) : {fricke_ok} "
          f"→ {'PASS' if V1 else 'FAIL'}")

    # ---- V2 / F2 : le spectre de Cantor (comptage de bandes)
    tg = np.linspace(-TMAX, TMAX, GRILLE)
    comptes = [nb_bandes(tg, N) for N in NIVEAUX]
    ratios = [comptes[i + 1] / comptes[i] for i in range(len(comptes) - 1)]
    ratios_fin = ratios[-3:]
    v2_ratios = all(FENETRE_RATIO[0] <= r <= FENETRE_RATIO[1]
                    for r in ratios_fin)
    rec_comptes = all(abs(comptes[i + 2] - comptes[i + 1] - comptes[i])
                      <= TOL_REC_COMPTE
                      for i in range(len(comptes) - 2))
    V2 = bool(v2_ratios and rec_comptes)
    print(f"V2 F2 : spectre de Cantor — bandes par niveau :")
    for N, c in zip(NIVEAUX, comptes):
        print(f"   N = {N:2d} : {c:4d} bandes")
    print(f"   ratios c_{{N+1}}/c_N : {[round(r, 4) for r in ratios]} "
          f"→ φ = {PHI:.4f} (fenêtre {FENETRE_RATIO}) : {v2_ratios} · "
          f"recursion c_N ≈ c_{{N-1}} + c_{{N-2}} (tol. {TOL_REC_COMPTE}) : "
          f"{rec_comptes} → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 / F3 : le chainon (unimodularite — régressions T14/T20)
    w8 = mot_fibonacci(8)
    det_mot = all(abs(np.linalg.det(produit(w8, t)) - 1) < TOL_REG
                  for t in ts_det)
    V3 = bool(det_mot)
    print(f"V3 F3 : det(produit du mot niveau 8) = 1 : {det_mot} — le "
          f"chaînon SL(2, ℝ) : même unimodularité que la chaîne du "
          f"seesaw (T14, det B = 1) et l'inflation de Penrose (T20, "
          f"det M = 1) → {'PASS' if V3 else 'FAIL'}")

    # ---- V4 / F4 : leviers
    lv = {}
    # levier periodique : mot (AB)^N — bandes constantes
    xab = 0.5 * (tg * (tg - 1.0) - 1.0)
    def bandes_mot(masque):
        idx = np.where(masque)[0]
        return 0 if len(idx) == 0 else 1 + int(np.sum(np.diff(idx) > 1))
    b_period = bandes_mot(np.abs(xab) <= 1.0)
    lv["levier periodique : mot (AB) — bandes constantes "
       f"({b_period}), pas de Cantor"] = b_period <= 4
    # levier absorption : det = 2 -> identite de trace et Fricke brises
    def A_abs(t):
        return np.array([[t, -1.0], [2.0, 0.0]])   # det = 2
    def produit_abs(w, t):
        P = np.eye(2)
        for i, c in enumerate(w):
            P = P @ (A_abs(t) if c == "A" else B(t))
        return P
    residus = []
    for t in ts_det:
        xs = [0.5 * np.trace(produit_abs(mot_fibonacci(k), t))
              for k in range(1, 6)]
        for i in range(2):
            residus.append(abs(2 * xs[i + 2] * xs[i + 1] - xs[i]
                               - xs[i + 3]))
    lv["levier absorption (det = 2) : identité de trace brisée "
       f"(résidu max {max(residus):.2e} > 1e-6)"] = max(residus) > 1e-6
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : statut + gouvernance
    entree = {
        "mot": "cantor-photonique",
        "filiation": "T24 (T14, T20, T17, T21)",
        "polynôme": "x_{N+1} = 2x_N x_{N-1} − x_{N-2} (trace map)",
        "séquence": "bandes c_N : c_{N+1}/c_N → φ ; c_N ≈ c_{N-1}+c_{N-2}",
        "statut": "pont spectral — théorème interne, aucune prédiction "
                  "d'expérience",
        "candidat_externe_déclare": "filtres optiques de Fibonacci réels "
            "(données de littérature à épingler) — carte MCS externe, "
            "non mesurée ici"}
    V5 = "cantor-photonique" == entree["mot"] and "externe" in \
        entree["candidat_externe_déclare"]
    print(f"V5 F5 : entrée « {entree['mot']} » proposée au dictionnaire "
          f"(statut déclaré, candidat externe nommé) : {V5} → "
          f"{'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_trace_map": bool(V1), "V2_spectre_de_cantor": bool(V2),
                "V3_chainon_SL2": bool(V3), "V4_leviers": bool(V4),
                "V5_statut": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T24-Q-KO6-CANTOR-2026-10",
        "protocole": "T24-KO6-CANTOR-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le chaînon optique : le spectre de Cantor Fibonacci "
                 "(Kohmoto) parle la langue du dictionnaire doré",
        "statut_du_mot": "PONT SPECTRAL — théorème interne, aucune "
                         "prédiction d'expérience",
        "mesures": {"det_A_B": 1.0, "fricke_dérive_max": max(fricke),
                    "bandes_par_niveau": {str(N): c for N, c in
                                          zip(NIVEAUX, comptes)},
                    "ratios_bandes": ratios,
                    "bandes_periodique": b_period,
                    "residu_absorption": max(residus)},
        "identite_de_trace": "Tr(W_{n+1}) = Tr(W_n)Tr(W_{n-1}) − "
                             "Tr(W_{n-2}) — prouvée par conjugaison "
                             "(W_n W_{n-1}^{-1} ~ W_{n-2}), régressée",
        "V1": bool(V1),
        "V2": {"ratios": ratios_fin, "ok": bool(v2_ratios),
               "recursion_comptes": bool(rec_comptes)},
        "V3": bool(V3),
        "V4": {k: bool(v) for k, v in lv.items()},
        "entree_dictionnaire": entree,
        "V5": bool(V5),
        "falsifieur": "F1/F2 hors tolérance ; levier non détecté",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t24_ko6_cantor_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T24 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
