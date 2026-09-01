#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P48 — F17 voie (ii) : BASELINE DE REPOS FIGÉE COMME D
======================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [EEG-BASE-1.0 gelé]

P44 a mesuré la réfutation de l'asymétrie absolue (0,540) et de la
baseline intra-essai (0,520) ; P47 a mesuré l'insuffisance du vote
(0,5926 < 0,60 figé). Voie (ii) du registre F17 : figer la baseline de
repos du sujet comme D — une DONNÉE de référence déclarée (C12.1), pas
un paramètre ajusté sur les essais.

Règle pré-enregistrée (zéro paramètre au sens C12.1)
  D_sujet = occupation μ moyenne de repos par canal, mesurée sur les
  segments pré-repère [−1,5 s, −0,5 s] de TOUS les essais du sujet —
  figée AVANT toute lecture des essais MI (déclaré).
  Par essai : Δc = o_c(MI) − D_sujet[c] ; prédire DROITE si
  ΔC3 < ΔC4 (C3 chute davantage que sa propre baseline → main droite).
  Aucune calibration sur les étiquettes : la baseline est une mesure de
  repos, publiée avec ses empreintes.

Attentes pré-enregistrées (tuables — mêmes seuils que P44, figés)
  B1  précision moyenne (9 sujets) ≥ 0,60 — OU l'échec est publié avec
      les mesures par sujet (B3-FAIL).
  B2  ≥ 5/9 sujets individuellement au-dessus du hasard au seuil
      binomial p ≤ 0,05 (seuil recomputé dans le script).
  B3  leviers effondrés : même règle sur θ (0,479 à P44) et sur P1/P2
      (0,514) ne doivent pas dépasser 0,55 — sinon la discrimination
      n'est pas portée par l'ERD μ et le verdict est retiré.

Falsifieur global : B1 ou B2 non tenus → la voie (ii) est mesurée comme
insuffisante, publiée (B3-FAIL) ; reste (iii). Un levier non effondré
retire le verdict même si B1/B2 tiennent.

D = BCICIV-2a (zip figé SHA 65fe93cb…) — même pipeline que P44/P47.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p43_ash_core_v100 import ASH

FS = 250.0
NOTE_MIN_MU, NOTE_MAX_MU = 36, 44
NOTE_MIN_THETA, NOTE_MAX_THETA = 24, 35
MI_OFFSET_S, MI_DUREE_S = 1.0, 3.0
DIR = Path("/tmp/p44_gdf")
SUJETS = [f"A0{i}T" for i in range(1, 10)]
CLASSES = {769: "gauche", 770: "droite"}
MONTAGE = {"C3": "EEG-C3", "C4": "EEG-C4", "P1": "EEG-14", "P2": "EEG-15"}


def occupation(sig, n_min, n_max):
    ash = ASH(fs=FS, signal_type="generic", f0=1.0, n_octaves=5,
              window_duration=MI_DUREE_S, overlap=0.5)
    r = ash.process_window(np.asarray(sig, dtype=float))
    c = np.asarray(r["coeffs"])
    tot = float(np.sum(c))
    return float(np.sum(c[n_min:n_max + 1]) / tot) if tot > 1e-12 else 0.0


def essais_sujet(path):
    import mne
    raw = mne.io.read_raw_gdf(str(path), preload=True, verbose="ERROR")
    segs = {c: {ch: [] for ch in MONTAGE} for c in CLASSES.values()}
    base = {ch: [] for ch in MONTAGE}
    for ann in raw.annotations:
        if not (ann["description"].isdigit() and int(ann["description"]) in CLASSES):
            continue
        i0 = int((ann["onset"] + MI_OFFSET_S) * FS)
        i1 = i0 + int(MI_DUREE_S * FS)
        b0 = int((ann["onset"] - 1.5) * FS)
        b1 = int((ann["onset"] - 0.5) * FS)
        if i1 > raw.n_times or b0 < 0:
            continue
        for ch, nom in MONTAGE.items():
            j = raw.ch_names.index(nom)
            segs[CLASSES[int(ann["description"])]][ch].append(
                raw.get_data(picks=[j], start=i0, stop=i1)[0])
            base[ch].append(raw.get_data(picks=[j], start=b0, stop=b1)[0])
    return segs, base


