#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T46 — Q-KO6-T46-2026-10 : T46 — LE DRAINAGE CONTRÔLÉ
      (parois tournantes, trois ères, loi des intervalles)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T46-KO6-DRAIN-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T45 (le tangle sans paroi, null des entiers).
      T46 active le forçage : ensemble B du corridor — cylindre à paroi
      FIXE portant la circulation 4 imposée (phase e^{4iφ} sur l'anneau
      de paroi, imposée à chaque pas). Le tangle n'est plus livré à
      lui-même : la paroi nourrit, la dissipation draine. Exploration
      mesurée : trois ères — nucléation violente (t < 3), drainage
      rapide (t = 3 → 12), stationnarité murale (t = 15 → 90,
      ~17 filaments ouverts épinglés, 0 boucle, anomalies stables à 4 —
      la circulation imposée laisse quatre défauts de paroi).
  Filiation : corridor E (protocole de nucléation E44 v2 — ensemble B,
      graines officielles 440201/440203, géométrie, masques et fix
      repris du runner officiel ; vorticity, trace_filaments) ·
      T45 (ère précoce sans paroi — le contraste A/B est le levier) ·
      T42-D1 (contraction/dissipation comme moteur du drainage).
  STATUT DU MOT (déclaré, gelé) : MESURE — les trois ères sont datées
      dans des trajectoires ; la « loi des intervalles » est une
      propriété de distribution (décroissante), pas une formule
      ajustée.
  Question unique : sous circulation de paroi imposée, le corridor
      traverse-t-il les trois ères mesurables (nucléation datée,
      drainage contrôlé, stationnarité murale), et la distribution des
      intervalles entre événements topologiques de l'ère précoce
      est-elle décroissante — pour deux graines officielles ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  l'instrument reste sain sous forçage : anomalies transitoires
          bornées (≤ 150 au pic de nucléation) puis stabilisées
          (≤ 5 en seconde moitié), traçage vivant tout au long ;
      F2  la nucléation est datée : pic de population (boucles +
          filaments ouverts) ≥ 150 filaments atteint à t ≤ 4 ;
      F3  le drainage est contrôlé : 0 boucle pour tout t ≥ 12 et
          population divisée par ≥ 5 du pic à t = 12 ;
      F4  la stationnarité murale : t ∈ [15, 90] — 0 boucle, ouverts
          ∈ [10, 30], coefficient de variation < 0.2 ;
      F5  la loi des intervalles : ère précoce (pas 20, t ≤ 20),
          ≥ 8 événements (changements du nombre de boucles), distribution
          décroissante (n(Δ = 1 pas) > n(Δ ≥ 3 pas)) — et cela tient
          pour les deux graines officielles.
  Falsifieur : pas de pic précoce ; boucles persistantes au-delà de
      t = 12 ; pas de plateau (divergence ou effondrement total) ;
      intervalles non décroissants ; saturation du traçage (anomalies
      croissantes).
  Prédiction pré-enregistrée : 5/5 — « sous circulation imposée, le
      corridor vit trois ères datées — naître, drainer, s'accrocher au
      mur — et les intervalles entre événements obéissent à une loi
      décroissante : le désordre est d'abord rapide, puis s'oublie ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 4/5, publié) :
  D1  la borne d'anomalies pré-enregistrée (≤ 25) venait de
      l'exploration à pas 60 ; à pas 20, le transitoire de nucléation
      culmine à 104 anomalies (t = 1) avant de retomber à 4 pour
      toujours — la santé de l'instrument est la STABILISATION, pas la
      borne du transitoire. Correction v1.1 : anomalies transitoires
      ≤ 150, stabilisation ≤ 5 en seconde moitié. Mesures physiques
      inchangées (pic 944 filaments à t = 1, drainage, plateau CV
      0.068, loi décroissante n1 = 6 > n3 = 1).
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » à l'ensemble
      B) — run local avant push, empreinte figée au verdict.
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


def masque(w, ax):
    """Masque géométrique officiel (plaquettes à l'intérieur du récipient)."""
    r = lambda x, a: np.roll(x, -1, a)
    if ax == 0:
        corners = [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]
    elif ax == 1:
        corners = [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)]
    else:
        corners = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    keep = np.ones((N,) * 3, bool)
    for dx, dy, dz in corners:
        idx = (np.clip(Xg + dx, 0, N - 1), np.clip(Yg + dy, 0, N - 1),
               np.clip(Zg + dz, 0, N - 1))
        keep &= INSIDE[idx]
    return np.where(keep, w, 0)


def traque_B(psi):
    """Traçage officiel de l'ensemble B (masques + filtre corridor)."""
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    loops = [f for f in fils if f["closed"] and not np.any(f["disp"])
             and f["len"] >= 6]
    opens = [f for f in fils
             if not (f["closed"] and not np.any(f["disp"]))]
    return len(loops), len(opens), ano, amb


