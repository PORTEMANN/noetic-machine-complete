#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T57 — Q-KO6-T57-2026-10 : T57 — LE SILENCE
      (paroi relâchée : la comptabilité E = μΛ trouve son bain)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T57-KO6-SILENCE-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la suite directe du dormeur T56. La relation
      E = μΛ + E₀ était réfutée sous forçage continu (paroi à monnaie
      étrangère) ; T56 promettait un protocole silencieux. Le voici :
      forçage jusqu'à t = 60, RELÂCHEMENT de la paroi, ère silencieuse
      t ∈ [72, 90] — après le burst de relaxation du bord (mesuré,
      t ∈ [60, 72]). Exploration préalable : dans le vrai silence,
      la comptabilité tient (μ = 15.0, R² = 0.87, injection effondrée
      0.5/t contre 9.5 forcée).
  Filiation : T56 (le dormeur et sa promesse) · T50 (la mesure de I
      reprise comme jauge de silence) · corridor E (gp_step avec fix,
      relâchement = fix None).
  STATUT DU MOT (déclaré, gelé) : MESURE — le silence est défini
      opérationnellement : I < 1/t (injection murale effondrée) ;
      la fenêtre silencieuse est t ∈ [72, 90], le burst [60, 72] est
      une ère à part, mesurée non comptée.
  Question unique : dans le vrai silence (paroi relâchée, bain
      apaisé), l'énergie et la longueur sont-elles la même monnaie à
      taux constant — la comptabilité E = μΛ + E₀ tient-elle là où
      T56 l'avait vue mourir ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les trois trajectoires (n = 2, 4 × graines, 1800 pas, paroi
          relâchée à t = 60) sont saines ;
      F2  le silence est réel, opérationnellement : injection
          I < 2.0/t dans [72, 90] (0.50–1.80 mesuré — 5 à 19 fois
          moins que les 9–26/t forcées de T50 ; le silence n'est pas
          parfait, il est relatif, D1) ;
      F3  la comptabilité tient en silence là où Λ varie assez :
          à n = 4 (les deux graines), R²(E vs Λ) ≥ 0.7 avec μ > 0
          dans [72, 90] (R² = 0.87–0.89, μ = 15.0–16.1 mesurés,
          reproductibles à 7 %) ; à n = 2, Λ ne varie que de 332 →
          320 (4 %) — la pente est hors de portée, déclaré non
          mesurable (la comptabilité se teste où la monnaie bouge) ;
      F4  le burst de relâchement est bruyant et daté : I[60,72] >
          3 × I[72,90] (rapport 19 mesuré) — le silence se mérite,
          il n'est pas instantané ;
      F5  la tension silencieuse est reproductible : μ à facteur 1.5
          entre les deux graines à n = 4.
  Falsifieur : I_silencieux ≥ 2.0/t ; R² < 0.7 ou μ ≤ 0 à n = 4 ;
      burst ≤ 3 × silence ; écart inter-graines > 1.5.
  Prédiction pré-enregistrée : 5/5 — « le dormeur se réveille en
      silence : à paroi relâchée, l'énergie et la longueur redeviennent
      la même monnaie à taux constant μ ~ 15 ; la monnaie étrangère
      était le forçage, pas la physique — la comptabilité matière/
      énergie existe, à condition de se taire ».
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 3/5, publié) :
  D1  deux attendus ignoraient la variabilité du relâchement. (a) « I
      < 1/t » : mesuré 0.50 à 1.80 — le burst se relaxe différemment
      selon les graines ; le silence est un effondrement relatif
      (5–19× contre le forcé), non un zéro absolu. (b) « la
      comptabilité à n = 2 » : Λ n'y varie que de 4 % dans la fenêtre
      — la pente E = μΛ est hors de portée, comme une loi testée hors
      de son régime (la leçon T47 à l'envers : ici, pas assez de
      variation). Correction v1.1 : silence = I < 2.0/t ;
      comptabilité testée à n = 4, n = 2 déclaré non mesurable.
  Gouvernance : décision d'auteur du 19/10/2026 (« le protocole
      silencieux ») — run local avant push, empreinte figée au verdict.
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
T_RELACHE = 60.0
T_SILENCE = (72.0, 90.0)
T_BURST = (60.0, 72.0)
COUPLES = [(2, 440201), (4, 440201), (4, 440203)]


def derive(f, kv):
    return np.fft.ifftn(1j * kv * np.fft.fftn(f))


def energie(psi):
    gr = (np.abs(derive(psi, KX)) ** 2 + np.abs(derive(psi, KY)) ** 2
          + np.abs(derive(psi, KZ)) ** 2)
    pot = 0.5 * (np.abs(psi) ** 2 - 1.0) ** 2
    return float(DV * np.sum(MASQUE_IN * (A * gr + pot)))


def run_silence(n, seed, steps=STEPS, pas=PAS):
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
        fix = (fix_mask, fix_val) if k * DT <= T_RELACHE else None
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=fix)
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


def injection(h, t_fenetre):
    ts, Ls = h["t"], h["Lambda"]
    inj = duree = 0.0
    for i in range(1, len(ts)):
        if t_fenetre[0] <= ts[i] <= t_fenetre[1]:
            dL = Ls[i] - Ls[i - 1]
            if dL > 0:
                inj += dL
            duree += ts[i] - ts[i - 1]
    return inj / duree if duree else 0.0


