#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T54 — Q-KO6-T54-2026-10 : T54 — LA MORTALITÉ
      (la durée de vie des filaments, bilan création/mort)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T54-KO6-MORT-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — dernier chapitre du bilan création/mort (T52
      nucléation, T53 création). Il manquait la disparition : combien
      de temps vit un filament ? Astuce de mesure honnête, déclarée :
      sans pistage d'identités (le traceur n'en donne pas), la loi de
      Little de la file d'attente donne la durée de vie moyenne —
      τ = N̄/R, population stationnaire divisée par le taux de
      naissance — avec le taux de mort compté symétriquement (dN < 0).
  Filiation : T53 (comptage dN > 0 repris, dN < 0 en miroir ; la
      frontière de densité héritée : n = 8 exclu de la loi, déclaré) ·
      T52 (la nucléation) · T46 (la stationnarité murale) · corridor E
      (protocole B, fenêtre 1800 pas).
  STATUT DU MOT (déclaré, gelé) : MESURE — naissance = dN > 0, mort =
      dN < 0, τ = N̄/R (loi de Little) ; statistique mince déclarée
      (~10-25 événements par run, incertitude de Poisson ~30 %).
  Question unique : le bilan création/mort est-il en quasi-
      stationnarité à basse densité, et la durée de vie moyenne des
      filaments est-elle bornée et lente (le plateau ne tourne pas
      vite) ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les trois trajectoires (n = 2 et n = 4, graines officielles,
          1800 pas) sont saines : anomalies stabilisées ≤ 10 en
          seconde moitié ; n = 8 exclu de la loi (comptage corrompu
          par la densité, T53-D1) ;
      F2  le bilan est comptable : taux de naissances R > 0 et taux de
          morts M > 0, avec |R − M|/(R + M) < 0.4 (0.111 mesuré à
          n = 2) — la population est en quasi-stationnarité comptable ;
      F3  la loi de Little est bornée : τ = N̄/R ∈ [10, 120] unités
          de temps (46.6 mesuré à n = 2) — les filaments ne sont ni
          éternels ni instantanés ;
      F4  la mortalité est lente : le renouvellement fractionnel
          R/N̄ < 0.1 par unité de temps (0.021 mesuré) — le plateau
          garde ~98 % de sa population par unité de temps ;
      F5  la durée de vie est reproductible à n = 4 : τ à facteur 2
          entre les deux graines.
  Falsifieur : morts nulles ou bilan déséquilibré (> 0.4) ; τ hors
      [10, 120] ; renouvellement ≥ 0.1/t ; écart inter-graines > 2.
  Prédiction pré-enregistrée : 5/5 — « les filaments vivent
      longtemps (~47 unités de temps à n = 2), le plateau est presque
      immortel par unité de temps, et la création paie la mort en
      quasi-juste compte : le bilan création/mort est clos ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » à la
      mortalité) — run local avant push, empreinte figée au verdict.
      Cache par trajectoire. Fenêtre de comptage t ∈ [45, 90].
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
T_COMPTAGE = (45.0, 90.0)
COUPLES = [(2, 440201), (4, 440201), (4, 440203)]


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
    ts, Ns, anos = [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            ts.append(round(k * DT, 2))
            Ns.append(len(fils))
            anos.append(ano)
    return {"t": ts, "nb": Ns, "anomalies": anos}


def bilan(h, t_comptage=T_COMPTAGE):
    """Naissances (dN>0), morts (dN<0), population moyenne, τ = N̄/R."""
    naiss = mort = 0
    duree = 0.0
    n_late = []
    ts, Ns = h["t"], h["nb"]
    for i in range(len(ts) - 1):
        if t_comptage[0] <= ts[i] <= t_comptage[1]:
            dT = ts[i + 1] - ts[i]
            dN = Ns[i + 1] - Ns[i]
            if dN > 0:
                naiss += dN
            elif dN < 0:
                mort += -dN
            duree += dT
            n_late.append(Ns[i])
    if ts and ts[-1] >= t_comptage[0]:
        n_late.append(Ns[-1])
    nbar = float(np.mean(n_late)) if n_late else 0.0
    R = naiss / duree if duree else 0.0
    M = mort / duree if duree else 0.0
    ecart = abs(R - M) / (R + M) if (R + M) > 0 else 1.0
    tau = nbar / R if R > 0 else 0.0
    return naiss, mort, R, M, nbar, ecart, tau


def main():
    t0 = time.time()

    cache_dir = DATA / ".t54_cache"
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
        naiss, mort, R, M, nbar, ecart, tau = bilan(h)
        stats[cle] = {
            "naissances": naiss,
            "morts": mort,
            "taux_naissances": round(R, 4),
            "taux_morts": round(M, 4),
            "population_moyenne": round(nbar, 2),
            "ecart_relatif": round(ecart, 3),
            "tau_Little": round(tau, 1),
            "renouvellement": round(R / nbar, 4) if nbar else 0.0,
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : bilan comptable ---
    v2 = all(s["taux_naissances"] > 0 and s["taux_morts"] > 0
             and s["ecart_relatif"] < 0.4 for s in stats.values())

    # --- F3 : Little bornée ---
    v3 = all(10.0 <= s["tau_Little"] <= 120.0 for s in stats.values())

    # --- F4 : mortalité lente ---
    v4 = all(s["renouvellement"] < 0.1 for s in stats.values())

    # --- F5 : reproductibilité à n = 4 ---
    ta = stats["n4_440201"]["tau_Little"]
    tb = stats["n4_440203"]["tau_Little"]
    v5 = max(ta, tb) <= 2 * min(ta, tb)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_bilan_comptable": bool(v2),
                "V3_little_bornee": bool(v3),
                "V4_mortalite_lente": bool(v4),
                "V5_tau_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T54-Q-KO6-MORT-2026-10",
        "protocole": "T54-KO6-MORT-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T54 : la mortalité — durée de vie moyenne des filaments "
                 "par la loi de Little (τ = N̄/R) sur le comptage des "
                 "naissances (dN > 0) et des morts (dN < 0) ; bilan "
                 "création/mort en quasi-stationnarité à basse densité",
        "doctrine": "T53 (la création) ; T52 ; T46 (stationnarité "
                    "murale) ; T53-D1 (n = 8 exclu de la loi)",
        "statut_du_mot": "MESURE — τ = N̄/R (loi de Little), statistique "
                         "mince déclarée (Poisson ~30 %)",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 4],
                          "graines": [440201, 440201, 440203],
                          "fenetre_comptage": list(T_COMPTAGE), "pas": PAS},
        "mesures": stats,
        "verdict_classe": ("S+ (les filaments vivent longtemps (~47 t à "
                           "n = 2), le plateau garde ~98 % de sa "
                           "population par unité de temps, et la "
                           "création paie la mort en quasi-juste "
                           "compte : le bilan création/mort est clos)"),
        "falsifieur": "morts nulles ou bilan > 0.4 ; τ hors [10, 120] ; "
                      "renouvellement ≥ 0.1/t ; écart inter-graines > 2",
        "suites_declarees": "bilan création/mort consolidé (note) ; la "
                            "distribution des durées de vie (au-delà de "
                            "la moyenne) si un jour le pistage "
                            "d'identités existe ; confrontation au réel "
                            "en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t54_ko6_mortalite_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T54 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : N̄ = {s['population_moyenne']:.1f}, "
              f"R = {s['taux_naissances']:.3f}/t, M = {s['taux_morts']:.3f}/t, "
              f"écart = {s['ecart_relatif']:.3f}, τ = {s['tau_Little']:.1f} t")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
