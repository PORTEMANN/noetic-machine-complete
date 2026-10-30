# -*- coding: utf-8 -*-
"""D1e — physique effective de la masse constituante (premiere passe).

Question ouverte de D1d : pourquoi la masse constituante est-elle la
bonne variable d'un modele a seuils discrets ?

Ancrage 1 (D1d, baryons)  : m_q = m_N/3 = 313 MeV ; m_s via hyperons = 496.
Ancrage 2 (ce script, moments magnetiques, zero parametre, PDG) :
  modele NR a quarks constituants : mu_p = e/(2 m_q) -> m_q = m_N/mu_p
  (en unites du magneton nucleaire) ; test mu_n/mu_p = -2/3.
Pont IR : le seuil est un phenomene infrarouge — la sonde a
Lambda ~ 300-500 MeV voit des quarks habilles, non des partons
(R-hadronique resonant vs R partonique 2 — a documenter avant scellement).
"""
import numpy as np

M_P = 0.938272088
MU_P, MU_N = 2.79284734462, -1.91304273  # magnetons nucleaires (PDG)

# ancrage 2 : moment magnetique du proton
mq_mu = M_P / MU_P
print(f"Ancrage 2 — moments magnetiques (zero parametre, PDG)")
print(f"  mu_p = {MU_P:.6f} mu_N  ->  m_q^const = m_p/mu_p = {mq_mu*1000:.1f} MeV")
print(f"  mu_n/mu_p predit (-2/3) = {-2/3:.4f} | mesure = {MU_N/MU_P:.4f} "
      f"| ecart {abs(-2/3 - MU_N/MU_P)/(2/3)*100:.1f} %")

# synthese des trois ancrages independants
a1, a1s = 312.97, 496.2   # D1d : baryons
a2 = mq_mu * 1000          # moments magnetiques
print(f"\nSynthese des ancrages de m_q^const :")
print(f"  baryons (D1d)      : {a1:7.1f} MeV")
print(f"  moments magnetiques: {a2:7.1f} MeV")
et = (a2 - a1) / a1 * 100
print(f"  dispersion inter-ancrages : {et:.1f} % (corrections spin/orbite du NR)")
print(f"  -> le concept 'masse constituante' est SURDETERMINE par la")
print(f"     spectroscopie : deux observables independantes y ancrent")

# pont IR : le seuil comme phenomene habille
print(f"\nPont IR (a documenter avant scellement) :")
print(f"  sous ~ 2 GeV, sigma(e+e- -> hadrons) est RESONNANT (rho, omega, phi)")
print(f"  et non partonique : R_mesure != 3*Somme(Q_f^2) = 2.")
print(f"  Un seuil a Lambda ~ 300-500 MeV est donc franchi par des")
print(f"  degres de liberte habilles : la masse constituante est la")
print(f"  variable exacte du regime. Valeurs R quantitatives : a sourcer")
print(f"  dans la revue PDG e+e- (chantier D2, dette beta fonctions).")

# lien explicite avec la dette D2
print(f"\nLien avec le registre des dettes :")
print(f"  l'escalier = integrale d'une fonction beta dont le contenu")
print(f"  leger est habille ; DERIVER cette beta = dette D2.")
