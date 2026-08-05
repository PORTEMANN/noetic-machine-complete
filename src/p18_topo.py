#!/usr/bin/env python3
# P18 -- Les etats topologiques de la matiere
# Levier : la topologie (P0), etendue aux bandes electroniques.
# Versant A : isolant quantique de Hall (reseau carre, flux alpha=p/q par plaquette).
#   Spectre de Hofstadter ; nombre de Chern -> conductance de Hall = C e^2/h (quantifiee).
# Versant B : isolant topologique SSH (chaine dimerisee) : etat de bord zero-mode
#   protégé par la topologie (phase non triviale) vs absence (phase triviale).
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"

# ------------------------------------------------------- versant A : Hofstadter
def hofstadter_spectrum(q, nkx=40):
    """Spectre de Hofstadter pour flux alpha=1/q (approximation rationnelle)."""
    Es=[]
    for kx in np.linspace(-np.pi,np.pi,nkx):
        # matrice q x q (Harper) pour le flux 1/q
        H=np.zeros((q,q))
        for m in range(q):
            H[m,m]=2*np.cos(2*np.pi*m/q + kx)
        for m in range(q-1):
            H[m,m+1]=H[m+1,m]=1.0
        H[0,q-1]=H[q-1,0]=1.0   # bord periodique en y
        Es.append(np.linalg.eigvalsh(H))
    return np.sort(np.concatenate(Es))

def chern_number(q, band):
    """Nombre de Chern de la bande `band` (0-indexe) pour flux 1/q, par integration de Berry."""
    nkx=nky=30
    kxs=np.linspace(-np.pi,np.pi,nkx,endpoint=False)
    kys=np.linspace(-np.pi,np.pi,nky,endpoint=False)
    dkx=kxs[1]-kxs[0]; dky=kys[1]-kys[0]
    def eigvec(kx,ky):
        H=np.zeros((q,q),dtype=complex)
        for m in range(q): H[m,m]=2*np.cos(2*np.pi*m/q + kx)
        for m in range(q-1): H[m,m+1]=H[m+1,m]=1.0
        # couture avec phase ky
        H[0,q-1]=np.exp(-1j*ky); H[q-1,0]=np.exp(1j*ky)
        w,v=np.linalg.eigh(H)
        return v[:,band]
    C=0.0
    for i in range(nkx):
        for j in range(nky):
            u1=eigvec(kxs[i],kys[j])
            u2=eigvec(kxs[(i+1)%nkx],kys[j])
            u3=eigvec(kxs[(i+1)%nkx],kys[(j+1)%nky])
            u4=eigvec(kxs[i],kys[(j+1)%nky])
            def link(a,b):
                z=np.vdot(a,b); return z/np.abs(z) if np.abs(z)>1e-12 else 1.0
            C+=np.angle(link(u1,u2)*link(u2,u3)*link(u3,u4)*link(u4,u1))
    return C/(2*np.pi)

# flux 1/3 : 3 bandes, Chern attendus (1,-2,1)
q=3
cherns=[chern_number(q,b) for b in range(q)]
spec_hof=hofstadter_spectrum(q)

# ------------------------------------------------------- versant B : SSH
def ssh_spectrum(N, t1, t2, bc="open"):
    """Chaine SSH : N cellules, hopping intra t1, inter t2."""
    M=2*N; H=np.zeros((M,M))
    for c in range(N):
        H[2*c,2*c+1]=H[2*c+1,2*c]=t1
        if c<N-1:
            H[2*c+1,2*c+2]=H[2*c+2,2*c+1]=t2
    return np.linalg.eigvalsh(H)

N=40
# phase triviale (t1>t2) vs non triviale (t2>t1)
E_triv=ssh_spectrum(N,1.0,0.5)      # t1>t2 : pas de zero-mode
E_topo=ssh_spectrum(N,0.5,1.0)      # t2>t1 : 2 zero-modes (bords)
zm_topo=np.sum(np.abs(E_topo)<1e-6)
zm_triv=np.sum(np.abs(E_triv)<1e-6)

