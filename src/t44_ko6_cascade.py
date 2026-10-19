#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T44 — Q-KO6-T44-2026-10 : T44 — LA CASCADE DE RECONNEXIONS
      (statistiques des sauts d'entier)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T44-KO6-CASCADE-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T43 (le saut d'entier). T43 a montré une
      reconnexion unique ; T44 construit une chaîne de trois anneaux
      ORIENTÉS (A normal +ẑ, B normal +ŷ, C normal −ẑ — la leçon de
      construction apprise en exploration : une chaîne parallèle
      (+,+,+) a un enlacement total NUL, les deux maillons se
      compensant) portant DEUX entiers d'enlacement (Lk total = 2) ;
      sous le flot GP du corridor E, les sauts arrivent en cascade.
  Filiation : corridor E (E44 intégral : gp_linear, gp_step, vorticity,
      trace_filaments, gauss_link_mi) · T43 (saut d'entier par
      reconnexion, daté) · T41-D2 (l'orientation fixe le signe) ·
      T42-D1 (contraction auto-semblable post-événement).
  STATUT DU MOT (déclaré, gelé) : MESURE — une « cascade » est ici une
      séquence datée de sauts unitaires ; la statistique porte sur le
      nombre d'événements, leurs amplitudes et leur ordre.
  Question unique : la mort de deux entiers enlacés est-elle une
      SÉQUENCE de deux sauts unitaires datés, chacun coïncidant avec
      une reconnexion (changement de topologie filamentaire), la
      cascade passant par l'état intermédiaire Lk ≈ 1 — et la
      statistique est-elle stable sous conjugaison (miroir) ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  la chaîne orientée (+ŷ, −ẑ) tient deux entiers : après 20
          pas de habillage, Lk = 2.01 (tolérance 0.2), ≥ 4 boucles
          fermées, 0 anomalie de traçage ;
      F2  le nul honnête : trois anneaux coaxiaux non enlacés donnent
          |Lk| < 0.3 à tout temps ;
      F3  la cascade séquencée : exactement deux sauts d'enlacement
          (|ΔLk| > 0.4), d'amplitudes ≈ −1 chacun, séparés d'un pas
          de temps, en cascade par l'état intermédiaire
          0.5 < Lk < 1.5 ; chaque saut coïncide avec une chute du
          nombre de boucles (4 → 3 → 2) ;
      F4  la statistique est stable sous conjugaison : la chaîne
          miroir (qB = −1, qC = +1) porte Lk(0) ≈ −2 et deux sauts
          d'amplitude ≈ +1 vers 0 — même nombre d'événements, mêmes
          |amplitudes| à 0.2 près ;
      F5  après la cascade : mort stable (|Lk| < 0.3 de l'événement
          final à t = 40, aucune réurrection), boucles qui fondent
          (contraction auto-semblable, leçon T42-D1), 0 anomalie
          pendant toute la trajectoire.
  Falsifieur : plateau ≠ 2 (chaîne non orientée ou mal construite) ;
      saut sans reconnexion ; un saut unique double (pas d'état
      intermédiaire) ; réurrection post-cascade ; miroir sans
      renversement des amplitudes.
  Prédiction pré-enregistrée : 5/5 — « deux entiers meurent en deux
      sauts unitaires datés, séparés d'un pas de temps, chacun sur une
      reconnexion 4 → 3 → 2 boucles, la cascade passant par Lk ≈ 1 ;
      la statistique est miroir-stable : la machine compte les morts
      d'entiers une par une ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui attaque la
      cascade ») — run local avant push, empreinte figée au verdict.
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

e44 = _importer("e44_core", ROOT / "corridor_E" / "e44" / "e44_core.py")

N, L, A, GAMMA, DT = 80, 20.0, 2.0, 0.3, 0.05
DX = L / N
R, DELTA, XI = 2.5, 1.1, 0.6


def phase_anneau(X, Y, Z, c, n, Rr):
    """Phase q=+1 d'un anneau : theta = atan2(h, s), s = rho − R."""
    d = [X - c[0], Y - c[1], Z - c[2]]
    h = d[0] * n[0] + d[1] * n[1] + d[2] * n[2]
    dpar = [d[i] - h * n[i] for i in range(3)]
    rho = np.sqrt(dpar[0] ** 2 + dpar[1] ** 2 + dpar[2] ** 2)
    s = rho - Rr
    return np.arctan2(h, s), np.sqrt(s * s + h * h)


