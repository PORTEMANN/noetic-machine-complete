"""P2bis v2 — flexion TROIS POINTS (remplace la methode des rails, contaminee).
Principe : pinning repulsif sur 3 tranches seulement (z=0 et z=NZ-1 a x=c ;
z=NZ//2 a x=c+A). La ligne est LIBRE et droite entre les appuis : pas de
gouttiere le long de la ligne, pas d'approximation petite pente.
  E(A)-E(0) = T_eff * DeltaL,  DeltaL = 2 sqrt((L/2)^2+A^2) - L  (exact)
Controle sans vortex soustrait (energie propre des appuis).
Controle attendu : ligne vide -> T ~ 11-13 (Kelvin / dispersion P1-P2).
Usage: python3 p2bis2_troispoints.py <m_ratio> [chi_frac]  env: AMPS, N_RELAX, W_PIN
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1d2_core import soft_wall, vortex_positions

M_RATIO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
CHI_FRAC = float(sys.argv[2]) if len(sys.argv) > 2 else (0.0 if M_RATIO <= 1.0 else 1.0)

NZ, NXY, DT = 32, 48, 0.05
GAA, MU_A, U_CORE = 1.0, 1.0, 1.0
GBB = GAA
DELTA = float(os.environ.get("DELTA", "0.5"))
GAB = np.sqrt(GAA*GBB)*(1.0+DELTA)
MU_B = float(os.environ.get("MU_B", "1.0"))
SIG_CHI = float(os.environ.get("SIG_CHI", "2.0"))
N_RELAX = int(os.environ.get("N_RELAX", "2500"))
AMPS = [float(s) for s in os.environ.get("AMPS", "0,2,4,6,8").split(",")]
W_PIN = float(os.environ.get("W_PIN", "4.0"))
S_PIN = 1.5

c = (NXY-1)/2.0
zzg, xxg, yyg = np.indices((NZ, NXY, NXY), dtype=float)
zz = np.arange(NZ)
Vt = soft_wall(NZ, NXY, 16.0, 10.0)

kz = 2*np.pi*np.fft.fftfreq(NZ)
kx = 2*np.pi*np.fft.fftfreq(NXY)
K2 = kz[:,None,None]**2 + kx[None,:,None]**2 + kx[None,None,:]**2

def build_lin(damp, m_ratio=1.0):
    return np.exp(-(1j+damp)*K2*DT/2.0/m_ratio)

def step(psi, lin, dt, damp, g_self, g_ab, other2, mu, Vtrap, m_ratio=1.0):
    p2 = np.abs(psi)**2
    V = g_self*p2 + g_ab*other2 - mu + Vtrap
    psi = psi*np.exp(-(1j+damp)*V*dt/2)
    psi = np.fft.ifftn(np.fft.fftn(psi)*lin)
    psi = np.fft.ifftn(np.fft.fftn(psi)*lin)
    p2 = np.abs(psi)**2
    V = g_self*p2 + g_ab*other2 - mu + Vtrap
    psi = psi*np.exp(-(1j+damp)*V*dt/2)
    return psi

def pins(A):
    """3 appuis repulsifs ponctuels : extremites a x=c, milieu a x=c+A."""
    V = np.zeros((NZ, NXY, NXY))
    def spot(z, x0):
        r2 = (xxg[z]-x0)**2 + (yyg[z]-c)**2
        V[z] += W_PIN*np.exp(-r2/(2*S_PIN**2))
    for z in (0, NZ-1):
        spot(z, c)
    spot(NZ//2, c+A)
    spot(NZ//2-1, c+A)
    return V

def energie_interne(psi, chi):
    ph = np.fft.fftn(psi)
    kin_p = 0.5*np.sum(K2*np.abs(ph)**2)/psi.size
    ch = np.fft.fftn(chi)
    kin_c = 0.5/M_RATIO*np.sum(K2*np.abs(ch)**2)/chi.size
    p2 = np.abs(psi)**2; c2 = np.abs(chi)**2
    pot = np.sum(0.5*GAA*p2**2 + 0.5*GBB*c2**2 + GAB*p2*c2
                 - MU_A*p2 - MU_B*c2)
    return float(kin_p+kin_c+pot)

def relax_etat(A, avec_vortex=True):
    # condition initiale : ligne deja en tente xc(z) (la relaxation amortie est
    # locale — le vortex ne peut pas sauter vers un appui lointain)
    xcz = c + A*(1.0 - np.abs(zz - NZ/2)/(NZ/2))
    r2t = np.zeros((NZ, NXY, NXY))
    for z in range(NZ):
        r2t[z] = (xxg[z]-xcz[z])**2 + (yyg[z]-c)**2
    if avec_vortex:
        theta = np.zeros((NZ, NXY, NXY))
        for z in range(NZ):
            theta[z] = np.arctan2(yyg[z]-c, xxg[z]-xcz[z])
        psi = np.sqrt(r2t/(r2t+U_CORE**2))*np.exp(1j*theta)
    else:
        psi = np.ones((NZ, NXY, NXY), dtype=np.complex128)
    if CHI_FRAC > 0:
        chi = np.sqrt(CHI_FRAC)*np.exp(-r2t/(2*SIG_CHI**2)).astype(np.complex128)
    else:
        chi = np.zeros_like(psi)
    lin = build_lin(0.4); lin_chi = build_lin(0.4, M_RATIO)
    nchi0 = (np.abs(chi)**2).sum()
    Vp = pins(A)
    Es = []
    for i in range(N_RELAX):
        cd2 = np.abs(chi)**2; pd2 = np.abs(psi)**2
        psi = step(psi, lin, DT, 0.4, GAA, GAB, cd2, MU_A, Vt+Vp)
        if CHI_FRAC > 0:
            chi = step(chi, lin_chi, DT, 0.4, GBB, GAB, pd2, MU_B, Vt, M_RATIO)
            chi *= np.sqrt(nchi0/((np.abs(chi)**2).sum()+1e-12))
        psi /= np.sqrt((np.abs(psi)**2).mean()+1e-12)
        if i >= N_RELAX-600 and i % 100 == 0:
            Es.append(energie_interne(psi, chi))
    return psi, chi, np.array(Es)

print(f"[3pts] m={M_RATIO} chi_frac={CHI_FRAC} AMPS={AMPS} W_PIN={W_PIN}", flush=True)
out = {"m_ratio": M_RATIO, "chi_frac": CHI_FRAC, "W_pin": W_PIN, "L": NZ, "points": []}
for A in AMPS:
    t0 = time.time()
    psi, chi, Es = relax_etat(A, True)
    E = energie_interne(psi, chi)
    psi0, chi0, _ = relax_etat(A, False)
    E0 = energie_interne(psi0, chi0)
    # verification : positions de la ligne aux 3 appuis + quart de ligne
    Xv, Yv = vortex_positions(psi)
    pos = {"z0": float(Xv[0]), "zmid": float(Xv[NZ//2]), "zend": float(Xv[-1]),
           "zq1": float(Xv[NZ//4]), "zq3": float(Xv[3*NZ//4])}
    drift = float(abs(Es[-1]-Es[0])/max(abs(Es[-1]),1e-12)) if len(Es) > 1 else float('nan')
    dL = 2*np.sqrt((NZ/2)**2+A**2) - NZ
    out["points"].append({"A": A, "E": E, "E_novtx": E0, "d": E-E0, "dL": dL,
                          "pos": pos, "drift_rel": drift})
    print(f"[3pts] m={M_RATIO} A={A:3.1f} : E={E:.2f} E0={E0:.2f} d={E-E0:.2f} "
          f"dL={dL:.3f} zmid={pos['zmid']:.2f} zq1={pos['zq1']:.2f} drift={drift:.1e} "
          f"t+{time.time()-t0:.0f}s", flush=True)

As = np.array([p["A"] for p in out["points"]])
Ds = np.array([p["d"] for p in out["points"]])
Ls = np.array([p["dL"] for p in out["points"]])
dE = Ds - Ds[0]
m = As > 0
T = float(np.sum(dE[m]*Ls[m])/np.sum(Ls[m]**2))     # dE = T * dL
out["T_eff_3pts"] = T
out["T_kelvin_ref"] = float(np.pi*np.log(NZ))
print(f"[3pts] m={M_RATIO} : T_eff={T:.2f} (Kelvin ref {np.pi*np.log(NZ):.2f})")
tag = f"p2bis2_m{int(M_RATIO):03d}"
json.dump(out, open(f"/mnt/agents/output/e44_data/{tag}.json", "w"), indent=2)
print(f"[3pts] sauve {tag}.json")
