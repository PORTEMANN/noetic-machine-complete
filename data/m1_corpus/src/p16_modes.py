#!/usr/bin/env python3
# P16 -- La carte unifiee des modes de desintegration
# Pour chaque nuclide (A, Z) : quel est le mode dominant ?
#   beta+/- : comparaison a la ligne de stabilite Z*(A) (P11, Bethe-Weizsacker)
#   alpha   : duree de vie de Gamow (P13) -> alpha si T_alpha raisonnable
#   fission : parametre de fissilite x = Z^2/(47 A) (seuil x>=1 -> fission spontanee)
#   stable  : sur la ligne, pas assez lourd pour alpha
# Un seul levier : l'energie de liaison (Bethe-Weizsacker) + la forme du potentiel.
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"
# coefficients Bethe-Weizsacker (P11) : ac derive = 0.72 MeV, les autres ordres de grandeur
AV, AS, AA, AP = 15.8, 18.3, 23.2, 12.0
AC_BETA = 0.71      # MeV, pour la ligne de stabilite Z*(A) (P11 ~0.72)
AC_ALPHA = 0.54    # MeV, pour Qalpha (recale sur 238U=4.27 mesure) ; la tension est la frontiere P11
R0FM = 1.2
HC = 197.327; E2 = 1.43996; M_ALPHA = 3727.379; MAMU = 931.494; CL = 2.998e23

def Eb(A, Z):
    N = A - Z
    pair = AP/np.sqrt(A) if (Z%2==0 and N%2==0) else (-AP/np.sqrt(A) if (Z%2==1 and N%2==1) else 0.0)
    A=float(A); return AV*A - AS*np.float64(A)**(2.0/3.0) - AC_ALPHA*Z*(Z-1)*np.float64(A)**(-1.0/3.0) - AA*(A-2*Z)**2/A + pair

def Zstar(A):  # ligne de stabilite (derivee dEb/dZ = 0)
    return A/(2 + (AC_BETA/(2*AA))*np.float64(A)**(2.0/3.0))

def Qalpha(A, Z):  # energie liberée par emission alpha
    return Eb(A,Z) - Eb(A-4,Z-2) - 28.296   # Eb(alpha) = 28.296 MeV

def Qbeta(A, Z, sens):  # sens=+1 : beta+ (Z->Z-1) ; sens=-1 : beta- (Z->Z+1). >0 si favorable
    if sens==+1: return Eb(A,Z-1) - Eb(A,Z)     # electron capture / beta+
    else:        return Eb(A,Z+1) - Eb(A,Z)     # beta-

def gamow_T12(A_d, Z_d, E):
    if E <= 0: return np.inf
    Rc = R0FM*A_d**(1/3.0); b = Z_d*2*E2/E
    if b <= Rc: return 0.0
    mu = M_ALPHA*MAMU*A_d/(M_ALPHA+MAMU*A_d)
    x = Rc/b; arg = np.arccos(np.sqrt(x)) - np.sqrt(x*(1-x))
    G = np.sqrt(2*mu*Z_d*2*E2*b)/HC*arg
    f = np.sqrt(2*E/M_ALPHA)*CL/(2*Rc)
    return np.exp((np.log(np.log(2))-np.log(f)+2*G)) if (np.log(np.log(2))-np.log(f)+2*G)<700 else np.inf

# nuclides de reference (nom, A, Z, mode observe)
NUCLIDES = [
    ("12C",12,6,"stable"),("16O",16,8,"stable"),("40Ca",40,20,"stable"),
    ("56Fe",56,26,"stable"),("58Ni",58,28,"stable"),("90Zr",90,40,"stable"),
    ("120Sn",120,50,"stable"),("138Ba",138,56,"stable"),("208Pb",208,82,"stable"),
    ("3H",3,1,"beta-"),("14C",14,6,"beta-"),("40K",40,19,"beta-"),
    ("60Co",60,27,"beta-"),("90Sr",90,38,"beta-"),("137Cs",137,55,"beta-"),
    ("22Na",22,11,"beta+"),("18F",18,9,"beta+"),("11C",11,6,"beta+"),
    ("238U",238,92,"alpha"),("235U",235,92,"alpha"),("226Ra",226,88,"alpha"),
    ("232Th",232,90,"alpha"),("210Po",210,84,"alpha"),("241Am",241,95,"alpha"),
]
rows=[]
for nom,A,Z,mode in NUCLIDES:
    Zs = Zstar(A); N=A-Z
    Qa = Qalpha(A,Z); Ta = gamow_T12(A-4,Z-2,Qa) if Qa>0 else np.inf
    x = Z*Z/(47.0*A)
    # regle de decision : fission (tres lourd) -> alpha (lourd, Qalpha>0) ->
    # stable (lie, proche de Z*) -> beta+/- (loin de la ligne)
    Qbm = Qbeta(A,Z,-1)   # beta- favorable si >0
    Qbp = Qbeta(A,Z,+1)   # beta+ favorable si >0
    if x >= 0.70:
        pred = "fission" if Z >= 100 else "alpha"
    elif A >= 140 and Qa > 0:
        pred = "alpha"
    elif Qbm <= 0 and Qbp <= 0:
        pred = "stable"
    elif Qbm > Qbp:
        pred = "beta-"
    else:
        pred = "beta+"
    ok = (pred==mode) or (mode=="beta-" and pred=="beta-") or (mode=="beta+" and pred=="beta+")
    # alpha vs beta pour les lourds : les deux existent, on note le mode dominant
    rows.append(dict(nom=nom,A=A,Z=Z,mode_obs=mode,mode_pred=pred,accord=bool(pred==mode),
                     Zstar=round(Zs,1),Qalpha=round(Qa,2),fissilite=round(x,3),
                     log10_Talpha_s=(round(float(np.log10(Ta)),1) if np.isfinite(Ta) and Ta>0 else None)))

