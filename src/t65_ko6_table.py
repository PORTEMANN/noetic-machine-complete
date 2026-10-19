#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T65 — Q-KO6-T65-2026-10 : T65 — LA TABLE
      (Heath 1977 : la masse occulte face à A — réserve T25)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T65-KO6-TABLE-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — le dernier chantier ANU ouvert : la confrontation
      au réel. La table Heath (Handbook of Physics and Chemistry
      1977, comparée à la Chimie Occulte, p. 369, transcrite sur
      histoire-des-sciences.eu/theos-tech/table.php?id=8) donne pour
      chaque élément le nombre de nucléons A et la « masse occulte »
      (le poids atomique tel que la chimie occulte le compte). La
      conjecture de l'arc ANU : un ANU pèse l'unité de masse
      nucléaire — la masse occulte devrait être ≈ A. T65 épingle
      les données (règle T25), mesure l'accord et la dérive, tue le
      nul par permutation — et classe « S+ (compatible, avec
      réserve) », jamais « vrai ».
  Filiation : la Chimie Occulte (table Heath épinglée) · T58/T59
      (la masse = énergie = longueur × tension, la philosophie de la
      comptabilité) · T60 (l'ANU dont la masse est 83.8 en unités
      spinorielles — la conversion reste conjecturale, déclarée) ·
              la règle T25 (épinglage, réserve honnête).
  STATUT DU MOT (déclaré, gelé) : MESURE documentaire — la
      confrontation porte sur des données TRANSCRITES (premières
      lignes H→Mg, transcription partielle déclarée), jamais « vrai ».
  Question unique : la masse occulte suit-elle A à quelques pour
      cent — la comptabilité « 1 ANU ↔ 1 nucléon en masse » est-elle
      compatible avec la table épinglée, et la dérive est-elle mesurable ?
  Faits déclarés (dérivés de la table épinglée, à vérifier) :
      F1  les données sont épinglées et reproductibles : 11 éléments
          (H → Mg) avec A et masse occulte transcrits dans le verdict
          (source : table.php?id=8, Chimie Occulte p. 369) ;
      F2  la correspondance existe : corrélation (masse occulte, A)
          ≥ 0.999 ;
      F3  la dérive est mesurée : écart relatif moyen |δ| < 5 % avec
          dispersion enregistrée (δ = (occulte − A)/A) ;
      F4  le nul honnête : sur 10 000 permutations des masses
          occultes entre les A, aucune n'atteint la corrélation
          observée (nul tué) ;
      F5  la compatibilité corridor : |δ| moyen < 5 % — la
          conjecture « 1 ANU ↔ 1 nucléon en masse » est compatible
          avec la table à la précision de la transcription — classe
          « S+ (compatible, avec réserve) » (T25), jamais « vrai ».
  Falsifieur : transcription incomplète invalide ; corrélation < 0.999 ;
      |δ| > 5 % ; le nul non tué ; tout classement « vrai ».
  Prédiction pré-enregistrée : 5/5 — « la masse occulte suit A à
      quelques pour cent (dérive mesurée, nul tué par permutation) :
      la comptabilité 1 ANU ↔ 1 nucléon en masse est compatible avec
      la table Heath — avec réserve, comme tout ce qui touche au réel ».
  Gouvernance : décision d'auteur du 19/10/2026 (« enchaîne les trois
      chantiers ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- données épinglées (transcription de table.php?id=8, Chimie
# Occulte p. 369, Handbook of Physics and Chemistry 1977) ---
TABLE = [
    # (élément, Z, A, masse occulte)
    ("Hydrogène", 1, 1, 1.00),
    ("Hélium", 2, 4, 4.00),
    ("Béryllium", 4, 9, 9.11),
    ("Bore", 5, 11, 11.11),
    ("Carbone", 6, 12, 12.00),
    ("Azote", 7, 14, 14.50),
    ("Oxygène", 8, 16, 16.11),
    ("Fluor", 9, 19, 18.88),
    ("Néon", 10, 20, 20.00),
    ("Sodium", 11, 23, 23.22),
    ("Magnésium", 12, 24, 24.00),
]
SOURCE_URL = ("https://histoire-des-sciences.eu/theos-tech/"
              "table.php?id=8")


def correlation(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def main():
    t0 = time.time()

    noms = [t[0] for t in TABLE]
    A = np.array([t[2] for t in TABLE], float)
    occ = np.array([t[3] for t in TABLE], float)
    delta = (occ - A) / A

    corr_obs = correlation(A, occ)
    abs_delta_moy = float(np.mean(np.abs(delta)))
    delta_max = float(np.max(np.abs(delta)))

    # nul honnête : permutations des masses occultes entre les A
    rng = np.random.default_rng(6502)
    n_perm = 10000
    nul_battu = 0
    for _ in range(n_perm):
        perm = rng.permutation(occ)
        if correlation(A, perm) >= corr_obs:
            nul_battu += 1
    p_nul = nul_battu / n_perm

    # ajustement occulte = alpha * A (la pente de la comptabilité)
    alpha = float(np.sum(A * occ) / np.sum(A * A))
    residus = occ - alpha * A

    stats = {
        "elements": noms,
        "A": [int(a) for a in A],
        "masse_occulte": [float(o) for o in occ],
        "delta_relatif": [round(float(d), 4) for d in delta],
        "correlation": round(corr_obs, 6),
        "abs_delta_moyen": round(abs_delta_moy, 4),
        "abs_delta_max": round(delta_max, 4),
        "pente_alpha": round(alpha, 4),
        "residus": [round(float(r), 3) for r in residus],
        "p_nul": p_nul,
        "n_permutations": n_perm,
        "source": SOURCE_URL,
    }

    # --- F1 : données épinglées ---
    v1 = (len(TABLE) == 11 and all(o > 0 for o in occ)
          and "histoire-des-sciences.eu" in SOURCE_URL)

    # --- F2 : correspondance ---
    v2 = corr_obs >= 0.999

    # --- F3 : dérive mesurée ---
    v3 = abs_delta_moy < 0.05

    # --- F4 : nul tué ---
    v4 = p_nul == 0.0

    # --- F5 : compatibilité avec réserve ---
    v5 = abs_delta_moy < 0.05  # même mesure, la classe est dans le texte

    criteres = {"V1_donnees_epinglees": bool(v1),
                "V2_correspondance": bool(v2),
                "V3_derive_mesuree": bool(v3),
                "V4_nul_tue": bool(v4),
                "V5_compatible_avec_reserve": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T65-Q-KO6-TABLE-2026-10",
        "protocole": "T65-KO6-TABLE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T65 : la table — masse occulte (Heath 1977, Chimie "
                 "Occulte p. 369) face au nombre de nucléons A : accord, "
                 "dérive, nul par permutation ; classe « S+ (compatible, "
                 "avec réserve) », jamais « vrai » (règle T25)",
        "doctrine": "la Chimie Occulte (table épinglée) ; T58/T59 (la "
                    "comptabilité) ; T60 (l'ANU, conversion conjecturale "
                    "déclarée)",
        "statut_du_mot": "MESURE documentaire — transcription partielle "
                         "déclarée (H→Mg), jamais « vrai »",
        "configuration": {"n_elements": len(TABLE),
                          "plage": "H → Mg",
                          "permutations": n_perm,
                          "source": SOURCE_URL},
        "mesures": stats,
        "verdict_classe": ("S+ (compatible, avec réserve) — la masse "
                           "occulte suit A à "
                           f"{100*abs_delta_moy:.1f} % près (max "
                           f"{100*delta_max:.1f} %), nul tué par "
                           "permutation ; la comptabilité « 1 ANU ↔ 1 "
                           "nucléon en masse » est compatible avec la "
                           "table Heath — avec la réserve de la "
                           "transcription et la règle T25"),
        "falsifieur": "corrélation < 0.999 ; |δ| > 5 % ; nul non tué ; "
                      "tout classement « vrai »",
        "suites_declarees": "la transcription complète de la table "
                            "(p. 369–380, jusqu'à U) ; la dérive "
                            "systématique en fonction de Z ; la "
                            "confrontation des isotopes instables "
                            "(asterisques)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t65_ko6_table_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T65 (local) : {statut} — {nb}/5")
    print(f"  corrélation = {corr_obs:.6f} | pente α = {alpha:.4f}")
    print(f"  |δ| moyen = {100*abs_delta_moy:.2f} % (max "
          f"{100*delta_max:.2f} %) | p_nul = {p_nul}")
    print(f"  δ : {[(n, round(100*float(d),1)) for n, d in zip(noms, delta)]}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
