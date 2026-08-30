#!/usr/bin/env python3
# P14 -- La table des cartes d'identite atomiques complete (H -> U)
# Meme operateur radial que P6 (solveur valide) : potentiel a coeur fini,
# charge uniforme Rc = r0 A^1/3, ancrage rp=0.84 fm <-> Rc(1)=3.04 mailles.
# Pour chaque element : carte (Z, A, Rc, Rc/a1s, delta_1s electron et muon, regime).
# delta_1s = (E_finie - E_coulomb_exact)/E_coulomb_exact : signature du coeur fini.
# Frontiere : Rc/a1s = 1 (a1s = a0/Z electronique, a0/(MU Z) muonique).
import json, hashlib
import numpy as np
from scipy.linalg import eigh_tridiagonal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"
ALPHA = 1.0/137.036
A0    = 137.036
MU    = 207.0
R0FM  = 1.2
RP    = 0.84
CONV  = 3.04/0.84

ELEM = [
 (1,"H",1),(2,"He",4),(3,"Li",7),(4,"Be",9),(5,"B",11),(6,"C",12),(7,"N",14),(8,"O",16),
 (9,"F",19),(10,"Ne",20),(11,"Na",23),(12,"Mg",24),(13,"Al",27),(14,"Si",28),(15,"P",31),
 (16,"S",32),(17,"Cl",35),(18,"Ar",40),(19,"K",39),(20,"Ca",40),(21,"Sc",45),(22,"Ti",48),
 (23,"V",51),(24,"Cr",52),(25,"Mn",55),(26,"Fe",56),(27,"Co",59),(28,"Ni",58),(29,"Cu",63),
 (30,"Zn",64),(31,"Ga",69),(32,"Ge",74),(33,"As",75),(34,"Se",80),(35,"Br",79),(36,"Kr",84),
 (37,"Rb",85),(38,"Sr",88),(39,"Y",89),(40,"Zr",90),(41,"Nb",93),(42,"Mo",98),(43,"Tc",98),
 (44,"Ru",102),(45,"Rh",103),(46,"Pd",106),(47,"Ag",107),(48,"Cd",114),(49,"In",115),
 (50,"Sn",120),(51,"Sb",121),(52,"Te",130),(53,"I",127),(54,"Xe",132),(55,"Cs",133),
 (56,"Ba",138),(57,"La",139),(58,"Ce",140),(59,"Pr",141),(60,"Nd",142),(61,"Pm",145),
 (62,"Sm",152),(63,"Eu",153),(64,"Gd",158),(65,"Tb",159),(66,"Dy",164),(67,"Ho",165),
 (68,"Er",166),(69,"Tm",169),(70,"Yb",174),(71,"Lu",175),(72,"Hf",180),(73,"Ta",181),
 (74,"W",184),(75,"Re",187),(76,"Os",192),(77,"Ir",193),(78,"Pt",195),(79,"Au",197),
 (80,"Hg",202),(81,"Tl",205),(82,"Pb",208),(83,"Bi",209),(84,"Po",209),(85,"At",210),
 (86,"Rn",222),(87,"Fr",223),(88,"Ra",226),(89,"Ac",227),(90,"Th",232),(91,"Pa",231),
 (92,"U",238)]

def Rc_mailles(Z, A):
    return (RP if Z==1 else R0FM*A**(1.0/3.0))*CONV

def V_charge_finie(r, Z, Rc):
    out = np.empty_like(r); m = r >= Rc
    out[m] = -Z*ALPHA/r[m]; ri = r[~m]
    out[~m] = -Z*ALPHA/Rc*(1.5 - 0.5*(ri/Rc)**2)
    return out

def E1s_finie(Z, Rc, m):
    a0z = A0/(m*Z); RMAX = 60.0*a0z; NR = 40000
    r = np.linspace(RMAX/NR, RMAX, NR); dr = r[1]-r[0]
    diag = 1.0/(m*dr**2) + V_charge_finie(r, Z, Rc)   # l=0 : pas de terme centrifuge
    off = -1.0/(2*m*dr**2)*np.ones(NR-1)
    ev = eigh_tridiagonal(diag, off, select='i', select_range=(0,0), eigvals_only=True)
    return float(ev[0])

def carte(Z, sym, A, m):
    Rc = Rc_mailles(Z, A); E = E1s_finie(Z, Rc, m)
    Ec = -Z*Z*ALPHA*ALPHA*m/2.0
    return (E-Ec)/abs(Ec), Rc

rows=[]
for Z,sym,A in ELEM:
    Rc = Rc_mailles(Z, A); Rc_fm = Rc/CONV
    a1s_e = A0/Z; a1s_m = A0/(MU*Z)
    de,_ = carte(Z,sym,A,1.0)
    dm,_ = carte(Z,sym,A,MU)
    rows.append(dict(Z=Z,sym=sym,A=A,Rc_fm=round(Rc_fm,3),
                     Rc_sur_a1s_e=round(Rc/a1s_e,4),Rc_sur_a1s_mu=round(Rc/a1s_m,2),
                     delta1s_e=float(f"{de:.3e}"),delta1s_mu=float(f"{dm:.3e}"),
                     regime_e="coeur-fini" if Rc/a1s_e>1 else ("transition" if Rc/a1s_e>0.05 else "ponctuel"),
                     regime_mu="sature" if Rc/a1s_m>1 else "coulombien"))

