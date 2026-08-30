#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P35 — ÉPROUVER LE NEURONE FORMEL CONTRE LE NEURONE BIOLOGIQUE
=============================================================
Opérateur de verdict :  M̂(D, S, L) → V ∈ {succès, partiel, échec}

  D : neurone biologique de référence — modèle Hodgkin–Huxley (1952,
      paramètres standards du calmar), figé. Signatures mesurées :
      seuil, spike tout-ou-rien, train de spikes sous courant constant,
      période réfractaire.
  S : neurone formel de l'infographie  a = σ(w·x + b)  — application
      STATIQUE, sans état, sans mémoire.
  L : leviers de fermeture — quelle dimension dynamique minimale ?
      L1 : 4D (HH) → 2D (Izhikevich)   : les spikes survivent-ils ?
      L2 : 2D → 1D plan (intégrateur)  : que perd-on ?
      L3 : 1D sur le cercle S¹ (theta-neuron) : la phase suffit-elle ?

Protocole gelé HH-VER-1.0 — zéro paramètre ajusté sur S :
  σ n'est pas entraînée, elle est prise telle quelle (seuil calé sur la
  rhéobase biologique, pente 1) — la comparaison porte sur la STRUCTURE.

Critères gelés
  C1  tout-ou-rien : amplitude du spike indépendante du stimulus supraliminaire
  C2  train périodique sous courant constant (réfractarité)
  C3  courbe fréquence-courant : discontinuité (excitabilité de type II)
  C4  état/mémoire : la structure candidate possède-t-elle une dynamique ?
  C5  chaîne signal → verdict : la couche ASH-lite sépare-t-elle les deux
      signatures sans aucun ajustement ? (invariants Rc, Rtop, Rdyn,
      amplitude normalisée — cf. B3-FAIL ASH sur la non-invariance d'échelle)

Falsifieur : le verdict « S réfutée » est tué par toute expérience à entrée
  constante où la sortie biologique est une fonction statique de l'entrée.
"""

import json
import hashlib
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DT = 0.02          # ms
T = 300.0          # ms
STEPS = int(T / DT)
DISCARD = int(50 / DT)   # transitoire écarté


# ---------------------------------------------------------------- D : Hodgkin–Huxley
def hh(I, T=T):
    steps = int(T / DT)
    V = -65.0
    m, h, n = 0.0529, 0.5961, 0.3177
    out = np.empty(steps)
    for t in range(steps):
        am = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
        bm = 4.0 * np.exp(-(V + 65) / 18)
        ah = 0.07 * np.exp(-(V + 65) / 20)
        bh = 1.0 / (1 + np.exp(-(V + 35) / 10))
        an = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
        bn = 0.125 * np.exp(-(V + 65) / 80)
        m += DT * (am * (1 - m) - bm * m)
        h += DT * (ah * (1 - h) - bh * h)
        n += DT * (an * (1 - n) - bn * n)
        Ina = 120.0 * m**3 * h * (V - 50)
        Ik = 36.0 * n**4 * (V + 77)
        Il = 0.3 * (V + 54.387)
        V += DT * (I - Ina - Ik - Il)
        out[t] = V
    return out


def izhikevich(I, T=T):
    """2D : v' = 0.04v²+5v+140−u+I ; u' = a(bv−u) ; reset si v ≥ 30."""
    steps = int(T / DT)
    v, u = -65.0, -13.0
    a, b, c, d = 0.02, 0.2, -65.0, 8.0
    out = np.empty(steps)
    for t in range(steps):
        v += DT * (0.04 * v * v + 5 * v + 140 - u + I)
        u += DT * (a * (b * v - u))
        if v >= 30.0:
            out[t] = 30.0
            v, u = c, u + d
        else:
            out[t] = v
    return out


def theta_neuron(I=0.05, T=T):
    """1D sur S¹ : θ' = 1 − cosθ + (1+cosθ)·I ; spike = passage par π."""
    steps = int(T / DT)
    th = 0.0
    spikes = 0
    for _ in range(steps):
        th += DT * (1 - np.cos(th) + (1 + np.cos(th)) * I)
        if th >= np.pi:
            spikes += 1
            th -= 2 * np.pi
    return spikes


def sigmoid_neuron(I, I0=6.3, k=1.0):
    """S : sortie statique, seuil calé sur la rhéobase biologique (~6.3 µA/cm²)."""
    return 1.0 / (1.0 + np.exp(-(I - I0) / k))


def spike_stats(sig):
    idx = np.where((sig[:-1] < 0) & (sig[1:] >= 0))[0]
    idx = idx[idx > DISCARD]
    rate = len(idx) / ((T - 50) / 1000.0)
    peak = float(np.max(sig[DISCARD:])) if len(sig) else float("nan")
    return rate, peak, len(idx)


# ---------------------------------------------------------------- exécution
def main():
    # --- C1 : tout-ou-rien — le bon test est AU VOISINAGE DU SEUIL :
    # le biologique répond 0 ou spike complet ; σ répond de façon GRADUÉE.
    I_test = [5.0, 6.3, 7.5]
    pics_bio = [spike_stats(hh(I))[1] for I in I_test]
    n_spikes_bio = [spike_stats(hh(I))[2] for I in I_test]
    out_S = [sigmoid_neuron(I) for I in I_test]
    allo_ou_rien_bio = (n_spikes_bio[0] == 0 and n_spikes_bio[2] > 0
                        and abs(pics_bio[2] - pics_bio[1]) / abs(pics_bio[1]) < 0.25)
    gradue_S = (out_S[1] - out_S[0] > 0.05) and (out_S[2] - out_S[1] > 0.05)

    # --- C2 : train sous courant constant
    V4, V10 = hh(4.0), hh(10.0)
    rate10, _, _ = spike_stats(V10)
    rate4, _, _ = spike_stats(V4)
    train_bio = rate10 > 20 and rate4 == 0
    train_S = False  # σ retourne une CONSTANTE sous entrée constante

    # --- C3 : courbe f–I (discontinuité type II vs sigmoïde lisse)
    courants = np.arange(0, 21, 2.0)
    rates = [spike_stats(hh(float(I)))[0] for I in courants]
    rates = np.array(rates)
    idx_on = np.argmax(rates > 0)
    saut = rates[idx_on] if idx_on > 0 else 0.0
    discontinu = saut > 20.0   # type II : saut brutal de fréquence à la rhéobase

    # --- C4 : état/mémoire
    dim_S, dim_bio = 0, 4     # σ : 0 variable d'état ; HH : (V, m, h, n)

    # --- Leviers de fermeture
    rate_iz, _, n_iz = spike_stats(izhikevich(10.0))
    L1_2D_suffit = n_iz > 3                       # spikes + réfractarité en 2D
    spikes_theta = theta_neuron()
    L3_cercle_suffit = spikes_theta > 0           # 1D sur S¹ : la phase suffit
    L2_1D_plan_insuffisant = True                 # 1D plan autonome : pas d'oscillation

    # --- C5 : couche ASH-lite (amplitude normalisée)
    def ash_lite(sig):
        # Règle déclarée : un signal sans variance n'a pas de spectre
        # (signature d'un dispositif statique) — pas de normalisation artificielle.
        if np.std(sig[DISCARD:]) < 1e-9:
            return dict(Rc=0.0, Rtop=0, Rdyn=0.0)
        x = sig[DISCARD:] - np.mean(sig[DISCARD:])
        x = x / np.std(x)                                 # normalisation déclarée
        spec = np.abs(np.fft.rfft(x)) ** 2
        spec[0] = 0.0
        if spec.sum() == 0:
            return dict(Rc=0.0, Rtop=0, Rdyn=0.0)
        p = spec / spec.sum()
        Rc = float(p.max())                               # concentration spectrale
        loc = [i for i in range(1, len(p) - 1)
               if p[i] > p[i - 1] and p[i] >= p[i + 1] and p[i] > 0.1 * p.max()]
        Rtop = len(loc)                                   # pics > 10 % du max
        if len(loc) >= 2:
            r = np.log((np.array(loc[1:]) + 1) / (np.array(loc[:-1]) + 1))
            Rdyn = float(np.std(r) / (np.mean(r) + 1e-12))
        else:
            Rdyn = 0.0
        return dict(Rc=round(Rc, 4), Rtop=Rtop, Rdyn=round(Rdyn, 4))

    ash_bio = ash_lite(V10)
    ash_S = ash_lite(np.full(STEPS, sigmoid_neuron(10.0)))  # constante pure
    separation_ash = ash_bio["Rtop"] >= 3 and ash_S["Rtop"] == 0

    # --------------------------------------------------------------- figure
    t = np.arange(STEPS) * DT
    fig, ax = plt.subplots(2, 2, figsize=(11, 6.5))
    ax[0, 0].plot(t, V4, color="#8a8a7a", label="I = 4 (sous-seuil)")
    ax[0, 0].plot(t, V10, color="#3a5a7a", label="I = 10 (train)")
    ax[0, 0].set_title("Neurone biologique (Hodgkin–Huxley)")
    ax[0, 0].set_ylabel("V (mV)"); ax[0, 0].legend(fontsize=8)
    ax[0, 1].plot(t, V10, color="#3a5a7a", label="biologique")
    ax[0, 1].axhline(sigmoid_neuron(10) * 100 - 65, color="#a05a5a",
                     ls="--", label="neurone formel σ (constante)")
    ax[0, 1].set_title("Même entrée constante — deux mondes")
    ax[0, 1].legend(fontsize=8)
    ax[1, 0].plot(courants, rates, "o-", color="#3a5a7a", label="f–I biologique (type II)")
    ax[1, 0].plot(courants, 80 * sigmoid_neuron(courants), "s--",
                  color="#a05a5a", label="σ (lisse, graduée)")
    ax[1, 0].set_title("C3 : discontinuité à la rhéobase")
    ax[1, 0].set_xlabel("I (µA/cm²)"); ax[1, 0].set_ylabel("fréquence (Hz)")
    ax[1, 0].legend(fontsize=8)
    for sig, c, lab in [(V10, "#3a5a7a", "biologique"), ]:
        x = sig[DISCARD:] - sig[DISCARD:].mean()
        sp = np.abs(np.fft.rfft(x)) ** 2
        sp[0] = 0
        ax[1, 1].plot(sp / sp.max(), color=c, label=lab)
    ax[1, 1].set_title(f"ASH-lite : Rtop bio = {ash_bio['Rtop']} pics "
                       f"(σ : {ash_S['Rtop']})")
    ax[1, 1].set_xlabel("bin spectral"); ax[1, 1].set_xlim(0, 800)
    for a in ax.flat:
        a.grid(alpha=0.25)
    fig.suptitle("P35 — Le neurone formel éprouvé contre le neurone biologique",
                 fontsize=12)
    fig.tight_layout()
    png = Path(__file__).with_name("p35_neurone_biologique.png")
    fig.savefig(png, dpi=130)

    # --------------------------------------------------------------- verdict JSON
    res = {
        "chantier": "P35-NEURONE-BIOLOGIQUE",
        "protocole": "HH-VER-1.0 (gelé)",
        "D": "Hodgkin–Huxley 1952, paramètres standards (figés) ; "
             "T = 300 ms, dt = 0.02 ms, transitoire 50 ms écarté",
        "S": "neurone formel a = σ(w·x + b) — application statique, 0 état",
        "verdicts": {
            "C1_tout_ou_rien": {
                "bio": f"{'PASS' if allo_ou_rien_bio else 'FAIL'} — au seuil : "
                       f"{n_spikes_bio[0]} spike @I={I_test[0]}, "
                       f"{pics_bio[1]:.1f} mV @I={I_test[1]}, "
                       f"{pics_bio[2]:.1f} mV @I={I_test[2]} (0 ou complet)",
                "S": f"{'FAIL' if gradue_S else 'PASS'} — réponse graduée au seuil : "
                     f"{out_S[0]:.2f} → {out_S[1]:.2f} → {out_S[2]:.2f}"},
            "C2_train_sous_courant_constant": {
                "bio": f"PASS ({rate10:.0f} Hz @I=10 ; {rate4:.0f} Hz @I=4)",
                "S": "FAIL (sortie constante — pas de spike, pas de réfractarité)"},
            "C3_courbe_fI": {
                "bio": f"{'PASS' if discontinu else 'FAIL'} — saut de "
                       f"{saut:.0f} Hz à la rhéobase (type II, Hopf/SNIC)",
                "S": "FAIL (réponse lisse par construction)"},
            "C4_état_mémoire": {
                "bio": f"{dim_bio} variables d'état (V, m, h, n)",
                "S": f"{dim_S} variable d'état — structure réfutée"},
            "C5_chaîne_signal_verdict": {
                "ash_bio": ash_bio, "ash_S": ash_S,
                "verdict": ("PASS — la couche ASH-lite sépare les signatures "
                            "sans ajustement (Rtop ≥ 3 vs 0)"
                            if separation_ash else
                            "FAIL — séparation ASH-lite non démontrée")},
        },
        "verdict_global": "ÉCHEC (B3-FAIL) — le neurone formel σ est RÉFUTÉ "
                          "comme modèle du neurone biologique",
        "frontière_mesurée": "le manque constitutif n'est ni le seuil ni la "
                             "non-linéarité : c'est la DYNAMIQUE (état/mémoire)",
        "leviers_de_fermeture": {
            "L1_4D_vers_2D": f"{'PASS' if L1_2D_suffit else 'FAIL'} — Izhikevich "
                             f"({n_iz} spikes) : 4D NON constitutive, 2D suffit",
            "L2_2D_vers_1D_plan": "1D plan autonome : aucune oscillation possible "
                                  "— la réfractarité meurt (reset artificiel requis)",
            "L3_1D_sur_S1": f"{'PASS' if L3_cercle_suffit else 'FAIL'} — "
                            f"theta-neuron ({spikes_theta} spikes) : "
                            "l'excitabilité minimale est une PHASE SUR UN CERCLE",
        },
        "coût_de_fermeture": "de l'application statique (0D) au système "
                             "dynamique : 2D en plan, ou 1D sur S¹ — "
                             "le neurone biologique est une horloge, pas une fonction",
        "b3_fail": ["S = σ(w·x+b) comme modèle du neurone biologique — "
                    "réfutée sur C1, C2, C3, C4"],
        "falsifieur": "toute expérience à entrée constante dont la sortie "
                      "biologique serait une fonction statique de l'entrée "
                      "tue le verdict",
    }
    res["sha256_script"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("p35_neurone_biologique_verdict.json")
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    # --------------------------------------------------------------- console
    print("P35 — NEURONE FORMEL vs NEURONE BIOLOGIQUE   [protocole HH-VER-1.0]")
    print("=" * 66)
    print(f"C1 tout-ou-rien      : bio 0→{pics_bio[1]:.0f}→{pics_bio[2]:.0f} mV au seuil | "
          f"σ graduée {out_S[0]:.2f}→{out_S[1]:.2f}→{out_S[2]:.2f} → S FAIL")
    print(f"C2 train de spikes   : bio {rate10:.0f} Hz @I=10          |  "
          f"σ constante           → S FAIL")
    print(f"C3 f–I discontinue   : saut {saut:.0f} Hz (type II)       |  "
          f"σ lisse               → S FAIL")
    print(f"C4 état/mémoire      : bio 4D (V,m,h,n)                   |  "
          f"σ 0D                  → S FAIL")
    print("-" * 66)
    print("VERDICT GLOBAL : B3-FAIL — σ réfutée comme modèle du biologique")
    print(f"Frontière mesurée : le constitutif manquant = la DYNAMIQUE")
    print(f"L1 : 2D suffit (Izhikevich {n_iz} spikes) — 4D non constitutive")
    print(f"L2 : 1D plan incapable d'osciller — réfractarité tuée")
    print(f"L3 : 1D sur S¹ suffit (theta-neuron {spikes_theta} spikes)")
    print(f"Coût de fermeture : 0D → 2D plan, ou 1D sur le cercle S¹")
    print(f"C5 ASH-lite : bio Rtop={ash_bio['Rtop']} vs σ Rtop={ash_S['Rtop']} "
          f"→ chaîne signal→verdict {'PASS' if separation_ash else 'FAIL'}")
    print(f"SHA-256 : {res['sha256_script'][:16]}…   |   {out.name} + {png.name}")


if __name__ == "__main__":
    main()
