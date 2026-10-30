# -*- coding: utf-8 -*-
"""Dette D1 — comptabilite de Kolmogorov : premiere mesure.

Le comite (COMITE-LECTURE-ACIDE, objection 1) soutient que le generateur
{phi, pi, e, sqrt(2), sqrt(3), 2^(1/12), entiers Fibonacci/Lucas,
dimensions de Lie} forme un reseau dense sur la droite reelle, et que
toute coincidence « sans parametre » a theta = 1-5 % doit etre penalisee
par la taille de la recherche (look-elsewhere).

Mesure livrée ici, sans jugement a priori : la DENSITE du reseau.
On enumere toutes les combinaisons
    v = n * phi^a * pi^b * e^c * 2^(d/12) * sqrt(2)^p * sqrt(3)^q
avec |a|,|b|,|c| <= 3, d in [-12, 12], p,q in {0,1}, n entier de Lucas
ou Fibonacci <= 1000 (ou n = 1), et on compte les valeurs distinctes
dans [1, 2000]. La densite moyenne (valeurs par octave) donne le nombre
d'essais effectifs N_eff contenu dans toute affirmation « tombe a theta
pres ».
"""
import numpy as np
from itertools import product

PHI = (1 + 5 ** 0.5) / 2

# generateur du reseau (bibliotheque declaree par le comite)
def fib_lucas_upto(m):
    fib, luc = [1, 1], [1, 3]
    while fib[-1] <= m:
        fib.append(fib[-1] + fib[-2])
    while luc[-1] <= m:
        luc.append(luc[-1] + luc[-2])
    return sorted(set(fib[:-1] + luc[:-1]))

N_S = fib_lucas_upto(1000)
values = set()
for a, b, c, d, p, q in product(range(-3, 4), range(-3, 4), range(-3, 4),
                                range(-12, 13), [0, 1], [0, 1]):
    base = (PHI ** a) * (np.pi ** b) * (np.e ** c) * (2.0 ** (d / 12.0)) \
        * (np.sqrt(2) ** p) * (np.sqrt(3) ** q)
    for n in N_S:
        v = base * n
        if 1.0 <= v <= 2000.0:
            values.add(round(v, 6))

vals = np.array(sorted(values))
print(f"valeurs distinctes du reseau dans [1, 2000] : {len(vals)}")
print(f"densite moyenne : {len(vals) / np.log2(2000):.1f} valeurs par octave")
print(f"espacement median relatif : {np.median(np.diff(vals) / vals[:-1]) * 100:.4f} %")

# N_eff : nombre de valeurs du reseau dans une fenetre +-1% d'une cible
# = penalite look-elsewhere exacte pour theta = 1%
for theta in (0.01, 0.05):
    hits_par_cible = []
    rng = np.random.default_rng(20261030)
    for _ in range(2000):
        t = rng.uniform(1, 2000)
        hits = np.sum(np.abs(vals - t) <= theta * t)
        hits_par_cible.append(hits)
    hits_par_cible = np.array(hits_par_cible)
    print(f"theta={theta:.0%} : hits moyens par cible aleatoire = "
          f"{hits_par_cible.mean():.2f} (mediane {np.median(hits_par_cible):.0f}, "
          f"max {hits_par_cible.max()})")

# application aux cibles du corpus (affirmations de classe « bibliotheque »)
CIBLES = [
    ("alpha^-1(IR) ~ 137 (horizon)", 137.036),
    ("alpha^-1(M_Z) predite", 128.397),
    ("masse ANU (MeV)", 83.8),
    ("m_triade = m_p/3 (MeV)", 312.757),
    ("2^(1/12) (demi-ton, x100)", 105.946),
    ("g-dague x 1e10", 1.2e-10 * 1e10),
]
print("\nCibles corpus — nombre de valeurs du reseau a theta = 1 % pres :")
for nom, t in CIBLES:
    if 1 <= t <= 2000:
        h = int(np.sum(np.abs(vals - t) <= 0.01 * t))
        print(f"  {nom:34s} cible={t:10.3f}  hits={h}")
