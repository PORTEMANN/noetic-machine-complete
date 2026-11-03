#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P2 — PALIER B' : construction alpha (fiche v1.1, palier A' PASS)
========================================================================
Porteur par substitution : lettres A = M_1(t), B = M_y(t), mot de Fibonacci,
trace map x_{n+1} = 2 x_n x_{n-1} - x_{n-2} (identite verifiee A' V3).

Mesures (fiche §3.3) :
  P2 : kappa(y, t) = Tr([A,B])/2 sur la grille y x seeds ; verification
       I = (k+1)/2 (forme A1 etablie au palier A') ;
  P3 : statut d'orbite a t = ±φ, ±1/φ, N = 200 iterations : portee si
       derive Fricke <= 1e-12 (seuil gelé point 4) ;
  P5 : distance relative orbite(y) vs orbite(y=1) (mesure nouvelle,
       sans cible gelee).
Sortie : data/phidyn2_p2_palierBp.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
GRILLE_Y = [2.0, 1.1, 1.01, 1.001, 1.0001, 1.0]
SEEDS_T = [PHI, -PHI, 1 / PHI, -1 / PHI]
N_ORB = 200
L_ORB = 10_000


def M(v, t):
    return np.array([[t, -v], [1.0 / v, 0.0]])


def orbite_traces(y, t, n=N_ORB):
    """Orbite de la trace map, graines calculees par produits directs."""
    A, B = M(1.0, t), M(y, t)
    x1 = 0.5 * np.trace(A)
    x2 = 0.5 * np.trace(A @ B)
    x3 = 0.5 * np.trace(A @ B @ A)
    xs = [x1, x2, x3]
    for _ in range(n - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    return np.array(xs)


def fricke(xs):
    I = (xs[2:] ** 2 + xs[1:-1] ** 2 + xs[:-2] ** 2
         - 2 * xs[2:] * xs[1:-1] * xs[:-2])
    fini = np.isfinite(I)
    if fini.sum() < 5:
        return np.inf
    If = I[fini]
    return float(If.max() - If.min())


def kappa(y, t):
    A, B = M(1.0, t), M(y, t)
    return 0.5 * np.trace(A @ B @ np.linalg.inv(A) @ np.linalg.inv(B))


def main():
    t0 = time.time()
    print("Φ-DYN-2 P2 — PALIER B' : construction α (porteur par substitution)")
    print("=" * 78)

    # ---- P3 : statuts d'orbite aux seeds gelés ±φ, ±1/φ
    print("P3 : statuts d'orbite (N=200, seuil portée 1e−12) :")
    p3 = {}
    for y in GRILLE_Y:
        ligne = []
        for s in SEEDS_T:
            xs = orbite_traces(y, s)
            drv = fricke(xs)
            bornee = np.isfinite(xs).all() and np.abs(xs).max() <= 1e6
            portee = drv <= 1e-12 and bornee
            ligne.append({"seed": float(s), "derive_fricke": drv,
                          "bornee": bool(bornee), "portee": bool(portee),
                          "max_abs": float(np.nanmax(np.abs(xs)))})
        p3[str(y)] = ligne
        statuts = ["P" if c["portee"] else ("B!" if c["bornee"] else "div")
                   for c in ligne]
        print(f"  y={y:7.4f} : κ={kappa(y, PHI):+.4f} · "
              f"statuts [+φ,−φ,+1/φ,−1/φ] = {statuts} · "
              f"dérives {[f'{c['derive_fricke']:.1e}' for c in ligne]}")

    # ---- P2 : kappa(y) aux seeds (limites y -> 1)
    print("\nP2 : κ(y, t) sur la grille y (dégénérescence propre si κ → 1) :")
    p2 = {}
    for s in SEEDS_T:
        vals = [float(kappa(y, s)) for y in GRILLE_Y]
        p2[str(s)] = vals
        print(f"  t={s:+.4f} : κ = {[round(v, 4) for v in vals]} "
              f"(y = {GRILLE_Y})")

    # ---- P5 : distance orbite(y) -> orbite(1) à t = +φ
    print("\nP5 : distance relative orbite(y) vs orbite(y=1), t=+φ :")
    ref = orbite_traces(1.0, PHI)
    p5 = []
    for y in GRILLE_Y[:-1]:
        xs = orbite_traces(y, PHI)
        d = np.abs(xs - ref)
        rel = float(d.max() / max(1.0, np.abs(ref).max()))
        p5.append({"y": y, "distance_rel_max": rel})
        print(f"  y={y:7.4f} : distance relative max = {rel:.3e}")

    out = {
        "chantier": "PHI-DYN-2-P2-PALIER-Bp",
        "fiche": "FICHE-PHI-DYN-2-P2-PORTEUR v1.1 (erratum criteres relatifs, scellee 2026-11-03)",
        "P3": p3, "P2": p2, "P5": p5,
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn2_p2_palierBp.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
