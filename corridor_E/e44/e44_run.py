"""E44 — run officiel (protocole figé, sha 42c65a0c...). Usage: python3 e44_run.py A|B <graine>"""
import sys, os, pickle, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e44_core import *

ENS, SEED = sys.argv[1], int(sys.argv[2])
N, A, GAMMA, DT = 64, 2.0, 0.3, 0.05
SNAP_PAS = [400, 900, 1800]
C = 31.5  # centre du récipient (coordonnées des points de grille)

Xg, Yg, Zg = np.meshgrid(np.arange(N), np.arange(N), np.arange(N), indexing='ij')
Rg = np.sqrt((Xg-C)**2 + (Yg-C)**2)
inside   = (Rg < 26) & (Zg >= 2) & (Zg <= 61)
ring     = (Rg >= 26) & (Rg < 28) & (Zg >= 2) & (Zg <= 61)
exterior = ~(inside | ring)
PHI = np.arctan2(Yg-C, Xg-C)

fix_mask, fix_val = None, None
if ENS == 'B':
    fix_mask = ring | exterior
    fix_val = np.zeros((N,)*3, dtype=complex)
    fix_val[ring] = np.exp(4j*PHI[ring])

rng = np.random.default_rng(SEED)
psi = np.exp(1j*rng.uniform(0, 2*np.pi, (N,)*3))
if ENS == 'B':
    psi[~inside] = 0.0
    psi[ring] = np.exp(4j*PHI[ring])

lin = gp_linear(N, A, GAMMA, DT)

def mask_plaq_B(w, ax):
    """met à zéro les plaquettes dont un coin est hors du récipient (masque géométrique)."""
    r = lambda x,a: np.roll(x,-1,a)
    if ax == 0: corners = [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]
    elif ax == 1: corners = [(0,0,0),(0,0,1),(1,0,1),(1,0,0)]
    else: corners = [(0,0,0),(1,0,0),(1,1,0),(0,1,0)]
    keep = np.ones((N,)*3, bool)
    for dx,dy,dz in corners:
        idx = (np.clip(Xg+dx,0,N-1), np.clip(Yg+dy,0,N-1), np.clip(Zg+dz,0,N-1))
        keep &= inside[idx]
    return np.where(keep, w, 0)

def axial_winding(P):
    dx = (P[:,0]-C); dy = (P[:,1]-C)
    ph = np.arctan2(dy, dx)
    ph2 = np.roll(ph,-1)
    return float(np.sum((ph2-ph+np.pi)%(2*np.pi)-np.pi)/(2*np.pi))

results = {'ensemble': ENS, 'seed': SEED, 'snapshots': {}}
t_start = time.time()
for step in range(1, SNAP_PAS[-1]+1):
    psi = gp_step(psi, lin, GAMMA, DT,
                  fix=(fix_mask, fix_val) if ENS=='B' else None)
    if step in SNAP_PAS:
        t = step*DT
        wx,wy,wz = vorticity(psi, amp_gate=0.0)
        if ENS == 'B':
            wx,wy,wz = mask_plaq_B(wx,0), mask_plaq_B(wy,1), mask_plaq_B(wz,2)
        nfaces = int(np.sum(wx!=0)+np.sum(wy!=0)+np.sum(wz!=0))
        fils, anom, amb = trace_filaments(wx,wy,wz)
        loops = [f for f in fils if f['closed'] and not np.any(f['disp']) and f['len']>=6]
        opens = [f for f in fils if not (f['closed'] and not np.any(f['disp']))]
        loops.sort(key=lambda f: -f['len'])
        if len(loops) > 400: loops = loops[:400]
        pairs, polys = [], {}
        import itertools
        for i,j in itertools.combinations(range(len(loops)),2):
            lk = gauss_link_mi(loops[i]['pts'], loops[j]['pts'], N)
            if abs(lk) >= 0.5:
                pairs.append((i,j,round(lk,3)))
                polys[f'{i}_{j}'] = (loops[i]['pts'].astype(np.float32),
                                     loops[j]['pts'].astype(np.float32))
        parent = list(range(len(loops)))
        def find(a):
            while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
            return a
        for i,j,_ in pairs:
            pi,pj = find(i),find(j)
            if pi!=pj: parent[pi]=pj
        cl = {}
        for i,j,_ in pairs:
            cl.setdefault(find(i),set()).update([i,j])
        mult = sorted(len(v) for v in cl.values())
        axial = [f['len'] for f in opens if f['len']>40]
        embr = [round(axial_winding(f['pts']),2) for f in loops]
        results['snapshots'][t] = {
            'nfaces': nfaces, 'nloops': len(loops),
            'loop_lens': [int(f['len']) for f in loops],
            'nopens': len(opens), 'n_axial40': len(axial), 'axial_lens': axial[:10],
            'anom': anom, 'amb': amb, 'pairs': pairs, 'cluster_mult': mult,
            'embrace': embr, 'polys': polys}
        print(f"[{ENS}/{SEED}] t={t:.0f}: faces={nfaces} boucles={len(loops)} "
              f"liées={len(pairs)} ouverts={len(opens)} axial40={len(axial)} anom={anom}",
              flush=True)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'run_{ENS}_{SEED}.pkl')
with open(out,'wb') as f: pickle.dump(results, f)
print(f"[{ENS}/{SEED}] TERMINE en {time.time()-t_start:.0f}s -> {out}", flush=True)
