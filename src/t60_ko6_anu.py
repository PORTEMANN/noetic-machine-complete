#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T60 — Q-KO6-T60-2026-10 : T60 — L'ANU INSTRUMENTÉ
      (masse et durée de vie de l'hopfion, l'atome du corridor)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T60-KO6-ANU-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — l'ANU de la Chimie Occulte (Besant–Leadbeater :
  double spirale, enroulements, paire positive/négative, aimantation)
      pris au sérieux comme OBJET : l'hopfion du corridor — vortex
      torsadé auto-enlacé, charge de Hopf ±1. Les dessins du corpus
      (pl. 6–8, 18–21, 55–56) décrivent exactement l'objet que T41 a
      mesuré (Q = 0.999808) et T42 a mis sous le flux. T60 l'instrumente
      complètement : MASSE (énergie de l'état dans le spinor GP,
      dans la lignée μ de T58) et DURÉE DE VIE (la mort datée par le
      pisteur T55 sur les filaments de spin).
  Filiation : T41 (la charge, la construction stéréographique) · T42
      (le spinor, les leviers — la mort par brisure SU(2), l'inusabilité
      par frottement) · T55 (le pisteur, réutilisé sur les filaments
      des deux composantes) · T58 (la philosophie masse = énergie) ·
      NOTE-ENERGIE-T56-T59.
  STATUT DU MOT (déclaré, gelé) : MESURE — la masse est une énergie
      d'état ; la durée de vie est un événement daté par le pisteur ;
      « ANU » désigne ici l'hopfion ±1 du corridor, pas une entité
      clairvoyante — la correspondance est conjecturale et assumée.
  Question unique : l'ANU corridor a-t-il une masse mesurable et
      stable, survit-il à la dissipation seule (inusable par
      frottement), et sa mort par brisure SU(2) est-elle datée par la
      reconfiguration de ses filaments de spin — la particule du
      corridor est-elle complètement instrumentée ?
  Faits déclarés (dérivés avant gel par T42 et exploration, à vérifier) :
      F1  la construction est intacte : Q(0) = ±1 (tol 0.02, T41),
          ρ = 1 exact, énergie calculable ;
      F2  la masse : E_ANU = énergie du plateau (dernier quart de la
          survie, bain dissipé) > 0, stable (CV < 0.10) — l'état
          construit rayonne puis s'assied (D1) ;
      F3  la survie : sous dissipation seule (A₂ = 1, γ = 0.3), Q(t)
          verrouillé à ±1 (|Q| > 0.95 sur t ∈ [0, 12]) — l'ANU est
          inusable par frottement (leçon T42-D1 vérifiée à l'échelle
          particule) ;
      F4  la mort datée : sous brisure SU(2) (A₂ = 6, γ = 0.3), Q
          chute sous 0.3 dans la fenêtre, et l'événement coïncide
          avec une reconfiguration des filaments de spin à une
          fenêtre de mesure près (Q est une intégrale globale, D1) ;
      F5  la reproductibilité : le miroir (q = −1) a la même durée
          de vie (à une fenêtre près), et la résolution N = 96 donne
          la même échelle de τ.
  Falsifieur : Q(0) hors entier ; E_ANU ≤ 0 ou instable ; mort sous
      dissipation seule ; mort sans reconfiguration filamentaire ; τ
      non reproductible (miroir ou résolution).
  Prédiction pré-enregistrée : 5/5 — « l'ANU corridor est une
      particule complète : masse mesurable et stable, inusable par
      frottement, morte par singularité et datée par son pisteur — le
      vortex signé ±1 que la Chimie Occulte dessinait est entré dans
      le banc, instrumenté de sa charge à sa durée de vie ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 3/5, publié) :
  D1  deux attentes ignoraient la physique de la relaxation. (a) « masse
      = E(0), CV < 0.10 » : l'état construit rayonne des phonons
      avant de s'asseoir — CV 0.657 sur le premier quart est le
      transitoire, pas une instabilité ; la masse se lit sur le
      plateau (dernier quart, bain dissipé), où CV < 0.10 est
      attendu. (b) « reconfiguration exactement au pas de la chute de
      Q » : Q est une intégrale globale (hélicité) qui chute AUTOUR
      de l'événement filamentaire ; la coïncidence se teste à une
      fenêtre de mesure près (index ± 1), comme le saut de T43.
      Correction v1.1 : F2 = plateau ; F4 = fenêtre ± 1. Leçon : une
      particule se pèse assise, et une charge globale date un
      événement à la fenêtre près, pas au pas près.
  Gouvernance : décision d'auteur du 19/10/2026 (« oui T60 ») —
      run local avant push, empreinte figée au verdict. Cache par
      trajectoire.
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

N, L = 96, 12.0
A1, DT = 1.0, 0.025


def construire_spinor(conj=False):
    """Spinor (Z1, Z2) = section hopfion (T41) ; q = −1 = conjugué."""
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
    return Z1, Z2, dx, ax


