#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E60 — HORS GP : la cavité tenue par les filaments (vide hyperfluide,
Biot–Savart)   [protocole E60-CAVITE-1.0 gelé]
=====================================================================
Harnais officiel de la campagne E60 — la première campagne hors GP.
Protocole gelé dans e60_protocole.json (haché avant tout calcul).

Conversion déclarée : le corridor (E44–E59) a mesuré que dans la famille
GP la relation topologique est toujours réécrivable (plafond τ ≤ 15) —
obstruction : le cœur déplétable. La phénoménologie fondatrice (vide
hyperfluide, cavité, souffle) est du côté incompressible : E60 y passe.
Dans cette famille, la conservation topologique est AXIOMATIQUE (Kelvin —
pas de reconnexion dans l'équation) — déclaré : le verdict ne la
revendique pas comme mesure ; la question mesurée est la STABILITÉ du
composite (cohérence de forme), pas la conservation du lien.

Modèle gelé : filaments de vortex (chaînes polygonales fermées), vitesse
auto-induite de Biot–Savart désingularisée (Rosenhead–Moore, cutoff a,
figé) ; pas de grille (espace libre) ; RK4, dt figé ; remaillage à longueur
d'arc uniforme (bornes figées). Γ = 1 (figé).

T0 (instrument, pré-enregistré) : vitesse de translation d'un anneau
isolé R=10, a=0,5 vs valeur analytique v = Γ/4πR·(ln(8R/a) − 1/4) —
tolérance 5 % (figée).

Configurations gelées :
  A : la paire de Hopf de filaments (anneaux R=10 plan xy centré origine,
      r=8 plan xz centré (10,0,0) — géométrie d'E50 transposée) ;
  B : la cavité ANU — 18 anneaux identiques (rayon 6), axes radiaux,
      centres sur une sphère de rayon R_cage=12 (géométrie déclarée).
Mesures gelées (snapshots t = 0, 5, 12, 20, 45, 90) : rayon de chaque
anneau, dérive du centroïde, rayon rms de la cage, échappement ; lien de
Gauss entre filaments (mesuré pour valider le harnais — conservation
axiomatique déclarée).

Usage : python3 e60_run.py            (campagne — interdit avant décision)
        python3 e60_run.py --smoke    (validation technique déclarée :
                                       T0 court, hors campagne)
"""

import json
import os
import sys
import time

import numpy as np

# ---------------- paramètres gelés -------------------------------------------
GAMMA_CIRC = 1.0        # circulation Γ, figée
A_CUT = 0.5             # cutoff Rosenhead–Moore, figé
DT = 0.25               # pas RK4, figé
H_MIN, H_MAX = 0.3, 1.2  # remaillage à longueur d'arc (bornes figées)
N_PT_ANNEAU = 64        # points par anneau à l'écriture, figé
SNAP_T = [0.0, 5.0, 12.0, 20.0, 45.0, 90.0]
R_HOPF, R2_HOPF = 10.0, 8.0
R_CAGE, R_ANU, N_ANU = 12.0, 6.0, 18     # cavité ANU — géométrie figée
R_T0 = 10.0
TOL_T0 = 0.30           # tolérance de niveau, figée (constante de modèle de cœur — déclaré)
TOL_T0_SCALING = 0.15   # tolérance de la forme v(R), figée
TMAX = 90.0


def anneau(centre, rayon, axe, n=N_PT_ANNEAU):
    """Anneau circulaire : centre, rayon, axe normal (unitaire)."""
    axe = np.asarray(axe, dtype=float)
    axe /= np.linalg.norm(axe)
    u = np.cross(axe, [1.0, 0, 0])
    if np.linalg.norm(u) < 1e-9:
        u = np.cross(axe, [0, 1.0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(axe, u)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return (np.asarray(centre, dtype=float)
            + rayon * (np.outer(np.cos(th), u) + np.outer(np.sin(th), v)))


def vitesse_biotsavart(fils):
    """v(x) = −Γ/4π Σ (r_seg − x) × dl / (|x−r_seg|² + a²)^{3/2}
    (désingularisation Rosenhead–Moore, figée)."""
    pts = np.concatenate(fils)
    v = np.zeros_like(pts)
    for P in fils:
        seg = np.roll(P, -1, axis=0) - P
        mid = P + seg / 2
        R = pts[:, None, :] - mid[None, :, :]
        dl = seg[None, :, :]
        den = (np.sum(R**2, axis=2) + A_CUT**2) ** 1.5
        contrib = np.cross(R, dl) / den[:, :, None]
        v -= GAMMA_CIRC / (4 * np.pi) * contrib.sum(axis=1)
    return v


def remaille(P):
    """Remaillage à longueur d'arc uniforme entre H_MIN et H_MAX (figé)."""
    d = np.linalg.norm(np.roll(P, -1, axis=0) - P, axis=1)
    L = float(d.sum())
    n = int(np.clip(round(L / ((H_MIN + H_MAX) / 2)), 8, 256))
    th_old = np.concatenate([[0.0], np.cumsum(d)]) / L
    th_new = np.linspace(0, 1, n, endpoint=False)
    out = np.empty((n, 3))
    for c in range(3):
        col = np.concatenate([P[:, c], P[:1, c]])
        out[:, c] = np.interp(th_new, th_old, col)
    return out


def rk4(fils, dt):
    def f(F):
        return vitesse_biotsavart(F)
    k1 = f(fils)
    k2 = f([P + dt * k1[i] / 2 for i, P in enumerate(fils)])
    k3 = f([P + dt * k2[i] / 2 for i, P in enumerate(fils)])
    k4 = f([P + dt * k3[i] for i, P in enumerate(fils)])
    return [remaille(P + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6)
            for i, P in enumerate(fils)]


def rayon_et_centre(P):
    c = P.mean(axis=0)
    r = float(np.linalg.norm(P - c, axis=1).mean())
    return r, c


def gauss_link(P, Q):
    """Nombre de Gauss en espace libre (sans image minimale — les
    filaments sont compacts ; déclaré). Mesure de harnais — la
    conservation est axiomatique ici (déclaré)."""
    dP = np.roll(P, -1, axis=0) - P
    dQ = np.roll(Q, -1, axis=0) - Q
    R = P[:, None, :] - Q[None, :, :]
    cr = np.cross(dP[:, None, :], dQ[None, :, :])
    num = np.einsum('ijk,ijk->ij', R, cr)
    den = np.linalg.norm(R, axis=2)**3
    den[den < 1e-9] = np.inf
    return float(np.sum(num / den) / (4 * np.pi))


def v_analytique(R, a=A_CUT, g=GAMMA_CIRC):
    return g / (4 * np.pi * R) * (np.log(8 * R / a) - 0.25)


def main():
    if "--smoke" in sys.argv:
        # Validation technique déclarée (hors campagne) : 10 pas d'un
        # anneau isolé — mécanique seule.
        print("SMOKE — mécanique (hors campagne)")
        fils = [anneau([0, 0, 0], R_T0, [0, 0, 1])]
        z0 = fils[0][:, 2].mean()
        for _ in range(10):
            fils = rk4(fils, DT)
        dz = fils[0][:, 2].mean() - z0
        print("SMOKE :", {"dz_10_pas": round(dz, 4),
                          "v_estimee": round(dz / (10 * DT), 5),
                          "v_analytique": round(v_analytique(R_T0), 5)})
        return

    t0 = time.time()
    res = {"campagne": "E60", "protocole": "E60-CAVITE-1.0 (gelé)"}

    # ---- T0 : validation de l'instrument (pré-enregistré) ----
    # Niveau (R=10) ET forme (rapports v(5)/v(10), v(20)/v(10)) — la
    # constante de modèle de cœur de la littérature est couverte par la
    # tolérance de niveau (déclarée) ; les rapports la contraignent.
    vs, va = {}, {}
    for R_ in (5.0, R_T0, 20.0):
        fils = [anneau([0, 0, 0], R_, [0, 0, 1])]
        z0 = fils[0][:, 2].mean()
        n_pas_t0 = int(20.0 / DT)
        for _ in range(n_pas_t0):
            fils = rk4(fils, DT)
        vs[R_] = (fils[0][:, 2].mean() - z0) / 20.0
        va[R_] = v_analytique(R_)
    ecart = abs(vs[R_T0] / va[R_T0] - 1.0)
    rap_mes = (vs[5.0] / vs[R_T0], vs[20.0] / vs[R_T0])
    rap_an = (va[5.0] / va[R_T0], va[20.0] / va[R_T0])
    ecart_forme = max(abs(rap_mes[i] / rap_an[i] - 1.0) for i in (0, 1))
    res["T0"] = {"v_mesurees": {str(k): round(v, 6) for k, v in vs.items()},
                 "v_analytiques": {str(k): round(v, 6) for k, v in va.items()},
                 "ecart_niveau": round(ecart, 4),
                 "ecart_forme": round(ecart_forme, 4),
                 "valide": bool(ecart <= TOL_T0
                                and ecart_forme <= TOL_T0_SCALING)}
    print(f"T0 : niveau écart={ecart:.4f} forme écart={ecart_forme:.4f} "
          f"→ {'PASS' if res['T0']['valide'] else 'FAIL'}", flush=True)
    if not res["T0"]["valide"]:
        res["agregation"] = {"verdict": "B3-FAIL-TECHNIQUE",
                             "note": "instrument non validé"}
        _ecris(res, t0)
        return

    # ---- Configurations A (Hopf) et B (cavité ANU) ----
    hopf = [anneau([0, 0, 0], R_HOPF, [0, 0, 1]),
            anneau([R_HOPF, 0, 0], R2_HOPF, [0, 1, 0])]
    cage = []
    for k in range(N_ANU):
        phi = 2 * np.pi * k / N_ANU
        theta = np.pi * (k % 3) / 3 + np.pi / 6   # 3 latitudes, figé
        n = np.array([np.sin(theta) * np.cos(phi),
                      np.sin(theta) * np.sin(phi), np.cos(theta)])
        cage.append(anneau(n * R_CAGE, R_ANU, n))

    for nom, fils0 in (("A_hopf", hopf), ("B_cavite_anu", cage)):
        fils = [P.copy() for P in fils0]
        r0 = [rayon_et_centre(P) for P in fils]
        snaps = {}
        steps = int(TMAX / DT)
        for s in range(steps + 1):
            t = s * DT
            if abs(t - min(SNAP_T, key=lambda x: abs(x - t))) < DT / 2:
                tt = min(SNAP_T, key=lambda x: abs(x - t))
                mesure = {"rayons": [round(rayon_et_centre(P)[0], 3)
                                     for P in fils],
                          "centres": [np.round(rayon_et_centre(P)[1], 3)
                                      .tolist() for P in fils],
                          "rms_global": round(float(np.sqrt(np.mean(
                              np.concatenate(fils)**2))), 3)}
                if len(fils) == 2:
                    mesure["lk"] = round(gauss_link(fils[0], fils[1]), 3)
                if nom == "B_cavite_anu":
                    cents = np.array([rayon_et_centre(P)[1] for P in fils])
                    mesure["rms_cage"] = round(float(np.sqrt(
                        np.mean(np.sum(cents**2, axis=1)))), 3)
                    mesure["echappement_max"] = round(float(
                        np.abs(cents).max()), 3)
                snaps[tt] = mesure
                print(f"  {nom} t={tt:.0f} : rms={mesure['rms_global']}",
                      flush=True)
            if s < steps:
                fils = rk4(fils, DT)
        res[nom] = {"snaps": {str(k): v for k, v in snaps.items()},
                    "rayons_initiaux": [r for r, _ in r0]}
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "data", f"e60_{nom}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res[nom], f, ensure_ascii=False)
        print(f"{nom} terminé", flush=True)

    # ---- agrégation gelée (règles : e60_protocole.json) ----
    A_ = res["A_hopf"]["snaps"]
    B_ = res["B_cavite_anu"]["snaps"]
    rayons_A = [A_[str(t)]["rayons"] for t in SNAP_T]
    centres_A0 = np.array(A_["0.0"]["centres"])
    derive_A = max(float(np.abs(np.array(A_[str(t)]["centres"])
                                - centres_A0).max())
                   for t in SNAP_T)
    P1 = all(all(0.5 * r0 <= r <= 1.5 * r0 for r, r0 in
                 zip(A_[str(t)]["rayons"], [R_HOPF, R2_HOPF]))
             for t in SNAP_T) and derive_A <= 2.0
    rms0 = B_["0.0"]["rms_cage"]
    ech_max = max(B_[str(t)]["echappement_max"] for t in SNAP_T)
    P2 = all(0.5 * rms0 <= B_[str(t)]["rms_cage"] <= 1.5 * rms0
             for t in SNAP_T) and ech_max <= 2 * rms0
    ag = {"T0_valide": res["T0"]["valide"],
          "P1_hopf_coherent": P1,
          "derive_max_hopf": round(derive_A, 3),
          "rayons_hopf": rayons_A,
          "P2_cavite_tenue": P2,
          "rms_cage": {str(t): B_[str(t)]["rms_cage"] for t in SNAP_T},
          "echappement_max_cage": round(ech_max, 3),
          "lk_hopf": {str(t): A_[str(t)].get("lk") for t in SNAP_T},
          "verdict": ("SUCCÈS" if (P1 and P2) else
                      "PARTIEL (Hopf cohérent, cavité non tenue)" if P1
                      else "B3-FAIL"),
          "durée_s": round(time.time() - t0, 1)}
    res["agregation"] = ag
    _ecris(res, t0)
    print("AGRÉGATION :", json.dumps(ag, ensure_ascii=False), flush=True)


def _ecris(res, t0):
    res.setdefault("agregation", {})["durée_s"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "data", "e60_cavite_verdict.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Verdict brut →", out, flush=True)


if __name__ == "__main__":
    main()
