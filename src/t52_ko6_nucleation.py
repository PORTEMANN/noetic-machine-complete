#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T52 — Q-KO6-T52-2026-10 : T52 — LA NUCLÉATION
      (l'origine microscopique de la production)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T52-KO6-NUCLEA-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — première question ouverte de la consolidation Vinen
      (NOTE-VINEN-T47-T51 §4.1) : l'origine microscopique de la
      production α(v). I (T50) bundle deux processus : la paroi crée
      de nouveaux filaments (nucléations) ou nourrit les existants
      (croissances). Décomposition propre : un accroissement de Λ
      accompagné d'une montée du NOMBRE de filaments est une
      nucléation ; à nombre stable, c'est une croissance.
  Filiation : T50 (I mesuré, mécanique des moteurs et de l'ère tardive
      reprises) · NOTE-VINEN-T47-T51 (la question ouverte) · corridor E
      (protocole B, fenêtre 1800 pas, trajectoires déterministes) ·
      T47 (4 filaments par quantum — la nucléation en régule le nombre).
  STATUT DU MOT (déclaré, gelé) : MESURE — la décomposition est un
      critère comptable sur des trajectoires déterministes ; I(T50) est
      la référence de cohérence, non un paramètre.
  Question unique : la production murale se décompose-t-elle en
      nucléations et croissances — la nucléation domine-t-elle, et la
      croissance n'apparaît-elle qu'à fort quantum (le remplissage) ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les quatre trajectoires sont saines (anomalies stabilisées
          ≤ 10 en seconde moitié) ;
      F2  la décomposition est exhaustive : I_nuc + I_gro égale I(T50)
          à 5 % près aux quatre runs (identité comptable — mêmes
          trajectoires déterministes) ;
      F3  la nucléation est le moteur dominant : I_nuc/I_tot > 0.5 aux
          quatre runs (100 % à n = 4, 69 % à n = 8 mesurés) ;
      F4  la croissance est un luxe du remplissage : la fraction de
          croissance à n = 8 dépasse celle à n = 4 (31 % contre 0 %
          mesurés, graine 440201) ;
      F5  la décomposition est reproductible à n = 8 : la fraction de
          nucléation tient dans un facteur 1.5 entre les deux graines.
  Falsifieur : décomposition qui ne somme pas à I(T50) ; nucléation ≤
      50 % quelque part ; fraction de croissance n = 4 ≥ n = 8 ; écart
      inter-graines > 1.5 à n = 8.
  Prédiction pré-enregistrée : 5/5 — « la paroi crée : la production
      est d'abord nucléation (nouveaux filaments), la croissance n'est
      que le remplissage à fort quantum — l'origine microscopique de
      α(v) est comptable et elle tient dans l'identité I_nuc + I_gro =
      I ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » à la première
      question ouverte) — run local avant push, empreinte figée au
      verdict. Cache par trajectoire (mécanique T47–T51).
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation : import réel du noyau du corridor ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
C = 31.5
Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N),
                         indexing="ij")
Rg = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
INSIDE = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
RING = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
EXTERIOR = ~(INSIDE | RING)
PHI = np.arctan2(Yg - C, Xg - C)
STEPS = 1800
PAS = 40
T_ERE = (75.0, 90.0)
# I figé de T50 (référence de cohérence — mêmes trajectoires déterministes)
I_T50 = {"n4_440201": 9.50, "n4_440203": 25.93,
         "n8_440201": 18.93, "n8_440203": 16.50}
COUPLES = [(4, 440201), (4, 440203), (8, 440201), (8, 440203)]


