#!/usr/bin/env python3
"""
Préparation des données P51 — Sleep-EDFx -> NPZ
Auteur : Patrice Portemann — ORCID: 0009-0009-4016-8389
Version 1.0 (2026-09-08) — script manquant de la v1.0 du package.

Entrées : paires PSG.edf / *-Hypnogram.edf (Sleep-EDFx 1.0.0, PhysioNet)
Sortie  : npz avec 'signals' (N, 3000) float64 et 'labels' (N,) int64
          0=Wake, 1=N1, 2=N2, 3=N3, 4=REM
Canal   : EEG Fpz-Cz (100 Hz), epochs de 30 s.
Les classes sont sous-échantillonnées au effectif de la classe minoritaire
(graine fixe 0) pour un diagnostic par paires équilibré.
"""
import numpy as np
import pyedflib
import sys, glob, os

MAP = {'Sleep stage W': 0, 'Sleep stage 1': 1, 'Sleep stage 2': 2,
       'Sleep stage 3': 3, 'Sleep stage 4': 3, 'Sleep stage R': 4}

def load_night(psg_path, hyp_path):
    f = pyedflib.EdfReader(psg_path)
    labels = f.getSignalLabels()
    idx = labels.index('EEG Fpz-Cz')
    fs = f.getSampleFrequency(idx)
    assert int(fs) == 100, f'fs inattendue: {fs}'
    sig = f.readSignal(idx)
    f.close()

    h = pyedflib.EdfReader(hyp_path)
    onsets, durations, descs = h.readAnnotations()
    h.close()

    n_epochs = len(sig) // 3000
    X, y = [], []
    for onset, dur, desc in zip(onsets, durations, descs):
        if desc not in MAP:
            continue
        lab = MAP[desc]
        start_epoch = int(onset // 30)
        n = max(1, int(round(dur / 30)))
        for e in range(start_epoch, start_epoch + n):
            if 0 <= e < n_epochs:
                seg = sig[e*3000:(e+1)*3000]
                if np.std(seg) > 1e-6:  # segment non plat
                    X.append(seg); y.append(lab)
    return X, y

def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else 'edf'
    out_path = sys.argv[2] if len(sys.argv) > 2 else 'data/sleep_edf_segments.npz'
    nights = []
    for psg in sorted(glob.glob(os.path.join(data_dir, '*-PSG.edf'))):
        base = os.path.basename(psg).split('-')[0]  # SC4001E0
        prefix = base[:6]                            # SC4001
        hyps = glob.glob(os.path.join(data_dir, prefix + '*-Hypnogram.edf'))
        if hyps:
            nights.append((psg, hyps[0]))
    print(f'{len(nights)} nuits trouvées')

    X, y = [], []
    for psg, hyp in nights:
        try:
            Xn, yn = load_night(psg, hyp)
            X.extend(Xn); y.extend(yn)
            print(os.path.basename(psg), len(Xn), 'segments')
        except Exception as e:
            print(os.path.basename(psg), 'ERREUR:', e)

    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y, dtype=np.int64)

    # Sous-échantillonnage équilibré (graine 0)
    rng = np.random.default_rng(0)
    counts = [np.sum(y == c) for c in range(5)]
    n_min = min(c for c in counts if c > 0)
    keep = []
    for c in range(5):
        idx = np.where(y == c)[0]
        keep.append(rng.choice(idx, size=min(n_min, len(idx)), replace=False))
    keep = np.sort(np.concatenate(keep))
    X, y = X[keep], y[keep]
    print('Effectifs par classe avant:', counts, '-> après:', [int(np.sum(y==c)) for c in range(5)])

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.savez(out_path, signals=X, labels=y)
    print('Écrit:', out_path, X.shape)

if __name__ == '__main__':
    main()