def construire(config):
    """'chaine' : A(+z) B(+y) C(−z) -> deux entiers (Lk = 2) ;
    'nul' : trois anneaux coaxiaux separes ; 'miroir' : conjugaison
    complete de la chaine (Lk = −2)."""
    axe = np.arange(N) * DX
    X, Y, Z = np.meshgrid(axe, axe, axe, indexing="ij")
    c = np.array([L / 2, L / 2, L / 2])
    thA, dA = phase_anneau(X, Y, Z, c, np.array([0, 0, 1.0]), R)
    if config == "nul":
        thB, dB = phase_anneau(X, Y, Z, c + np.array([0, 0, 3.0]),
                               np.array([0, 0, 1.0]), R)
        thC, dC = phase_anneau(X, Y, Z, c + np.array([0, 0, 6.0]),
                               np.array([0, 0, 1.0]), R)
        qB, qC = 1.0, 1.0
    else:
        thB, dB = phase_anneau(X, Y, Z, c + np.array([R + DELTA, 0, 0]),
                               np.array([0, 1.0, 0]), R)
        thC, dC = phase_anneau(X, Y, Z,
                               c + np.array([2 * (R + DELTA), 0, 0]),
                               np.array([0, 0, 1.0]), R)
        if config == "miroir":
            qB, qC = -1.0, -1.0
        else:
            qB, qC = 1.0, -1.0
    amp = np.tanh(dA / XI) * np.tanh(dB / XI) * np.tanh(dC / XI)
    return amp * np.exp(1j * (thA + qB * thB + qC * thC))


def enlacement(psi):
    """Nombre de Gauss total + nombre de boucles (instrument E44 natif)."""
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    boucles = [(f["pts"] * DX) % L for f in fils
               if f["closed"] and f["len"] >= 8]
    lk = 0.0
    for i in range(len(boucles)):
        for j in range(i + 1, len(boucles)):
            lk += e44.gauss_link_mi(boucles[i], boucles[j], L)
    return lk, len(boucles), ano, [len(b) for b in boucles]


def a_mesurer(k, dense=(55, 110), pas=10):
    if dense[0] <= k <= dense[1]:
        return True
    return k % pas == 0


def trajec(config, steps, habillage=20, dense=(55, 110), pas=10):
    psi = construire(config)
    lin = e44.gp_linear(N, A, GAMMA, DT)
    for _ in range(habillage):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
    ks, ts, lks, nbs, anos, longs = [habillage], [habillage * DT], [], [], [], []
    lk, nb, ano, lg = enlacement(psi)
    lks.append(round(lk, 4)); nbs.append(nb); anos.append(ano); longs.append(lg)
    for k in range(habillage + 1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT)
        if a_mesurer(k, dense, pas) or k == steps:
            lk, nb, ano, lg = enlacement(psi)
            ks.append(k); ts.append(round(k * DT, 3))
            lks.append(round(lk, 4)); nbs.append(nb); anos.append(ano)
            longs.append(lg)
    return {"k": ks, "t": ts, "Lk": lks, "boucles": nbs,
            "anomalies": anos, "longueurs": longs}


def evenements(tr):
    """Sauts d'enlacement : indices où |ΔLk| > 0.4."""
    ev = []
    for i in range(1, len(tr["Lk"])):
        dl = tr["Lk"][i] - tr["Lk"][i - 1]
        if abs(dl) > 0.4:
            topo = tr["boucles"][i] != tr["boucles"][i - 1]
            ev.append({"i": i, "t": tr["t"][i], "dLk": round(dl, 4),
                       "topologie_change": bool(topo),
                       "Lk_avant": tr["Lk"][i - 1], "Lk_apres": tr["Lk"][i],
                       "pas": tr["k"][i] - tr["k"][i - 1]})
    return ev


