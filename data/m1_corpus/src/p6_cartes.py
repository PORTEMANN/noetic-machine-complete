#!/usr/bin/env python3
# P6 - cartes d'identite atomiques : ions hydrogenoides a coeur fini.
# Charge finie = sphere uniforme de rayon R_c (potentiel standard des corrections
# de taille finie, pas une troncature). R_c = r0 A^(1/3), ancrage r_p=0.84 fm
# <-> R_c(1)=3.04 mailles (P1). Verdict : spectre E_nl, ecart au Coulomb pur
# delta_nl (signature du coeur, reelle et independante de la grille), hierarchie.
# Double version : electronique (m_e) et muonique (m_mu=207 m_e).
import os, json
import numpy as np
from scipy.linalg import eigh_tridiagonal

ALPHA = 1.0/137.036
A0    = 137.036
MU    = 207.0
R0FM  = 1.2
CONV  = 3.04/0.84

SAMPLE = [("H",1,1),("He",2,4),("C",6,12),("O",8,16),("Al",13,27),
          ("Fe",26,56),("Cu",29,63),("Sn",50,120),("Pb",82,208)]

def Rc_mailles(Z, A):
    return (0.84 if Z==1 else R0FM*A**(1.0/3.0))*CONV

def V_charge_finie(r, Z, Rc):
    # sphere uniforme : V=-Z*a/r dehors ; V=-Z*a/Rc*(3/2 - r^2/(2 Rc^2)) dedans
    out = np.empty_like(r)
    m = r >= Rc
    out[m] = -Z*ALPHA/r[m]
    ri = r[~m]
    out[~m] = -Z*ALPHA/Rc*(1.5 - 0.5*(ri/Rc)**2)
    return out

def spectre(Z, Rc, m):
    a0z = A0/(m*Z)
    RMAX = 60.0*a0z
    NR = 40000
    r = np.linspace(RMAX/NR, RMAX, NR); dr = r[1]-r[0]
    Veff = V_charge_finie(r, Z, Rc)
    out = {}
    for l in range(3):
        diag = 1.0/(m*dr**2) + l*(l+1)/(2*m*r**2) + Veff
        off  = -1.0/(2*m*dr**2)*np.ones(NR-1)
        nval = 3 - l
        ev, evec = eigh_tridiagonal(diag, off, select='i', select_range=(0, nval-1))
        rows = []
        for k in range(len(ev)):
            n = k + 1 + l
            E = float(ev[k])
            E_coul = -Z*Z*ALPHA*ALPHA*m/(2*n*n)
            delta = (E - E_coul)/E_coul
            u = evec[:,k]; p = u*u; p /= p.sum()
            rows.append({"n":n,"l":l,"E":E,"E_coul":E_coul,"delta":float(delta),
                         "r_mean":float((r*p).sum())})
        out[l] = rows
    return out, a0z

def carte(el, Z, A, m, label):
    Rc = Rc_mailles(Z, A)
    sp, a0z = spectre(Z, Rc, m)
    return {"element":el,"Z":Z,"A":A,"lepton":label,"m":m,
            "R_c_mailles":Rc,"R_c_fm":Rc/CONV,"a0_sys":a0z,
            "hierarchie_Rc_over_a0":Rc/a0z,"delta_1s":sp[0][0]["delta"],
            "spectre":{str(k):v for k,v in sp.items()}}

cartes = []
for m,label in [(1.0,"electronique"),(MU,"muonique")]:
    for el,Z,A in SAMPLE:
        c = carte(el,Z,A,m,label); cartes.append(c)
        print(f"[P6 {label:12}] {el:3} Z={Z:3} : Rc={c['R_c_mailles']:6.2f}  "
              f"hier={c['hierarchie_Rc_over_a0']:9.4f}  delta_1s={c['delta_1s']:+.3e}",
              flush=True)

json.dump({"conv_mailles_par_fm":CONV,"r0_fm":R0FM,"rp_fm":0.84,
           "ALPHA":ALPHA,"MU":MU,"potentiel":"sphere_uniforme","cartes":cartes},
          open("/mnt/agents/output/e44_data/p6_cartes.json","w"), indent=1)
print("[P6] sauve", flush=True)
