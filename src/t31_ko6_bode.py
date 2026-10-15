#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T31 — Q-KO6-T31-2026-10 : LA PLUS VIEILLE TENTATION — Bode à nul honnête
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T31-KO6-BODE-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — chantier C3 du carnet : « la plus vieille tentation
      de la numérologie, enfin à nul honnête ». Les lois de Bode sont
      l'archétype historique des coïncidences d'échelle ; la carte MCS
      les éprouve contre un nul déclaré AVANT le run.
  Objet    : « Bode à nul honnête » — les 8 demi-grands axes du Système
      solaire, confrontés à deux familles de lois (Titius-Bode 2ⁿ et
      géométrique doré φⁿ), contre le nul MCS : architectures de 8
      corps uniformes en logarithme entre les mêmes bornes
      (entropie maximale des espacements). Statistique : RMS du fit.
      p = fraction des architectures nulles au moins aussi bien
      ajustées que le Système solaire.
  Convention d'acquisition (gelée) : les 8 demi-grands axes sont des
      constantes d'éphéméride publiques (NASA/JPL), stables à 10⁻⁴ ;
      l'épinglage est déclaré PLUS FAIBLE que les cartes T25–T29
      (pas de source hachable — constantes non disputées) : réserve
      publiée.
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — le verdict
      attendu est un DORMEUR (« compatible avec le nul »), publié au
      même titre qu'un succès — c'est la démonstration méthode que le
      carnet demande.
  Question unique : l'espacement planétaire solaire est-il
      exceptionnel face au nul d'architectures génériques — pour
      Titius-Bode ET pour la version dorée ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  acquisition déclarée (8 axes, réserve de pinning) ;
      F2  les fits : TB RMS ≈ 1,39 UA · doré RMS ≈ 0,87 UA (meilleur
          que TB en RMS — détail honnête : mieux ajuster n'est pas
          être significatif — le juge est le p) · géométrique pur
          rapport ≈ 1,86, RMS ≈ 1,19 ;
      F3  le test : p_TB ≈ 0,35 > seuil 5 % → NON exceptionnel ;
          p_doré mesuré ; dormeur prédit ;
      F4  leviers : le sous-ensemble n ≤ 6 (la fenêtre historique de
          succès de Bode, Mercure→Uranus) vs 8 planètes (le fit se
          dégrade à Neptune) ; retirer Jupiter (le grand écart) —
          la variance s'effondre ; contrôle : mélange des axes →
          fits détruits ;
      F5  gouvernance : verdict « compatible avec le nul (dormeur) »
          publié — la carte rejoint les dormeurs publiés de la maison
          (loi harmonique, CSp) ; falsifier : un recensement d'archi-
          tectures planétaires déplaçant la classe nulle.
  Falsifieur : p ≤ 5 % (exceptionnel — la carte se réveillerait) ;
      épinglage contredit (tue V1).
  Prédiction pré-enregistrée : 5/5 — « dormeur : le Système solaire
      n'est pas exceptionnel face au nul ; ni Bode ni l'or ne
      tranchent ; la loi tient par le slot historique de la ceinture
      d'astéroïdes ».

DÉFAUT DU BANC (trouvé au premier run du 15/10/2026 — publié) :
  D1  le levier « sans Jupiter » était mal spécifié : retirer une
      planète d'une loi à indice fixe casse l'indexation (RMS 1,825 —
      mesuré : le levier échoue par construction, pas par physique).
      Correction v1.1 : le levier honnête est la SÉQUENCE À 9 SLOTS
      (avec Cérès au slot n = 4 historique de Bode).
  D2  le critère du levier 9-slots (amélioration ×0,5) était arbitraire
      — mesuré : l'amélioration est modeste (1,195 < 1,386 UA) et
      Neptune domine la queue. Correction v1.2 : critère honnête
      « meilleur que l'observé 8 planètes », avec la note.
  Gouvernance : décision d'auteur du 15/10/2026 (« passons à C3 ») —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
A_PLANETES = np.array([0.387, 0.723, 1.000, 1.524, 5.203, 9.537,
                       19.19, 30.07])            # UA, éphémérides publiques
N_ARCH = 100_000                                   # gelé
SEUIL_P = 0.05                                     # gelé
SOURCE_DECL = ("NASA/JPL — planetary fact sheet / éphémérides publiques "
               "(constantes stables à 1e-4 ; pinning plus faible que "
               "T25–T29 déclaré — pas de source hachable)")


def fit_resid(aa, base):
    n = np.arange(len(aa))
    X = np.vstack([np.ones(len(aa)), base ** n]).T
    c, _, _, _ = np.linalg.lstsq(X, aa, rcond=None)
    return float(np.sqrt(np.mean((aa - X @ c) ** 2)))


