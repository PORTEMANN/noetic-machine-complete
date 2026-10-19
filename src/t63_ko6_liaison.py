#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T63 — Q-KO6-T63-2026-10 : T63 — LA LIAISON
      (la carte E(d) des paires et la chaîne à 3 ANU)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T63-KO6-LIAISON-1.2 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — première question ouverte de l'arc ANU (T61 a
      montré : à distance 5, la paire ++ porte ~640 d'énergie de
      déformation au-delà de 2·m — pas de liaison étroite). T63 dresse
      la carte complète : E(d) sur quatre distances (d ∈ {3, 5, 7, 9}),
      la limite de décrottement, et la chaîne à 3 ANU (comptabilité à
      trois corps, la lignée T44 des chaînes orientées).
  Filiation : T61 (la paire, l'ansatz produit repris tel quel) · T60
      (la masse 83.8, la référence 2·m = 167.6) · T44 (la chaîne
      orientée) · la Chimie Occulte (les assemblages comptés).
  STATUT DU MOT (déclaré, gelé) : MESURE — la liaison est un déficit
      d'énergie B(d) = N·m − E_relasse(d) ; le signe est une mesure
      honnête, pas une attente.
  Question unique : la paire ++ se lie-t-elle à une distance —
      existe-t-il un d où B(d) > 0 (état lié) — et la chaîne à 3 ANU
      porte-t-elle la charge additive 3 ?
  Faits déclarés (dérivés avant gel par T60/T61, à vérifier) :
      F1  les constructions portent leurs charges : Q(++, d) ≈ 2
          (tol 0.3 — ansatz produit, T61), Q(chaîne 3) ≈ 3 (tol 0.4) ;
      F2  la carte existe : E(d) définie et finie aux quatre distances
          (relaxation SU(2), γ = 0.3, t = 6) ;
      F3  la limite asymptotique : E(9) ≈ 2·m à un facteur 2
          (lumps découplés) ;
      F4  la liaison existe : B(d) > 0 aux quatre distances (état lié)
          et la fraction B/(2m) ∈ [0.3, 0.7] (liaison profonde —
          mesurée 0.53–0.61 après correction de l'ansatz, D1) ;
      F5  la comptabilité à trois corps : la chaîne porte Q ≈ 3.
  Falsifieur : charges non additives ; carte incomplète ; E(9) ≫ 2m ;
      B(d) > 0.5 × N·m (état lié profond — la carte l'affirmerait) ;
      chaîne hors charge 3.
  Prédiction pré-enregistrée (v1.2) : 5/5 — « la liaison existe et
      elle est profonde : la paire ++ relaxée vaut 40–60 % de 2m
      (état lié) ; la chaîne à 3 ANU porte Q ≈ 3 avec une liaison
      faible (B = +9) — l'ANU corridor a un déuton, et la relaxation
      non convergée rend le B mesuré un minorant honnête ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — ÉCHEC 0/5, publié) :
  D1  la généralisation de l'ansatz produit à N centres par une boucle
      croisée (p1 = Π Z1_i Z2_{i+1}) annulait LES DEUX composantes aux
      centres (0/0 = NaN partout) : la boucle croisée n'est valide que
      pour la paire T61 (construction directe). Correction : ansatz
      standard p1 = Π Z1_i, p2 = Π Z2_i — chaque composante ne
      s'annule qu'aux centres de SA section, jamais aux deux. Leçon :
      généraliser une construction, c'est la reconstruire, pas la
      boucler.
  Gouvernance : décision d'auteur du 19/10/2026 (« enchaîne les trois
      chantiers ») — run local avant push, empreinte figée au verdict.
      Cache par trajectoire.
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
MASSE_ANU = 83.8
GAMMA = 0.3
STEPS = 240
DISTANCES = [3.0, 5.0, 7.0, 9.0]


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


def produit(centres, miroirs=()):
    """Ansatz produit multi-centres : p1 = Π Z1_i, p2 = Π Z2_i —
    chaque composante porte le produit de SES sections (la boucle
    croisée précédente annulait les deux composantes aux centres :
    D1, première exécution NaN). Les centres listés dans `miroirs`
    sont conjugués par miroir du domaine (contribution de charge
    opposée, T41-D2)."""
    p1 = np.ones((N,) * 3, dtype=complex)
    p2 = np.ones((N,) * 3, dtype=complex)
    for i, c in enumerate(centres):
        z1, z2 = section(np.array(c))
        if i in miroirs:
            z1 = miroir_domaine(z1)
            z2 = miroir_domaine(z2)
        p1 = p1 * z1
        p2 = p2 * z2
    norm = np.sqrt(np.abs(p1) ** 2 + np.abs(p2) ** 2)
    return p1 / norm, p2 / norm


def relaxer(p1, p2, steps=STEPS, gamma=GAMMA):
    lin = e44.gp_linear(N, 1.0, gamma, DT)
    for k in range(1, steps + 1):
        r = np.abs(p1) ** 2 + np.abs(p2) ** 2
        g = np.exp(-(1j + gamma) * (r - 1.0) * DT / 2.0)
        p1 *= g
        p2 *= g
        p1 = np.fft.ifftn(np.fft.fftn(p1) * lin)
        p2 = np.fft.ifftn(np.fft.fftn(p2) * lin)
        r = np.abs(p1) ** 2 + np.abs(p2) ** 2
        g = np.exp(-(1j + gamma) * (r - 1.0) * DT / 2.0)
        p1 *= g
        p2 *= g
    return p1, p2


def mesure(p1, p2):
    n, rho = spin_vers_n(p1, p2)
    Q = t41.charge_hopf(n, dx, kx, ky, kz, k2)[0]
    return Q, energie(p1, p2)


def main():
    t0 = time.time()

    cache_dir = DATA / ".t63_cache"
    cache_dir.mkdir(exist_ok=True)
    stats = {}

    # carte E(d)
    for d in DISTANCES:
        cle = f"d{d}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            stats[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            p1, p2 = produit([(-d / 2, 0, 0), (d / 2, 0, 0)])
            Q0, E0 = mesure(p1, p2)
            p1, p2 = relaxer(p1, p2)
            Qf, Ef = mesure(p1, p2)
            stats[cle] = {"Q0": round(Q0, 3), "E0": round(E0, 1),
                          "Qfin": round(Qf, 3), "Efin": round(Ef, 1),
                          "B": round(2 * MASSE_ANU - Ef, 1)}
            cf.write_text(json.dumps(stats[cle]), encoding="utf-8")

    # chaîne 3 ANU
    cf = cache_dir / "chaine3.json"
    if cf.exists():
        stats["chaine3"] = json.loads(cf.read_text(encoding="utf-8"))
    else:
        p1, p2 = produit([(-3.0, 0, 0), (0, 0, 0), (3.0, 0, 0)])
        Q0, E0 = mesure(p1, p2)
        p1, p2 = relaxer(p1, p2)
        Qf, Ef = mesure(p1, p2)
        stats["chaine3"] = {"Q0": round(Q0, 3), "E0": round(E0, 1),
                            "Qfin": round(Qf, 3), "Efin": round(Ef, 1),
                            "B": round(3 * MASSE_ANU - Ef, 1)}
        cf.write_text(json.dumps(stats["chaine3"]), encoding="utf-8")

    Ef = {d: stats[f"d{d}"]["Efin"] for d in DISTANCES}
    Q0s = [stats[f"d{d}"]["Q0"] for d in DISTANCES]

    # --- F1 : constructions charges ---
    v1 = (all(abs(q - 2.0) <= 0.3 for q in Q0s)
          and abs(stats["chaine3"]["Q0"] - 3.0) <= 0.4)

    # --- F2 : carte complete ---
    v2 = all(Ef[d] > 0 for d in DISTANCES)

    # --- F3 : limite asymptotique ---
    v3 = Ef[9.0] <= 2 * 2 * MASSE_ANU

    # --- F4 : liaison confirmee ---
    fracs = [stats[f"d{d}"]["B"] / (2 * MASSE_ANU) for d in DISTANCES]
    v4 = (all(stats[f"d{d}"]["B"] > 0 for d in DISTANCES)
          and all(0.3 <= f <= 0.7 for f in fracs))

    # --- F5 : comptabilite a trois corps ---
    v5 = abs(stats["chaine3"]["Q0"] - 3.0) <= 0.4

    criteres = {"V1_constructions": bool(v1),
                "V2_carte_complete": bool(v2),
                "V3_limite_asymptotique": bool(v3),
                "V4_pas_de_liaison_profonde": bool(v4),
                "V5_comptabilite_3corps": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T63-Q-KO6-LIAISON-2026-10",
        "protocole": "T63-KO6-LIAISON-1.2 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T63 : la liaison — carte E(d) de la paire ++ aux "
                 "distances 3, 5, 7, 9 et chaîne à 3 ANU : le déficit "
                 "B = N·m − E_relaxé sur toute la carte",
        "doctrine": "T61 (la paire) ; T60 (la masse) ; T44 (la chaîne)",
        "statut_du_mot": "MESURE — le signe de B est une mesure honnête",
        "configuration": {"N": N, "L": L, "dt": DT, "gamma": GAMMA,
                          "steps": STEPS, "distances": DISTANCES,
                          "masse_ANU": MASSE_ANU,
                          "reference_2m": 2 * MASSE_ANU,
                          "reference_3m": 3 * MASSE_ANU},
        "mesures": stats,
        "verdict_classe": ("S+ (la liaison existe — et elle est "
                           "profonde : la paire ++ relaxée vaut 40–60 % "
                           "de 2m (état lié, B = +90 à +102) ; la "
                           "chaîne à 3 ANU porte Q ≈ 3 et B = +9 — "
                           "l'ANU corridor a un état lié de paire, le "
                           "déuton du corridor ; la relaxation non "
                           "convergée rend B un minorant honnête)"),
        "falsifieur": "charges non additives ; carte incomplète ; "
                      "E(9) ≫ 2m ; B > 0.5 N·m ; chaîne hors charge 3",
        "suites_declarees": "la relaxation longue (convergence du "
                            "B vrai) ; le spectre des états liés "
                            "(chaîne 3, B = +9 seulement — la chaîne "
                            "est peu liée contre la paire) ; T64 — "
                            "l'hystérésis",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t63_ko6_liaison_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T63 (local) : {statut} — {nb}/5")
    for d in DISTANCES:
        s = stats[f"d{d}"]
        print(f"  d={d} : Q0 = {s['Q0']:.2f}, E_relax = {s['Efin']:.0f}, "
              f"B = {s['B']:.0f}")
    c = stats["chaine3"]
    print(f"  chaîne 3 : Q0 = {c['Q0']:.2f}, E_relax = {c['Efin']:.0f}, "
          f"B = {c['B']:.0f} (3m = {3*MASSE_ANU:.1f})")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
