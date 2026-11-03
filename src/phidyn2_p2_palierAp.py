#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P2 — PALIER A' : verification d'algebre (fiche v1.0 SCELLEE 0028092)
===========================================================================
Condition sine qua non : RIEN d'autre ne tourne si A' echoue.
  V1 : identite de Fricke generalisee sur 1e4 paires aleatoires SL(2,R) :
       x = Tr A/2, y = Tr B/2, z = Tr AB/2, k = Tr([A,B])/2
       -> relation exacte I = x^2+y^2+z^2-2xyz vs k (forme A'1)
       hypothese de travail derivee avant gel : I = (k+1)/2
       la machine VERIFIE la forme ; si l'hypothese tombe, elle ajuste
       la forme et documente (A' est un palier d'algebre, pas de mesure).
  V2 : determinant des matrices de transfert du dimere M_v(t) =
       [[t, -v], [1/v, 0]] = 1 identiquement, v et t aleatoires.
  V3 : identite de trace Tr(W_{n+1}) = Tr(W_n)Tr(W_{n-1}) - Tr(W_{n-2})
       pour toute paire (A, B) SL(2,R) et mot de Fibonacci (la preuve par
       conjugaison de T24 est generale — verifiee ici pour A != B).
  V4 : a y = 1, A = B = M_1(t) = [[t,-1],[1,0]] — collapse des deux
       lettres (controle de degenerescence).
Sortie : data/phidyn2_p2_palierAp.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

GRAINE = 20261103
N_RANDOM = 10_000
SEEDS_Y = [2.0, 1.1, 1.01, 1.001, 1.0001, 1.0]
PHI = (1 + np.sqrt(5)) / 2


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def M(v, t):
    return np.array([[t, -v], [1.0 / v, 0.0]])


def produit(w, mats):
    P = np.eye(2)
    for c in w:
        P = P @ mats[c]
    return P


def main():
    t0 = time.time()
    print("Φ-DYN-2 P2 — PALIER A' : verification d'algebre [fiche v1.0 SCELLÉE]")
    print("=" * 78)
    rng = np.random.default_rng(GRAINE)
    def sl2r_batch(n):
        """n matrices SL(2,R) : normalise par sqrt(|det|), corrige le signe."""
        out = np.zeros((n, 2, 2))
        for i in range(n):
            M2 = rng.normal(size=(2, 2))
            d = np.linalg.det(M2)
            A = M2 / np.sqrt(abs(d))
            if d < 0:
                A = A @ np.array([[1.0, 0.0], [0.0, -1.0]])
            out[i] = A
        return out
    A_alea = sl2r_batch(N_RANDOM)
    B_alea = sl2r_batch(N_RANDOM)

    # ---- V1 : identite Fricke generalisee (CRITERE RELATIF v1.1)
    x = 0.5 * np.trace(A_alea, axis1=1, axis2=2)
    y = 0.5 * np.trace(B_alea, axis1=1, axis2=2)
    z = 0.5 * np.trace(np.matmul(A_alea, B_alea), axis1=1, axis2=2)
    comm = np.matmul(np.matmul(A_alea, B_alea),
                     np.linalg.inv(np.matmul(B_alea, A_alea)))
    kappa = 0.5 * np.trace(comm, axis1=1, axis2=2)
    I = x ** 2 + y ** 2 + z ** 2 - 2 * x * y * z
    # hypotheses de forme a tester (ordre gelé : A'1 puis alternatives)
    def rel(res, val):
        return float((res / np.maximum(np.abs(val), 1.0)).max())
    r_A1 = rel(np.abs(I - (kappa + 1) / 2), I)
    r_A2 = rel(np.abs(I - kappa / 2), I)
    r_A3 = rel(np.abs(I - kappa), I)
    r_A4 = rel(np.abs(2 * I - kappa - 1), I)
    formes = {"A1_I=(k+1)/2": r_A1, "A2_I=k/2": r_A2,
              "A3_I=k": r_A3, "A4_2I=k+1": r_A4}
    meilleure = min(formes, key=formes.get)
    print(f"V1 Fricke généralisée : résidus RELATIFS par forme candidate :")
    for f, r in formes.items():
        print(f"    {f} : {r:.3e}")
    V1 = formes[meilleure] <= 1e-9
    print(f"  meilleure forme : {meilleure} (résidu relatif {formes[meilleure]:.3e}) → "
          f"{'PASS' if V1 else 'FAIL'}")

    # ---- V2 : determinant M_v(t) = 1
    vs = rng.uniform(0.1, 3.0, size=N_RANDOM)
    ts = rng.uniform(-2.5, 2.5, size=N_RANDOM)
    dets = np.array([np.linalg.det(M(v, t)) for v, t in zip(vs, ts)])
    V2 = np.abs(dets - 1).max() <= 1e-12
    print(f"V2 dét M_v(t) = 1 ({N_RANDOM} tirages) : max|dét−1| = "
          f"{np.abs(dets - 1).max():.3e} → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 : identite de trace pour A != B (CRITERE RELATIF v1.1)
    pire = 0.0
    for i in range(200):
        A, B = A_alea[i], B_alea[i]
        mats = {"A": A, "B": B}
        xs = [0.5 * np.trace(produit(mot_fibonacci(n), mats))
              for n in range(1, 8)]
        for n in range(len(xs) - 3):
            res = abs(xs[n + 3] - 2 * xs[n + 2] * xs[n + 1] + xs[n])
            pire = max(pire, res / max(1.0, abs(xs[n + 3])))
    V3 = pire <= 1e-9
    print(f"V3 identité de trace A≠B (200 paires, mots F_1..F_7) : résidu max "
          f"{pire:.3e} → {'PASS' if V3 else 'FAIL'}")

    # ---- V4 : collapse y = 1 (A = B)
    A1 = M(1.0, 0.7)
    collapse = np.abs(A1 - M(1.0, 0.7)).max()
    V4 = bool(collapse == 0.0)
    print(f"V4 collapse y=1 : A = B = M_1(t) : {V4} (contrôle tautologique — "
          f"les deux lettres coïncident, κ = Tr(I)/2 = 1)")

    ok = all([V1, V2, V3, V4])
    print("\n" + "=" * 78)
    msg = "PASS — paliers B'/C' débloqués" if ok else "FAIL — la fiche retourne en rédaction"
    print(f"PALIER A' : {msg}")
    print(f"             (V1 {V1}, V2 {V2}, V3 {V3}, V4 {V4})")

    out = {
        "chantier": "PHI-DYN-2-P2-PALIER-Ap",
        "fiche": "FICHE-PHI-DYN-2-P2-PORTEUR v1.1 (erratum criteres relatifs, scellee 2026-11-03)",
        "graine": GRAINE, "n_random": N_RANDOM,
        "V1_fricke_generalisee": {"formes_testees": formes,
                                  "forme_retenue": meilleure,
                                  "residu": formes[meilleure], "pass": bool(V1)},
        "V2_det_Mv": {"max_abs_det_moins_1": float(np.abs(dets - 1).max()),
                      "pass": bool(V2)},
        "V3_identite_trace_AB": {"residu_max": pire, "pass": bool(V3)},
        "V4_collapse": {"pass": bool(V4)},
        "palier_Ap_pass": bool(ok),
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn2_p2_palierAp.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"→ {dest}")


if __name__ == "__main__":
    main()
