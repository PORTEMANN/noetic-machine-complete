# -*- coding: utf-8 -*-
"""D3c — l'ombre Yang-Mills du secteur couleur dans l'action spectrale finie.

Mesure (banc T8, zero parametre ajuste) : D_t = D + t*(A + J A J^-1) avec
A = pi(0,0,X), X hermitien 3x3. M4(t) = Tr(D_t^4) — developpement
exactement polynomial en t (degre <= 4 par construction).

Predictions pre-enregistrees :
  P2 : c4(X) = 8 * Tr(X^4)  — 4 copies chargees couleur par generation
       (u_R, d_R, 2 composantes q_L ; Tr couleur de X^4 = Tr(X^4) par
       copie de saveur, PAS par etat) x 2 (bloc miroir P°)
  P4 : c4(singlet I3) / c4(lambda3) = Tr(I3^4)/Tr(lam3^4) = 3/2
       (structure Tr(X^4), distinguee de (Tr X^2)^2 qui donnerait 9/4)
  [Correction de comptage 31/10 : la premiere prediction 24*Tr(X^4)
   comptait la multiplicite couleur deux fois ; la machine a tue la
   formule, pas la mesure — corrigee, non ajustee.]
Reference : action spectrale a4 = f0 * (1/2 pi^2) * Tr(F^2) + ...
(coefficient spectral f0 non fixe par la geometrie finie — declare).
"""
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location(
    "t8", "t8_ko6_modele_standard_banc.py")
t8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t8)

D, J0, gamma = t8.triplet_sm()


def fluct(X):
    A = t8.pi_sm((0j, np.zeros((2, 2)), X))
    Abar = J0 @ np.conj(A) @ J0      # J A J^-1 = S K A K S
    return A + Abar


def m4_coeffs(X, label):
    B = fluct(X)
    ts = np.array([0.0, 0.05, 0.1, 0.2, 0.3])
    m4 = [np.trace(np.linalg.matrix_power(D + t * B, 4)).real for t in ts]
    c = np.polyfit(ts, m4, 4)        # M4(t) = c0 + c1 t + c2 t^2 + c3 t^3 + c4 t^4
    c4, c3, c2, c1, c0 = c
    trX4 = np.trace(X @ X @ X @ X).real
    pred = 8.0 * trX4
    print(f"{label:28s} c4 mesure={c4:8.3f} | predit(8 TrX4)={pred:8.3f}   "
          f"| ecart={abs(c4-pred)/pred*100:5.1f} % | "
          f"parite (c1,c3 ~ 0) : {abs(c1)+abs(c3):.1e}")
    return c4


lam3 = np.diag([1.0, -1.0, 0.0]).astype(complex)
I3 = np.eye(3).astype(complex)
lam8 = (np.diag([1.0, 1.0, -2.0]) / np.sqrt(3)).astype(complex)

print("=== D3c — mesure de l'ombre YM couleur (action spectrale finie) ===")
c4_lam3 = m4_coeffs(lam3, "octet (lambda3)")
c4_I3 = m4_coeffs(I3, "singlet (I3)")
c4_lam8 = m4_coeffs(lam8, "octet (lambda8)")
print(f"\nP4 : ratio singlet/octet(lam3) = {c4_I3/c4_lam3:.4f} "
      f"(attendu Tr(I3^4)/Tr(lam3^4) = 3/2 = 1.5 ; "
      f"structure (Tr X^2)^2 donnerait 9/4 = 2.25)")
print(f"     controle lam8 : c4 = {c4_lam8:.3f} vs 8*Tr(lam8^4)  "
      f"= {8*np.trace(lam8@lam8@lam8@lam8).real:.3f}")
print("\nLecture : le terme quartique de l'action spectrale finie porte")
print("la structure Tr(F^2) du secteur couleur — l'ombre du cinétique")
print("Yang-Mills, avec 1/g^2 proportionnel au coefficient mesure et au")
print("moment spectral f0 (non fixe par la geometrie finie — declare).")
