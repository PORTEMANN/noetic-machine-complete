#!/usr/bin/env python3
# P8 - effet EMC : le nucleon lie est-il un coeur deforme ?
# Le nucleon = coeur de charge finie (Rc=r0 A_n^(1/3)). Ses "partons" effectifs sont
# des etats lies DANS le coeur (puits de la sphere de charge). La fonction de
# structure analogue = distribution de ces etats (proportionnelle aux energies de
# liaison / profondeur effective du puits). La modification EMC = changement de ce
# spectre quand le coeur est lie a un environnement.
#
# Deux regimes (test discriminant) :
#   (a) MEAN-FIELD : le coeur est plonge dans un champ moyen de densite rho
#       (puits uniforme supplementaire, profondeur V_mf ~ rho). Modification de
#       TOUS les nucleons, ~ densite, isotrope, sature aux lourds.
#   (b) SRC : le coeur est lie a UN voisin a courte distance d (paire). Puits de
#       deux spheres superposees. Modification seulement des nucleons en paire,
#       ~ 1/d, isospin-dependant (np dominant), actif des A=3.
# Verdict : quelle forme reproduit la pente EMC mesuree et sa dependance (A, isospin) ?
import os, json
import numpy as np
from scipy.linalg import eigh_tridiagonal

ALPHA=1.0/137.036; A0=137.036; CONV=3.04/0.84
# Le nucleon = coeur de charge Z_n=1, rayon Rc_n = r_p (proton) -> 3.04 mailles.
# "partons effectifs" = etats lies du coeur : puits interne de la sphere de charge.
Z_N=1; RC_N=3.04

def Vsphere(r,Rc_,Zc):
    out=np.empty_like(r); m=r>=Rc_
    out[m]=-Zc*ALPHA/r[m]; ri=r[~m]; out[~m]=-Zc*ALPHA/Rc_*(1.5-0.5*(ri/Rc_)**2)
    return out

def spectre_partons(Veff,m=1.0,NR=20000,RMAX=None):
    """Spectre des etats lies (partons effectifs) dans le puits Veff."""
    if RMAX is None: RMAX=60*A0
    r=np.linspace(RMAX/NR,RMAX,NR); dr=r[1]-r[0]
    diag=1.0/(m*dr**2)+Veff; off=-1.0/(2*m*dr**2)*np.ones(NR-1)
    ev,_=eigh_tridiagonal(diag,off,select='i',select_range=(0,5))
    return ev

# --- coeur LIBRE (reference) ---
r=np.linspace(60*A0/20000,60*A0,20000)
V_libre=Vsphere(r,RC_N,Z_N)
E_libre=spectre_partons(V_libre)
prof_libre=-E_libre[0]   # profondeur de liaison du fondamental (proxy "x" moyen)
print(f"[P8] coeur libre : E_parton fond = {E_libre[0]:.6e}  (prof={prof_libre:.6e})",flush=True)

# --- (a) MEAN-FIELD : champ moyen de densite rho -> puits uniforme V_mf ---
# V_mf proportionnel a la densite nucleaire ; on balaie rho en unites de rho0.
res_mf=[]
for rho in [0.0,0.25,0.5,0.75,1.0,1.25,1.5]:
    V_mf = -rho*0.05*Z_N*ALPHA/RC_N   # puits moyen ~ densite, echelle coeur
    V=Vsphere(r,RC_N,Z_N)+V_mf
    E=spectre_partons(V)
    modif=(E[0]-E_libre[0])/E_libre[0] if E_libre[0]!=0 else 0
    res_mf.append({"rho":rho,"E0":float(E[0]),"modif_rel":float(modif)})
    print(f"[P8 MF ] rho={rho:4.2f} : E0={E[0]:+.6e}  modif={modif:+.4f}",flush=True)

# --- (b) SRC : paire a courte distance d -> deux spheres superposees ---
# le nucleon est lie a UN voisin a distance d (unites du rayon du coeur).
res_src=[]
for d_over_Rc in [100,20,8,4,3,2.5,2.2,2.0]:
    d=d_over_Rc*RC_N
    # potentiel de l'autre sphere vu depuis le premier (axe z) : approximation
    # cylindrique moyennee -> on ajoute le puits du voisin centre a r=d.
    rr=np.abs(r-d)
    rr=np.maximum(rr, r[0])
    Vpair=Vsphere(rr,RC_N,Z_N)
    V=Vsphere(r,RC_N,Z_N)+Vpair
    E=spectre_partons(V)
    modif=(E[0]-E_libre[0])/E_libre[0] if E_libre[0]!=0 else 0
    res_src.append({"d_over_Rc":d_over_Rc,"E0":float(E[0]),"modif_rel":float(modif)})
    print(f"[P8 SRC] d/Rc={d_over_Rc:5.1f} : E0={E[0]:+.6e}  modif={modif:+.4f}",flush=True)

json.dump({"Z_N":Z_N,"RC_N":RC_N,"E_libre":E_libre.tolist(),
           "mean_field":res_mf,"src":res_src},
          open("/mnt/agents/output/e44_data/p8_emc.json","w"),indent=1)
print("[P8] sauve",flush=True)
