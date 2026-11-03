#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P1 — PILIER B : levier phason (fiche v1.1 SCELLEE)
==========================================================
Grille gelée §3.3 : rho ∈ {0, 0.001, 0.01, 0.05, 0.15, 0.3}, 20 réalisations,
graine de générateur aléatoire 20261103.

Déclarations d'implémentation (calibrées au run 1, documentées) :
  - INDEXATION DES MOTS (correction run 1) : la trace x_N de T24 porte sur
    le mot W_N de longueur F_N, avec W_1="A", W_2="AB", W_{n+1}=W_n W_{n-1}.
    La fonction mot_fibonacci(n) rend un mot de longueur F_{n+2} ; donc
    W_14 = mot_fibonacci(12) (377 lettres) et W_13 = mot_fibonacci(11)
    (233 lettres) — le run 1 avait utilisé F_{n+2}=987 lettres, alias de
    grille (982 « bandes » fantômes, polynôme de degré 987 sous-échantillonné).
    Au rho=0 corrigé, les comptes doivent reproduire T24 : 126 et 202.
  - flips (correction run 1, deuxième) : densité rho implantée par masque de
    Bernoulli indépendant par position (probabilité rho), graine
    20261103 instanciée une fois par valeur de rho — l'implémentation
    précédente (nombre fixe floor(rho*L)) quantifiait rho=0.001 à ZÉRO
    flip (mot de 377 lettres), rendant la valeur de grille muette ; la
    densité Bernoulli est la lecture fidèle de « flips à densité rho » ;
  - comptage de bandes : |Tr(produit du mot)/2| <= 1 sur la grille T24
    2^18 x [-2.5, 2.5] — produit vectorisé ;
  - résidu d'identité de trace : max sur n=3..12 de
    |x_{n+1} - 2 x_n x_{n-1} + x_{n-2}| à t = 0.7 (énergie de bande),
    traces des préfixes du mot déformé (produits exacts) — mesure de la
    brisure de la map par le désordre.

Usage : python phidyn2_p1_pilierB.py <rho>
Sortie : data/phidyn2_p1_pilierB_rho<RHO>.json
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

GRILLE = 1 << 18
TMAX = 2.5
PHI = (1 + np.sqrt(5)) / 2
NIVEAU = 14
T_TRACE = 0.7
N_REAL = 20


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def compte_bandes_mot(w, tg):
    """Compte les bandes |Tr(P(t))/2| <= 1 sur la grille, par produit
    vectorise 2x2."""
    a = np.ones_like(tg)
    b = np.zeros_like(tg)
    c = np.zeros_like(tg)
    d = np.ones_like(tg)
    for ch in w:
        if ch == "A":
            # P <- A(t) @ P avec A = [[t,-1],[1,0]]
            na = tg * a - c
            nb = tg * b - d
            nc = a
            nd = b
        else:
            # P <- B(t) @ P avec B = [[t-1,-1],[1,0]]
            na = (tg - 1.0) * a - c
            nb = (tg - 1.0) * b - d
            nc = a
            nd = b
        a, b, c, d = na, nb, nc, nd
    tr = 0.5 * (a + d)
    m = np.abs(tr) <= 1.0
    idx = np.where(m)[0]
    if len(idx) == 0:
        return 0
    return 1 + int(np.sum(np.diff(idx) > 1))


def trace_prefixes(w, t, k_max=13):
    """Traces exactes des préfixes de w (longueurs F_1..F_k_max) en t."""
    lgs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377][:k_max]
    xs = []
    P = np.eye(2)
    li = 0
    for lg in lgs:
        while li < lg:
            ch = w[li]
            M = np.array([[t, -1.0], [1.0, 0.0]]) if ch == "A" \
                else np.array([[t - 1.0, -1.0], [1.0, 0.0]])
            P = M @ P
            li += 1
        xs.append(0.5 * np.trace(P))
    return xs


def residu_trace(w, t):
    xs = trace_prefixes(w, t)
    r = 0.0
    for i in range(len(xs) - 3):
        r = max(r, abs(xs[i + 3] - 2 * xs[i + 2] * xs[i + 1] + xs[i]))
    return r


def main():
    rho = float(sys.argv[1])
    t0 = time.time()
    tg = np.linspace(-TMAX, TMAX, GRILLE)
    # W_14 = mot de longueur F_14 = 377 ; W_13 = préfixe de 233 lettres
    w14 = mot_fibonacci(NIVEAU - 2)
    w13 = mot_fibonacci(NIVEAU - 3)
    assert len(w14) == 377 and len(w13) == 233, (len(w14), len(w13))
    assert w14.startswith(w13)

    rng = np.random.default_rng(20261103)
    ratios, residus, comptes13, comptes14, n_flips = [], [], [], [], []
    for r in range(N_REAL):
        # masque de Bernoulli sur W_14 (377 positions) ; W_13 reçoit les
        # flips à positions < 233 (préfixe)
        masque = rng.random(len(w14)) < rho
        n_flips.append(int(masque.sum()))
        if masque.any():
            w14d = "".join("B" if (masque[i] and c == "A") or (not masque[i] and c == "B")
                           else "A" for i, c in enumerate(w14))
            m13 = masque[:233]
            w13d = "".join("B" if (m13[i] and c == "A") or (not m13[i] and c == "B")
                           else "A" for i, c in enumerate(w13))
        else:
            w14d = w14
            w13d = w13
        c13 = compte_bandes_mot(w13d, tg)
        c14 = compte_bandes_mot(w14d, tg)
        comptes13.append(c13)
        comptes14.append(c14)
        ratios.append(c14 / max(1, c13))
        residus.append(residu_trace(w14d, T_TRACE))
        print(f"  réalisation {r + 1:2d}/{N_REAL} : c13={c13} c14={c14} "
              f"ratio={ratios[-1]:.4f} résidu trace={residus[-1]:.3e}",
              flush=True)

    ratios = np.array(ratios)
    res = np.array(residus)
    med = float(np.median(ratios))
    ecart_type = float(ratios.std())
    conformes = int(np.sum(np.abs(ratios - PHI) <= 0.02))
    print("\n" + "=" * 78)
    print(f"PILIER B — rho={rho} : ratios c14/c13 = med {med:.4f} "
          f"(σ {ecart_type:.4f}) · {conformes}/{N_REAL} dans φ±0.02 "
          f"· résidu trace médian {np.median(res):.3e}")

    out = {
        "chantier": "PHI-DYN-2-P1-PILIER-B",
        "fiche": "FICHE-PHI-DYN-2-P1-GENERATEUR v1.1 SCELLÉE (4ad4875)",
        "rho": rho, "n_flips_par_realisation": n_flips, "graine": 20261103,
        "n_realisations": N_REAL,
        "comptes13": comptes13, "comptes14": comptes14,
        "ratios": ratios.tolist(),
        "residus_trace": res.tolist(),
        "resume": {"ratio_mediane": med, "ratio_sigma": ecart_type,
                   "n_dans_fenetre_phi": conformes,
                   "residu_trace_mediane": float(np.median(res))},
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    tag = str(rho).replace(".", "p")
    dest = Path(f"data/phidyn2_p1_pilierB_rho{tag}.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"→ {dest}")


if __name__ == "__main__":
    main()
