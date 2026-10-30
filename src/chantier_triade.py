# -*- coding: utf-8 -*-
"""Chantier triade — m_p/3 comme masse constituante effective.

Hypothese testee (zero parametre ajuste, masses PDG uniquement) :
les seuils u/d et s de l'escalier spectral sont les MASSES CONSTITUANTES
des quarks legers, ancrables par la spectroscopie baryonique :
  m_q^const = m_N / 3
  m_s^const (via Lambda) = m_Lambda - m_N + m_q^const
  m_s^const (via Xi)     = (m_Xi - m_q^const) / 2   [Xi = ssq]
comparees au seuil s = 0.500 GeV du corpus.
Test annexe : m_p/3 vs Lambda_QCD (PDG, nf = 3,4,5).
"""
import numpy as np

M_P, M_N = 0.938272088, 0.939565421
M_LAMBDA, M_XI = 1.115683, 1.318267
S_SEUIL = 0.500

m_N = (M_P + M_N) / 2
mq = m_N / 3
print(f"m_N (moyenne p,n)        = {m_N*1000:9.3f} MeV")
print(f"m_q^const = m_N/3        = {mq*1000:9.3f} MeV  (= seuil u/d triade)")

ms_lam = M_LAMBDA - m_N + mq
ms_xi = (M_XI - mq) / 2
ms = (ms_lam + ms_xi) / 2
print(f"\nm_s^const via Lambda     = {ms_lam*1000:9.3f} MeV")
print(f"m_s^const via Xi         = {ms_xi*1000:9.3f} MeV")
print(f"m_s^const moyenne        = {ms*1000:9.3f} MeV")
print(f"seuil s du corpus        = {S_SEUIL*1000:9.3f} MeV")
print(f"accord Lambda : {abs(ms_lam-S_SEUIL)/S_SEUIL*100:.1f} % | "
      f"Xi : {abs(ms_xi-S_SEUIL)/S_SEUIL*100:.1f} % | "
      f"moyenne : {abs(ms-S_SEUIL)/S_SEUIL*100:.1f} %")

# consequence sur l'escalier : seuil s = m_s^const mesure (zero choix)
ALPHA_0_INV, M_Z, EXP = 137.035999084, 91.1876, 127.952
steps = [("e", 0.00051099895, 1.0), ("mu", 0.1056583755, 1.0),
         ("u_triade", mq, 4.0/3.0), ("d_triade", mq, 1.0/3.0),
         ("s_const", ms, 1.0/3.0), ("c", 1.27, 4.0/3.0),
         ("tau", 1.77686, 1.0), ("b", 4.18, 1.0/3.0), ("t", 172.69, 4.0/3.0)]
d = sum(w*np.log(M_Z/m) for _, m, w in steps if m < M_Z)
pred = ALPHA_0_INV - (2/(3*np.pi))*d
err = abs(pred-EXP)/EXP*100
print(f"\nescalier avec s = m_s^const mesure : pred = {pred:.4f} "
      f"(ecart {err:.2f} %, {'S+' if err <= 1 else 'P' if err <= 2 else 'S-'})")

# annexe : m_p/3 vs Lambda_QCD (PDG 2022)
print("\n--- annexe : m_p/3 vs Lambda_QCD(MS) ---")
for lam, nf in [(0.334, 3), (0.294, 4), (0.213, 5)]:
    print(f"  Lambda^({nf}) = {lam*1000:.0f} MeV | "
          f"m_p/3 = {mq*1000:.1f} MeV | ecart {abs(mq-lam)/lam*100:.0f} %")
print("  -> m_p/3 n'est PAS Lambda_QCD (6-47 % d'ecart) ;")
print("     l'ancrage est la masse constituante (0.5 %), pas l'echelle de divergence.")
