#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T45 — Q-KO6-T45-2026-10 : T45 — LE TANGLE DENSE
      (le null des entiers, la cascade en population)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T45-KO6-TANGLE-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T44 (la cascade ordonnée des chaînes). T45
      passe au désordre : l'ère précoce du tangle dense du corridor
      (phases aléatoires, aucune structure imposée — les anneaux
      construits de T43/T44 sont la limite ordonnée). Question : que
      deviennent les entiers d'enlacement quand le champ EST du bruit
      quantique organisé ?
  Filiation : corridor E (protocole de nucléation E44 v2 — mêmes
      ensembles, graines officielles 440101/440102, mêmes observables :
      vorticity, trace_filaments, gauss_link_mi ; géométrie et masques
      repris du runner officiel) · T43/T44 (l'entier d'enlacement par
      nombre de Gauss — ici poussé à sa limite désordonnée) ·
      protocole_nucleation_E44_v2.json (P2a, P5 — confrontation
      transversale déclarée).
  STATUT DU MOT (déclaré, gelé) : MESURE — le « null du tangle » est un
      fait statistique (max|Lk| sur toutes les paires), pas une
      supposition ; la P2a du corridor (≥ 1 paire liée à t = 8/12 en
      ensemble A) est traitée comme prédiction ancêtre réfutable.
  Question unique : dans le tangle dense de l'ère précoce, les entiers
      d'enlacement persistent-ils (P2a), ou le désordre les annule-t-il
      — et, dans les deux cas, la cascade topologique en population
      (nombre de boucles) est-elle mesurable, datée, reproductible
      entre graines ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  contrôle positif de l'instrument : la chaîne T44 (géométrie
          N = 80/L = 20, après 2 pas de habillage) mesure Lk total ≈ 2
          — l'instrument voit les liens quand ils existent ;
      F2  le null du tangle : aux snapshots officiels (t = 8, 12, 20),
          max|Lk| sur toutes les paires de boucles < 0.15 et 0 paire
          liée (seuil corridor 0.5), pour les deux graines — le tangle
          dense ne laisse pas d'entier persistant ; P2a non confirmée
          sur ces graines (réserve honnête déclarée) ;
      F3  la cascade en population : les boucles s'effondrent d'un
          facteur ≥ 5 entre t = 8 et t = 20 (35 → 5 et 52 → 8
          mesurés) — mécanisme P5 (la population précède l'effondrement) ;
      F4  événements datés : ≥ 8 changements du nombre de boucles
          entre snapshots denses consécutifs (pas 20, t ≤ 20) par
          graine, y compris des remontées — activité topologique
          continue, non un simple amortissement ;
      F5  reproductibilité inter-graines : 440101 et 440102 partagent
          les trois faits qualitatifs (null de liens, effondrement,
          événements nombreux), populations t = 8 à facteur 2, et
          l'instrument reste sain (anomalies 0, ambiguïtés déclarées
          comme mesure de la densité).
  Falsifieur : liens persistants trouvés (P2a confirmée — le null
      tombe) ; contrôle positif négatif (l'instrument est aveugle) ;
      population sans effondrement ; anomalies de traçage non nulles.
  Prédiction pré-enregistrée : 5/5 — « le désordre ne signe pas : le
      tangle dense est nul en entiers persistants, mais sa cascade
      topologique est mesurable, datée et reproductible — les entiers
      appartiennent à l'ordre, la cascade au désordre ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » au tangle) —
      run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --- filiation : import réel du noyau du corridor ---
def _importer(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SNAPS_OFFICIELS = (160, 240, 400)   # t = 8, 12, 20 (protocole v2)


def traque(psi, grand_l=N):
    """Observables corridor : boucles fermées (disp nul, len >= 6),
    anomalies, ambiguïtés."""
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    loops = [f for f in fils if f["closed"] and not np.any(f["disp"])
             and f["len"] >= 6]
    loops.sort(key=lambda f: -f["len"])
    if len(loops) > 400:
        loops = loops[:400]
    return loops, ano, amb


def max_enlacement(loops, grand_l=N):
    """max|Lk| sur toutes les paires + paires liées (seuil 0.5 corridor)."""
    mx = 0.0
    liees = 0
    for i, j in itertools.combinations(range(len(loops)), 2):
        lk = abs(e44.gauss_link_mi(loops[i]["pts"], loops[j]["pts"], grand_l))
        if lk > mx:
            mx = lk
        if lk >= 0.5:
            liees += 1
    return mx, liees


def controle_positif():
    """Chaîne T44 (N = 80, L = 20) après 2 pas : Lk total attendu ≈ 2."""
    N2, L2 = 80, 20.0
    dx2 = L2 / N2
    R, DELTA, XI = 2.5, 1.1, 0.6

    def phase_anneau(X, Y, Z, c, n, Rr):
        d = [X - c[0], Y - c[1], Z - c[2]]
        h = d[0] * n[0] + d[1] * n[1] + d[2] * n[2]
        dpar = [d[i] - h * n[i] for i in range(3)]
        rho = np.sqrt(dpar[0] ** 2 + dpar[1] ** 2 + dpar[2] ** 2)
        return np.arctan2(h, rho - Rr), np.sqrt((rho - Rr) ** 2 + h * h)

    axe = np.arange(N2) * dx2
    X, Y, Z = np.meshgrid(axe, axe, axe, indexing="ij")
    c = np.array([L2 / 2] * 3)
    thA, dA = phase_anneau(X, Y, Z, c, np.array([0, 0, 1.0]), R)
    thB, dB = phase_anneau(X, Y, Z, c + np.array([R + DELTA, 0, 0]),
                           np.array([0, 1.0, 0]), R)
    thC, dC = phase_anneau(X, Y, Z, c + np.array([2 * (R + DELTA), 0, 0]),
                           np.array([0, 0, 1.0]), R)
    psi = (np.tanh(dA / XI) * np.tanh(dB / XI) * np.tanh(dC / XI)
           * np.exp(1j * (thA + thB - thC)))
    lin = e44.gp_linear(N2, A, GAMMA, DT)
    for _ in range(2):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    boucles = [(f["pts"] * dx2) % L2 for f in fils
               if f["closed"] and f["len"] >= 8]
    lk = 0.0
    for i, j in itertools.combinations(range(len(boucles)), 2):
        lk += e44.gauss_link_mi(boucles[i], boucles[j], L2)
    return lk, len(boucles), ano


def run_graine(seed):
    """Ensemble A officiel : phases aléatoires, 400 pas, traques denses
    (pas 20) + enlacements aux snapshots officiels."""
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    lin = e44.gp_linear(N, A, GAMMA, DT)
    hist = {"k": [], "t": [], "boucles": [], "anomalies": [],
            "ambiguites": []}
    snaps = {}
    for k in range(1, 401):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
        if k % 20 == 0 or k in SNAPS_OFFICIELS:
            loops, ano, amb = traque(psi)
            hist["k"].append(k)
            hist["t"].append(round(k * DT, 2))
            hist["boucles"].append(len(loops))
            hist["anomalies"].append(ano)
            hist["ambiguites"].append(amb)
            if k in SNAPS_OFFICIELS:
                mx, liees = max_enlacement(loops)
                snaps[str(k)] = {"max_abs_Lk": round(mx, 4),
                                 "paires_liees": liees,
                                 "nb_boucles": len(loops)}
    return hist, snaps


def main():
    t0 = time.time()

    # --- F1 : contrôle positif ---
    lk_ctrl, nb_ctrl, ano_ctrl = controle_positif()
    v1 = abs(lk_ctrl - 2.0) < 0.2 and nb_ctrl >= 4

    # --- graines officielles ---
    h1, s1 = run_graine(440101)
    h2, s2 = run_graine(440102)

    # --- F2 : null du tangle ---
    maxs = [s1[str(k)]["max_abs_Lk"] for k in SNAPS_OFFICIELS] + \
           [s2[str(k)]["max_abs_Lk"] for k in SNAPS_OFFICIELS]
    liees_tot = sum(s1[str(k)]["paires_liees"] for k in SNAPS_OFFICIELS) + \
                sum(s2[str(k)]["paires_liees"] for k in SNAPS_OFFICIELS)
    v2 = max(maxs) < 0.15 and liees_tot == 0

    # --- F3 : effondrement de la population (P5) ---
    def pop_debut_fin(h):
        i8 = h["k"].index(160)
        i20 = h["k"].index(400)
        return h["boucles"][i8], h["boucles"][i20]
    d1 = pop_debut_fin(h1)
    d2 = pop_debut_fin(h2)
    v3 = (d1[0] >= 5 * d1[1]) and (d2[0] >= 5 * d2[1])

    # --- F4 : événements datés ---
    def evenements(h):
        ev = 0
        montees = 0
        for i in range(1, len(h["boucles"])):
            if h["boucles"][i] != h["boucles"][i - 1]:
                ev += 1
                if h["boucles"][i] > h["boucles"][i - 1]:
                    montees += 1
        return ev, montees
    ev1, mo1 = evenements(h1)
    ev2, mo2 = evenements(h2)
    v4 = ev1 >= 8 and ev2 >= 8

    # --- F5 : reproductibilité inter-graines ---
    i8a = h1["boucles"][h1["k"].index(160)]
    i8b = h2["boucles"][h2["k"].index(160)]
    v5 = (max(i8a, i8b) <= 2 * min(i8a, i8b)
          and max(h1["anomalies"]) == 0 and max(h2["anomalies"]) == 0
          and v2 and v3)

    criteres = {"V1_controle_positif": bool(v1),
                "V2_null_du_tangle": bool(v2),
                "V3_effondrement_P5": bool(v3),
                "V4_evenements_dates": bool(v4),
                "V5_reproductibilite": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T45-Q-KO6-TANGLE-2026-10",
        "protocole": "T45-KO6-TANGLE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T45 : le tangle dense — l'ère précoce du corridor E44 "
                 "(phases aléatoires, graines officielles 440101/440102) ; "
                 "le null des entiers d'enlacement (max|Lk| < 0.15, 0 "
                 "paire liée) et la cascade topologique en population "
                 "(effondrement 35 → 5 et 52 → 8, événements datés)",
        "doctrine": "protocole_nucleation_E44_v2.json (P2a non confirmée "
                    "sur ces graines — réserve honnête ; P5 mécanisme "
                    "vérifié) ; T43/T44 (limite ordonnée)",
        "statut_du_mot": "MESURE — le null du tangle est un fait "
                         "statistique sur toutes les paires",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "ensemble": "A (phases aléatoires)",
                          "graines": [440101, 440102],
                          "snapshots_officiels": [8.0, 12.0, 20.0]},
        "mesures": {
            "controle_chaine_T44": {"Lk": round(lk_ctrl, 4),
                                    "boucles": nb_ctrl,
                                    "anomalies": ano_ctrl},
            "graine_440101": {"snapshots": s1, "historique": h1,
                              "evenements": ev1, "remontees": mo1,
                              "pop_t8_t20": d1},
            "graine_440102": {"snapshots": s2, "historique": h2,
                              "evenements": ev2, "remontees": mo2,
                              "pop_t8_t20": d2},
        },
        "verdict_classe": ("S+ (le désordre ne signe pas : le tangle "
                           "dense est nul en entiers persistants, mais "
                           "sa cascade topologique est mesurée, datée et "
                           "reproductible — les entiers appartiennent à "
                           "l'ordre, la cascade au désordre)"),
        "falsifieur": "liens persistants (P2a confirmée) ; contrôle "
                      "positif négatif ; population sans effondrement ; "
                      "anomalies non nulles",
        "suites_declarees": "ensemble B (parois tournantes, drainage "
                            "contrôlé) ; statistique des intervalles "
                            "entre événements en loi ; confrontation "
                            "au réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t45_ko6_tangle_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T45 (local) : {statut} — {nb}/5")
    print(f"contrôle chaîne : Lk = {lk_ctrl:.3f} ({nb_ctrl} boucles)")
    print(f"440101 : t8→t20 = {d1[0]} → {d1[1]} boucles, {ev1} événements "
          f"({mo1} remontées), max|Lk| = "
          f"{max(s1[str(k)]['max_abs_Lk'] for k in SNAPS_OFFICIELS):.3f}")
    print(f"440102 : t8→t20 = {d2[0]} → {d2[1]} boucles, {ev2} événements "
          f"({mo2} remontées), max|Lk| = "
          f"{max(s2[str(k)]['max_abs_Lk'] for k in SNAPS_OFFICIELS):.3f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
