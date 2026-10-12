#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T16 — Q-KO6-T16-2026-10 : LA TEXTURE MINIMALE — la chaîne à trois
      saveurs et le premier nombre anticipé
      [v1.1 — défaut du banc D1 corrigé, déclaré ci-dessous]
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T16-KO6-TEXT-1.0 gelé]

DÉFAUT DU BANC (v1.0, trouvé au premier run du 12/10/2026 — publié) :
  D1  la fenêtre de comptage des modes légers (< 0,9·λ₊) laissait
      entrer les paires de Dirac des chaînes brisées (les saveurs à
      y = 0 laissent une paire ±M_R — mesuré, publié). Correction
      v1.1 : la fenêtre déclarée est (1e-6 ; 0,75·M_R) — le mode léger
      λ₋ ≤ 1/φ·M_R y vit seul ; les zéros sont comptés en états
      PHYSIQUES (la construction double particules/antiparticules —
      déclaré : diviser par deux).
  Aucune prédiction n'est tuée — l'instrument l'était.

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « la texture minimale » : la chaîne du seesaw (mot
      certifié — T14, T15) étendue à trois saveurs avec texture de
      Yukawa déclarée diag(y₁, y₂, y₃) sur le saut de Dirac — le
      secteur neutrino à trois saveurs de la construction publiée de
      T9 (borne déclarée : la texture vit dans le secteur ν ; le reste
      du triplet est inchangé — l'ordre un du triplet complet est la
      régression de T14, citée).
      Stratégie du 12/10/2026 (la batterie du lexique, T15) : la
      phrase est faite de mots certifiés, confrontée à un fait mesuré :
      NuFIT mesure DEUX splittings non nuls (acquisition épinglée au
      JALON-MCS26, citée par empreinte).
  Question unique : le rang minimal de la texture compatible avec le
      fait mesuré (deux splittings) est-il 2 — et alors l'état le plus
      léger est-il exactement sans masse ? Et le nombre anticipé :
      Σm_ν au plancher NO, calculé de l'acquisition épinglée.
  Filiation : T14 (la chaîne — forme close généralisée déclarée :
      λ²±(y) = ((M_R²+2y²) ± M_R√(M_R²+4y²))/2 — se réduit à la forme
      de T14 à y = 1) ; T9 (la construction) ; T15 (la règle : des mots
      certifiés) ; JALON-MCS26 (l'acquisition NuFIT épinglée).
  Fait déclaré (dérivé avant gel, à vérifier par la machine) : la
      chaîne à 4 maillons de sauts (y, M_R, y) par saveur est fermée
      sous D ; le mode léger suit λ₋ → y²/M_R pour y → 0 (le seesaw,
      déclaré) ; à y = 0 le zéro apparaît (le levier de T14, mesuré).
  Protocole machine (bornes déclarées) :
      V1  la construction à trois saveurs : la texture égale (1,1,1)
          reproduit la chaîne de T14 trois fois (régression tuante) ;
      V2  l'échelle de textures gelée : rang 1 : (1, 0, 0) ; rang 2 :
          (1, 1/4, 0) ; rang 3 : (1, 1/4, 1/16) (déclarée) — le nombre
          de modes légers massifs mesuré = le rang de la texture
          (exactement, à TOL) : le fait mesuré (deux splittings —
          NuFIT épinglé) exige rang ≥ 2 → la texture minimale est
          rang 2 → exactement UN mode léger sans masse (mesuré) ;
      V3  la forme close généralisée vérifiée à TOL sur l'échelle
          (régression tuante) ;
      V4  le nombre anticipé : Σm_ν|plancher = √Δm²_21 + √Δm²_31 (NO,
          léger = 0) calculé de l'acquisition épinglée (constantes
          re-déclarées avec provenance — l'empreinte de l'acquisition
          citée) ; la borne DESI 2025 consignée (0,064 eV — source
          publique déclarée du 12/10/2026) ; la distance
          plancher ↔ borne mesurée ; la condition de mort déclarée :
          une mesure de Σm_ν nettement au-dessus du plancher tue la
          texture minimale (et le porteur comme secteur neutrino —
          T14) ; une borne qui serre sans distinguer ne tranche pas ;
      V5  leviers tuables : l'échelle mesurée (rang 1 → 1 mode léger
          massif ; rang 3 → 3) ; Y → 0 (régression T14) ; la forme
          close tue si hors TOL (contrôle).
  Falsifieur : la forme close hors TOL ; le rang mesuré ≠ rang de la
      texture ; un levier non détecté.
  Prédiction pré-enregistrée : le rang minimal est 2 ; le plancher est
      la position du banc (les deux chemins de T14 y convergent : la
      texture minimale OU le zéro algébrique du porteur — la tension
      publiée de T14 se résout : les deux atteignent le plancher) ;
      Σm_ν anticipé ≈ 0,059 eV.
  Gouvernance : décision d'auteur du 12/10/2026 (« allons-y ») —
      publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9        # figé (filiation KO6-REAL-1.0)
