"""P2bis — rigidite statique du composite ligne+tube (hors programme).
Protocole : ligne ancree aux bouts (heritage D3) + rails gaussiens suivant la
courbe imposee u(z) = A sin(pi z/NZ). Relaxation amortie COMPLETE (equilibre
statique), mesure de l'energie INTERNE GP (cinetique spectrale + interactions,
sans le potentiel des rails). E(A)-E(0) = (1/2) T_eff L k^2 A^2 -> T_eff.
Question : beta_stat (energie) vs beta_dyn (dispersion D3, x20 Kelvin) —
le tube agit-il sur l'energie (tension) ou sur la cinematique (gyroscopique) ?
Controle : ligne vide m=1 doit redonner la tension de Kelvin.
Usage: python3 p2bis_rigidite.py <m_ratio> [chi_frac]  env: SIG_CHI, AMPS, N_RELAX
"""
import sys, os, json, time
import numpy as np
from scipy.ndimage import map_coordinates
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
N_RELAX = int(os.environ.get("N_RELAX", "3000"))
AMPS = [float(s) for s in os.environ.get("AMPS", "0,0.5,1.0,1.5,2.0").split(",")]
W_RAIL = float(os.environ.get("W_RAIL", "1.0"))      # force des rails (meme puits que l'ancrage D3)
S_RAIL = 2.0
N_CAP = 2

c = (NXY-1)/2.0
zzg, xxg, yyg = np.indices((NZ, NXY, NXY), dtype=float)
zz = np.arange(NZ)
Vt = soft_wall(NZ, NXY, 16.0, 10.0)
K_FLEX = np.pi/NZ           # mode fondamental sin(pi z/NZ), nul aux bords

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

def rails(A):
    """Gouttiere REPULSIVE le long de u(z)=A sin(pi z/NZ) : une gouttiere de
    basse densite attire le coeur du vortex (son energie ~ densite locale).
    Un puits attractif, lui, le repousserait (defaut corrige, B3-FAIL).
    + ancrage repulsif aux bouts."""
    xc = c + A*np.sin(np.pi*zz/NZ)
    r2 = np.zeros((NZ, NXY, NXY))
    for z in range(NZ):
        r2[z] = (xxg[z]-xc[z])**2 + (yyg[z]-c)**2
    V = W_RAIL*np.exp(-r2/(2*S_RAIL**2))
    for z in range(N_CAP):
        w = 1.0 - z/N_CAP
        V[z] += w*(W_RAIL*np.exp(-((xxg[z]-c)**2+(yyg[z]-c)**2)/(2*S_RAIL**2)))
        V[-1-z] += w*(W_RAIL*np.exp(-((xxg[-1-z]-c)**2+(yyg[-1-z]-c)**2)/(2*S_RAIL**2)))
    return V

def energie_interne(psi, chi):
    """Energie GP interne : cinetique spectrale + interactions - mu N.
    EXCLUT le potentiel externe (mur + rails)."""
    ph = np.fft.fftn(psi)
    kin_p = 0.5*np.sum(K2*np.abs(ph)**2)/psi.size
    ch = np.fft.fftn(chi)
    kin_c = 0.5/M_RATIO*np.sum(K2*np.abs(ch)**2)/chi.size
    p2 = np.abs(psi)**2; c2 = np.abs(chi)**2
    pot = np.sum(0.5*GAA*p2**2 + 0.5*GBB*c2**2 + GAB*p2*c2
                 - MU_A*p2 - MU_B*c2)
    return float(kin_p+kin_c+pot), float(kin_p), float(kin_c), float(pot)

