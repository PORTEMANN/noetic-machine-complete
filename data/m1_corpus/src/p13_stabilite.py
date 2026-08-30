#!/usr/bin/env python3
# P13 -- La stabilite comme forme du potentiel
# Versant 1 : radioactivite alpha (barriere finie, effet tunnel de Gamow)
# Versant 2 : confinement (barriere infinie, corde de flux, Regge)
import json, hashlib
import numpy as np
from scipy.special import airy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"
# constantes naturelles (unites MeV, fm, s) -- codees en dur pour la clarte
HC = 197.3269804              # hbar.c en MeV.fm
C_LIGHT = 2.99792458e23       # c en fm/s
E2 = 1.4399645                # e^2/(4 pi eps0) en MeV.fm
R0 = 1.2                        # fm, ancrage P6/P9/P11
M_AMU = 931.494                 # MeV/c^2
M_ALPHA = 3727.379              # MeV/c^2
ZALPHA = 2.0                    # charge de la particule alpha (e evite : e = charge scipy)

# ---------------------------------------------------------------- versant 1
# noyaux alpha-emetters : (nom, A_fils, Z_fils, E_alpha MeV, T1/2 mesuree en s)
ALPHA = [
    ("212Po",208,82,8.784, 2.99e-7),
    ("218Po",214,82,6.115, 0.186),
    ("216Po",212,82,6.906, 0.145),
    ("214Po",210,82,7.833, 1.64e-4),
    ("226Ra",222,86,4.784, 1.60e3*3.156e7),
    ("228Th",224,88,5.423, 1.912*3.156e7),
    ("230Th",226,88,4.687, 7.54e4*3.156e7),
    ("232Th",228,88,4.083, 1.40e10*3.156e7),
    ("235U",231,90,4.679, 7.04e8*3.156e7),
    ("238U",234,90,4.270, 4.468e9*3.156e7),
    ("241Pu",237,92,5.150, 14.3*3.156e7),
    ("244Cm",240,94,5.805, 18.1*3.156e7),
    ("252Cf",248,96,6.118, 2.645*3.156e7),
    ("148Gd",144,62,3.183, 70.9*3.156e7),
    ("151Eu",147,63,1.964, 4.62e18*3.156e7),
]

def gamow(A_d, Z_d, E):
    """Facteur de Gamow G et T1/2 : T = exp(-2G), T1/2 = ln2*Rc/(v*T)."""
    Rc = R0*A_d**(1/3.0)
    b = Z_d*ZALPHA*E2/E                     # point de retour exterieur
    if b <= Rc: return Rc, b, 0.0, 0.0, 0.0
    mu = (M_ALPHA*M_AMU*A_d)/(M_ALPHA+M_AMU*A_d)   # masse reduite
    # integrale fermee du WKB Coulomb : G = sqrt(2 mu V0 b) * [acos(sqrt x)-sqrt(x(1-x))] / hbar
    x = Rc/b
    arg = np.arccos(np.sqrt(x)) - np.sqrt(x*(1-x))
    V0 = Z_d*ZALPHA*E2                      # produit Z1 Z2 e^2 (MeV.fm)
    G = np.sqrt(2*mu*V0*b)/HC*arg
    v = np.sqrt(2.0*E/M_ALPHA)*C_LIGHT    # vitesse alpha dans le noyau (fm/s)
    f = v/(2*Rc)                          # frequence de frappe (s^-1), v en fm/s, Rc en fm
    # espace logarithmique : log10(T1/2) direct, sans jamais calculer exp(2G)
    log10_t12 = (np.log(np.log(2)) - np.log(f) + 2*G)/np.log(10)
    t12 = 10**log10_t12 if log10_t12 < 300 else np.inf
    return Rc, b, G, t12, log10_t12

rows=[]; xs=[]; ycalc=[]; ymes=[]
for nom,Ad,Zd,E,t in ALPHA:
    Rc,b,G,t12,l10 = gamow(Ad,Zd,E)
    x = Zd/np.sqrt(E)                  # variable Geiger-Nuttall
    lm=float(np.log10(t))
    rows.append(dict(nom=nom,A=Ad,Z=Zd,E=E,Rc=round(Rc,3),b=round(b,2),
                     G=round(G,4),t12_calc_s=float(f"{t12:.3e}"),
                     t12_mes_s=float(f"{t:.3e}"),
                     log10_calc=float(l10),log10_mes=lm,
                     ecart_log=float(l10-lm)))
    xs.append(x); ycalc.append(l10); ymes.append(lm)

