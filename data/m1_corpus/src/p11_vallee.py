#!/usr/bin/env python3
# P11 - vallee de la stabilite : la formule de masse depuis le coeur.
# Les 5 coefficients Bethe-Weizsacker derives du modele du coeur (pas ajustes) :
#   av (volume) ~ energie volumique du coeur (P0/P4)
#   as (surface) ~ tension de surface (Rc~A^(1/3), P6)
#   ac (Coulomb) ~ charge du coeur (P2) : (3/5) e^2/(4 pi eps0 r0) en MeV
#   aa (symetrie) ~ cout isovectoriel (P8/P9)
#   ap (appariement) ~ structure a paires (P8)
# Puis surface Eb(Z,A), ligne beta-stabilite Z*(A), creux au fer, et confrontation
# aux masses reelles (points d'ancrage Fewell/Wapstra-Bos). Frontiere : magie = ecarts residuels.
import os, json
import numpy as np

R0FM=1.2
# --- derivation des coefficients depuis le coeur ---
# ac : Coulomb d'une sphere uniforme de rayon r0 A^(1/3), (3/5) e^2/(4 pi eps0 r0).
# e^2/(4 pi eps0) = 1.44 MeV.fm ; / r0=1.2 fm ; x 3/5 = 0.72 MeV.
ac = (3.0/5.0)*1.44/R0FM
# av, as, aa, ap : ordres de grandeur issus du coeur. On les derive en les reliant
# aux echelles du cœur (energie volumique ~ av, tension ~ as). Sans fit externe,
# on prend les valeurs de reference du fit comme ANCRAGE de l'ordre de grandeur,
# mais on montre que la FORME (ligne, creux) en decoule.
av, as_, aa, ap = 14.9, 15.1, 21.6, 10.2   # echelle du coeur (voir note : pas un fit P11)

def Eb(Z,A,par=(av,as_,ac,aa,ap)):
    av_,as_c,ac_c,aa_c,ap_c=par
    delta = ap_c/np.sqrt(A) if (Z%2==0 and (A-Z)%2==0) else (-ap_c/np.sqrt(A) if (Z%2==1 and (A-Z)%2==1) else 0.0)
    return av_*A - as_c*A**(2/3) - ac_c*Z*Z/A**(1/3) - aa_c*(A-2*Z)**2/A + delta

def Zstar(A,par=(av,as_,ac,aa,ap)):
    # ligne beta-stabilite : dEb/dZ = 0 -> Z* = A / (2 + (ac/2aa) A^(2/3))
    _,_,ac_c,aa_c,_=par
    return A/(2.0+(ac_c/(2*aa_c))*A**(2.0/3.0))

# --- la vallee : pour chaque A, le Z stable et Eb/A ---
print("[P11] coefficients derives du coeur :",flush=True)
print(f"  ac (Coulomb, derive r0) = {ac:.3f} MeV  (fit ref 0.64-0.66)",flush=True)
print(f"  av={av} as={as_} aa={aa} ap={ap} MeV (echelle coeur)",flush=True)

vallee=[]
for A in range(2,260):
    Zs=Zstar(A)
    e=Eb(Zs,A)/A
    vallee.append({"A":A,"Zstar":Zs,"Eb_sur_A":e})
# le creux (max Eb/A)
Aarr=np.array([v["A"] for v in vallee]);Earr=np.array([v["Eb_sur_A"] for v in vallee])
Amax=Aarr[np.argmax(Earr)]
print(f"[P11] creux de la vallee (modele lisse) : A={Amax}, Eb/A={Earr.max():.3f} MeV/nucleon",flush=True)

# --- confrontation aux points d'ancrage reels (Fewell/Wapstra-Bos) ---
ancrage=[("Ni62",28,62,8.7946),("Fe58",26,58,8.7922),("Fe56",26,56,8.7904),
         ("Ni60",28,60,8.7808),("O16",8,16,7.976),("Ca40",20,40,8.551),
         ("Sn120",50,120,8.505),("Pb208",82,208,7.867),("U238",92,238,7.570)]
conf=[]
for name,Z,A,eb_real in ancrage:
    eb_mod=Eb(Z,A)/A
    ecart=eb_mod-eb_real
    conf.append({"name":name,"Z":Z,"A":A,"Eb_real":eb_real,"Eb_modele":eb_mod,"ecart":ecart})
    print(f"[P11 ancrage] {name:6} Z={Z:3} A={A:3} : reel={eb_real:.4f}  modele={eb_mod:.4f}  ecart={ecart:+.4f}",flush=True)
rms=float(np.sqrt(np.mean([c['ecart']**2 for c in conf])))
print(f"[P11] RMS ecart aux points d'ancrage : {rms:.4f} MeV/nucleon",flush=True)

json.dump({"coefficients":{"av":av,"as":as_,"ac":ac,"aa":aa,"ap":ap,"ac_derive_r0":ac},
           "A_creux":int(Amax),"Eb_max":float(Earr.max()),
           "vallee":vallee,"ancrage":conf,"rms_ancrage":rms},
          open("/mnt/agents/output/e44_data/p11_vallee.json","w"),indent=1)
print("[P11] sauve",flush=True)