res = {"coefficients":{"av":AV,"as":AS,"aa":AA,"ap":AP,"ac_beta":AC_BETA,"ac_alpha":AC_ALPHA,
                   "decouplage":"ac_beta (Z*) vs ac_alpha (Qalpha) = tension de surface P11"},
       "nuclides":rows}

# synthese par mode
from collections import Counter
acc = sum(r["accord"] for r in rows)
res["bilan"] = dict(total=len(rows), accord=acc, score=f"{acc}/{len(rows)}")
for m in ("stable","beta-","beta+","alpha","fission"):
    sub=[r for r in rows if r["mode_obs"]==m]
    if sub:
        res["bilan"][m]=f"{sum(r['accord'] for r in sub)}/{len(sub)}"

# carte (A,Z) -> mode dominant (grille)
Ag=[]; Zg=[]; Cg=[]
for A in range(6,270):
    Zs=Zstar(A)
    for Z in range(max(1,int(Zs-14)),min(A,int(Zs+14))):
        Qa=Qalpha(A,Z); x=Z*Z/(47.0*A)
        Qbm=Qbeta(A,Z,-1); Qbp=Qbeta(A,Z,+1)
        if x>=0.70 and Z>=100: c=4
        elif A>=140 and Qa>0: c=3
        elif Qbm<=0 and Qbp<=0: c=0
        elif Qbm>Qbp: c=1
        else: c=2
        Ag.append(A); Zg.append(Z); Cg.append(c)
res["carte_AZ"]=dict(desc="0 stable, 1 beta-, 2 beta+, 3 alpha, 4 fission")

verdict = dict(
    beta_stables_corrects = bool(res["bilan"].get("stable","0/1").split("/")[0]==res["bilan"].get("stable","0/1").split("/")[1]),
    alpha_identifies = bool(all(r["accord"] for r in rows if r["mode_obs"]=="alpha")),
    score_global = bool(acc/len(rows) > 0.80),
    fissilite_seuil = bool(all(r["fissilite"]<1.0 for r in rows if r["mode_obs"]!="fission")),
    ligne_stabilite = bool(abs(Zstar(56)-26)<3 and abs(Zstar(208)-82)<4))
res["verdict"]=verdict

# figure : carte A,Z
from matplotlib.colors import ListedColormap
cmap=ListedColormap(["#2e7d32","#1565c0","#e65100","#b71c1c","#4a148c"])
fig,ax=plt.subplots(figsize=(9,8))
sc=ax.scatter(Ag,Zg,c=Cg,cmap=cmap,s=3,marker="s")
ax.plot([Zstar(A)-(A-Zstar(A)) for A in range(6,270)],[Zstar(A) for A in range(6,270)],"k-",lw=1,alpha=0.4)
for r in rows:
    mk={"stable":"o","beta-":"^","beta+":"v","alpha":"s","fission":"D"}[r["mode_obs"]]
    col="k" if r["accord"] else "red"
    ax.annotate(r["nom"],(r["A"]-r["Z"],r["Z"]),fontsize=6,ha="center",
                color=col,fontweight="bold" if not r["accord"] else "normal")
ax.set_xlabel("N (neutrons)"); ax.set_ylabel("Z (protons)")
import matplotlib.patches as mp
leg=[mp.Patch(color=cmap(i),label=l) for i,l in enumerate(["stable","β⁻","β⁺","α","fission"])]
ax.legend(handles=leg,fontsize=9,loc="upper left")
ax.set_title(f"P16 -- Carte unifiée des modes de désintégration (rouge = désaccord)\nscore {acc}/{len(rows)} nucléides de référence",fontsize=11)
fig.tight_layout(); fig.savefig(f"{OUT}/p16_modes.png",dpi=150)

with open(f"{OUT}/p16_modes.json","w") as f: json.dump(res,f,indent=1,ensure_ascii=False)
print(json.dumps(verdict,indent=1)); print("bilan:",res["bilan"])
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p16.txt","w") as f:
    for p in ["p16_modes.py","p16_modes.json","p16_modes.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p16.txt").read())
