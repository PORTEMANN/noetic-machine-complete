#!/usr/bin/env python3
# P25 — Isolants topologiques : Haldane (Chern + frontiere 3sqrt3), Kane-Mele (Z2),
# correspondance bord-volume (ruban helicoidal), 3D Wilson-Dirac (parite TRIM -> nu0)
import numpy as np, json, hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = {"chantier": "P25", "titre": "Isolants topologiques 2D/3D — Chern, Z2, indice fort derives"}
SQRT3 = np.sqrt(3.0)

# ============ geometrie nid d'abeille (distance PP = 1) ============
d1 = np.array([0.0, 1.0]); d2 = np.array([SQRT3/2, -0.5]); d3 = np.array([-SQRT3/2, -0.5])
b1 = d2 - d3; b2 = d3 - d1; b3 = d1 - d2          # vecteurs NNN = Bravais (b1+b2+b3=0)
a1, a2 = b1, b3                                   # base de Bravais
det = a1[0]*a2[1] - a1[1]*a2[0]
G1 = 2*np.pi*np.array([a2[1], -a2[0]])/det
G2 = 2*np.pi*np.array([-a1[1], a1[0]])/det

def haldane_H(u, v, M, t2, sphi, t1=1.0):
    """H(u,v) avec k = u*G1 + v*G2, u,v in [0,1)."""
    k = u*G1 + v*G2
    f = sum(np.exp(1j*np.dot(k, d)) for d in (d1, d2, d3))
    dz = M - 2*t2*sphi*sum(np.sin(np.dot(k, b)) for b in (b1, b2, b3))
    return np.array([[dz, t1*f], [t1*np.conj(f), -dz]], dtype=complex)

def occ_vec(H):
    w, V = np.linalg.eigh(H)
    return V[:, 0]                                  # bande occupee (plus basse)

def chern_FHS(Hfunc, N=36):
    """Chern de la bande occupee par variables de liaison de Berry (Fukui-Hatsugai-Suzuki)."""
    U1 = np.zeros((N, N), complex); U2 = np.zeros((N, N), complex)
    for i in range(N):
        for j in range(N):
            u, v = i/N, j/N
            n = occ_vec(Hfunc(u, v))
            n1 = occ_vec(Hfunc(((i+1) % N)/N, v)); n2 = occ_vec(Hfunc(u, ((j+1) % N)/N))
            l1 = np.vdot(n, n1); l2 = np.vdot(n, n2)
            U1[i, j] = l1/abs(l1); U2[i, j] = l2/abs(l2)
    F = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            f = (U1[i, j]*U2[(i+1) % N, j])/(U1[i, (j+1) % N]*U2[i, j])
            F[i, j] = np.angle(f)
    return F.sum()/(2*np.pi)

# ---------- T1 : Chern de Haldane vs M/t2, frontiere 3 sqrt(3) sin phi ----------
t2, sphi = 0.3, 1.0                                # phi = pi/2
Ms = np.linspace(-7.0, 7.0, 57)*t2
Cs = []
for M in Ms:
    Cs.append(chern_FHS(lambda u, v, M=M: haldane_H(u, v, M, t2, sphi), N=30))
Cs = np.array(Cs)
# transition numerique : dernier |M| avec |C|>0.5
idx = np.where(np.abs(Cs) > 0.5)[0]
M_trans = np.abs(Ms[idx]).max() if len(idx) else 0.0
frontiere_theo = 3*SQRT3*t2*abs(sphi)
out["T1_haldane"] = {"C_dans_phase": sorted(set(np.round(Cs[idx]).astype(int).tolist())),
                     "M_transition_num/t2": round(float(M_trans/t2), 3),
                     "frontiere_theorique_3sqrt3/t2": round(float(frontiere_theo/t2), 4),
                     "accord": bool(abs(M_trans - frontiere_theo) < 0.3*t2)}

# ---------- T2 : frontiere derivee analytiquement ----------
# d_z(K) = M + 3 sqrt(3) t2 sin phi ; d_z(K') = M - 3 sqrt(3) t2 sin phi (sommes verifiees)
K = np.array([4*np.pi/(3*SQRT3), 0.0])
sK = sum(np.sin(np.dot(K, b)) for b in (b1, b2, b3))
sKp = sum(np.sin(np.dot(-K, b)) for b in (b1, b2, b3))
out["T2_frontiere_analytique"] = {"somme_sin_K": round(float(sK), 6),
    "valeur_theorique": round(float(-3*SQRT3/2), 6),
    "d_z_K": "M + 3√3 t2 sinφ", "d_z_Kp": "M - 3√3 t2 sinφ",
    "condition_fermeture": "|M/t2| = 3√3|sinφ| ≈ 5.196|sinφ|"}

