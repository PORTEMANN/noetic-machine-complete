#!/usr/bin/env python3
# P0 - monopole SU(2) ('t Hooft--Polyakov radial) : minimisation L-BFGS.
# E/(4pi v/e) = int dxi [ K'^2 + (K^2-1)^2/(2 xi^2) + (xi H' - H)^2/(2 xi^2)
#                + K^2 H^2 + rho (H^2-1)^2/4 ],  C(rho), C(0)=1 BPS.
# Gradient discret exact valide par differences finies (num = DX * ana).
import os, json
import numpy as np
from scipy.optimize import minimize

RHO  = float(os.environ.get("RHO", "1.0"))
XMAX = float(os.environ.get("XMAX", "30.0"))
DX   = float(os.environ.get("DX", "0.02"))
TAG  = os.environ.get("TAG", f"p0_r{RHO}")
x = np.arange(DX/2, XMAX, DX); N = len(x); xi = x

def d1(u):
    g = np.gradient(u, DX)
    g[0] = (u[1]-u[0])/DX; g[-1] = (u[-1]-u[-2])/DX
    return g

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
    # conditions aux limites dures : on gele x=0 (H=0, K=1)
    EH[0] = 0.0; EK[0] = 0.0
    g = np.concatenate([EH, EK])
    return E, g

H0 = np.tanh(xi); K0 = 1.0/np.cosh(xi)
y0 = np.concatenate([H0, K0])
E0 = energy(H0, K0)
print(f"[P0 {TAG}] depart C={E0:.5f}  (BPS attendu rho=0 : 1 ; rho=1 : ~1.2-1.6)", flush=True)

res = minimize(fg, y0, jac=True, method='L-BFGS-B',
               options={'maxiter': 20000, 'ftol': 1e-14, 'gtol': 1e-10})
H = res.x[:N]; K = res.x[N:]
# reimposer CL
H[0] = 0.0; K[0] = 1.0
C = energy(H, K)
print(f"[P0 {TAG}] convergence L-BFGS : {res.message}", flush=True)
print(f"[P0 {TAG}] C_final={C:.5f}  niter={res.nit}", flush=True)

# decomposition + viriel + profils
Kp = d1(K); Hp = d1(H)
E_gauge = DX*(Kp**2 + (K**2-1)**2/(2*xi**2)).sum()
E_higgs = DX*((xi*Hp - H)**2/(2*xi**2) + K**2*H**2).sum()
E_pot   = DX*(RHO*(H**2-1)**2/4).sum()
viriel = E_higgs + 3*E_pot
# rayon du coeur : ou H atteint 0.5
ih = np.argmin(np.abs(H - 0.5)); xcore = xi[ih]
print(f"[P0 {TAG}] C={C:.5f}  E_gauge(l0)={E_gauge:.5f}  E_higgs(l1)={E_higgs:.5f} "
      f"E_pot(l3)={E_pot:.5f}  viriel(E1+3E3)={viriel:.5f}  coeur_xi={xcore:.2f}", flush=True)
print(f"[P0 {TAG}] H(xi) aux xi=0.5,1,2,4,8 : "
      f"{[round(H[np.argmin(abs(xi-v))],4) for v in (0.5,1,2,4,8)]}", flush=True)
print(f"[P0 {TAG}] K(xi) aux xi=0.5,1,2,4,8 : "
      f"{[round(K[np.argmin(abs(xi-v))],4) for v in (0.5,1,2,4,8)]}", flush=True)

json.dump({"TAG": TAG, "RHO": RHO, "C0": E0, "C_final": C, "niter": int(res.nit),
           "E_gauge": E_gauge, "E_higgs": E_higgs, "E_pot": E_pot, "viriel": viriel,
           "xi": [float(v) for v in xi[::20]], "H": [float(v) for v in H[::20]],
           "K": [float(v) for v in K[::20]]},
          open(f"/mnt/agents/output/e44_data/p0_{TAG}.json", "w"), indent=1)
print(f"[P0 {TAG}] sauve", flush=True)
