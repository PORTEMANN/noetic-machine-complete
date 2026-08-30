#!/usr/bin/env python3
# P31 — La portee derivee : dernier test de la frontiere r12
# u(r) = (1/2) r exp(-beta r) : cusp 1/2 impose (Kato), factorisation imposee (u->0 a l'infini)
# beta fixe par UNE regle derivee, 0 parametre libre :
#   R1 echelle      : beta = (a+b)/2 (seule longueur du probleme)
#   R2 orthogonalite: <u' cos theta12>_{Psi J} = 0 (reponse 2-corps pure, P28)
#   R3 densite      : <r1^2>_{Psi J} = <r1^2>_Phi (coeur invariant 1-corps, P28)
# Criteres geles : si aucune regle ne bat la borne split-zeta (meme integrateur),
# la frontiere r12 est DECLAREE CONSTITUTIVE et publiee comme telle.
import numpy as np, json, hashlib, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = {"chantier": "P31", "titre": "Portee derivee du facteur a deux corps — frontiere r12 ?"}
E_HF = -(27/16)**2            # -2.84765625
E_EXACT = -2.903724377        # Pekeris
t0 = time.time()

r1d = np.linspace(1e-7, 14, 300)
R1, R2 = np.meshgrid(r1d, r1d, indexing="ij")
ABS = np.abs(R1 - R2); SUM = R1 + R2
W0 = 8*np.pi**2 * R1 * R2
def slater(r, z): return z**1.5*np.exp(-z*r)

def he_full(a, b, c, beta, npts=192):
    """u(r) = c r e^{-beta r}. Retourne E, terme croise, <r1^2>."""
    A1 = slater(R1, a); B2 = slater(R2, b)
    Phi2 = (A1*B2)**2
    uq = np.linspace(1e-9, 2*r1d[-1], npts)
    den = num = num_cross = num_r1sq = 0.0
    for u in uq:
        M = (ABS <= u) & (u <= SUM)
        if not M.any(): continue
        ebu = np.exp(-beta*u)
        up = c*ebu*(1 - beta*u)                 # u'
        upp = c*ebu*(beta*beta*u - 2*beta)      # u''
        cos1 = np.clip((R1**2 + R2**2 - u**2)/(2*R1*R2), -1, 1)
        J2 = np.exp(2*c*u*ebu)
        wPhi = W0 * u * J2 * M * Phi2
        den += np.trapezoid(np.trapezoid(wPhi, r1d, axis=1), r1d)
        f = ( 0.5*(a*a + b*b)
              + 0.5*(2*up*up - 2*upp - 4*up/u)
              + up*cos1*(a + b)
              - 2/R1 - 2/R2 + 1/u )
        num += np.trapezoid(np.trapezoid(wPhi*f, r1d, axis=1), r1d)
        num_cross += np.trapezoid(np.trapezoid(wPhi*up*cos1*(a + b), r1d, axis=1), r1d)
        num_r1sq += np.trapezoid(np.trapezoid(wPhi*R1**2, r1d, axis=1), r1d)
    return {"E": num/den, "cross": num_cross/den, "r1sq": num_r1sq/den}

def scan_ab(c, beta_mode, beta_fixe=None, pas=0.1, amin=1.5, amax=2.31):
    """beta_mode: 'echelle' -> beta=(a+b)/2 ; 'fixe' -> beta=beta_fixe ; c=0 -> split seul."""
    res = []
    for a in np.arange(amin, amax, pas):
        for b in np.arange(amin, amax, pas):
            beta = (a+b)/2 if beta_mode == "echelle" else (beta_fixe if beta_fixe else 1.0)
            r = he_full(a, b, c, beta)
            res.append((r["E"], a, b, beta))
    res.sort()
    return res[0]

# ---------- T0 : controle ----------
ctl = he_full(1.6875, 1.6875, 0.0, 1.0)
out["T0_controle"] = {"E_c=0_HF": round(ctl["E"], 5), "cible": E_HF,
    "accord": bool(abs(ctl["E"] - E_HF) < 0.02), "r1sq_Phi": round(ctl["r1sq"], 4)}

# ---------- T1 : diagnostic libre beta (publie comme levier, pas comme reponse) ----------
betas = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
diag = []
for bt in betas:
    r = he_full(1.6875, 1.6875, 0.5, bt)
    diag.append({"beta": bt, "E": round(r["E"], 5), "cross": round(r["cross"], 5),
                 "r1sq": round(r["r1sq"], 4)})
