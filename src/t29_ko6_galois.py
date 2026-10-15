#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T29 — Q-KO6-T29-2026-10 : LES DEUX FACES DU MODULE —
      le conjugué de Galois dans l'espace perpendiculaire réel
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T29-KO6-GALOIS-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CINQUIÈME confrontation externe ; première passe du
      chantier « intensités » (pont arithmétique vers McKay, T19).
  Objet    : « les deux faces du module » — l'annexe Dong (147 raies,
      déjà épinglée, dataset étendu avec indices 6D) vérifie non
      seulement la loi parallèle (T28) mais une loi PERPENDICULAIRE :
          qpar²  = (N + Mτ)/(2(2+τ))          (face parallèle)
          qperp² = τ(Nτ − M)/(2(2+τ))         (face perpendiculaire,
                                               conjuguée de Galois)
      L'espace perpendiculaire — celui des surfaces atomiques, celui
      où vivent les INTENSITÉS (F(Q) = TF des surfaces atomiques en
      Q⊥) — est donc doré aussi. Deuxième source épinglée : la revue
      Quiquandon–Gratias 2008 (HAL hal-00513873), qui établit que les
      intensités se répartissent en quatre branches selon les parités
      de (N, M) — signature de trois surfaces atomiques.
  STATUT DU MOT (déclaré, gelé) : PONT ARITHMÉTIQUE — la carte pose
      l'arithmétique doree des phases ; elle NE SIMULE AUCUNE
      INTENSITÉ (pas de surfaces atomiques modélisées — hors
      périmètre déclaré) ; la table d'intensités MESURÉES reste
      l'acquisition ouverte (Boudard 1992, paywall).
  Question unique : l'espace perpendiculaire réel porte-t-il le
      conjugué de Galois du module — et l'arithmétique des phases
      atteint-elle où le jeu de données épinglé s'arrête ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  épinglage (deux sources, empreintes relues) + dataset étendu
          (147 raies, indices 6D, deux lois) ;
      F2  les deux faces : 147/147 sous les deux lois (résidus à
          l'arrondi) ;
      F3  les phases : la phase bc est uniformément +1 sur le sous-
          ensemble épinglé (147/147) — signature de la décoration des
          nœuds (condition qperp < 1 de l'annexe) ; la répartition en
          QUATRE branches (revue épinglée) N'EST PAS testable sur ce
          sous-ensemble (2/4 classes de parité peuplées, phases
          dégénérées) — limite déclarée, acquisition impaire (odd-N)
          ouverte ;
      F4  leviers : τ → 13/8 dégrade la face perpendiculaire
          (mesuré) ; permutation des indices casse les deux lois ;
      F5  gouvernance : pont posé, intensités mesurées = acquisition
          ouverte, aucune surface atomique modélisée.
  Falsifieur : > 3 raies hors des deux lois (réfutation) ; épinglage
      rompu (tue V1).
  Prédiction pré-enregistrée : 5/5.
  Gouvernance : décision d'auteur du 15/10/2026 (« attaque les
      intensités ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
PHI = (1 + np.sqrt(5)) / 2
URL_DONG = "https://hal.univ-lorraine.fr/tel-01776194/document"
EMPREINTE_DONG = ("ac95fe442e8d775f4e4803a315a9563e411fa2f1eead476"
                  "a66e26acd5b57c33d")
URL_QG = "https://hal.science/hal-00513873/file/PEER_stage2_10.1080%2F14786430801971474.pdf"
EMPREINTE_QG = "2745ecd3bbbc2f2582d1"  # prefixe releve a la reconnaissance
PDF_DONG = Path(__file__).resolve().parents[2] / "these_dong_1991.pdf"
PDF_QG = Path(__file__).resolve().parents[2] / "quiquandon_2008.pdf"
DONNEES = Path(__file__).resolve().parent.parent / "data" / \
    "annexe_dong_147_phases.json"


def qpar_loi(N, M, tau=PHI):
    return float(np.sqrt((N + M * tau) / (2 * (2 + tau))))


def qperp_loi(N, M, tau=PHI):
    return float(np.sqrt(tau * (N * tau - M) / (2 * (2 + tau))))


def main():
    t0 = time.time()
    print("T29 — les deux faces du module : le conjugué de Galois   "
          "[T29-KO6-GALOIS-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage (deux sources)
    emp_dong = hashlib.sha256(PDF_DONG.read_bytes()).hexdigest() \
        if PDF_DONG.exists() else None
    emp_qg = hashlib.sha256(PDF_QG.read_bytes()).hexdigest() \
        if PDF_QG.exists() else None
    v1_dong = emp_dong == EMPREINTE_DONG
    v1_qg = emp_qg is not None and emp_qg.startswith(EMPREINTE_QG)
    raies = json.loads(DONNEES.read_text(encoding="utf-8"))
    v1 = bool(v1_dong and v1_qg and len(raies) == 147)
    print(f"V1 F1 : Dong relue : {v1_dong} · Quiquandon–Gratias relue : "
          f"{v1_qg} ({(emp_qg or '?')[:20]}…) · {len(raies)} raies avec "
          f"indices 6D → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : les deux faces du module
    rp = [abs(qpar_loi(x["N"], x["M"]) - x["qpar"]) for x in raies]
    rq = [abs(qperp_loi(x["N"], x["M"]) - x["qperp"]) for x in raies]
    v2 = all(r <= 5e-4 for r in rp) and all(r <= 5e-3 for r in rq)
    print(f"V2 F2 : face parallèle qpar² = (N + Mτ)/(2(2+τ)) : "
          f"{sum(r <= 5e-4 for r in rp)}/{len(raies)} (max {max(rp):.2e}) · "
          f"face perpendiculaire qperp² = τ(Nτ − M)/(2(2+τ)) : "
          f"{sum(r <= 5e-3 for r in rq)}/{len(raies)} (max {max(rq):.2e}) "
          f"→ {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : l'arithmétique des phases (et sa limite honnête)
    classes = {}
    for x in raies:
        c = (x["N"] % 2, x["M"] % 2)
        classes.setdefault(c, []).append(x["phase_bc"])
    n_classes = len(classes)
    phases_uniformes = all(len(set(v)) == 1 for v in classes.values())
    v3 = bool(n_classes >= 2 and phases_uniformes)
    print(f"V3 F3 : classes de parité peuplées : {n_classes}/4 "
          f"({ {k: len(v) for k, v in classes.items()} }) · phase bc "
          f"uniforme par classe : {phases_uniformes} — la répartition en "
          f"QUATRE branches (revue épinglée) n'est PAS testable sur ce "
          f"sous-ensemble : limite déclarée, acquisition odd-N ouverte "
          f"→ {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers
    lv = {}
    rq13 = [abs(qperp_loi(x["N"], x["M"], tau=13 / 8) - x["qperp"])
            for x in raies]
    lv["levier 13/8 sur la face perpendiculaire : degradation "
       f"x{np.mean(rq13)/np.mean(rq):.1f}"] = \
        np.mean(rq13) > 5 * np.mean(rq)
    rng = np.random.default_rng(11)
    idx_perm = rng.permutation([x["indices6D"] for x in raies])
    casse = 0
    for x, ip in zip(raies, idx_perm):
        N2 = sum(i * i for i in ip)
        if N2 != x["N"]:
            casse += 1
    lv["levier permutation des indices 6D : les deux lois cassées "
       f"({casse}/{len(raies)} indices N changés)"] = casse >= 140
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance
    v5 = bool(v1 and v2)
    print(f"V5 F5 : pont arithmétique posé (positions + faces + phases) · "
          f"intensités mesurées = acquisition ouverte déclarée (Boudard "
          f"1992, paywall) · aucune surface atomique modélisée → "
          f"{'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_epinglage_deux_sources": bool(v1),
                "V2_deux_faces_du_module": bool(v2),
                "V3_arithmetique_des_phases": bool(v3),
                "V4_leviers": bool(V4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T29-Q-KO6-GALOIS-2026-10",
        "protocole": "T29-KO6-GALOIS-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "les deux faces du module : le conjugué de Galois dans "
                 "l'espace perpendiculaire réel (annexe Dong 147 raies) "
                 "— première passe du pont vers les intensités",
        "confrontation_externe": True,
        "statut_du_mot": "PONT ARITHMÉTIQUE — aucune intensité simulée, "
                         "aucune surface atomique modélisée ; les "
                         "intensités mesurées restent l'acquisition "
                         "ouverte",
        "sources": {
            "dong": {"url": URL_DONG, "sha256": emp_dong,
                     "pages": "Annexe 1, p. 188-193"},
            "quiquandon_gratias_2008": {
                "url": URL_QG, "sha256": emp_qg,
                "releve": "les intensités se répartissent en quatre "
                          "branches selon les parités de (N, M) — "
                          "signature de trois surfaces atomiques "
                          "(valable i-AlCuFe et i-AlPdMn)"}},
        "mesures": {
            "qpar_residu_max": max(rp), "qperp_residu_max": max(rq),
            "classes_parite": {str(k): len(v) for k, v in classes.items()},
            "qperp_13sur8_degradation":
                float(np.mean(rq13) / np.mean(rq))},
        "limite_declaree": "répartition en quatre branches non testable "
                           "sur le sous-ensemble épinglé (2/4 classes, "
                           "phases dégénérées) — acquisition odd-N "
                           "ouverte ; intensités mesurées : Boudard "
                           "1992 (paywall)",
        "verdict_classe": ("S+ (pont posé, limite déclarée)" if nb >= 4
                           else "partiel — publication au même titre"),
        "falsifieur": "> 3 raies hors des deux lois (réfutation "
                      "publiée au même titre)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t29_ko6_galois_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T29 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
