# P27 - correlation a deux electrons : He et H2
# La frontiere multi-corps est-elle un mur ou un gradient ?
#   He : HF simple (analytique) -> split-zeta in-out (MC, orbitales 1-corps)
#   H2 : MO gerade double (RHF, MC) -> Heitler-London covalent (MC)
# Levier : operateur 1-corps uniquement ; la correlation radiale/covalente
# s'exprime avec des orbitales a un corps, l'angulaire (r12 explicite) non.
import numpy as np, json, hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RY = 27.2114
E_HE_EXACT = -2.903724   # Pekeris
I_HE_MES = 24.587        # eV
R_H2_EXACT = 1.401       # a0
D_H2_EXACT = 4.75        # eV

# ---------- outils H2+ (P20) ----------
def Sov(R, z):
    zR = z*R
    return np.exp(-zR)*(1+zR+zR*zR/3.0)
def E_gerade(R, z):
    s = Sov(R, z); zR = z*R
    j = (1.0-np.exp(-2*zR)*(1+zR))/R
    k = z*np.exp(-zR)*(1+zR)
    T = 0.5*z*z
    return (T - z - j + T*s - z*s - k)/(1+s)

# ---------- echantillons de base (nombres aleatoires communs) ----------
rng = np.random.default_rng(20270803)
N = 400000
g1 = rng.gamma(3.0, 1.0, N); g2 = rng.gamma(3.0, 1.0, N)
u1 = rng.normal(size=(N, 3)); u1 /= np.linalg.norm(u1, axis=1, keepdims=True)
u2 = rng.normal(size=(N, 3)); u2 /= np.linalg.norm(u2, axis=1, keepdims=True)
c1 = rng.choice([-1, 1], N); c2 = rng.choice([-1, 1], N)
NU = 300000

def J_gg(R, z):
    """repulsion e-e de deux electrons dans l'orbitale gerade (MC)."""
    p1 = u1[:NU]*(g1[:NU]/(2*z))[:, None]; p1[:, 2] += c1[:NU]*R/2
    p2 = u2[:NU]*(g2[:NU]/(2*z))[:, None]; p2[:, 2] += c2[:NU]*R/2
    r1a = np.sqrt(p1[:, 0]**2+p1[:, 1]**2+(p1[:, 2]-R/2)**2)
    r1b = np.sqrt(p1[:, 0]**2+p1[:, 1]**2+(p1[:, 2]+R/2)**2)
    r2a = np.sqrt(p2[:, 0]**2+p2[:, 1]**2+(p2[:, 2]-R/2)**2)
    r2b = np.sqrt(p2[:, 0]**2+p2[:, 1]**2+(p2[:, 2]+R/2)**2)
    xa = np.exp(-z*r1a); xb = np.exp(-z*r1b)
    ya = np.exp(-z*r2a); yb = np.exp(-z*r2b)
    s = Sov(R, z)
    w1 = (xa+xb)**2/((1+s)*(xa**2+xb**2))
    w2 = (ya+yb)**2/((1+s)*(ya**2+yb**2))
    r12 = np.sqrt(((p1-p2)**2).sum(1))
    return float(np.mean(w1*w2/np.maximum(r12, 1e-12)))

def E_H2_MO(R):
    best = None
    for z in np.arange(1.0, 1.5, 0.05):
        E = 2*E_gerade(R, z) + J_gg(R, z) + 1/R
        if best is None or E < best[1]:
            best = (float(z), float(E))
    return best

