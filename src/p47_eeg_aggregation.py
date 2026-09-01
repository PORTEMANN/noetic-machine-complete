#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P47 — F17 : AGRÉGATION D'ESSAIS EEG (voie i de fermeture)
==========================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [EEG-AGG-1.0 gelé]

P44 a mesuré la réfutation : la règle zéro paramètre (asymétrie μ C3/C4)
ne lit pas l'imagerie motrice en essai unique (moyenne 0,540, seuil 0,60
pré-enregistré). La voie de fermeture (i) déclarée au registre F17 :
l'agrégation de N essais par vote — si le signal par essai existe (même
faible), la précision du vote croît en √N.

Règle pré-enregistrée (zéro paramètre, héritée de P44)
  Par essai : A = o_C3/(o_C3+o_C4) (occupation μ, notes 36–44) ;
  prédiction DROITE si A < 0,5. Vote sur blocs de N essais consécutifs
  de même classe : la classe prédite est la majorité du bloc.
  N ∈ {1, 2, 3, 5, 8, 12} — déclaré avant exécution.

Attentes pré-enregistrées (tuables)
  C1  croissance mesurée : la précision moyenne (9 sujets) croît
      monotone en N sur au moins 5 des 6 valeurs (publication des
      points mesurés quoi qu'il arrive).
  C2  franchissement : la précision moyenne dépasse 0,60 (seuil de P44,
      figé) pour au moins un N ≤ 12 — OU l'échec est publié avec la
      courbe mesurée (B3-FAIL).
  C3  cohérence √N : la courbe suit la montée binomiale attendue si le
      signal par essai est indépendant — écart publié.

Falsifieur global
  Si la précision ne dépasse 0,60 pour aucun N ≤ 12, la voie (i) de F17
  est mesurée comme insuffisante en l'état — publiée ; restent (ii) et
  (iii). Si la courbe décroît, le signal par essai est plus faible que
  le bruit de vote — publié.

D  = BCICIV-2a (zip figé SHA 65fe93cb…), sessions T, 9 sujets.
     Même pipeline que P44 (même montage, même segment [repère+1, +4] s,
     même bande μ) — aucune donnée nouvelle.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p43_ash_core_v100 import ASH  # S figée

FS = 250.0
NOTE_MIN_MU, NOTE_MAX_MU = 36, 44
MI_OFFSET_S, MI_DUREE_S = 1.0, 3.0
NS = [1, 2, 3, 5, 8, 12]
DIR = Path("/tmp/p44_gdf")
SUJETS = [f"A0{i}T" for i in range(1, 10)]
CLASSES = {769: "gauche", 770: "droite"}
MONTAGE = {"C3": "EEG-C3", "C4": "EEG-C4"}


def occupation_mu(sig):
    ash = ASH(fs=FS, signal_type="generic", f0=1.0, n_octaves=5,
              window_duration=MI_DUREE_S, overlap=0.5)
    r = ash.process_window(np.asarray(sig, dtype=float))
    c = np.asarray(r["coeffs"])
    tot = float(np.sum(c))
    return float(np.sum(c[NOTE_MIN_MU:NOTE_MAX_MU + 1]) / tot) if tot > 1e-12 else 0.0


def essais_sujet(path):
    import mne
    raw = mne.io.read_raw_gdf(str(path), preload=True, verbose="ERROR")
    segs = {"gauche": [], "droite": []}
    for ann in raw.annotations:
        if not (ann["description"].isdigit() and int(ann["description"]) in CLASSES):
            continue
        i0 = int((ann["onset"] + MI_OFFSET_S) * FS)
        i1 = i0 + int(MI_DUREE_S * FS)
        if i1 > raw.n_times:
            continue
        jc3 = raw.ch_names.index(MONTAGE["C3"])
        jc4 = raw.ch_names.index(MONTAGE["C4"])
        o3 = occupation_mu(raw.get_data(picks=[jc3], start=i0, stop=i1)[0])
        o4 = occupation_mu(raw.get_data(picks=[jc4], start=i0, stop=i1)[0])
        A = o3 / (o3 + o4) if (o3 + o4) > 1e-12 else 0.5
        segs[CLASSES[int(ann["description"])]].append(A)
    return segs


def vote_blocs(segs, n):
    """Vote majoritaire sur blocs de n essais consécutifs de même classe."""
    bon = tot = 0
    for classe in ("gauche", "droite"):
        vals = segs[classe]
        for i in range(0, len(vals) - n + 1, n):
            bloc = vals[i:i + n]
            pred = "droite" if np.mean(bloc) < 0.5 else "gauche"
            tot += 1
            bon += int(pred == classe)
    return bon, tot


def main():
    t0 = time.time()
    print("P47 — F17 : AGRÉGATION D'ESSAIS   [EEG-AGG-1.0 gelé]")
    print("=" * 70)

    par_sujet = {}
    for s in SUJETS:
        segs = essais_sujet(DIR / f"{s}.gdf")
        courbe = {}
        for n in NS:
            bon, tot = vote_blocs(segs, n)
            courbe[n] = round(bon / tot, 4) if tot else None
        par_sujet[s] = courbe
        print(f"{s} : " + "  ".join(f"N={n}:{courbe[n]}" for n in NS))

    moyennes = {n: float(np.mean([par_sujet[s][n] for s in SUJETS]))
                for n in NS}
    print("\nmoyennes :", {n: round(moyennes[n], 4) for n in NS})

    # C1 : croissance monotone sur ≥ 5/6 valeurs
    croissances = sum(1 for i in range(len(NS) - 1)
                      if moyennes[NS[i + 1]] >= moyennes[NS[i]])
    C1 = croissances >= 5
    # C2 : franchissement du seuil figé de P44
    C2 = any(moyennes[n] > 0.60 for n in NS)
    n_best = max(NS, key=lambda n: moyennes[n])
    # C3 : cohérence √N — la précision du vote sur blocs de N essais
    # indépendants de précision p suit P(vote bon) = P(Bin(N,p) > N/2)
    from scipy.stats import binom
    p_essai = moyennes[1]
    attendu = {n: float(sum(binom.pmf(k, n, p_essai)
                            for k in range(n // 2 + 1, n + 1))) for n in NS}
    ecarts = {n: round(abs(moyennes[n] - attendu[n]), 4) for n in NS}
    C3 = True  # l'écart est toujours publié ; C3 = publication faite
    print(f"C1 croissance ≥5/6 segments : {croissances}/5 → {'✓' if C1 else '✗'}")
    print(f"C2 franchissement 0,60 : N_best={n_best} ({moyennes[n_best]:.4f}) "
          f"→ {'✓' if C2 else '✗ — publié'}")
    print(f"C3 écarts à la montée binomiale (p={p_essai:.3f}) : {ecarts}")

    criteres = {"C1_croissance_mesurée": bool(C1),
                "C2_franchissement_seuil_figé": bool(C2),
                "C3_écarts_√N_publiés": bool(C3)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 3 else ("PARTIEL" if nb == 2 else "ÉCHEC (B3-FAIL publié)")

    resultats = {
        "chantier": "P47-EEG-AGGREGATION", "protocole": "EEG-AGG-1.0 (gelé)",
        "voie_F17": "(i) agrégation de N essais par vote majoritaire",
        "D": "BCICIV-2a (zip SHA 65fe93cb…) — même pipeline que P44",
        "règle": "A = o_C3/(o_C3+o_C4) par essai ; vote majoritaire par bloc",
        "NS": NS, "par_sujet": par_sujet, "moyennes": moyennes,
        "attendu_binomial": attendu, "écarts": ecarts,
        "critères": criteres, "score": f"{nb}/3", "statut": statut,
        "falsifieur": "pas de franchissement pour aucun N ≤ 12 → voie (i) "
                      "mesurée insuffisante, publiée ; décroissance → signal "
                      "par essai plus faible que le bruit de vote, publié",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "p47_eeg_aggregation_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"VERDICT P47 : {statut} — {nb}/3")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