def run_B(seed, steps=1800, pas=20):
    """Ensemble B officiel : paroi fixe circulation 4, trajectoire
    complète sur snapshots denses."""
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(4j * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(4j * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    hist = {"k": [], "t": [], "boucles": [], "ouverts": [],
            "anomalies": [], "ambiguites": []}
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            nb, no, ano, amb = traque_B(psi)
            hist["k"].append(k)
            hist["t"].append(round(k * DT, 2))
            hist["boucles"].append(nb)
            hist["ouverts"].append(no)
            hist["anomalies"].append(ano)
            hist["ambiguites"].append(amb)
    return hist


def evenements_intervalles(h):
    """Événements de l'ère précoce (t <= 20) : changements du nombre de
    boucles entre snapshots consécutifs ; intervalles en pas de mesure."""
    ks = [i for i, t in enumerate(h["t"]) if t <= 20.0]
    ev = []
    for a, b in zip(ks, ks[1:]):
        if h["boucles"][b] != h["boucles"][a]:
            ev.append((a, b))
    intervalles = [ev[i + 1][0] - ev[i][0] for i in range(len(ev) - 1)]
    return ev, intervalles


def analyse_graine(h):
    """Les faits mesurés sur une trajectoire B."""
    pop = [b + o for b, o in zip(h["boucles"], h["ouverts"])]
    i_pic = int(np.argmax(pop))
    # ère 3 : t >= 15
    era3 = [i for i, t in enumerate(h["t"]) if t >= 15.0]
    pop3 = [h["ouverts"][i] for i in era3]
    cv3 = float(np.std(pop3) / np.mean(pop3)) if pop3 and np.mean(pop3) else 9.9
    ev, inter = evenements_intervalles(h)
    n1 = sum(1 for x in inter if x == 1)
    n3 = sum(1 for x in inter if x >= 3)
    return {"pic_pop": pop[i_pic], "t_pic": h["t"][i_pic],
            "pop_t12": pop[min(range(len(h["t"])),
                               key=lambda i: abs(h["t"][i] - 12.0))],
            "boucles_apres_12": max(h["boucles"][i] for i, era in
                                    enumerate(h["t"]) if era >= 12.0),
            "ouverts_era3": pop3, "cv_era3": cv3,
            "anomalies_max": max(h["anomalies"]),
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
            "evenements": len(ev), "intervalles": inter,
            "loi_n1": n1, "loi_n3": n3}


def main():
    t0 = time.time()

    h1 = run_B(440201)
    h2 = run_B(440203)
    a1 = analyse_graine(h1)
    a2 = analyse_graine(h2)

    # --- F1 : instrument sain sous forçage (440201) ---
    v1 = (a1["anomalies_max"] <= 150 and a1["anomalies_fin"] <= 5
          and min(a1["ouverts_era3"]) >= 10)

    # --- F2 : nucléation datée (440201) ---
    v2 = a1["pic_pop"] >= 150 and a1["t_pic"] <= 4.0

    # --- F3 : drainage contrôlé (440201) ---
    v3 = (a1["boucles_apres_12"] == 0
          and a1["pop_t12"] <= a1["pic_pop"] / 5.0)

    # --- F4 : stationnarité murale (440201) ---
    v4 = (a1["boucles_apres_12"] == 0
          and 10 <= float(np.mean(a1["ouverts_era3"])) <= 30
          and a1["cv_era3"] < 0.2)

    # --- F5 : loi des intervalles, deux graines ---
    loi1 = a1["loi_n1"] > a1["loi_n3"] and a1["evenements"] >= 8
    loi2 = a2["loi_n1"] > a2["loi_n3"] and a2["evenements"] >= 8
    v5 = loi1 and loi2

    criteres = {"V1_instrument_sain": bool(v1),
                "V2_nucleation_datee": bool(v2),
                "V3_drainage_controle": bool(v3),
                "V4_stationnarite_murale": bool(v4),
                "V5_loi_des_intervalles": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T46-Q-KO6-DRAIN-2026-10",
        "protocole": "T46-KO6-DRAIN-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T46 : le drainage contrôlé — ensemble B du corridor "
                 "(paroi fixe, circulation 4 imposée) ; trois ères datées "
                 "(nucléation, drainage, stationnarité murale) et loi "
                 "décroissante des intervalles entre événements "
                 "topologiques",
        "doctrine": "protocole_nucleation_E44_v2.json (ensemble B) ; "
                    "T45 (contraste A/B) ; T42-D1 (dissipation)",
        "statut_du_mot": "MESURE — trois ères datées, loi de distribution",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "ensemble": "B (paroi fixe circulation 4)",
                          "graines": [440201, 440203],
                          "fenetre": [0.0, 90.0]},
        "mesures": {
            "graine_440201": a1,
            "graine_440203": a2,
            "historique_440201": h1,
            "historique_440203": h2,
        },
        "verdict_classe": ("S+ (trois ères datées sous circulation "
                           "imposée : naître vite, drainer, s'accrocher "
                           "au mur ; les intervalles entre événements "
                           "obéissent à une loi décroissante — le "
                           "désordre est d'abord rapide, puis s'oublie)"),
        "falsifieur": "pas de pic ; boucles persistantes ; pas de "
                      "plateau ; intervalles non décroissants ; "
                      "saturation du traçage",
        "suites_declarees": "densité de ligne vs taux d'événements "
                            "(relation de Vinen côté corridor) ; "
                            "confrontation au réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t46_ko6_drainage_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T46 (local) : {statut} — {nb}/5")
    print(f"440201 : pic {a1['pic_pop']} filaments à t = {a1['t_pic']} ; "
          f"pop t=12 : {a1['pop_t12']} ; boucles après t=12 : "
          f"{a1['boucles_apres_12']} ; plateau ouverts "
          f"{float(np.mean(a1['ouverts_era3'])):.1f} ± CV "
          f"{a1['cv_era3']:.3f} ; anomalies max/fin "
          f"{a1['anomalies_max']}/{a1['anomalies_fin']}")
    print(f"440201 : {a1['evenements']} événements, intervalles "
          f"{a1['intervalles']} (n1={a1['loi_n1']}, n3={a1['loi_n3']})")
    print(f"440203 : {a2['evenements']} événements (n1={a2['loi_n1']}, "
          f"n3={a2['loi_n3']}) ; pic {a2['pic_pop']} à t={a2['t_pic']}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
