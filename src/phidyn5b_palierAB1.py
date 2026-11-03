#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-5b — PALIERS A (instrument) + B1 (mot pur : F1, F2, F4) — fiche v1.0 SCELLEE (f95512f)
=============================================================================================
RG declaree : decimation = passage de niveau N -> N+1 (raffinement par
substitution). Observable : distribution des ratios de gaps consecutifs
r_i = g_{i+1}/g_i sur la structure de bandes du niveau N (grille 2^18,
gaps < 3 cellules exclus — standard P1). Niveaux 9..14 (jamais 15).
F1 : D_KS(N, N+1) decroissante ? F2 : D(13,14) + permutation gelee
(1000, graine 20261103) + fraction des ratios dans {1/φ, 1/φ²} ± 0.02.
F4 : pente log-log de D vs niveau.
Sortie : data/phidyn5b_palierAB1.json
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
ATTENDUS = {9: 19, 10: 30, 11: 48, 12: 78, 13: 126, 14: 202}
CELL_EXCL = 3
GRAINE = 20261103
N_PERM = 1000


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def bandes_niveau(tg, N):
    """Structure de bandes |x_N| <= 1 (mot W_N, trace map, grille 2^18)."""
    t = tg
    x1 = 0.5 * t
    x2 = 0.5 * (t * (t - 1.0) - 1.0)
    x3 = 0.5 * (t * (t * (t - 1.0) - 1.0) - (t - 1.0))
    xs = [x1, x2, x3]
    for _ in range(N - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    xN = xs[-1]
    m = np.abs(xN) <= 1.0
    idx = np.where(m)[0]
    if len(idx) == 0:
        return []
    coupe = np.where(np.diff(idx) > 1)[0]
    debuts = np.concatenate([[0], coupe + 1])
    fins = np.concatenate([coupe, [len(idx) - 1]])
    return [(idx[d], idx[f]) for d, f in zip(debuts, fins)]


def gaps_ratios(bandes, dt):
    """Liste ordonnee des gaps (en t) > 3 cellules, puis ratios consecutifs."""
    gaps = []
    for i in range(1, len(bandes)):
        g = (bandes[i][0] - bandes[i - 1][1]) * dt
        if g > CELL_EXCL * dt:
            gaps.append(g)
    ratios = [gaps[i + 1] / gaps[i] for i in range(len(gaps) - 1)
              if np.isfinite(gaps[i]) and gaps[i] > 0]
    return np.array(gaps), np.array(ratios)


def ks_2samp(a, b):
    """Distance de Kolmogorov-Smirnov a distributions empiriques."""
    a, b = np.sort(a), np.sort(b)
    tous = np.sort(np.concatenate([a, b]))
    ecdf_a = np.searchsorted(a, tous, side="right") / len(a)
    ecdf_b = np.searchsorted(b, tous, side="right") / len(b)
    return float(np.max(np.abs(ecdf_a - ecdf_b)))


def permutation_p(a, b, graine=GRAINE, n_perm=N_PERM):
    rng = np.random.default_rng(graine)
    obs = ks_2samp(a, b)
    pool = np.concatenate([a, b])
    na = len(a)
    compte = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if ks_2samp(pool[:na], pool[na:]) >= obs:
            compte += 1
    return (compte + 1) / (n_perm + 1)


def main():
    t0 = time.time()
    print("Φ-DYN-5b — PALIERS A + B1 (mot pur) [fiche v1.1 SCELLÉE]")
    print("=" * 78)
    tg = np.linspace(-TMAX, TMAX, GRILLE)
    dt = tg[1] - tg[0]

    # ---- PALIER A : reproduction des comptes T24
    print("PALIER A — structures de bandes (mot pur) :")
    structures = {}
    A_ok = True
    for N in NIVEAUX:
        w = mot_fibonacci(N - 2)
        assert len(w) == {9: 34, 10: 55, 11: 89, 12: 144, 13: 233, 14: 377}[N]
        b = bandes_niveau(tg, N)
        structures[N] = b
        ok = len(b) == ATTENDUS[N]
        A_ok &= ok
        print(f"  niveau {N} : {len(b)} bandes (attendu {ATTENDUS[N]}) : "
              f"{'PASS' if ok else 'FAIL'}")
    print(f"  PALIER A : {'PASS — palier B débloqué' if A_ok else 'FAIL'}")

    # ---- F1 : D(N, N+1) sur les distributions de ratios
    print("\nF1 — distances KS entre niveaux consécutifs (ratios de gaps) :")
    ratios_par_niveau = {}
    for N in NIVEAUX:
        _, r = gaps_ratios(structures[N], dt)
        ratios_par_niveau[N] = r
        print(f"  niveau {N} : {len(r)} ratios de gaps")
    distances = {}
    for i in range(len(NIVEAUX) - 1):
        n1, n2 = NIVEAUX[i], NIVEAUX[i + 1]
        d = ks_2samp(ratios_par_niveau[n1], ratios_par_niveau[n2])
        distances[f"{n1}-{n2}"] = d
        print(f"  D({n1}, {n2}) = {d:.4f}")
    # F1 v1.1 : decroissante a bande de plateau declaree (theorie KS)
    paires = [(NIVEAUX[i], NIVEAUX[i + 1]) for i in range(len(NIVEAUX) - 1)]
    diffs = np.diff([distances[f"{a}-{b}"] for a, b in paires])
    bandes = []
    for (a, b) in paires:
        na, nb = len(ratios_par_niveau[a]), len(ratios_par_niveau[b])
        bandes.append(0.27 * np.sqrt((na + nb) / (na * nb)))
    pas_ok = [bool(diffs[i] <= bandes[i]) for i in range(len(diffs))]
    tendance = distances[f"9-10"] > distances[f"13-14"]
    f1_tenu = bool(all(pas_ok) and tendance)
    print(f"  F1 v1.1 (bande plateau 0.27*sqrt((n+m)/nm)) : "
          f"pas {['OK' if x else 'KO' for x in pas_ok]} · tendance {tendance}"
          f" → {'TENU' if f1_tenu else 'NON TENU'}")
    # F2 complementaire v1.1 : ratio de comptes, fenêtre T24 gelée
    comptes = {N: len(structures[N]) for N in NIVEAUX}
    ratios_comptes = [comptes[NIVEAUX[i+1]] / comptes[NIVEAUX[i]]
                      for i in range(len(NIVEAUX) - 1)]
    fenetre_t24 = all(abs(r - PHI) <= 0.02 for r in ratios_comptes[-3:])
    rec_comp = all(abs(comptes[NIVEAUX[i+2]] - comptes[NIVEAUX[i+1]] - comptes[NIVEAUX[i]]) <= 4
                   for i in range(len(NIVEAUX) - 2))
    print(f"  F2-complémentaire (comptes T24) : ratios "
          f"{[round(r, 4) for r in ratios_comptes]} · 3 derniers dans φ±0,02 : "
          f"{fenetre_t24} · récursion ±4 : {rec_comp}")

    # ---- F2 : distribution fixe
    r13, r14 = ratios_par_niveau[13], ratios_par_niveau[14]
    d_fixe = ks_2samp(r13, r14)
    p_perm = permutation_p(r13, r14)
    tous_ratios = np.concatenate([r13, r14])
    fenetre = ((np.abs(tous_ratios - 1 / PHI) <= 0.02)
               | (np.abs(tous_ratios - 1 / PHI ** 2) <= 0.02))
    frac_phi = float(fenetre.mean())
    print(f"\nF2 — distribution fixe : D(13,14) = {d_fixe:.4f} · "
          f"permutation p = {p_perm:.4f} (gelée, {N_PERM} permutations)")
    print(f"  fraction des ratios dans {{1/φ, 1/φ²}} ± 0,02 : {frac_phi:.3f}")
    print(f"  (réserve : KS asymptotique sur ~{len(r13)} gaps — fiche §3.4)")

    # ---- F4 : exposant log-log
    ns = np.array(NIVEAUX[:-1], float)
    ds = np.array([distances[f"{NIVEAUX[i]}-{NIVEAUX[i+1]}"]
                   for i in range(len(NIVEAUX) - 1)])
    pente = float(np.polyfit(np.log(ns), np.log(np.maximum(ds, 1e-12)), 1)[0])
    print(f"\nF4 — pente log-log D vs niveau : {pente:.4f} (mesure nouvelle)")

    out = {
        "chantier": "PHI-DYN-5B-PALIER-AB1",
        "fiche": "FICHE-PHI-DYN-5B-POINT-FIXE v1.1 SCELLÉE (3de8d75)",
        "palier_A_pass": bool(A_ok),
        "n_ratios_par_niveau": {str(N): len(ratios_par_niveau[N]) for N in NIVEAUX},
        "F1": {"distances": distances, "differences": [float(x) for x in diffs],
               "tenu": f1_tenu},
        "F2": {"D_fixe_13_14": d_fixe, "permutation_p": p_perm,
               "fraction_phi": frac_phi,
               "comptes_T24": {"ratios": ratios_comptes,
                               "fenetre": bool(fenetre_t24),
                               "recursion": bool(rec_comp)}},
        "F1_v1_1": {"pas_ok": pas_ok, "bandes": [float(x) for x in bandes],
                    "tendance": bool(tendance), "tenu": f1_tenu},
        "F4_exposant_loglog": pente,
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn5b_palierAB1.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
