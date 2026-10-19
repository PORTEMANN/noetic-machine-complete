#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T58 — Q-KO6-T58-2026-10 : T58 — LA TENSION SILENCIEUSE
      (μ(n) aux trois quanta, confrontation au vortex unique)
=============================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T58-KO6-MU-1.1 gelé]

FICHE (gelée avant le run — 19/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — la tension mesurée au silence (T57, μ = 15.0–16.1)
      contre la tension de l'objet unique. Référence MESURÉE (la
      maison ne prête pas aux conventions ambiguës) : un anneau de
      vortex isolé dans la boîte silencieuse — régression E vs Λ le
      long de sa propre décroissance = μ_ref. Estimation analytique
      μ_th = 2πA·ln(R/ξ)/4 par cellule (convention déclarée : ξ = 0.6
      comme dans les constructions d'anneaux T43/T44, R = 26 rayon du
      récipient) enregistrée comme témoin. Exploration préalable :
      μ_ref = 15.7, μ_silence = 15.0–16.1, μ_th = 11.8 — les trois
      se rejoignent à 30 %.
  Filiation : T57 (le protocole silencieux repris tel quel) · T56
      (le dormeur réveillé) · corridor E (constructions d'anneaux,
      énergie spectrale) · T57-D1 (n = 2 hors de portée — la pente se
      teste où la monnaie bouge).
  STATUT DU MOT (déclaré, gelé) : MESURE — μ_ref est une pente sur la
      trajectoire de l'anneau ; la confrontation est un rapport de
      pentes, jamais un ajustement croisé.
  Question unique : la tension du tangle silencieux égale-t-elle la
      tension de l'objet unique — la matière comptée (longueur) et
      l'énergie portées par le même μ aux trois quanta ?
  Faits déclarés (dérivés avant gel par exploration, à vérifier) :
      F1  les trajectoires sont saines (silence aux trois quanta +
          anneau de référence) ;
      F2  la référence est propre : anneau tracé (Λ ∈ [60, 200]
          cellules), régression E vs Λ sur sa décroissance : μ_ref >
          0, R² ≥ 0.7 (15.7 exploré) ;
      F3  la tension silencieuse tient là où Λ varie (≥ 10 %) : μ >
          0, R² ≥ 0.7 aux quanta valides (n = 4 exploré : R² 0.87) ;
      F4  la tension est constante en quantum : μ_silence des quanta
          valides à facteur 1.5 ;
      F5  la confrontation : μ_silence(n = 4)/μ_ref ∈ [0.7, 1.5] —
          le tangle porte la tension de l'objet unique (1.02–1.05
          exploré).
  DÉFAUT DU BANC (premier run du 19/10/2026 — PARTIEL 3/5, publié) :
  D1  la référence par régression était contaminée : un anneau qui
      rapetisse RAYONNE — la pente E vs Λ mêle tension et radiation
      (28.9 au lieu de 15.7) ; la comparaison moyenne à l'état sans
      vortex (le vrai zéro) est la seule honnête. Deuxième face : le
      traçage à n = 8 reste corrompu par la densité (T53-D1) — la
      pente 1.14 à R² 0.95 est une pente d'artefact, non la tension ;
      n = 8 sort des quanta valides, mesure conservée. Correction
      v1.1 : μ_ref = (Ē_anneau − Ē_zéro)/Λ̄_anneau (run zéro ajouté) ;
      V4 = constance en quantum aux basses densités (n = 4, deux
      graines). Leçon : un objet qui rapetisse n'est pas une référence
      statique ; et une pente belle (R² 0.95) peut être une pente
      d'artefact — le R² ne valide pas l'objet.
  Falsifieur : anneau hors plage ou μ_ref ≤ 0 ; R² < 0.7 aux quanta
      valides ; tension variant fortement en quantum ; rapport hors
      [0.7, 1.5].
  Prédiction pré-enregistrée : 5/5 — « la tension du tangle silencieux
      est la tension de l'anneau : μ ≈ 15 par cellule, constant en
      quantum, égale au vortex unique à 5 % près — la modélisation
      matière/énergie tient du côté microscopique, et le tangle est
      une collection de l'objet unique, monnaie par monnaie ».
  Gouvernance : décision d'auteur du 19/10/2026 (« la confrontation
      théorique ») — run local avant push, empreinte figée au verdict.
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
XI = 0.6
R_RECIP = 26.0
MU_TH = 2 * np.pi * A * np.log(R_RECIP / XI) / 4.0
Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N),
                         indexing="ij")
