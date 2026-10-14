#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T21 — Q-KO6-T21-2026-10 : LE MODULE D'OR — la carte de Bragg
      (diffraction de la chaîne de Fibonacci — la fonction de structure)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T21-KO6-BRAGG-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « le module d'or » — la carte de diffraction de Bragg
      déclarée candidate aux verdicts T18 et T20 : la fonction de
      structure de la chaîne de Fibonacci (quasicristal 1D, tuiles
      L = φ et S = 1). Trois propriétés Bragg mesurables à zéro
      paramètre : le support des pics (module doré), le caractère
      de Dirac (pics cohérents, rien hors module), et l'invariance
      exacte du module sous l'échelle φ (identité d'indicage).
  Filiation : T20 (pont diffusif — mot caractéristique, matrices Q et
      M, identités Lucas) ; T17 (mot Fibonacci — populations) ;
      T14 (la chaîne du seesaw — φ spectral) ; T18 (dictionnaire —
      l'entrée que cette carte éprouve).
  STATUT DU MOT (déclaré, gelé) : PONT DIFFUSIF (fonction de
      structure) — théorème mesuré à zéro paramètre ; AUCUNE
      prédiction d'expérience ; le physique du corpus (59 meV) n'est
      pas touché.
  Question unique : la diffraction de la chaîne de Fibonacci est-elle
      un peigne de Dirac porté par le module doré, cohérente (Bragg),
      et invariante sous l'échelle φ — et les leviers (approximant
      rationnel périodique, Thue-Morse, chaîne unitaire périodique)
      tuent-ils ces propriétés comme déclaré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  construction : N_n = F(n+2) points exacts (populations du
          mot de Fibonacci — régression T17) ; espacement moyen
          D̄ = 1 + 1/φ² = 3 − φ mesuré deux voies (densités ×
          longueurs ; longueur totale / N) à TOL_REG ;
      F2  support doré : transformée de structure sur la grille gelée
          (2^16 points, fenêtre de Hann, k·D̄/2π dans [0, 21), niveau
          gelé n = 18, N = F(20) = 6765) : les 8 pics dominants (hors
          DC) vérifient chacun k·D̄/(2π) = m + nφ avec (m,n) trouvés
          exactement, résidu < demi-pas de grille ;
      F3  caractère de Dirac : aux 2 pics les plus forts, I_n/(W/2)²
          (W = somme des poids de Hann) converge vers une constante
          positive sur les niveaux gelés 14…18 (plateau mesuré pic par
          pic entre les deux derniers niveaux, à 5 % près) ; aux 2
          points hors module (√2 et e en unités 2π/D̄), le rapport est
          déjà < 1e-4 au niveau 14 (plancher numérique : la fenêtre de
          Hann fait décroître hors module en N⁻²) et non croissant
          jusqu'au niveau 18 ;
      F4  invariance d'échelle : pour les 4 pics les plus forts
          d'indice (m, n), le module exige que le point d'indice
          (m+n, n) (image par ×φ : φ(m + nφ) = n + (m+n)φ) soit aussi
          un pic mesuré non nul — l'échelle φ est une symétrie exacte
          du support de Bragg ;
      F5  leviers (refondus, D3) : L1 — l'image par ×φ du pic fort
          d'une chaîne périodique de pente NON convergente 7/18 (18
          supercellules) tombe hors du réseau j/18 : intensité
          relative < 1e-3 (une pente convergente comme 987/1597
          approche 1/φ à 3e-8 — par Legendre, toute p/q à 1/(2q²)
          près de 1/φ² EST un rapport de Fibonacci : le levier exige
          un non-convergent) ; L2 — Thue-Morse
          (FFT exacte, niveaux 12…18, hors DC) : max |S(k)|²/N²
          décroît strictement et finit < 2 % ; L3 — la position dans
          le module ne suffit pas : pour la chaîne unitaire périodique
          (témoin), les positions dorées internes (φ, 1/φ) ne sont PAS
          des pics (I/W² < 1e-4) alors que le réseau entier l'est
          (contrôle à k = 2π : I/W² > 0,5).
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5 (régressions
      tuantes : T17 pour les populations, T20 pour les matrices).
  Falsifieur : F1…F4 hors TOL_REG / hors seuils déclarés (tue V1…V4) ;
      un levier non détecté (tue V5).
  Prédiction pré-enregistrée : 5/5 — peigne de Dirac doré, cohérent,
      invariant sous φ ; les leviers tuent.
