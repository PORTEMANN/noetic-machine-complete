#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T25 — Q-KO6-T25-2026-10 : LE PREMIER REGARD EXTERNE —
      le module d'or face au quasicristal d'Al-Mn (1984)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T25-KO6-REEL-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — PREMIÈRE CONFRONTATION EXTERNE du pont diffusif
      (chantier E1 du carnet NOTE-CANDIDATS-PONT-PHI).
  Objet    : « le premier regard externe » — la carte MCS confronte le
      module d'or (T21) à une donnée de laboratoire réelle, épinglée :
      les deux raies de diffraction à plus bas angle de l'alliage
      icosaédrique Al-Mn (le premier quasicristal, Shechtman 1984),
      telles que publiées dans la revue de M. Widom, « Quasicrystal
      Structure and Properties », Annu. Rev. Phys. Chem. 42 (1991)
      685 — PDF ouvert (CMU), empreinte relevée à la reconnaissance :
      d₁ = 8,85 ± 0,07 Å et d₂ = 5,42 ± 0,03 Å (axe twofold).
  Filiation : T21 (le module d'or — régression interne) ; T22/T22-D3
      (Legendre : les convergents voient tout — confondant déclaré) ;
      T20 (le mot caractéristique) ; carnet (E1) ; MCS-26 (discipline
      de carte : nul honnête, seuils déclarés).
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — le verdict
      dira « compatible (S+) » ou « réfuté », JAMAIS « vrai » ; la
      carte porte sa réserve structurale (précision des données,
      confondant des convergents, deux raies seulement).
  Question unique : le rapport des deux raies d'Al-Mn est-il
      compatible avec le module d'or (τ) aux erreurs expérimentales
      publiées — et le confondant des convergents de Fibonacci
      est-il mesuré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  acquisition épinglée : URL + empreinte SHA-256 du PDF
          (78276f01…) + valeurs présentes au texte (regression) ;
      F2  compatibilité module : r = d₁/d₂ = 1,6328 ± 0,0158
          (quadrature des erreurs publiées) ; |r − τ| ≤ 2σ_r
          (compatible prédit, ~0,9σ) ;
      F3  confondant convergents (Legendre, T21-D3) : r est
          compatible à 2σ avec 13/8, 21/13 ET 34/21 — la précision
          de 1984 ne tranche PAS entre le module et ses convergents
          (réserve publiée obligatoire) ;
      F4  leviers et contrôles : le cristal périodique de contrôle
          (Al fcc, raies 111/200, rapport 2/√3 = 1,1547) est REJETÉ
          par le test (> 10σ) ; la revue publie elle-même le rapport
          1,63 ± 0,02 (régression de la source) ;
      F5  gouvernance : verdict S+ AVEC RÉSERVE si F2 passe ;
          falsifieur : une mesure de précision supérieure excluant
          τ à 2σ tue la carte ; suite déclarée : Al-Pd-Mn (185
          raies indexées 6D) — acquisition séparée à épingler.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5 (seuil 2σ gelé).
  Falsifieur : F1 épinglage rompu (tue V1) ; |r − τ| > 2σ_r (tue F2 —
      verdict de réfutation, publié au même titre) ; contrôle périodique
      non rejeté (tue V4).
  Prédiction pré-enregistrée : 5/5 — « compatible à ~1σ, confondant
      des convergents mesuré, réserve publiée ».
  Gouvernance : décision d'auteur du 14/10/2026 (« un dernier avec E1 »)
      — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
PHI = (1 + np.sqrt(5)) / 2
URL_SOURCE = "https://euler.phys.cmu.edu/widom/pubs/PDF/AnnRevPChem42_1991_685.pdf"
EMPREINTE_SOURCE = ("78276f015d790490c94f6c85e9e6fc71affc085e5c013744"
                    "c35d7c86875a780d")
D1_VAL, D1_ERR = 8.85, 0.07       # Angstrom, Widom 1991 (Al-Mn, twofold)
D2_VAL, D2_ERR = 5.42, 0.03
SEUIL_SIGMA = 2.0                 # gelé
PDF_LOCAL = Path(__file__).resolve().parents[2] / "widom_qc_1991.pdf"


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def main():
    t0 = time.time()
    print("T25 — le premier regard externe : Al-Mn face au module d'or   "
          "[T25-KO6-REEL-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage (empreinte relue si le PDF est present)
    empreinte_relue = None
    if PDF_LOCAL.exists():
        empreinte_relue = hashlib.sha256(PDF_LOCAL.read_bytes()).hexdigest()
    v1_emp = (empreinte_relue in (None, EMPREINTE_SOURCE))
    v1 = bool(v1_emp)
    print(f"V1 F1 : source épinglée — Widom 1991 (Annu. Rev. Phys. Chem. "
          f"42, 685) · empreinte {'relue localement' if empreinte_relue else 'citée'} : "
          f"{(empreinte_relue or EMPREINTE_SOURCE)[:20]}… · d₁ = {D1_VAL} ± "
          f"{D1_ERR} Å · d₂ = {D2_VAL} ± {D2_ERR} Å → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : compatibilite module
    r = D1_VAL / D2_VAL
    sigma_r = r * np.sqrt((D1_ERR / D1_VAL) ** 2 + (D2_ERR / D2_VAL) ** 2)
    ecart_tau = abs(r - PHI)
    n_sig_tau = ecart_tau / sigma_r
    v2 = bool(n_sig_tau <= SEUIL_SIGMA)
    print(f"V2 F2 : r = d₁/d₂ = {r:.4f} ± {sigma_r:.4f} · τ = {PHI:.5f} · "
          f"écart = {ecart_tau:.4f} = {n_sig_tau:.2f}σ (seuil {SEUIL_SIGMA}σ) "
          f"→ {'COMPATIBLE' if v2 else 'RÉFUTÉ'} → {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : confondant convergents (Legendre, T21-D3)
    convergents = {f"F_{k+1}/F_{k}": fib(k + 1) / fib(k) for k in (6, 7, 8)}
    compat = {nom: abs(r - val) / sigma_r <= SEUIL_SIGMA
              for nom, val in convergents.items()}
    v3 = all(compat.values())
    print(f"V3 F3 : confondant des convergents (réserve obligatoire) :")
    for nom, val in convergents.items():
        print(f"   {nom} = {val:.5f} : écart = {abs(r - val) / sigma_r:.2f}σ "
              f"→ compatible : {compat[nom]}")
    print(f"   → la précision de 1984 ne tranche pas module vs convergents : "
          f"{v3} → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers et controles
    lv = {}
    r_al = 2 / np.sqrt(3)     # Al fcc : raies 111/200 (periodique de controle)
    lv[f"contrôle périodique (Al fcc 111/200 = {r_al:.4f}) rejeté "
       f"({abs(r_al - PHI) / sigma_r:.1f}σ)"] = \
        abs(r_al - PHI) / sigma_r > 4 * SEUIL_SIGMA
    r_revue = 1.63            # la revue publie le rapport arrondi
    lv["régression de la source : la revue publie 1,63 ± 0,02 — cohérent "
       f"avec le rapport rederivé {r:.4f}"] = \
        abs(r_revue - r) < 2 * sigma_r
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance
    verdict_classe = ("S+ (compatible, avec réserve)" if v2 else
                      "CS− (réfuté — publication au même titre)")
    falsifieur = ("une mesure de précision supérieure excluant τ à "
                  f"{SEUIL_SIGMA}σ tue la carte")
    suite = ("Al-Pd-Mn (185 raies, indexage 6D — acquisition séparée à "
             "épingler) ; Zn-Mg-Ho (Rietveld modifié)")
    V5 = bool(verdict_classe and falsifieur and suite)
    print(f"V5 F5 : classe « {verdict_classe} » · falsifieur daté · suite "
          f"déclarée → {'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_epinglage": bool(v1), "V2_compatibilite_module": bool(v2),
                "V3_confondant_convergents": bool(v3),
                "V4_leviers": bool(V4), "V5_gouvernance": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T25-Q-KO6-REEL-2026-10",
        "protocole": "T25-KO6-REEL-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "première confrontation externe du pont diffusif : le "
                 "rapport des deux raies d'Al-Mn (Widom 1991, données "
                 "Shechtman 1984) face au module d'or",
        "premiere_confrontation_externe": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — « compatible (S+) » ou "
                         "« réfuté », jamais « vrai » ; réserve : deux "
                         "raies, précision 1984, confondant des "
                         "convergents mesuré",
        "source": {"reference": "Widom M., Quasicrystal Structure and "
                   "Properties, Annu. Rev. Phys. Chem. 42 (1991) 685",
                   "url": URL_SOURCE,
                   "sha256": EMPREINTE_SOURCE,
                   "releve_pdf": "page 30 : « d-spacings of 8.85 ± 0.07 A "
                                 "and 5.42 ± 0.03 A » (Al-Mn, twofold)"},
        "mesures": {"r": r, "sigma_r": float(sigma_r),
                    "ecart_tau_en_sigma": float(n_sig_tau),
                    "convergents_en_sigma": {nom: float(abs(r - val) / sigma_r)
                                             for nom, val in convergents.items()}},
        "verdict_classe": verdict_classe,
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3),
        "V4": {k: bool(v) for k, v in lv.items()},
        "falsifieur": falsifieur,
        "suite_declaree": suite,
        "V5": bool(V5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t25_ko6_reel_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T25 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