def relax_etat(A, avec_vortex=True):
    r2c = (xxg-c)**2+(yyg-c)**2
    if avec_vortex:
        theta = np.arctan2(yyg-c, xxg-c)
        psi = np.sqrt(r2c/(r2c+U_CORE**2))*np.exp(1j*theta)
    else:
        psi = np.ones((NZ, NXY, NXY), dtype=np.complex128)   # controle sans vortex
    if CHI_FRAC > 0:
        chi = np.sqrt(CHI_FRAC)*np.exp(-r2c/(2*SIG_CHI**2)).astype(np.complex128)
    else:
        chi = np.zeros_like(psi)
    lin = build_lin(0.4); lin_chi = build_lin(0.4, M_RATIO)
    nchi0 = (np.abs(chi)**2).sum()
    Vr = rails(A)
    Es = []
    for i in range(N_RELAX):
        cd2 = np.abs(chi)**2; pd2 = np.abs(psi)**2
        psi = step(psi, lin, DT, 0.4, GAA, GAB, cd2, MU_A, Vt+Vr)
        if CHI_FRAC > 0:
            chi = step(chi, lin_chi, DT, 0.4, GBB, GAB, pd2, MU_B, Vt, M_RATIO)
            chi *= np.sqrt(nchi0/((np.abs(chi)**2).sum()+1e-12))
        psi /= np.sqrt((np.abs(psi)**2).mean()+1e-12)
        if i >= N_RELAX-600 and i % 100 == 0:
            Es.append(energie_interne(psi, chi)[0])
    return psi, chi, np.array(Es)

print(f"[P2bis] m={M_RATIO} sig_chi={SIG_CHI} chi_frac={CHI_FRAC} "
      f"AMPS={AMPS} N_RELAX={N_RELAX}", flush=True)

out = {"m_ratio": M_RATIO, "sig_chi": SIG_CHI, "chi_frac": CHI_FRAC,
       "k_flex": K_FLEX, "L": NZ, "W_rail": W_RAIL, "points": []}
for A in AMPS:
    t0 = time.time()
    psi, chi, Es = relax_etat(A, avec_vortex=True)
    E, kin_p, kin_c, pot = energie_interne(psi, chi)
    psi0, chi0, _ = relax_etat(A, avec_vortex=False)
    E0, *_ = energie_interne(psi0, chi0)
    # verification : la ligne suit-elle les rails ?
    Xv, Yv = vortex_positions(psi)
    xc = c + A*np.sin(np.pi*zz/NZ)
    ecart = float(np.nanmedian(np.abs(Xv - xc)))
    drift = float(abs(Es[-1]-Es[0])/max(abs(Es[-1]), 1e-12)) if len(Es) > 1 else float('nan')
    out["points"].append({"A": A, "E": E, "E_novtx": E0, "E_vtx_moins_novtx": E-E0,
                          "kin_psi": kin_p, "kin_chi": kin_c, "pot": pot,
                          "ecart_rails": ecart, "drift_rel": drift})
    print(f"[P2bis] m={M_RATIO} A={A:4.1f} : E={E:.2f} E0={E0:.2f} d={E-E0:.2f} "
          f"ecart_rails={ecart:.3f} drift={drift:.2e} t+{time.time()-t0:.0f}s", flush=True)

# extraction T_eff sur l'energie SOUSTRAITE du controle sans vortex :
# [E_vtx(A)-E_novtx(A)] - [E_vtx(0)-E_novtx(0)] = (1/2) T_eff L k^2 A^2
As = np.array([p["A"] for p in out["points"]])
Ds = np.array([p["E_vtx_moins_novtx"] for p in out["points"]])
dE = Ds - Ds[0]
mask = As > 0
C = float(np.sum(dE[mask]*As[mask]**2)/np.sum(As[mask]**4))   # dE = C A^2
T_eff = 2*C/(NZ*K_FLEX**2)
T_kelvin = np.pi*np.log(NZ/1.0)          # rho_s kappa^2/(4 pi) ln(L/xi), rho=1 kappa=2 pi
out["C"] = C
out["T_eff_stat"] = T_eff
out["T_kelvin_ref"] = T_kelvin
out["ratio_stat_kelvin"] = T_eff/T_kelvin
print(f"[P2bis] m={M_RATIO} : T_eff_stat={T_eff:.2f} (Kelvin ref {T_kelvin:.2f}, "
      f"ratio {T_eff/T_kelvin:.2f})")
tag = f"p2bis_m{int(M_RATIO):03d}_s{int(SIG_CHI*10):02d}"
json.dump(out, open(f"/mnt/agents/output/e44_data/{tag}.json", "w"), indent=2)
print(f"[P2bis] sauve {tag}.json")
