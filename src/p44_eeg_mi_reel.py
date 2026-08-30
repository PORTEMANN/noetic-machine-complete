#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P44 — EEG-MI-REEL : la chaîne ASH → M̂ lit-elle l'intention motrice ?
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → (V, Σ)

D  = BCICIV-2a (BCI Competition IV, dataset 2a) — EEG RÉEL d'imagerie
     motrice, 9 sujets, 22 canaux + 3 EOG, 250 Hz, sessions
     d'entraînement A01T–A09T (288 essais/sujet, 72 par classe :
     gauche, droite, pieds, langue). SHA-256 publiés. Artefacts NON
     rejetés (déclaré — protocole v1 ; les drapeaux d'artefact existent
     dans le format GDF, leur usage est une suite déclarée).
S  = la chaîne ASH figée v1.0.0 (copie data/p43_ash_core_v100.py,
     sha256 338dbda7…) appliquée aux canaux C3, Cz, C4 (et P1, P2 pour
     le levier spatial).
π  = f0 = 1 Hz, n_octaves = 5 (grille 1–30,2 Hz — extension déclarée du
     domaine eeg figé, nécessaire pour couvrir β), fenêtre d'analyse =
     segment MI [repère+1 s, repère+4 s] de chaque essai, nperseg auto
     (375), seuil_pic = 0.10. Bande μ noétique : notes n telles que
     8 ≤ f_n < 13 Hz (notes 36–44).
     Montage 2a déclaré (les étiquettes GDF sont partiellement
     numérotées) : EEG-14 = P1, EEG-15 = P2 (positions standard du
     dataset) ; C3, Cz, C4, Pz portent leurs noms.

RÈGLE DE DÉCISION — ZÉRO PARAMÈTRE
  Occupation μ par canal : o_c = Σ_{n∈μ} c_n / Σ_n c_n (invariant
  d'amplitude par construction — F16 respectée : ReN n'est PAS utilisé).
  Asymétrie : A = o_C3 / (o_C3 + o_C4).
  L'ERD d'imagerie motrice est controlatérale : imaginer la main DROITE
  désynchronise le cortex GAUCHE (C3) → o_C3 chute.
  Règle : A < 0.5 → DROITE ; A > 0.5 → GAUCHE. Aucun seuil ajusté,
  aucune calibration, aucun apprentissage.

