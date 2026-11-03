#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BRUME-1 — La brume sous phason (fiche v1.0 SCELLEE d4949d1)
=============================================================
Instrument : anneau M-pair non-Hermitien (NOTE-CORRESPONDANCE-RESOLUE)
niveaux 12/13/14 ; flips phason Bernoulli (graine 20261103 par rho) ;
grille rho {0, 0.001, 0.01, 0.05, 0.15, 0.3} x 20 realisations.
Observables gelés : B1 mediane |Im| (le delta de brume), B2 max |Im|,
B3 fraction Im>0.05, B4 fraction hors discriminant (structure),
B5 etendue reelle ; annexe A : ancre complexe <-> delta.
Sortie : data/brume1_paliersAB.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from mpmath import mp, mpf

C = np.exp(2j * np.pi / 3)
GRAINE = 20261103
RHOS = [0.0, 0.001, 0.01, 0.05, 0.15, 0.3]
N_REAL = 20
NIVEAU_PRINCIPAL = 13
NIVEAUX = [12, 13, 14]
TOL_VAR = 0.20


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if ch == "A" else "A" for ch in w)
    return w


MOTS = {N: mot_fibonacci(N - 2) for N in NIVEAUX}


def xN_precis(N, t, dps=40):
    mp.dps = dps
    tt = mpf(t)
    a = mpf("0.5") * tt
    b = mpf("0.5") * (tt * (tt - 1) - 1)
    c = mpf("0.5") * (tt * (tt * (tt - 1) - 1) - (tt - 1))
    for _ in range(N - 3):
        a, b, c = b, c, 2 * c * b - a
    return c


def anneau_M(word):
    """Anneau M-pair : psi_{n+1} = (E - v_n) psi_n - q_n psi_{n-1}."""
    L = len(word)
    v = np.array([0.0 if ch == "A" else 1.0 for ch in word])
    q = np.array([1.0 + 0j if ch == "A" else C for ch in word])
    J = np.diag(v).astype(complex)
    for n in range(L):
        J[(n + 1) % L, n] = 1.0
        J[n, (n - 1) % L] = q[(n - 1) % L]
    vals, vecs = np.linalg.eig(J)
    return vals, J


def observables(vals, N):
    re, im = vals.real, np.abs(vals.imag)
    ancre = float(np.max(np.abs(vals)) ** 2 + 3.0
                  - np.mean(np.abs(vals) ** 2))
    hors = 0
    for la in vals[::3]:
        if abs(xN_precis(N, float(la.real))) > 1 + 1e-9:
            hors += 1
    return {
        "B1_median_im": float(np.median(im)),
        "B2_max_im": float(im.max()),
        "B3_frac_im": float((im > 0.05).mean()),
        "B4_frac_hors": float(hors / len(vals[::3])),
        "B5_re_etendue": [float(re.min()), float(re.max())],
        "ancre_cplx": ancre,
    }