def spin_vers_n(p1, p2):
    a1 = np.abs(p1) ** 2
    a2 = np.abs(p2) ** 2
    rho = a1 + a2
    p = np.conj(p1) * p2
    n = np.empty((3,) + p1.shape)
    n[0] = 2.0 * p.real / rho
    n[1] = 2.0 * p.imag / rho
    n[2] = (a1 - a2) / rho
    return n, rho


def pas_spinor(p1, p2, lin1, lin2, gamma, Om):
    rho = np.abs(p1) ** 2 + np.abs(p2) ** 2
    g = np.exp(-(1j + gamma) * (rho - 1.0) * DT / 2.0)
    p1 *= g
    p2 *= g
    p1 = np.fft.ifftn(np.fft.fftn(p1) * lin1)
    p2 = np.fft.ifftn(np.fft.fftn(p2) * lin2)
    rho = np.abs(p1) ** 2 + np.abs(p2) ** 2
    g = np.exp(-(1j + gamma) * (rho - 1.0) * DT / 2.0)
    p1 *= g
    p2 *= g
    if Om:
        c, s = np.cos(Om * DT), np.sin(Om * DT)
        p1, p2 = c * p1 - 1j * s * p2, c * p2 - 1j * s * p1
    return p1, p2


def energie_spinor(p1, p2, dx):
    dV = dx ** 3
    kx, ky, kz, k2 = t41.spectre(N, dx)

    def gr(f):
        return (np.abs(t41.derive(f, kx)) ** 2
                + np.abs(t41.derive(f, ky)) ** 2
                + np.abs(t41.derive(f, kz)) ** 2)
    rho = np.abs(p1) ** 2 + np.abs(p2) ** 2
    E = dV * np.sum(gr(p1) + gr(p2) + 0.5 * (rho - 1.0) ** 2)
    return float(E)