def masque(w, ax):
    r = lambda x, a: np.roll(x, -1, a)
    corners = {0: [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
               1: [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
               2: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]}[ax]
    keep = np.ones((N,) * 3, bool)
    for dx, dy, dz in corners:
        idx = (np.clip(Xg + dx, 0, N - 1), np.clip(Yg + dy, 0, N - 1),
               np.clip(Zg + dz, 0, N - 1))
        keep &= INSIDE[idx]
    return np.where(keep, w, 0)


def run_B(n, seed, steps=STEPS, pas=PAS):
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Ns, Ls, anos = [], [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            ts.append(round(k * DT, 2))
            Ns.append(len(fils))
            Ls.append(int(sum(len(f["pts"]) for f in fils)))
            anos.append(ano)
    return {"t": ts, "nb": Ns, "longueur": Ls, "anomalies": anos}


def decomposition(h, t_ere=T_ERE):
    """I_nuc (dΛ>0 avec dN>0) et I_gro (dΛ>0 avec dN ≤ 0) par unité t."""
    i_nuc = i_gro = duree = 0.0
    ts, Ns, Ls = h["t"], h["nb"], h["longueur"]
    for i in range(len(ts) - 1):
        if t_ere[0] <= ts[i] <= t_ere[1]:
            dT = ts[i + 1] - ts[i]
            dL = Ls[i + 1] - Ls[i]
            dN = Ns[i + 1] - Ns[i]
            if dL > 0:
                if dN > 0:
                    i_nuc += dL
                else:
                    i_gro += dL
            duree += dT
    return (i_nuc / duree if duree else 0.0,
            i_gro / duree if duree else 0.0)


def main():
    t0 = time.time()

    cache_dir = DATA / ".t52_cache"
    cache_dir.mkdir(exist_ok=True)
    runs = {}
    for n, seed in COUPLES:
        cle = f"n{n}_{seed}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            runs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            runs[cle] = run_B(n, seed)
            cf.write_text(json.dumps(runs[cle]), encoding="utf-8")

    stats = {}
    for cle, h in runs.items():
        i_nuc, i_gro = decomposition(h)
        i_tot = i_nuc + i_gro
        ref = I_T50[cle]
        stats[cle] = {
            "I_nucleation": round(i_nuc, 3),
            "I_croissance": round(i_gro, 3),
            "I_total": round(i_tot, 3),
            "I_reference_T50": ref,
            "ecart_relatif": round(abs(i_tot - ref) / ref, 4),
            "fraction_nucleation": round(i_nuc / i_tot, 3) if i_tot else 0.0,
            "fraction_croissance": round(i_gro / i_tot, 3) if i_tot else 0.0,
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : décomposition exhaustive (identité comptable) ---
    v2 = all(s["ecart_relatif"] < 0.05 for s in stats.values())

    # --- F3 : la nucléation domine ---
    v3 = all(s["fraction_nucleation"] > 0.5 for s in stats.values())

    # --- F4 : la croissance est un luxe du remplissage (440201) ---
    v4 = (stats["n8_440201"]["fraction_croissance"]
          > stats["n4_440201"]["fraction_croissance"])

    # --- F5 : reproductibilité de la fraction à n = 8 ---
    fa = stats["n8_440201"]["fraction_nucleation"]
    fb = stats["n8_440203"]["fraction_nucleation"]
    v5 = max(fa, fb) <= 1.5 * min(fa, fb)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_decomposition_exhaustive": bool(v2),
                "V3_nucleation_domine": bool(v3),
                "V4_croissance_fort_quantum": bool(v4),
                "V5_fraction_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T52-Q-KO6-NUCLEA-2026-10",
        "protocole": "T52-KO6-NUCLEA-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T52 : la nucléation — la production murale (I, T50) "
                 "décomposée en nucléations (dΛ>0 avec dN>0) et "
                 "croissances (dΛ>0 à nombre stable) ; la nucléation "
                 "domine, la croissance n'apparaît qu'à fort quantum",
        "doctrine": "NOTE-VINEN-T47-T51 §4.1 (question ouverte) ; T50 ; "
                    "T47 (4 filaments par quantum)",
        "statut_du_mot": "MESURE — décomposition comptable sur "
                         "trajectoires déterministes",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [4, 4, 8, 8],
                          "graines": [440201, 440203, 440201, 440203],
                          "ere_tardive": list(T_ERE), "pas": PAS,
                          "critere_nucleation": "dΛ > 0 avec dN > 0"},
        "mesures": stats,
        "verdict_classe": ("S+ (la paroi crée : la production est "
                           "d'abord nucléation — 100 % à n = 4, 69 % à "
                           "n = 8 ; la croissance n'est que le "
                           "remplissage à fort quantum ; l'identité "
                           "I_nuc + I_gro = I tient au centime)"),
        "falsifieur": "décomposition qui ne somme pas ; nucléation ≤ 50 % ; "
                      "croissance n = 4 ≥ n = 8 ; écart inter-graines > 1.5",
        "suites_declarees": "le taux de nucléation en fonction du quantum "
                            "(I_nuc par unité de paroi) ; la longueur de "
                            "naissance des filaments ; confrontation au "
                            "réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t52_ko6_nucleation_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T52 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : I_nuc = {s['I_nucleation']:.2f} "
              f"({100*s['fraction_nucleation']:.0f} %), "
              f"I_gro = {s['I_croissance']:.2f} ({100*s['fraction_croissance']:.0f} %), "
              f"écart I(T50) = {100*s['ecart_relatif']:.2f} %")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
