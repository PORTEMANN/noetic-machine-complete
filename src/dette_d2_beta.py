# -*- coding: utf-8 -*-
"""Dette D2 (premiere passe) — la fonction beta de l'escalier.

Derivee formelle : l'escalier est l'integrale exacte d'une beta
fermionique a une boucle a contenu de saveurs Heaviside :
    d alpha^-1 / d ln(Lambda) = -(1/2 pi)(4/3) Somme_active N_c Q^2
(meme forme que la beta QED standard ; les seuils constituent
habilles portent le contenu non perturbatif).

Decomposition chiffree a M_Z (zero parametre ajuste) :
  modele (escalier)          vs canonique PDG (Delta alpha = 0.0590 +- 5e-4)
  ecart localise : leptons (boucles superieures QED),
  secteur hadronique leger (seuils habilles vs VP hadronique),
  bosons W/Z/H + ordres superieurs.
"""
import numpy as np

A0 = 137.035999084
MZ = 91.1876
EXP_INV = 127.951  # PDG (sourcé : 127.951(9))
CANON_DA = 0.0590  # PDG electroweak (sourcé : 0.0590 +- 0.0005)
CANON_DA_LEP = 0.03150   # revue PDG electroweak (standard)
CANON_DA_HAD = 0.02757   # revue PDG electroweak, Delta alpha_had^(5)

C = 2.0 / (3.0 * np.pi)

steps = [("e", 0.00051099895, 1.0), ("mu", 0.1056583755, 1.0),
         ("u", 0.312757, 4/3), ("d", 0.312757, 1/3), ("s", 0.4962, 1/3),
         ("c", 1.27, 4/3), ("tau", 1.77686, 1.0), ("b", 4.18, 1/3),
         ("t", 172.69, 4/3)]
ouvert = [(n, m, w) for n, m, w in steps if m < MZ]

dinv_modele = C * sum(w * np.log(MZ / m) for _, m, w in ouvert)
inv_modele = A0 - dinv_modele
print("=== beta derivee ===")
print("d alpha^-1/d ln Lambda = -(1/2 pi)(4/3) Somme_active N_c Q^2")
print(f"R(Lambda) = somme active : M_Z -> {sum(w for _,_,w in ouvert):.4f} (t ferme)")
print()
print("=== decomposition a M_Z ===")
print(f"modele    : alpha^-1 = {inv_modele:.4f} | Delta(alpha^-1) = {dinv_modele:.4f}")
canon_dinv = A0 - EXP_INV
print(f"canon PDG : alpha^-1 = {EXP_INV:.4f} | Delta(alpha^-1) = {canon_dinv:.4f}")
deficit = canon_dinv - dinv_modele
print(f"deficit du modele (Delta alpha^-1) : {deficit:+.4f}")
da_modele = 1 - inv_modele / A0
print(f"en unites Delta alpha : modele {da_modele:.5f} | canon {CANON_DA:.5f} "
      f"| ecart {da_modele - CANON_DA:+.5f}")

print()
print("=== localisation de l'ecart (Delta alpha) ===")
d_lep = C * sum(w * np.log(MZ / m) for n, m, w in ouvert if n in ("e", "mu", "tau"))
da_lep_1loop = d_lep / A0
print(f"leptons 1 boucle (modele)      : {da_lep_1loop:.5f} | canon 3 boucles : "
      f"{CANON_DA_LEP:.5f} | ordres superieurs QED : {CANON_DA_LEP - da_lep_1loop:+.5f}")
d_q = dinv_modele - d_lep
print(f"secteur quark (modele, seuils habilles) : {d_q / A0:.5f}")
print(f"VP hadronique canonique (non pert.)     : {CANON_DA_HAD:.5f}")
print(f"-> le modele porte le secteur habille dans SES seuils ;")
print(f"   le residu W/Z/H + 2 boucles + matching reste a deriver (D2b-D2d).")

print()
print("=== programme D2 ===")
print("D2a (ce script) : beta une boucle derivee + decomposition. SOLDEE en passe 1.")
print("D2b : conditions de matching aux seuils (decouplage EFT propre).")
print("D2c : boucles W/Z/H (contributions EW a la VP du photon).")
print("D2d : 2e boucle QED+QCD + renormalisation MSbar->pole.")
print("D2e : pont hadronique — Pi_had(s) mesuree (e+e-) vs seuils habilles.")