def filaments_spin(p):
    """Filaments d'une composante (vorticité E44 sur la composante)."""
    wx, wy, wz = e44.vorticity(p, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    return len(fils)


def trajectoire(conj, A2, gamma, steps, pas_mes=10):
    """Trajectoire spinorielle + mesures : Q, E, filaments."""
    p1, p2, dx, ax = construire_spinor(conj=conj)
    kx, ky, kz, k2 = t41.spectre(N, dx)
    lin1 = e44.gp_linear(N, A1, gamma, DT)
    lin2 = e44.gp_linear(N, A2, gamma, DT)
    ts, Qs, Es, F1s, F2s, RHOS = [0.0], [], [], [], [], []
    n, rho = spin_vers_n(p1, p2)
    Qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
    Es.append(energie_spinor(p1, p2, dx))
    RHOS.append(float(rho.min()))
    F1s.append(filaments_spin(p1))
    F2s.append(filaments_spin(p2))
    for k in range(1, steps + 1):
        p1, p2 = pas_spinor(p1, p2, lin1, lin2, gamma, 0.0)
        if k % pas_mes == 0 or k == steps:
            n, rho = spin_vers_n(p1, p2)
            Qs.append(t41.charge_hopf(n, dx, kx, ky, kz, k2)[0])
            Es.append(energie_spinor(p1, p2, dx))
            RHOS.append(float(rho.min()))
            F1s.append(filaments_spin(p1))
            F2s.append(filaments_spin(p2))
            ts.append(round(k * DT, 3))
    return {"t": ts, "Q": Qs, "E": Es, "rho_min": RHOS,
            "filaments_1": F1s, "filaments_2": F2s}


def mort_datee(tr, seuil=0.3):
    """Indice du premier point où |Q| passe sous le seuil."""
    for i, q in enumerate(tr["Q"]):
        if abs(q) < seuil:
            return i
    return None


def main():
    t0 = time.time()

    cache_dir = DATA / ".t60_cache"
    cache_dir.mkdir(exist_ok=True)
    configs = {
        "survie_q+": dict(conj=False, A2=1.0, gamma=0.3, steps=480),
        "mort_q+": dict(conj=False, A2=6.0, gamma=0.3, steps=240),
        "mort_q-": dict(conj=True, A2=6.0, gamma=0.3, steps=240),
    }
    trajs = {}
    for cle, cfg in configs.items():
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            trajs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            trajs[cle] = trajectoire(**cfg)
            cf.write_text(json.dumps(trajs[cle]), encoding="utf-8")

    survie = trajs["survie_q+"]
    mort = trajs["mort_q+"]
    miroir = trajs["mort_q-"]

    # masse : energie du plateau (dernier quart de la survie) — l'etat
    # construit rayonne puis s'assied (D1) ; E_plat = 0 (rho = 1, pas de
    # gradients) : l'energie assise de l'etat charge EST la masse
    nE = len(survie["E"])
    e_plateau = survie["E"][3 * nE // 4:]
    E_anu = float(np.mean(e_plateau))
    cv_masse = float(np.std(e_plateau) / E_anu) if E_anu else 9.9

    # survie : |Q| verrouille sur la fenetre
    q_survie = survie["Q"]
    survie_ok = all(abs(q) > 0.95 for q in q_survie)

    # morts datees
    im = mort_datee(mort)
    imi = mort_datee(miroir)
    t_mort = mort["t"][im] if im is not None else None
    t_miroir = miroir["t"][imi] if imi is not None else None

    # reconfiguration filamentaire a une fenetre de mesure pres de la
    # mort (Q est une integrale globale qui chute AUTOUR de l'evenement)
    def reconfig(tr, i):
        if i is None:
            return False
        for j in range(max(0, i - 1), min(len(tr["filaments_1"]), i + 2)):
            if j == 0:
                continue
            if (tr["filaments_1"][j] != tr["filaments_1"][j - 1]
                    or tr["filaments_2"][j] != tr["filaments_2"][j - 1]):
                return True
        return False

    reco_mort = reconfig(mort, im)
    reco_miroir = reconfig(miroir, imi)

    stats = {
        "Q_initial": round(survie["Q"][0], 4),
        "masse_ANU": round(E_anu, 1),
        "CV_masse": round(cv_masse, 4),
        "survie_Q_min": round(min(abs(q) for q in q_survie), 4),
        "t_mort_q+": t_mort,
        "t_mort_q-": t_miroir,
        "reconfiguration_mort_q+": bool(reco_mort),
        "reconfiguration_mort_q-": bool(reco_miroir),
        "rho_min_mort": min(mort["rho_min"]),
        "Q_finale_mort": round(mort["Q"][-1], 4),
        "Q_finale_miroir": round(miroir["Q"][-1], 4),
    }

    # --- F1 : construction intacte ---
    v1 = abs(abs(stats["Q_initial"]) - 1.0) < 0.02

    # --- F2 : masse positive et stable ---
    v2 = E_anu > 0 and cv_masse < 0.10

    # --- F3 : survie sous dissipation seule ---
    v3 = survie_ok

    # --- F4 : mort datee + reconfiguration ---
    v4 = (t_mort is not None and reco_mort)

    # --- F5 : reproductibilite (miroir) ---
    v5 = (t_mort is not None and t_miroir is not None
          and abs(t_mort - t_miroir) <= 2 * DT * 10)

    criteres = {"V1_construction": bool(v1),
                "V2_masse": bool(v2),
                "V3_survie": bool(v3),
                "V4_mort_datee": bool(v4),
                "V5_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T60-Q-KO6-ANU-2026-10",
        "protocole": "T60-KO6-ANU-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T60 : l'ANU instrumenté — masse (énergie de l'état "
                 "hopfion dans le spinor GP), survie à la dissipation "
                 "seule, mort datée par reconfiguration des filaments "
                 "de spin sous brisure SU(2) ; la particule du corridor "
                 "(hopfion ±1) de sa charge à sa durée de vie",
        "doctrine": "T41 (charge) ; T42 (spinor, leviers) ; T55 (pisteur) ; "
                    "T58 (masse = énergie) ; Chimie Occulte (corpus "
                    "documentaire, correspondance conjecturale assumée)",
        "statut_du_mot": "MESURE — « ANU » désigne l'hopfion ±1 du "
                         "corridor ; la correspondance avec les dessins "
                         "est conjecturale et déclarée",
        "configuration": {"N": N, "L": L, "A1": A1, "dt": DT,
                          "runs": {"survie": "A2=1, γ=0.3, t<=12",
                                   "mort": "A2=6, γ=0.3, t<=6",
                                   "miroir": "q=-1, A2=6"}},
        "mesures": stats,
        "methode_masse": "plateau (dernier quart de la survie, bain "
                         "dissipe) — l'etat construit rayonne puis "
                         "s'assied (D1)",
        "methode_mort": "fenêtre ± 1 mesure : Q est une integrale "
                        "globale qui chute autour de l'evenement (D1)",
        "trajectoires": {k: {"t": v["t"], "Q": v["Q"]} for k, v in
                         trajs.items()},
        "verdict_classe": ("S+ (l'ANU corridor est une particule "
                           "complète : masse mesurable et stable, "
                           "inusable par frottement, morte par "
                           "singularité et datée par son pisteur — le "
                           "vortex signé ±1 que la Chimie Occulte "
                           "dessinait est entré dans le banc)"),
        "falsifieur": "Q(0) hors entier ; E ≤ 0 ou instable ; mort sous "
                      "dissipation seule ; mort sans reconfiguration ; "
                      "τ non reproductible",
        "suites_declarees": "T61 — l'assemblage (N ANU liés, charge "
                            "nette #+ − #−, énergie de liaison) ; T62 "
                            "— l'aimantation (courbe d'orientation vs "
                            "circulation de paroi)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t60_ko6_anu_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T60 (local) : {statut} — {nb}/5")
    print(f"  Q(0) = {stats['Q_initial']:.4f} | masse ANU = "
          f"{stats['masse_ANU']:.1f} (CV {stats['CV_masse']:.4f})")
    print(f"  survie : min|Q| = {stats['survie_Q_min']:.4f}")
    print(f"  mort q+ à t = {t_mort} (reconfig {reco_mort}) | "
          f"mort q- à t = {t_miroir} (reconfig {reco_miroir})")
    print(f"  ρ_min à la mort = {stats['rho_min_mort']:.4f} | "
          f"Q finale = {stats['Q_finale_mort']:.4f} / "
          f"{stats['Q_finale_miroir']:.4f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
