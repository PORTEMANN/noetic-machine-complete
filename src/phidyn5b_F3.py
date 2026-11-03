#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-5b — PALIER B2 (F3 : instabilite phason) — fiche v1.1 SCELLEE (3de8d75)
==============================================================================
Pour rho donne (0.001 ou 0.01) : 20 realisations Bernoulli (graine 20261103
instanciee une fois par rho, reprise gelée P1-B) ; mots W_12, W_13, W_14
deformes (mot_fibonacci(10,11,12) = 144/233/377 lettres) ; structures de
bandes par produit de transfert vectorise sur grille 2^18 ; distributions de
ratios de gaps ; F1-style par realisation ; signature de comptes T24.
Reference : mot pur (rho=0) via le meme chemin de produit.
Sortie : data/phidyn5b_F3_rho<RHO>.json
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
NIVEAUX = [12, 13, 14]
MOTS = {12: 10, 13: 11, 14: 12}   # W_N = mot_fibonacci(N-2)
CELL_EXCL = 3
GRAINE = 20261103
N_REAL = 20
ATTENDUS = {12: 78, 13: 126, 14: 202}


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def bandes_produit(w, tg, y=1.0):
    """Bandes |Tr(produit du mot)/2| <= 1 par produit vectorise (mot deforme
    ou pur ; A -> saut 1, B -> saut y)."""
    a = np.ones_like(tg)
    b = np.zeros_like(tg)
    c = np.zeros_like(tg)
    d = np.ones_like(tg)
    for ch in w:
        if ch == "A":
            na, nb = tg * a - c, tg * b - d
        else:
            na, nb = (tg - y) * a - c, (tg - y) * b - d
        nc, nd = a, b
        a, b, c, d = na, nb, nc, nd
    tr = 0.5 * (a + d)
    m = np.abs(tr) <= 1.0
    idx = np.where(m)[0]
    if len(idx) == 0:
        return []
    coupe = np.where(np.diff(idx) > 1)[0]
    debuts = np.concatenate([[0], coupe + 1])
    fins = np.concatenate([coupe, [len(idx) - 1]])
    return [(idx[dd], idx[ff]) for dd, ff in zip(debuts, fins)]


def gaps_ratios(bandes, dt):
    gaps = []
    for i in range(1, len(bandes)):
        g = (bandes[i][0] - bandes[i - 1][1]) * dt
        if g > CELL_EXCL * dt:
            gaps.append(g)
    ratios = [gaps[i + 1] / gaps[i] for i in range(len(gaps) - 1) if gaps[i] > 0]
    return np.array(gaps), np.array(ratios)


def ks_2samp(a, b):
    a, b = np.sort(a), np.sort(b)
    tous = np.sort(np.concatenate([a, b]))
    ea = np.searchsorted(a, tous, side="right") / len(a)
    eb = np.searchsorted(b, tous, side="right") / len(b)
    return float(np.max(np.abs(ea - eb)))


def f1_style(d12, d23, n12a, n12b, n23a, n23b):
    band12 = 0.27 * np.sqrt((n12a + n12b) / (n12a * n12b))
    band23 = 0.27 * np.sqrt((n23a + n23b) / (n23a * n23b))
    return bool(d23 < d12 + band12 + band23 and d23 < d12)


def main():
    rho = float(sys.argv[1])
    t0 = time.time()
    tg = np.linspace(-TMAX, TMAX, GRILLE)
    dt = tg[1] - tg[0]
    mots_purs = {N: mot_fibonacci(MOTS[N]) for N in NIVEAUX}

    print(f"Φ-DYN-5b — F3 rho={rho} [fiche v1.1 SCELLÉE]")

    # reference mot pur via le meme chemin produit
    ref = {}
    for N in NIVEAUX:
        bandes = bandes_produit(mots_purs[N], tg)
        assert len(bandes) == ATTENDUS[N], (N, len(bandes))
        _, r = gaps_ratios(bandes, dt)
        ref[N] = {"n_bandes": len(bandes), "ratios": r}
    d_ref_12_13 = ks_2samp(ref[12]["ratios"], ref[13]["ratios"])
    d_ref_13_14 = ks_2samp(ref[13]["ratios"], ref[14]["ratios"])
    print(f"  référence mot pur (produit) : D(12,13)={d_ref_12_13:.4f} "
          f"D(13,14)={d_ref_13_14:.4f} · comptes "
          f"{[ref[N]['n_bandes'] for N in NIVEAUX]}")

    rng = np.random.default_rng(GRAINE)
    resultats = []
    for k in range(N_REAL):
        masque = rng.random(len(mots_purs[14])) < rho
        per_niveau = {}
        for N in NIVEAUX:
            w = list(mots_purs[N])
            for i in range(len(w)):
                if masque[i]:
                    w[i] = "B" if w[i] == "A" else "A"
            bandes = bandes_produit("".join(w), tg)
            _, r = gaps_ratios(bandes, dt)
            per_niveau[N] = {"n_bandes": len(bandes), "ratios": r}
        d1 = ks_2samp(per_niveau[12]["ratios"], per_niveau[13]["ratios"])
        d2 = ks_2samp(per_niveau[13]["ratios"], per_niveau[14]["ratios"])
        ok = f1_style(d1, d2, len(per_niveau[12]["ratios"]),
                      len(per_niveau[13]["ratios"]),
                      len(per_niveau[13]["ratios"]),
                      len(per_niveau[14]["ratios"]))
        resultats.append({"realisation": k, "D_12_13": d1, "D_13_14": d2,
                          "F1_style": ok,
                          "comptes": [per_niveau[N]["n_bandes"] for N in NIVEAUX]})
        print(f"  réalisation {k + 1:2d}/{N_REAL} : D(12,13)={d1:.4f} "
              f"D(13,14)={d2:.4f} · F1-style {'OK' if ok else 'KO'} · "
              f"comptes {resultats[-1]['comptes']}", flush=True)

    n_ok = sum(1 for r in resultats if r["F1_style"])
    print(f"\n  rho={rho} : F1-style OK dans {n_ok}/{N_REAL} réalisations "
          f"(référence mot pur : D décroît {d_ref_12_13:.4f} → {d_ref_13_14:.4f})")
    print(f"  critère gelé F3 : à rho >= 0.001, échec dans au moins 15/20")

    out = {
        "chantier": "PHI-DYN-5B-F3",
        "fiche": "FICHE-PHI-DYN-5B-POINT-FIXE v1.1 SCELLÉE (3de8d75)",
        "rho": rho, "graine": GRAINE, "n_realisations": N_REAL,
        "reference_pur": {"D_12_13": d_ref_12_13, "D_13_14": d_ref_13_14,
                          "comptes": [ref[N]["n_bandes"] for N in NIVEAUX]},
        "resultats": resultats, "n_F1_ok": n_ok,
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    tag = str(rho).replace(".", "p")
    dest = Path(f"data/phidyn5b_F3_rho{tag}.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"→ {dest}")


if __name__ == "__main__":
    main()