def E_H2_VB(R, z):
    """Heitler-London : psi = xa1 xb2 + xb1 xa2, energie locale MC."""
    M = NU
    r1 = np.empty(M); r2 = np.empty(M); sgn = np.empty(M)
    h = M//2
    r1[:h] = g1[:h]/(2*z); r2[:h] = g2[:h]/(2*z); sgn[:h] = 1     # q1 : e1@a, e2@b
    r1[h:] = g1[h:M]/(2*z); r2[h:] = g2[h:M]/(2*z); sgn[h:] = -1  # q2 : e1@b, e2@a
    p1 = u1[:M]*r1[:, None]; p1[:, 2] += R/2*sgn     # e1@a puis e1@b
    p2 = u2[:M]*r2[:, None]; p2[:, 2] -= R/2*sgn     # e2@b puis e2@a
    r1a = np.sqrt(p1[:, 0]**2+p1[:, 1]**2+(p1[:, 2]-R/2)**2)
    r1b = np.sqrt(p1[:, 0]**2+p1[:, 1]**2+(p1[:, 2]+R/2)**2)
    r2a = np.sqrt(p2[:, 0]**2+p2[:, 1]**2+(p2[:, 2]-R/2)**2)
    r2b = np.sqrt(p2[:, 0]**2+p2[:, 1]**2+(p2[:, 2]+R/2)**2)
    psi1 = np.exp(-z*(r1a+r2b)); psi2 = np.exp(-z*(r1b+r2a))
    psi = psi1+psi2
    w = psi**2/(psi1**2+psi2**2)
    r12 = np.sqrt(((p1-p2)**2).sum(1))
    Vn = 1/r1a+1/r1b+1/r2a+1/r2b
    EL = ((psi1*(-z*z+z*(1/r1a+1/r2b))+psi2*(-z*z+z*(1/r1b+1/r2a)))/psi
          - Vn + 1/np.maximum(r12, 1e-12) + 1/R)
    return float(np.sum(w*EL)/np.sum(w))

def E_H2_VB_min(R):
    best = None
    for z in np.arange(1.0, 1.5, 0.05):
        E = E_H2_VB(R, z)
        if best is None or E < best[1]:
            best = (float(z), float(E))
    return best

# ---------- He ----------
E_HF = -(27/16)**2                       # zeta = 27/16, solution analytique
I_HF = ((-2.0) - E_HF)*RY                # ionisation = E(He+) - E(He)
rng2 = np.random.default_rng(417)
M = 300000
G1 = rng2.gamma(3.0, 1.0, M); G2 = rng2.gamma(3.0, 1.0, M)
V1 = rng2.normal(size=(M, 3)); V1 /= np.linalg.norm(V1, axis=1, keepdims=True)
V2 = rng2.normal(size=(M, 3)); V2 /= np.linalg.norm(V2, axis=1, keepdims=True)

def E_He_split(a, b, Z=2):
    h = M//2
    r1 = np.empty(M); r2 = np.empty(M)
    r1[:h] = G1[:h]/(2*a); r2[:h] = G2[:h]/(2*b)
    r1[h:] = G1[h:]/(2*b); r2[h:] = G2[h:]/(2*a)
    D1 = np.exp(-a*r1-b*r2); D2 = np.exp(-b*r1-a*r2); psi = D1+D2
    w = psi**2/(D1**2+D2**2)
    p1 = V1*r1[:, None]; p2 = V2*r2[:, None]
    r12 = np.sqrt(((p1-p2)**2).sum(1))
    EL = ((D1*(a/r1+b/r2)+D2*(b/r1+a/r2))/psi - (a*a+b*b)/2
          - Z*(1/r1+1/r2) + 1/np.maximum(r12, 1e-12))
    return float(np.sum(w*EL)/np.sum(w))

best_he = None
for a in np.arange(1.0, 1.6, 0.1):
    for b in np.arange(1.8, 2.6, 0.1):
        E = E_He_split(a, b)
        if best_he is None or E < best_he[2]:
            best_he = (float(a), float(b), float(E))
# raffinement
a0, b0, _ = best_he
for a in np.arange(a0-0.08, a0+0.09, 0.04):
    for b in np.arange(b0-0.08, b0+0.09, 0.04):
        E = E_He_split(a, b)
        if E < best_he[2]:
            best_he = (float(a), float(b), float(E))
a_he, b_he, E_split = best_he
E_c = abs(E_HE_EXACT-E_HF)
recupere = (E_split-E_HF)/(E_HE_EXACT-E_HF)

# ---------- H2 ----------
Rs = np.arange(1.0, 3.4, 0.2)
mo = [E_H2_MO(R) for R in Rs]
vb = [E_H2_VB_min(R) for R in Rs]
imo = int(np.argmin([e for _, e in mo])); E_mo = mo[imo][1]; R_mo = Rs[imo]
ivb = int(np.argmin([e for _, e in vb])); E_vb = vb[ivb][1]; R_vb = Rs[ivb]
z_mo = [z for z, e in mo if e == E_mo][0]; z_vb = [z for z, e in vb if e == E_vb][0]
E_diss_mo = E_H2_MO(8.0)[1]
E_diss_vb = E_H2_VB_min(8.0)[1]
D_mo = (-1.0-E_mo)*RY
D_vb = (-1.0-E_vb)*RY
gap = D_H2_EXACT-D_mo
recup_vb = (D_vb-D_mo)/gap

