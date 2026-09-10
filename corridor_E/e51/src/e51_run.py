#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E51 — PINNING APPARIÉ : un réseau de puits adapté au lien imprimé le
conserve-t-il sous trempe amortie ?   [protocole E51-PINNING-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E51. Protocole gelé dans
e51_protocole.json (haché avant tout calcul — aveugle préservé).

Filiation déclarée : détecteur E44 byte-identique (e44_core.py,
sha256 604c2232…60ae1ac7) ; construction du lien imprimé d'E50
(reprise à l'identique) ; suivi spatial d'E48/E49/E50 (inchangé).

Classe de mécanisme (déclarée) : ancrage SPATIAL — la seule classe non
testée du corridor (la famille « mur de densité sous GP » est close par
E46→E50 ; la dissipation par E45). Précédent physique : flux pinning des
supraconducteurs de type II — le discret persiste dans le continu quand
il est ancré à une structure déclarée.

Construction gelée :
  Lien de Hopf imprimé : identique à E50 (anneau 1 : plan xy,
  centre (31,5;31,5;31,5), R=10 ; anneau 2 : plan xz,
  centre (41,5;31,5;31,5), r=8 ; δ=1,5 ; relaxation 100 pas à γ=0,3,
  SANS puits — entrée identique à E50).
  Réseau de puits : V_ext(x) = −U0 Σ_w exp(−|x−w|²/2σ²), U0=2, σ=1,5
  (figés) ; puits le long des cœurs des deux anneaux, espacés d'environ
  4 mailles (n1 = round(2πR/4) = 16 sur l'anneau 1, n2 = round(2πr/4)
  = 13 sur l'anneau 2 — comptage figé). Appariement DÉCLARÉ et assumé :
  test d'existence, pas de statistique.
Bras depuis l'état relaxé (t=5) :
  A : γ=0,3, sans puits — témoin (reproduit E50-A : évaporation)
  B : γ=0,3, puits APPARIÉS — le cas supraconducteur
  C : γ=0,3, puits DÉCALÉS d'un demi-pas angulaire sur chaque anneau
      (hors cœur d'environ 2 mailles — figé) — témoin de non-appariement
Snapshots : t=5 (entrée), t=45, t=90. Suivi : identique à E48→E50.

Usage : python3 e51_run.py            (campagne — interdit avant décision)
        python3 e51_run.py --smoke    (validation technique déclarée :
                                       N=32, homothétie, hors campagne)
"""

import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import vorticity, trace_filaments, gauss_link_mi  # filiation

# ---------------- paramètres gelés (filiation E44→E50, sauf mention) --------
N, A, DT = 64, 2.0, 0.05
GAMMA = 0.3
PAS_RELAX = 100
R_ANNEAU1 = 10.0
R_ANNEAU2 = 8.0
DELTA_COEUR = 1.5
U0_PIN = 2.0           # profondeur des puits, figée
SIGMA_PIN = 1.5        # largeur, figée
PAS_PUITS = 4.0        # espacement le long des cœurs, figé
RHO_MIN = 0.5
SNAP_SUITE = [(900, 45.0), (1800, 90.0)]
SEUIL_LK = 0.5
MIN_LEN = 6
MAX_LOOPS = 400
DIST_TRACK = 3.0
MIN_LEN_CAND = 20
AMB_MAX = 4
P0_BORNE = (0.9, 1.1)


def gp_linear(N_, A_, gamma_, dt_):
    k = 2 * np.pi * np.fft.fftfreq(N_)
    k2 = (k[:, None, None]**2 + k[None, :, None]**2
          + k[None, None, :]**2)
    return np.exp(-(1j + gamma_) * A_ * k2 * dt_)


def gp_step(psi, lin, gamma_, dt_, Vext=None):
    """Pas Strang — filiation e44_core.gp_step ; V_ext (puits) ajouté au
    kick de potentiel quand présent (déclaré)."""
    V = np.abs(psi)**2 - 1.0
    if Vext is not None:
        V = V + Vext
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    psi = np.fft.ifftn(np.fft.fftn(psi) * lin)
    psi *= np.exp(-(1j + gamma_) * V * dt_ / 2)
    return psi


def geometrie_lien(N_=N):
    """Anneaux gelés (identique E50) + positions des puits le long des
    cœurs (comptage figé par PAS_PUITS)."""
    C = (N_ - 1) / 2.0
    s = N_ / 64.0
    R1, R2 = R_ANNEAU1 * s, R_ANNEAU2 * s
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    rho1 = np.sqrt((X - C)**2 + (Y - C)**2)
    u1, w1 = rho1 - R1, Z - C
    d1 = np.sqrt(u1**2 + w1**2)
    phi1 = np.arctan2(w1, u1)
    rho2 = np.sqrt((X - (C + R1))**2 + (Z - C)**2)
    u2, w2 = rho2 - R2, Y - C
    d2 = np.sqrt(u2**2 + w2**2)
    phi2 = np.arctan2(w2, u2)
    psi = (np.tanh(d1 / (DELTA_COEUR * s)) * np.tanh(d2 / (DELTA_COEUR * s))
           * np.exp(1j * (phi1 + phi2)))
    n1 = int(round(2 * np.pi * R1 / (PAS_PUITS * s)))
    n2 = int(round(2 * np.pi * R2 / (PAS_PUITS * s)))
    puits = []
    for k in range(n1):
        th = 2 * np.pi * k / n1
        puits.append((C + R1 * np.cos(th), C + R1 * np.sin(th), C))
    for k in range(n2):
        ph = 2 * np.pi * k / n2
        puits.append((C + R1 + R2 * np.cos(ph), C, C + R2 * np.sin(ph)))
    return psi, np.array(puits), (n1, n2)


def V_ext_de(puits, N_=N, demi_pas=False, ns=None):
    """Réseau de puits gaussiens ; demi_pas=True → rotation d'un demi-pas
    angulaire (témoin de non-appariement, figé)."""
    X, Y, Z = np.meshgrid(np.arange(N_), np.arange(N_), np.arange(N_),
                          indexing='ij')
    C = (N_ - 1) / 2.0
    s = N_ / 64.0
    R1, R2 = R_ANNEAU1 * s, R_ANNEAU2 * s
    n1, n2 = ns
    dth = (np.pi / n1) if demi_pas else 0.0
    dph = (np.pi / n2) if demi_pas else 0.0
    pts = []
    for k in range(n1):
        th = 2 * np.pi * k / n1 + dth
        pts.append((C + R1 * np.cos(th), C + R1 * np.sin(th), C))
    for k in range(n2):
        ph = 2 * np.pi * k / n2 + dph
        pts.append((C + R1 + R2 * np.cos(ph), C, C + R2 * np.sin(ph)))
    V = np.zeros((N_,) * 3)
    sig = SIGMA_PIN * s
    for w in pts:
        V -= U0_PIN * np.exp(-((X - w[0])**2 + (Y - w[1])**2
                               + (Z - w[2])**2) / (2 * sig**2))
    return V


def detecte(psi, avec_loops=False):
    """Détecteur E44 (filiation) — identique à E48→E50."""
    wx, wy, wz = vorticity(psi, amp_gate=0.0)
    fils, anom, amb = trace_filaments(wx, wy, wz)
    loops = [f for f in fils if f['closed'] and not np.any(f['disp'])
             and f['len'] >= MIN_LEN]
    loops.sort(key=lambda f: -f['len'])
    if len(loops) > MAX_LOOPS:
        loops = loops[:MAX_LOOPS]
    pairs = []
    for i, j in itertools.combinations(range(len(loops)), 2):
        lk = gauss_link_mi(loops[i]['pts'], loops[j]['pts'], psi.shape[0])
        if abs(lk) >= SEUIL_LK:
            pairs.append((i, j, lk))
    s = {"lie": len(pairs) > 0, "nboucles": len(loops),
         "longueur_totale": int(sum(f['len'] for f in loops)),
         "npaires": len(pairs),
         "paires": [(i, j, round(lk, 3)) for i, j, lk in pairs],
         "anom": anom, "amb": amb,
         "lisible": (anom == 0) and (amb <= AMB_MAX)}
    if avec_loops:
        s["_loops"] = loops
        s["_pairs_brut"] = pairs
    return s


def dist_median_mi(P, Q, L):
    best = np.full(len(P), np.inf)
    for c in range(0, len(Q), 512):
        R = P[:, None, :] - Q[None, c:c + 512, :]
        R = (R + L / 2) % L - L / 2
        best = np.minimum(best, np.linalg.norm(R, axis=2).min(axis=1))
    return float(np.median(best))


def suivi(loops, suivies, L):
    """Identique à E48→E50 (figé)."""
    cands = [f for f in loops if f['len'] >= MIN_LEN_CAND]
    retrouvees = []
    dists = []
    for T in suivies:
        best = None
        for f in cands:
            d = dist_median_mi(f['pts'], T, L)
            if best is None or d < best[0]:
                best = (d, f)
        dists.append(best[0] if best else None)
        retrouvees.append(best[1] if (best and best[0] < DIST_TRACK)
                          else None)
    conservee = False
    lk = None
    if all(r is not None for r in retrouvees):
        lk = gauss_link_mi(retrouvees[0]['pts'], retrouvees[1]['pts'], L)
        conservee = abs(lk) >= SEUIL_LK
    return conservee, lk, dists


def snapshot_suivi(psi, suivies, N_=N):
    s = detecte(psi, avec_loops=True)
    conservee, lk, dists = suivi(s["_loops"], suivies, N_)
    out = {k: v for k, v in s.items() if not k.startswith('_')}
    out["paire_conservee"] = conservee
    out["lk_suivi"] = round(lk, 3) if lk is not None else None
    out["dist_suivi"] = [round(d, 2) if d is not None else None
                         for d in dists]
    return out


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée : N=32 (homothétie), hors campagne.
        print("SMOKE — validation technique (hors campagne, N=32)")
        psi, puits, ns = geometrie_lien(32)
        Vb = V_ext_de(puits, 32, demi_pas=False, ns=ns)
        Vc = V_ext_de(puits, 32, demi_pas=True, ns=ns)
        lin = gp_linear(32, A, GAMMA, DT)
        for _ in range(20):
            psi = gp_step(psi, lin, GAMMA, DT)
        s = detecte(psi, avec_loops=True)
        print("SMOKE :", {"nboucles": s["nboucles"], "npaires": s["npaires"],
                          "paires": s["paires"], "anom": s["anom"],
                          "amb": s["amb"], "n_puits": ns,
                          "Vext_min_apparie": round(float(Vb.min()), 3),
                          "Vext_min_decale": round(float(Vc.min()), 3)})
        return

    t0 = time.time()
    res = {"campagne": "E51", "protocole": "E51-PINNING-1.0 (gelé)"}

    # ---- construction + relaxation (sans puits — identique E50) ----
    psi, puits, ns = geometrie_lien(N)
    lin = gp_linear(N, A, GAMMA, DT)
    for step in range(1, PAS_RELAX + 1):
        psi = gp_step(psi, lin, GAMMA, DT)
    s5 = detecte(psi, avec_loops=True)
    res["entree_relaxee"] = {k: v for k, v in s5.items()
                             if not k.startswith('_')}
    res["n_puits"] = list(ns)
    if not s5["lie"]:
        res["agregation"] = {"P0_filiation_T0": False,
                             "note": "pas de paire après relaxation — "
                                     "B3-FAIL technique"}
        _ecris(res, t0)
        return
    i, j, lk0 = max(s5["_pairs_brut"], key=lambda p: abs(p[2]))
    suivies = [s5["_loops"][i]['pts'].copy(), s5["_loops"][j]['pts'].copy()]
    res["paire_suivie"] = {"lk_entree": round(lk0, 3),
                           "P0_filiation_T0": bool(
                               P0_BORNE[0] <= abs(lk0) <= P0_BORNE[1])}
    print(f"t=5 : paire suivie Lk={lk0:.3f} anom={s5['anom']}", flush=True)

    # ---- trois bras ----
    Vb = V_ext_de(puits, N, demi_pas=False, ns=ns)
    Vc = V_ext_de(puits, N, demi_pas=True, ns=ns)
    for bras, Vext in {"A": None, "B": Vb, "C": Vc}.items():
        psi_b = psi.copy()
        lin_b = gp_linear(N, A, GAMMA, DT)
        snaps = {5.0: snapshot_suivi(psi_b, suivies, N)}
        for step in range(PAS_RELAX + 1, SNAP_SUITE[-1][0] + 1):
            psi_b = gp_step(psi_b, lin_b, GAMMA, DT, Vext=Vext)
            for pas, t in SNAP_SUITE:
                if step == pas:
                    snaps[t] = snapshot_suivi(psi_b, suivies, N)
                    print(f"  bras {bras} t={t:.0f} : conservée="
                          f"{snaps[t]['paire_conservee']} boucles="
                          f"{snaps[t]['nboucles']} anom={snaps[t]['anom']}",
                          flush=True)
        res[f"bras_{bras}"] = {str(k): v for k, v in snaps.items()}
        print(f"bras {bras} terminé", flush=True)

    # ---- agrégation gelée (règles : e51_protocole.json) ----
    def pers(b):
        return any(res[f"bras_{b}"][str(t)]["paire_conservee"]
                   for t in (45.0, 90.0))

    def lisible(b):
        return all(res[f"bras_{b}"][str(t)]["lisible"]
                   for t in ("5.0", "45.0", "90.0"))

    ag = {"P0_filiation_T0": res["paire_suivie"]["P0_filiation_T0"],
          "lk_entree": res["paire_suivie"]["lk_entree"],
          "P0b_temoin_A_zero": not pers("A"),
          "persistance_A": pers("A"), "persistance_B": pers("B"),
          "persistance_C": pers("C"),
          "P1_B_conserve": pers("B"),
          "P2_C_ne_conserve_pas": not pers("C"),
          "lisibilite_A": lisible("A"), "lisibilite_B": lisible("B"),
          "lisibilite_C": lisible("C"),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e51_pinning_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