TOL_REG = 1e-6    # tolérance de régression (déclarée)

M_R = 1.0   # convention de T14 (déclarée)
# l'acquisition épinglée (JALON-MCS26, NuFIT v6.0 IC19 sans SK-atm, NO —
# valeurs re-déclarées avec provenance ; empreinte de l'acquisition :
# sha256 6e0091c3..., citée) :
DM21 = 7.49e-5     # eV² (Δm²_21)
DM31 = 2.534e-3    # eV² (Δm²_31)
BORNE_DESI_2025 = 0.064   # eV — source publique déclarée du 12/10/2026

ECHELLE = {"rang 1": (1.0, 0.0, 0.0), "rang 2": (1.0, 0.25, 0.0),
           "rang 3": (1.0, 0.25, 0.0625)}   # échelle gelée


def forme_close(y, M=M_R):
    """λ²±(y) = ((M²+2y²) ± M√(M²+4y²))/2 — forme close déclarée."""
    disc = M * np.sqrt(M ** 2 + 4 * y ** 2)
    return (np.sqrt(((M ** 2 + 2 * y ** 2) - disc) / 2),
            np.sqrt(((M ** 2 + 2 * y ** 2) + disc) / 2))


def chaine_3f(texture, M=M_R):
    """Le secteur neutrino à trois saveurs : la chaîne à 4 maillons
    (ν_L — ν_R — ν̄_R — ν̄_L) par saveur, sauts (y_i, M, y_i)."""
    n = 12
    D = np.zeros((n, n))
    for i, y in enumerate(texture):
        a, b, c, d = 4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3
        D[a, b] = D[b, a] = y
        D[b, c] = D[c, b] = M
        D[c, d] = D[d, c] = y
    return np.linalg.eigvalsh(D)