diag.sort(key=lambda d: d["E"])
beta_star_E = diag[0]["beta"]
out["T1_diagnostic_beta_libre"] = {"grille": diag, "beta*_E_non_contraint": beta_star_E}

# ---------- R1 : echelle beta=(a+b)/2 ----------
E_R1, a1, b1, be1 = scan_ab(0.5, "echelle")
out["R1_echelle"] = {"regle": "beta=(a+b)/2", "E_min": round(E_R1, 5),
    "(a,b)": (round(a1, 2), round(b1, 2)), "beta": round(be1, 3)}

# ---------- R2 : orthogonalite (terme croise nul, resolu a Phi=HF puis scan (a,b)) ----------
def cross_of(beta): return he_full(1.6875, 1.6875, 0.5, beta)["cross"]
cr = {bt: cross_of(bt) for bt in betas}
bracket = None
for i in range(len(betas)-1):
    if cr[betas[i]]*cr[betas[i+1]] < 0:
        bracket = (betas[i], betas[i+1]); break
if bracket:
    lo, hi = bracket
    for _ in range(22):
        mid = (lo+hi)/2
        if cross_of(lo)*cross_of(mid) <= 0: hi = mid
        else: lo = mid
    beta_R2 = (lo+hi)/2
else:
    beta_R2 = None
out["R2_orthogonalite"] = {"regle": "<u' cos theta> = 0 dans l'etat d'essai",
    "cross_par_beta": {str(bt): round(v, 5) for bt, v in cr.items()}}
if beta_R2:
    E_R2_hf = he_full(1.6875, 1.6875, 0.5, beta_R2)["E"]
    E_R2, a2, b2, _ = scan_ab(0.5, "fixe", beta_R2)
    out["R2_orthogonalite"].update({"beta_R2": round(beta_R2, 4), "E_a_Phi_HF": round(E_R2_hf, 5),
        "E_min": round(E_R2, 5), "(a,b)": (round(a2, 2), round(b2, 2))})
else:
    out["R2_orthogonalite"]["solution"] = "aucune — regle inapplicable (publie comme tel)"
    E_R2, a2, b2 = None, None, None

# ---------- R3 : densite (<r1^2> preserve) ----------
r1sq_Phi = ctl["r1sq"]
def dr1sq(beta): return he_full(1.6875, 1.6875, 0.5, beta)["r1sq"] - r1sq_Phi
dvals = {bt: dr1sq(bt) for bt in betas}
bracket = None
for i in range(len(betas)-1):
    if dvals[betas[i]]*dvals[betas[i+1]] < 0:
        bracket = (betas[i], betas[i+1]); break
if bracket:
    lo, hi = bracket
    for _ in range(22):
        mid = (lo+hi)/2
        if dr1sq(lo)*dr1sq(mid) <= 0: hi = mid
        else: lo = mid
    beta_R3 = (lo+hi)/2
else:
    beta_R3 = None
out["R3_densite"] = {"regle": "<r1^2>_{Psi J} = <r1^2>_Phi",
    "r1sq_Phi": round(r1sq_Phi, 4),
    "delta_par_beta": {str(bt): round(v, 4) for bt, v in dvals.items()}}
if beta_R3:
    E_R3_hf = he_full(1.6875, 1.6875, 0.5, beta_R3)["E"]
    E_R3, a3, b3, _ = scan_ab(0.5, "fixe", beta_R3)
    out["R3_densite"].update({"beta_R3": round(beta_R3, 4), "E_a_Phi_HF": round(E_R3_hf, 5),
        "E_min": round(E_R3, 5), "(a,b)": (round(a3, 2), round(b3, 2))})
else:
    out["R3_densite"]["solution"] = "aucune"
    E_R3, a3, b3 = None, None, None

# ---------- reference : split-zeta seul, MEME integrateur ----------
E_sp, as_, bs_, _ = scan_ab(0.0, "fixe", 1.0)
out["reference_split_zeta"] = {"E_min": round(E_sp, 5), "(a,b)": (round(as_, 2), round(bs_, 2)),
    "P27_51.5pct": "E ~ -2.8765 (MC P27)"}

