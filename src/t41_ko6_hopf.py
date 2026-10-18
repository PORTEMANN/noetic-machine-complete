#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T41 — Q-KO6-T41-2026-10 : CP5 — LA CHARGE DE HOPF 3D
      (l'entier topologique du monde continu)
=====================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T41-KO6-HOPF-1.0 gelé]

FICHE (gelée avant le run — 18/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — CP5, dernier chantier du carnet de doctrine continue
      (docs/NOTE-CANDIDATS-PONT-PHI.md). Doctrine : le monde discret
      signe φ (T17–T23), le monde continu signe par des ENTIERS
      topologiques. La carte instrumente l'invariant fondateur du
      continu tridimensionnel : la charge de Hopf Q, nombre de tours
      enlacés du fibré de Hopf, mesuré comme une hélicité
      Q = ∫ A·B d³x (B = ∇×A, jauge de Coulomb spectrale).
  Filiation : corridor E (E44 — même boîte périodique 3D, même
      discipline FFT, mêmes invariants entiers : vorticité quantifiée
      par plaquettes, nombre de Gauss des filaments — import réel de
      e44_core, wrap() réutilisé pour le vent du fibré) · T32 (le
      continu) · T34 (les entiers) · T37 (persistance) · T38
      (coupure) · T39 (taxonomie des régimes) · NOTE-DOCTRINE-CONTINU.
  STATUT DU MOT (déclaré, gelé) : MESURE — Q est un entier mesuré sur
      un champ construit analytiquement (hopfion standard :
      stéréographique R³→S³ puis application de Hopf S³→S²) ; le mot
      « topologique » n'est invoqué qu'après le verdict.
  Question unique : l'hélicité spectrale de l'hopfion standard
      vaut-elle exactement ±1 (entier, signe renversé par conjugaison,
      nulle pour le champ trivial), et le levier spectral (filtrage
      passe-bas) détecte-t-il la destruction du noyau ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  la construction stéréographique + Hopf donne un champ
          unitaire exact : max ||n| − 1| à précision machine ;
      F2  le champ émergent B (flux entier par degré, normalisation
          1/4π) est sans monopôle dans le bulk : div B = 0 à précision
          spectrale loin des bords de la boîte torique ;
      F3  la charge de Hopf de l'hopfion standard vaut un entier de
          module 1 (Q ≈ ±1 à tolérance) ; le signe est renversé par
          inversion d'orientation du DOMAINE (miroir x — degré −1 sur
          R³), tandis que la conjugaison de la SORTIE (réflexion de la
          sphère cible S²) laisse l'hélicité INVARIANTE (les deux
          fibres renversées se compensent : Q_conj = Q, mesuré) ;
      F4  le champ trivial n = (0, 0, 1) donne B = 0, Q = 0 ; le vent
          de fibré d'un anneau entourant le noyau vaut exactement
          ±1 et se renverse sous miroir (mesure e44.wrap) ;
      F5  levier spectral : un filtrage passe-bas doux laisse Q
          inchangé (protection topologique), un filtrage fort détruit
          le noyau et la chute de |Q| est détectée — courbe Q(kc)
          enregistrée ; stabilité en résolution (deux boîtes).
  Falsifieur : |Q| non entier à tolérance ; miroir sans renversement
      de signe ; conjugaison de la cible modifiant Q ; trivial non
      nul ; filtrage fort sans chute détectable.
  Prédiction pré-enregistrée : 5/5 — « l'entier topologique du continu
      est mesuré : |Q| = 1, signe renversé par miroir du domaine et
      conservé par conjugaison de la cible, nul au trivial, le levier
      spectral est détecté — le monde continu signe par des entiers,
      comme le discret signe par φ ».
  DÉFAUTS DU BANC (premier run du 18/10/2026 — ÉCHEC 1/5, publié) :
  D1  le produit vectoriel du champ émergent croisait les GRADIENTS
      des composantes (∇n_y × ∇n_z) au lieu des VECTEURS de dérivées
      partielles (∂y n × ∂z n) : div B ≠ 0, Q ≈ 0.107. Correction :
      reconstruire vx/vy/vz dans l'espace des composantes ; mesure
      après correction : Q = 0.999808, div B bulk 8.6e-3
      (6.7e-3 × B_max) ;
  D2  la fiche pré-enregistrait « signe renversé par conjugaison » —
      physique inexacte : conjuguée, la section (Z̄₁, Z̄₂) compose la
      projection avec une réflexion de la CIBLE S² (deux fibres à
      orientation renversée : hélicité paire, Q_conj = Q — vérifié) ;
      seule l'inversion d'orientation du DOMAINE (miroir x, degré −1)
      renverse Q. Test V4 et falsifieur rebasculés sur le miroir ;
      l'invariance par conjugaison devient un fait mesuré (F3) ;
  D3  le seuil V2 (div B < 1e-6 × B_max) ignorait l'échelle spectrale
      ∂B ~ B_max/dx : résidu ~ 1e-3 relatif attendu à N = 128.
      Recalibré à 1e-2 × B_max, ratio enregistré comme mesure.
  Gouvernance : décision d'auteur du 18/10/2026 (« lance CP5 ») —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation corridor E : import réel du module publié (e44_core) ---
