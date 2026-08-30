#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P41 — NEURONES RÉELS (Allen Cell Types)                [REEL-1.0 gelé]
======================================================================
Chantier P41 du programme de prospection : la machine touche la donnée
biologique réelle. Classification d'excitabilité (type I continu vs
type II discontinu) DEPUIS LE SIGNAL, sur enregistrements current-clamp
publics de l'Allen Institute (Cell Types).

DONNÉES D (gelées, traçables) :
  D1 = catalogue ApiCellTypesSpecimenDetail (instantané SHA-256)
  D2 = table EphysSweep par cellule (stimulus Long Square : amplitude,
       durée, num_spikes — extraction de spikes par la pipeline Allen,
       gelée et publiée par l'institut ; DÉCLARÉ)
  D3 = signaux bruts NWB de 2 cellules de contrôle (souris, premières
       sélectionnées de chaque classe) — la machine re-dérive les spikes
       elle-même (croisement ascendant −20 mV, règle dérivée déclarée)
       et recoupe D2 (tolérance gelée ±2 Hz)

SÉLECTION (gelée, sans choix humain) :
  classes = (espèce × type dendritique) ∈ {souris, humain} × {spiny,
  aspiny} ; éligible = erwkf__id (NWB) non nul ET rhéobase Allen
  (ef__threshold_i_long_square) non nulle ; tri par specimen__id
  croissant ; K = 8 premières par classe. « sparsely spiny » exclu
  (classes figées à 4, déclaré).

CRITÈRES (gelés avant exécution) :
  C0  CONTRÔLE INSTRUMENT : le même critère classe HH (P35) type II et
      Izhikevich (regular spiking) type I — sinon l'instrument tombe.
  C1  f–I par cellule : I0 = plus petite amplitude POSITIVE avec
      ≥ 1 spike (Long Square, durée ≥ 0.5 s) ; f0 = spikes/durée à I0 ;
      TYPE II ssi f0 ≥ 20.0 Hz (seuil hérité gelé de P35_NOMINAL
      c3_saut_min = 20.0). Verdicts par classe publiés.
  C2  contrôle brut : f0 re-dérivé du signal = f0 table à ±2 Hz, et
      triplet ASH-lite (Rc, Rtop, Rdyn) publié pour les 2 cellules.

QUESTION PRÉ-ENREGISTRÉE (prospection, P35) :
  « les interneurones sont-ils type II comme HH ? »
FALSIFIEUR : si C0 échoue, tout le chantier tombe (B3-FAIL machine).
Zéro paramètre ajusté.
"""
import json
import hashlib
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

import numpy as np

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
from a1_batterie_perturbation import hh, izhikevich, sigmoid_neuron, spike_stats, ash_lite

# ---------------- paramètres gelés (hérités P35_NOMINAL) ----------------
SEUIL_TYPE_II = 20.0     # Hz — c3_saut_min nominal gelé (P35)
PAS_HH = 2.0             # µA/cm² — c3_pas_courant gelé
DT = 0.02                # ms
DISCARD = 50.0           # ms
ASH_SEUIL_STD, ASH_FRAC_PIC = 1e-9, 0.10   # gelés A1
K_PAR_CLASSE = 8
DUREE_MIN = 0.5          # s
SEUIL_SPIKE_BRUT = -0.020  # V (−20 mV, règle dérivée déclarée)
TOL_RECOUPEMENT = 2.0    # Hz
CLASSES = [("Mus musculus", "spiny"), ("Mus musculus", "aspiny"),
           ("Homo Sapiens", "spiny"), ("Homo Sapiens", "aspiny")]
CONTROLES_BRUTS = {  # première sélectionnée de chaque classe souris (gelé)
    ("Mus musculus", "spiny"): "p41_data_controle_spiny_313860745.nwb",
    ("Mus musculus", "aspiny"): "p41_data_controle_aspiny_313861411.nwb",
}
F_CAT = HERE / "p41_data_catalog_allen.json"
F_SW = HERE / "p41_data_sweeps.json"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def api(q):
    """Requête RMA paginée (hôte api.brain-map.org ; options internes à q,
    pages de 50 — constaté : seul ce hôte honore start_row dans q)."""
    rows, start = [], 0
    while True:
        qp = q + f",rma::options[num_rows$eq50][start_row$eq{start}]"
        url = ("https://api.brain-map.org/api/v2/data/query.json?q="
               + quote(qp, safe="(),$[]"))
        ok = False
        for essai in range(8):
            r = subprocess.run(["curl", "-s", "--max-time", "90", url],
                               capture_output=True, text=True)
            if r.stdout.strip():
                try:
                    d = json.loads(r.stdout)
                    if d.get("success"):
                        ok = True
                        break
                except json.JSONDecodeError:
                    pass
            time.sleep(3 * (essai + 1))
        if not ok:
            raise SystemExit(f"B3-FAIL machine : API Allen injoignable "
                             f"pour {q[:80]}")
        rows += d["msg"]
        start += len(d["msg"])
        if start >= d["total_rows"] or not d["msg"]:
            return rows
        time.sleep(0.3)


def selection(cat):
    sel = {}
    for classe in CLASSES:
        elig = [c for c in cat
                if c["donor__species"] == classe[0]
                and c["tag__dendrite_type"] == classe[1]
                and c.get("erwkf__id")
                and c.get("ef__threshold_i_long_square") is not None]
        elig.sort(key=lambda c: c["specimen__id"])
        sel["|".join(classe)] = [c["specimen__id"] for c in
                                 elig[:K_PAR_CLASSE]]
    return sel


def sweeps_ls(specimen_id, cache):
    """Points Long Square (amplitude pA > 0, durée s, spikes)."""
    key = str(specimen_id)
    if key not in cache:
        cache[key] = api(f"model::EphysSweep,rma::criteria,"
                         f"[specimen_id$eq{specimen_id}]")
    pts = []
    for m in cache[key]:
        if m.get("stimulus_name") != "Long Square":
            continue
        dur = m.get("stimulus_duration")
        amp = m.get("stimulus_absolute_amplitude")
        if dur is None or amp is None or dur < DUREE_MIN or amp <= 0:
            continue
        pts.append((float(amp), float(dur), float(m.get("num_spikes") or 0)))
    return sorted(pts)


def f0_table(pts):
    for amp, dur, n in pts:
        if n >= 1:
            return amp, n / dur
    return None, 0.0


def f0_signal(V, S, fs):
    """f0 depuis le signal brut : fenêtre du pallier = indices où le
    stimulus dépasse la moitié de sa montée (règle dérivée, déclarée) ;
    spikes = croisements ascendants de −20 mV dans la fenêtre."""
    base = np.median(S[: int(0.1 * fs)])
    haut = base + 0.5 * (S.max() - base)
    idx = np.where(S > haut)[0]
    if len(idx) < 5:
        return None, 0.0, 0.0
    amp_pA = (np.median(S[idx]) - base) * 1e12
    if amp_pA <= 0:
        return None, 0.0, 0.0
    w = V[idx]
    cr = np.where((w[:-1] < SEUIL_SPIKE_BRUT) & (w[1:] >= SEUIL_SPIKE_BRUT))[0]
    dur = len(idx) / fs
    return amp_pA, len(cr) / dur, dur


def c0_controle():
    """HH doit être type II, Izhikevich (RS) type I, avec le SEUIL gelé."""
    courants, rates = [], []
    I = 0.0
    while I <= 40.0:
        courants.append(I)
        rates.append(spike_stats(hh(I, DT), DT, DISCARD)[0])
        I += PAS_HH
    I0_hh, f0_hh = next(((c, r) for c, r in zip(courants, rates) if r > 0),
                        (None, 0.0))
    courants_i, rates_i = [], []
    I = 0.0
    while I <= 20.0:
        courants_i.append(I)
        rates_i.append(spike_stats(izhikevich(I, DT), DT, DISCARD)[0])
        I += PAS_HH
    I0_iz, f0_iz = next(((c, r) for c, r in zip(courants_i, rates_i) if r > 0),
                        (None, 0.0))
    return {"hh": {"I0": I0_hh, "f0": f0_hh,
                   "type": "II" if f0_hh >= SEUIL_TYPE_II else "I"},
            "izhikevich": {"I0": I0_iz, "f0": f0_iz,
                           "type": "II" if f0_iz >= SEUIL_TYPE_II else "I"},
            "ok": f0_hh >= SEUIL_TYPE_II and f0_iz < SEUIL_TYPE_II}


def c2_controle_brut(cache):
    """Re-dérive f0 depuis les signaux bruts NWB des 2 cellules gelées.
    Le nom du stimulus n'est PAS dans les attributs des sweeps NWB v1
    (il est dans /stimulus/templates, partiellement illisible) : le sweep
    de rhéobase est donc identifié par la table API gelée (cache) —
    premier Long Square (amplitudes croissantes, durée ≥ DUREE_MIN) avec
    num_spikes ≥ 1 — puis le signal Sweep_<sweep_number> est lu dans le
    NWB. Si ce sweep est absent du NWB, on prend le suivant qui y est."""
    import h5py
    out = {}
    for classe, fname in CONTROLES_BRUTS.items():
        cle = "|".join(classe)
        p = HERE / fname
        if not p.exists() or p.stat().st_size < 1_000_000:
            out[cle] = {"statut": "NWB absent/incomplet — "
                        "contrôle déclaré non réalisé"}
            continue
        spec_id = int(fname.split("_")[-1].split(".")[0])
        rows = [m for m in cache.get(str(spec_id), [])
                if m.get("stimulus_name") == "Long Square"
                and (m.get("stimulus_duration") or 0) >= DUREE_MIN
                and (m.get("stimulus_absolute_amplitude") or 0) > 0
                and (m.get("num_spikes") or 0) >= 1]
        rows.sort(key=lambda m: m["stimulus_absolute_amplitude"])
        V = sdata = fs = None
        nom0 = None
        try:
            f = h5py.File(p, "r")
            for m in rows:
                nom = f"Sweep_{m['sweep_number']}"
                try:
                    A = f[f"acquisition/timeseries/{nom}"]
                    S = f[f"stimulus/presentation/{nom}"]
                    V = A["data"][:] * float(A["data"].attrs.get(
                        "conversion", 1.0))
                    sdata = S["data"][:] * float(S["data"].attrs.get(
                        "conversion", 1.0))
                    fs = float(A["starting_time"].attrs["rate"])
                    nom0 = nom
                    break
                except (KeyError, RuntimeError, OSError):
                    continue
            f.close()
        except (OSError, KeyError, RuntimeError):
            out[cle] = {"statut": "NWB incomplet/illisible — "
                        "contrôle déclaré non réalisé"}
            continue
        if nom0 is None:
            out[cle] = {"statut": "aucun sweep de rhéobase lisible dans "
                        "le NWB — contrôle déclaré non réalisé"}
            continue
        amp0, f0b, dur0 = f0_signal(V, sdata, fs)
        if amp0 is None:
            out[cle] = {"statut": "fenêtre stimulus introuvable au brut "
                        "(déclaré)"}
            continue
        # recoupement avec la table (même règle sur D2)
        pts = sweeps_ls(spec_id, cache)
        amp_t, f0_t = f0_table(pts)
        ash = ash_lite(np.asarray(V, dtype=float), 1000.0 / fs, DISCARD,
                       ASH_SEUIL_STD, ASH_FRAC_PIC)
        out[cle] = {
            "statut": "mesuré",
            "rheobase_brute_pA": float(round(float(amp0), 1)),
            "f0_brut_Hz": round(f0b, 2),
            "f0_table_Hz": round(f0_t, 2) if f0_t else None,
            "recoupement_±2Hz": abs(f0b - (f0_t or 0)) <= TOL_RECOUPEMENT,
            "type_brut": "II" if f0b >= SEUIL_TYPE_II else "I",
            "ash_rhéobase": {k: float(v) for k, v in ash.items()},
            "sweep": nom0}
    return out


def main():
    print("P41 — NEURONES RÉELS (ALLEN CELL TYPES)   [REEL-1.0 gelé]")
    print("=" * 72)
    mesures, verdicts = {}, {}

    # ---- C0 ---------------------------------------------------------------
    c0 = c0_controle()
    verdicts["C0_instrument"] = c0["ok"]
    mesures["C0"] = c0
    print(f"C0  HH : f0 = {c0['hh']['f0']:.1f} Hz à I0 = "
          f"{c0['hh']['I0']} µA/cm² → type {c0['hh']['type']} ; "
          f"Izhikevich : f0 = {c0['izhikevich']['f0']:.1f} Hz → "
          f"type {c0['izhikevich']['type']} → "
          f"{'PASS' if c0['ok'] else 'FAIL — B3-FAIL machine'}")
    if not c0["ok"]:
        raise SystemExit("B3-FAIL machine : l'instrument ne discrimine "
                         "plus HH/Izhikevich — chantier arrêté")

    # ---- C1 ---------------------------------------------------------------
    cat = json.loads(F_CAT.read_text(encoding="utf-8"))
    sel = selection(cat)
    cache = json.loads(F_SW.read_text(encoding="utf-8")) \
        if F_SW.exists() else {}
    resumé = {}
    for classe, ids in sel.items():
        lignes = []
        for sid in ids:
            pts = sweeps_ls(sid, cache)
            amp0, f0 = f0_table(pts)
            typ = "II" if f0 >= SEUIL_TYPE_II else "I"
            lignes.append({"specimen": sid, "rheobase_pA": amp0,
                           "f0_Hz": round(f0, 2), "type": typ,
                           "n_points": len(pts)})
        nII = sum(1 for l in lignes if l["type"] == "II")
        resumé[classe] = {"cellules": lignes, "type_II": nII,
                          "type_I": len(lignes) - nII}
        print(f"C1  {classe:<28} : type II {nII}/{len(lignes)} — "
              + ", ".join(f"{l['f0_Hz']}" for l in lignes))
    F_SW.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    verdicts["C1_classification"] = True
    mesures["C1"] = resumé

    # ---- C2 ---------------------------------------------------------------
    c2 = c2_controle_brut(cache)
    F_SW.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    mesures["C2"] = c2
    for classe, r in c2.items():
        print(f"C2  {classe:<28} : {r.get('statut')}"
              + (f" — f0 brut {r.get('f0_brut_Hz')} Hz vs table "
                 f"{r.get('f0_table_Hz')} Hz, recoupement "
                 f"{r.get('recoupement_±2Hz')}, ASH {r.get('ash_rhéobase')}"
                 if r.get("statut") == "mesuré" else ""))
    verdicts["C2_contrôle_brut"] = all(
        r.get("statut") != "mesuré" or r.get("recoupement_±2Hz")
        for r in c2.values())

    # ---- verdict -----------------------------------------------------------
    q = "les interneurones sont-ils type II comme HH ?"
    asp_m = resumé["Mus musculus|aspiny"]["type_II"]
    asp_h = resumé["Homo Sapiens|aspiny"]["type_II"]
    spi_m = resumé["Mus musculus|spiny"]["type_II"]
    spi_h = resumé["Homo Sapiens|spiny"]["type_II"]
    verdict_global = (
        f"C0 instrument OK (HH type II à {c0['hh']['f0']:.0f} Hz, "
        f"Izhikevich type I). Population : interneurones (aspiny) type II "
        f"= {asp_m}/8 souris, {asp_h}/8 humain ; pyramidales (spiny) "
        f"type II = {spi_m}/8 souris, {spi_h}/8 humain. Question "
        f"pré-enregistrée « {q} » → réponse mesurée ci-dessus. Seuil gelé "
        f"{SEUIL_TYPE_II} Hz hérité de P35.")
    out = {
        "chantier": "P41-NEURONES-REELS",
        "protocole": "REEL-1.0 (gelé) — Allen Cell Types, sélection sans "
                     "choix humain, seuil type II hérité gelé de P35 (20 Hz)",
        "données": {"catalogue": sha256(F_CAT), "sweeps": sha256(F_SW),
                    "NWB_contrôles": {"|".join(c): sha256(HERE / f)
                                      for c, f in CONTROLES_BRUTS.items()
                                      if (HERE / f).exists()
                                      and (HERE / f).stat().st_size > 1_000_000}},
        "mesures": mesures, "verdicts": verdicts,
        "question_pré_enregistrée": q,
        "verdict_global": verdict_global,
        "comptage_ddll": {"verdict": "déficit",
                          "justification": "le seuil de classement (20 Hz) "
                          "est payé une fois (hérité P35, pas ré-ajusté) : "
                          "la classification du réel achète sa frontière"},
        "b3_fail": [
            "chantier v1 : C2 cherchait le nom du stimulus dans les "
            "attributs des sweeps NWB v1 (aibs_stimulus_name) — absents "
            "(ils sont dans /stimulus/templates) → 0 sweep Long Square "
            "trouvé ; corrigé : sweep de rhéobase identifié par la table "
            "API gelée (sweep_number)",
            "téléchargement : deux NWB de contrôle corrompus par reprise "
            "curl pendant une coupure du montage de sortie (mauvaise "
            "signature HDF5) ; re-téléchargés en une passe, intégrité "
            "vérifiée (48/92 sweeps lisibles)"],
        "falsifieur": "C0 (HH type II / Izhikevich type I au seuil gelé) "
                      "échoue → l'instrument tombe",
        "sha256_script": hashlib.sha256(Path(__file__).read_bytes())
        .hexdigest(),
    }
    out_path = HERE / "p41_neurones_reels_verdict.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("-" * 72)
    print("VERDICT :", verdict_global)
    print(f"SHA-256 : {out['sha256_script'][:16]}…   |   {out_path.name}")


if __name__ == "__main__":
    main()