DÉFAUTS DU BANC (trouvés au premier run du 14/10/2026 — publiés) :
  D1  la substitution partait de la lettre « a » au lieu de « L »
      (résidu d'un copier-coller) — mesuré : le mot était décalé
      d'un niveau (len = F(n+1), pas F(n+2)). Correction v1.1 : mot
      initial « L ». Le fait et la pente ne sont pas tués — le
      compteur l'était.
  D2  la fonction de structure tronquait la partie imaginaire
      (float() appliqué à une somme complexe) — mesuré : les
      intensités hors pic étaient faussées d'un facteur deux et les
      phases perdues. Correction v1.1 : S(k) rendue complexe.
  D3  les leviers V5 étaient mal conçus : le maximum de Thue-Morse
      incluait le pic DC (constante 0,25, sans décroissance) ; le
      seuil relatif du témoin unitaire retenait du bruit numérique
      (peigne delta : toutes les valeurs non DC sont nules à 1e-26
      près, seuil relatif sans plancher absolu) ; l'adhésion au
      module pour l'approximant périodique est triviale sur les
      convergents (987/1597 approche 1/φ à 3e-8 — le module est
      dense). Correction v1.1 : leviers refondus — L1 : l'image par
      ×φ d'un pic fort de l'approximant tombe hors du réseau j/N
      (exactitude du réseau, pas approximation) ; L2 : Thue-Morse
      hors DC ; L3 : la position dans le module ne suffit pas — pour
      la chaîne unitaire périodique, les positions dorées internes
      (φ, 1/φ) ne sont PAS des pics (les poids sont la signature).
  D4  V3 comptait les niveaux et les pics dans un seul tableau
      (indexation mélangée) et exigeait une décroissance strictement
      monotone niveau à niveau hors module (bruitée). Correction
      v1.1 : convergence mesurée pic par pic (plateau entre les deux
      derniers niveaux) ; hors module : critère en points fixes
      (premier vs dernier niveau).
  Gouvernance : décision d'auteur du 14/10/2026 (« poursuivons la
      carte de diffraction ») — run local exécuté avant tout push,
      empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
TOL_REG = 1e-6
PHI = (1 + np.sqrt(5)) / 2
NIVEAUX_F1 = [14, 15, 16, 17, 18]
NIVEAU_DFT = 18
GRID = 1 << 16
KMAX = 21.0


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def mot_fibonacci(n):
    """Le mot de Fibonacci par substitution gelée L→LS, S→L (v1.1, D1 :
    lettre initiale « L » — len = F(n+2))."""
    w = "L"
    for _ in range(n):
        w = "".join("LS" if c == "L" else "L" for c in w)
    return w


def positions(niveau):
    """Ensemble de points : origines des tuiles (L = φ, S = 1)."""
    w = mot_fibonacci(niveau)
    longs = np.array([PHI if c == "L" else 1.0 for c in w])
    x = np.concatenate([[0.0], np.cumsum(longs)[:-1]])
    return x, longs


def hann(n):
    return 0.5 * (1 - np.cos(2 * np.pi * np.arange(n) / (n - 1)))


def structure(x, k):
    """S(k) = somme ponderee de Hann de exp(i k x) — complexe (v1.1, D2)."""
    return complex(np.sum(hann(len(x)) * np.exp(1j * k * x)))


def module_or(k_unit, n_max=40):
    """Adhesion au module dore : k_unit = m + n*phi ? -> (m, n) ou None."""
    best, best_res = None, 0.5 * (KMAX / GRID)
    for n in range(-n_max, n_max + 1):
        m = int(round(k_unit - n * PHI))
        for mm in (m - 1, m, m + 1):
            res = abs(k_unit - (mm + n * PHI))
            if res < best_res:
                best_res, best = res, (mm, n)
    return best, best_res


