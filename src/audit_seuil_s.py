# -*- coding: utf-8 -*-
"""Audit des seuils de l'escalier spectral (muscle micro).

Question : la prediction alpha^-1(M_Z) = 128.397 (ecart 0.35 %, S+)
est-elle stable quand chaque seuil varie dans ses fourchettes honnetes
(PDG/MSbar/pole/constituante) ? Charge portante de chaque canal.
Aucun ajustement : scenarios declares, calcul direct.
"""
import numpy as np

ALPHA_0_INV = 137.035999084
M_Z = 91.1876
EXP = 127.952


def run(steps, label):
    """steps : liste (nom, masse, poids N_c Q^2). Fermions charges.
    Projecteur de Heaviside : seuil ouvert seulement si m < Lambda."""
    ouverts = [(n, m, w) for n, m, w in steps if m < M_Z]
    d = sum(w * np.log(M_Z / m) for _, m, w in ouverts)
    pred = ALPHA_0_INV - (2.0 / (3.0 * np.pi)) * d
    err = abs(pred - EXP) / EXP * 100
    verdict = "S+" if err <= 1.0 else ("P" if err <= 2.0 else "S-")
    fermes = [n for n, m, _ in steps if m >= M_Z]
    note = f" [ferme: {','.join(fermes)}]" if fermes else ""
    print(f"{label:58s} pred={pred:9.4f}  ecart={err:5.2f}%  {verdict}{note}")
    return pred, err


# scenario de base (corpus, tests.py)
BASE = [
    ("e", 0.00051099895, 1.0), ("mu", 0.1056583755, 1.0),
    ("u_triade", 0.312757, 4.0 / 3.0), ("d_triade", 0.312757, 1.0 / 3.0),
    ("s_const", 0.500, 1.0 / 3.0), ("c", 1.27, 4.0 / 3.0),
    ("tau", 1.77686, 1.0), ("b", 4.18, 1.0 / 3.0), ("t", 172.69, 4.0 / 3.0),
]
print("=" * 84)
run(BASE, "BASE (corpus : triade m_p/3, s constituante 0.500)")

print("\n--- sensibilite au seuil s (le point faible declare) ---")
for ms, lab in [(0.0935, "s MSbar(2GeV)=0.0935"), (0.075, "s bas PDG 0.075"),
                (0.120, "s haut PDG 0.120"), (0.300, "s intermediaire 0.300"),
                (0.500, "s constituante 0.500"), (0.950, "s courant 0.950")]:
    steps = [(n, ms if n == "s_const" else m, w) for n, m, w in BASE]
    run(steps, f"  s = {lab}")

print("\n--- sensibilite a la triade u/d ---")
for mu, md, lab in [(0.00214, 0.00470, "u/d MSbar physiques"),
                    (0.312757, 0.312757, "u/d triade m_p/3"),
                    (0.336, 0.336, "u/d = m_p/2.8 (test)")]:
    steps = [(n, mu if n == "u_triade" else md if n == "d_triade" else m, w)
             for n, m, w in BASE]
    run(steps, f"  {lab}")

print("\n--- sensibilite c, b, t (MSbar vs pole) ---")
steps = [(n, 1.67 if n == "c" else m, w) for n, m, w in BASE]
run(steps, "  c pole 1.67 au lieu de MS 1.27")
steps = [(n, 4.78 if n == "b" else m, w) for n, m, w in BASE]
run(steps, "  b pole 4.78 au lieu de MS 4.18")
steps = [(n, 163.0 if n == "t" else m, w) for n, m, w in BASE]
run(steps, "  t MSbar 163 au lieu de pole 172.69")

print("\n--- combinaisons honnetes completes ---")
steps = [(n, {"s_const": 0.0935, "u_triade": 0.00214, "d_triade": 0.00470}.get(n, m), w)
         for n, m, w in BASE]
run(steps, "TOUT MSbar (u,d,s physiques, c/b MS, t pole)")
steps = [(n, {"s_const": 0.0935}.get(n, m), w) for n, m, w in BASE]
run(steps, "triade conservee + s MSbar")

print("\n--- reference canonique ---")
print("Valeur canonique SM (fermions seuls, 3 boucles QED+QCD) : ~128.95")
print(f"(ecart a l'exp = {abs(128.95-EXP)/EXP*100:.2f}% — le residu est la")
print("polarisation hadronique, non modelisee a un boucle fermionique)")