xs=np.array(xs); ycalc=np.array(ycalc); ymes=np.array(ymes)
rms = float(np.sqrt(np.mean((ycalc-ymes)**2)))
med = float(np.median(ycalc-ymes))
# pente Geiger-Nuttall ajustee sur le calcul (pente physique, pas ajustee sur mesure)
pente_calc = float(np.polyfit(xs,ycalc,1)[0])
pente_mes  = float(np.polyfit(xs,ymes,1)[0])

res = {"constantes":{"hc_MeVfm":HC,"e2_MeVfm":E2,"r0_fm":R0,"m_alpha_MeV":M_ALPHA},
       "versant1_alpha":{"noyaux":rows,"rms_log10":rms,"decalage_median_log10":med,
                         "pente_calc":pente_calc,"pente_mes":pente_mes,
                         "ordres_de_grandeur_couvert":float(max(ymes)-min(ymes)),
                         "note":"le decalage absolu (prefacteur de preformation) est consigne; "
                                "le test porte sur pente et hierarchie"}}

# ---------------------------------------------------------------- versant 2
SIGMA = 0.18       # GeV^2, tension de corde mesuree
M_MESON = 0.775    # GeV, rho (etat lie le plus leger de la corde u-d)
res["versant2_confinement"]={}

# 1) cassure de corde
r_casse = 2*M_MESON/SIGMA           # fm (sigma en GeV/fm : 0.18 GeV^2 = 0.18/0.1973 GeV/fm)
sigma_GeVfm = SIGMA/0.197327        # GeV/fm
r_casse = 2*M_MESON/sigma_GeVfm
res["versant2_confinement"]["cassure"]=dict(
    sigma_GeV2=SIGMA, sigma_GeVfm=round(sigma_GeVfm,4),
    energie_cassure_GeV=round(2*M_MESON,3), distance_fm=round(r_casse,3),
    lecture="la corde casse quand sigma*r atteint la masse de deux mesons -> 2 mesons, pas de quark libre")

# 2) trajectoires de Regge : spectre du potentiel lineaire V = sigma r (s-wave, spin mis dans J)
# modele : M^2 = 2 pi sigma (n + J) + C -> pente 2 pi sigma
# spectre radial exact d'un quark ultra-relativistique confine: E_n = sigma * x_n, x_n = zeros de Ai
# trajectoire J: M^2 ~ 2 pi sigma (n + J) ; on calcule la pente du spectre lineaire
ai_zeros = [2.3381,4.0879,5.5206,6.7867]  # -zeros de Ai pour le puits lineaire
# pente Regge canonique
alpha_p = 1/(2*np.pi*SIGMA)   # GeV^-2
res["versant2_confinement"]["regge"]=dict(
    pente_calculee_GeV_2=round(alpha_p,4), pente_mesuree_GeV_2=0.9,
    zeros_Ai=ai_zeros,
    lecture="M^2 lineaire en J, pente 1/(2 pi sigma) ; "
            "avec sigma=0.18 GeV^2 -> 0.884 GeV^-2, vs 0.9 mesure")

# 3) spectre du puits lineaire (masses radiales, normalisation)
# E_n (GeV) pour V = sigma r, quark sans masse (relativistique) : E_n = (sigma^2/... )*x_n
# forme : E_n = x_n * (3 pi sigma^2 / (2 * 2 mu))^{1/3}? -- on prend la forme relativiste M_n^2 = 2 pi sigma n
res["versant2_confinement"]["spectre_lineaire"]=dict(
    M2_n=[round(2*np.pi*SIGMA*(n+1),3) for n in range(4)],
    lecture="M_n^2 = 2 pi sigma n (corde relativiste)")

