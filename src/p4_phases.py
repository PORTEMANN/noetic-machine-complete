#!/usr/bin/env python3
# P4 - diagramme de phases du monopole de banc : balayage de rho = lambda/e^2.
# rho est le parametre constitutif qui controle le regime :
#   rho -> 0 : limite BPS (jauge domine) ; rho grand : Higgs rigide (jauge negligeable).
# Invariants mesures par point : masse C(rho), rayon de coeur, E_gauge (l0),
# E_higgs (l1), E_pot (l3), et le viriel. La transition de regime se lit dans
# le rapport des energies et la taille du coeur.
import os, json
import numpy as np
from scipy.optimize import minimize

XMAX, DX = 30.0, 0.02
x = np.arange(DX/2, XMAX, DX); N = len(x); xi = x

def d1(u):
    g = np.gradient(u, DX)
    g[0] = (u[1]-u[0])/DX; g[-1] = (u[-1]-u[-2])/DX
    return g

def solve(RHO):
    def energy(H, K):
        Kp = d1(K); Hp = d1(H)
        e = Kp**2 + (K**2-1)**2/(2*xi**2) + (xi*Hp - H)**2/(2*xi**2) \
            + K**2*H**2 + RHO*(H**2-1)**2/4
        return DX*e.sum()
    def fg(y):
        H = y[:N]; K = y[N:]
        Kp = d1(K); Hp = d1(H); Hpp = d1(Hp)
        E = energy(H, K)
        EK = DX*(-2*d1(Kp) + 2*K*(K**2-1)/xi**2 + 2*K*H**2)
        EH = DX*(-Hpp + d1(H/xi) - Hp/xi + H/xi**2 + 2*K**2*H + RHO*H*(H**2-1))
        EH[0] = 0.0; EK[0] = 0.0
        return E, np.concatenate([EH, EK])
    H0 = np.tanh(xi); K0 = 1.0/np.cosh(xi)
    y0 = np.concatenate([H0, K0])
    res = minimize(fg, y0, jac=True, method='L-BFGS-B',
                   options={'maxiter': 8000, 'ftol': 1e-14, 'gtol': 1e-10})
    H = res.x[:N]; K = res.x[N:]
    H[0] = 0.0; K[0] = 1.0
    C = energy(H, K)
    Kp = d1(K); Hp = d1(H)
    E_gauge = DX*(Kp**2 + (K**2-1)**2/(2*xi**2)).sum()
    E_higgs = DX*((xi*Hp - H)**2/(2*xi**2) + K**2*H**2).sum()
    E_pot   = DX*(RHO*(H**2-1)**2/4).sum()
    # rayon de coeur : ou K tombe a 1/2 (habillage) et H monte a 1/2
    iK = np.argmin(np.abs(K - 0.5)); iH = np.argmin(np.abs(H - 0.5))
    return {"rho": RHO, "C": C, "E_gauge": E_gauge, "E_higgs": E_higgs,
            "E_pot": E_pot, "viriel": E_higgs + 3*E_pot,
            "r_gauge": float(xi[iK]), "r_higgs": float(xi[iH]),
            "conv": bool(res.success)}

RHOS = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0]
out = []
for RHO in RHOS:
    r = solve(RHO)
    out.append(r)
    print(f"[P4] rho={RHO:6.2f}  C={r['C']:.4f}  r_gauge={r['r_gauge']:5.2f} "
          f"r_higgs={r['r_higgs']:5.2f}  Eg={r['E_gauge']:.3f} Eh={r['E_higgs']:.3f} "
          f"Ep={r['E_pot']:.3f}  conv={r['conv']}", flush=True)

json.dump({"XMAX": XMAX, "DX": DX, "scan": out},
          open("/mnt/agents/output/e44_data/p4_phases.json", "w"), indent=1)
print("[P4] sauve", flush=True)