res = dict(
 He=dict(E_HF=E_HF, E_exact=E_HE_EXACT, E_c_Ha=round(E_c, 4),
         E_c_eV=round(E_c*RY, 2), ecart_relatif_pct=round(abs(E_HF-E_HE_EXACT)/abs(E_HE_EXACT)*100, 2),
         ionisation_HF_eV=round(I_HF, 2), ionisation_mes_eV=I_HE_MES,
         ecart_ion_pct=round(abs(I_HF-I_HE_MES)/I_HE_MES*100, 1),
         split_zeta=dict(a=a_he, b=b_he, E=round(E_split, 4),
                         reference_Eckart=-2.8757,
                         E_c_recuperee_pct=round(100*recupere, 1))),
 H2=dict(MO=dict(R_eq=float(R_mo), zeta=z_mo, D_e_eV=round(D_mo, 2),
                 E_diss=round(E_diss_mo, 3),
                 contamination_ionique_eV=round((E_diss_mo-(-1.0))*RY, 2)),
         VB=dict(R_eq=float(R_vb), zeta=z_vb, D_e_eV=round(D_vb, 2),
                 E_diss=round(E_diss_vb, 3),
                 gap_recupere_pct=round(100*recup_vb, 1)),
         exact=dict(R_eq=R_H2_EXACT, D_e_eV=D_H2_EXACT)),
 lecture=("la frontiere multi-corps est un gradient : la correlation radiale (He in-out) "
          "et covalente (H2 VB) s'expriment en orbitales 1-corps et recuperent ~50-65% ; "
          "le mur residuel est la correlation angulaire (r12 explicite)"))

verdict = {
 "He_energie_2pct": bool(abs(E_HF-E_HE_EXACT)/abs(E_HE_EXACT) < 0.02),
 "He_ionisation_10pct": bool(abs(I_HF-I_HE_MES)/I_HE_MES < 0.10),
 "He_inout_recupere_45pct": bool(recupere >= 0.45),
 "H2_liaison_MO_R_eq_15pct": bool(abs(R_mo-R_H2_EXACT)/R_H2_EXACT < 0.15),
 "H2_VB_recupere_50pct_du_gap": bool(recup_vb >= 0.50),
}
res["verdict"] = verdict
res["score"] = f"{sum(verdict.values())}/5"
print(json.dumps(res, indent=2, ensure_ascii=False))

# figure
fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
labels = ["Hartree\n(1 zeta)", "in-out\n(split-zeta)", "exact"]
vals = [E_HF, E_split, E_HE_EXACT]
ax[0].bar(labels, vals, color=["#c33", "#36c", "#393"])
ax[0].set_ylim(-2.95, -2.80)
ax[0].set_ylabel("E (Hartree)")
ax[0].set_title(f"A - He : correlation radiale recuperee a {100*recupere:.0f}%")
for i, v in enumerate(vals):
    ax[0].text(i, v-0.004, f"{v:.4f}", ha="center", fontsize=8)
ax[1].plot(Rs, [e for _, e in mo], 'o-', label="MO (RHF) - D=%.2f eV" % D_mo)
ax[1].plot(Rs, [e for _, e in vb], 's-', label="VB (Heitler-London) - D=%.2f eV" % D_vb)
ax[1].axhline(-1.0, ls="--", c="gray", label="2 H (asymptote)")
ax[1].axhline(-1.0-D_H2_EXACT/RY, ls=":", c="k", label="exact (D=4.75 eV)")
ax[1].axvline(R_H2_EXACT, ls=":", c="k", alpha=0.4)
ax[1].set_xlabel("R (a0)"); ax[1].set_ylabel("E (Hartree)")
ax[1].set_title("B - H2 : MO vs covalent VB"); ax[1].legend(fontsize=8)
plt.tight_layout()
plt.savefig("/mnt/agents/output/e44_data/p27_correlation.png", dpi=110)

with open("/mnt/agents/output/e44_data/p27_correlation.json", "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
for p in ["p27_correlation.py", "p27_correlation.json", "p27_correlation.png"]:
    h = hashlib.sha256(open("/mnt/agents/output/e44_data/"+p, 'rb').read()).hexdigest()[:12]
    open(f"/mnt/agents/output/e44_data/sha_{p.split('.')[0]}_{p.split('.')[1]}.txt", "w").write(h)
    print(p, h)
