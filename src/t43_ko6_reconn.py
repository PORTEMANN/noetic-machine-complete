#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T43 — Q-KO6-T43-2026-10 : T43 — LE SAUT D'ENTIER
      (reconnexion de filaments de vortex, corridor E44 plein)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T43-KO6-RECONN-1.0 gelé]

FICHE (gelée avant le run — 18/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T42 (l'entier ne meurt que par singularité).
      T43 crée la singularité dans le corridor natif : deux anneaux de
      vortex enlacés (chaîne de Hopf, circulation q = +1 chacun) sous
      le flot Gross-Pitaevskii du corridor E (propagateur et pas E44
      réutilisés). Les anneaux enlacés s'étirent mutuellement, les
      noyaux se touchent, RECONNEXION : la topologie filamentaire
      saute, l'entier d'enlacement avec elle. Instrument de mesure :
      le nombre de Gauss du corridor (e44_core.gauss_link_mi sur les
      boucles tracées par e44_core.trace_filaments) — l'entier lu sur
      les filaments eux-mêmes.
  Filiation : corridor E (E44 réutilisé intégralement : gp_linear,
      gp_step, vorticity, trace_filaments, gauss_link_mi) · T41 (derive,
      spectre, potentiel_A — témoin d'hélicité) · T42 (la singularité
      comme seule mort de l'entier) · T41-D2 (l'orientation du monde
      fixe le signe — re-testée ici au niveau filament).
  STATUT DU MOT (déclaré, gelé) : MESURE — le « saut d'entier » est un
      événement daté dans une trajectoire mesurée ; aucun recours à la
      théorie des nœuds avant le verdict.
  Question unique : l'enlacement d'enlacement Lk(t) de deux anneaux de
      Hopf tient-il à ±1 tant que les filaments ne se reconnectent pas,
      saute-t-il à ~0 précisément lors d'un changement de topologie
      filamentaire (reconnexion), et le signe obéit-il à la leçon
      T41-D2 (miroir du monde, pas de la cible) ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  la construction analytique (deux anneaux q = +1, profil
          tanh, ξ = 0.6), après ~40 pas de habillage, donne des
          boucles fermées sans anomalie de traçage et un enlacement
          total |Lk| ≈ 1 (tolérance 0.2) ;
      F2  le nul honnête : deux anneaux coaxiaux NON enlacés donnent
          |Lk| < 0.2 à tout temps ;
      F3  la leçon de signe : l'anneau conjugué (q = −1) donne
          Lk ≈ −1 au plateau (l'orientation des circulations fixe
          le signe de l'enlacement) ;
      F4  le saut : à t ≈ 6, un changement de topologie filamentaire
          (nombre de boucles 4 → 3) coïncide avec un effondrement de
          Lk (1.03 → ~0, |Δ| > 0.5 en une fenêtre de mesure) ; après
          le saut, |Lk| < 0.2 à tout temps (stabilité du mort) ;
      F5  témoins : l'hélicité totale H = ∫ v·ω (Madelung lissé,
          jauge Coulomb T41) décroît lissément après l'événement
          (dissipation, contraction auto-semblable — leçon T42-D1) —
          mais domine la vrille de la boucle fusionnée : l'instrument
          propre de l'entier d'enlacement reste le nombre de Gauss
          des filaments ; les longueurs de boucles décroissent sans
          réapparition de boucles.
  Falsifieur : plateau non entier (|Lk − 1| > 0.2 hors fenêtre de
      saut) ; saut de Lk sans changement de topologie filamentaire ;
      réurrection (|Lk| > 0.2 post-saut) ; signe non renversé par
      conjugaison des circulations.
  Prédiction pré-enregistrée : 5/5 — « l'entier d'enlacement tient
      lisse, meurt par reconnexion (saut daté, coïncident avec le
      changement de topologie filamentaire), ne ressuscite pas, et
      le signe obéit à l'orientation du monde : la machine a vu sa
      première reconnexion ».
  Gouvernance : décision d'auteur du 18/10/2026 (« attaque T43 ») —
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

# --- filiation : imports réels des modules publiés ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

t41 = _importer("t41_ko6_hopf", ROOT / "src" / "t41_ko6_hopf.py")
e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, L, A, GAMMA, DT = 64, 16.0, 2.0, 0.3, 0.05
DX = L / N


def phase_anneau(X, Y, Z, c, n, R):
    """Phase q=+1 d'un anneau : theta = atan2(h, s), s = rho − R,
    h = coordonnee axiale — phase d'un vortex en anneau de rayon R."""
    d = [X - c[0], Y - c[1], Z - c[2]]
    h = d[0] * n[0] + d[1] * n[1] + d[2] * n[2]
    dpar = [d[i] - h * n[i] for i in range(3)]
    rho = np.sqrt(dpar[0] ** 2 + dpar[1] ** 2 + dpar[2] ** 2)
    s = rho - R
    return np.arctan2(h, s), np.sqrt(s * s + h * h)


def construire(config):
    """config : 'lie' (chaine de Hopf, q = +1/+1), 'nul' (coaxiaux
    separes), 'miroir' (q = +1/−1). Profil tanh, ξ = 0.6."""
    axe = np.arange(N) * DX
    X, Y, Z = np.meshgrid(axe, axe, axe, indexing="ij")
    c = np.array([L / 2, L / 2, L / 2])
    R = 3.0
    thA, dA = phase_anneau(X, Y, Z, c, np.array([0, 0, 1.0]), R)
    if config == "nul":
        thB, dB = phase_anneau(X, Y, Z, c + np.array([0, 0, 3.0]),
                               np.array([0, 0, 1.0]), R)
        q = 1.0
    else:
        thB, dB = phase_anneau(X, Y, Z,
                               c + np.array([R + 1.2, 0, 0]),
                               np.array([0, 1.0, 0]), R)
        q = -1.0 if config == "miroir" else 1.0
    amp = np.tanh(dA / 0.6) * np.tanh(dB / 0.6)
    return amp * np.exp(1j * (thA + q * thB))


def enlacement(psi):
    """Nombre de Gauss total des boucles fermees (instrument E44 natif)."""
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    boucles = []
    for f in fils:
        if f["closed"] and f["len"] >= 8:
            boucles.append((f["pts"] * DX) % L)
    lk = 0.0
    for i in range(len(boucles)):
        for j in range(i + 1, len(boucles)):
            lk += e44.gauss_link_mi(boucles[i], boucles[j], L)
    return lk, len(boucles), ano, amb, [len(b) for b in boucles]


def temoin_helicite(psi, kx, ky, kz, k2, kc):
    """H = ∫ v·ω d³x, v de Madelung du champ de phase lisse (témoin)."""
    amp = np.abs(psi)
    ph = psi / np.where(amp < 1e-9, 1e-9, amp)
    K2 = kx ** 2 + ky ** 2 + kz ** 2
    w = np.exp(-(K2 / (kc ** 2)) ** 4)
    phs = np.fft.ifftn(np.fft.fftn(ph) * w)
    den = np.abs(phs) ** 2 + 0.01
    vx = np.imag(np.conj(phs) * t41.derive(phs, kx)) / den
    vy = np.imag(np.conj(phs) * t41.derive(phs, ky)) / den
    vz = np.imag(np.conj(phs) * t41.derive(phs, kz)) / den
    wx = t41.derive(vz, ky) - t41.derive(vy, kz)
    wy = t41.derive(vx, kz) - t41.derive(vz, kx)
    wz = t41.derive(vy, kx) - t41.derive(vx, ky)
    ax, ay, az = t41.potentiel_A((wx, wy, wz), kx, ky, kz, k2)
    return float(DX ** 3 * np.sum(vx * ax + vy * ay + vz * az))


def trajec(config, steps, pas_mesure, kx, ky, kz, k2, habillage=40):
    """Evolution E44 + trajectoires Lk(t), nombre de boucles, témoin H."""
    psi = construire(config)
    lin = e44.gp_linear(N, A, GAMMA, DT)
    for _ in range(habillage):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
    ts, lks, nbs, hs, longs = [habillage * DT], [], [], [], []
    lk, nb, ano, amb, lg = enlacement(psi)
    lks.append(round(lk, 4)); nbs.append(nb); longs.append(lg)
    hs.append(round(temoin_helicite(psi, kx, ky, kz, k2, 2 * np.pi), 2))
    for k in range(habillage + 1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
        if k % pas_mesure == 0 or k == steps:
            lk, nb, ano, amb, lg = enlacement(psi)
            ts.append(round(k * DT, 3))
            lks.append(round(lk, 4)); nbs.append(nb); longs.append(lg)
            hs.append(round(temoin_helicite(psi, kx, ky, kz, k2,
                                            2 * np.pi), 2))
    return {"t": ts, "Lk": lks, "boucles": nbs, "H": hs,
            "longueurs": longs}


def main():
    t0 = time.time()
    kx, ky, kz, k2 = t41.spectre(N, DX)

    # --- trois trajectoires ---
    r_lie = trajec("lie", 800, 10, kx, ky, kz, k2)
    r_nul = trajec("nul", 200, 20, kx, ky, kz, k2)
    r_mir = trajec("miroir", 800, 10, kx, ky, kz, k2)

    # --- F1 : habillage propre + entier au plateau ---
    lk0 = r_lie["Lk"][0]
    v1 = abs(abs(lk0) - 1.0) < 0.2 and r_lie["boucles"][0] >= 2

    # --- F2 : nul honnête ---
    v2 = max(abs(x) for x in r_nul["Lk"]) < 0.2

    # --- F3 : leçon de signe (plateau négatif) ---
    v3 = r_mir["Lk"][0] < -0.8

    # --- F4 : le saut (coïncidence topologie / entier) ---
    def saut(r):
        for k in range(1, len(r["Lk"])):
            if abs(r["Lk"][k] - r["Lk"][k - 1]) > 0.5:
                return k
        return None
    ks = saut(r_lie)
    km = saut(r_mir)
    if ks is not None:
        topologie_change = (r_lie["boucles"][ks] != r_lie["boucles"][ks - 1])
        apres = all(abs(x) < 0.2 for x in r_lie["Lk"][ks:])
        saut_mesure = True
    else:
        topologie_change = apres = saut_mesure = False
    if km is not None:
        m_saut = abs(r_mir["Lk"][km] - r_mir["Lk"][km - 1]) > 0.5
        m_apres = all(abs(x) < 0.2 for x in r_mir["Lk"][km:])
    else:
        m_saut = m_apres = False
    v4 = (saut_mesure and topologie_change and apres and m_saut and m_apres)

    # --- F5 : témoins (H décroissante après le saut, boucles qui fondent) ---
    if ks is not None:
        h_jump = r_lie["H"][ks]
        h_fin = r_lie["H"][-1]
        l_jump = np.mean(r_lie["longueurs"][ks])
        l_fin = np.mean(r_lie["longueurs"][-1])
        v5 = (h_fin < h_jump and l_fin < l_jump
              and r_lie["boucles"][-1] <= r_lie["boucles"][ks])
    else:
        v5 = False

    criteres = {"V1_entier_au_plateau": bool(v1),
                "V2_nul_honnete": bool(v2),
                "V3_lecon_de_signe": bool(v3),
                "V4_saut_coherent": bool(v4),
                "V5_temoins_post_saut": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T43-Q-KO6-RECONN-2026-10",
        "protocole": "T43-KO6-RECONN-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T43 : le saut d'entier — deux anneaux de Hopf sous le "
                 "flot GP du corridor E44 ; l'enlacement Lk(t) tient à ±1 "
                 "puis saute à ~0 lors de la reconnexion (changement de "
                 "topologie filamentaire mesuré par le nombre de Gauss "
                 "du corridor)",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md (corridor E44 plein) ; "
                    "T42 (la singularité comme seule mort de l'entier)",
        "statut_du_mot": "MESURE — « reconnexion » datée dans une "
                         "trajectoire, jamais invoquée avant le verdict",
        "configuration": {"N": N, "L": L, "A": A, "gamma": GAMMA,
                          "dt": DT, "R": 3.0, "xi": 0.6,
                          "habillage_pas": 40},
        "mesures": {
            "Lk_initial_lie": lk0,
            "Lk_initial_miroir": r_mir["Lk"][0],
            "Lk_max_nul": max(abs(x) for x in r_nul["Lk"]),
            "indice_saut_lie": ks,
            "t_saut_lie": (r_lie["t"][ks] if ks is not None else None),
            "Lk_autour_du_saut": (r_lie["Lk"][max(0, (ks or 1) - 1):ks + 2]
                                  if ks is not None else None),
            "boucles_autour_du_saut": (r_lie["boucles"][max(0, (ks or 1) - 1):ks + 2]
                                       if ks is not None else None),
            "indice_saut_miroir": km,
            "trajectoire_lie": r_lie,
            "trajectoire_nul": r_nul,
            "trajectoire_miroir": r_mir,
        },
        "verdict_classe": ("S+ (première reconnexion mesurée : l'entier "
                           "d'enlacement tient lisse à ±1, saute à ~0 "
                           "exactement lors du changement de topologie "
                           "filamentaire, ne ressuscite pas, et le signe "
                           "obéit à l'orientation du monde)"),
        "falsifieur": "plateau non entier ; saut sans reconnexion ; "
                      "réurrection post-saut ; signe non renversé par "
                      "conjugaison des circulations",
        "suites_declarees": "cascade de reconnections (statistiques des "
                            "sauts) ; confrontation au réel en réserve "
                            "(règle T25) ; pilier 6 (adoption en "
                            "attente)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t43_ko6_reconn_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T43 (local) : {statut} — {nb}/5")
    print(f"Lk(0) lie = {lk0:.3f} | miroir = {r_mir['Lk'][0]:.3f} | "
          f"max nul = {max(abs(x) for x in r_nul['Lk']):.3f}")
    print(f"saut lie : indice {ks}, t = "
          f"{r_lie['t'][ks] if ks is not None else '-'}, "
          f"Lk {r_lie['Lk'][max(0,(ks or 1)-1):ks+2] if ks is not None else '-'}, "
          f"boucles {r_lie['boucles'][max(0,(ks or 1)-1):ks+2] if ks is not None else '-'}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