# ------------------------------------------------------------------ verdict
verdict = dict(
    geiger_nuttall_pente = bool(abs(pente_calc-pente_mes)/abs(pente_mes) < 0.15),
    hierarchie_20_ordres = bool((max(ymes)-min(ymes)) > 15),
    cassure_corde_calculee = bool(1.0 < r_casse < 2.0),
    regge_pente = bool(abs(alpha_p-0.9)/0.9 < 0.15))
res["verdict"]=verdict

# ------------------------------------------------------------------ figure
fig,ax=plt.subplots(1,2,figsize=(12,5.4))

# A : Geiger-Nuttall
a=ax[0]
a.plot(xs,ymes,"o",color="steelblue",ms=7,label="mesuré",zorder=3)
a.plot(xs,ycalc,"s",color="indianred",ms=5,alpha=0.8,label="calculé (Gamow)",zorder=3)
for x,y,n in zip(xs,ymes,[r["nom"] for r in rows]):
    a.annotate(n,(x,y),textcoords="offset points",xytext=(0,6),fontsize=6.5,ha="center")
xo=np.linspace(xs.min(),xs.max(),10)
a.plot(xo,np.polyval(np.polyfit(xs,ymes,1),xo),"--",color="steelblue",lw=1)
a.plot(xo,np.polyval(np.polyfit(xs,ycalc,1),xo),"--",color="indianred",lw=1)
a.set_xlabel(r"$Z_d/\sqrt{E_\alpha}$  (variable de Geiger-Nuttall)")
a.set_ylabel(r"$\log_{10}\,T_{1/2}$ (s)")
a.set_title(f"A -- Geiger-Nuttall sur {res['versant1_alpha']['ordres_de_grandeur_couvert']:.0f} ordres\n"
            f"pente calcul {pente_calc:.2f} / mesure {pente_mes:.2f}  (rms {rms:.2f} log)",fontsize=10)
a.legend(fontsize=8)

# B : confinement -- V= sigma r, cassure + Regge
a=ax[1]
r=np.linspace(0,2.2,200); a.plot(r,sigma_GeVfm*r,color="k",lw=2,label=r"$V=\sigma r$")
a.axhline(2*M_MESON,color="gray",ls=":",lw=1)
a.axvline(r_casse,color="indianred",ls="--",lw=1.5)
a.annotate(f"cassure\n{r_casse:.2f} fm",(r_casse,2*M_MESON),textcoords="offset points",
           xytext=(8,-30),fontsize=9,color="indianred")
a.text(0.05,0.55,"un quark seul\ncoûte $\\sigma r\\to\\infty$\n(confiné)",fontsize=9)
a.text(1.55,0.8,"la corde casse\n$\\to$ 2 mésons",fontsize=9)
a.set_xlabel("r (fm)"); a.set_ylabel("V (GeV)")
a.set_title(f"B -- Confinement : barrière infinie\n"
            f"Regge : pente 1/(2πσ) = {alpha_p:.3f} GeV$^{{-2}}$ (mesure ≈ 0.9)",fontsize=10)
a.legend(fontsize=9,loc="upper left")

fig.suptitle("P13 -- La stabilité comme forme du potentiel : barrière finie (α) / infinie (quarks)",fontsize=12)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig(f"{OUT}/p13_stabilite.png",dpi=150)

with open(f"{OUT}/p13_stabilite.json","w") as f: json.dump(res,f,indent=1,ensure_ascii=False)

print(json.dumps(verdict,indent=1))
print(f"GN: {len(rows)} noyaux, {res['versant1_alpha']['ordres_de_grandeur_couvert']:.1f} ordres, "
      f"pente calc {pente_calc:.2f} vs mes {pente_mes:.2f}, rms {rms:.2f} log")
print(f"cassure: {r_casse:.2f} fm | Regge: {alpha_p:.3f} vs 0.9")
print("pires ecarts (log10):")
for r in sorted(rows,key=lambda z:-abs(z["ecart_log"]))[:4]:
    print(f"  {r['nom']:6s} E={r['E']:.3f}  calc {r['log10_calc']:7.2f}  mes {r['log10_mes']:7.2f}  ecart {r['ecart_log']:+.2f}")

def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p13.txt","w") as f:
    for p in ["p13_stabilite.py","p13_stabilite.json","p13_stabilite.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p13.txt").read())
