#!/usr/bin/env python3
# P9 - puzzle PREX-CREX (v4) : calcul de densite par couches, avec spin-orbite.
# Le spin-orbite est le mecanisme cle (Zhang-Chen) : il leve la degenerescence
# j=l+1/2 / j=l-1/2, et ce differentiel change la repartition de surface selon les
# couches occupees. 48Ca, 132Sn, 208Pb ont des couches de valence differentes ->
# peaux differentes. On calcule les rayons de matiere (n+p) et de charge (p) par
# remplissage des couches d'un puits Woods-Saxon + spin-orbite, pour n et p.
import os, json
import numpy as np
from scipy.linalg import eigh_tridiagonal

R0FM=1.2; CONV=3.04/0.84; A_DIFF=0.65*CONV
# unites banc : masse nucleon=1. Profondeur V0, spin-orbite Vso (constitutifs).
V0=0.20; VSO=0.06; ETA=0.5
TRIPLET=[("Ca48",20,28),("Sn132",50,82),("Pb208",82,126)]

def puits(r,Rc,W): return -W/(1.0+np.exp((r-Rc)/A_DIFF))

def spectre_j(Rc,W,l,j,NR=30000):
    """Energies des niveaux (n,l,j) avec spin-orbite Vso <l.s> dans le puits."""
    RMAX=Rc+10*A_DIFF
    r=np.linspace(RMAX/NR,RMAX,NR); dr=r[1]-r[0]
    ls = 0.5*(j*(j+1)-l*(l+1)-0.75)      # <l.s>
    Veff=puits(r,Rc,W)+l*(l+1)/(2*r**2)+VSO*ls/(r**2+ (0.5*Rc)**2)
    diag=1.0/(dr**2)+Veff; off=-1.0/(2*dr**2)*np.ones(NR-1)
    nmax=min(6,NR-1)
    try: ev,evec=eigh_tridiagonal(diag,off,select='i',select_range=(0,nmax-1))
    except: return []
    out=[]
    for k in range(len(ev)):
        if ev[k]<0:
            u=evec[:,k];p=u*u;p/=p.sum();rm=float(np.sqrt((r*r*p).sum()))
            out.append((float(ev[k]),rm))
    return out

def couches(NN,Rc,W):
    """Remplit les couches par energie croissante, retourne rayon quadratique moyen."""
    niveaux=[]
    for l in range(0,7):
        for j in ([l+0.5] if l==0 else [l-0.5,l+0.5]):
            if j<0.5: continue
            for E,rm in spectre_j(Rc,W,l,j):
                niveaux.append((E,l,j,rm))
    niveaux.sort()
    placed=0; r2=0.0
    for E,l,j,rm in niveaux:
        cap=int(2*j+1)
        take=min(cap,NN-placed)
        if take<=0: break
        r2+=take*rm*rm; placed+=take
    if placed<NN: # complete au rayon du coeur
        r2+=(NN-placed)*(Rc*np.sqrt(3/5))**2
    return float(np.sqrt(r2/NN))

res=[]
for name,Z,N in TRIPLET:
    A=Z+N; Nex=N-Z; Rc=R0FM*A**(1/3)*CONV
    Wn=V0*(1-ETA*Nex/A); Wp=V0
    r_n=couches(N,Rc,Wn); r_p=couches(Z,Rc,Wp)
    peau_fm=(r_n-r_p)/CONV
    res.append({"name":name,"Z":Z,"N":N,"Nex":Nex,"A":A,"peau_fm":peau_fm,
                "peau_rel":(r_n-r_p)/Rc,"r_n":r_n,"r_p":r_p})
    print(f"[P9v4] {name:6} N-Z={Nex:3} : peau={peau_fm:+.3f} fm  rel={(r_n-r_p)/Rc:+.4f}  "
          f"(r_n={r_n:.2f} r_p={r_p:.2f})",flush=True)

json.dump({"TRIPLET":res,"V0":V0,"VSO":VSO,"ETA":ETA},
          open("/mnt/agents/output/e44_data/p9_prex.json","w"),indent=1)
print("[P9v4] sauve",flush=True)