# ---------- T3 : Kane-Mele = 2 copies Haldane (phi, -phi) ----------
C_up = chern_FHS(lambda u, v: haldane_H(u, v, 0.0, t2, +1.0), N=30)
C_dn = chern_FHS(lambda u, v: haldane_H(u, v, 0.0, t2, -1.0), N=30)
Z2 = int(round(abs(C_up - C_dn)/2)) % 2
out["T3_kane_mele"] = {"C_up": int(round(C_up)), "C_dn": int(round(C_dn)),
    "C_total": int(round(C_up + C_dn)), "Z2": Z2,
    "lecture": "C_total=0 (TR) mais Z2=1 : topologie sans Hall net"}

# ---------- T4 : correspondance bord-volume — ruban BHZ helicoidal ----------
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
m_bhz = -1.0
def bloc(kx, ky, s):
    """s=+1 : h(k) ; s=-1 : h*(-k) (copie TR)."""
    return (s*np.sin(kx)*sx + np.sin(ky)*sy
            + (m_bhz + np.cos(kx) + np.cos(ky))*sz)
Ny = 16
def ruban_H(kx):
    H = np.zeros((4*Ny, 4*Ny), complex)
    for y in range(Ny):
        for sgn, off in ((+1, 0), (-1, 2)):
            diag = (sgn*np.sin(kx)*sx + (m_bhz + np.cos(kx))*sz)
            H[y*4+off:y*4+off+2, y*4+off:y*4+off+2] += diag
            if y < Ny-1:
                T = sy/(2j) + sz/2.0                  # hopping y -> y+1
                H[y*4+off:y*4+off+2, (y+1)*4+off:(y+1)*4+off+2] += T
                H[(y+1)*4+off:(y+1)*4+off+2, y*4+off:y*4+off+2] += T.conj().T
    return H