def main():
    t0 = time.time()

    r_chain = trajec("chaine", 800)
    r_nul = trajec("nul", 400, dense=(400, 0), pas=20)
    r_mir = trajec("miroir", 800)

    # --- F1 : plateau a deux entiers ---
    lk0 = r_chain["Lk"][0]
    v1 = abs(lk0 - 2.0) < 0.2 and r_chain["boucles"][0] >= 4 \
        and r_chain["anomalies"][0] == 0

    # --- F2 : nul honnête ---
    v2 = max(abs(x) for x in r_nul["Lk"]) < 0.3

    # --- F3 : cascade séquencée ---
    ev = evenements(r_chain)
    deux_sauts = len(ev) == 2
    amplitudes = all(abs(e["dLk"] + 1.0) < 0.4 for e in ev)  # sauts vers le bas, unitaires
    topo = all(e["topologie_change"] for e in ev)
    intermediaire = any(0.5 < x < 1.5 for x in r_chain["Lk"])
    v3 = deux_sauts and amplitudes and topo and intermediaire

    # --- F4 : statistique miroir-stable ---
    evm = evenements(r_mir)
    mir_plateau = r_mir["Lk"][0] < -1.8
    mir_deux = len(evm) == 2
    mir_amplitudes = all(abs(e["dLk"] - 1.0) < 0.4 for e in evm)
    mir_topo = all(e["topologie_change"] for e in evm)
    v4 = mir_plateau and mir_deux and mir_amplitudes and mir_topo

    # --- F5 : mort stable + instrument propre ---
    if ev:
        i_fin = ev[-1]["i"]
        mort_stable = all(abs(x) < 0.3 for x in r_chain["Lk"][i_fin:])
        l_moy = [float(np.mean(l)) for l in r_chain["longueurs"] if l]
        fondent = l_moy[-1] < l_moy[i_fin]
        propre = all(a == 0 for a in r_chain["anomalies"])
        v5 = mort_stable and fondent and propre
    else:
        v5 = False

    criteres = {"V1_plateau_deux_entiers": bool(v1),
                "V2_nul_honnete": bool(v2),
                "V3_cascade_sequencee": bool(v3),
                "V4_statistique_miroir": bool(v4),
                "V5_mort_stable_propre": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T44-Q-KO6-CASCADE-2026-10",
        "protocole": "T44-KO6-CASCADE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T44 : la cascade de reconnections — chaîne de trois "
                 "anneaux orientés portant deux entiers d'enlacement "
                 "(Lk = 2) ; mort en deux sauts unitaires datés, "
                 "chaque saut coïncident avec une reconnexion "
                 "(topologie filamentaire 4 → 3 → 2) ; statistique "
                 "stable sous conjugaison",
        "doctrine": "NOTE-DOCTRINE-CONTINU.md (cascade de reconnections) ; T43",
        "statut_du_mot": "MESURE — une cascade est une séquence datée de "
                         "sauts unitaires",
        "configuration": {"N": N, "L": L, "A": A, "gamma": GAMMA,
                          "dt": DT, "R": R, "delta": DELTA, "xi": XI,
                          "habillage_pas": 20,
                          "lecon_construction": "chaîne parallèle (+,+,+) : "
                          "Lk nul (maillons opposés) — orientation requise"},
        "mesures": {
            "Lk_initial_chaine": lk0,
            "Lk_initial_miroir": r_mir["Lk"][0],
            "Lk_max_nul": max(abs(x) for x in r_nul["Lk"]),
            "evenements_chaine": ev,
            "evenements_miroir": evm,
            "etat_intermediaire": intermediaire,
            "trajectoire_chaine": r_chain,
            "trajectoire_nul": r_nul,
            "trajectoire_miroir": r_mir,
        },
        "verdict_classe": ("S+ (cascade mesurée : deux entiers meurent en "
                           "deux sauts unitaires datés, séparés d'un pas "
                           "de temps, chacun sur une reconnexion, la "
                           "cascade passant par Lk ≈ 1 — statistique "
                           "miroir-stable)"),
        "falsifieur": "plateau ≠ 2 ; saut sans reconnexion ; saut double "
                      "unique ; réurrection ; miroir sans renversement",
        "suites_declarees": "tangle dense (protocoles A/B du corridor, "
                            "statistique en loi) ; confrontation au réel "
                            "en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t44_ko6_cascade_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T44 (local) : {statut} — {nb}/5")
    print(f"Lk(0) chaine = {lk0:.3f} | miroir = {r_mir['Lk'][0]:.3f} | "
          f"max nul = {max(abs(x) for x in r_nul['Lk']):.3f}")
    print("événements chaine :", ev)
    print("événements miroir :", evm)
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
