#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P2 — PALIER C' : construction beta (fiche v1.1, A' PASS)
================================================================
Porteur natif : C(1) matrice seesaw 4x4 (sauts 1,1,1), u_n = Tr C(1)^n.
Test P4 (point 2, section 7) : la suite de Lucas verifie-t-elle une
recurrence NON LINEAIRE d'ordre 3 a coefficients constants
    v_{m+3} = a v_{m+2} v_{m+1} + b v_m + c
sur les sous-suites paire et impaire separement ?
Critere binaire gele : residu max <= 1e-12 -> structure Fricke ;
> 1e-6 -> la dynamique native n'est PAS une restriction de Fricke (T-2').
De plus (verification de la filiation T17) : u_{2m} = 2 Lucas(2m),
recurrence lineaire v_{m+2} = 3 v_{m+1} - v_m.
Sortie : data/phidyn2_p2_palierCp.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
N_MAX = 120


def lucas(n):
    return PHI ** n + (1 - PHI) ** n


def main():
    t0 = time.time()
    print("Φ-DYN-2 P2 — PALIER C' : construction β (embaumement Fricke-Lucas)")
    print("=" * 78)

    C = np.array([[0., 1., 0., 0.],
                  [1., 0., 1., 0.],
                  [0., 1., 0., 1.],
                  [0., 0., 1., 0.]])
    vp = np.linalg.eigvals(C)
    print("valeurs propres C(1) :", sorted([complex(v) for v in vp],
                                           key=lambda z: -abs(z.imag - 0) if abs(z.imag) > 1e-12 else -z.real))
    u = [float(np.trace(np.linalg.matrix_power(C, n))) for n in range(N_MAX)]

    # ---- filiation T17 (CRITERES RELATIFS v1.1 : suite non bornee)
    even = u[0::2]
    lin_res = max(abs(even[m + 2] - 3 * even[m + 1] + even[m])
                  / max(1.0, abs(even[m + 2]))
                  for m in range(len(even) - 2))
    lucas_ok = all(abs(even[m] - 2 * lucas(2 * m)) / max(1.0, abs(even[m])) < 1e-9
                   for m in range(min(20, len(even))))
    print(f"filiation T17 : u_{{2m}} = 2·Lucas(2m) (relatif) : {lucas_ok} · "
          f"récurrence linéaire v_{{m+2}} = 3v_{{m+1}} − v_m : "
          f"résidu relatif max {lin_res:.3e}")
    print(f"sous-suite impaire : max |u_{{2m+1}}| = {max(abs(x) for x in u[1::2]):.1e}"
          f" (identiquement nulle : dégénérée pour le test P4)")

    # ---- P4 : identification non linéaire sur la sous-suite paire
    v = np.array(even)
    M3 = len(v) - 3
    A = np.column_stack([v[2:2 + M3] * v[1:1 + M3], v[:M3], np.ones(M3)])
    b = v[3:3 + M3]
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    a, bb, cc = sol
    residus = np.abs(A @ sol - b)
    res_max = float(residus.max())
    res_rel = float((residus / np.maximum(np.abs(b), 1)).max())
    print(f"\nP4 fit non linéaire v_{{m+3}} = a·v_{{m+2}}·v_{{m+1}} + b·v_m + c :")
    print(f"  a = {a:.6e} · b = {bb:.6e} · c = {cc:.6e}")
    print(f"  résidu max absolu = {res_max:.3e} · relatif = {res_rel:.3e}")
    verdict_p4 = ("FRICKE (<=1e-12)" if res_max <= 1e-12 else
                  "NON_FRICKE (>1e-6)" if res_max > 1e-6 else
                  "ZONE_GRISE (1e-12..1e-6)")
    print(f"  verdict P4 : {verdict_p4}")
    # croissance : v_m ~ 2 phi^{2m} ; si a != 0 le terme produit croit en
    # phi^{4m} et doit dominer — mesure du desequilibre des echelles
    print(f"  échelle : v_10/v_5 = {v[10]/v[5]:.4f} (φ⁶ = {PHI**6:.4f}) — "
          f"croissance φ² par pas, φ⁶ sur 3 pas : un terme produit v·v "
          f"croit en φ⁴·…·, structurellement incompatible avec a ≠ 0")

    out = {
        "chantier": "PHI-DYN-2-P2-PALIER-Cp",
        "fiche": "FICHE-PHI-DYN-2-P2-PORTEUR v1.1 (erratum criteres relatifs, scellee 2026-11-03)",
        "valeurs_propres": [str(complex(v)) for v in vp],
        "filiation_T17": {"u_2m_egal_2_Lucas": bool(lucas_ok),
                          "recurrence_lineaire_residu": lin_res},
        "P4": {"a": float(a), "b": float(bb), "c": float(cc),
               "residu_max_abs": res_max, "residu_max_rel": res_rel,
               "verdict": verdict_p4},
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn2_p2_palierCp.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
