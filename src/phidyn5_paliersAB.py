#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-5 — PALIERS A (instrument) + B (mesure) — fiche v1.0 SCELLEE (34399d3)
============================================================================
Banc : approximant periodique de Kohmoto niveau 13 (matrice de Jacobi
233x233, sauts suivant W_13 : A -> 1, B -> y=1.5), diagonale nulle.
Blocking : fusion des paires adjacentes d'ecart relatif < delta, moyenne,
itere jusqu'a stabilite (plafond 50). Grille delta : {1/φ, 1/φ², 1/φ³, 1/φ⁴}
(1/φ² = valeur principale gelée ; les trois autres = robustesse pre-enregistree).
Observables : R1 clusters, R2 signature φ des gaps (8 plus grands, ±0.02),
R3 ancre Λ²_sel = ρ² + 3 − a₂/a₀, R4 trajectoire/exposant.
Controles palier A : y=1 = chaine uniforme 2cos(k) ; symetrie spectrale ;
idempotence du blocking ; valeur de controle Λ²_sel(y=1) = 5.
Sortie : data/phidyn5_paliersAB.json
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
NIVEAU = 13
Y_DECL = 1.5
DELTA_PRINCIPAL = 1 / PHI ** 2
DELTAS = [1 / PHI, 1 / PHI ** 2, 1 / PHI ** 3, 1 / PHI ** 4]
PLAFOND_ITER = 50


def mot_fibonacci(n):
    w = "A"
    for _ in range(n):
        w = "".join("AB" if c == "A" else "A" for c in w)
    return w


def jacobi_spectre(y, n=NIVEAU):
    """Matrice de Jacobi : sauts selon W_n (A->1, B->y), diagonale nulle.
    Off-diagonale : hop[i] entre sites i et i+1 (periodique)."""
    w = mot_fibonacci(n - 2)   # W_n : longueur F_n (convention T24, v1.1)
    L = len(w)
    hop = np.array([1.0 if c == "A" else y for c in w], float)
    J = np.zeros((L, L))
    idx = np.arange(L - 1)
    J[idx, idx + 1] = hop[:L - 1]          # liens i <-> i+1
    J[idx + 1, idx] = hop[:L - 1]
    J[L - 1, 0] = hop[L - 1]               # bouclage periodique
    J[0, L - 1] = hop[L - 1]
    return np.linalg.eigvalsh(J)


def blocking(spectre, delta, plafond=PLAFOND_ITER):
    """Fusion iterative : paires adjacentes d'ecart relatif < delta."""
    s = np.sort(np.asarray(spectre, float))
    traj = [len(s)]
    ancres = [ancre(s)]
    for _ in range(plafond):
        if len(s) < 2:
            break
        ecarts = np.abs(np.diff(s)) / np.maximum(np.abs(s[:-1]), 1e-300)
        fusionner = ecarts < delta
        if not fusionner.any():
            break
        nouveau = []
        i = 0
        while i < len(s):
            if i < len(s) - 1 and fusionner[i]:
                nouveau.append(0.5 * (s[i] + s[i + 1]))
                i += 2
            else:
                nouveau.append(s[i])
                i += 1
        s = np.array(nouveau)
        traj.append(len(s))
        ancres.append(ancre(s))
    return s, traj, ancres


def ancre(spectre):
    rho = float(np.max(np.abs(spectre)))
    a0 = float(len(spectre))
    a2 = float(np.sum(spectre ** 2))
    return rho ** 2 + 3.0 - a2 / a0


def signature_phi(spectre, k=8):
    """Ratios des k plus grands gaps consécutifs vs φ (fenêtre ±0,02)."""
    s = np.sort(np.asarray(spectre, float))
    if len(s) < k + 2:
        return None
    gaps = np.diff(s)
    idx = np.argsort(gaps)[::-1][:k + 1]
    idx = np.sort(idx)
    ratios = []
    for i in range(len(idx) - 1):
        if idx[i + 1] == idx[i] + 1 and gaps[idx[i]] > 1e-12:
            r = gaps[idx[i + 1]] / gaps[idx[i]]
            if np.isfinite(r) and r < 100:
                ratios.append(float(r))
    if not ratios:
        return {"n_ratios": 0}
    ecarts = [abs(r - PHI) for r in ratios]
    return {"n_ratios": len(ratios), "ratios": ratios,
            "ecarts_a_phi": ecarts,
            "n_dans_fenetre": int(sum(e <= 0.02 for e in ecarts))}


