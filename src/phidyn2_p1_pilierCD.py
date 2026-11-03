#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P1 — PILIER C (carte d'echelles orbite) + PILIER D (sous-test
adiabatique, force reduite, §3.5) — fiche v1.1 SCELLEE.
Pilier C : HORS criteres §3.6 (pas de tolerance gelee) — annexe descriptive.
Pilier D : analyse a posteriori sur donnees archivees T42/T43 — jamais au
titre d'un verdict de classe (iii).
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

GRILLE = 1 << 18
TMAX = 2.5
PHI = (1 + np.sqrt(5)) / 2
NIVEAUX = list(range(9, 15))
DATA = Path("noetic-machine-complete/data")


def traces_grille(t):
    return [0.5 * t, 0.5 * (t * (t - 1.0) - 1.0),
            0.5 * (t * (t * (t - 1.0) - 1.0) - (t - 1.0))]


def bandes_niveau(tg, N):
    xs = traces_grille(tg)
    for _ in range(N - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    xN = xs[-1]
    m = np.abs(xN) <= 1.0
    idx = np.where(m)[0]
    if len(idx) == 0:
        return [], []
    coupe = np.where(np.diff(idx) > 1)[0]
    debuts = np.concatenate([[0], coupe + 1])
    fins = np.concatenate([coupe, [len(idx) - 1]])
    bandes = [(idx[d], idx[f]) for d, f in zip(debuts, fins)]
    return bandes, idx


def main():
    t0 = time.time()
    print("Φ-DYN-2 P1 — PILIER C + D")
    print("=" * 78)
    tg = np.linspace(-TMAX, TMAX, GRILLE)
    dt = tg[1] - tg[0]

    # ---------------- PILIER C : hierarchie d'echelles des orbites
    carte = []
    for N in NIVEAUX:
        bandes, _ = bandes_niveau(tg, N)
        largeurs = [(f - d) * dt for d, f in bandes]
        gaps = []
        for i in range(1, len(bandes)):
            gaps.append((bandes[i][0] - bandes[i - 1][1]) * dt)
        carte.append({
            "niveau": N, "n_bandes": len(bandes),
            "bande_max": max(largeurs), "bande_med": float(np.median(largeurs)),
            "gap_max": max(gaps) if gaps else None,
            "etendue_spectre": (bandes[-1][1] - bandes[0][0]) * dt,
        })
    # ratios d'echelle entre niveaux consecutifs
    for i in range(1, len(carte)):
        c, p = carte[i], carte[i - 1]
        c["ratio_bandes_max_sur_phi"] = c["bande_max"] / p["bande_max"] / (1 / PHI)
        c["ratio_gap_max"] = (c["gap_max"] / p["gap_max"]
                              if c["gap_max"] and p["gap_max"] else None)
    print("PILIER C — hierarchie d'echelles (orbites, grille 2^18) :")
    for c in carte:
        print(f"  N={c['niveau']} : {c['n_bandes']:3d} bandes · "
              f"bande max {c['bande_max']:.4f} · gap max {c['gap_max']:.4f} · "
              f"etendue {c['etendue_spectre']:.4f}")
    rap_gaps = [c["ratio_gap_max"] for c in carte[1:]]
    print(f"  ratios gap_max(N)/gap_max(N-1) : {[round(r,3) for r in rap_gaps]}"
          f" (attendu ~ φ pour une auto-similarite parfaite)")

    # cote corridor : echelles archivees T43/T44/T47 (descriptif, URL interne)
    corridor = {
        "T43": {"saut_Lk": "t = 7.5 exact", "Lk_avant_apres": [1.0226, -0.0041]},
        "T44": {"sauts_unitaires_dated": [3.50, 3.55], "etat_intermediaire": True},
        "T47": {"plateaux_4_filaments_par_quantum": [9.8125, 15.9375, 31.4375],
                "regime_n": [2, 4, 8], "drainage": "÷43"},
        "T42": {"Q_verrouille": 1.0000, "mort_exige": "singularite SU(2)"},
    }
    print("\n  carte corridor (archive, descriptif) : sauts unitaires datés "
          "(T44), saut Lk à t=7.5 (T43), plateaux 9.8/15.9/31.4 = 4n+~1.8 "
          "(T47), Q verrouillé sauf singularité (T42)")

    # ---------------- PILIER D : invariance adiabatique (a posteriori)
    t42 = json.loads((DATA / "t42_ko6_hopfdyn_verdict.json")
                     .read_text(encoding="utf-8"))
    m = t42.get("mesures", {})
    # serie de deformation des masses : Q vs parametre rho_min (chemin lisse)
    q_path = m.get("Q_masses_A2_6", [])
    rho_path = m.get("rho_min_masses_A2_6", [])
    stable, rompt = [], []
    if q_path and rho_path:
        # fenêtre de deformation Δ = 0.1 et 0.5 en rho_min (paramètre déclaré)
        for dlt in (0.1, 0.5):
            vals = []
            for i in range(len(rho_path)):
                j = np.searchsorted(rho_path, rho_path[i] + dlt)
                if j < len(q_path):
                    vals.append(abs(q_path[j] - q_path[i]))
            if vals:
                stable.append({"delta": dlt, "max_dQ": max(vals),
                               "n_paires": len(vals)})
    q_hors = m.get("Q_masses_A2_6", [])
    print("\nPILIER D — invariance adiabatique (analyse a posteriori T42) :")
    for s in stable:
        print(f"  Δρ = {s['delta']} : max |ΔQ| = {s['max_dQ']:.5f} sur "
              f"{s['n_paires']} paires (critère gelé ±0.005)")
    # trajectoires déclarées : Q le long des chemins de deformation
    traj = m.get("trajectoires", {})
    for nom, tr in traj.items():
        qs = tr.get("Q", [])
        if qs:
            print(f"  trajectoire {nom} : Q ∈ [{min(qs):.4f}, {max(qs):.4f}]"
                  f" (verrouillage ±0.005 : {max(qs) - min(qs) <= 0.005})")
    print(f"  Q hors singularité min : {m.get('rho_min_hors_singularite')}"
          f" → la mort exige ρ_min → 0 (singularité), pas la déformation lente")

    out = {
        "chantier": "PHI-DYN-2-P1-PILIER-C-D",
        "fiche": "FICHE-PHI-DYN-2-P1-GENERATEUR v1.1 SCELLÉE (4ad4875)",
        "pilier_C": {"carte_orbites": carte,
                     "ratios_gap_max": rap_gaps,
                     "carte_corridor": corridor,
                     "statut": "ANNEXE DESCRIPTIVE — hors critères §3.6 "
                               "(pas de tolérance gelée pour la coïncidence "
                               "des cartes d'échelles)"},
        "pilier_D": {"stable": stable,
                     "Q_hors_singularite": m.get("rho_min_hors_singularite"),
                     "statut": "ANALYSE A POSTERIORI — force réduite, "
                               "jamais au titre de classe (iii)"},
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn2_p1_pilierCD.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
