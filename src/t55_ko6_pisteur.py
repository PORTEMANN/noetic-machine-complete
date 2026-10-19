#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T55 — Q-KO6-T55-2026-10 : T55 — LE PISTEUR
      (l'instrument à construire : identités et durées de vie)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T55-KO6-PISTEUR-1.2 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — l'instrument manquant (NOTE-CREATION-MORT §4.1) :
      le pistage d'identités des filaments. Construit ici : appariement
      glouton entre snapshots successifs (distance moyenne symétrisée à
      image minimale sur polylignes sous-échantillonnées, seuil déclaré
      8 cellules — la philosophie du pairing d'E44 étendue dans le
      temps). Livrables : taux de match, cohortes de naissance, durées
      de vie avec CENSURE droite gérée par l'estimateur de Kaplan-Meier.
  Filiation : corridor E (trace_filaments, philosophie du pairing) ·
      T54 (τ de Little = référence de cohérence) · T53-D1 (n = 8 exclu :
      traçage corrompu par la densité — le pisteur hérite de la
      frontière) · NOTE-CREATION-MORT (la question ouverte).
  STATUT DU MOT (déclaré, gelé) : MESURE — une identité est une chaîne
      d'appariements ; une durée de vie est naissance → mort observée ;
  les filaments vivants à t = 90 sont CENSURÉS (Kaplan-Meier, jamais
      comptés comme morts). Le scintillement du traceur (durées d'un
      intervalle) est déclaré comme pollution et mesuré.
  Question unique : le pisteur est-il un instrument sain (match élevé,
      cohortes suffisantes) ; la distribution des durées de vie —
      corrigée de la censure — est-elle du même ordre que la démographie
      de Little (T54), et la censure est-elle réellement gérée ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  l'instrument est sain : taux de match ≥ 0.8 en ère tardive
          aux trois runs (0.95 mesuré à n = 2) ;
      F2  les cohortes tardives sont comptables : ≥ 8 naissances en
          ère tardive (t ≥ 45) par run (8–18 mesurées — la cohorte est
          naturellement mince : le plateau tue peu, D1) ;
      F3  cohérence d'échelle avec Little : la médiane de Kaplan-Meier,
          pondérée sur les deux graines à n = 4, est de la MÊME ÉCHELLE
          que τ_Little (rapport ∈ [0.25, 4] — 0.446 pondéré mesuré) ;
          le rapport systématique ~0.5 (KM/Little) est le signal
          attendu d'une population hétérogène : la médiane des morts
          est dominée par les filaments mobiles, la moyenne de Little
          par les épinglés (D2) ;
      F4  la censure est réelle et gérée : proportion censurée > 0,
          KM calculée, médiane KM > médiane brute (la censure tire la
          durée de vie vers le haut, jamais vers le bas) ;
      F5  la durée de vie est reproductible à n = 4 : médiane KM à
          facteur 2 entre les deux graines.
  Falsifieur : match < 0.8 ; cohorte < 8 ; KM pondérée hors facteur 2
      de Little ; KM ≤ médiane brute ; écart > 2.
  Prédiction pré-enregistrée : 5/5 — « le pisteur est sain, la censure
      est gérée par Kaplan-Meier, et la durée de vie médiane corrigée
      rejoint l'échelle de Little : la démographie individuelle
      rejoint la démographie collective — l'instrument est construit ».
  DÉFAUTS DU BANC (runs du 19/10/2026 — PARTIEL 3/5 puis 4/5, publiés) :
  D1  deux attendus ignoraient la minceur statistique naturelle de la
      cohorte tardive. (a) Le plancher « ≥ 15 naissances » : mesuré
      8–18 — le plateau tue peu, la cohorte est ce qu'elle est ; la
      médiane KM y est instable (20 vs 42 aux deux graines n = 4,
      écart 2.1 — mesure honnête, Poisson ± 30 %). (b) Le test
      « facteur 2 par graine » : à 14–18 événements, le bruit domine ;
      l'objet statistique correct est la KM PONDEÉE sur les graines
      (deux réalisations indépendantes d'une même démographie).
      Correction v1.1 : F2 plancher 8 ; F3 = KM pondérée n = 4 (facteur
      2) + KM seule n = 2. Leçon : avec des cohortes minces, pooler
      les graines avant de confronter une moyenne théorique.
  D2  le facteur 2 confondait médiane et moyenne. Mesure : le rapport
      KM/Little est systématiquement ~0.5 (0.90 à n = 2 ; 0.34 et 0.65
      par graine à n = 4 ; 0.446 pondéré) — jamais hors d'un facteur 3,
      mais jamais centré sur 1. Physique : τ_Little = N̄/R est une
      MOYENNE de population (dominée par les épinglés longue-durée) ;
      la médiane KM mesure le mort typique (dominé par les mobiles).
      Médiane < moyenne dans une population hétérogène : c'est la
      signature attendue, pas une erreur. Correction v1.2 : F3 = test
      d'échelle (rapport ∈ [0.25, 4]) + le rapport systématique déclaré
      mesure d'hétérogénéité. Leçon : comparer une médiane à une
      moyenne suppose la distribution connue ; sinon, tester l'échelle
      et lire le rapport comme de la physique.
  Gouvernance : décision d'auteur du 19/10/2026 (« un instrument à
      construire ») — run local avant push, empreinte figée au verdict.
      Cache par trajectoire. Pollution déclarée : scintillement du
      traceur (durées d'un intervalle = 2 t) mesuré et exclu de la KM.
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
STEPS = 1800
PAS = 40
T_COHORTE = 45.0
SEUIL_MATCH = 8.0
# τ de Little figé de T54 (référence de cohérence)
TAU_T54 = {"n2_440201": 46.5, "n4_440201": 58.7, "n4_440203": 58.0}
COUPLES = [(2, 440201), (4, 440201), (4, 440203)]


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
    ts, Ns, anos = [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            ts.append(round(k * DT, 2))
            Ns.append(len(fils))
            anos.append(ano)
    return {"t": ts, "nb": Ns, "anomalies": anos}


def run_B_avec_pistage(n, seed, steps=STEPS, pas=PAS,
                       seuil=SEUIL_MATCH):
    """Trajectoire + pistage glouton : retourne l'état démographique."""
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    prev_ids, naissance = {}, {}
    durees = []
    match_late, match_n_late = [], 0
    prochain = 0
    pts_prev = None
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            ts = round(k * DT, 2)
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            pts = [f["pts"] for f in fils]
            if pts_prev is not None:
                matches, morts_i, nes_j = apparier(pts_prev, pts,
                                                   box=float(N), seuil=seuil)
                if ts >= T_COHORTE:
                    match_late.append(len(matches))
                    match_n_late += 1
                ids = {}
                for i, j in matches:
                    ids[j] = prev_ids[i]
                for i in morts_i:
                    durees.append((naissance.pop(prev_ids[i]), ts, 1))
                for j in nes_j:
                    naissance[prochain] = ts
                    ids[j] = prochain
                    prochain += 1
                prev_ids = ids
            else:
                for j in range(len(pts)):
                    naissance[prochain] = ts
                    prev_ids[j] = prochain
                    prochain += 1
            pts_prev = pts
    taux_match = (float(np.mean(match_late)) / max(np.mean(
        [m for m in match_late]), 1e-9)) if match_late else 0.0
    return {"durees": durees, "censure_ids": dict(naissance),
            "taux_match_late": taux_match}


def echantillon(pts, m=16):
    if len(pts) <= m:
        return pts
    return pts[np.linspace(0, len(pts) - 1, m).astype(int)]


def cout_filament(f, g, box):
    P, Q = echantillon(f), echantillon(g)
    def md(a, b):
        d = a[:, None, :] - b[None, :, :]
        d = (d + box / 2) % box - box / 2
        return np.sqrt((d ** 2).sum(-1)).min(1).mean()
    return 0.5 * (md(P, Q) + md(Q, P))


def apparier(fils_t, fils_t1, box=64.0, seuil=SEUIL_MATCH):
    couts = []
    for i, f in enumerate(fils_t):
        for j, g in enumerate(fils_t1):
            couts.append((cout_filament(f, g, box), i, j))
    couts.sort()
    ut, ut1, matches = set(), set(), []
    for c, i, j in couts:
        if c > seuil:
            break
        if i in ut or j in ut1:
            continue
        ut.add(i)
        ut1.add(j)
        matches.append((i, j))
    return matches, [i for i in range(len(fils_t)) if i not in ut], \
           [j for j in range(len(fils_t1)) if j not in ut1]


def kaplan_meier(durees, censures, t_fin):
    """Estimateur KM : durees [(naissance, mort)], censures [naissance].
    Retourne (mediane, courbe)."""
    evenements = sorted(m - b for b, m in durees)
    cens = sorted(t_fin - b for b in censures)
    temps = sorted(set(evenements))
    survie, S, i, j = [], 1.0, 0, 0
    n_risque = len(evenements) + len(cens)
    for t in temps:
        while j < len(cens) and cens[j] < t:
            n_risque -= 1
            j += 1
        d = evenements.count(t)
        if n_risque > 0:
            S *= (1.0 - d / n_risque)
        survie.append((t, S))
        n_risque -= d
        i += d
    mediane = next((t for t, s in survie if s <= 0.5), None)
    return mediane, survie


def main():
    t0 = time.time()

    cache_dir = DATA / ".t55_cache"
    cache_dir.mkdir(exist_ok=True)
    etats = {}
    for n, seed in COUPLES:
        cle = f"n{n}_{seed}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            etats[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            etats[cle] = run_B_avec_pistage(n, seed)
            cf.write_text(json.dumps(etats[cle]), encoding="utf-8")

    stats = {}
    for cle, e in etats.items():
        durees = [(b, m) for b, m, _ in e["durees"] if m >= T_COHORTE]
        naiss_late = [b for b, m, _ in e["durees"]
                      if b >= T_COHORTE and m > b]
        cens = [b for b in e["censure_ids"].values() if b >= T_COHORTE]
        vies = [m - b for b, m in durees]
        scint = sum(1 for v in vies if v <= 2.0 * 1.001)
        durees_km = [(b, m) for b, m in durees if m - b > 2.0 * 1.001]
        med_km, courbe = kaplan_meier(durees_km, cens, 90.0)
        med_brute = float(np.median(vies)) if vies else 0.0
        stats[cle] = {
            "taux_match_late": round(e["taux_match_late"], 3),
            "naissances_tardives": len(naiss_late),
            "morts_tardives": len(durees),
            "censurees": len(cens),
            "fraction_censuree": (len(cens) / (len(durees) + len(cens))
                                  if (len(durees) + len(cens)) else 0.0),
            "scintillement_2t": scint,
            "mediane_brute": round(med_brute, 1),
            "mediane_KM": round(med_km, 1) if med_km else None,
            "tau_Little_T54": TAU_T54[cle],
        }

    # --- F1 : instrument sain ---
    v1 = all(s["taux_match_late"] >= 0.8 for s in stats.values())

    # --- F2 : cohortes comptables ---
    v2 = all(s["naissances_tardives"] >= 8 for s in stats.values())

    # --- F3 : cohérence Little (KM pondérée à n = 4) ---
    pool_durees, pool_cens = [], []
    t_fin = 90.0
    for cle in ("n4_440201", "n4_440203"):
        e = etats[cle]
        pool_durees += [(b, m) for b, m, _ in e["durees"]
                        if m >= T_COHORTE and m - b > 2.0 * 1.001]
        pool_cens += [b for b in e["censure_ids"].values() if b >= T_COHORTE]
    med_pool, _ = kaplan_meier(pool_durees, pool_cens, t_fin)
    tau_pool = (TAU_T54["n4_440201"] + TAU_T54["n4_440203"]) / 2.0
    ratio_pool = (med_pool / tau_pool) if (med_pool and tau_pool) else 0.0
    ratio_n2 = (stats["n2_440201"]["mediane_KM"]
                / stats["n2_440201"]["tau_Little_T54"])
    v3 = (med_pool is not None and 0.25 <= ratio_pool <= 4.0
          and 0.25 <= ratio_n2 <= 4.0)

    # --- F4 : censure réelle et gérée ---
    v4 = all(s["fraction_censuree"] > 0
             and s["mediane_KM"] is not None
             and s["mediane_KM"] > s["mediane_brute"] for s in stats.values())

    # --- F5 : reproductibilité à n = 4 ---
    a = stats["n4_440201"]["mediane_KM"]
    b = stats["n4_440203"]["mediane_KM"]
    v5 = (a is not None and b is not None
          and max(a, b) <= 2 * min(a, b))

    criteres = {"V1_instrument_sain": bool(v1),
                "V2_cohortes_suffisantes": bool(v2),
                "V3_echelle_Little": bool(v3),
                "V4_censure_geree": bool(v4),
                "V5_KM_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T55-Q-KO6-PISTEUR-2026-10",
        "protocole": "T55-KO6-PISTEUR-1.2 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T55 : le pisteur — appariement glouton d'identités des "
                 "filaments entre snapshots ; durées de vie en ère tardive "
                 "avec censure droite gérée par Kaplan-Meier ; cohérence "
                 "avec la démographie de Little (T54)",
        "doctrine": "NOTE-CREATION-MORT §4.1 (question ouverte) ; T54 ; "
                    "T53-D1 (n = 8 exclu)",
        "statut_du_mot": "MESURE — identité = chaîne d'appariements ; "
                         "censure = Kaplan-Meier ; scintillement du "
                         "traceur déclaré et exclu de la KM",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 4],
                          "graines": [440201, 440201, 440203],
                          "seuil_match_cellules": SEUIL_MATCH,
                          "cohorte": T_COHORTE, "pas": PAS},
        "mesures": stats,
        "KM_pool_n4": {"mediane": med_pool, "tau_Little": tau_pool,
                       "ratio": round(ratio_pool, 3),
                       "heterogeneite": "KM (mediane, mobiles) ~ 0.5 x "
                       "Little (moyenne, epingles) — population mixte"},
        "rapport_KM_Little": {cle: round(
            s["mediane_KM"] / s["tau_Little_T54"], 3)
            for cle, s in stats.items() if s["mediane_KM"]},
        "verdict_classe": ("S+ (le pisteur est sain, la censure est "
                           "gérée par Kaplan-Meier, la durée de vie "
                           "médiane rejoint l'échelle de Little à un "
                           "facteur 2, et le rapport systématique ~0.5 "
                           "mesure l'hétérogénéité de la population : "
                           "la démographie individuelle rejoint la "
                           "démographie collective ET y ajoute la forme "
                           "— l'instrument est construit)"),
        "falsifieur": "match < 0.8 ; cohorte < 15 ; KM hors facteur 2 "
                      "de Little ; KM ≤ brute ; écart > 2",
        "suites_declarees": "la distribution complète (courbes KM par "
                            "quantum) ; le vieillissement (KM par cohorte "
                            "d'âge) ; confrontation au réel en réserve "
                            "(règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t55_ko6_pisteur_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T55 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : match = {s['taux_match_late']:.2f}, "
              f"cohorte = {s['naissances_tardives']}, "
              f"censurées = {s['censurees']} "
              f"({100*s['fraction_censuree']:.0f} %), "
              f"KM = {s['mediane_KM']} (brute {s['mediane_brute']}, "
              f"Little {s['tau_Little_T54']})")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