def main():
    t0 = time.time()
    print("Φ-DYN-5 — PALIERS A (instrument) + B (mesure) [fiche v1.1 SCELLÉE]")
    print("=" * 78)

    # ---------------- PALIER A
    print("PALIER A — contrôles :")
    s_y1 = jacobi_spectre(1.0)
    L = len(s_y1)
    k_uniforme = 2 * np.cos(2 * np.pi * np.arange(L) / L)
    ctl_uniforme = float(np.max(np.abs(np.sort(s_y1) - np.sort(k_uniforme))))
    ctl_reel = bool(np.all(np.isreal(s_y1)))
    ctl_N = (len(s_y1) == 233)
    ctl_trace = float(abs(np.sum(s_y1)))
    s_ctl, traj_ctl, _a = blocking(s_y1, DELTA_PRINCIPAL)
    _, traj_ctl2, _a2 = blocking(s_ctl, DELTA_PRINCIPAL)
    ctl_idem = (traj_ctl2 == [len(s_ctl)])
    ctl_ancre = ancre(s_y1)  # v1.1 : vrai spectre uniforme -> 4+3-2 = 5
    print(f"  A1 y=1 = chaîne uniforme 2cos(k) : max écart {ctl_uniforme:.3e}"
          f" ({L} eigenvalues) → {'PASS' if ctl_uniforme < 1e-12 else 'FAIL'}")
    print(f"  A2 spectre reel {ctl_reel}, N = {len(s_y1)} (=233 : {ctl_N}), "
          f"|trace| = {ctl_trace:.3e} -> "
          f"{'PASS' if ctl_reel and ctl_N and ctl_trace < 1e-12 else 'FAIL'}")
    print(f"  A3 idempotence blocking : {ctl_idem} (traj fixpoint {traj_ctl[-1]})")
    print(f"  A4 ancre Λ²_sel(y=1) = {ctl_ancre:.6f} (attendu 5) → "
          f"{'PASS' if abs(ctl_ancre - 5) < 1e-9 else 'FAIL'}")
    A_ok = ctl_uniforme < 1e-12 and ctl_reel and ctl_N and ctl_trace < 1e-12 \
        and ctl_idem and abs(ctl_ancre - 5) < 1e-9
    print(f"  PALIER A : {'PASS — palier B débloqué' if A_ok else 'FAIL — retour rédaction'}")

    # ---------------- PALIER B
    print("\nPALIER B — mesure (banc niveau 13, y = 1,5) :")
    s15 = jacobi_spectre(Y_DECL)
    print(f"  spectre brut : {len(s15)} eigenvalues, ρ = "
          f"{np.max(np.abs(s15)):.4f}, ancre = {ancre(s15):.6f}")
    resultats = {}
    for d in DELTAS:
        sb, traj, ancres_traj = blocking(s15, d)
        anc = ancre(sb)
        sig = signature_phi(sb)
        # R4 : decroissance de N en log-log (exposant apparent)
        r4_pente = None
        if len(traj) > 2 and traj[-1] < traj[0]:
            n_it = np.arange(1, len(traj) + 1, dtype=float)
            r4_pente = float(np.polyfit(np.log(n_it), np.log(np.maximum(traj, 1)), 1)[0])
        resultats[str(round(d, 6))] = {
            "delta": d, "traj_N": traj, "N_fixpoint": len(sb),
            "ancre_fixpoint": anc,
            "signature_phi": sig, "R4_exposant_loglog": r4_pente,
            "R4_ancre_par_iteration": ancres_traj,
            "R4_monotone": bool(all(np.diff(ancres_traj) > 0)) if len(ancres_traj) > 1 else None,
        }
        ligne_sig = (f"ratios φ {sig['n_dans_fenetre']}/{sig['n_ratios']}"
                     if sig and sig["n_ratios"] else "pas de ratios")
        print(f"  δ={d:.6f} : N {traj[0]}→{len(sb)} (itérations {len(traj) - 1})"
              f" · ancre → {anc:.6f} · {ligne_sig}")

    # robustesse : verdict qualitatif par delta
    def qualitatif(r):
        sig = r["signature_phi"]
        phi_ok = sig and sig["n_ratios"] and sig["n_dans_fenetre"] > 0
        return "phi_fixe" if phi_ok else "phi_ecoule"
    verdicts = {d: qualitatif(r) for d, r in resultats.items()}
    robustes = len(set(verdicts.values())) == 1
    print(f"\n  verdicts qualitatifs par δ : {verdicts}")
    print(f"  robustesse (tueur T-1''') : {'verdict unique → robuste' if robustes else 'VERDICT δ-DÉPENDANT'}")

    # contrôle niveau 14
    s14 = jacobi_spectre(Y_DECL, n=14)
    sb14, traj14, _a14 = blocking(s14, DELTA_PRINCIPAL)
    ctl14 = {"N_fixpoint_13": resultats[str(round(DELTA_PRINCIPAL, 6))]["N_fixpoint"],
             "N_fixpoint_14": len(sb14)}
    print(f"  contrôle niveau 14 : N fixpoint 377-pts = {len(sb14)} "
          f"(vs 233-pts = {ctl14['N_fixpoint_13']})")

    out = {
        "chantier": "PHI-DYN-5-PALIERS-AB",
        "fiche": "FICHE-PHI-DYN-5-RG-SPECTRALE v1.1 SCELLÉE (0ef9289)",
        "palier_A": {"uniforme": ctl_uniforme, "reel": ctl_reel, "N": len(s_y1),
                     "trace": ctl_trace,
                     "idempotence": bool(ctl_idem), "ancre_controle": ctl_ancre,
                     "pass": bool(A_ok)},
        "palier_B": resultats,
        "verdicts_par_delta": verdicts, "robuste": bool(robustes),
        "controle_niveau_14": ctl14,
        "duree_s": round(time.time() - t0, 2),
    }
    out["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    dest = Path("data/phidyn5_paliersAB.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    print(f"\n→ {dest}")


if __name__ == "__main__":
    main()
