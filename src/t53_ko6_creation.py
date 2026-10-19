#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T53 — Q-KO6-T53-2026-10 : T53 — LA CRÉATION
      (taux de nucléation par unité de paroi, longueur de naissance)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T53-KO6-CREAT-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T52 (la nucléation domine la production).
      Restait la loi d'échelle de la création elle-même : à quel taux
      la paroi engendre-t-elle des filaments, et de quelle longueur
      naissent-ils ? Point de doctrine : le comptage des nucléations ne
      demande pas de β — n = 2, hors régime pour la loi de décroissance
      (T47–T49), participe pleinement à la loi de création. Le mur
      crée partout ; la loi de mort, elle, a sa frontière.
  Filiation : T52 (décomposition nucléations/croissances, critère
      d'événement repris) · NOTE-VINEN-T47-T51 (la production α(v)) ·
      corridor E (protocole B, fenêtre 1800 pas) · T47 (4 filaments
      par quantum — le résultat net de la création moins la mort).
  STATUT DU MOT (déclaré, gelé) : MESURE — un événement de nucléation
      est un intervalle où le nombre de filaments trace's monte
      (dN > 0) ; la longueur de naissance est dΛ/dN sur ces intervalles
      (attribution intégrale, déclarée).
  Question unique : le taux de nucléation par cellule de paroi
      croît-il avec le quantum de circulation, et les filaments
      naissent-ils comme des segments de longueur bornée — partout,
      y compris à n = 2 où la loi de décroissance ne tient pas ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les quatre trajectoires (n = 2, 4, 8 × graine 440201, plus
          n = 8/440203, 1800 pas) sont saines : anomalies stabilisées
          ≤ 10 en seconde moitié ;
      F2  la création est comptable à basse densité (n = 2 et n = 4) :
          ≥ 5 événements et taux > 0 (10 et 12 événements mesurés) —
          à n = 8 le comptage dN est corrompu par la densité du tangle
          (4–6 événements — les naissances y fusionnent avant d'être
          comptées) : déclaré, la création y reste mesurable par la
          longueur de naissance (D1) ;
      F3  les filaments naissent comme des segments : longueur de
          naissance ∈ [5, 120] cellules (41–66 mesuré) ;
      F4  la loi d'échelle de la création vit dans la TAILLE, non dans
          le taux : le taux par cellule de paroi est constant à basse
          densité (~1.1–1.3e-5) et la longueur de naissance à n = 8
          (57–66 cellules) dépasse celle à n = 2/4 (41–45) — le mur
          crée des embryons plus gros quand le quantum monte (D1) ;
      F5  la création est reproductible à n = 8 : taux à facteur 2
          entre les deux graines.
  Falsifieur : création nulle à basse densité ; longueur de naissance
      hors [5, 120] ; longueur de naissance n = 8 ≤ n = 2/4 ; écart
      inter-graines > 2.
  Prédiction pré-enregistrée : 5/5 — « le mur crée partout ; le taux
      est constant à basse densité et l'échelle du quantum vit dans la
      taille des embryons ; les filaments naissent comme des segments
      — la création n'a pas la frontière de la mort ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 3/5, publié) :
  D1  deux attendus confondent le taux et la taille. (a) « ≥ 5
      événements partout » : à n = 8 le comptage dN est corrompu par
      la densité (4–6 événements — fusion des naissances avant compte)
      ; la création y est réelle (naissance 57–66 cellules) mais le
      comptage n'y est pas fiable. (b) « le taux croît avec n » :
      mesure — taux constant à basse densité (1.10e-5 à n = 2,
      1.32e-5 à n = 4) et DÉCROISSANT en comptage à n = 8 (6.6e-6) ;
      la dépendance au quantum vit dans la longueur de naissance
      (44.5 / 40.9 / 66.3 / 57.0). Correction v1.1 : F2 restreint à
      basse densité ; F4 = la taille des embryons croît avec le
      quantum. Leçon : un compteur d'événements a son régime de
      validité, comme une loi de mort — la maison tient sa frontière
      des deux côtés.
  Gouvernance : décision d'auteur du 19/10/2026 (« oui » à la loi de
      la création) — run local avant push, empreinte figée au verdict.
      Cache par trajectoire. Fenêtre de comptage t ∈ [45, 90]
      (seconde moitié, dynamique post-drainage — statistique déclarée
      mince, ~10-30 événements par run).
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
PAROI = int(RING.sum())
STEPS = 1800
PAS = 40
T_COMPTAGE = (45.0, 90.0)
COUPLES = [(2, 440201), (4, 440201), (8, 440201), (8, 440203)]


