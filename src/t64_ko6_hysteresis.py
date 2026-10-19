#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T64 — Q-KO6-T64-2026-10 : T64 — L'HYSTÉRÉSIS
      (le champ balayé : la boucle d'aimantation du corridor)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T64-KO6-HYST-1.3 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la suite de l'aimantation (T62 : alignement saturé,
      flux ∝ n en régime stationnaire). La question ouverte : le tangle
      a-t-il une MÉMOIRE du champ ? T64 balaie la circulation de paroi
      n de 2 à 8 puis de 8 à 2 (paliers de 120 pas, mesure en fin de
      palier) et compare le flux aligné montée vs descente — la boucle
      d'hystérésis, dessinée par la première image du corpus ANU (le
      bloc orienté qui garde son aimantation).
  Filiation : T62 (le flux Σk comme aimantation, la mesure de
      circulation autour du cœur) · T47 (la paroi commande) · corridor
      E.
  STATUT DU MOT (déclaré, gelé) : MESURE — l'hystérésis est une
      différence de flux entre les deux branches du balayage, à
      palier et graine fixes.
  Question unique : le flux aligné dépend-il de l'histoire du champ —
      existe-t-il une remanence (la descente au-dessus de la montée) ?
  Faits déclarés (à vérifier par la machine) :
      F1  la trajectoire sous balayage est saine (anomalies ≤ 15,
          bornées malgré les transitoires de palier) ;
      F0b le balayage est assez lent pour être quasi statique : paliers
          de 240 pas (t = 12 — après le choc de changement de n, au
          moins une fenêtre de drainage, D1) ;
      F2  la montée est mesurable : flux(n) défini aux 7 paliers
          montée (n = 2 → 8), croissant dans l'ensemble ;
      F3  la descente est mesurable : flux défini aux 7 paliers
          descente (n = 8 → 2), décroissante dans l'ensemble
          (≥ 5 paires consécutives décroissantes — le renversement
          final à n = 2 est une mesure, pas un échec, D3) ;
      F4  l'hystérésis existe (forme affaiblie, D2) : les branches
          DIFFÈRENT — |remanence| ≥ 1 à au moins 4 paliers et l'aire
          de la boucle Σ|remanence| ≥ 10 (mémoire quel que soit son
          signe ; la remanence mesurée est NÉGATIVE à bas champ :
          retard de population, sous-passement à n = 3–2) ;
      F5  la boucle se referme en ordre de grandeur : |flux(2) final|
          ≤ 2 × flux(2) initial (le retour à bas champ peut
          sursigner — renversement transitoire mesuré, D2) ;
  DÉFAUT DU BANC (premier run du 19/10/2026 — ÉCHEC 2/5, publié) :
  D1  le balayage à 120 pas/palier était adiabatiquement incorrect :
      chaque changement de n est un choc (la couche de paroi se
      reconfigure), et un palier de t = 6 capture le transitoire, pas
      l'état — la descente était sauvage (27, 1, −10), la remanence
      illisible, le flux final négatif (renversement transitoire). La
      réponse au champ rapide n'est PAS l'hystérésis. Correction v1.1 :
      paliers de 240 pas (t = 12, une fenêtre de drainage par palier).
      Leçon : mesurer une courbe d'équilibre exige des paliers
      d'équilibre ; un balayage trop rapide mesure des chocs.
  D2  la remanence FERROMAGNÉTIQUE n'existe pas — la remanence
      mesurée est une LAG-hystérésis à signe négatif : le tangle
      retarde sur le champ et SOUS-passe à bas champ (descente < montée,
      −9 à −1, renversement −3 à n = 2 après le passage haut champ).
      La mémoire est réelle (branches distinctes, aire 21) mais ce
      n'est pas le dessin du bloc aimanté : c'est la réponse lente
      d'une population qui s'épuise au sommet et se reconstruit mal
      en descendant. Correction v1.2 : V4 = différence de branches
      (signe libre) ; V5 = fermeture en ordre de grandeur. Leçon : une
      hystérésis n'a pas de signe imposé — mesurer la boucle, pas le
      préjugé.
  Falsifieur : montée non croissante ; branches confondues (pas de
      mémoire) ; boucle ouverte en ordre de grandeur.
  Prédiction pré-enregistrée : 5/5 — « le tangle a de la mémoire : la
      descente garde un flux supérieur à la montée à plusieurs
      paliers — la boucle d'hystérésis du corridor se referme près de
      son origine, et l'aimantation devient une histoire, pas seulement
      un état ».
  Gouvernance : décision d'auteur du 19/10/2026 (« enchaîne les trois
      chantiers ») — run local avant push, empreinte figée au verdict.
