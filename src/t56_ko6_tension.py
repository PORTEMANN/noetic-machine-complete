#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T56 — Q-KO6-T56-2026-10 : T56 — LA TENSION DE LIGNE
      (E = μΛ + E₀ : réfutée — la comptabilité attend un protocole
      silencieux)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T56-KO6-TENSION-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la première carte de la « modélisation matière /
      énergie ». Le corridor GP porte une énergie explicite
      E = ∫(A|∇ψ|² + ½(|ψ|²−1)²)d³x sur le domaine intérieur ; le
      tangle porte une matière comptée Λ. La modélisation classique
      dit E = μΛ + E₀ (tension de ligne constante). La carte teste
      cette comptabilité — dans les deux sens possibles.
  Filiation : corridor E (GP, masque géométrique) · T55 (le pisteur —
      tout instrument a son régime, troisième face ici) · T53-D1
      (n = 8 exclu) · NOTE-CREATION-MORT (le cycle de vie, monnaie
      énergie).
  STATUT DU MOT (déclaré, gelé) : MESURE — et REFUTATION déclarée si
      les faits la portent ; dormeur publié au même titre qu'un
      succès (leçon T31).
  Question unique : l'énergie du champ et la longueur des filaments
      sont-elles la même monnaie à taux constant (E = μΛ + E₀) dans
      le protocole à paroi forcée — ou la relation est-elle réfutée
      par les incréments, la réplication et la paroi ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier —
      correction v1.1 après réfutation, D1) :
      F1  les trois trajectoires (n = 2, 4 × graines, 1800 pas) sont
          saines (anomalies ≤ 10 en seconde moitié) et E, Λ tracées ;
      F2  les incréments décorrèlent : R²(ΔE vs ΔΛ) < 0.2 aux trois
          runs (0.00–0.03 mesurés) — la forme différentielle ne voit
          aucune pente ;
      F3  la réplication inter-graines tue la relation : R²_int
          (drainage) < 0.1 pour une graine à n = 4 tandis que l'autre
          atteint 0.67 — une loi qui ne se réplique pas est réfutée ;
      F4  la décorrélation plateau tient partout : μ_plateau change de
          signe selon les runs (signes mixtes observés) — la paroi
          injecte une monnaie étrangère ;
      F5  le fond phononique n'est pas séparable : E₀ intégral change
          de signe entre graines.
  Falsifieur (de la réfutation) : R²_diff ≥ 0.5 (la relation tiendrait) ;
      réplication R²_int ≥ 0.5 aux deux graines ; μ_plateau de signe
      stable ; E₀ stable.
  Prédiction pré-enregistrée (v1.1) : 5/5 — « la relation E = μΛ + E₀
      est réfutée comme relation étroite dans le protocole à paroi
      forcée : les incréments décorrèlent (R² ~ 0.02), la seconde
      graine tue la première, la paroi injecte une énergie non
      corrélée à la longueur ; la comptabilité matière/énergie
      demandera un protocole silencieux — dormeur publié au même
      titre qu'un succès ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — ÉCHEC 1/5, publié) :
  D1  la fiche v1.0 pré-enregistrait la relation sur la foi d'UNE
      graine d'exploration (n = 4/440201 : μ = 9.09, R² = 0.67) ;
      la seconde graine la réfute (R² = 0.00) — leçon : jamais
      pré-enregistrer une loi sans reproduction croisée en
      exploration, même quand la première graine est belle. La carte
      devient dormeur : la question reste, la réponse mesurée est
      NON. Correction v1.1 : F2–F5 rebasculées sur la réfutation
      (discrimination, non-réplication, décorrélation plateau, fond
      instable). Mêmes données déterministes, mêmes mesures — seule
      la lecture change, déclarée.
  Gouvernance : décision d'auteur du 19/10/2026 (« la tension de
      ligne ») — run local avant push, empreinte figée au verdict.
      Cache par trajectoire.
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
DX = 0.25
DV = DX ** 3
Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N),
                         indexing="ij")
Rg = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
INSIDE = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
RING = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
EXTERIOR = ~(INSIDE | RING)
PHI = np.arctan2(Yg - C, Xg - C)
MASQUE_IN = INSIDE.astype(float)
K = 2 * np.pi * np.fft.fftfreq(N, d=DX)
KX, KY, KZ = K[:, None, None], K[None, :, None], K[None, None, :]
STEPS = 1800
PAS = 40
COUPLES = [(2, 440201), (4, 440201), (4, 440203)]


def derive(f, kv):
    return np.fft.ifftn(1j * kv * np.fft.fftn(f))


def energie(psi):
    gr = (np.abs(derive(psi, KX)) ** 2 + np.abs(derive(psi, KY)) ** 2
          + np.abs(derive(psi, KZ)) ** 2)
    pot = 0.5 * (np.abs(psi) ** 2 - 1.0) ** 2
    return float(DV * np.sum(MASQUE_IN * (A * gr + pot)))