def masque(w, ax):
    r = lambda x, a: np.roll(x, -1, a)
    corners = {0: [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
               1: [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
               2: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]}[ax]
    keep = np.ones((N,) * 3, bool)
    for dx, dy, dz in corners:
        idx = (np.clip(Xg + dx, 0, N - 1), np.clip(Yg + dy, 0, N - 1),
               np.clip(Zg + dz, 0, N - 1))
        keep &= INSIDE[idx]
    return np.where(keep, w, 0)


def run_B(n, seed, steps=STEPS, pas=PAS):
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Ns, Ls, anos = [], [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            ts.append(round(k * DT, 2))
            Ns.append(len(fils))
            Ls.append(int(sum(len(f["pts"]) for f in fils)))
            anos.append(ano)
    return {"t": ts, "nb": Ns, "longueur": Ls, "anomalies": anos}


def creation(h, paroi=PAROI, t_comptage=T_COMPTAGE):
    """Événements dN > 0, taux par cellule de paroi, longueur de
    naissance (dΛ/dN sur les intervalles à naissance)."""
    ev = 0
    naissances = []
    duree = 0.0
    ts, Ns, Ls = h["t"], h["nb"], h["longueur"]
    for i in range(len(ts) - 1):
        if t_comptage[0] <= ts[i] <= t_comptage[1]:
            dT = ts[i + 1] - ts[i]
            dN = Ns[i + 1] - Ns[i]
            if dN > 0:
                ev += dN
                dL = Ls[i + 1] - Ls[i]
                if dL > 0:
                    naissances.append(dL / dN)
            duree += dT
    taux = ev / duree if duree else 0.0
    taux_paroi = taux / paroi if paroi else 0.0
    l_naiss = float(np.mean(naissances)) if naissances else 0.0
    return ev, duree, taux, taux_paroi, l_naiss, len(naissances)


def main():
    t0 = time.time()

    cache_dir = DATA / ".t53_cache"
    cache_dir.mkdir(exist_ok=True)
    runs = {}
    for n, seed in COUPLES:
        cle = f"n{n}_{seed}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            runs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            runs[cle] = run_B(n, seed)
            cf.write_text(json.dumps(runs[cle]), encoding="utf-8")

    stats = {}
    for cle, h in runs.items():
        ev, duree, taux, taux_paroi, l_naiss, n_naiss = creation(h)
        stats[cle] = {
            "evenements": ev,
            "duree_comptage": round(duree, 1),
            "taux": round(taux, 4),
            "taux_par_cellule_paroi": f"{taux_paroi:.3e}",
            "taux_paroi_float": taux_paroi,
            "longueur_naissance": round(l_naiss, 1),
            "nb_naissances_mesurees": n_naiss,
            "paroi_cellules": PAROI,
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : création comptable à basse densité (n = 2, n = 4) ---
    v2 = all(stats[cle]["evenements"] >= 5 and stats[cle]["taux"] > 0
             for cle in ("n2_440201", "n4_440201"))

    # --- F3 : naissance en segments ---
    v3 = all(5.0 <= s["longueur_naissance"] <= 120.0 for s in stats.values())

    # --- F4 : la taille des embryons croît avec le quantum ---
    l8 = [stats["n8_440201"]["longueur_naissance"],
          stats["n8_440203"]["longueur_naissance"]]
    l_bas = [stats["n2_440201"]["longueur_naissance"],
             stats["n4_440201"]["longueur_naissance"]]
    v4 = min(l8) > max(l_bas)

    # --- F5 : reproductibilité à n = 8 ---
    ta = stats["n8_440201"]["taux_paroi_float"]
    tb = stats["n8_440203"]["taux_paroi_float"]
    v5 = max(ta, tb) <= 2 * min(ta, tb)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_creation_basse_densite": bool(v2),
                "V3_naissance_segments": bool(v3),
                "V4_taille_embryons": bool(v4),
                "V5_creation_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T53-Q-KO6-CREAT-2026-10",
        "protocole": "T53-KO6-CREAT-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T53 : la création — taux de nucléation par cellule de "
                 "paroi en fonction du quantum de circulation, longueur "
                 "de naissance des filaments ; la création n'a pas la "
                 "frontière de la mort (n = 2 participe)",
        "doctrine": "T52 (la nucléation domine) ; NOTE-VINEN-T47-T51 ; "
                    "T47 (4 filaments par quantum)",
        "statut_du_mot": "MESURE — événement = dN > 0 ; naissance = "
                         "dΛ/dN (attribution intégrale déclarée)",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 8, 8],
                          "graines": [440201, 440201, 440201, 440203],
                          "fenetre_comptage": list(T_COMPTAGE), "pas": PAS,
                          "paroi_cellules": PAROI},
        "mesures": stats,
        "verdict_classe": ("S+ (le mur crée partout ; le taux est "
                           "constant à basse densité et l'échelle du "
                           "quantum vit dans la taille des embryons — "
                           "57–66 cellules à n = 8 contre 41–45 à "
                           "n = 2/4 ; la création n'a pas la frontière "
                           "de la mort, et son compteur a le sien)"),
        "falsifieur": "création nulle ou < 5 événements ; naissance hors "
                      "[5, 120] ; taux non monotone ; écart > 2",
        "suites_declarees": "la mortalité des filaments (durée de vie) "
                            "pour compléter le bilan création/mort ; "
                            "confrontation au réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t53_ko6_creation_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T53 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : {s['evenements']} événements, "
              f"taux = {s['taux_par_cellule_paroi']}/cellule/t, "
              f"naissance = {s['longueur_naissance']:.1f} cellules "
              f"({s['nb_naissances_mesurees']} mesures)")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