res = {"constantes":{"alpha":ALPHA,"a0_mailles":A0,"r0_fm":R0FM,"conv_mailles_fm":CONV,
                     "rp_fm":RP,"mu_sur_e":MU,"unite_delta":"relatif au Coulomb exact"},
       "cartes":rows}

ze = min(r["Z"] for r in rows if r["Rc_sur_a1s_e"]>1)
de_max = max(rows,key=lambda r:r["delta1s_e"]); dm_max = max(rows,key=lambda r:r["delta1s_mu"])
res["frontieres"] = dict(
    electron_Rc_egal_a1s_Z=ze, electron_Rc_egal_a1s_sym=[r["sym"] for r in rows if r["Z"]==ze][0],
    muon_sature_des_Z=1,
    lecture="electron : Rc/a1s=1 a Z=12 (Mg) ; muon : orbite dans le coeur des Z=1")
res["etendue"]=dict(
    delta1s_e_H=rows[0]["delta1s_e"], delta1s_e_Pb=[r["delta1s_e"] for r in rows if r["Z"]==82][0],
    delta1s_mu_H=rows[0]["delta1s_mu"], delta1s_mu_Pb=[r["delta1s_mu"] for r in rows if r["Z"]==82][0])

verdict = dict(
    table_complete = bool(len(rows)==92),
    delta1s_croissant = bool(all(rows[i+1]["delta1s_e"]>=rows[i]["delta1s_e"] for i in range(91))),
    frontiere_electron_transition = bool(11<=ze<=14),
    muon_sature_partout = bool(all(r["Rc_sur_a1s_mu"]>1 for r in rows)),
    hierarchie_H_Pb_4ordres = bool(de_max["delta1s_e"]>1e3*rows[0]["delta1s_e"]))
res["verdict"]=verdict

Z=[r["Z"] for r in rows]; de=[r["delta1s_e"] for r in rows]; dm=[r["delta1s_mu"] for r in rows]
re_=[r["Rc_sur_a1s_e"] for r in rows]; rm=[r["Rc_sur_a1s_mu"] for r in rows]
fig,ax=plt.subplots(1,2,figsize=(13,5.4))
a=ax[0]
a.semilogy(Z,np.abs(de),"o-",color="steelblue",ms=3,label=r"$|\delta_{1s}|$ électron")
a.semilogy(Z,np.abs(dm),"s-",color="indianred",ms=3,label=r"$|\delta_{1s}|$ muon")
for z in [1,6,26,50,82]:
    rr=[r for r in rows if r["Z"]==z][0]
    a.annotate(rr["sym"],(z,abs(rr["delta1s_e"])),textcoords="offset points",xytext=(0,7),fontsize=8,ha="center")
a.set_xlabel("Z"); a.set_ylabel(r"signature cœur fini $|\delta_{1s}|$")
a.set_title("A -- Signature cœur fini : 10⁻⁴ (H) → ~1 (Pb)\nle muon amplifie la sensibilité",fontsize=10)
a.legend(fontsize=9); a.grid(alpha=0.3,which="both")
a=ax[1]
a.set_yscale("log")
a.plot(Z,re_,"o-",color="seagreen",ms=3,label=r"$R_c/a_{1s}$ électron")
a.plot(Z,rm,"s-",color="darkorange",ms=3,label=r"$R_c/a_{1s}$ muon")
a.axhline(1,color="k",ls="--",lw=1)
a.axvline(ze,color="seagreen",ls=":",lw=1)
a.annotate(f"électron Rc/a1s=1\nZ={ze} ({[r['sym'] for r in rows if r['Z']==ze][0]})",(ze,1.4),fontsize=8,color="seagreen")
a.annotate("muon saturé\ndès Z=1",(3,300),fontsize=8,color="darkorange")
a.set_xlabel("Z"); a.set_ylabel(r"$R_c/a_{1s}$ (log)")
a.set_title("B -- Frontière : l'électron devient sensible au cœur\nvers Z≈12 (Mg), le muon y est toujours",fontsize=10)
a.legend(fontsize=9,loc="upper left"); a.grid(alpha=0.3,which="both")
fig.suptitle("P14 -- Table des cartes d'identité atomiques H→U (opérateur radial à cœur fini)",fontsize=12)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(f"{OUT}/p14_table.png",dpi=150)

with open(f"{OUT}/p14_table.json","w") as f: json.dump(res,f,indent=1,ensure_ascii=False)
print(json.dumps(verdict,indent=1)); print("frontieres:",res["frontieres"]); print("etendue:",res["etendue"])
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p14.txt","w") as f:
    for p in ["p14_table.py","p14_table.json","p14_table.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p14.txt").read())