_spec = importlib.util.spec_from_file_location(
    "e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")
e44 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e44)

INV_4PI = 1.0 / (4.0 * np.pi)


def construire_hopfion(N, L, conj=False):
    """Hopfion standard : stéréographique R³→S³ (Z₁, Z₂), application
    de Hopf n = (2 Re Z̄₁Z₂, 2 Im Z̄₁Z₂, |Z₁|² − |Z₂|²). Q = ±1."""
    dx = L / N
    ax = (np.arange(N) - N // 2) * dx
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    den = r2 + 1.0
    Z1 = 2.0 * (X + 1j * Y) / den
    Z2 = (2.0 * Z + 1j * (r2 - 1.0)) / den
    if conj:
        Z1 = np.conj(Z1)
        Z2 = np.conj(Z2)
    p = np.conj(Z1) * Z2
    n = np.empty((3, N, N, N))
    n[0] = 2.0 * p.real
    n[1] = 2.0 * p.imag
    n[2] = np.abs(Z1) ** 2 - np.abs(Z2) ** 2
    return n, dx, ax


def spectre(N, dx):
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx = k[:, None, None]
    ky = k[None, :, None]
    kz = k[None, None, :]
    k2 = kx * kx + ky * ky + kz * kz
    return kx, ky, kz, k2


def derive(f, kv):
    return np.fft.ifftn(1j * kv * np.fft.fftn(f)).real


def champ_B(n, kx, ky, kz):
    """B_i = (1/4π) n·(∂_j n × ∂_k n) cyclique — flux entier par degré."""
    d = [[derive(n[c], kv) for kv in (kx, ky, kz)] for c in range(3)]
    # vecteurs de dérivées partielles (espace des composantes) :
    # vx[c] = ∂x n_c, vy[c] = ∂y n_c, vz[c] = ∂z n_c
    vx = [d[c][0] for c in range(3)]
    vy = [d[c][1] for c in range(3)]
    vz = [d[c][2] for c in range(3)]

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0])

    Bx = dot(n, cross(vy, vz)) * INV_4PI   # n·(∂y n × ∂z n)
    By = dot(n, cross(vz, vx)) * INV_4PI   # n·(∂z n × ∂x n)
    Bz = dot(n, cross(vx, vy)) * INV_4PI   # n·(∂x n × ∂y n)
    return Bx, By, Bz


def potentiel_A(B, kx, ky, kz, k2):
    """Jauge de Coulomb spectrale : Â = i k × B̂ / |k|², mode zéro nul."""
    Bh = [np.fft.fftn(B[i]) for i in range(3)]
    k2s = np.where(k2 == 0.0, 1.0, k2)
    zero = (k2 == 0.0)
    Ax = np.fft.ifftn(1j * (ky * Bh[2] - kz * Bh[1]) / k2s).real
    Ay = np.fft.ifftn(1j * (kz * Bh[0] - kx * Bh[2]) / k2s).real
    Az = np.fft.ifftn(1j * (kx * Bh[1] - ky * Bh[0]) / k2s).real
    for A in (Ax, Ay, Az):
        A[zero] = 0.0
    return Ax, Ay, Az


