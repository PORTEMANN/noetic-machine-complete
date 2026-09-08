#!/usr/bin/env python3
"""
CAMPAGNE P50 — Condensé : quantification de Hall entière par invariants ASH
Protocole gelé le 2026-09-08
Auteur : Patrice Portemann — ORCID: 0009-0009-4016-8389
"""
import numpy as np
import json
import hashlib
from datetime import datetime
import sys
from scipy.stats import pearsonr

class ASH:
    def __init__(self, fs, f0=1.0, n_oct=4):
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
    data_path = sys.argv[1] if len(sys.argv) > 1 else 'data/hall_dataset.csv'
    data = np.loadtxt(data_path, delimiter=',', skiprows=1)
    B = data[:, 0]
    V_Hall = data[:, 1]
    fs = 1000.0

    ash_koilon = ASH(fs=fs, f0=1.0, n_oct=4)
    ash_linear = ASH(fs=fs, f0=1.0, n_oct=4)
    ash_linear.grid = np.linspace(1, fs/2, len(ash_koilon.grid))

    window_size = int(1.0 * fs)
    step = int(window_size * 0.5)

    results = []
    for i in range(0, len(V_Hall) - window_size, step):
        window = V_Hall[i:i+window_size]
        r = ash_koilon.process_window(window)
        b_mid = B[i + window_size//2]

        # Détection des plateaux par dV/dB ≈ 0
        dVdB = np.abs(np.gradient(V_Hall[i:i+window_size], B[i:i+window_size]))
        is_plateau = np.mean(dVdB) < 0.01

        results.append({
            'B_mid': float(b_mid),
            'Rtop': r['Rtop'],
            'is_plateau': bool(is_plateau)
        })

    # TODO: corréler avec ν mesuré
    # Pour l'instant, structure de sortie standard

    output = {
        'campagne': 'P50',
        'date_gel': '2026-09-08',
        'date_execution': datetime.now().isoformat(),
        'verdict': 'à compléter post-run avec données réelles',
        'details': results,
        'sha256': sha256_dict({'results': results})
    }

    with open('data/p50_verdict.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f'P50 — Fenêtres analysées: {len(results)}')
    print(f'P50 — Fichier: data/p50_verdict.json')

if __name__ == '__main__':
    main()