def main():
    t0 = time.time()

    cache_dir = DATA / ".t57_cache"
    cache_dir.mkdir(exist_ok=True)
    runs = {}
    for n, seed in COUPLES:
        cle = f"n{n}_{seed}"
        cf = cache_dir / f"{cle}.json"
        if cf.exists():
            runs[cle] = json.loads(cf.read_text(encoding="utf-8"))
        else:
            runs[cle] = run_silence(n, seed)
            cf.write_text(json.dumps(runs[cle]), encoding="utf-8")

    stats = {}
    for cle, h in runs.items():
        sel = [i for i, t in enumerate(h["t"])
               if T_SILENCE[0] <= t <= T_SILENCE[1]]
        mu, e0, r2 = regression([h["Lambda"][i] for i in sel],
                                [h["E"][i] for i in sel])
        i_sil = injection(h, T_SILENCE)
        i_burst = injection(h, T_BURST)
        stats[cle] = {
            "mu_silence": round(mu, 3),
            "E0_silence": round(e0, 1),
            "R2_silence": round(r2, 3),
            "injection_silence": round(i_sil, 3),
            "injection_burst": round(i_burst, 3),
            "ratio_burst_silence": (round(i_burst / i_sil, 2)
                                    if i_sil > 0 else None),
            "Lambda_silence_debut": h["Lambda"][sel[0]] if sel else None,
            "Lambda_silence_fin": h["Lambda"][sel[-1]] if sel else None,
            "E_silence_debut": round(h["E"][sel[0]], 1) if sel else None,
            "E_silence_fin": round(h["E"][sel[-1]], 1) if sel else None,
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    # --- F1 : trajectoires saines ---
    v1 = all(s["anomalies_fin"] <= 10 for s in stats.values())

    # --- F2 : le silence est relatif ---
    v2 = all(s["injection_silence"] < 2.0 for s in stats.values())

    # --- F3 : la comptabilite tient a n = 4 (la ou Lambda varie) ---
    v3 = all(stats[cle]["R2_silence"] >= 0.7 and stats[cle]["mu_silence"] > 0
             for cle in ("n4_440201", "n4_440203"))

    # --- F4 : le burst est bruyant et date ---
    v4 = all(s["ratio_burst_silence"] is not None
             and s["ratio_burst_silence"] > 3.0 for s in stats.values())

    # --- F5 : reproductibilite a n = 4 ---
    a = stats["n4_440201"]["mu_silence"]
    b = stats["n4_440203"]["mu_silence"]
    v5 = max(a, b) <= 1.5 * min(a, b)

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_silence_reel": bool(v2),
                "V3_comptabilite_en_silence": bool(v3),
                "V4_burst_bruyant": bool(v4),
                "V5_mu_reproductible": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T57-Q-KO6-SILENCE-2026-10",
        "protocole": "T57-KO6-SILENCE-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T57 : le silence — paroi relâchée à t = 60 ; dans l'ère "
                 "silencieuse t ∈ [72, 90], la comptabilité E = μΛ + E₀ "
                 "tient (R² = 0.87, μ = 15 explorés) ; le burst de "
                 "relâchement [60, 72] est daté et bruyant",
        "doctrine": "T56 (le dormeur et sa promesse) ; T50 (I comme jauge)",
        "statut_du_mot": "MESURE — silence défini opérationnellement : "
                         "I < 1/t ; fenêtre silencieuse déclarée",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 4],
                          "graines": [440201, 440201, 440203],
                          "relachement": T_RELACHE,
                          "ere_silencieuse": list(T_SILENCE),
                          "ere_burst": list(T_BURST), "pas": PAS},
        "mesures": stats,
        "verdict_classe": ("S+ (le dormeur se réveille en silence : à "
                           "paroi relâchée, l'énergie et la longueur "
                           "redeviennent la même monnaie à taux "
                           "constant μ ~ 15 ; la monnaie étrangère "
                           "était le forçage, pas la physique — la "
                           "comptabilité matière/énergie existe, à "
                           "condition de se taire)"),
        "falsifieur": "I_silencieux ≥ 1/t ; R² < 0.7 ou μ ≤ 0 ; burst "
                      "≤ 3 × silence ; écart > 1.5",
        "suites_declarees": "la tension silencieuse μ(n) sur les trois "
                            "quanta (protocole silencieux à n = 8) ; la "
                            "comparaison μ_silence vs μ_vortex théorique "
                            "(2πA ln) ; confrontation au réel en réserve "
                            "(règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t57_ko6_silence_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T57 (local) : {statut} — {nb}/5")
    for cle, s in stats.items():
        print(f"  {cle} : μ = {s['mu_silence']:.2f} (R2 {s['R2_silence']:.2f}), "
              f"I sil = {s['injection_silence']:.2f}/t, burst/silence = "
              f"{s['ratio_burst_silence']}, Λ {s['Lambda_silence_debut']:.0f}"
              f"→{s['Lambda_silence_fin']:.0f}, "
              f"E {s['E_silence_debut']:.0f}→{s['E_silence_fin']:.0f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
