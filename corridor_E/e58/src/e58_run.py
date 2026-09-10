#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E58 — RÉSEAU IMPRIMÉ : un réseau ordonné de lignes, écrit directement,
persiste-t-il ?   [protocole E58-RESEAU-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E58. Protocole gelé dans
e58_protocole.json (haché avant tout calcul — aveugle préservé).

Motivation (corridor, 09/09/2026) : la cristallisation spontanée est
réfutée (E57) ; la persistance de la relation est au plancher (E56-x) ;
le seul précédent de relation conservée est le réseau ordonné (R4b,
documentaire). E58 teste la dernière cellule de la carte : écrire
directement le réseau ordonné, puis mesurer s'il tient.

Construction gelée : réseau triangulaire de lignes axiales (winding +1)
dans le récipient d'E44-B : pas a0=8 mailles, sites avec Rg<22 (figé) ;
ψ = Π_i tanh(d_i/δ)·exp(iθ_i), δ=1,5 (filiation E50) ; paroi à
circulation = nombre de lignes imprimées (commensurable, figé) ;
relaxation 100 pas (γ=0,3) puis snapshots t=45, 90 (et entrée t=5).
Bras A : réseau ordonné + rotation (le test : l'ordre persiste-t-il ?) ;
bras B : mêmes lignes aux positions brassées (graine 770001, figée) +
rotation (l'ordre se forme-t-il ? — témoin de nucléation d'ordre).
Campagne déterministe (A) + une graine figée (B) — déclaré.

Usage : python3 e58_run.py            (campagne — interdit avant décision)
        python3 e58_run.py --smoke    (validation technique déclarée :
                                       N=32, homothétie, hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments  # filiation byte-level

# ---------------- paramètres gelés (filiation E44→E57, sauf mention) --------
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
PAS_A0 = 8.0            # pas du réseau triangulaire, figé
R_SITES = 22.0          # sites avec Rg < 22 (figé)
DELTA_COEUR = 1.5
PAS_RELAX = 100
SNAP = [(900, 45.0), (1800, 90.0)]
SEUIL_PSI6 = 0.7
FACTEUR_VOISINS = 1.3
GRAINE_BRASSEE = 770001   # figée
LONG_MIN = 40
ETENDUE_Z_MIN = 30.0


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_, fix=None):
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * (np.abs(psi)**2 - 1.0) * dt_ / 2)
    if fix is not None:
        psi[fix[0]] = fix[1][fix[0]]
    return psi


def geometrie_B(N_, wind):
    C = (N_ - 1) / 2.0
    Xg, Yg, Zg = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                             indexing='ij')
    Rg = np.sqrt((Xg - C)**2 + (Yg - C)**2)
    z0, z1 = int(2 * N_ / 64), int(61 * N_ / 64)
    inside = (Rg < 26 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    ring = (Rg >= 26 * N_ / 64) & (Rg < 28 * N_ / 64) & (Zg >= z0) & (Zg <= z1)
    PHI = np.arctan2(Yg - C, Xg - C)
    fix_val = np.zeros((N_,) * 3, dtype=complex)
    fix_val[ring] = np.exp(1j * wind * PHI[ring])
    return inside, ring, fix_val, C, (Xg, Yg, Zg)


def sites_reseau(N_, C, brouiller=False):
    """Sites triangulaires figés ; brassés (même compte, positions
    aléatoires dans Rg < 22, graine figée) pour le bras B."""
    s = N_ / 64.0
    a0, rmax = PAS_A0 * s, R_SITES * s
    sites = []
    j = 0
    y = C - rmax
    while y <= C + rmax:
        x = C - rmax + (0.5 * a0 if j % 2 else 0.0)
        while x <= C + rmax:
            if (x - C)**2 + (y - C)**2 < rmax**2:
                sites.append((x, y))
            x += a0
        y += a0 * np.sqrt(3) / 2
        j += 1
    sites = np.array(sites)
    if brouiller:
        rng = np.random.default_rng(GRAINE_BRASSEE)
        n = len(sites)
        th = rng.uniform(0, 2 * np.pi, n)
        rr = rmax * np.sqrt(rng.uniform(0, 1, n))
        sites = np.stack([C + rr * np.cos(th), C + rr * np.sin(th)],
                         axis=1)
    return sites


def imprime_reseau(N_, sites):
    """ψ = Π_i tanh(d_i/δ)·exp(iθ_i) — multi-vortex, filiation E50."""
    s = N_ / 64.0
    X, Y = np.meshgrid(np.arange(N_), np.arange(N_), indexing='ij')
    psi_xy = np.ones((N_, N_), dtype=complex)
    for x0, y0 in sites:
        d = np.sqrt((X - x0)**2 + (Y - y0)**2)
        psi_xy *= np.tanh(d / (DELTA_COEUR * s)) * np.exp(
            1j * np.arctan2(Y - y0, X - x0))
    return np.repeat(psi_xy[:, :, None], N_, axis=2)


def positions_lignes(psi, inside, Xg, Yg, Zg):
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    # Masquage au niveau des COINS de plaquette (filiation exacte
    # d'E44-B : mask_plaq_B de e44_run.py) — le masquage par cellule
    # créait des anomalies artificielles au bord (mesuré en smoke64 :
    # 1 par ligne) ; celui-ci est celui de la campagne de référence.
    r = lambda x, a: np.roll(x, -1, a)
    def mask_plaq(w, ax):
        if ax == 0:
            corners = [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]
        elif ax == 1:
            corners = [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)]
        else:
            corners = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        keep = np.ones(w.shape, bool)
        for dx, dy, dz in corners:
            idx = (np.clip(Xg + dx, 0, w.shape[0] - 1),
                   np.clip(Yg + dy, 0, w.shape[1] - 1),
                   np.clip(Zg + dz, 0, w.shape[2] - 1))
            keep &= inside[idx]
        return np.where(keep, w, 0)
    wx, wy, wz = mask_plaq(wx, 0), mask_plaq(wy, 1), mask_plaq(wz, 2)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f['closed'] and not np.any(f['disp']))]
    axiaux = [f for f in ouverts
              if f['len'] >= LONG_MIN
              and (f['pts'][:, 2].max() - f['pts'][:, 2].min())
              >= ETENDUE_Z_MIN]
    pos = np.array([f['pts'][:, :2].mean(axis=0) for f in axiaux]) \
        if axiaux else np.zeros((0, 2))
    return pos, len(axiaux), anom, amb