# ---------- verdict (criteres geles) ----------
candidats = [("R1", E_R1)] + ([("R2", E_R2)] if E_R2 else []) + ([("R3", E_R3)] if E_R3 else [])
candidats.sort(key=lambda x: x[1])
nom_best, E_best = candidats[0]
beta_best = {"R1": be1, "R2": beta_R2, "R3": beta_R3}[nom_best]
gain = E_sp - E_best
resid = E_sp - E_EXACT
criteres = {
    "C0_integrateur_valide": bool(abs(ctl["E"] - E_HF) < 0.02),
    "C1_une_regle_bat_split-zeta": bool(E_best < E_sp),
    "C2_gain_>=20pct_residuel": bool(gain >= 0.20*resid),
    "C3_beta_derive_proche_beta*": bool(min(
        [abs(np.log(be1/beta_star_E))]
        + ([abs(np.log(beta_R2/beta_star_E))] if beta_R2 else [])
        + ([abs(np.log(beta_R3/beta_star_E))] if beta_R3 else [])) <= np.log(2)),
    "C4_zero_parametre": True,
}
criteres = {k: bool(v) for k, v in criteres.items()}
nb = sum(criteres.values())
out["verdict"] = {"criteres": criteres, "score": f"{nb}/5",
    "statut": "SUCCES" if nb == 5 else ("SUCCES PARTIEL" if nb >= 3 else "ECHEC — FRONTIERE CONSTITUTIVE"),
    "meilleure_regle": nom_best, "E_best": round(E_best, 5), "E_split": round(E_sp, 5),
    "gain_Ha": round(gain, 5), "residuel_split_Ha": round(resid, 5),
    "declaration": ("la portee est derivable — premiere brique de la reponse a deux corps"
        if nb == 5 else
        ("progres partiel — la portee reste partiellement libre" if nb >= 3 else
         "FRONTIERE r12 DECLAREE CONSTITUTIVE : contact derivable, portee non derivable sans parametre"))}
out["meta"] = {"grille": "r 300, u 192", "duree_s": round(time.time()-t0, 1)}

# ---------- figure ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))
d = sorted(out["T1_diagnostic_beta_libre"]["grille"], key=lambda x: x["beta"])
ax1.plot([x["beta"] for x in d], [x["E"] for x in d], "o-", ms=5, color="tab:blue",
         label=r"$E(\beta)$ à $\Phi$ HF, cusp 1/2")
ax1.axhline(E_EXACT, color="k", ls=":", lw=1, label="exact")
ax1.axhline(E_sp, color="gray", ls="--", lw=1, label=f"split-ζ (même intégrateur) = {E_sp:.4f}")
for bt, lab, col in [(be1, "R1", "tab:green"), (beta_R2, "R2", "tab:red"), (beta_R3, "R3", "tab:purple")]:
    if bt: ax1.axvline(bt, color=col, ls="--", lw=1.1, label=f"{lab} dérivé β={bt:.2f}")
ax1.set_xlabel(r"portée $\beta$"); ax1.set_ylabel("E (Ha)")
ax1.set_title("Les règles dérivées vs l'optimum libre"); ax1.legend(fontsize=7)
labs = ["HF", "split-ζ", "R1", "R2", "R3", "exact"]
vals = [ctl["E"], E_sp, E_R1, E_R2 if E_R2 else np.nan, E_R3 if E_R3 else np.nan, E_EXACT]
ax2.bar(labs, [v - E_EXACT for v in vals],
        color=["gray", "tab:blue", "tab:green", "tab:red", "tab:purple", "k"])
ax2.set_ylabel("E − E_exact (Ha)"); ax2.set_title("Distance à l'exact (plus bas = mieux)")
fig.tight_layout()
fig.savefig("/mnt/agents/output/e44_data/p31_portee.png", dpi=140)

with open("/mnt/agents/output/e44_data/p31_portee.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
for fn in ["p31_portee.py", "p31_portee.json", "p31_portee.png"]:
    print(fn, sha(f"/mnt/agents/output/e44_data/{fn}"))
print(json.dumps(out["verdict"], indent=2, ensure_ascii=False))
print("R1:", out["R1_echelle"])
print("R2:", out["R2_orthogonalite"].get("beta_R2"), out["R2_orthogonalite"].get("E_min"))
print("R3:", out["R3_densite"].get("beta_R3"), out["R3_densite"].get("E_min"))
print("split:", out["reference_split_zeta"], "| beta*_E:", beta_star_E)
