#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — point d'entrée de rejou du banc spectral (Machine III)
================================================================
Le certificat d'etalonnage (Banc-spectral-KO6-machine-III.pdf, §5) promet :
    python run.py --chantier <id>

Rejou honnete : chaque chantier rejouable re-execute le calcul reel et
compare le resultat a la valeur consignee (avec sa source). Un divergence
est un incident metrologique : elle doit etre signalee.

Usage :
    python run.py --liste                 # carte des rejou
    python run.py --chantier kohmoto      # Fricke + comptes de bandes (T24/ΦDYN2-P1)
    python run.py --chantier brume        # profil imaginaire M-pair (CORRESPONDANCE/BRUME-1)
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parent
DOCS = RACINE / "docs"
DATA = RACINE / "data"

CAS = {
    "kohmoto": {
        "titre": "Chaînon de Fibonacci — Fricke 2,6e−30, comptes T24",
        "sources": ["data/t24_ko6_cantor_verdict.json",
                    "data/phidyn2_p1_pilierA.json"],
        "attendu": "Fricke conservee a 1e−12 sur orbites de bandes · "
                   "comptes 19/30/48/78/126/202 (niveaux 9–14)",
    },
    "brume": {
        "titre": "Brume spectrale — anneau M-pair non-Hermitien (niveau 13)",
        "sources": ["data/brume1_paliersAB.json"],
        "attendu": "médiane |Im| ≈ 0,627 · 0 % hors discriminant (mot pur)",
    },
}

ARCHIVES = [
    ("T13", "zéro protégé de ℂ⊕M₂(ℂ)", "docs/NOTE-BILAN-MACHINES.md + campagne d'origine"),
    ("T9/T10", "mort du junk U(1) par sa trace", "docs/ (compte-rendu) — pas de rejeu en une commande"),
    ("T3/E1", "erratum « 63 160 »", "erratum daté au registre — l'archive est le document"),
]


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def rejou_kohmoto():
    print("== REJOU kohmoto — chaînon de Fibonacci, discriminant T24 ==")
    tg = np.linspace(-2.5, 2.5, 1 << 18)
    ok = True
    # 1. comptes de bandes niveaux 9..14 (recurrence T24)
    attendus = {9: 19, 10: 30, 11: 48, 12: 78, 13: 126, 14: 202}
    comptes = {}
    for N in attendus:
        xs = [0.5 * tg, 0.5 * (tg * (tg - 1.0) - 1.0),
              0.5 * (tg * (tg * (tg - 1.0) - 1.0) - (tg - 1.0))]
        for _ in range(N - 3):
            xs.append(2 * xs[-1] * xs[-2] - xs[-3])
        m = np.abs(xs[-1]) <= 1.0
        idx = np.where(m)[0]
        c = 0 if len(idx) == 0 else 1 + int(np.sum(np.diff(idx) > 1))
        comptes[N] = c
        statut = "OK" if c == attendus[N] else "DIVERGENCE"
        ok &= c == attendus[N]
        print(f"   niveau {N:2d} : {c:3d} bandes (attendu {attendus[N]}) : {statut}")
    # 2. conservation de Fricke sur seeds de bandes (référence exacte limsup,
    #    protocole ΦDYN2-P1 v1.1 — les seeds aveugles sont classés d'abord)
    rng = np.random.default_rng(20261103)
    portees = 0
    bandes = 0
    total = 0
    for _ in range(64):
        t = float(rng.uniform(-1.45, 2.4))
        xs0 = [0.5 * t, 0.5 * (t * (t - 1.0) - 1.0),
               0.5 * (t * (t * (t - 1.0) - 1.0) - (t - 1.0))]
        limsup = 0.0
        xs_ref = list(xs0)
        for n in range(3, 120):
            vv = 2 * xs_ref[-1] * xs_ref[-2] - xs_ref[-3]
            xs_ref.append(vv)
            if abs(vv) > limsup:
                limsup = abs(vv)
            if limsup > 1.0 and n > 25:
                break
        if limsup > 1.0:
            continue                      # gap : orbite divergente, hors critère
        bandes += 1
        xs = list(xs0)
        for _ in range(997):
            xs.append(2 * xs[-1] * xs[-2] - xs[-3])
        a = np.array(xs[2:])
        I = a ** 2 + np.array(xs[1:-1]) ** 2 + np.array(xs[:-2]) ** 2 \
            - 2 * a * np.array(xs[1:-1]) * np.array(xs[:-2])
        fini = np.isfinite(I)
        if fini.sum() > 10 and (I[fini].max() - I[fini].min()) <= 1e-12:
            portees += 1
        total += 1
    ok_f = bandes > 0 and portees == bandes
    print(f"   Fricke : {portees}/{bandes} orbites de bandes portées (écart ≤ 1e−12) : "
          f"{'OK' if ok_f else 'DIVERGENCE'}")
    ok &= ok_f
    print(f"VERDICT DU REJOU : {'CONFORME au journal' if ok else 'INCIDENT — signaler'}")
    return 0 if ok else 1


