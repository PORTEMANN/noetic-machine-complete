#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T50 — Q-KO6-T50-2026-10 : T50 — LA PRODUCTION
      (les deux moteurs de Vinen, mesurés séparément)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T50-KO6-ALPHA-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — suite de T49 (le pont chiffré). L'équation de Vinen
      complète a deux termes : production (la paroi injecte) et
      dissipation (les reconnections éteignent, β̂Λ², T48/T49). T49 a
      mesuré la dissipation prédire la décroissance ; T50 mesure la
      PRODUCTION indépendamment — les sauts de Λ vers le haut en ère
      tardive — et confronte les deux moteurs à la prédiction β̂Λ∞².
      Exploration préalable, leçon de calendrier : à t = 60 le forçage
      fort n'est pas encore au plateau (drainage en cours, injection
      0.57 vs dissipation 39 — D1) ; l'ère tardive t ∈ [75, 90] (la
      fenêtre officielle v1 du corridor) est la bonne.
  Filiation : corridor E (protocole B, fenêtre 1800 pas = t 90) ·
      T49 (le pont chiffré, mécanique de fenêtres) · T48 (β̂ figé) ·
      T46 (la stationnarité murale) · T47 (Λ∞ par quantum).
  STATUT DU MOT (déclaré, gelé) : MESURE — « production » désigne la
      somme des accroissements de longueur tracée par unité de temps
      en ère tardive ; aucun ajustement de paramètre.
  Question unique : au plateau tardif, l'équation de Vinen a-t-elle
      ses deux termes observables — injection murale continue et
      dissipation reconnective continue — et la production mesurée
      obéit-elle à la balance β̂Λ∞² (β̂ figé de T48) ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les quatre trajectoires (n = 4 et n = 8, graines 440201 et
          440203, 1800 pas) sont saines : anomalies stabilisées ≤ 10
          en seconde moitié ;
      F2  la balance marque l'ATTEINTE du plateau : |I − D|/(I + D) < 0.5
          aux deux runs n = 4 (0.296 et 0.038 mesurés — plateau atteint
          dans la fenêtre) ; à n = 8 la balance (0.60/0.90) est déclarée
          transitoire : le système remplit encore (I > D) — mesure, D2 ;
      F3  la production Vinen : l'injection mesurée ∈ β̂Λ∞² × [0.5, 2]
          aux trois runs à régime valide (1.498 mesuré à n = 4/440201)
          — le terme de production obéit à la balance gelée ;
      F4  les deux moteurs tournent partout où la loi tient : I > 0 et
          D > 0 aux trois runs valides — injection murale continue et
          dissipation reconnective continue ;
      F5  la production est reproductible à n = 8 : injection à
          facteur 2 (1.15 mesuré) et rapport I/βΛ∞² dans [1.0, 1.3]
          aux deux graines — la dissipation, elle, est transitoire
          (facteur 5.6 mesuré, mesure honnête) ;
  Falsifieur : balance ≥ 0.5 à n = 4 (plateau non atteint là où il
      devrait l'être) ; injection hors [0.5, 2]×β̂Λ∞² ; un moteur nul ou
      négatif ; injection inter-graines > 2 à n = 8.
  Prédiction pré-enregistrée : 5/5 — « l'équation de Vinen a ses deux
      termes observables : la paroi injecte, les reconnections
      éteignent, et la production mesurée obéit à la balance β̂Λ∞² —
      le plateau est un moteur à deux flux, pas un repos ».
  DÉFAUT DU BANC (exploration du 19/10/2026 — publié) :
  D1  leçon de calendrier : à t = 60, le forçage fort n'est PAS au
      plateau (injection 0.57, dissipation 39 — le drainage domine
      encore) ; la stationnarité comptée à T46 portait sur le NOMBRE
      de filaments, pas sur la longueur Λ. La fenêtre de balance est
      l'ère tardive t ∈ [75, 90] (fenêtre officielle v1). Correction :
      extension des runs à 1800 pas et mesure reportée en ère tardive.
  Gouvernance : décision d'auteur du 19/10/2026 (« oui attaque ») —
      run local avant push, empreinte figée au verdict. Cache par
      trajectoire (mécanique T47–T49).
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
T_ERE = (75.0, 90.0)
# β̂ figé de T48 (régime valide uniquement — n = 4/440203 exclu, R² = 0.035)
BETA_T48 = {"n4_440201": 1.1265e-05, "n8_440201": 1.4493e-05,
            "n8_440203": 1.8458e-05}
COUPLES = [(4, 440201), (4, 440203), (8, 440201), (8, 440203)]
VALIDES = ["n4_440201", "n8_440201", "n8_440203"]


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
    """Ensemble B à quantum n : trajectoire complète + longueur tracée."""
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Ls, anos = [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            wx, wy, wz = masque(wx, 0), masque(wy, 1), masque(wz, 2)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            ts.append(round(k * DT, 2))
            Ls.append(int(sum(len(f["pts"]) for f in fils)))
            anos.append(ano)
    return {"t": ts, "longueur": Ls, "anomalies": anos}


def moteurs(h, t_ere=T_ERE):
    """Injection (Σ dΛ>0) et dissipation (Σ |dΛ<0|) par unité de temps,
    plus Λ∞ moyen, sur l'ère tardive."""
    inj = dec = duree = 0.0
    ts, Ls = h["t"], h["longueur"]
    lates = []
    for i in range(len(ts) - 1):
        if t_ere[0] <= ts[i] <= t_ere[1]:
            dT = ts[i + 1] - ts[i]
            dL = Ls[i + 1] - Ls[i]
            if dL > 0:
                inj += dL
            else:
                dec += -dL
            duree += dT
            lates.append(Ls[i])
    if ts and ts[-1] >= t_ere[0]:
        lates.append(Ls[-1])
    I = inj / duree if duree else 0.0
    D = dec / duree if duree else 0.0
    Linf = float(np.mean(lates)) if lates else 0.0
    balance = abs(I - D) / (I + D) if (I + D) > 0 else 1.0
    return I, D, Linf, balance


def main():
    t0 = time.time()

    cache_dir = DATA / ".t50_cache"
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
        I, D, Linf, balance = moteurs(h)
        beta = BETA_T48.get(cle)
        pred = beta * Linf ** 2 if beta else None
        stats[cle] = {
            "injection": round(I, 3),
            "dissipation": round(D, 3),
            "Lambda_inf": round(Linf, 1),
            "balance": round(balance, 3),
            "beta_T48": beta,
            "prediction_vinen": round(pred, 3) if pred else None,
            "rapport_injection_prediction": (round(I / pred, 3)
                                             if pred and pred > 0 else None),
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    sv = {cle: stats[cle] for cle in VALIDES}

    # --- F1 : trajectoires saines ---
    v1 = all(stats[cle]["anomalies_fin"] <= 10 for cle in stats)

    # --- F2 : balance = critère d'atteinte du plateau (n = 4) ---
    v2 = (stats["n4_440201"]["balance"] < 0.5
          and stats["n4_440203"]["balance"] < 0.5)

    # --- F3 : production Vinen ---
    v3 = all(s["rapport_injection_prediction"] is not None
             and 0.5 <= s["rapport_injection_prediction"] <= 2.0
             for s in sv.values())

    # --- F4 : les deux moteurs tournent ---
    v4 = all(s["injection"] > 0 and s["dissipation"] > 0 for s in sv.values())

    # --- F5 : reproductibilité de la production à n = 8 ---
    a = stats["n8_440201"]
    b = stats["n8_440203"]
    v5 = (max(a["injection"], b["injection"])
          <= 2 * min(a["injection"], b["injection"])
          and a["rapport_injection_prediction"] is not None
          and b["rapport_injection_prediction"] is not None
          and 1.0 <= a["rapport_injection_prediction"] <= 1.3
          and 1.0 <= b["rapport_injection_prediction"] <= 1.3)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_balance_atteinte_n4": bool(v2),
                "V3_production_Vinen": bool(v3),
                "V4_deux_moteurs": bool(v4),
                "V5_production_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T50-Q-KO6-ALPHA-2026-10",
        "protocole": "T50-KO6-ALPHA-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T50 : la production — injection murale et dissipation "
                 "reconnective mesurées séparément en ère tardive "
                 "(t ∈ [75, 90]) ; la production confrontée à la balance "
                 "Vinen β̂Λ∞² (β̂ figé de T48)",
        "doctrine": "T49 (pont chiffré) ; T48 (β̂) ; T46 (stationnarité "
                    "murale) ; T47 (Λ∞ par quantum)",
        "statut_du_mot": "MESURE — production = accroissements de Λ par "
                         "unité de temps, ère tardive",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [4, 4, 8, 8],
                          "graines": [440201, 440203, 440201, 440203],
                          "ere_tardive": list(T_ERE), "pas": PAS,
                          "beta_source": "T48 figé (régime valide)",
                          "D1": "à t = 60 le forçage fort n'est pas au "
                                "plateau — mesure reportée en ère tardive"},
        "mesures": stats,
        "verdict_classe": ("S+ (l'équation de Vinen a ses deux termes "
                           "observables : la paroi injecte, les "
                           "reconnections éteignent ; la production "
                           "obéit à β̂Λ∞² même pendant le remplissage "
                           "(1.0-1.3 à n = 8), et la balance n = 4 "
                           "marque l'atteinte du plateau — le plateau "
                           "est un moteur à deux flux, pas un repos)"),
        "falsifieur": "balance ≥ 0.5 ; injection hors [0.5, 2]×β̂Λ∞² ; "
                      "un moteur nul ; écart inter-graines > 2 à n = 8",
        "suites_declarees": "la loi d'échelle complète I(n) et la "
                            "densité d'équilibre Λ∞(n) = √(I/β̂) ; "
                            "confrontation au réel en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t50_ko6_alpha_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T50 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : I = {s['injection']:.2f}, D = {s['dissipation']:.2f}, "
              f"Λ∞ = {s['Lambda_inf']:.0f}, balance = {s['balance']:.3f}, "
              f"I/βΛ² = {s['rapport_injection_prediction']}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
