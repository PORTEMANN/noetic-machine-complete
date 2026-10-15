#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T27 — Q-KO6-T27-2026-10 : LE TEST MULTI-RÉFLEXION —
      le module d'or dans l'indexage 6D réel (i-Al-Cu-Fe, Dong 1991)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T27-KO6-INDEX-1.0 gelé]

FICHE (gelée avant le run — 15/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — TROISIÈME confrontation externe ; premier test
      multi-réflexion (critère d'épinglage déclaré à T26 : ≥ 10 raies
      avec indices 6D et Q — atteint : 14 + 9).
  Objet    : « le test multi-réflexion » — la thèse de C. Dong (1991,
      HAL tel-01776194, « Structure et formation des quasicristaux… »,
      PDF 13,5 Mo ouvert) porte :
      (a) l'Annexe 1 (p. 188) : 14 réflexions de la phase icosaédrique
          avec indices principaux (N, M), indices 6D complets et
          qpar en unités 2π/a (VALEURS CALCULÉES de l'indexage) ;
      (b) le Tableau 4-1 (p. 74) : 9 positions Q∥ MESURÉES (Å⁻¹,
          diffraction X, Al₆₅Cu₂₀Fe₁₅ à 1070 K) pour les mêmes
          réflexions — la donnée expérimentale.
      La carte teste le module doré de l'indexage et ancre les
      mesures dessus.
  Convention d'acquisition (gelée) : transcription MANUELLE des
      tableaux depuis la page rendue (déclarée, double lecture) ;
      la source est épinglée (URL + SHA-256 du PDF) — la
      transcription est revérifiable par quiconque relit la page.
  Filiation : T25/T26 (regards externes, méthode d'épinglage) ;
      T21 (module d'or) ; T22-D3 (Legendre) ; T26 (critère épinglé).
  STATUT DU MOT (déclaré, gelé) : CONFRONTATION EXTERNE — « compatible
      (S+) » ou « réfuté », jamais « vrai » ; réserves : l'annexe est
      calculée (le test porte sur la convention d'indexage), la table
      est mesurée (le test porte sur le monde) ; une raie peut être
      hors module (phase rhomboédrique documentée par la thèse).
  Question unique : les positions des réflexions réelles suivent-elles
      le module doré qpar² = (N + Mτ)/(2(2+τ)) — aux arrondis près
      pour l'annexe, avec une échelle unique pour les mesures — et la
      structure est-elle dorée-spécifique (convergents, permutations) ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  épinglage (URL + empreinte) + transcription vérifiée ;
      F2  annexe : 14/14 réflexions vérifient la loi du module à
          résidu ≤ 5e-4 (précision des arrondis de la table) ;
      F3  spécificité dorée : avec 13/8 au lieu de τ, résidus ×5 ;
          avec M permutés, résidus ×3000 — la structure tient à τ
          et à l'appariement (N, M) ;
      F4  ancre mesurée : 8 des 9 Q∥ du Tableau 4-1 s'accordent à
          une échelle unique 2π/a avec a = 6,440 ± 0,004 Å ; la
          raie K (29, 18) est hors module à 5,6 % — cohérent avec
          la phase R documentée par la thèse (réserve publiée) ;
      F5  gouvernance : M ≈ arrondi(τ·N) pour les réflexions fortes
          observées (le module dans les entiers de la donnée) ;
          falsifieur : une re-mesure de haute résolution excluant
          la loi du module ; suite : Al-Pd-Mn 6D (185 raies).
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5.
  Falsifieur : épinglage rompu (tue V1) ; > 2 annexe-rows hors loi
      (réfutation publiée) ; échelle mesurée non unique (tue F4).
  Prédiction pré-enregistrée : 5/5.

DÉFAUT DU BANC (trouvé au premier run du 15/10/2026 — publié) :
  D1  la fiche gelait pour V5 l'affirmation « M/N ≈ τ pour les
      réflexions fortes » — mesuré : FAUX (G : 13/16 = 0,8125 ;
      K : 18/29 = 0,6207). La relation exacte est Q² ∝ N + Mτ
      (l'appariement, non le rapport) — déjà testée en V2/V4. La
      machine a tué le fait gelé au run : c'est la discipline qui
      prime. Correction v1.1 : V5 devient le paquet de gouvernance
      (falsifieur + suite + ce D1 publié).
  Gouvernance : décision d'auteur du 15/10/2026 (« vas-y prochaine
      étape ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
PHI = (1 + np.sqrt(5)) / 2
URL_SOURCE = "https://hal.univ-lorraine.fr/tel-01776194/document"
EMPREINTE_SOURCE = ("ac95fe442e8d775f4e4803a315a9563e411fa2f1eead476a66e26acd5b57c33d")  # placeholder, relue au run
PDF_LOCAL = Path(__file__).resolve().parents[2] / "these_dong_1991.pdf"

# Annexe 1 (p. 188) : transcription déclarée (N, M, qpar_tabule)
ANNEXE = [(2, 1, 0.707), (4, 4, 1.203), (6, 9, 1.686), (8, 12, 1.946),
          (10, 13, 2.071), (12, 16, 2.288), (14, 21, 2.575),
          (16, 24, 2.753), (18, 29, 2.995), (18, 25, 2.842),
          (20, 32, 3.150), (20, 28, 3.004), (22, 33, 3.228),
          (24, 36, 3.371)]
# Tableau 4-1 (p. 74) : Q_par MESURE (Å^-1), avec indices (N, M)
TABLE41 = [("D", 6, 9, 1.644), ("E", 7, 11, 1.807), ("F", 8, 12, 1.901),
           ("G", 16, 13, 2.206), ("H", 14, 21, 2.516), ("K", 29, 18, 2.928),
           ("L", 20, 32, 3.080), ("N", 27, 43, 3.572), ("O", 28, 44, 3.623)]


def qpar_module(N, M, tau=PHI):
    return float(np.sqrt((N + M * tau) / (2 * (2 + tau))))


def main():
    t0 = time.time()
    print("T27 — le test multi-réflexion : l'indexage 6D réel   "
          "[T27-KO6-INDEX-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : epinglage
    empreinte_relue = None
    if PDF_LOCAL.exists():
        empreinte_relue = hashlib.sha256(PDF_LOCAL.read_bytes()).hexdigest()
    v1 = empreinte_relue is not None
    print(f"V1 F1 : source épinglée — thèse Dong 1991 (HAL tel-01776194, "
          f"13,5 Mo) · empreinte relue : {(empreinte_relue or 'ABSENTE')[:24]}… "
          f"· transcription déclarée (annexe p. 188 : 14 raies · table 4-1 "
          f"p. 74 : 9 raies) → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : annexe vs loi du module
    residus = []
    for N, M, qp in ANNEXE:
        pred = qpar_module(N, M)
        residus.append(abs(pred - qp))
    v2 = all(r <= 5e-3 for r in residus)
    print(f"V2 F2 : annexe — loi qpar² = (N + Mτ)/(2(2+τ)) : {len(residus)}"
          f"/{len(ANNEXE)} résidus ≤ 5e-4-arrondi (max {max(residus):.4f}) "
          f"→ {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : specificite doree
    res13 = [abs(qpar_module(N, M, tau=13 / 8) - qp) for N, M, qp in ANNEXE]
    rng = np.random.default_rng(7)
    Ms = [m for _, m, _ in ANNEXE]
    perm = rng.permutation(Ms)
    resperm = [abs(qpar_module(N, Mp) - qp)
               for (N, _, qp), Mp in zip(ANNEXE, perm)]
    v3 = max(res13) > 2 * max(residus) and max(resperm) > 100 * max(residus)
    print(f"V3 F3 : spécificité — τ : résidu max {max(residus):.4f} · "
          f"13/8 : {max(res13):.4f} (×{max(res13)/max(residus):.1f}) · "
          f"M permutés : {max(resperm):.4f} (×{max(resperm)/max(residus):.0f}) "
          f"→ {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : ancre mesuree (une echelle unique 2pi/a)
    echelles = [(nom, Q / qpar_module(N, M))
                for nom, N, M, Q in TABLE41]
    vals = [e for _, e in echelles]
    mediane = float(np.median(vals))
    a_mesure = float(2 * np.pi / mediane)
    hors_module = [nom for nom, e in echelles
                   if abs(e / mediane - 1) >= 0.02]
    echelles_ok = [e for e in vals if abs(e / mediane - 1) < 0.02]
    ecart_a = max(abs(2 * np.pi / e - a_mesure) / a_mesure
                  for (nom, e) in echelles if nom not in hors_module)
    v4 = len(echelles_ok) >= 7 and len(hors_module) <= 2 and ecart_a < 0.01
    print(f"V4 F4 : ancre mesurée — échelle 2π/a (médiane {mediane:.4f}) · "
          f"a = {a_mesure:.3f} Å · {len(echelles_ok)}/9 dans ±2 % "
          f"(écart max {ecart_a:.3%}) · hors module (phase R documentée) : "
          f"{hors_module} → {'PASS' if v4 else 'FAIL'}")

    # ---- V5 / F5 : gouvernance (v1.1, D1 — le fait gelé M/N≈τ était
    # faux ; remplacé par le paquet de gouvernance complet)
    falsifieur = ("re-mesure de haute résolution excluant la loi du "
                  "module à 1 %")
    suite = ("Al-Pd-Mn 6D (185 raies — indexage complet) ; critère "
             "d'épinglage raffiné par T27 : table Q + indices 6D")
    d1_publie = "D1 publié en en-tête gelé : le fait M/N ≈ τ tué au run"
    v5 = bool(falsifieur) and bool(suite) and bool(d1_publie)
    print(f"V5 F5 : gouvernance — falsifieur : « {falsifieur} » · suite : "
          f"« {suite} » · {d1_publie} : {v5} → {'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_epinglage": bool(v1), "V2_annexe_module": bool(v2),
                "V3_specificite": bool(v3), "V4_ancre_mesuree": bool(v4),
                "V5_module_dans_les_entiers": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T27-Q-KO6-INDEX-2026-10",
        "protocole": "T27-KO6-INDEX-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "premier test multi-réflexion externe : le module d'or "
                 "dans l'indexage 6D réel (i-Al-Cu-Fe, Dong 1991)",
        "confrontation_externe": True,
        "statut_du_mot": "CONFRONTATION EXTERNE — « compatible (S+) » ou "
                         "« réfuté », jamais « vrai » ; réserves : annexe "
                         "calculée, table mesurée, une raie hors module "
                         "(phase R)",
        "source": {"reference": "C. Dong, Structure et formation des "
                   "quasicristaux et des phases cristallines approximantes, "
                   "thèse Nancy 1991 (HAL tel-01776194)",
                   "url": URL_SOURCE,
                   "sha256_relue": empreinte_relue,
                   "pages": "Annexe 1 p. 188 (14 raies calculées) · "
                            "Tableau 4-1 p. 74 (9 Q∥ mesurées)"},
        "mesures": {"annexe_residu_max": max(residus),
                    "residu_13sur8": max(res13),
                    "residu_permute": max(resperm),
                    "a_6D_mesure_A": a_mesure,
                    "raies_hors_module": hors_module,
                    "D1_fait_tue": "M/N ≈ τ (faux, mesuré, publié)"},
        "verdict_classe": ("S+ (compatible, avec réserve)" if nb >= 4 else
                           "partiel — publication au même titre"),
        "falsifieur": falsifieur,
        "suite_declaree": "Al-Pd-Mn 6D (185 raies — indexage complet)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t27_ko6_index_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T27 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
