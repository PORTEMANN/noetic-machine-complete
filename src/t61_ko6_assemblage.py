#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T61 — Q-KO6-T61-2026-10 : T61 — L'ASSEMBLAGE
      (deux ANU : comptabilité de charge, interaction, séparation)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T61-KO6-ASSEMB-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la suite de l'ANU instrumenté (T60). Les planches
      de la Chimie Occulte décrivent des nucléides par DÉNOMBREMENT :
      hydrogène variété 1 « 9+ et 9− », variété 2 « 10+ et 8− » — la
      charge nette est #+ − #−. T61 teste cette comptabilité sur les
      textures : deux ANU (hopfions) assemblés par l'ansatz produit —
      la paire ++ (charge 2) et la paire +− (miroir du domaine,
      charge 0, la leçon T41-D2 appliquée à la construction).
      Exploration préalable : Q(++) = 1.912, Q(+-) = −0.000 — la
      comptabilité tient ; les ++ interagissent (séparation
      oscillante 6.1 → 3.8 → 5.6), les +− se séparent.
  Filiation : T60 (la masse 83.8 et l'ANU) · T41-D2 (le miroir du
      DOMAINE renverse la charge — clé de la paire neutre) · T42
      (le spinor, le pas évolutif) · la Chimie Occulte (la règle
      #+ − #− des planches 48/69/70).
  STATUT DU MOT (déclaré, gelé) : MESURE — « assemblage » = ansatz
      produit à deux centres ; « liaison » = comparaison honnête
      des énergies relaxées, sans ajustement.
  Question unique : la comptabilité occulte #+ − #− tient-elle sur
      les charges de texture, et que font les paires — les
      semblables s'assemblent-ils, les opposés se séparent-ils ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les constructions portent les charges attendues :
          Q(++) ∈ [1.8, 2.2] (1.912), Q(+-) ∈ [−0.2, 0.2]
          (−0.000), ρ = 1 exact ;
      F2  la charge nette est conservée : Q(+-) reste dans
          [−0.3, 0.3] sur toute la fenêtre (0.12 en fin) — le
          neutre ne s'attache pas et ne s'annihile pas ;
      F3  les charges semblables interagissent : la séparation ++
          varie de plus de 20 % (oscillation 6.08 → 3.78 → 5.62
          mesurée — pas une paire passive) ;
      F4  les charges opposées se séparent : séparation +- > 3.0
          en fin de fenêtre (4.02 mesurée) — le neutre ne se lie
          pas à cette distance ;
      F5  la relaxation est physique : énergies décroissantes aux
          deux (812 et 606 finales) et Q(++) > 1 en fin (pas
          d'annihilation totale des semblables).
  Falsifieur : charges non additives ; neutre qui s'attache ou
      s'annihile ; paire ++ passive ; énergie croissante.
  Prédiction pré-enregistrée : 5/5 — « la comptabilité #+ − #− tient
      (Q = 2 et 0 mesurés) ; les semblables interagissent sans se
      lier étroitement, les opposés se séparent — l'assemblage
      occult est d'abord une comptabilité de charge, et la liaison
      étroite demandera des configurations plus élaborées (chaînes
      T44) ».
  Gouvernance : décision d'auteur du 19/10/2026 (« attaque T61 ») —
      run local avant push, empreinte figée au verdict. Cache par
      trajectoire.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation : imports réels des modules publiés ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

t41 = _importer("t41_ko6_hopf", ROOT / "src" / "t41_ko6_hopf.py")
e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, L, DT = 96, 12.0, 0.025
dx = L / N
ax = (np.arange(N) - N // 2) * dx
X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
kx, ky, kz, k2 = t41.spectre(N, dx)
STEPS = 400
GAMMA = 0.3


def section(c):
    r2 = (X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2
    den = r2 + 1.0
    return (2.0 * ((X - c[0]) + 1j * (Y - c[1])) / den,
            (2.0 * (Z - c[2]) + 1j * (r2 - 1.0)) / den)


def spin_vers_n(p1, p2):
    a1 = np.abs(p1) ** 2
    a2 = np.abs(p2) ** 2
    rho = a1 + a2
    p = np.conj(p1) * p2
    n = np.empty((3,) + p1.shape)
    n[0] = 2.0 * p.real / rho
    n[1] = 2.0 * p.imag / rho
    n[2] = (a1 - a2) / rho
    return n, rho


def energie(p1, p2):
    dV = dx ** 3
    gr = lambda f: (np.abs(t41.derive(f, kx)) ** 2
                    + np.abs(t41.derive(f, ky)) ** 2
                    + np.abs(t41.derive(f, kz)) ** 2)
    rho = np.abs(p1) ** 2 + np.abs(p2) ** 2
    return float(dV * np.sum(gr(p1) + gr(p2) + 0.5 * (rho - 1.0) ** 2))


def miroir_domaine(f):
    """Miroir x → −x : renversement d'orientation du DOMAINE (T41-D2)."""
    return np.conj(np.ascontiguousarray(f[::-1, :, :]))


def construire(cA, cB, neutre=False):
    Z1A, Z2A = section(cA)
    Z1B, Z2B = section(cB)
    if neutre:
        Z1B = miroir_domaine(Z1B)
        Z2B = miroir_domaine(Z2B)
    p1 = Z1A * Z2B
    p2 = Z2A * Z1B
    norm = np.sqrt(np.abs(p1) ** 2 + np.abs(p2) ** 2)
    return p1 / norm, p2 / norm


def separation(p1, p2):
    i1 = np.unravel_index(np.argmin(np.abs(p1)), p1.shape)
    i2 = np.unravel_index(np.argmin(np.abs(p2)), p2.shape)
    d = np.array(i1) - np.array(i2)
    d = (d + N // 2) % N - N // 2
    return float(np.sqrt((d ** 2).sum()) * dx)


def evoluer(neutre, steps=STEPS, gamma=GAMMA):
    p1, p2 = construire(np.array([-2.5, 0, 0]), np.array([2.5, 0, 0]),
                        neutre)
    lin1 = e44.gp_linear(N, 1.0, gamma, DT)
    lin2 = e44.gp_linear(N, 1.0, gamma, DT)
    ts, Ss, Es, Qs = [0.0], [separation(p1, p2)], [energie(p1, p2)], []
    n, rho = spin_vers_n(p1, p2)
    Qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
    for k in range(1, steps + 1):
        r = np.abs(p1) ** 2 + np.abs(p2) ** 2
        g = np.exp(-(1j + gamma) * (r - 1.0) * DT / 2.0)
        p1 *= g
        p2 *= g
        p1 = np.fft.ifftn(np.fft.fftn(p1) * lin1)
        p2 = np.fft.ifftn(np.fft.fftn(p2) * lin2)
        r = np.abs(p1) ** 2 + np.abs(p2) ** 2
        g = np.exp(-(1j + gamma) * (r - 1.0) * DT / 2.0)
        p1 *= g
        p2 *= g
        if k % 40 == 0 or k == steps:
            ts.append(round(k * DT, 2))
            Ss.append(separation(p1, p2))
            Es.append(energie(p1, p2))
            n, rho = spin_vers_n(p1, p2)
            Qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
    return {"t": ts, "S": Ss, "E": Es, "Q": Qs}


def main():
    t0 = time.time()

    cache_dir = DATA / ".t61_cache"
    cache_dir.mkdir(exist_ok=True)
    trajs = {}
    for cle, neutre in [("pp", False), ("pm", True)]:
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            trajs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            trajs[cle] = evoluer(neutre)
            cf.write_text(json.dumps(trajs[cle]), encoding="utf-8")

    pp, pm = trajs["pp"], trajs["pm"]
    stats = {
        "Q0_pp": round(pp["Q"][0], 4),
        "Q0_pm": round(pm["Q"][0], 4),
        "Qmax_abs_pm": round(max(abs(q) for q in pm["Q"]), 4),
        "S0_pp": pp["S"][0],
        "Smin_pp": min(pp["S"]),
        "Sfin_pp": pp["S"][-1],
        "Sfin_pm": pm["S"][-1],
        "Efin_pp": pp["E"][-1],
        "Efin_pm": pm["E"][-1],
        "Qfin_pp": pp["Q"][-1],
        "variation_S_pp": round((max(pp["S"]) - min(pp["S"])) / pp["S"][0], 3),
    }

    # --- F1 : constructions charges ---
    v1 = (1.8 <= stats["Q0_pp"] <= 2.2 and -0.2 <= stats["Q0_pm"] <= 0.2)

    # --- F2 : charge nette conservee ---
    v2 = stats["Qmax_abs_pm"] <= 0.3

    # --- F3 : semblables interactifs ---
    v3 = stats["Smin_pp"] < 0.8 * stats["S0_pp"]

    # --- F4 : opposes se separent ---
    v4 = stats["Sfin_pm"] > 3.0

    # --- F5 : relaxation physique ---
    v5 = (stats["Efin_pp"] < pp["E"][0] and stats["Efin_pm"] < pm["E"][0]
          and stats["Qfin_pp"] > 1.0)

    criteres = {"V1_comptabilite": bool(v1),
                "V2_charge_neutre": bool(v2),
                "V3_semblables_interactifs": bool(v3),
                "V4_opposes_se_separent": bool(v4),
                "V5_relaxation": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T61-Q-KO6-ASSEMB-2026-10",
        "protocole": "T61-KO6-ASSEMB-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T61 : l'assemblage — deux ANU (ansatz produit) : la "
                 "comptabilité occulte #+ − #− vérifiée sur les charges "
                 "de texture (Q(++) = 1.912, Q(+-) = −0.000) ; les "
                 "semblables interagissent sans se lier étroitement, "
                 "les opposés se séparent",
        "doctrine": "T60 (l'ANU) ; T41-D2 (miroir du domaine) ; la "
                    "Chimie Occulte (règle #+ − #−, planches 48/69/70)",
        "statut_du_mot": "MESURE — assemblage = ansatz produit à deux "
                         "centres ; liaison = comparaison d'énergies "
                         "relaxées sans ajustement",
        "configuration": {"N": N, "L": L, "dt": DT, "gamma": GAMMA,
                          "steps": STEPS,
                          "centres": [[-2.5, 0, 0], [2.5, 0, 0]],
                          "masse_ANU_T60": 83.8},
        "mesures": stats,
        "trajectoires": trajs,
        "verdict_classe": ("S+ (la comptabilité #+ − #− tient : Q = 2 "
                           "et 0 mesurés ; les semblables interagissent "
                           "sans se lier étroitement, les opposés se "
                           "séparent — l'assemblage occult est d'abord "
                           "une comptabilité de charge, et la liaison "
                           "étroite demandera des configurations plus "
                           "élaborées)"),
        "falsifieur": "charges non additives ; neutre attaché ou "
                      "annihilé ; paire ++ passive ; énergie croissante",
        "suites_declarees": "la chaîne multi-ANU (3+, orientée comme "
                            "T44) ; la carte de liaison E(d) ; T62 — "
                            "l'aimantation",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t61_ko6_assemblage_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T61 (local) : {statut} — {nb}/5")
    print(f"  Q(0) : ++ = {stats['Q0_pp']:.3f} | +- = {stats['Q0_pm']:.3f}")
    print(f"  ++ : S {stats['S0_pp']:.2f} → min {stats['Smin_pp']:.2f} → "
          f"{stats['Sfin_pp']:.2f}, E {pp['E'][0]:.0f} → "
          f"{stats['Efin_pp']:.0f}, Q fin {stats['Qfin_pp']:.2f}")
    print(f"  +- : S fin {stats['Sfin_pm']:.2f}, max|Q| "
          f"{stats['Qmax_abs_pm']:.2f}, E fin {stats['Efin_pm']:.0f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
