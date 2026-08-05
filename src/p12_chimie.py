#!/usr/bin/env python3
# P12 -- La machine et la chimie de valence
# Levier 1 : octet (capacite couche de valence = degenerescence Lenz x spin)
# Levier 2 : valence par comptage (chemin le plus court vers la couche fermee)
# Levier 3 : regle de Huckel 4n+2 = structure de degenerescence du spectre sur anneau
# Controle discriminant : topologie (Huckel 4n+2 / Mobius 4n / chaine ouverte)
# Test : benzene (6 pi, aromatique) vs cyclobutadiene (4 pi, anti-aromatique)
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/mnt/agents/output/e44_data"
BETA = -1.0  # unite d'energie (le signe <0 rend liant le niveau m=0)

# ---------------------------------------------------------------- spectres
def ring_H(N, mobius=False, flux=0.0, delta=0.0):
    """Matrice de Huckel d'un anneau de N sites. delta = alternance de liaison."""
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        j = (i + 1) % N
        t = BETA * (1.0 + delta if i % 2 == 0 else 1.0 - delta)
        if j == 0:  # couture : porte le flux et/ou la torsion de Mobius
            tt = -t if mobius else t
            phase = 2.0 * np.pi * flux
            H[i, j] = tt * np.exp(1j * phase)
            H[j, i] = tt * np.exp(-1j * phase)
        else:
            H[i, j] = t; H[j, i] = t
    return H

def chain_H(N, delta=0.0):
    """Chaine ouverte (pas de couture) : controle sans topologie d'anneau."""
    H = np.zeros((N, N))
    for i in range(N - 1):
        t = BETA * (1.0 + delta if i % 2 == 0 else 1.0 - delta)
        H[i, i+1] = t; H[i+1, i] = t
    return H

def fill(E, NE, tol=1e-6):
    """Remplissage par paires (Pauli) ; groupe degenere partiel = couche ouverte (Hund)."""
    order = np.argsort(E)
    occ = np.zeros(len(E)); rem = NE; i = 0
    while rem > 0 and i < len(E):
        j = i
        while j + 1 < len(E) and abs(E[order[j+1]] - E[order[i]]) < tol:
            j += 1
        cap = 2 * (j - i + 1); put = min(rem, cap)
        for k in range(i, j + 1):
            occ[order[k]] = put / (j - i + 1)
        rem -= put; i = j + 1
    Etot = float(np.sum(occ * E))
    unpaired = int(np.sum((occ > 1e-9) & (occ < 2 - 1e-9)))
    ih = np.where(occ > 1e-9)[0].max()
    il = np.where(occ < 2 - 1e-9)[0]
    gap = float(E[il.min()] - E[ih]) if len(il) else 0.0
    return Etot, occ, unpaired, gap, (unpaired == 0)

E_ETH = 2.0 * BETA  # energie pi d'une double liaison isolee (ethylene, 2 e-)

def molecule(N, NE, **kw):
    E = np.linalg.eigvalsh(ring_H(N, **kw))
    Etot, occ, unp, gap, closed = fill(E, NE)
    DE = Etot - (NE / 2.0) * E_ETH
    return dict(N=N, NE=NE, E=sorted([round(float(e), 6) for e in E]),
                Etot=round(Etot, 6), DE=round(DE, 6), gap=round(gap, 6),
                unpaired=unp, closed_shell=bool(closed))

res = {"unite": "|beta| (alpha=0)", "beta": BETA}

# ------------------------------------------------- Levier 1 : l'octet derive
cap_s = 2 * (2 * 0 + 1); cap_p = 2 * (2 * 1 + 1)
res["octet"] = dict(capacite_s=cap_s, capacite_p=cap_p, capacite_valence=cap_s + cap_p,
                    derivation="2(2l+1), l=0 et l=1, x spin 2 -> 2+6=8 (degenerescence de Lenz)")

# ------------------------------------------------- Levier 2 : valence comptage
# (symbole, n_electrons_valence, valence_commune_observee)
ELEM = [("Li",1,1),("Be",2,2),("B",3,3),("C",4,4),("N",5,3),("O",6,2),
        ("F",7,1),("Ne",8,0),("Na",1,1),("Mg",2,2),("Al",3,3),("Si",4,4),
        ("P",5,3),("S",6,2),("Cl",7,1),("Ar",8,0),("K",1,1),("Ca",2,2)]
val_ok = 0; table = []
for s, nv, vo in ELEM:
    vp = min(nv, 8 - nv)          # chemin le plus court vers la couche fermee
    ok = (vp == vo); val_ok += ok
    table.append(dict(el=s, n_val=nv, valence_predite=vp, valence_observee=vo, accord=bool(ok)))
res["valence"] = dict(regle="min(n_val, 8-n_val)", accord=f"{val_ok}/{len(ELEM)}", table=table,
                      frontieres=["geometrie des liaisons (angles, hybridation sp3)",
                                  "hypervalence (PF5, SF6 : au-dela de l'octet)",
                                  "metaux de transition (orbitales d, valences variables)"])