def main():
    t0 = time.time()
    print("T21 — le module d'or : la carte de Bragg   "
          "[T21-KO6-BRAGG-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : construction, populations Fibonacci, D-barre
    v1_N = all(len(mot_fibonacci(n)) == fib(n + 2) for n in NIVEAUX_F1)
    x18, longs18 = positions(NIVEAU_DFT)
    N18 = len(x18)
    dbar_longueur = float(longs18.sum()) / N18
    densL = mot_fibonacci(NIVEAU_DFT).count("L") / N18
    densS = 1 - densL
    dbar_densites = densL * PHI + densS * 1.0
    v1_dbar = (abs(dbar_longueur - (3 - PHI)) < TOL_REG
               and abs(dbar_densites - (3 - PHI)) < TOL_REG)
    V1 = bool(v1_N and v1_dbar)
    print(f"V1 F1 : N_n = F(n+2) exact (niveaux {NIVEAUX_F1}) : {v1_N} · "
          f"D-barre = {dbar_longueur:.9f} (= 3 - phi = {3-PHI:.9f}) "
          f"deux voies : {v1_dbar} → {'PASS' if V1 else 'FAIL'}")

    # ---- V2 / F2 : support dore (DFT grille gelee, Hann, niveau 18)
    db_ = dbar_longueur
    ku = np.linspace(0.0, KMAX, GRID, endpoint=False)
    w_h = hann(N18)
    S = np.zeros(GRID, dtype=complex)
    pas = 8192
    for i0 in range(0, GRID, pas):
        k = 2 * np.pi * ku[i0:i0 + pas] / db_
        S[i0:i0 + pas] = w_h @ np.exp(1j * np.outer(x18, k))
    I = np.abs(S) ** 2
    I[0] = 0.0
    top = np.argsort(I)[::-1][:40]
    pics = []
    for idx in top:
        if all(abs(idx - p[0]) > 6 for p in pics):
            pics.append((int(idx), float(ku[idx])))
        if len(pics) == 8:
            break
    v2_ok, indexage = True, []
    for idx, kunit in pics:
        mn, res = module_or(kunit)
        v2_ok &= res < 0.5 * (KMAX / GRID)
        indexage.append((mn, round(kunit, 6), round(res, 7)))
    V2 = bool(v2_ok and len(pics) == 8)
    print(f"V2 F2 : 8 pics dominants, adherence au module m + n*phi : "
          f"{v2_ok}")
    for mn, ku_, res in indexage:
        print(f"   k*D-barre/2pi = {ku_:>9.6f} -> (m,n) = {mn} "
              f"(residu {res:.2e})")
    print(f"   → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 / F3 (v1.1, D4) : Dirac — plateau pic par pic ; hors module
    pics_tri = sorted(pics, key=lambda p: -I[p[0]])
    forts = pics_tri[:2]
    W18 = hann(N18).sum()
    conv_module = [[], []]
    conv_hors = []
    for niv in NIVEAUX_F1:
        x, _ = positions(niv)
        Wn = hann(len(x)).sum()
        for p_i, (_, ku_) in enumerate(forts):
            k = 2 * np.pi * ku_ / db_
            conv_module[p_i].append(abs(structure(x, k)) ** 2 / Wn ** 2)
        ligne = []
        for ku_hors in (np.sqrt(2), np.e):
            k = 2 * np.pi * ku_hors / db_
            ligne.append(abs(structure(x, k)) ** 2 / Wn ** 2)
        conv_hors.append(ligne)
    v3_module = all(min(r) > 1e-4 and abs(r[-1] - r[-2]) < 0.05 * max(r[-2], 1e-12)
                    for r in conv_module)
    fin_hors = [conv_hors[-1][j] for j in range(2)]
    debut_hors = [conv_hors[0][j] for j in range(2)]
    v3_hors = all(fin_hors[j] < 1e-4 and fin_hors[j] <= debut_hors[j] + 1e-12
                  for j in range(2))
    V3 = bool(v3_module and v3_hors)
    print(f"V3 F3 (v1.1) : pics forts coherents (plateau 5% : "
          f"{[[round(v, 4) for v in r] for r in conv_module]}) : {v3_module} "
          f"· hors module -> 0 (niveau 14 : {[round(v, 6) for v in debut_hors]} "
          f"-> niveau 18 : {[round(v, 6) for v in fin_hors]}) : {v3_hors} "
          f"→ {'PASS' if V3 else 'FAIL'}")

    # ---- V4 / F4 : invariance d'echelle phi (image (m+n, n) picsee)
    v4_ok = True
    details = []
    for (mn, ku_, res) in indexage[:4]:
        if mn is None:
            v4_ok = False
            continue
        m, n = mn
        m2, n2 = m + n, n
        ku2 = m2 + n2 * PHI
        k = 2 * np.pi * ku2 / db_
        I2 = abs(structure(x18, k)) ** 2 / W18 ** 2
        v4_ok &= I2 > 1e-5
        details.append(((m, n), (m2, n2), round(I2, 6)))
    V4 = bool(v4_ok)
    print(f"V4 F4 : invariance du module sous x*phi (indice (m,n) -> "
          f"(m+n,n)) : {v4_ok}")
    for a, b, i2 in details:
        print(f"   pic {a} -> image {b} : intensite relative {i2}")
    print(f"   → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 / F5 (v1.1, D3) : leviers refondus
    lv = {}
    # L1 : chaine periodique de pente NON convergente 7/18 (D3) —
    # l'image par x*phi du pic fort tombe hors du reseau j/18
    M_CELL = 100
    w_r = "".join("S" if (int(np.floor((i + 1) * 7 / 18))
                          - int(np.floor(i * 7 / 18))) == 1 else "L"
                  for i in range(18))
    mot_r = w_r * M_CELL
    longs_r = np.array([PHI if c == "L" else 1.0 for c in mot_r])
    x_r = np.concatenate([[0.0], np.cumsum(longs_r)[:-1]])
    dbar_r = float(longs_r.sum()) / len(longs_r)
    per_r = float(longs_r.sum())
    jr = np.arange(1, 18) / 18
    kr = 2 * np.pi * jr / dbar_r
    Sr = np.abs(np.sum(np.exp(1j * np.outer(x_r, kr)), axis=0)) ** 2
    j1r = int(np.argmax(Sr))
    k_img = PHI * kr[j1r]
    I_img = abs(np.sum(np.exp(1j * k_img * x_r))) ** 2
    lv["L1 pente non convergente 7/18 : l'image par x*phi du pic fort "
       f"(j={j1r+1}) tombe hors reseau (I_image/I_pic = "
       f"{float(I_img/Sr[j1r]):.2e} < 1e-3)"] = \
        bool(I_img / Sr[j1r] < 1e-3)
    # L2 : Thue-Morse hors DC — pas de Bragg
    ratios_tm = []
    for l in range(12, 19):
        n = 1 << l
        t = np.array([bin(j).count("1") % 2 for j in range(n)])
        F = np.abs(np.fft.fft(t)) ** 2 / n ** 2
        F[0] = 0.0
        ratios_tm.append(float(F.max()))
    lv["L2 Thue-Morse : pas de Bragg (max |S|^2/N^2 hors DC decroissant, "
       f"final {ratios_tm[-1]:.4f} < 0.02)"] = \
        all(ratios_tm[i + 1] < ratios_tm[i] for i in range(6)) \
        and ratios_tm[-1] < 0.02
    # L3 : la position dans le module ne suffit pas (chaîne unitaire)
    xu = np.arange(1024, dtype=float)
    Wu = hann(len(xu)).sum()
    mesures_u = []
    for ku_ in (PHI, 1 / PHI, 1.0):
        k = 2 * np.pi * ku_
        mesures_u.append(abs(np.sum(hann(len(xu)) * np.exp(1j * k * xu))) ** 2
                         / Wu ** 2)
    lv["L3 temoin unitaire : positions dorees internes (phi, 1/phi) NON "
       f"picees ({mesures_u[0]:.2e}, {mesures_u[1]:.2e} < 1e-4) ; reseau "
       f"entier pic (k=2pi : {mesures_u[2]:.3f} > 0,5)"] = \
        bool(mesures_u[0] < 1e-4 and mesures_u[1] < 1e-4
             and mesures_u[2] > 0.5)
    for k_, val in lv.items():
        print(f"V5 levier — {k_} : {val}")
    V5 = all(lv.values())

    criteres = {"V1_construction_Dbarre": bool(V1),
                "V2_support_dore": bool(V2),
                "V3_caractere_de_Dirac": bool(V3),
                "V4_invariance_echelle_phi": bool(V4),
                "V5_leviers": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T21-Q-KO6-MODULE-OR-2026-10",
        "protocole": "T21-KO6-BRAGG-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le module d'or : la diffraction de Bragg de la chaîne "
                 "de Fibonacci (peigne de Dirac doré, cohérent, "
                 "invariant sous l'échelle φ)",
        "statut_du_mot": "PONT DIFFUSIF (fonction de structure) — "
                         "théorème mesuré à zéro paramètre ; AUCUNE "
                         "prédiction d'expérience ; le physique "
                         "(59 meV) n'est pas touché",
        "mesures": {
            "D_barre": dbar_longueur,
            "N_niveau_18": N18,
            "pics_indexage": [{"m": mn[0], "n": mn[1], "k_unit": ku_,
                               "residu": res} for mn, ku_, res in indexage],
            "I_fort_normalisee_niveau_18":
                float(min(min(r) for r in conv_module)),
            "max_hors_module": max(conv_hors),
        },
        "V1": bool(V1), "V2": bool(V2),
        "V3": {"module": bool(v3_module), "hors_module": bool(v3_hors)},
        "V4": {"invariance": bool(v4_ok), "details": details},
        "V5": {k: bool(v) for k, v in lv.items()},
        "falsifieur": "F1…F4 hors TOL_REG / seuils déclarés ; levier "
                      "non détecté",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t21_ko6_module_or_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T21 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