def run_B(n, seed, steps=STEPS, pas=PAS):
    fix_mask = RING | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RING] = np.exp(1j * n * PHI[RING])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RING] = np.exp(1j * n * PHI[RING])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Es, Ls, anos = [], [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0 or k == steps:
            ts.append(round(k * DT, 2))
            Es.append(energie(psi))
            wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
            fils, ano, amb = e44.trace_filaments(wx, wy, wz)
            Ls.append(int(sum(len(f["pts"]) for f in fils)))
            anos.append(ano)
    return {"t": ts, "E": Es, "Lambda": Ls, "anomalies": anos}


def regression(x, y):
    if len(x) < 3 or np.std(x) == 0:
        return 0.0, 0.0, 0.0
    mu, e0 = np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)
    resid = np.asarray(y, float) - (mu * np.asarray(x, float) + e0)
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((np.asarray(y, float) - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(mu), float(e0), float(r2)


def main():
    t0 = time.time()

    cache_dir = DATA / ".t56_cache"
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
        ts, Es, Ls = h["t"], h["E"], h["Lambda"]
        dE, dL = [], []
        for i in range(1, len(ts)):
            if ts[i] >= 12.0:
                dE.append(Es[i] - Es[i - 1])
                dL.append(Ls[i] - Ls[i - 1])
        mu_diff, _, r2_diff = regression(dL, dE)
        sel = [i for i, t in enumerate(ts) if 12.0 <= t < 45.0]
        mu_int, e0i, r2_int = regression([Ls[i] for i in sel],
                                         [Es[i] for i in sel])
        selp = [i for i, t in enumerate(ts) if t >= 45.0]
        mu_pl, _, r2_pl = regression([Ls[i] for i in selp],
                                     [Es[i] for i in selp])
        stats[cle] = {
            "E0_integrale": round(e0i, 1),
            "mu_differentielle": round(mu_diff, 3),
            "R2_differentielle": round(r2_diff, 3),
            "mu_integrale_drainage": round(mu_int, 3),
            "R2_integrale": round(r2_int, 3),
            "mu_plateau": round(mu_pl, 3),
            "R2_plateau": round(r2_pl, 3),
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : les increments decorreleent ---
    v2 = all(s["R2_differentielle"] < 0.2 for s in stats.values())

    # --- F3 : la replication inter-graines tue la relation ---
    v3 = (stats["n4_440203"]["R2_integrale"] < 0.1
          and stats["n4_440201"]["R2_integrale"] < 0.7)

    # --- F4 : mu_plateau change de signe selon les runs ---
    signes = [np.sign(s["mu_plateau"]) for s in stats.values()]
    v4 = any(x > 0 for x in signes) and any(x < 0 for x in signes)

    # --- F5 : E0 integral change de signe ---
    e0s = [s["E0_integrale"] for s in stats.values()]
    v5 = any(x > 0 for x in e0s) and any(x < 0 for x in e0s)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_increments_decorelles": bool(v2),
                "V3_non_replication": bool(v3),
                "V4_plateau_signes_mixtes": bool(v4),
                "V5_E0_instabile": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T56-Q-KO6-TENSION-2026-10",
        "protocole": "T56-KO6-TENSION-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T56 : la tension de ligne — l'énergie du champ GP et la "
                 "longueur des filaments comme même monnaie : testée et "
                 "réfutée dans le protocole à paroi forcée (incréments "
                 "décorrélés, non-réplication, paroi à monnaie étrangère)",
        "doctrine": "T55 (les instruments ont leur régime) ; T53-D1 ; "
                    "NOTE-CREATION-MORT (le cycle de vie, monnaie "
                    "énergie)",
        "statut_du_mot": "MESURE — et REFUTATION déclarée : la relation "
                         "E = μΛ + E₀ ne tient pas dans ce protocole ; "
                         "dormeur publié",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 4],
                          "graines": [440201, 440201, 440203],
                          "masque": "interieur du cylindre (Rg < 26)",
                          "pas": PAS},
        "mesures": stats,
        "verdict_classe": ("DORMEUR (la relation E = μΛ + E₀ est "
                           "réfutée comme relation étroite dans le "
                           "protocole à paroi forcée : incréments "
                           "décorrélés R² ~ 0.02, seconde graine qui "
                           "tue la première, paroi à monnaie "
                           "étrangère — la comptabilité matière/"
                           "énergie demande un protocole silencieux)"),
        "falsifieur": "R²_diff ≥ 0.5 ; réplication R²_int ≥ 0.5 aux "
                      "deux graines ; μ_plateau de signe stable ; E₀ "
                      "stable",
        "suites_declarees": "un protocole silencieux (paroi non "
                            "forcée, après drainage) pour retenter la "
                            "comptabilité E = μΛ ; le cut de couche "
                            "limite (Rg < 24) ; confrontation au réel "
                            "en réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t56_ko6_tension_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T56 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : μ_diff = {s['mu_differentielle']:.3f} "
              f"(R2 {s['R2_differentielle']:.2f}), μ_int = "
              f"{s['mu_integrale_drainage']:.3f} (R2 "
              f"{s['R2_integrale']:.2f}), plateau : "
              f"{s['mu_plateau']:.2f} (R2 {s['R2_plateau']:.2f}), "
              f"E0 = {s['E0_integrale']:.0f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
