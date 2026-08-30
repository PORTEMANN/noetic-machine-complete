""""P33 - Decroissance asymptotique imposee (double constrainte cusp + queue sqrt(2I))
Protocole C12.1 fige (sha edd48a73de744843). Jastrow double constrainte :
u(r)= c r e^{-beta r} - A r/(1+gamma r), A=zeta-kappa derive de I (donnee, non ajustee).
Levier : c=0 et A=0 -> 1s2 exact (ecart 0.0). Resultat : queue exacte degrade a tout Z."""
import numpy as np
KAPPA={2:1.3443,3:2.3578,4:3.3632,5:4.3662,6:5.3682}
def vee33(Z,zeta,c,beta,A,g,npts=80):
    rmax=14.0/Z
    r1=np.linspace(2e-4,rmax,npts);r2=np.linspace(2e-4,rmax,npts);u=np.linspace(2e-4,2*rmax,npts)
    d1=r1[1]-r1[0];d2=r2[1]-r2[0];du=u[1]-u[0]
    R1,R2,U=np.meshgrid(r1,r2,u,indexing='ij')
    mask=(U>=np.abs(R1-R2))&(U<=R1+R2)
    with np.errstate(divide='ignore',invalid='ignore'):
        cos12=(R1**2+R2**2-U**2)/(2*R1*R2)
    ebu=np.exp(-beta*U);uf=c*U*ebu-A*U/(1+g*U)
    up=c*ebu*(1-beta*U)-A/(1+g*U)**2;upp=c*ebu*(beta*beta*U-2*beta)+2*A*g/(1+g*U)**3
    phi=np.exp(-zeta*R1-zeta*R2+uf);w=np.where(mask,8*np.pi**2*R1*R2*U*phi*phi,0.0)
    W=w.sum()*d1*d2*du
    return (w*(1.0/U)).sum()*d1*d2*du/W,(w*0.5*(2*up*up-2*upp-4*up/U)).sum()*d1*d2*du/W,(w*up*cos12*(2*zeta)).sum()*d1*d2*du/W
_c={}
def E33(Z,zeta,c,beta,A,g,npts=80):
    V,Tc,X=vee33(Z,zeta,c,beta,A,g,npts);k=(Z,round(zeta,4),npts)
    if k not in _c:_c[k]=vee33(Z,zeta,0,0,0,1.0,npts)[0]
    return zeta*zeta-2*Z*zeta+(5.0/8.0)*zeta+(V-_c[k])+Tc+X
def E33_opt(Z,c,A,g):
    zs=np.linspace(Z-0.55,Z-0.10,10);return min((E33(Z,z,c,0.42*z,A,g),z) for z in zs)
if __name__=="__main__":
    for Z in [2,3,4,5,6]:
        z0=Z-5/16;Eref=E33(Z,z0,0,0.42*z0,0,1.0);Er3,_=E33_opt(Z,0.5,0,1.0)
        A=z0-KAPPA[Z];Eq,_=E33_opt(Z,0.5,A,1.0)
        print(f"Z={Z} ref={Eref:.4f} R3={Er3:.4f} R3+queue={Eq:.4f} queueAide={Eq<Er3}")
