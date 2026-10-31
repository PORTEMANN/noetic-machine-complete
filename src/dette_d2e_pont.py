# -*- coding: utf-8 -*-
"""D2e — pont hadronique direct : modele a seuils vs donnees e+e-.

Parse les tables de data/hadr5x26.f (F. Jegerlehner, HU-Berlin,
juin 2026) : ESA/DAS = Delta_alpha_had^(5)(e^2) interpole de 2180
points R(s) (0.282 - 38.29 GeV) ; EMA/DAM = continuation pQCD
(13 GeV - 20 TeV). Interpoler DAM a M_Z donne la valeur data-driven
de Delta_alpha_had, comparee au secteur habille du modele
(NOTE-DETTE-D1 §7-8 : seuils constituants u/d/s = 0.02775).

Reference croisee : PDG Delta alpha_had^(5)(M_Z^2) = 0.02757 +- 0.011.
"""
import os
import re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "data", "hadr5x26.f"),
           encoding="ascii", errors="replace").read()


def parse_block(name, idx_dim):
    """DATA Fortran decoupes en tranches de 100, ordonnees (J, I)."""
    pat = re.compile(
        r"DATA\s*\(\(?\s*" + name + r"\s*\(\s*" + idx_dim +
        r"\s*\)[^/]*?/\s*(.*?)\s*/", re.S | re.I)
    chunks = []
    for m in pat.finditer(SRC):
        rng = re.search(r"I=\s*(\d+)\s*,\s*(\d+)", m.group(0))
        a = int(rng.group(1)) if rng else 0
        rj = re.search(r"J=\s*(\d+)\s*,\s*(\d+)", m.group(0))
        j = int(rj.group(1)) if rj else 1
        vals = [float(x.replace("D", "E").replace("d", "e")) for x in
                re.findall(r"[+-]?\d+\.?\d*(?:[DdEe][+-]?\d+)?", m.group(1))]
        chunks.append((j, a, vals))
    chunks.sort(key=lambda c: (c[0], c[1]))
    out = []
    for _, _, v in chunks:
        out.extend(v)
    return np.array(out)


EMA = parse_block("EMA", "I")
DAM = parse_block("DAM", "I,J")
MZ = 91.1876
MODELE = 0.02775

dalpha_data = float(np.interp(np.log(MZ), np.log(EMA), DAM[:len(EMA)]))

if __name__ == "__main__":
    print(f"Delta_alpha_had^(5)(M_Z^2) [donnees e+e-, compilation 06/2026]")
    print(f"  interpolation a M_Z      : {dalpha_data:.5f}")
    print(f"  reference PDG            : 0.02757 +- 0.011")
    print(f"  modele (seuils habilles) : {MODELE:.5f}")
    print(f"  accord direct modele/donnees : "
          f"{abs(dalpha_data - MODELE) / dalpha_data * 100:.2f} %")
