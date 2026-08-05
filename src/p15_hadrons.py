#!/usr/bin/env python3
# P15 -- Le spectre mesure des hadrons
# Versant A : trajectoires de Regge du potentiel lineaire (corde relativiste).
#   Relation universelle : M^2 = 2 pi sigma (2 n + L) -> pente J(ou L) vs M^2 = 1/(2 pi sigma)
# Versant B : charmonium par potentiel de Cornell (-k/r + sigma r).
#   La constante V0 n'est pas derivable -> on teste les ECARTS (S-P, 2S-1S), qui l'annulent.
import json, hashlib
import numpy as np
from scipy.linalg import eigh_tridiagonal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"
SIGMA = 0.18        # GeV^2 tension de corde (ancrage P13)

# ---------------------------------------------------------------- versant A
RHO_RAD = [(0,0.775), (1,1.465), (2,1.700), (3,2.15)]            # S 1-- , J=1, excitations radiales n
RHO_ORB = [(1,0.775), (2,1.318), (3,1.691), (4,1.978)]           # leading, excitations de spin L=J

def fit_slope(pts):
    x = np.array([m*m for _, m in pts]); y = np.array([j for j, _ in pts])
    return np.polyfit(x, y, 1)[0], x, y

slope_rad, xr, yr = fit_slope(RHO_RAD)
slope_orb, xo, yo = fit_slope(RHO_ORB)
pente_univ = 1.0/(2*np.pi*SIGMA)      # 1/(2 pi sigma) = 0.884

res = {"sigma_GeV2": SIGMA,
       "versantA_regge": {
         "relation_universelle": "M^2 = 2 pi sigma (2n + L) ; pente = 1/(2 pi sigma)",
         "pente_theorique": round(pente_univ,3),
         "radiale": dict(points=RHO_RAD, pente_mes=round(slope_rad,3),
                         ecart_pct=round(100*(slope_rad-pente_univ)/pente_univ,1)),
         "orbitale": dict(points=RHO_ORB, pente_mes=round(slope_orb,3),
                          ecart_pct=round(100*(slope_orb-pente_univ)/pente_univ,1)),
         "lecture": "les deux trajectoires encadrent la pente universelle 1/(2 pi sigma) = 0.884"}}

# ---------------------------------------------------------------- versant B
SIGF = SIGMA
def spectre_charmonium(MC, KC):
    mu = MC/2.0; RMAX = 8.0; NR = 20000
    r = np.linspace(RMAX/NR, RMAX, NR); dr = r[1]-r[0]
    out = {}
    for l in (0,1):
        diag = 1.0/(mu*dr**2) + l*(l+1)/(2*mu*r**2) - KC/r + SIGF*r
        off = -1.0/(2*mu*dr**2)*np.ones(NR-1)
        ev = eigh_tridiagonal(diag, off, select='i', select_range=(0,2), eigvals_only=True)
        out[l] = [float(e) for e in ev]     # energies de liaison relatives (sans V0, sans 2mc)
    return out

MC, KC = 1.84, 0.52
spec = spectre_charmonium(MC, KC)
# ecarts mesures (annulent V0 et 2mc) :
#   S-P : 1P - 1S = 3526-3097 = 429 MeV ; 2S-1S = 3686-3097 = 589 MeV
ecarts = dict(
    SP_calc_MeV = round(1000*(spec[1][0]-spec[0][0]),1), SP_mes_MeV = 3526-3097,
    S21_calc_MeV = round(1000*(spec[0][1]-spec[0][0]),1), S21_mes_MeV = 3686-3097,
    P21_calc_MeV = round(1000*(spec[1][1]-spec[1][0]),1), P21_mes_MeV = 4040-3526)
res["versantB_charmonium"] = dict(mc_GeV=MC, k_GeVfm=KC, sigma=SIGF, ecarts=ecarts,
    lecture="V0 non derivable -> test sur les ecarts de niveaux (structure), pas les masses absolues")

# ---------------------------------------------------------------- verdict
eSP = abs(ecarts["SP_calc_MeV"]-ecarts["SP_mes_MeV"])/ecarts["SP_mes_MeV"]
e21 = abs(ecarts["S21_calc_MeV"]-ecarts["S21_mes_MeV"])/ecarts["S21_mes_MeV"]
verdict = dict(
    regge_radial_pente_univ = bool(abs(slope_rad-pente_univ)/pente_univ < 0.20),
    regge_orbital_pente_univ = bool(abs(slope_orb-pente_univ)/pente_univ < 0.20),
    regge_pente_universelle = bool(abs(slope_rad-slope_orb)/pente_univ < 0.20),
    charmonium_ecart_SP = bool(eSP < 0.30),
    charmonium_ecart_2S1S = bool(e21 < 0.30),
    charmonium_ordre = bool(spec[0][0]<spec[1][0]<spec[0][1]))