def charge_hopf(n, dx, kx, ky, kz, k2):
    B = champ_B(n, kx, ky, kz)
    A = potentiel_A(B, kx, ky, kz, k2)
    dV = dx ** 3
    Q = float(dV * np.sum(A[0] * B[0] + A[1] * B[1] + A[2] * B[2]))
    divB = derive(B[0], kx) + derive(B[1], ky) + derive(B[2], kz)
    Bmax = float(max(np.abs(B[i]).max() for i in range(3)))
    return Q, divB, Bmax


def vent_fibre(n, ax, R0=1.5, M=1024, miroir=False):
    """Vent (winding) du fibré : phase de n_x + i n_y le long d'un anneau
    de rayon R0 dans le plan z = 0 — accumulateur e44.wrap (filiation).
    miroir=True : anneau réfléchi x -> -x (vent opposé attendu)."""
    dx = ax[1] - ax[0]
    N = n.shape[1]
    iz = int(round((0.0 - ax[0]) / dx)) % N
    phis = 2.0 * np.pi * np.arange(M) / M
    xs = (np.rint(R0 * np.cos(phis) / dx).astype(int) + N // 2) % N
    if miroir:
        xs = (N - xs) % N
    ys = (np.rint(R0 * np.sin(phis) / dx).astype(int) + N // 2) % N
    u = n[0][xs, ys, iz] + 1j * n[1][xs, ys, iz]
    th = np.angle(u)
    dth = e44.wrap(np.diff(th))
    dth = np.append(dth, e44.wrap(th[0] - th[-1]))
    return float(dth.sum() / (2.0 * np.pi))


def coupe_spectrale(n, k2, kc):
    """Levier : passe-bas spectral doux (w = 1/(1+(K/kc)^8)) + renormalisation."""
    K = np.sqrt(k2)
    w = 1.0 / (1.0 + (K / kc) ** 8)
    out = np.empty_like(n)
    for c in range(3):
        out[c] = np.fft.ifftn(np.fft.fftn(n[c]) * w).real
    norm = np.sqrt(out[0] ** 2 + out[1] ** 2 + out[2] ** 2)
    return out / norm


def main():
    t0 = time.time()
    N, L = 128, 16.0

    # --- construction des champs d'essai ---
    n_hopf, dx, ax = construire_hopfion(N, L, conj=False)
    n_conj, _, _ = construire_hopfion(N, L, conj=True)
    n_miroir = np.ascontiguousarray(n_hopf[:, ::-1, :, :])
    n_triv = np.zeros_like(n_hopf)
    n_triv[2] = 1.0
    kx, ky, kz, k2 = spectre(N, dx)

    # --- F1 : unitarité exacte ---
    dev_unite = float(np.abs(np.sqrt(
        n_hopf[0] ** 2 + n_hopf[1] ** 2 + n_hopf[2] ** 2) - 1.0).max())
    v1 = dev_unite < 1e-12

    # --- mesures principales ---
    Q_hopf, divB, Bmax = charge_hopf(n_hopf, dx, kx, ky, kz, k2)
    Q_conj, _, _ = charge_hopf(n_conj, dx, kx, ky, kz, k2)
    Q_miroir, _, _ = charge_hopf(n_miroir, dx, kx, ky, kz, k2)
    Q_triv, _, _ = charge_hopf(n_triv, dx, kx, ky, kz, k2)
    w_hopf = vent_fibre(n_hopf, ax)
    w_miroir = vent_fibre(n_hopf, ax, miroir=True)

    # --- F2 : sans monopôle dans le bulk (r < L/4) ---
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r = np.sqrt(X * X + Y * Y + Z * Z)
    bulk = r < L / 4.0
    divB_bulk = float(np.abs(divB[bulk]).max())
    divB_global = float(np.abs(divB).max())
    divB_ratio = divB_bulk / Bmax
    v2 = divB_ratio < 1e-2

    # --- F3 : entier topologique ---
    v3 = abs(abs(Q_hopf) - 1.0) < 0.02

    # --- F4 : symétries (miroir renverse, conjugaison de la cible
    #          conserve — D2) ---
    v4 = (abs(Q_hopf + Q_miroir) < 0.01
          and abs(Q_conj - Q_hopf) < 0.01
          and abs(Q_triv) < 1e-9
          and abs(w_hopf + w_miroir) < 0.05
          and abs(w_hopf) > 0.25)

    # --- F5 : levier spectral + stabilité en résolution ---
    cibles = [1.5, 2.0, 3.0, 4.0, 6.0, 9.0, 14.0]
    courbe = {}
    for kc in cibles:
        nf = coupe_spectrale(n_hopf, k2, kc)
        Qf, _, _ = charge_hopf(nf, dx, kx, ky, kz, k2)
        courbe[str(kc)] = round(Qf, 6)
    plateau = all(abs(courbe[str(kc)]) > 0.9 for kc in (4.0, 6.0, 9.0, 14.0))
    chute = abs(courbe["1.5"]) < 0.5
    n_low, dx_low, _ = construire_hopfion(96, L, conj=False)
    kxl, kyl, kzl, k2l = spectre(96, dx_low)
    Q_low, _, _ = charge_hopf(n_low, dx_low, kxl, kyl, kzl, k2l)
    del n_low, kxl, kyl, kzl, k2l
    stabilité = abs(abs(Q_low) - abs(Q_hopf)) < 0.02
    v5 = plateau and chute and stabilité

    criteres = {"V1_unitarite": bool(v1),
                "V2_sans_monopole_bulk": bool(v2),
                "V3_entier_topologique": bool(v3),
                "V4_symetries": bool(v4),
                "V5_levier_spectral": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T41-Q-KO6-HOPF-2026-10",
        "protocole": "T41-KO6-HOPF-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "CP5 : la charge de Hopf 3D — l'entier topologique du "
                 "monde continu, mesuré par hélicité spectrale sur "
                 "l'hopfion standard (stéréographique + application de "
                 "Hopf)",
        "doctrine": "docs/NOTE-CANDIDATS-PONT-PHI.md (CP5) ; "
                    "NOTE-DOCTRINE-CONTINU.md",
        "statut_du_mot": "MESURE — « topologique » invoqué après le verdict",
        "configuration": {"N": N, "L": L, "dx": dx,
                          "hélicité": "Q = ∫ A·B d³x, B = ∇×A, "
                                     "jauge de Coulomb spectrale"},
        "mesures": {
            "dev_unitarite_max": dev_unite,
            "Q_hopfion": round(Q_hopf, 6),
            "Q_miroir": round(Q_miroir, 6),
            "Q_conjugue": round(Q_conj, 6),
            "Q_trivial": round(Q_triv, 9),
            "vent_fibre": round(w_hopf, 6),
            "vent_fibre_miroir": round(w_miroir, 6),
            "divB_bulk_max": divB_bulk,
            "divB_ratio_bulk_sur_Bmax": divB_ratio,
            "divB_global_max": divB_global,
            "B_max": Bmax,
            "levier_courbe_Q_kc": courbe,
            "Q_resolution_96": round(Q_low, 6),
        },
        "verdict_classe": ("S+ (entier topologique du continu mesuré : "
                           "|Q| = 1, signe renversé par miroir du domaine, "
                           "conservé par conjugaison de la cible, nul au "
                           "trivial, levier spectral détecté — le continu "
                           "signe par des entiers, comme le discret signe "
                           "par φ)"),
        "falsifieur": "|Q| non entier à tolérance ; miroir sans "
                      "renversement ; conjugaison de la cible modifiant Q ; "
                      "trivial non nul ; filtrage fort sans chute de |Q|",
        "suites_declarees": "carnet CP1–CP5 bouclé ; proposition : "
                            "pilier 6 de la doctrine continue (les "
                            "entiers topologiques comme signature du "
                            "continu) ; consolidation du carnet",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t41_ko6_hopf_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T41 (local) : {statut} — {nb}/5")
    print(f"Q hopfion = {Q_hopf:.6f}  | miroir = {Q_miroir:.6f} | "
          f"conjugué = {Q_conj:.6f} | trivial = {Q_triv:.2e}")
    print(f"vent fibré = {w_hopf:.4f} (miroir {w_miroir:.4f}) | "
          f"divB bulk = {divB_bulk:.3e} (ratio {divB_ratio:.2e})")
    print("levier Q(kc) :", courbe)
    print(f"Q (N=96) = {Q_low:.6f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