def main():
    t0 = time.time()
    print("P48 — F17 voie (ii) : BASELINE FIGÉE   [EEG-BASE-1.0 gelé]")
    print("=" * 70)

    par_sujet = {}
    for s in SUJETS:
        segs, base = essais_sujet(DIR / f"{s}.gdf")
        # D figée : baseline de repos par canal (mesurée avant les essais MI)
        D_fig = {ch: float(np.mean([occupation(b, NOTE_MIN_MU, NOTE_MAX_MU)
                                    for b in base[ch]])) for ch in MONTAGE}
        bon = tot = 0
        for classe in ("gauche", "droite"):
            for s3, s4 in zip(segs[classe]["C3"], segs[classe]["C4"]):
                d3 = occupation(s3, NOTE_MIN_MU, NOTE_MAX_MU) - D_fig["C3"]
                d4 = occupation(s4, NOTE_MIN_MU, NOTE_MAX_MU) - D_fig["C4"]
                pred = "droite" if d3 < d4 else "gauche"
                tot += 1
                bon += int(pred == classe)
        # leviers : θ et P1/P2
        def levier(n_min, n_max, c1, c2):
            D_l = {ch: float(np.mean([occupation(b, n_min, n_max)
                                      for b in base[ch]])) for ch in (c1, c2)}
            b_l = t_l = 0
            for classe in ("gauche", "droite"):
                for s1, s2 in zip(segs[classe][c1], segs[classe][c2]):
                    d1 = occupation(s1, n_min, n_max) - D_l[c1]
                    d2 = occupation(s2, n_min, n_max) - D_l[c2]
                    pred = "droite" if d1 < d2 else "gauche"
                    t_l += 1
                    b_l += int(pred == classe)
            return b_l / t_l if t_l else 0.0
        l1 = levier(NOTE_MIN_THETA, NOTE_MAX_THETA, "C3", "C4")
        l2 = levier(NOTE_MIN_MU, NOTE_MAX_MU, "P1", "P2")
        par_sujet[s] = {"précision": round(bon / tot, 4), "bon": bon,
                        "total": tot, "levier_θ": round(l1, 4),
                        "levier_P1P2": round(l2, 4),
                        "D_figée": {k: round(v, 6) for k, v in D_fig.items()}}
        print(f"{s} : baseline-figée {bon}/{tot} = {bon/tot:.3f} | "
              f"θ {l1:.3f} | P1P2 {l2:.3f}")

    precs = [r["précision"] for r in par_sujet.values()]
    moy = float(np.mean(precs))
    n_sig = 0
    for s, r in par_sujet.items():
        p = binomtest(int(r["bon"]), int(r["total"]), 0.5).pvalue
        if p <= 0.05 and r["bon"] / r["total"] > 0.5:
            n_sig += 1
    l1_moy = float(np.mean([r["levier_θ"] for r in par_sujet.values()]))
    l2_moy = float(np.mean([r["levier_P1P2"] for r in par_sujet.values()]))
    B1 = moy >= 0.60
    B2 = n_sig >= 5
    B3 = bool(l1_moy <= 0.55 and l2_moy <= 0.55)
    print(f"\nB1 moyenne {moy:.4f} (seuil 0,60 figé) → {'✓' if B1 else '✗ publié'}")
    print(f"B2 sujets significatifs {n_sig}/9 (seuil 5) → {'✓' if B2 else '✗ publié'}")
    print(f"B3 leviers θ {l1_moy:.3f} / P1P2 {l2_moy:.3f} (≤ 0,55) → "
          f"{'✓ effondrés' if B3 else '✗ — verdict retiré'}")

    criteres = {"B1_précision_moyenne": B1, "B2_sujets_significatifs": B2,
                "B3_leviers_effondrés": B3}
    nb = sum(criteres.values())
    statut = ("SUCCÈS" if nb == 3 else "PARTIEL" if nb == 2 else
              "ÉCHEC (B3-FAIL publié)")

    resultats = {
        "chantier": "P48-EEG-BASELINE-FIGEE", "protocole": "EEG-BASE-1.0 (gelé)",
        "voie_F17": "(ii) baseline de repos du sujet figée comme D (C12.1)",
        "règle": "Δc = o_c(MI) − D_sujet[c] ; DROITE si ΔC3 < ΔC4",
        "par_sujet": par_sujet, "précision_moyenne": round(moy, 4),
        "sujets_significatifs": n_sig,
        "leviers_moyens": {"θ": round(l1_moy, 4), "P1P2": round(l2_moy, 4)},
        "critères": criteres, "score": f"{nb}/3", "statut": statut,
        "falsifieur": "B1 ou B2 non tenus → voie (ii) mesurée insuffisante, "
                      "publiée ; levier non effondré retire le verdict",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "p48_eeg_base_figee_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"VERDICT P48 : {statut} — {nb}/3")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