def rejou_brume():
    print("== REJOU brume — anneau M-pair (c = e^{2iπ/3}), niveau 13 ==")
    from mpmath import mp, mpf
    mp.dps = 40
    C = np.exp(2j * np.pi / 3)
    w = mot_fibonacci(11)          # W_13, 233 sites
    L = len(w)
    v = np.array([0.0 if ch == "A" else 1.0 for ch in w])
    q = np.array([1.0 + 0j if ch == "A" else C for ch in w])
    J = np.diag(v).astype(complex)
    for n in range(L):
        J[(n + 1) % L, n] = 1.0
        J[n, (n - 1) % L] = q[(n - 1) % L]
    vals, _ = np.linalg.eig(J)
    im = np.abs(vals.imag)
    mediane = float(np.median(im))

    def xN(t):
        tt = mpf(t)
        a = mpf("0.5") * tt
        b = mpf("0.5") * (tt * (tt - 1) - 1)
        c = mpf("0.5") * (tt * (tt * (tt - 1) - 1) - (tt - 1))
        for _ in range(10):
            a, b, c = b, c, 2 * c * b - a
        return c
    hors = sum(1 for la in vals[::3]
               if abs(xN(float(la.real))) > 1 + 1e-9)
    frac_hors = hors / len(vals[::3])
    attendu = json.loads((DATA / "brume1_paliersAB.json").read_text(encoding="utf-8"))
    ref = attendu["resultats"]["0.0"]
    ok_med = abs(mediane - ref["B1_median_im"]) / ref["B1_median_im"] <= 0.02
    ok_disc = frac_hors <= 0.01
    print(f"   médiane |Im| = {mediane:.4f} (journal : {ref['B1_median_im']:.4f}) : "
          f"{'OK' if ok_med else 'DIVERGENCE'}")
    print(f"   fraction hors discriminant = {frac_hors:.3%} (attendu ≤ 1 %) : "
          f"{'OK' if ok_disc else 'DIVERGENCE'}")
    ok = ok_med and ok_disc
    print(f"VERDICT DU REJOU : {'CONFORME au journal' if ok else 'INCIDENT — signaler'}")
    return 0 if ok else 1


def liste():
    print("REJOU DU BANC SPECTRAL — carte des cas\n")
    for cle, c in CAS.items():
        print(f"  {cle:10s} {c['titre']}")
        print(f"             attendu : {c['attendu']}")
        for s in c["sources"]:
            chemin = RACINE / s
            marque = "présent" if chemin.exists() else "ABSENT"
            print(f"             journal : {s} [{marque}]")
        print()
    print("Consignés, non rejouables en une commande (archive = le document) :")
    for cid, titre, ou in ARCHIVES:
        print(f"  {cid:10s} {titre} — {ou}")


def main():
    p = argparse.ArgumentParser(prog="run.py", description="Rejou du banc spectral KO-6")
    p.add_argument("--liste", action="store_true", help="carte des rejou")
    p.add_argument("--chantier", choices=list(CAS.keys()), help="id du cas à rejouer")
    args = p.parse_args()
    if args.liste or not args.chantier:
        liste()
        return 0
    return {"kohmoto": rejou_kohmoto, "brume": rejou_brume}[args.chantier]()


if __name__ == "__main__":
    sys.exit(main())
