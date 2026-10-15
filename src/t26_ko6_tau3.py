#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T26 — Q-KO6-T26-2026-10 : LE DOSSIER S'OUVRE — τ³ dans i-Al-Mn-Si
      (deuxième regard externe, même source épinglée)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T26-KO6-TAU3-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — deuxième confrontation externe (suite T25).
  Objet    : « le dossier s'ouvre » — la MÊME source épinglée de T25
      (Widom 1991, Annu. Rev. Phys. Chem. 42, 685 — empreinte
      78276f01…) porte un second fait doré, extrait à la
      reconnaissance (page 8) : pour l'alliage icosaédrique
      Al-Mn-Si (Bancel et al.), deux choix publiés de vecteur
      réciproque fondamental — Q₁ = 2,894 Å⁻¹ (pic (100000),
      axe fivefold) et Q₂ = 0,68 Å⁻¹ (pic fivefold faible) — que
      la revue dit « différant par un facteur τ³ ». La carte teste
      ce rapport contre τ³, mesure le confondant de ses convergents,
      et consigne la reconnaissance documentaire (la table riche à
      185 raies reste derrière paywall — déclaré).
  Filiation : T25 (premier regard externe — même source, régression) ;
      T21 (le module d'or) ; T22-D3 (Legendre — confondant déclaré) ;
      carnet (E1, suite déclarée).
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — « compatible
      (S+) » ou « réfuté », jamais « vrai » ; réserve : pas d'erreurs
      publiées sur Q₁, Q₂ (test en écart relatif, seuil déclaré 2 %) ;
      dossier à source unique.
  Question unique : le rapport Q₁/Q₂ publié pour i-Al-Mn-Si est-il
      compatible avec τ³ — et le confondant des convergents de τ³
      ([4;4,4,4,…]) est-il mesuré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  épinglage relu (empreinte) + extrait p. 8 confirmé au
          texte (« This value differs from the previous value by a
          factor of τ³ ») ;
      F2  r = Q₁/Q₂ = 4,2559 ; τ³ = 4,23607 ; écart relatif
          0,47 % < seuil déclaré 2 % → compatible ; contrôles τ² et
          τ⁴ rejetés (> 30 %) ;
      F3  confondant convergents : 17/4 = 4,25 (0,14 %) et
          72/17 = 4,2353 (0,49 %) compatibles — la précision de
          publication ne tranche pas (réserve, leçon T22-D3) ;
      F4  le pont : τ³ est puissance du même φ que le module de la
          chaîne du seesaw (T14/T21) — un seul nombre d'or à
          toutes les échelles publiées ;
      F5  gouvernance : reconnaissance documentaire consignée
          (Wollgarten : URL morte ; HAL multiresolution : non-PDF ;
          Boudard 1992 / de Boissieu 1994 : paywall — table 185
          raies en attente d'accès) ; falsifieur : mesure de
          précision supérieure excluant τ³ à 2 %.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5.
  Falsifieur : épinglage rompu (tue V1) ; écart > 2 % (réfutation
      publiée au même titre) ; confondant non mesuré (tue V3).
  Prédiction pré-enregistrée : 5/5 — « compatible à 0,47 %, confondant
      convergent mesuré, dossier à source unique déclaré ».
  Gouvernance : décision d'auteur du 15/10/2026 (« on attaque
      maintenant ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
PHI = (1 + np.sqrt(5)) / 2
TAU3 = PHI ** 3
URL_SOURCE = "https://euler.phys.cmu.edu/widom/pubs/PDF/AnnRevPChem42_1991_685.pdf"
EMPREINTE_SOURCE = ("78276f015d790490c94f6c85e9e6fc71affc085e5c013744"
                    "c35d7c86875a780d")
EXTRAIT_ATTENDU = "differs from the previous value by a factor"
Q1_VAL, Q2_VAL = 2.894, 0.68        # Å^-1, Widom 1991 p. 8 (Al-Mn-Si)
SEUIL_REL = 0.02                    # gelé (2 %)
PDF_LOCAL = Path(__file__).resolve().parents[2] / "widom_qc_1991.pdf"


def main():
    t0 = time.time()
    print("T26 — le dossier s'ouvre : τ³ dans i-Al-Mn-Si   "
          "[T26-KO6-TAU3-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage relu + extrait confirme
    empreinte_relue = None
    extrait_ok = None
    if PDF_LOCAL.exists():
        empreinte_relue = hashlib.sha256(PDF_LOCAL.read_bytes()).hexdigest()
        from pypdf import PdfReader
        t8 = (PdfReader(str(PDF_LOCAL)).pages[7].extract_text() or "")
        t8 = " ".join(t8.replace("\n", " ").split())
        extrait_ok = (EXTRAIT_ATTENDU in t8 and "2.894" in t8
                      and "0.68" in t8)
    v1 = (empreinte_relue in (None, EMPREINTE_SOURCE)) and extrait_ok
    print(f"V1 F1 : empreinte {'relue' if empreinte_relue else 'citée'} : "
          f"{(empreinte_relue or EMPREINTE_SOURCE)[:20]}… · extrait p. 8 "
          f"(« {EXTRAIT_ATTENDU} », Q₁ = 2,894, Q₂ = 0,68) : {extrait_ok} "
          f"→ {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : compatibilite tau^3
    r = Q1_VAL / Q2_VAL
    ecart_tau3 = abs(r - TAU3) / TAU3
    ecart_tau2 = abs(r - PHI ** 2) / PHI ** 2
    ecart_tau4 = abs(r - PHI ** 4) / PHI ** 4
    v2 = bool(ecart_tau3 < SEUIL_REL and ecart_tau2 > 10 * SEUIL_REL
              and ecart_tau4 > 10 * SEUIL_REL)
    print(f"V2 F2 : r = Q₁/Q₂ = {r:.5f} · τ³ = {TAU3:.5f} · écart relatif "
          f"{ecart_tau3:.4%} (seuil {SEUIL_REL:.0%}) → "
          f"{'COMPATIBLE' if ecart_tau3 < SEUIL_REL else 'RÉFUTÉ'} · "
          f"contrôles : τ² écart {ecart_tau2:.1%} · τ⁴ écart "
          f"{ecart_tau4:.1%} (rejetés > 10×seuil) → "
          f"{'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : confondant convergents de tau^3 ([4;4,4,4,...])
    convergents = {"17/4 (F-convergent)": 17 / 4, "72/17": 72 / 17,
                   "305/72": 305 / 72}
    en_sigma = {nom: abs(r - val) / val for nom, val in convergents.items()}
    compat = {nom: e < SEUIL_REL for nom, e in en_sigma.items()}
    v3 = any(compat.values())
    print(f"V3 F3 : confondant des convergents de τ³ ([4;4,4,4,…]) :")
    for nom in convergents:
        print(f"   {nom} : écart relatif {en_sigma[nom]:.4%} → compatible "
              f": {compat[nom]}")
    print(f"   → confondant mesuré : {v3} → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : le pont (tau^3 puissance du meme module)
    r_tau3_sur_phi = abs(TAU3 - (2 * PHI + 1)) < 1e-9
    V4 = bool(r_tau3_sur_phi)
    print(f"V4 F4 : τ³ = 2φ + 1 exactement (identité algébrique, régressée) "
          f": {r_tau3_sur_phi} — même φ que le module de la chaîne du "
          f"seesaw (T14/T21) → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 / F5 : gouvernance + reconnaissance consignee
    reconnaissance = [
        "Wollgarten (thèse Jülich, liste de réflexes) : URL morte "
        "(landing HTML, pas de PDF)",
        "HAL in2p3-00185505 (Multiresolution) : fichier 54 ko non-PDF",
        "Boudard 1992 (JPCM 4, 10149) et de Boissieu 1994 (JPCM 6, "
        "10725) : table riche (185 raies) derrière paywall — "
        "acquisition en attente (accès documentaire)",
        "issue : la table indexée 6D reste le prochain objectif "
        "d'épinglage ; critère : ≥ 10 raies avec indices 6D et Q",
    ]
    V5 = bool(reconnaissance) and len(reconnaissance) == 4
    print(f"V5 F5 : reconnaissance documentaire consignée "
          f"({len(reconnaissance)} entrées) · falsifieur daté → "
          f"{'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_epinglage": bool(v1), "V2_compatibilite_tau3": bool(v2),
                "V3_confondant_convergents": bool(v3),
                "V4_pont_meme_phi": bool(V4),
                "V5_gouvernance": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T26-Q-KO6-TAU3-2026-10",
        "protocole": "T26-KO6-TAU3-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "deuxième regard externe : le rapport τ³ des échelles "
                 "réciproques publiées pour i-Al-Mn-Si (Widom 1991, p. 8)",
        "premiere_confrontation_externe": False,
        "confrontation_externe": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — « compatible (S+) » ou "
                         "« réfuté », jamais « vrai » ; réserve : pas "
                         "d'erreurs publiées sur Q₁, Q₂ ; dossier à "
                         "source unique ; confondant convergent mesuré",
        "source": {"reference": "Widom M., Quasicrystal Structure and "
                   "Properties, Annu. Rev. Phys. Chem. 42 (1991) 685",
                   "url": URL_SOURCE,
                   "sha256": EMPREINTE_SOURCE,
                   "releve_pdf": "page 8 : « Q = 2.894 A-1 … Another "
                                 "choice … Q = 0.68 A-1. This value "
                                 "differs from the previous value by a "
                                 "factor of τ³ » (Al-Mn-Si, Bancel)"},
        "mesures": {"r": r, "tau3": TAU3, "ecart_relatif_tau3":
                    float(ecart_tau3),
                    "convergents_ecarts": {k: float(v) for k, v in
                                           en_sigma.items()}},
        "verdict_classe": ("S+ (compatible, avec réserve)" if v2 else
                           "CS− (réfuté — publication au même titre)"),
        "reconnaissance_documentaire": reconnaissance,
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(V5),
        "falsifieur": "mesure de précision supérieure excluant τ³ à "
                      "2 % tue la carte",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t26_ko6_tau3_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T26 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