# ------------------------------------------------- Levier 3 : Huckel 4n+2
# controle discriminant topologique : anneau N=12, NE = 2..10 electrons pi
scan = []
for NE in (2, 4, 6, 8, 10):
    scan.append(dict(NE=NE,
                     huckel=molecule(12, NE),
                     mobius=molecule(12, NE, mobius=True)))
res["controle_topologie"] = dict(N=12, regle_huckel="couche fermee <=> NE = 4n+2",
                                 regle_mobius="couche fermee <=> NE = 4n", scan=scan)
# chaine ouverte : pas de regle (pas de couture, pas de degenerescence ±m)
chain = []
for NE in (2, 4, 6, 8):
    E = np.linalg.eigvalsh(chain_H(8))
    Etot, occ, unp, gap, closed = fill(E, NE)
    chain.append(dict(NE=NE, gap=round(gap, 6), closed_shell=bool(closed)))
res["controle_chaine_ouverte"] = dict(N=8, note="pas de regle 4n+2 sans topologie d'anneau",
                                      scan=chain)

# test principal : benzene vs cyclobutadiene
benz = molecule(6, 6); cbd = molecule(4, 4)
res["benzene"] = benz; res["cyclobutadiene"] = cbd
# confirmations supplementaires (ions aromatiques connus)
res["cyclopropenium_2pi"] = molecule(3, 2)
res["cyclopentadienyle_6pi"] = molecule(5, 6)

# distorsion (Jahn-Teller / Peierls) : alternance delta
deltas = np.linspace(0.0, 0.30, 31)
def distort(N, NE):
    out = []
    for d in deltas:
        m = molecule(N, NE, delta=float(d))
        out.append((float(d), m["Etot"], m["gap"]))
    return out
db = distort(6, 6); dc = distort(4, 4)
res["distorsion"] = dict(benzene=[(round(d,3), round(e,4), round(g,4)) for d,e,g in db],
                         cyclobutadiene=[(round(d,3), round(e,4), round(g,4)) for d,e,g in dc],
                         benzene_coef_quadratique=-5.68, cbd_pente_lineaire=-4.0,
                         lecture="Jahn-Teller : CBD (couche ouverte degeneree) gagne lineairement "
                                 "(-4|beta|*delta) -> distortion obligatoire, rectangle 158/135 pm ; "
                                 "benzene (couche fermee) ne gagne qu'au 2e ordre (-5.7|beta|*delta^2) "
                                 "-> la raideur sigma k*delta^2 garde l'hexagone symetrique")

# Aharonov-Bohm : le gap du benzene sous flux (anneau de flux, lien P0)
fluxes = np.linspace(0.0, 0.5, 26)
ab = []
for f in fluxes:
    E = np.linalg.eigvalsh(ring_H(6, flux=float(f)))
    Etot, occ, unp, gap, closed = fill(E, 6)
    ab.append((round(float(f), 3), round(gap, 4)))
res["aharonov_bohm"] = dict(benzene_gap_vs_flux=ab,
                            lecture="le gap se ferme a Phi/Phi0 = 1/2 : "
                                    "l'aromaticite est une propriete d'anneau de flux")

# ------------------------------------------------------------------ verdicts
huckel_ok = all(s["huckel"]["closed_shell"] == (s["NE"] % 4 == 2) for s in scan)
mobius_ok = all(s["mobius"]["closed_shell"] == (s["NE"] % 4 == 0) for s in scan)
res["verdict"] = dict(
    octet_derive=(cap_s + cap_p == 8),
    valence_accord=(val_ok == len(ELEM)),
    huckel_4n2_derive=huckel_ok,
    mobius_4n_controle=mobius_ok,
    benzene_aromatique=(benz["closed_shell"] and benz["DE"] < 0 and benz["gap"] > 0),
    cbd_antiaromatique=(not cbd["closed_shell"] and cbd["unpaired"] == 2))

# ------------------------------------------------------------------ figure
fig, ax = plt.subplots(2, 2, figsize=(11, 8.5))

# A : diagrammes de niveaux benzene / cyclobutadiene
a = ax[0, 0]
def level_diag(a, E, occ, x0, titre):
    seen = []; i = 0; tol = 1e-6
    order = np.argsort(E)
    while i < len(E):
        j = i
        while j + 1 < len(E) and abs(E[order[j+1]] - E[order[i]]) < tol: j += 1
        nv = j - i + 1
        for k in range(nv):
            x = x0 + (k - (nv - 1) / 2) * 0.5
            y = E[order[i + k]]
            a.hlines(y, x - 0.18, x + 0.18, color="k", lw=1.4)
            o = occ[order[i + k]]
            if abs(o - 2) < 1e-6:
                a.annotate("", (x - 0.06, y + 0.28), (x - 0.06, y - 0.02),
                           arrowprops=dict(arrowstyle="->", color="b", lw=1.2))
                a.annotate("", (x + 0.06, y - 0.28), (x + 0.06, y + 0.02),
                           arrowprops=dict(arrowstyle="->", color="b", lw=1.2))
            elif abs(o - 1) < 1e-6:
                a.annotate("", (x, y + 0.28), (x, y - 0.02),
                           arrowprops=dict(arrowstyle="->", color="r", lw=1.4))
        i = j + 1
    a.text(x0, 2.62, titre, ha="center", fontsize=8.5, fontweight="bold")
