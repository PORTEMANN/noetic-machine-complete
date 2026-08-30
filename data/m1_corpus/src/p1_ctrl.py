"""P1 — mesure du gap omega0 en fonction de la boite (test de forme ln(R/xi)/R^2).
Une ligne VIDE (controle le plus propre), mur souple a rayon R0 variable,
coup de pied uniforme sous-maille, frequence de precession du centre par FFT.
Usage: python3 p1_gapscan.py  (env: liste R0 via SCAN)
"""
import sys, os, json, time
import numpy as np
from scipy.ndimage import map_coordinates
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1d2_core import vortex_positions

NZ, NXY, DT = 32, 48, 0.05
GAA, MU_A, U_CORE = 1.0, 1.0, 1.0
N_RELAX = int(os.environ.get("N_RELAX", "1500"))
N_RUN = 12000
SAMP = 5
AMP = 0.05
SCAN = [8.0]

c = (NXY-1)/2.0
zzg, xxg, yyg = np.indices((NZ, NXY, NXY), dtype=float)

def build_lin(damp):
    kz = 2*np.pi*np.fft.fftfreq(NZ)
    kx = 2*np.pi*np.fft.fftfreq(NXY)
    k2 = kz[:,None,None]**2 + kx[None,:,None]**2 + kx[None,None,:]**2
    return np.exp(-(1j+damp)*k2*DT/2.0)

def wall(R0, V0=10.0, p=8):
    r2 = (xxg-c)**2 + (yyg-c)**2
    return V0*(np.sqrt(r2)/R0)**p*np.ones((NZ,1,1))

def step(psi, lin, dt, damp, Vtrap):
    p2 = np.abs(psi)**2
    V = GAA*p2 - MU_A + Vtrap
    psi = psi*np.exp(-(1j+damp)*V*dt/2)
    psi = np.fft.ifftn(np.fft.fftn(psi)*lin)
    psi = np.fft.ifftn(np.fft.fftn(psi)*lin)
    p2 = np.abs(psi)**2
    V = GAA*p2 - MU_A + Vtrap
    psi = psi*np.exp(-(1j+damp)*V*dt/2)
    return psi

results = []
for R0 in SCAN:
    Vt = wall(R0)
    theta = np.arctan2(yyg-c, xxg-c)
    r2c = (xxg-c)**2+(yyg-c)**2
    psi = np.sqrt(r2c/(r2c+U_CORE**2))*np.exp(1j*theta)
    lin = build_lin(0.4)
    for i in range(N_RELAX):
        psi = step(psi, lin, DT, 0.4, Vt)
        psi /= np.sqrt((np.abs(psi)**2).mean()+1e-12)
    # petit deplacement uniforme (0.05 cellule) : excite la precession
    coords = np.array([zzg, xxg-AMP, yyg])
    p = (map_coordinates(psi.real, coords, order=1, mode='nearest')
         + 1j*map_coordinates(psi.imag, coords, order=1, mode='nearest')).astype(np.complex128)
    Xv, Yv = vortex_positions(p)
    Xc, Yc = [], []
    linR = build_lin(0.0)
    t0 = time.time()
    for i in range(N_RUN):
        p = step(p, linR, DT, 0.0, Vt)
        if i % SAMP == 0:
            Xv, Yv = vortex_positions(p, prev=(Xv, Yv))
            Xc.append(float(np.nanmean(Xv))); Yc.append(float(np.nanmean(Yv)))
        if i % 5000 == 0:
            print(f"  R0={R0} run {i}/{N_RUN} t+{time.time()-t0:.0f}s", flush=True)
    Xc = np.array(Xc); Yc = np.array(Yc)
    s = (Xc-Xc.mean()) + 1j*(Yc-Yc.mean())
    nt = len(s)
    A = np.fft.fft(s*np.hanning(nt), n=16*nt)
    om = 2*np.pi*np.fft.fftfreq(16*nt, d=DT*SAMP)
    pos = om > 0
    i2 = np.argmax(np.abs(A[pos]))
    om0 = float(om[pos][i2])
    amp = float(np.sqrt(2*np.mean(np.abs(s)**2)))
    # prediction naive kappa=2pi : (2pi)/(2pi R0^2) ln(R0/xi), xi=1
    om_pred = np.log(R0)/R0**2
    results.append({"R0": R0, "omega0_mesure": om0, "amp": amp, "omega0_pred": om_pred,
                    "ratio": om0/om_pred if om_pred > 0 else 0.0})
    print(f"[P1] R0={R0} : omega0={om0:.5f} (pred naive {om_pred:.5f}, ratio {om0/om_pred:.2f}) amp={amp:.3f}",
          flush=True)

np.savez("/mnt/agents/output/e44_data/p1_ctrl.npz", Xc=Xc, Yc=Yc, dt_samp=DT*SAMP)
print("[P1] sauve p1_gapscan.json")
