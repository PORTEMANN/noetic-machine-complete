# P29 - completion 208Pb au kappa_opt=0.0 (calage central sur S moyenne)
import numpy as np, json, hashlib
from scipy.linalg import eigh_tridiagonal
from scipy.special import erfc
HC=197.3269804; MN=939.565; MP=938.272; E2=1.4399645; R0=1.2; RP=0.84
SIGF=RP/np.sqrt(3)
AV,AS,AA,AP,AC=15.8,18.3,23.2,12.0,0.71
def Eb(N,Z):
    A=N+Z
    if N<0 or Z<0: return 0.0
    pair=(1 if (N%2==0 and Z%2==0) else (-1 if (N%2==1 and Z%2==1) else 0))
    return AV*A-AS*A**(2/3)-AA*(N-Z)**2/A-AC*Z**2/A**(1/3)+pair*AP/np.sqrt(A)
def Sn(N,Z): return Eb(N,Z)-Eb(N-1,Z)
def Sp(N,Z): return Eb(N,Z)-Eb(N,Z-1)
def make_V(r,R,V0,Zc,sigma):
    V=-V0*0.5*erfc((r-R)/(sigma*np.sqrt(2)))
    if Zc and Zc>0: V+=np.where(r<R,Zc*E2/(2*R)*(3-(r/R)**2),Zc*E2/r)
    return V
def spectrum(R,V0,m,Zc,sigma,RMAX,dr,lmax=9,nmax=40,vectors=False):
    r=np.arange(dr,RMAX,dr); K2=HC**2/(2*m); V=make_V(r,R,V0,Zc,sigma)
    out=[]
    for l in range(lmax+1):
        diag=2*K2/dr**2+V+l*(l+1)*K2/r**2; off=-K2/dr**2*np.ones(len(r)-1)
        if vectors: ev,evec=eigh_tridiagonal(diag,off,select='i',select_range=(0,nmax-1))
        else: ev=eigh_tridiagonal(diag,off,select='i',select_range=(0,nmax-1),eigvals_only=True); evec=None
        for i,E in enumerate(ev[ev<0]): out.append((float(E),l,(evec[:,i]/np.sqrt(dr)) if vectors else None))
    out.sort(key=lambda t:t[0]); return out,r
def fermi_energy(states,Nocc):
    cum=0
    for E,l,_ in states:
        cum+=2*(2*l+1)
        if cum>=Nocc: return E
    return None
def density(R,V0,m,Zc,Nocc,sigma,RMAX,dr):
    st,r=spectrum(R,V0,m,Zc,sigma,RMAX,dr,vectors=True)
    cum=0; rho=np.zeros(len(r)); r2w=0.0
    for E,l,u in st:
        w=min(2*(2*l+1),Nocc-cum)
        if w<=0: break
        cum+=w; u2=u**2
        rho+=w*u2/(4*np.pi*r**2); r2w+=w*float(np.sum(u2*r**2*dr))
    return r,rho,np.sqrt(r2w/Nocc)
def tune_V0(R,m,Zc,Nocc,S,sigma,RMAX,dr):
    best=None
    for V0 in np.arange(40,88,0.5):
        st,_=spectrum(R,V0,m,Zc,sigma,RMAX,dr); EF=fermi_energy(st,Nocc)
        if EF is None: continue
        obj=abs(EF+S)
        if best is None or obj<best[0]: best=(obj,V0,EF)
    return best
Z,N=82,126; A=N+Z; R=R0*A**(1/3); RMAX=R+9; dr=0.008
Sm=(Sn(N,Z)*N+Sp(N,Z)*Z)/A
bc=tune_V0(R,MN,0,N,Sm,SIGF,RMAX,dr); V0c=bc[1]
stn,_=spectrum(R,V0c,MN,0,SIGF,RMAX,dr); stp,_=spectrum(R,V0c,MP,Z,SIGF,RMAX,dr)
EFn=fermi_energy(stn,N); EFp=fermi_energy(stp,Z)
r,rhon,rmsn=density(R,V0c,MN,0,N,SIGF,RMAX,dr)
_,rhop,rmsp=density(R,V0c,MP,Z,Z,SIGF,RMAX,dr)
d=dict(nom="208Pb",Z=Z,N=N,peau_iso=round(rmsn-rmsp,3),peau_mes=0.283,
       EFn=round(EFn,2),EFp=round(EFp,2),Sn=round(Sn(N,Z),1),Sp=round(Sp(N,Z),1),
       asy=round((N-Z)/A,3),V0c=round(V0c,1))
print(json.dumps(d,ensure_ascii=False))
json.dump(d,open("/mnt/agents/output/e44_data/p29_pb.json","w"))
print("sha:",hashlib.sha256(open("/mnt/agents/output/e44_data/p29_pb.py",'rb').read()).hexdigest()[:12])