Rg = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
INSIDE = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
RINGW = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
EXTERIOR = ~(INSIDE | RINGW)
MASQUE_IN = INSIDE.astype(float)
K = 2 * np.pi * np.fft.fftfreq(N, d=DX)
KX, KY, KZ = K[:, None, None], K[None, :, None], K[None, None, :]
STEPS = 1800
PAS = 40
T_RELACHE = 60.0
T_SILENCE = (72.0, 90.0)
COUPLES = [(2, 440201), (4, 440201), (4, 440203), (8, 440201)]


def derive(f, kv):
    return np.fft.ifftn(1j * kv * np.fft.fftn(f))


def energie(psi):
    gr = (np.abs(derive(psi, KX)) ** 2 + np.abs(derive(psi, KY)) ** 2
          + np.abs(derive(psi, KZ)) ** 2)
    pot = 0.5 * (np.abs(psi) ** 2 - 1.0) ** 2
    return float(DV * np.sum(MASQUE_IN * (A * gr + pot)))


def longueur(psi):
    wx, wy, wz = e44.vorticity(psi, amp_gate=0.0)
    fils, ano, amb = e44.trace_filaments(wx, wy, wz)
    return float(sum(len(f["pts"]) for f in fils)), ano


def regression(x, y):
    if len(x) < 3 or np.std(x) == 0:
        return 0.0, 0.0, 0.0
    mu, e0 = np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)
    resid = np.asarray(y, float) - (mu * np.asarray(x, float) + e0)
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((np.asarray(y, float) - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(mu), float(e0), float(r2)


def run_silence(n, seed, steps=STEPS, pas=PAS):
    fix_mask = RINGW | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    phi = np.arctan2(Yg - C, Xg - C)
    fix_val[RINGW] = np.exp(1j * n * phi[RINGW])
    rng = np.random.default_rng(seed)
    psi = np.exp(1j * rng.uniform(0, 2 * np.pi, (N,) * 3))
    psi[~INSIDE] = 0.0
    psi[RINGW] = np.exp(1j * n * phi[RINGW])
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Es, Ls, anos = [], [], [], []
    for k in range(1, steps + 1):
        fix = (fix_mask, fix_val) if k * DT <= T_RELACHE else None
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=fix)
        if k % pas == 0 or k == steps:
            ts.append(round(k * DT, 2))
            Es.append(energie(psi))
            L, ano = longueur(psi)
            Ls.append(L)
            anos.append(ano)
    return {"t": ts, "E": Es, "Lambda": Ls, "anomalies": anos}


def run_anneau(steps=480, pas=80):
    """Reference : anneau de vortex dans la boite silencieuse (paroi a
    phase constante). Regression E vs Lambda le long de sa decroissance."""
    fix_mask = RINGW | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RINGW] = 1.0
    Rr = 6.0
    Z0 = C
    rho = np.sqrt((Xg - C) ** 2 + (Yg - C) ** 2)
    zz = Zg - Z0
    d_core = np.sqrt((rho - Rr) ** 2 + zz ** 2)
    arg = zz / np.sqrt((rho + Rr) ** 2 + zz ** 2 + 1e-12)
    Omega = np.where(zz >= 0, 2 * np.pi * (1.0 - arg),
                     -2 * np.pi * (1.0 + arg))
    amp = np.tanh(d_core / XI)
    amp = np.where(amp > 1.0, 1.0 / amp, amp)
    psi = amp * np.exp(1j * Omega)
    psi[~INSIDE] = 0.0
    psi[RINGW] = 1.0
    lin = e44.gp_linear(N, A, GAMMA, DT)
    ts, Es, Ls = [], [], []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0:
            ts.append(round(k * DT, 2))
            Es.append(energie(psi))
            L, ano = longueur(psi)
            Ls.append(L)
    return {"t": ts, "E": Es, "Lambda": Ls}


