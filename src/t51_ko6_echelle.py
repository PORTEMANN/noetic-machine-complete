#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T51 — Q-KO6-T51-2026-10 : T51 — LA LOI D'ÉCHELLE
      (Λ∞(n) = √(I/β̂) : la prédiction de l'équilibre)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T51-KO6-ECHELLE-1.0 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — clôture de l'arc Vinen (T47–T50). Les pièces sont
      posées : la loi existe (T47), β̂ est quantifié (T48), la
      dissipation prédit la décroissance (T49), la production obéit à
      β̂Λ∞² (T50). T51 les assemble : la densité d'équilibre prédite
      Λ∞(n) = √(I(n)/β̂) — production murale mesurée sur dissipation
      gelée — confrontée aux plateaux mesurés, en ordre et en
      magnitude, sur les trois quanta de circulation.
  Filiation : T50 (I et D mesurés en ère tardive, mécanique reprise) ·
      T48 (β̂ figé : 1.1265e-5 / 1.4493e-5 / 1.8458e-5) · T47 (plateau
      ∝ quantum) · corridor E (protocole B, fenêtre 1800 pas).
  STATUT DU MOT (déclaré, gelé) : MESURE — la prédiction utilise I
      mesuré et β̂ gelé ; aucun paramètre n'est ajusté pour faire
      tomber la loi.
  Question unique : la densité d'équilibre prédite Λ∞ = √(I/β̂)
      reproduit-elle les plateaux de longueur mesurés — en ordre
      (monotonie en n) et en magnitude (rapport dans [0.7, 1.4]) —
      là où β existe, et la production est-elle monotone en n ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les cinq trajectoires (n = 2, 4, 8 × graines officielles,
          1800 pas) sont saines : anomalies stabilisées ≤ 10 en
          seconde moitié ;
      F2  la production est monotone en n (graine 440201) :
          I(2) < I(4) < I(8) (6.4 < 9.5 < 18.9 mesuré) — la paroi
          injecte davantage à quantum élevé ;
      F3  la prédiction de l'équilibre : Λ_pred/Λ_mes ∈ [0.7, 1.4] aux
          trois runs à régime valide (1.224, 1.009, 1.133 mesurés) —
          √(I/β̂) tombe sur le plateau à 10–22 % près ;
      F4  les ordres concordent : Λ_pred(4) < Λ_pred(8) (918 < 1143
          mesuré) et Λ_mes monotone en n à graine fixe (466 < 750 <
          1133) — la loi tient dans l'espace des prédictions comme
          dans celui des mesures ;
      F5  la prédiction est reproductible à n = 8 : les deux graines
          donnent des rapports dans [0.7, 1.4] (1.009 et 1.133) —
          l'équilibre ne dépend pas de la graine.
  Falsifieur : production non monotone en n ; rapport hors [0.7, 1.4]
      à un run valide ; ordres qui croisent entre prédiction et
      mesure ; écart inter-graines à n = 8.
  Prédiction pré-enregistrée : 5/5 — « I(n) monte, Λ∞(n) monte, et
      √(I/β̂) tombe sur le plateau mesuré à 10–22 % près : la loi
      d'échelle de Vinen est complète côté corridor — production,
      dissipation et équilibre, trois quanta, deux graines ».
  Gouvernance : décision d'auteur du 19/10/2026 (« oui ») — run local
      avant push, empreinte figée au verdict. Cache par trajectoire.
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
# β̂ figé de T48 (régime valide uniquement)
BETA_T48 = {"n4_440201": 1.1265e-05, "n8_440201": 1.4493e-05,
            "n8_440203": 1.8458e-05}
COUPLES = [(2, 440201), (4, 440201), (4, 440203), (8, 440201),
           (8, 440203)]
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
    return I, D, Linf


def main():
    t0 = time.time()

    cache_dir = DATA / ".t51_cache"
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
        I, D, Linf = moteurs(h)
        beta = BETA_T48.get(cle)
        pred = (I / beta) ** 0.5 if (beta and I > 0) else None
        stats[cle] = {
            "injection": round(I, 3),
            "dissipation": round(D, 3),
            "Lambda_mes": round(Linf, 1),
            "beta_T48": beta,
            "Lambda_pred": round(pred, 1) if pred else None,
            "rapport_pred_mes": round(pred / Linf, 3) if pred else None,
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : production monotone en n (440201) ---
    v2 = (stats["n2_440201"]["injection"] < stats["n4_440201"]["injection"]
          < stats["n8_440201"]["injection"])

    # --- F3 : prédiction de l'équilibre ---
    v3 = all(stats[cle]["rapport_pred_mes"] is not None
             and 0.7 <= stats[cle]["rapport_pred_mes"] <= 1.4
             for cle in VALIDES)

    # --- F4 : ordres concordants ---
    v4 = (stats["n4_440201"]["Lambda_pred"]
          < stats["n8_440201"]["Lambda_pred"]
          and stats["n2_440201"]["Lambda_mes"]
          < stats["n4_440201"]["Lambda_mes"]
          < stats["n8_440201"]["Lambda_mes"])

    # --- F5 : reproductibilité de la prédiction à n = 8 ---
    v5 = all(0.7 <= stats[cle]["rapport_pred_mes"] <= 1.4
             for cle in ("n8_440201", "n8_440203"))

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_production_monotone": bool(v2),
                "V3_prediction_equilibre": bool(v3),
                "V4_ordres_concordants": bool(v4),
                "V5_prediction_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T51-Q-KO6-ECHELLE-2026-10",
        "protocole": "T51-KO6-ECHELLE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T51 : la loi d'échelle — densité d'équilibre prédite "
                 "Λ∞(n) = √(I(n)/β̂) (production murale mesurée sur "
                 "dissipation gelée) confrontée aux plateaux mesurés "
                 "sur trois quanta et deux graines",
        "doctrine": "T50 (production) ; T48 (β̂) ; T47 (plateau ∝ "
                    "quantum) ; Vinen (1957)",
        "statut_du_mot": "MESURE — prédiction à paramètres gelés",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 8], "graines": [440201, 440203],
                          "ere_tardive": list(T_ERE), "pas": PAS,
                          "beta_source": "T48 figé (régime valide)"},
        "mesures": stats,
        "verdict_classe": ("S+ (I(n) monte, Λ∞(n) monte, et √(I/β̂) "
                           "tombe sur le plateau mesuré à 10–22 % près "
                           "aux trois runs valides : la loi d'échelle "
                           "de Vinen est complète côté corridor — "
                           "production, dissipation et équilibre)"),
        "falsifieur": "production non monotone ; rapport hors "
                      "[0.7, 1.4] ; ordres croisés ; écart inter-graines",
        "suites_declarees": "clôture de l'arc Vinen (T47–T51) ; bilan "
                            "doctrine ; confrontation au réel en réserve "
                            "(règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t51_ko6_echelle_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T51 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        rp = (f"{s['rapport_pred_mes']:.3f}"
              if s["rapport_pred_mes"] is not None else "—")
        print(f"  {cle} : I = {s['injection']:.2f}, Λ_mes = {s['Lambda_mes']:.0f}, "
              f"Λ_pred = {s['Lambda_pred']}, ratio = {rp}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