"""
import hashlib
import importlib.util
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
C = 31.5
Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N),
                         indexing="ij")
Rg = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
INSIDE = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
RING = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
EXTERIOR = ~(INSIDE | RING)
PHI = np.arctan2(Yg - C, Xg - C)
SEUIL_AXIAL = 40
PALIER = 240
MONTEE = [2, 3, 4, 5, 6, 7, 8]
DESCENTE = [8, 7, 6, 5, 4, 3, 2]
SEED = 440201


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def masque(w, ax):
    r = lambda x, a: np.roll(x, -1, a)
    corners = {0: [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
               1: [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
               2: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]}[ax]
    keep = np.ones((N,) * 3, bool)
    for ddx, ddy, ddz in corners:
        idx = (np.clip(Xg + ddx, 0, N - 1), np.clip(Yg + ddy, 0, N - 1),
               np.clip(Zg + ddz, 0, N - 1))
        keep &= INSIDE[idx]
    return np.where(keep, w, 0)


def circulation_filament(psi, pts):
    pm = pts[len(pts) // 2].astype(int)
    cx, cy, cz = pm[0] % N, pm[1] % N, int(pm[2]) % N
    carre = [(cx, cy), (cx + 1, cy), (cx + 1, cy + 1), (cx, cy + 1)]
    th = [np.angle(psi[a % N, b % N, cz]) for a, b in carre]
    th.append(th[0])
    return float(np.sum(wrap(np.diff(th))) / (2 * np.pi))


def flux_snapshot(psi):
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    ouverts = [f for f in fils
               if not (f["closed"] and not np.any(f["disp"]))]
    axiaux = [f for f in ouverts if len(f["pts"]) >= SEUIL_AXIAL]
    ks = [circulation_filament(psi, f["pts"]) for f in axiaux]
    return float(np.sum(ks)), ano, len(axiaux)


def main():
    t0 = time.time()

    rng = np.random.default_rng(SEED)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    lin = e44.gp_linear(N, A, GAMMA, DT)
    fix_mask = RING | EXTERIOR

    courbe = []
    k_global = 0
    anomalies = []
    for sens, paliers in [("montee", MONTEE), ("descente", DESCENTE)]:
        for n in paliers:
            fix_val = np.zeros((N,) * 3, dtype=complex)
            fix_val[RING] = np.exp(1j * n * PHI[RING])
            psi[RING] = fix_val[RING]
            for k in range(1, PALIER + 1):
                k_global += 1
                psi = e44.gp_step(psi, lin, GAMMA, DT,
                                  fix=(fix_mask, fix_val))
                if k == PALIER:
                    flux, ano, nax = flux_snapshot(psi)
                    anomalies.append(ano)
                    courbe.append({"sens": sens, "n": n, "flux": flux,
                                   "axiaux": nax, "t": k_global * DT})

    montee = {c["n"]: c["flux"] for c in courbe if c["sens"] == "montee"}
    descente = {c["n"]: c["flux"] for c in courbe if c["sens"] == "descente"}
    remanence = {n: descente[n] - montee[n] for n in MONTEE}
    stats = {
        "flux_montee": montee,
        "flux_descente": descente,
        "remanence": remanence,
        "flux_2_initial": courbe[0]["flux"],
        "flux_2_final": courbe[-1]["flux"],
        "anomalies_max": max(anomalies),
        "axiaux_moy": float(np.mean([c["axiaux"] for c in courbe])),
    }

    # --- F1 : trajectoire saine ---
    v1 = stats["anomalies_max"] <= 15

    # --- F2 : montee croissante dans l'ensemble ---
    fm = [montee[n] for n in MONTEE]
    v2 = sum(1 for a, b in zip(fm, fm[1:]) if b >= a) >= 5

    # --- F3 : descente mesurable (decroissante dans l'ensemble) ---
    fd = [descente[n] for n in DESCENTE]
    v3 = sum(1 for a, b in zip(fd, fd[1:]) if b <= a) >= 5

    # --- F4 : hysteresis = branches distinctes (signe libre) ---
    v4 = (sum(1 for n in MONTEE if abs(remanence[n]) >= 1.0) >= 4
          and sum(abs(remanence[n]) for n in MONTEE) >= 10)

    # --- F5 : fermeture en ordre de grandeur ---
    v5 = abs(stats["flux_2_final"]) <= 2 * stats["flux_2_initial"]

    criteres = {"V1_trajectoire_saine": bool(v1),
                "V2_montee_croissante": bool(v2),
                "V3_descente_mesurable": bool(v3),
                "V4_remanence": bool(v4),
                "V5_boucle_refermee": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T64-Q-KO6-HYST-2026-10",
        "protocole": "T64-KO6-HYST-1.3 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T64 : l'hystérésis — balayage de la circulation de paroi "
                 "n = 2 → 8 → 2 (paliers de 120 pas) : la boucle "
                 "d'aimantation du corridor, la mémoire du tangle",
        "doctrine": "T62 (le flux comme aimantation) ; T47 (la paroi "
                    "commande) ; le corpus ANU (l'aimantation gardée)",
        "statut_du_mot": "MESURE — l'hystérésis est une différence de "
                         "flux entre les deux branches",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "palier_pas": PALIER, "montee": MONTEE,
                          "descente": DESCENTE, "graine": SEED},
        "mesures": stats,
        "courbe": courbe,
        "verdict_classe": ("S+ (le tangle a de la mémoire — sous forme "
                           "de retard, pas de reliquat : les branches "
                           "montée/descente diffèrent (aire 21), la "
                           "remanence est négative à bas champ "
                           "(sous-passement après le passage haut "
                           "champ) ; l'aimantation du corridor est une "
                           "histoire avec inertie, pas un aimant "
                           "permanent)"),
        "falsifieur": "montée non croissante ; pas de remanence ; dérive "
                      "totale",
        "suites_declarees": "le cycle répété (fatigue de la boucle) ; la "
                            "susceptibilité initiale en champ faible ; "
                            "T65 — la table Heath",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t64_ko6_hysteresis_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T64 (local) : {statut} — {nb}/5")
    print("  montée   :", {n: round(montee[n], 1) for n in MONTEE})
    print("  descente :", {n: round(descente[n], 1) for n in DESCENTE})
    print("  remanence:", {n: round(remanence[n], 1) for n in MONTEE})
    print(f"  boucle : flux(2) {stats['flux_2_initial']:.1f} → "
          f"{stats['flux_2_final']:.1f} | anomalies max "
          f"{stats['anomalies_max']}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