def psi6(pos):
    """Identique à E57 (figé)."""
    n = len(pos)
    if n < 6:
        return None
    D = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    d_med = float(np.median(D.min(axis=1)))
    r_nn = FACTEUR_VOISINS * d_med
    tot = 0.0 + 0.0j
    for j in range(n):
        nn = [k for k in range(n) if D[j, k] <= r_nn]
        if not nn:
            continue
        th = [np.arctan2(pos[k, 1] - pos[j, 1], pos[k, 0] - pos[j, 0])
              for k in nn]
        tot += np.mean(np.exp(6j * np.array(th)))
    return float(np.abs(tot / n))


def main():
    if "--smoke64" in sys.argv:
        # Validation de l'instrument à l'échelle campagne (déclarée) :
        # construction + lecture de l'état d'ENTRÉE uniquement — aucune
        # évolution temporelle, aucune donnée de campagne produite.
        print("SMOKE64 — validation de l'entrée (N=64, sans évolution)")
        C = (N - 1) / 2.0
        sites = sites_reseau(N, C)
        inside, ring, fix_val, _, (Xg, Yg, Zg) = geometrie_B(N, len(sites))
        psi = imprime_reseau(N, sites)
        pos, nl, anom, amb = positions_lignes(psi, inside, Xg, Yg, Zg)
        p6 = psi6(pos)
        print("SMOKE64 :", {"n_sites": len(sites), "n_axiaux": nl,
                            "psi6_entree": round(p6, 3) if p6 else None,
                            "anom": anom, "amb": amb})
        return
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32 (homothétie), hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        inside, ring, fix_val, C, (Xg, Yg, Zg) = geometrie_B(32, 4)
        sites = sites_reseau(32, C)
        psi = imprime_reseau(32, sites)
        pos, nl, anom, amb = positions_lignes(psi, inside, Xg, Yg, Zg)
        print("SMOKE :", {"n_sites": len(sites), "n_axiaux": nl,
                          "psi6_entree": round(psi6(pos), 3)
                          if nl >= 6 else None, "anom": anom, "amb": amb})
        return

    t0 = time.time()
    C = (N - 1) / 2.0
    sites_A = sites_reseau(N, C)
    sites_B = sites_reseau(N, C, brouiller=True)
    n_lignes = len(sites_A)
    inside, ring, fix_val, _, (Xg, Yg, Zg) = geometrie_B(N, n_lignes)  # commensurable
    fix_mask = ring | ~inside
    res = {"campagne": "E58", "protocole": "E58-RESEAU-1.0 (gelé)",
           "n_lignes_imprimees": n_lignes, "bras": {}}
    for bras, sites in (("A", sites_A), ("B", sites_B)):
        psi = imprime_reseau(N, sites)
        lin = gp_linear(N, A, GAMMA, DT)
        for step in range(1, PAS_RELAX + 1):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        snaps = {}
        pos, nl, anom, amb = positions_lignes(psi, inside, Xg, Yg, Zg)
        p6 = psi6(pos)
        snaps[5.0] = {"n_lignes": nl, "psi6": p6,
                      "cristallise": (p6 is not None and p6 >= SEUIL_PSI6),
                      "anom": anom, "amb": amb}
        print(f"bras {bras} t=5 : lignes={nl} ψ6={p6 if p6 is None else round(p6, 3)}",
              flush=True)
        for step in range(PAS_RELAX + 1, SNAP[-1][0] + 1):
            psi = gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
            for pas, t in SNAP:
                if step == pas:
                    pos, nl, anom, amb = positions_lignes(psi, inside, Xg, Yg, Zg)
                    p6 = psi6(pos)
                    snaps[t] = {"n_lignes": nl, "psi6": p6,
                                "cristallise": (p6 is not None
                                                and p6 >= SEUIL_PSI6),
                                "anom": anom, "amb": amb}
                    print(f"bras {bras} t={t:.0f} : lignes={nl} "
                          f"ψ6={p6 if p6 is None else round(p6, 3)} "
                          f"cristal={snaps[t]['cristallise']}", flush=True)
        res["bras"][bras] = {str(k): v for k, v in snaps.items()}
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e58_bras_{bras}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res["bras"][bras], f, ensure_ascii=False)
        print(f"bras {bras} terminé", flush=True)

    # ---- agrégation gelée (règles : e58_protocole.json) ----
    A_ = res["bras"]["A"]
    ag = {"n_lignes_imprimees": n_lignes,
          "P0_entree_cristallisee": bool(A_["5.0"]["cristallise"]),
          "psi6_entree": A_["5.0"]["psi6"],
          "P1_ordre_persiste": bool(A_["45.0"]["cristallise"]
                                    and A_["90.0"]["cristallise"]),
          "psi6_A_t45": A_["45.0"]["psi6"], "psi6_A_t90": A_["90.0"]["psi6"],
          "compte_A": [A_["5.0"]["n_lignes"], A_["45.0"]["n_lignes"],
                       A_["90.0"]["n_lignes"]],
          "B_ordre_forme": bool(res["bras"]["B"]["90.0"]["cristallise"]),
          "psi6_B": {t: res["bras"]["B"][t]["psi6"]
                     for t in ("5.0", "45.0", "90.0")},
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e58_reseau_verdict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