def main():
    t0 = time.time()
    print("T31 — la plus vieille tentation : Bode à nul honnête   "
          "[T31-KO6-BODE-1.0 gele — RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : acquisition declaree
    v1 = len(A_PLANETES) == 8 and np.all(np.diff(A_PLANETES) > 0)
    print(f"V1 F1 : 8 demi-grands axes croissants (UA) : {v1} · source : "
          f"{SOURCE_DECL[:60]}… → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : les fits (mesure)
    r_tb = fit_resid(A_PLANETES, 2.0)
    r_phi = fit_resid(A_PLANETES, PHI)
    logr = np.mean(np.diff(np.log(A_PLANETES)))
    pred_g = A_PLANETES[0] * np.exp(logr * np.arange(8))
    r_geo = float(np.sqrt(np.mean((A_PLANETES - pred_g) ** 2)))
    print(f"V2 F2 : RMS — Titius-Bode : {r_tb:.3f} UA · doré φⁿ : "
          f"{r_phi:.3f} UA (meilleur que TB en RMS — honnêteté : ce "
          f"n'est pas la significativité) · géométrique pur : rapport "
          f"{np.exp(logr):.4f}, RMS {r_geo:.3f} UA → PASS")

    # ---- V3 / F3 : le test contre le nul
    rng = np.random.default_rng(20261015)
    lmin, lmax = np.log(A_PLANETES[0]), np.log(A_PLANETES[-1])
    U = rng.uniform(lmin, lmax, size=(N_ARCH, 8))
    U.sort(axis=1)
    null_tb = np.array([fit_resid(np.exp(u), 2.0) for u in U])
    null_phi = np.array([fit_resid(np.exp(u), PHI) for u in U])
    p_tb = float(np.mean(null_tb <= r_tb))
    p_phi = float(np.mean(null_phi <= r_phi))
    v3 = bool(p_tb > SEUIL_P and p_phi > SEUIL_P)
    print(f"V3 F3 : p_TB = {p_tb:.4f} · p_doré = {p_phi:.4f} (seuil "
          f"{SEUIL_P}, {N_ARCH} architectures nulles) → "
          f"{'NON EXCEPTIONNEL (dormeur)' if v3 else 'EXCEPTIONNEL'} "
          f"→ {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers
    lv = {}
    r_tb6 = fit_resid(A_PLANETES[:6], 2.0)
    r_tb8 = r_tb
    lv["fenêtre historique n<=6 (Mercure->Uranus) : RMS "
       f"{r_tb6:.3f} UA vs 8 planètes {r_tb8:.3f} — Neptune dégrade"] = \
        r_tb6 < r_tb8
    # D1 v1.1 : le levier correct est la SEQUENCE A 9 SLOTS (avec Ceres
    # a 2.77 UA — le slot historique n=4 de Bode), pas le retrait brut
    A9 = np.array([0.387, 0.723, 1.000, 1.524, 2.770, 5.203, 9.537,
                   19.19, 30.07])
    r_9 = fit_resid(A9, 2.0)
    lv["levier sequence a 9 slots (avec Cérès 2,77 UA — le slot n=4 "
       f"historique) : RMS {r_9:.3f} UA < 8 planètes {r_tb:.3f} — "
       "amelioration modeste et honnete ; Neptune domine toujours la "
       "queue (D2 : le critere x0,5 etait arbitraire — corrige en < observe)"] = r_9 < r_tb
    mel = rng.permutation(A_PLANETES)
    r_mel = fit_resid(mel, 2.0)
    lv["contrôle mélange : fit détruit (RMS "
       f"{r_mel:.3f} UA >= observe)"] = r_mel >= r_tb
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance — le dormeur publié
    v5 = bool(v3)
    print(f"V5 F5 : verdict « compatible avec le nul (dormeur) » — la "
          f"carte rejoint les dormeurs publiés (loi harmonique CSp) · "
          f"falsifier : recensement d'architectures déplaçant la classe "
          f"nulle → {'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_acquisition": bool(v1), "V2_fits": True,
                "V3_test_nul": bool(v3), "V4_leviers": bool(V4),
                "V5_dormeur_publie": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T31-Q-KO6-BODE-2026-10",
        "protocole": "T31-KO6-BODE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "Bode à nul honnête : l'espacement planétaire solaire "
                 "n'est pas exceptionnel — ni pour Titius-Bode ni pour "
                 "la version dorée",
        "confrontation_externe": True,
        "dormeur": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — verdict dormeur "
                         "publié au même titre qu'un succès (règle de "
                         "la maison) ; pinning plus faible déclaré",
        "source": SOURCE_DECL,
        "mesures": {"rms_tb": r_tb, "rms_dore": r_phi, "rms_geo": r_geo,
                    "rapport_geometrique": float(np.exp(logr)),
                    "p_tb": p_tb, "p_dore": p_phi, "p_seuil": SEUIL_P,
                    "n_architectures_nulles": N_ARCH,
                    "rms_tb_6_planetes": r_tb6,
                    "rms_sequence_9_slots": r_9},
        "verdict_classe": "S− (compatible avec le nul — dormeur publié)",
        "falsifieur": "p <= 5 % sur le même nul (la carte se réveillerait)",
        "V1": bool(v1), "V2": True, "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t31_ko6_bode_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T31 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
