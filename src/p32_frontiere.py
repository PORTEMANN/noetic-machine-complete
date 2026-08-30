""""P32 - Cartographie de la frontiere r12 (serie isoelectronique He, Z=2..6)
Protocole C12.1 fige (sha 81fb24f0c083977b). Integrateur delta : 1-corps analytique
exact, correlation Jastrow u=c r e^{-beta r} numerique en coordonnees perimetriques.
Levier discriminant : c=0 -> E = -(Z-5/16)^2 exactement (ecart 0.0).
Regles de portee derivees : R1 echelle (beta=zeta), R2 orthogonalite, R3 densite (0.42 zeta)."""
import numpy as np, json, hashlib
def vee_terms(Z,zeta,c,beta,npts=80):
    rmax=12.0/Z
    r1=np.linspace(2e-4,rmax,npts);r2=np.linspace(2e-4,rmax,npts);u=np.linspace(2e-4,2*rmax,npts)
    d1=r1[1]-r1[0];d2=r2[1]-r2[0];du=u[1]-u[0]
    R1,R2,U=np.meshgrid(r1,r2,u,indexing='ij')
    mask=(U>=np.abs(R1-R2))&(U<=R1+R2)
    with np.errstate(divide='ignore',invalid='ignore'):
        cos12=(R1**2+R2**2-U**2)/(2*R1*R2)
    ebu=np.exp(-beta*U);up=c*ebu*(1-beta*U);upp=c*ebu*(beta*beta*U-2*beta)
    phi=np.exp(-zeta*R1-zeta*R2+c*U*ebu)
    w=np.where(mask,8*np.pi**2*R1*R2*U*phi*phi,0.0)
    W=w.sum()*d1*d2*du
    return (w*(1.0/U)).sum()*d1*d2*du/W,(w*0.5*(2*up*up-2*upp-4*up/U)).sum()*d1*d2*du/W,(w*up*cos12*(2*zeta)).sum()*d1*d2*du/W
_c={}
def E_delta(Z,zeta,c,beta,npts=80):
    V,Tc,X=vee_terms(Z,zeta,c,beta,npts);k=(Z,round(zeta,4),npts)
    if k not in _c:_c[k]=vee_terms(Z,zeta,0.0,0.0,npts)[0]
    return zeta*zeta-2*Z*zeta+(5.0/8.0)*zeta+(V-_c[k])+Tc+X
def E_opt(Z,c,beta):
    zs=np.linspace(Z-0.55,Z-0.10,10);return min((E_delta(Z,z,c,beta),z) for z in zs)
if __name__=="__main__":
    EXACT={2:-2.903724377,3:-7.279913,4:-13.655566,5:-22.030972,6:-32.406247}
    for Z in [2,3,4,5,6]:
        z0=Z-5/16;Eref,_=E_opt(Z,0.0,0.0);E1,_=E_opt(Z,0.5,z0);E3,_=E_opt(Z,0.5,0.42*z0)
        print(f"Z={Z} ref={Eref:.4f} R1={E1:.4f} R3={E3:.4f} exact={EXACT[Z]:.4f} R3bat={E3<Eref}")