res={
 "versantA_hall":dict(flux="1/3 par plaquette",nb_bandes=q,
    chern_calcules=[round(float(c),2) for c in cherns],
    chern_attendus=[1,-2,1], somme=round(float(sum(cherns)),2),
    lecture="conductance de Hall = C e^2/h : quantifiee par le nombre de Chern (topologie)"),
 "versantB_ssh":dict(N_cellules=N,
    zero_modes_trivial=int(zm_triv), zero_modes_topologique=int(zm_topo),
    lecture="phase non triviale (t2>t1) : 2 etats de bord zero-mode proteges ; triviale : aucun"),
}

verdict=dict(
    chern_entiers = bool(all(abs(c-round(c))<0.15 for c in cherns)),
    chern_sequence = bool([int(round(c)) for c in cherns]==[1,-2,1]),
    chern_somme_nulle = bool(abs(sum(cherns))<0.3),
    ssh_bord_topologique = bool(zm_topo==2),
    ssh_trivial_sans_bord = bool(zm_triv==0))
res["verdict"]=verdict

# ------------------------------------------------------- figure
fig,ax=plt.subplots(1,3,figsize=(15,4.6))
a=ax[0]
a.plot(np.sort(spec_hof),np.zeros_like(spec_hof),"|",color="steelblue",ms=8)
for E in np.unique(np.round(spec_hof,1)):
    a.axvline(E,color="steelblue",alpha=0.15,lw=0.5)
a.set_xlabel("E (t)"); a.set_yticks([])
a.set_title("A -- Spectre de Hofstadter (flux 1/3)\n3 bandes séparées par des gaps",fontsize=9.5)

a=ax[1]
a.bar(range(q),cherns,color=["seagreen","indianred","seagreen"])
for i,c in enumerate(cherns): a.text(i,c+0.1*(-1 if c<0 else 1),f"C={int(round(c))}",ha="center",fontsize=10,fontweight="bold")
a.axhline(0,color="k",lw=0.8)
a.set_xticks(range(q)); a.set_xticklabels(["bande 1","bande 2","bande 3"])
a.set_ylabel("nombre de Chern")
a.set_title("B -- Chern des bandes = (1, −2, 1)\nHall : σ = C e²/h quantifiée",fontsize=9.5)

a=ax[2]
a.plot(np.sort(E_triv),np.ones(2*N),"o",color="gray",ms=3,label="triviale (t1>t2)")
a.plot(np.sort(E_topo),np.zeros(2*N),"o",color="seagreen",ms=3,label="topologique (t2>t1)")
a.axvline(0,color="k",ls=":",lw=0.8)
a.annotate(f"{zm_topo} zéro-modes\n(bords)",(0,0),textcoords="offset points",xytext=(15,-10),fontsize=9,color="seagreen")
a.set_xlabel("E (t)"); a.set_yticks([0,1]); a.set_yticklabels(["topo","triviale"])
a.set_title("C -- SSH : états de bord protégés\n2 zéro-modes (topo) vs 0 (triviale)",fontsize=9.5)
a.legend(fontsize=8,loc="upper right")

fig.suptitle("P18 -- Les états topologiques de la matière : Chern (Hall) et bords (SSH)",fontsize=12)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(f"{OUT}/p18_topo.png",dpi=150)

with open(f"{OUT}/p18_topo.json","w") as f: json.dump(res,f,indent=1,ensure_ascii=False)
print(json.dumps(verdict,indent=1))
print("Chern:",[round(float(c),2) for c in cherns],"somme",round(float(sum(cherns)),2))
print("SSH zero-modes: topo",zm_topo,"trivial",zm_triv)
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p18.txt","w") as f:
    for p in ["p18_topo.py","p18_topo.json","p18_topo.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p18.txt").read())