kxs = np.linspace(0, 2*np.pi, 61)
spec = np.array([np.linalg.eigvalsh(ruban_H(kx)) for kx in kxs])
# paires de Kramers a E=0 aux TRIM (croisement helicoidal epingle sur le TRIM)
tol = 0.1
def paires_kramers(kx):
    w = np.linalg.eigvalsh(ruban_H(kx))
    return int(np.sum(np.abs(w) < tol)//2)
P0, Ppi = paires_kramers(0.0), paires_kramers(np.pi)
# P0=2 (une paire par bord, deux bords), Ppi=0 ; par bord : 1 vs 0 -> parites differentes
Z2_bord = int((P0//2 + Ppi//2) % 2)          # par bord
accord_bord = (P0 % 2 == 0 and P0 > 0 and Ppi == 0)
out["T4_ruban"] = {"Ny": Ny, "m": m_bhz,
    "paires_Kramers_k=0": P0, "paires_Kramers_k=pi": Ppi,
    "par_bord": f"{P0//2} vs {Ppi//2}",
    "Z2_bord": Z2_bord, "accord": bool(accord_bord and Z2_bord == 1),
    "lecture": "paire de Kramers a E=0 epinglee sur k=0 (un par bord), aucune a k=pi : helicoidal, Z2=1 par le bord"}

# ---------- T5 : 3D Wilson-Dirac — parite aux TRIM ----------
def nu0_trim(m):
    masses = [m+3, m+1, m+1, m+1, m-1, m-1, m-1, m-3]
    deltas = [-np.sign(x) for x in masses]
    return int(0 if np.prod(deltas) > 0 else 1)
# verification numerique : parite des paires de Kramers aux TRIM = valeur propre de Gamma0 (operateur d'inversion)
G1d = np.array([np.kron(sx, sx), np.kron(sx, sy), np.kron(sx, sz)])  # Gamma_i = t_x ⊗ s_i
G0 = np.kron(sz, np.eye(2))
def H3(kx, ky, kz, m):
    return (np.sin(kx)*G1d[0] + np.sin(ky)*G1d[1] + np.sin(kz)*G1d[2]
            + (m + np.cos(kx) + np.cos(ky) + np.cos(kz))*G0)
TRIM = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
def parites_numeriques(m):
    """delta_a = parite de la paire occupee au TRIM a, mesuree par <Gamma0>."""
    deltas = []
    for (a, b, c) in TRIM:
        w, V = np.linalg.eigh(H3(a*np.pi, b*np.pi, c*np.pi, m))
        occ = V[:, w < 0]
        xi = np.sign(np.real(np.diag(occ.conj().T @ G0 @ occ)))
        deltas.append(int(xi[0]))
    return deltas
def nu0_numerique(m):
    return int(0 if np.prod(parites_numeriques(m)) > 0 else 1)
m_scan = np.arange(-4.5, 4.51, 0.5)
nu0_list = [nu0_trim(m) for m in m_scan]
check_ms = [-2.0, -0.5, 2.0, 0.5, 3.5, -3.5]
checks = []
for m in check_ms:
    n_num, n_ana = nu0_numerique(m), nu0_trim(m)
    checks.append({"m": m, "nu0_numerique": n_num, "nu0_analytique": n_ana,
                   "accord": bool(n_num == n_ana)})
out["T5_3D"] = {"masses_TRIM": "m+3 (x1), m+1 (x3), m-1 (x3), m-3 (x1)",
    "critere": "(-1)^nu0 = prod_a [-sgn(m_a)], parites mesurees par <Gamma0> aux 8 TRIM",
    "phases_fortes": "1 < |m| < 3",
    "verifications": checks,
    "accord_global": all(c["accord"] for c in checks)}

# ---------- T6 : levier discriminant ----------
C_phi0 = chern_FHS(lambda u, v: haldane_H(u, v, 0.0, t2, 0.0), N=30)   # phi=0 : TR restaure
C_t20 = chern_FHS(lambda u, v: haldane_H(u, v, 0.0, 0.0, 1.0), N=30)  # t2=0 : graphene massless->M=0
C_Mlarge = chern_FHS(lambda u, v: haldane_H(u, v, 3.0, t2, 1.0), N=30)
nu0_hors = nu0_trim(4.0)
out["T6_levier"] = {"C_phi=0": int(round(C_phi0)), "C_t2=0": int(round(C_t20)),
    "C_|M|>3sqrt3": int(round(C_Mlarge)), "nu0_m=4": nu0_hors,
    "conclusion": "sans flux (phi=0) ou hors fenetre de masse : trivial — la topologie exige le mecanisme"}

# ---------- verdict ----------
criteres = {
    "C1_Chern_Haldane_+-1_et_0": out["T1_haldane"]["accord"] and len(out["T1_haldane"]["C_dans_phase"]) == 1,
    "C2_frontiere_3sqrt3_exacte": abs(sK + 3*SQRT3/2) < 1e-9,
    "C3_KaneMele_Z2": (out["T3_kane_mele"]["C_total"] == 0 and Z2 == 1),
    "C4_bord_volume_ruban": out["T4_ruban"]["accord"],
    "C5_3D_parite_TRIM": out["T5_3D"]["accord_global"],
    "C6_levier": (out["T6_levier"]["C_phi=0"] == 0 and out["T6_levier"]["C_|M|>3sqrt3"] == 0
                  and out["T6_levier"]["nu0_m=4"] == 0),
}
criteres = {k: bool(v) for k, v in criteres.items()}
nb = sum(criteres.values())
out["verdict"] = {"criteres": criteres, "score": f"{nb}/6",
    "statut": "SUCCES" if nb == 6 else ("SUCCES PARTIEL" if nb >= 4 else "ECHEC")}

# ---------- figure ----------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13.5, 3.9))
ax1.plot(Ms/t2, Cs, "o-", color="tab:blue", ms=4)
for s in (-1, 1):
    ax1.axvline(s*3*SQRT3*abs(sphi), color="tab:red", ls="--", lw=1.2,
                label=r"$\pm 3\sqrt{3}\sin\varphi$" if s > 0 else None)
ax1.set_xlabel(r"$M/t_2$"); ax1.set_ylabel("Chern C"); ax1.set_title("Haldane : transition à $3\\sqrt{3}$")
ax1.legend(fontsize=8)
sub2 = kxs <= 2*np.pi
for n in range(4*Ny):
    ax2.plot(kxs, spec[:, n], color="tab:blue", lw=0.5, alpha=0.6)
ax2.axhline(0, color="k", lw=0.6)
ax2.set_xlim(0, 2*np.pi); ax2.set_ylim(-1.2, 1.2)
ax2.set_xticks([0, np.pi, 2*np.pi]); ax2.set_xticklabels(["0", r"$\pi$", r"$2\pi$"])
ax2.set_xlabel(r"$k_x$"); ax2.set_ylabel("E"); ax2.set_title("Ruban BHZ : bord hélicoïdal")
ax3.plot(m_scan, nu0_list, "s-", color="tab:blue", ms=4)
for xm in (-3, -1, 1, 3):
    ax3.axvline(xm, color="tab:red", ls="--", lw=1.0)
ax3.set_xlabel("m"); ax3.set_ylabel(r"$\nu_0$"); ax3.set_title("3D : indice fort (TRIM)")
fig.tight_layout()
fig.savefig("/mnt/agents/output/e44_data/p25_topologie.png", dpi=140)

with open("/mnt/agents/output/e44_data/p25_topologie.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
for fn in ["p25_topologie.py", "p25_topologie.json", "p25_topologie.png"]:
    print(fn, sha(f"/mnt/agents/output/e44_data/{fn}"))
print(json.dumps(out["verdict"], indent=2, ensure_ascii=False))
print("T1:", out["T1_haldane"]); print("T3:", out["T3_kane_mele"])
print("T4 paires Kramers (0, pi):", P0, Ppi, "| T5 accord:", out["T5_3D"]["accord_global"])