def main():
    t0 = time.time()
    print("BRUME-1 — la brume sous phason [fiche v1.0 SCELLÉE]")
    print("=" * 78)

    # ---- PALIER A : exactitude instrument (niveau 13 pur)
    print("PALIER A — exactitude de l'instrument (niveau 13, mot pur) :")
    vals0, J0 = anneau_M(MOTS[13])
    v0, w0 = np.linalg.eig(J0)
    idx = np.random.default_rng(1).choice(len(v0), 12, replace=False)
    residus = [float(np.max(np.abs(J0 @ w0[:, i] - v0[i] * w0[:, i])))
               for i in idx]
    trace = float(np.trace(J0).real)
    nB = MOTS[13].count("B")
    print(f"  résidu max (12 modes) : {max(residus):.2e} (seuil 1e-8)")
    print(f"  Tr(J) = {trace:.1f} (attendu {nB})")
    A_ok = max(residus) <= 1e-8 and abs(trace - nB) <= 1e-9
    print(f"  PALIER A : {'PASS' if A_ok else 'FAIL'}")

    # ---- PALIER B : grille rho complete
    print("\nPALIER B — grille phason (niveau 13 principal) :")
    reference = None
    resultats = {}
    for rho in RHOS:
        rng = np.random.default_rng(GRAINE)
        obs_list = []
        for k in range(N_REAL):
            if rho == 0.0:
                word = MOTS[13]
            else:
                masque = rng.random(len(MOTS[14])) < rho
                wl = list(MOTS[13])
                for i in range(len(wl)):
                    if masque[i]:
                        wl[i] = "B" if wl[i] == "A" else "A"
                word = "".join(wl)
            vals, _ = anneau_M(word)
            obs_list.append(observables(vals, 13))
        agg = {key: float(np.mean([o[key] for o in obs_list]))
               for key in ["B1_median_im", "B2_max_im", "B3_frac_im",
                           "B4_frac_hors", "ancre_cplx"]}
        agg["B5_re_etendue"] = obs_list[0]["B5_re_etendue"]
        agg["ecart_type_B1"] = float(np.std([o["B1_median_im"] for o in obs_list]))
        resultats[str(rho)] = agg
        if rho == 0.0:
            reference = agg
        print(f"  rho={rho:5.3f} : B1={agg['B1_median_im']:.4f} (σ "
              f"{agg['ecart_type_B1']:.3f}) · B2={agg['B2_max_im']:.4f} · "
              f"B3={agg['B3_frac_im']:.3f} · B4={agg['B4_frac_hors']:.3f} · "
              f"ancre={agg['ancre_cplx']:.4f}")

    # criteres pre-enregistres
    ref_B1, ref_B3 = reference["B1_median_im"], reference["B3_frac_im"]
    var_B1 = {r: abs(resultats[str(r)]["B1_median_im"] - ref_B1) / ref_B1
              for r in RHOS}
    var_B3 = {r: abs(resultats[str(r)]["B3_frac_im"] - ref_B3) / max(ref_B3, 1e-9)
              for r in RHOS}
    morte_B1 = next((r for r in RHOS[1:] if var_B1[r] > TOL_VAR), None)
    morte_B3 = next((r for r in RHOS[1:] if var_B3[r] > TOL_VAR), None)
    print(f"\n  variation B1 vs rho=0 : "
          f"{[f'{r}:{var_B1[r]:.2f}' for r in RHOS]}")
    print(f"  variation B3 vs rho=0 : "
          f"{[f'{r}:{var_B3[r]:.2f}' for r in RHOS]}")
    print(f"  frontiere (tol {TOL_VAR:.0%}) : B1 -> {morte_B1} · B3 -> {morte_B3}")
    robuste = all(v <= TOL_VAR for v in list(var_B1.values())[1:])
    print(f"  H-BRUME (robuste jusqu'a rho=0.3) : {robuste}")

    # contrôle niveau 14 a rho=0 et rho=0.15
    print("\n  contrôle niveau 14 :")
    ctl = {}
    for rho in [0.0, 0.15]:
        rng = np.random.default_rng(GRAINE)
        obs = []
        for k in range(6):
            if rho == 0.0:
                word = MOTS[14]
            else:
                masque = rng.random(len(MOTS[14])) < rho
                wl = list(MOTS[14])
                for i in range(len(wl)):
                    if masque[i]:
                        wl[i] = "B" if wl[i] == "A" else "A"
                word = "".join(wl)
            vals, _ = anneau_M(word)
            obs.append(observables(vals, 14))
        agg = {key: float(np.mean([o[key] for o in obs]))
               for key in ["B1_median_im", "B3_frac_im", "B4_frac_hors"]}
        ctl[str(rho)] = agg
        print(f"    rho={rho} : B1={agg['B1_median_im']:.4f} · "
              f"B3={agg['B3_frac_im']:.3f} · B4={agg['B4_frac_hors']:.3f}")

    # ---- annexe A : ancre vs delta
    print("\nAnnexe A — co-évolution (ancre, δ=B1) :")
    annexe = [{"rho": r, "ancre": resultats[str(r)]["ancre_cplx"],
               "delta": resultats[str(r)]["B1_median_im"]} for r in RHOS]
    for a in annexe:
        print(f"  rho={a['rho']:5.3f} : ancre={a['ancre']:.4f} · δ={a['delta']:.4f}")
    la = np.log([a["ancre"] for a in annexe])
    ld = np.log([a["delta"] for a in annexe])
    pente = float(np.polyfit(la, ld, 1)[0]) if len(set(la)) > 1 else None
    print(f"  pente log-log δ vs ancre : {pente:.3f} (attendu −0,5 si "
          f"δ ∝ µ_eff^{{-1/2}})")

    out = {
        "chantier": "BRUME-1-PALIERS-AB",
        "fiche": "FICHE-BRUME-1-PHASON v1.0 SCELLÉE (d4949d1)",
        "palier_A_pass": bool(A_ok),
        "grille_rho": RHOS, "n_realisations": N_REAL,
        "resultats": resultats,
        "criteres": {"var_B1": {str(k): v for k, v in var_B1.items()},
                     "var_B3": {str(k): v for k, v in var_B3.items()},
                     "frontiere_B1": morte_B1, "frontiere_B3": morte_B3,
                     "robuste": bool(robuste)},
        "controle_niveau_14": ctl,
        "annexe_A": {"trajectoire": annexe, "pente_loglog": pente},
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/brume1_paliersAB.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
