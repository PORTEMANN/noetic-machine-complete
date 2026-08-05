#!/usr/bin/env python3
# P7 - isotopes : meme Z, A different -> meme Coulomb, coeur different.
# Le deplacement isotopique (shift) est la signature PURE du coeur (la charge
# ponctuelle est identique pour tous les isotopes). Chlore 35/37 (lien corpus
# Meta-Chlore 37.06 ANU <-> 37Cl). Charge finie = sphere uniforme, R_c=r0 A^(1/3).
# Verdict : shift isotopique deltaE_1s(37-35), et ce que la machine apporte.
import os, json
import numpy as np
from scipy.linalg import eigh_tridiagonal

ALPHA=1.0/137.036; A0=137.036; MU=207.0; R0FM=1.2; CONV=3.04/0.84
Z=17
ISOTOPES=[("Cl35",35),("Cl36",36),("Cl37",37),("Cl40",40)]

def Rc(A): return R0FM*A**(1.0/3.0)*CONV

def Vfin(r,Rc_):
    out=np.empty_like(r); m=r>=Rc_
    out[m]=-Z*ALPHA/r[m]; ri=r[~m]; out[~m]=-Z*ALPHA/Rc_*(1.5-0.5*(ri/Rc_)**2)
    return out

def e1s(Rc_,m):
    a0z=A0/(m*Z); RMAX=60*a0z; NR=40000
    r=np.linspace(RMAX/NR,RMAX,NR); dr=r[1]-r[0]
    diag=1.0/(m*dr**2)+Vfin(r,Rc_); off=-1.0/(2*m*dr**2)*np.ones(NR-1)
    ev,_=eigh_tridiagonal(diag,off,select='i',select_range=(0,0))
    return float(ev[0]), a0z, dr

def delta_th(Rc_,m):
    # theorie perturbations : deltaE_taille = (2/5) Z^4 a^4 m^3 Rc^2  (sphere uniforme)
    return (2.0/5.0)*Z**4*ALPHA**4*m**3*Rc_**2

res={"Z":Z,"R0FM":R0FM,"CONV":CONV,"isotopes":{}}
for m,lab in [(1.0,"electronique"),(MU,"muonique")]:
    E={}
    for name,A in ISOTOPES:
        e,a0z,dr=e1s(Rc(A),m); E[A]=e
        res["isotopes"].setdefault(name,{"A":A,"R_c":Rc(A)})[lab]={"E1s":e,"a0":a0z}
    # deplacement isotopique (le coeur seul bouge)
    for a1,a2 in [(35,37),(35,36),(36,37),(35,40)]:
        shift=E[a2]-E[a1]
        shift_th=delta_th(Rc(a2),m)-delta_th(Rc(a1),m)
        key=f"shift_{a2}-{a1}_{lab}"
        res[key]={"numerique":shift,"theorie_pert":shift_th,
                  "ratio":shift/shift_th if shift_th else None,
                  "relatif_a_E1s":shift/abs(E[a1])}
        print(f"[P7 {lab:12}] shift {a2}-{a1} : num={shift:+.4e}  th={shift_th:+.4e}  "
              f"ratio={shift/shift_th:.3f}  relatif={shift/abs(E[a1]):+.2e}",flush=True)
    # reference Coulomb ponctuel (Z=17) : identique pour tous les isotopes
    Ec=-Z*Z*ALPHA**2*m/2
    print(f"[P7 {lab:12}] E1s Coulomb ponctuel (Z=17) = {Ec:.6e}  (identique 35/36/37/40)",flush=True)

json.dump(res,open("/mnt/agents/output/e44_data/p7_isotopes.json","w"),indent=1)
print("[P7] sauve",flush=True)