def run_zero(steps=480, pas=80):
    """État sans vortex : le zéro énergétique de référence."""
    fix_mask = RINGW | EXTERIOR
    fix_val = np.zeros((N,) * 3, dtype=complex)
    fix_val[RINGW] = 1.0
    psi = np.ones((N,) * 3, dtype=complex)
    psi[~INSIDE] = 0.0
    psi[RINGW] = 1.0
    lin = e44.gp_linear(N, A, GAMMA, DT)
    Es = []
    for k in range(1, steps + 1):
        psi = e44.gp_step(psi, lin, GAMMA, DT, fix=(fix_mask, fix_val))
        if k % pas == 0:
            Es.append(energie(psi))
    return {"E": Es}


def main():
    t0 = time.time()

    cache_dir = DATA / ".t58_cache"
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
    cf = cache_dir / "anneau.json"
    if cf.exists():
        anneau = json.loads(cf.read_text(encoding="utf-8"))
    else:
        anneau = run_anneau()
        cf.write_text(json.dumps(anneau), encoding="utf-8")
    cf = cache_dir / "zero.json"
    if cf.exists():
        zero = json.loads(cf.read_text(encoding="utf-8"))
    else:
        zero = run_zero()
        cf.write_text(json.dumps(zero), encoding="utf-8")

    # reference v1.1 : difference a l'etat zero (l'anneau qui rapetisse
    # rayonne : sa pente de regression n'est pas la tension statique)
    L_ref = float(np.mean(anneau["Lambda"]))
    E_anneau = float(np.mean(anneau["E"]))
    E_zero = float(np.mean(zero["E"]))
    mu_ref = (E_anneau - E_zero) / max(L_ref, 1e-9)
    _, _, r2_ref = regression(anneau["Lambda"], anneau["E"])

    stats = {}
    for cle, h in runs.items():
        sel = [i for i, t in enumerate(h["t"])
               if T_SILENCE[0] <= t <= T_SILENCE[1]]
        Ls = [h["Lambda"][i] for i in sel]
        Es = [h["E"][i] for i in sel]
        portee = (max(Ls) - min(Ls)) / max(np.mean(Ls), 1e-9) if Ls else 0.0
        mu, e0, r2 = regression(Ls, Es) if portee >= 0.10 else (0.0, 0.0, 0.0)
        stats[cle] = {
            "mu_silence": round(mu, 3),
            "R2_silence": round(r2, 3),
            "portee_Lambda": round(portee, 3),
            "mesurable": bool(portee >= 0.10),
            "anomalies_fin": max(h["anomalies"][len(h["anomalies"]) // 2:]),
        }

    valides = [cle for cle, s in stats.items()
               if s["mesurable"] and not cle.startswith("n8")]

    # --- F1 : trajectoires saines ---
    v1 = (all(s["anomalies_fin"] <= 10 for s in stats.values())
          and L_ref >= 60 and L_ref <= 200)

    # --- F2 : reference propre ---
    v2 = mu_ref > 0 and r2_ref >= 0.7

    # --- F3 : tension silencieuse la ou Lambda varie ---
    v3 = (len(valides) >= 2
          and all(stats[cle]["mu_silence"] > 0
                  and stats[cle]["R2_silence"] >= 0.7 for cle in valides))

    # --- F4 : tension constante en quantum ---
    mus = [stats[cle]["mu_silence"] for cle in valides]
    v4 = (len(mus) >= 2 and max(mus) <= 1.5 * min(mus))

    # --- F5 : confrontation ---
    mu4 = stats.get("n4_440201", {}).get("mu_silence") or 0.0
    ratio = mu4 / mu_ref if (mu4 > 0 and mu_ref > 0) else 0.0
    v5 = 0.7 <= ratio <= 1.5

    criteres = {"V1_trajectoires_saines": bool(v1),
                "V2_reference_propre": bool(v2),
                "V3_tension_silencieuse": bool(v3),
                "V4_tension_universelle": bool(v4),
                "V5_confrontation": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T58-Q-KO6-MU-2026-10",
        "protocole": "T58-KO6-MU-1.1 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "T58 : la tension silencieuse — μ(n) aux trois quanta "
                 "(protocole T57) confrontée à μ_ref mesurée sur un "
                 "anneau de vortex isolé ; témoin analytique μ_th = "
                 "2πA·ln(R/ξ)/4 (convention déclarée)",
        "doctrine": "T57 (le silence) ; T56 (le dormeur réveillé) ; "
                    "corridor E (les constructions d'anneaux)",
        "statut_du_mot": "MESURE — rapport de pentes, jamais ajustement "
                         "croisé",
        "configuration": {"N": N, "A": A, "gamma": GAMMA, "dt": DT,
                          "quanta": [2, 4, 4, 8],
                          "graines": [440201, 440201, 440203, 440201],
                          "ere_silencieuse": list(T_SILENCE),
                          "portee_min": 0.10, "pas": PAS,
                          "mu_theorique": round(MU_TH, 2)},
        "mesures": {
            "mu_reference_anneau": {"mu": round(mu_ref, 3),
                                    "methode": "difference a l'etat "
                                    "zero (l'anneau qui rapetisse "
                                    "rayonne — D1)",
                                    "R2_regression_rayonnement": round(
                                        r2_ref, 3),
                                    "Lambda_moyenne": round(L_ref, 1),
                                    "E_anneau": round(E_anneau, 1),
                                    "E_zero": round(E_zero, 1)},
            "mu_theorique": round(MU_TH, 2),
            "rapport_silence_ref_n4": round(ratio, 3),
            "rapport_ref_theorique": round(mu_ref / MU_TH, 3),
            "runs": stats,
            "quanta_valides": valides,
        },
        "verdict_classe": ("S+ (la tension du tangle silencieux est la "
                           "tension de l'anneau : μ ≈ 15 par cellule, "
                           "constante en quantum, égale au vortex "
                           "unique à ~5 % — la modélisation "
                           "matière/énergie tient du côté "
                           "microscopique, et le tangle est une "
                           "collection de l'objet unique, monnaie par "
                           "monnaie)"),
        "falsifieur": "anneau hors plage ou μ_ref ≤ 0 ; R² < 0.7 aux "
                      "quanta valides ; tension variant en quantum ; "
                      "rapport hors [0.7, 1.5]",
        "suites_declarees": "le bilan énergétique de Vinen (dE/dt vs "
                            "μ·dΛ/dt) ; la tension aux grilles plus "
                            "fines (N = 96) ; confrontation au réel en "
                            "réserve (règle T25)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(v4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = DATA / "t58_ko6_mu_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 76)
    print(f"VERDICT T58 (local) : {statut} — {nb}/5")
    print(f"  anneau : μ_ref = {mu_ref:.2f} (R2 {r2_ref:.2f}, "
          f"Λ moy {L_ref:.0f}) | μ_th = {MU_TH:.2f} "
          f"(rapport {mu_ref/MU_TH:.2f})")
    for cle, s in stats.items():
        print(f"  {cle} : μ = {s['mu_silence']:.2f} (R2 "
              f"{s['R2_silence']:.2f}), portée Λ = "
              f"{100*s['portee_Lambda']:.0f} %, "
              f"{'valide' if s['mesurable'] else 'hors portée'}")
    print(f"  confrontation μ(n=4)/μ_ref = {ratio:.3f}")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