res["verdict"]=verdict

# ---------------------------------------------------------------- figure
fig,ax=plt.subplots(1,2,figsize=(13,5.4))
a=ax[0]
a.plot(xr,yr,"o",color="steelblue",ms=9,label="ρ radiale (n)")
a.plot(xo,yo,"s",color="indianred",ms=9,label="ρ/a orbitale (L=J)")
xg=np.linspace(0,5,10)
a.plot(xg,np.polyval(np.polyfit(xr,yr,1),xg),"--",color="steelblue",lw=1.2)
a.plot(xg,np.polyval(np.polyfit(xo,yo,1),xg),"--",color="indianred",lw=1.2)
a.plot(xg,pente_univ*xg+0.5,":",color="k",lw=1.4,label=f"1/(2πσ) = {pente_univ:.2f}")
for (n,m),tag in zip(RHO_RAD,["ρ","ρ(1450)","ρ(1700)","ρ(2150)"]):
    a.annotate(tag,(m*m,n),textcoords="offset points",xytext=(5,-11),fontsize=7.5)
for (L,m),tag in zip(RHO_ORB,["ρ","a2","ρ3","a4"]):
    a.annotate(tag,(m*m,L),textcoords="offset points",xytext=(5,4),fontsize=7.5)
a.set_xlabel(r"$M^2$ (GeV$^2$)"); a.set_ylabel("n  ou  J")
a.set_title(f"A -- Regge : pente universelle 1/(2πσ)\nradiale {slope_rad:.2f} | orbitale {slope_orb:.2f} | théorie {pente_univ:.2f} GeV$^{{-2}}$",fontsize=9.5)
a.legend(fontsize=8.5); a.grid(alpha=0.3)

a=ax[1]
noms=["1S","1P","2S","2P"]; calc=[spec[0][0],spec[1][0],spec[0][1],spec[1][1]]
# aligner le fond sur 1S pour comparer la structure (ecarts)
base_c=calc[0]; calc_n=[1000*(c-base_c) for c in calc]
mes=[0, 429, 589, 943]   # ecarts mesures en MeV depuis 1S (1S,1P=3526-3097,2S=3686-3097,2P=4040-3097)
x=np.arange(4)
a.plot(x,mes,"o",color="seagreen",ms=11,label="écarts mesurés",zorder=3)
a.plot(x,calc_n,"s",color="darkorange",ms=9,label="écarts calculés (Cornell)",zorder=3)
for xi,(m1,m2) in enumerate(zip(mes,calc_n)):
    a.plot([xi,xi],[m1,m2],"k-",lw=0.8,alpha=0.4)
a.set_xticks(x); a.set_xticklabels(noms,fontsize=9)
a.set_ylabel("écart depuis 1S (MeV)")
a.set_title(f"B -- Charmonium (structure des écarts)\nS−P {ecarts['SP_calc_MeV']:.0f} vs {ecarts['SP_mes_MeV']} | 2S−1S {ecarts['S21_calc_MeV']:.0f} vs {ecarts['S21_mes_MeV']} MeV",fontsize=9.5)
a.legend(fontsize=9); a.grid(alpha=0.3)

fig.suptitle("P15 -- Le spectre mesuré des hadrons : Regge (linéaire) + charmonium (Cornell)",fontsize=12)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(f"{OUT}/p15_hadrons.png",dpi=150)

with open(f"{OUT}/p15_hadrons.json","w") as f: json.dump(res,f,indent=1,ensure_ascii=False)
print(json.dumps(verdict,indent=1))
print(f"Regge: radiale {slope_rad:.3f} | orbitale {slope_orb:.3f} | univ {pente_univ:.3f}")
print(f"charmonium SP {ecarts['SP_calc_MeV']:.0f} vs {ecarts['SP_mes_MeV']} ({100*eSP:.0f}%) | 2S-1S {ecarts['S21_calc_MeV']:.0f} vs {ecarts['S21_mes_MeV']} ({100*e21:.0f}%)")
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p15.txt","w") as f:
    for p in ["p15_hadrons.py","p15_hadrons.json","p15_hadrons.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p15.txt").read())
