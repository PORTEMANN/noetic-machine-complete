#!/usr/bin/env python3
# P1 - spectre des etats lies de l'electron (scalaire charge) dans le champ du
# monopole SU(2) mesure (P0). Le monopole fournit :
#   - potentiel Coulomb  V_c = -q_eff / r   (charge du noyau, queue 1/r)
#   - potentiel de moment magnetique du monopole : le flux K(xi) habille donne
#     un champ B ~ g_mag/r^2 -> terme de Pauli / spin-orbite effectif.
# L'electron = scalaire du corpus (masse m_e, couplage minimal mesure G13).
# Equation radiale de Schrodinger sur le fond monopole :
#   [-1/(2 m) d2/dr2 + l(l+1)/(2 m r^2) + V_c(r) + V_mag(r)] u = E u
# On diagonalise sur la grille radiale -> energies propres + fonctions d'onde.
# Cible corpus (G15) : orbites r_n = n^2 a0, R_cut = 3.04, facteur 92.45.
import os, json
import numpy as np
from scipy.linalg import eigh_tridiagonal

# --- fond monopole (P0, rho=1) : profil K(xi) -> charge effective et B ---
d = json.load(open('/mnt/agents/output/e44_data/p0_p0_r1.json'))
xi_m = np.array(d['xi']); K_m = np.array(d['K']); H_m = np.array(d['H'])
# densite de K aux 20 points (sous-echantillonne) -> on re-echantillonne fin
XI_MAX = xi_m[-1]

# --- parametres corpus / ancrage ---
# unites atomiques effectives du banc : m_e=1, q via couplage minimal mesure.
# L'ancrage (G14/G15) : c/c_s=120 fixe l'echelle ; a0 = echelle de Bohr.
# On travaille en unites reduites : a0 = 1, energies en Rydberg effectifs.
M_E   = float(os.environ.get("M_E", "1.0"))      # masse electron (unites banc)
ALPHA = float(os.environ.get("ALPHA", str(1/137.036)))  # constante structure fine
# charge effective du monopole : queue Coulomb. g_mag du monopole = 1 (unites Dirac eg=1/2)
RMAX  = float(os.environ.get("RMAX", "40.0"))
NR    = int(os.environ.get("NR", "4000"))
TAG   = os.environ.get("TAG", "p1")

r = np.linspace(RMAX/NR, RMAX, NR)
dr = r[1]-r[0]

# --- potentiel Coulomb (charge ponctuelle, noyau stable) ---
V_c = -ALPHA/r

# --- potentiel de moment magnetique du monopole ---
# Le monopole de 't Hooft-Polyakov a un champ magnetique B = g_mag r_hat / r^2
# au-dela du coeur (xi >~ 3). L'interaction d'un scalaire charge avec ce champ
# n'est PAS de Pauli (pas de spin) -> pour un SCALAIRE, seul le Coulomb + le
# couplage minimal |p - qA|^2. Le monopole a A purement de jauge a l'infini
# (charge magnetique, pas electrique) -> un scalaire ELECTRIQUEMENT charge ne
# voit que... rien a l'infini (A est pure jauge). L'etat lie exige une charge
# ELECTRIQUE du noyau -> c'est le dyon (monopole + charge electrique).
# G16/G17 : le deficit de densite = charge electrique localisee = dyon.
# On modelise : dyon de charge electrique Q_e (Coulomb) + coeur monopole.
# Le potentiel effectif : Coulomb attractif tronque a la taille du coeur R_core.
R_CORE = float(os.environ.get("R_CORE", "3.04"))   # taille du coeur (G15 : R_cut)
# Coulomb tronque au coeur (distribution de charge finie) :
V_eff = np.where(r >= R_CORE, -ALPHA/r, -ALPHA/R_CORE)

# --- Hamiltonien radial (scalaire, l=0..3) ---
def spectrum(l):
    # -1/(2m) u'' + [l(l+1)/(2 m r^2) + V_eff] u = E u
    diag = 1.0/(M_E*dr**2) + l*(l+1)/(2*M_E*r**2) + V_eff
    off  = -1.0/(2*M_E*dr**2)*np.ones(NR-1)
    evals, evecs = eigh_tridiagonal(diag, off, select='i', select_range=(0, 8))
    return evals, evecs

results = {}
for l in range(4):
    evals, evecs = spectrum(l)
    # rayon moyen de chaque etat
    rows = []
    for n in range(min(6, len(evals))):
        u = evecs[:, n]
        r2 = (u**2)
        r2 /= r2.sum()
        rmean = float((r*r2).sum())
        rows.append({"n": n+1+l, "l": l, "E": float(evals[n]), "r_mean": rmean})
    results[l] = rows
    print(f"[P1 {TAG}] l={l} : " + "  ".join(
        f"E{n+1+l}={rows[n]['E']:+.5f}(r={rows[n]['r_mean']:.2f})" for n in range(min(4,len(rows)))),
        flush=True)

# --- confrontation corpus G15 : orbites r_n = n^2 a0 ---
# energies attendues (Balmer effectif) : E_n = -ALPHA^2 M_E / (2 n^2)
print(f"[P1 {TAG}] reference Balmer : E_n = -a^2 m/(2 n^2)", flush=True)
for n in range(1, 5):
    E_balmer = -ALPHA**2*M_E/(2*n**2)
    print(f"  n={n} : E_Balmer={E_balmer:+.3e}  r_n=n^2 a0={n*n:.1f}", flush=True)

json.dump({"TAG": TAG, "ALPHA": ALPHA, "M_E": M_E, "R_CORE": R_CORE,
           "results": {str(k): v for k, v in results.items()}},
          open(f"/mnt/agents/output/e44_data/p1_{TAG}.json", "w"), indent=1)
print(f"[P1 {TAG}] sauve", flush=True)