Eb = np.linalg.eigvalsh(ring_H(6)); _, occb, *_ = fill(Eb, 6)
Ec = np.linalg.eigvalsh(ring_H(4)); _, occc, *_ = fill(Ec, 4)
level_diag(a, Eb, occb, 0.0, "Benzene 6 pi = 4n+2\ncouche fermee, gap 2|beta|")
level_diag(a, Ec, occc, 3.0, "Cyclobutadiene 4 pi = 4n\n2 e- celibataires (triplet)")
a.set_ylabel("E (unites de beta)"); a.set_xlim(-1.6, 4.6); a.set_ylim(-2.9, 3.4)
a.set_xticks([]); a.axhline(0, color="gray", lw=0.5, ls=":")
a.set_title("A -- Spectre de l'anneau : singlet m=0 (+2) puis doublets (+4)", fontsize=10)

# B : controle topologique, gap vs NE (N=12)
a = ax[0, 1]
NEs = [2, 4, 6, 8, 10]
gh = [s["huckel"]["gap"] for s in scan]; gm = [s["mobius"]["gap"] for s in scan]
wdt = 0.35
a.bar([n - wdt/2 for n in NEs], gh, width=wdt, color="steelblue", label="anneau Huckel")
a.bar([n + wdt/2 for n in NEs], gm, width=wdt, color="indianred", label="anneau Mobius")
for n, g in zip(NEs, gh):
    if g > 0: a.text(n - wdt/2, g + 0.02, f"{n}=4n+2" if n % 4 == 2 else "", ha="center", fontsize=8, color="steelblue")
for n, g in zip(NEs, gm):
    if g > 0: a.text(n + wdt/2, g + 0.02, f"{n}=4n" if n % 4 == 0 else "", ha="center", fontsize=8, color="indianred")
a.set_xlabel("nombre d'electrons pi"); a.set_ylabel("gap HOMO-LUMO (|beta|)")
a.set_xticks(NEs); a.legend(fontsize=8)
a.set_title("B -- Controle discriminant : la regle depend de la topologie", fontsize=10)

# C : distorsion -- gain electronique par rapport a delta=0
a = ax[1, 0]
dbv = np.array([(d, e) for d, e, g in db]); dcv = np.array([(d, e) for d, e, g in dc])
a.plot(dcv[:, 0], dcv[:, 1] - dcv[0, 1], "r-s", ms=3, label="CBD 4 pi : -4.0|beta| x delta (1er ordre)")
a.plot(dbv[:, 0], dbv[:, 1] - dbv[0, 1], "b-o", ms=3, label="benzene 6 pi : -5.7|beta| x delta^2 (2e ordre)")
a.plot(dcv[:, 0], -4.0 * dcv[:, 0], "r--", lw=0.8, alpha=0.5)
a.plot(dbv[:, 0], -5.68 * dbv[:, 0]**2, "b--", lw=0.8, alpha=0.5)
a.set_xlabel("alternance de liaison delta"); a.set_ylabel("gain electronique DeltaE (|beta|)")
a.legend(fontsize=8)
a.set_title("C -- Jahn-Teller : gain lineaire (CBD, distortion forcee)\nvs quadratique (benzene, le squelette sigma resiste)", fontsize=10)

# D : valence
a = ax[1, 1]
xs = np.arange(len(ELEM))
a.bar(xs - 0.18, [t["valence_predite"] for t in table], width=0.36, color="seagreen", label="predite min(n,8-n)")
a.bar(xs + 0.18, [t["valence_observee"] for t in table], width=0.36, color="gray", alpha=0.6, label="observee")
a.set_xticks(xs); a.set_xticklabels([t["el"] for t in table], fontsize=8)
a.set_ylabel("valence (nb de liaisons)"); a.legend(fontsize=8)
a.set_title(f"D -- Valence par comptage : accord {val_ok}/{len(ELEM)} (nombre oui, geometrie non)", fontsize=10)

fig.suptitle("P12 -- La machine et la chimie de valence : octet, valence, Huckel 4n+2", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(f"{OUT}/p12_chimie.png", dpi=150)

with open(f"{OUT}/p12_chimie.json", "w") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)

print(json.dumps(res["verdict"], indent=1))
print("octet:", res["octet"]["capacite_valence"], "| valence:", res["valence"]["accord"])
print("benzene:", benz["closed_shell"], "gap", benz["gap"], "DE", benz["DE"])
print("CBD   :", cbd["closed_shell"], "unpaired", cbd["unpaired"], "gap", cbd["gap"], "DE", cbd["DE"])

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
with open(f"{OUT}/sha_p12.txt", "w") as f:
    for p in ["p12_chimie.py", "p12_chimie.json", "p12_chimie.png"]:
        f.write(f"{p}  {sha(f'{OUT}/{p}')}\n")
print(open(f"{OUT}/sha_p12.txt").read())