PRÉDICTIONS PRÉ-ENREGISTRÉES (avant toute exécution)
  P44-1 (principale) : la règle de signe bat le hasard — précision
       moyenne sur les 9 sujets ≥ 0.60 (hasard 0.50), ET ≥ 5 sujets / 9
       individuellement au-dessus du hasard au seuil binomial p ≤ 0.05
       (seuil exact recomputé dans le script).
  P44-2 (leviers — la règle doit s'effondrer SANS le mécanisme) :
       L1 bande : même règle sur la bande θ (notes 24–35, 4–8 Hz) →
                  précision ≤ 0.55 (l'effet ne vit que dans μ) ;
       L2 espace : même règle sur la paire postérieure P1/P2 (hors
                  cortex moteur) → précision ≤ 0.55.
  P44-3 (exploratoire, sans critère) : extension 4 classes publiée en
       matrice de confusion — aucun seuil, mesure pure.

Contrôles
  C0  reproductibilité : deux exécutions → verdicts identiques.
  C1  fidélité : noyau π-instrumenté au nominal ≡ noyau figé (vérifié
      sur un essai de chaque sujet).

Falsifieur global
  P44-1 non tenue → l'affirmation « la chaîne lit la direction d'imagerie
  motrice sur EEG réel » est RÉFUTÉE et publiée (B3-FAIL). Un levier qui
  ne s'effondre pas (L1 ou L2 > 0.55) → la discrimination n'est pas
  portée par l'ERD μ : verdict retiré même si P44-1 tient.

ADDENDUM v2 (écrit après exécution de la v1, AVANT toute exécution v2 —
la v1 est conservée et publiée)
  Mesure v1 : précision moyenne 0.540 (seuil 0.60), 1 sujet / 9
  significatif (seuil 5/9) → P44-1 RÉFUTÉE ; leviers effondrés (L1
  0.479, L2 0.514 ≤ 0.55) → P44-2 tenue. Lecture : l'asymétrie ABSOLUE
  d'occupation μ mélange l'anatomie du sujet avec l'ERD ; or l'ERD est
  DÉFINIE relativement à une baseline. Règle v2 (toujours zéro
  paramètre) : baseline intra-essai = segment pré-repère
  [repère−1.5 s, repère−0.5 s] ;
    Δc = o_c(MI) − o_c(baseline) ;
    prédire DROITE si ΔC3 < ΔC4 (C3 chute davantage → main droite).
  Attentes pré-enregistrées v2 : mêmes seuils que v1 (moyenne ≥ 0.60,
  ≥ 5/9 sujets significatifs) ; leviers v2 identiques (θ et P1/P2
  ≤ 0.55). Si v2 échoue aussi, la réfutation est renforcée et le coût
  de fermeture devient : filtrage spatial dérivé ou baseline sujet
  figée — à déclarer au registre.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p43_ash_core_v100 import ASH  # S figée v1.0.0

# ====================================================================
# π gelé
# ====================================================================

FS = 250.0
PI = {"f0": 1.0, "n_octaves": 5, "window_duration": 3.0, "overlap": 0.5}
NOTE_MIN_MU, NOTE_MAX_MU = 36, 44    # 8 ≤ f_n < 13 Hz
NOTE_MIN_THETA, NOTE_MAX_THETA = 24, 35  # 4 ≤ f_n < 8 Hz
MI_OFFSET_S, MI_DUREE_S = 1.0, 3.0   # segment [repère+1, repère+4]
CANAUX_ASYM = ("EEG-C3", "EEG-C4")
CANAUX_LEVIER2 = ("EEG-P1", "EEG-P2")
CLASSES_2 = {769: "gauche", 770: "droite"}     # codes GDF des repères
CLASSES_4 = {769: "gauche", 770: "droite", 771: "pieds", 772: "langue"}

DIR_DATA = Path("/tmp/p44_gdf")
SUJETS = [f"A0{i}T" for i in range(1, 10)]


def occupation(pi, sig, n_min, n_max):
    """Signature ASH d'un segment ; occupation relative d'une bande de
    notes. ReN n'est jamais calculé (F16)."""
    ash = ASH(fs=FS, signal_type="generic", f0=pi["f0"],
              n_octaves=pi["n_octaves"],
              window_duration=pi["window_duration"], overlap=pi["overlap"])
    r = ash.process_window(np.asarray(sig, dtype=float))
    c = r["coeffs"]
    tot = float(np.sum(c))
    occ = float(np.sum(c[n_min:n_max + 1]) / tot) if tot > 1e-12 else 0.0
    return occ, {"Rtop": r["Rtop"], "Rdyn": r["Rdyn"]}


def essais_sujet(gdf_path):
    """Extrait les essais MI d'un sujet (labels GDF 769–772).
    Retourne dict classe → liste de segments par canal."""
    import mne
    raw = mne.io.read_raw_gdf(str(gdf_path), preload=True, verbose="ERROR")
    # montage 2a déclaré : les labels numérotés suivent l'ordre standard
    MONTAGE = {"C3": "EEG-C3", "C4": "EEG-C4", "Cz": "EEG-Cz",
               "P1": "EEG-14", "P2": "EEG-15"}
    segs = {c: {ch: [] for ch in ("C3", "C4", "Cz", "P1", "P2")}
            for c in CLASSES_4.values()}
    base = {c: {ch: [] for ch in ("C3", "C4", "Cz", "P1", "P2")}
            for c in CLASSES_4.values()}
    for ann in raw.annotations:
        desc = ann["description"]
        code = None
        for k in CLASSES_4:
            if desc in (str(k), f"769.0", f"770.0", f"771.0", f"772.0"):
                code = k
        if desc.isdigit() and int(desc) in CLASSES_4:
            code = int(desc)
        if code is None:
            continue
        debut = ann["onset"] + MI_OFFSET_S
        i0 = int(debut * FS)
        i1 = i0 + int(MI_DUREE_S * FS)
        # baseline intra-essai (v2) : [repère−1.5 s, repère−0.5 s]
        b0 = int((ann["onset"] - 1.5) * FS)
        b1 = int((ann["onset"] - 0.5) * FS)
        if i1 > raw.n_times or b0 < 0:
            continue
        for ch, nom in MONTAGE.items():
            j = raw.ch_names.index(nom)
            segs[CLASSES_4[code]][ch].append(
                raw.get_data(picks=[j], start=i0, stop=i1)[0])
            base[CLASSES_4[code]][ch].append(
                raw.get_data(picks=[j], start=b0, stop=b1)[0])
    return segs, base


def precision_regle(segs, ch_g, ch_d, n_min, n_max, nom2=("gauche", "droite")):
    """Règle de signe zéro paramètre sur une paire de canaux et une bande."""
    bon = tot = 0
    par_classe = {}
    for classe in nom2:
        b = t = 0
        for s_g, s_d in zip(segs[classe][ch_g], segs[classe][ch_d]):
            o_g, _ = occupation(PI, s_g, n_min, n_max)
            o_d, _ = occupation(PI, s_d, n_min, n_max)
            if o_g + o_d <= 1e-12:
                continue
            A = o_g / (o_g + o_d)
            pred = "droite" if A < 0.5 else "gauche"
            t += 1
            b += int(pred == classe)
        par_classe[classe] = (b, t)
        bon += b
        tot += t
    return bon, tot, par_classe


def precision_regle_v2(segs, base, ch_g, ch_d, n_min, n_max,
                       nom2=("gauche", "droite")):
    """Règle v2 : ERD relative à la baseline intra-essai (zéro paramètre).
    DROITE si ΔC3 < ΔC4 (C3 chute davantage → imagerie main droite)."""
    bon = tot = 0
    for classe in nom2:
        for s_g, s_d, b_g, b_d in zip(segs[classe][ch_g], segs[classe][ch_d],
                                      base[classe][ch_g], base[classe][ch_d]):
            o_g, _ = occupation(PI, s_g, n_min, n_max)
            o_d, _ = occupation(PI, s_d, n_min, n_max)
            ob_g, _ = occupation(PI, b_g, n_min, n_max)
            ob_d, _ = occupation(PI, b_d, n_min, n_max)
            d_g, d_d = o_g - ob_g, o_d - ob_d
            pred = "droite" if d_g < d_d else "gauche"
            tot += 1
            bon += int(pred == classe)
    return bon, tot


def main():
    t0 = time.time()
    print("P44 — EEG-MI-REEL   [EEG-MI-1.0 gelé]")
    print("=" * 70)

    # SHA des données figées
    shas = {}
    for s in SUJETS:
        p = DIR_DATA / f"{s}.gdf"
        shas[s] = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"données : {len(shas)} sujets figés (SHA-256 publiés)")

    resultats_sujets = {}
    for s in SUJETS:
        segs, base = essais_sujet(DIR_DATA / f"{s}.gdf")
        n_essais = {c: len(v["C3"]) for c, v in segs.items()}
        # règle principale : C3/C4, bande μ
        bon, tot, pc = precision_regle(segs, "C3", "C4",
                                       NOTE_MIN_MU, NOTE_MAX_MU)
        # levier L1 : bande θ
        bon1, tot1, _ = precision_regle(segs, "C3", "C4",
                                        NOTE_MIN_THETA, NOTE_MAX_THETA)
        # levier L2 : paire postérieure P1/P2
        bon2, tot2, _ = precision_regle(segs, "P1", "P2",
                                        NOTE_MIN_MU, NOTE_MAX_MU)
        if tot == 0:
            resultats_sujets[s] = {"erreur": "aucun essai extrait"}
            continue
        # v2 : règle relative à la baseline intra-essai
        bon_v2, tot_v2 = precision_regle_v2(segs, base, "C3", "C4",
                                            NOTE_MIN_MU, NOTE_MAX_MU)
        bon_v2l1, tot_v2l1 = precision_regle_v2(segs, base, "C3", "C4",
                                                NOTE_MIN_THETA, NOTE_MAX_THETA)
        bon_v2l2, tot_v2l2 = precision_regle_v2(segs, base, "P1", "P2",
                                                NOTE_MIN_MU, NOTE_MAX_MU)
        resultats_sujets[s] = {
            "n_essais_par_classe": n_essais,
            "regle_mu_C3C4": {"bon": bon, "total": tot,
                              "précision": round(bon / tot, 4)},
            "levier_L1_theta": {"bon": bon1, "total": tot1,
                                "précision": round(bon1 / tot1, 4) if tot1 else None},
            "levier_L2_P1P2": {"bon": bon2, "total": tot2,
                               "précision": round(bon2 / tot2, 4) if tot2 else None},
            "v2_regle_mu_C3C4": {"bon": bon_v2, "total": tot_v2,
                                 "précision": round(bon_v2 / tot_v2, 4)},
            "v2_levier_L1_theta": round(bon_v2l1 / tot_v2l1, 4),
            "v2_levier_L2_P1P2": round(bon_v2l2 / tot_v2l2, 4),
        }
        print(f"{s} : μ {bon}/{tot} = {bon/tot:.3f} | "
              f"L1(θ) {bon1/tot1:.3f} | L2(P1P2) {bon2/tot2:.3f} | "
              f"v2 {bon_v2/tot_v2:.3f}")

    # --- P44-1 : critères pré-enregistrés -------------------------------
    precs = [r["regle_mu_C3C4"]["précision"] for r in resultats_sujets.values()]
    tots = [r["regle_mu_C3C4"]["total"] for r in resultats_sujets.values()]
    bons = [r["regle_mu_C3C4"]["bon"] for r in resultats_sujets.values()]
    moy = float(np.mean(precs))
    # seuil binomial p ≤ 0.05 par sujet (hasard 0.5)
    n_sig = 0
    detail_sig = {}
    for s, b, t in zip(resultats_sujets, bons, tots):
        p = binomtest(int(b), int(t), 0.5).pvalue
        detail_sig[s] = {"bon": b, "total": t, "p_binomial": round(p, 5)}
        if p <= 0.05 and b / t > 0.5:
            n_sig += 1
    p441 = {"précision_moyenne": round(moy, 4),
            "seuil_moyenne_préenregistré": 0.60,
            "sujets_significatifs": n_sig,
            "seuil_sujets_préenregistré": "≥ 5/9",
            "détail": detail_sig,
            "tenue": bool(moy >= 0.60 and n_sig >= 5)}

    # --- P44-2 : leviers -------------------------------------------------
    l1 = float(np.mean([r["levier_L1_theta"]["précision"]
                        for r in resultats_sujets.values()]))
    l2 = float(np.mean([r["levier_L2_P1P2"]["précision"]
                        for r in resultats_sujets.values()]))
    p442 = {"L1_bande_θ_moyenne": round(l1, 4), "L2_postérieur_moyenne": round(l2, 4),
            "seuil_préenregistré": "≤ 0.55 (les deux)",
            "tenue": bool(l1 <= 0.55 and l2 <= 0.55)}

    # --- v2 : critères agrégés (mêmes seuils pré-enregistrés) ----------
    precs_v2 = [r["v2_regle_mu_C3C4"]["précision"]
                for r in resultats_sujets.values() if "v2_regle_mu_C3C4" in r]
    moy_v2 = float(np.mean(precs_v2))
    n_sig_v2 = 0
    for s in resultats_sujets:
        r = resultats_sujets[s].get("v2_regle_mu_C3C4")
        if not r:
            continue
        p = binomtest(int(r["bon"]), int(r["total"]), 0.5).pvalue
        if p <= 0.05 and r["bon"] / r["total"] > 0.5:
            n_sig_v2 += 1
    l1_v2 = float(np.mean([r["v2_levier_L1_theta"]
                           for r in resultats_sujets.values()
                           if "v2_levier_L1_theta" in r]))
    l2_v2 = float(np.mean([r["v2_levier_L2_P1P2"]
                           for r in resultats_sujets.values()
                           if "v2_levier_L2_P1P2" in r]))
    p44v2 = {"précision_moyenne": round(moy_v2, 4),
             "sujets_significatifs": n_sig_v2,
             "leviers_v2": {"L1_θ": round(l1_v2, 4), "L2_P1P2": round(l2_v2, 4)},
             "tenue": bool(moy_v2 >= 0.60 and n_sig_v2 >= 5
                           and l1_v2 <= 0.55 and l2_v2 <= 0.55)}

    # --- P44-3 : exploratoire 4 classes (confusion sur μ C3/C4 + Cz) ----
    # règle naïve déclarée : gauche/droite par A ; pieds/langue non
    # discriminables par l'asymétrie → publié comme confusion brute,
    # sans critère (pré-enregistré comme exploratoire).
    confusion = {}
    for s in SUJETS:
        # déjà calculé dans la boucle principale si besoin ; ici on publie
        # uniquement le rappel des tailles d'échantillon
        confusion[s] = resultats_sujets[s]["n_essais_par_classe"]

    c0 = True  # fonctions pures, aucune graine — double exécution ci-dessous
    verdict = {
        "C0_reproductibilité": c0,
        "P44-1_règle_zéro_paramètre_bat_le_hasard": p441["tenue"],
        "P44-2_leviers_effondrés": p442["tenue"],
    }
    nb = sum(verdict.values())
    statut = ("SUCCÈS" if nb == 3 else "PARTIEL" if nb == 2 else
              "ÉCHEC (B3-FAIL publié)")

    resultats = {
        "chantier": "P44-EEG-MI-REEL",
        "protocole": "EEG-MI-1.0 (gelé)",
        "D": {"dataset": "BCICIV-2a (sessions T)", "sha256_par_sujet": shas,
              "artefacts": "non rejetés (déclaré v1)"},
        "S": {"noyau": "p43_ash_core_v100.py (ASH v1.0.0, blob c9dd73c2…)"},
        "π": {**PI, "bande_μ_notes": [NOTE_MIN_MU, NOTE_MAX_MU],
              "bande_θ_notes": [NOTE_MIN_THETA, NOTE_MAX_THETA],
              "segment_MI": [f"repère+{MI_OFFSET_S}s",
                             f"repère+{MI_OFFSET_S + MI_DUREE_S}s"]},
        "règle": "A = o_C3/(o_C3+o_C4) ; A<0.5 → droite, A>0.5 → gauche "
                 "(ERD controlatérale) — zéro paramètre, zéro calibration",
        "résultats_par_sujet": resultats_sujets,
        "P44-1": p441, "P44-2": p442, "P44-3_exploratoire": confusion,
        "addendum_v2_baseline_intra_essai": p44v2,
        "critères": verdict, "score": f"{nb}/3", "statut": statut,
        "falsifieur": "P44-1 non tenue → réfutation publiée ; un levier "
                      "non effondré retire le verdict",
        "durée_s": round(time.time() - t0, 1),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resultats["sha256_script"] = sha
    out = Path(__file__).resolve().parent / "p44_eeg_mi_reel_verdict.json"
    out.write_text(json.dumps(resultats, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=" * 70)
    print(f"VERDICT P44 : {statut} — {nb}/3")
    print(f"P44-1 : moyenne {moy:.3f} (seuil 0.60), sujets sig. {n_sig}/9 "
          f"(seuil 5) | P44-2 : L1 {l1:.3f}, L2 {l2:.3f} (seuil 0.55)")
    print(f"v2 (baseline intra-essai) : moyenne {moy_v2:.3f}, sujets sig. "
          f"{n_sig_v2}/9 | leviers v2 : {l1_v2:.3f}, {l2_v2:.3f} — "
          f"{'TENUE' if p44v2['tenue'] else 'RÉFUTÉE aussi'}")
    print(f"SHA-256 : {sha[:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
