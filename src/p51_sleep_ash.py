#!/usr/bin/env python3
"""
CAMPAGNE P51 — Neuroscience : séparabilité des régimes de sommeil par invariants ASH
Protocole gelé le 2026-09-08
Auteur : Patrice Portemann — ORCID: 0009-0009-4016-8389

Version 1.1 (2026-09-08) — correctifs documentés (CHANGELOG) :
  B1. Rtop_norm := Rtop / max(Rtop, 1) valait toujours 1.0 dès qu'un pic
      existait (feature dégénérée). Remplacé par Rtop / N_points_de_grille.
  B2. Rdyn_norm := Rdyn / Rc mélangeait deux échelles sans rapport.
      Remplacé par Rdyn brut (déjà un ratio sans dimension).
  B3. Le split train/test prenait les 70% premiers de chaque classe
      (biais d'ordre). Remplacé par un tirage stratifié à graine fixe (0).
  B4. Ajout de accuracy_globale et du levier discriminant dans le verdict
      (présents dans le JSON de démo mais non produits par la v1.0).
  NB. Le champ "accuracy_avec_ReN_brut" du JSON de démo n'est reproduit
      par aucun script livré ; il est retiré du schéma (cf. CAMPAIGNS.md).
Données : Sleep-EDFx 1.0.0 (PhysioNet), EEG Fpz-Cz, segments 30 s @100 Hz.
"""
import numpy as np
import json
import hashlib
import os
from datetime import datetime
import sys
from scipy.spatial.distance import euclidean
from itertools import combinations

class ASH:
    def __init__(self, fs, f0=0.5, n_oct=5):
        self.fs = fs
        self.f0 = f0
        self.n_oct = n_oct
        self.grid = np.array([f0 * (2 ** (n / 12)) for n in range(n_oct * 12 + 1)])
        self.grid = self.grid[self.grid < fs / 2]

    def process_window(self, signal):
        n = len(signal)
        freqs = np.fft.rfftfreq(n, d=1.0/self.fs)
        amps = np.abs(np.fft.rfft(signal))
        grid_amps = np.interp(self.grid, freqs, amps, left=0, right=0)
        Rc = np.sum(grid_amps ** 2)
        max_amp = np.max(grid_amps) if np.max(grid_amps) > 0 else 1e-12
        threshold = 0.10 * max_amp
        Rtop = 0
        for i in range(1, len(grid_amps) - 1):
            if grid_amps[i] > threshold and grid_amps[i] > grid_amps[i-1] and grid_amps[i] > grid_amps[i+1]:
                Rtop += 1
        Rdyn = 0.0
        if Rtop >= 2:
            peaks = [self.grid[i] for i in range(1, len(grid_amps)-1)
                     if grid_amps[i] > threshold and grid_amps[i] > grid_amps[i-1] and grid_amps[i] > grid_amps[i+1]]
            if len(peaks) >= 2:
                fund = peaks[0]
                ratios = [p / fund for p in peaks[1:]]
                dys = [min(abs(r - round(r)), 0.5) for r in ratios]
                Rdyn = np.mean(dys)
        return {'Rc': float(Rc), 'Rtop': int(Rtop), 'Rdyn': float(Rdyn)}

def sha256_dict(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else 'data/sleep_edf_segments.npz'

    # Format attendu : npz avec 'signals' (N, 3000) et 'labels' (N,)
    data = np.load(data_path)
    signals = data['signals']
    labels = data['labels']
    classes = ['Wake', 'N1', 'N2', 'N3', 'REM']
    fs = 100.0

    ash = ASH(fs=fs, f0=0.5, n_oct=5)
    n_grid = len(ash.grid)

    features = []
    for i, (sig, label) in enumerate(zip(signals, labels)):
        r = ash.process_window(sig)
        Rtop_norm = r['Rtop'] / n_grid   # B1 : proportion de pics sur la grille
        Rdyn_norm = r['Rdyn']            # B2 : ratio sans dimension, brut
        features.append({
            'class': classes[int(label)],
            'Rtop_norm': float(Rtop_norm),
            'Rdyn_norm': float(Rdyn_norm)
        })

    # Séparation train/test (70/30 par classe, tirage stratifié graine fixe) — B3
    rng = np.random.default_rng(0)
    train_feats = []
    test_feats = []
    for cls in classes:
        cls_feats = [f for f in features if f['class'] == cls]
        idx = rng.permutation(len(cls_feats))
        n_train = int(len(cls_feats) * 0.7)
        train_feats.extend(cls_feats[i] for i in idx[:n_train])
        test_feats.extend(cls_feats[i] for i in idx[n_train:])

    # Centroïdes
    centroids = {}
    for cls in classes:
        cls_data = [(f['Rtop_norm'], f['Rdyn_norm']) for f in train_feats if f['class'] == cls]
        if cls_data:
            centroids[cls] = (np.mean([x[0] for x in cls_data]), np.mean([x[1] for x in cls_data]))

    def classify(feat):
        x, y = feat['Rtop_norm'], feat['Rdyn_norm']
        best_cls, best_dist = None, float('inf')
        for cls, (cx, cy) in centroids.items():
            d = euclidean([x, y], [cx, cy])
            if d < best_dist:
                best_dist, best_cls = d, cls
        return best_cls

    # Accuracy globale — B4
    correct_all = sum(1 for f in test_feats if classify(f) == f['class'])
    accuracy_globale = correct_all / len(test_feats) if test_feats else 0.0

    # Évaluation par paires
    pair_accuracies = {}
    for cls1, cls2 in combinations(classes, 2):
        test_pair = [f for f in test_feats if f['class'] in [cls1, cls2]]
        if test_pair:
            correct = sum(1 for f in test_pair if classify(f) == f['class'])
            pair_accuracies[f"{cls1}/{cls2}"] = round(correct / len(test_pair), 3)

    separated = [p for p, acc in pair_accuracies.items() if acc > 0.70]
    score = len(separated)

    verdict = 'succès' if score >= 7 else ('partiel' if score >= 4 else 'B3-FAIL')

    output = {
        'campagne': 'P51',
        'date_gel': '2026-09-08',
        'date_execution': datetime.now().isoformat(),
        'source_donnees': 'Sleep-EDFx 1.0.0 (PhysioNet) — EEG Fpz-Cz, segments 30 s',
        'n_segments': int(len(signals)),
        'accuracy_globale': round(accuracy_globale, 3),
        'pairs_separees_70plus': f'{score}/10',
        'pair_accuracies': pair_accuracies,
        'verdict': verdict,
        'levier_discriminant': {
            'accuracy_normalisee': round(accuracy_globale, 3),
            'effondrement': bool(accuracy_globale < 0.40)
        },
        'sha256': sha256_dict({'pair_accuracies': pair_accuracies, 'score': score})
    }

    os.makedirs('data', exist_ok=True)
    with open('data/p51_verdict.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f'P51 — Accuracy globale: {accuracy_globale:.3f}')
    print(f'P51 — Paires séparées >70%: {score}/10')
    print(f'P51 — Verdict: {verdict}')
    print(f'P51 — Fichier: data/p51_verdict.json')

if __name__ == '__main__':
    main()