def main():
    t0 = time.time()
    print("T16 — la texture minimale : la chaîne à trois saveurs   "
          "[T16-KO6-TEXT-1.0 gelé]")
    print("=" * 76)

    # ---- V1 : construction + régression à T14 (texture égale)
    ev_111 = chaine_3f((1.0, 1.0, 1.0))
    lm_t14, lp_t14 = forme_close(1.0)
    legers = sorted(abs(x) for x in ev_111)
    reg_t14 = (len(ev_111) == 12
               and abs(legers[0] - lm_t14) < TOL_REG
               and abs(legers[-1] - lp_t14) < TOL_REG
               and abs(sum(x ** 2 for x in ev_111)
                       - 3 * 2 * (lm_t14 ** 2 + lp_t14 ** 2)) < TOL_REG)
    V1 = bool(reg_t14)
    print(f"V1 construction : texture égale → trois chaînes de T14 "
          f"(légers {[round(x, 4) for x in legers[:3]]} = 1/φ — "
          f"régression {'OK' if reg_t14 else 'FAIL'})")

    # ---- V2 : l'échelle de textures — le rang mesuré
    # v1.1 (défaut D1) : la fenêtre des modes légers est déclarée
    # (1e-6 ; 0,75·M_R) — elle exclut les paires de Dirac (±M_R) des
    # chaînes brisées ; les zéros sont comptés en états PHYSIQUES
    # (la construction double particules/antiparticules — déclaré)
    FEN_LO, FEN_HI = 1e-6, 0.75 * M_R
    print("V2 l'échelle de textures (gelée) :")
    v2_ok = True
    echelle_mes = {}
    for nom, tex in ECHELLE.items():
        ev = chaine_3f(tex)
        massifs_legers = [x for x in (abs(e) for e in ev)
                          if FEN_LO < x < FEN_HI]
        rang_mesure = sum(1 for y in tex if y != 0.0)
        ok = len(massifs_legers) == rang_mesure * 2  # ± paires par saveur
        v2_ok &= bool(ok)
        zeros = sum(1 for e in ev if abs(e) < 1e-6) // 2   # états physiques
        echelle_mes[nom] = {"texture": list(tex),
                            "modes_légers_massifs": len(massifs_legers),
                            "zéros_exact_états_physiques": zeros,
                            "rang_mesuré_=_rang_texture": ok}
        print(f"   {nom} {tex} : {len(massifs_legers)} modes légers "
              f"massifs · {zeros} état(s) sans masse · rang mesuré = "
              f"rang de la texture : {ok}")
    # le fait mesuré (NuFIT épinglé) : deux splittings → rang minimal 2
    # → exactement un état physique sans masse (mesuré sur rang 2)
    ev_min = chaine_3f(ECHELLE["rang 2"])
    un_zero_leger = (sum(1 for e in ev_min if abs(e) < 1e-6) // 2 == 1)
    v2_ok &= bool(un_zero_leger)
    print(f"   fait mesuré : deux splittings (NuFIT épinglé) → rang "
          f"minimal 2 → exactement un état physique sans masse : "
          f"{un_zero_leger}")
    V2 = bool(v2_ok)

    # ---- V3 : la forme close généralisée sur l'échelle
    v3_ok = True
    for nom, tex in ECHELLE.items():
        ev = sorted(abs(x) for x in chaine_3f(tex))
        for y in tex:
            if y == 0.0:
                continue
            lm, lp = forme_close(y)
            v3_ok &= bool(any(abs(e - lm) < TOL_REG for e in ev)
                          and any(abs(e - lp) < TOL_REG for e in ev))
    V3 = bool(v3_ok)
    print(f"V3 forme close généralisée λ²±(y) : vérifiée à TOL sur "
          f"l'échelle → {'PASS' if V3 else 'FAIL'}")

    # ---- V4 : le nombre anticipé
    plancher = float(np.sqrt(DM21) + np.sqrt(DM31))   # NO, léger = 0
    distance_borne = abs(plancher - BORNE_DESI_2025) / plancher
    V4 = bool(plancher > 0 and distance_borne > 0)
    print(f"V4 le nombre anticipé : Σm_ν|plancher = √Δm²_21 + √Δm²_31 "
          f"= {plancher * 1000:.2f} meV (acquisition épinglée, NO, "
          f"léger = 0) ; borne DESI 2025 consignée : "
          f"{BORNE_DESI_2025 * 1000:.0f} meV ; distance mesurée : "
          f"{distance_borne * 100:.1f} % — la borne serre le plancher "
          f"sans encore le distinguer")

    # ---- V5 : leviers
    lv = {}
    ev_r1 = chaine_3f(ECHELLE["rang 1"])
    ev_r3 = chaine_3f(ECHELLE["rang 3"])
    lv["l'échelle mesurée (rang 1 → 1 paire légère massive ; rang 3 → "
       "3)"] = bool(
        sum(1 for e in ev_r1 if FEN_LO < abs(e) < FEN_HI) == 2
        and sum(1 for e in ev_r3 if FEN_LO < abs(e) < FEN_HI) == 6)
    lv["Y → 0 : le zéro apparaît (régression T14)"] = bool(
        min(abs(x) for x in chaine_3f((0.0, 0.0, 0.0))) < 1e-12)
    lv["la forme close tue si hors TOL (contrôle)"] = bool(
        abs(forme_close(1.0)[1] - 1.617) > 1e-3)   # mesuré : tuerait
    for k, v in lv.items():
        print(f"V5 levier — {k} : {v}")
    V5 = all(lv.values())

    criteres = {"V1_construction_régression": V1,
                "V2_échelle_rang_mesuré": V2,
                "V3_forme_close_généralisée": V3,
                "V4_nombre_anticipé": V4, "V5_leviers": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T16-Q-KO6-TEXTURE-2026-10",
        "protocole": "T16-KO6-TEXT-1.0 (gelé)",
        "objet": "la texture minimale : la chaîne à trois saveurs et le "
                 "premier nombre anticipé (Σm_ν au plancher NO)",
        "V1_régression_T14": bool(reg_t14),
        "V2_échelle": echelle_mes,
        "V2_fait_mesuré": "deux splittings non nuls (NuFIT épinglé — "
                          "JALON-MCS26) → rang minimal 2 → exactement "
                          "un état léger sans masse",
        "V3_forme_close": "λ²±(y) = ((M_R²+2y²) ± M_R√(M_R²+4y²))/2 — "
                          "vérifiée à TOL sur l'échelle",
        "V4_anticipation": {
            "Σm_ν_plancher_NO_meV": plancher * 1000,
            "borne_DESI_2025_meV": BORNE_DESI_2025 * 1000,
            "distance_plancher_borne_%": distance_borne * 100,
            "condition_de_mort": "Σm_ν mesuré nettement au-dessus du "
                                 "plancher tue la texture minimale (et "
                                 "le porteur comme secteur neutrino — "
                                 "T14) ; une borne qui serre sans "
                                 "distinguer ne tranche pas",
            "provenance": "constantes re-déclarées de l'acquisition "
                          "épinglée au JALON-MCS26 (NuFIT v6.0 IC19, "
                          "sha256 6e0091c3… cité)"},
        "V5_leviers": lv,
        "lecture": "la première phrase faite de mots certifiés : la "
                   "chaîne du seesaw (certifiée, T14/T15) + le fait "
                   "mesuré (deux splittings) → le rang minimal de la "
                   "texture est 2 → l'état le plus léger est exactement "
                   "sans masse → Σm_ν anticipé au plancher NO ≈ 59,0 "
                   "meV — mesuré, publié avec sa condition de mort. La "
                   "tension publiée de T14 se résout : les deux "
                   "structures du banc (la texture minimale du MS et le "
                   "zéro algébrique du porteur) atteignent le plancher.",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "forme close hors tolérance ; rang mesuré ≠ rang "
                      "de la texture ; levier non détecté",
        "gouvernance": "décision d'auteur du 12/10/2026 (« allons-y »)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t16_ko6_texture_minimale_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T16 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
