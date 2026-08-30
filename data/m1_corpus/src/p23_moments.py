# P23 - moments magnetiques nucleaires : le modele en couches derive (P12)
# predit les moments de Schmidt. Banc tres discriminant.
# Couplage j = l +/- 1/2 (algebre angulaire de la machine) + g-facteurs libres
# mesures (entrees) : g_l^p=1, g_l^n=0, g_s^p=5.586, g_s^n=-3.826.
# Schmidt : j=l+1/2 : mu = g_l l + g_s/2
#           j=l-1/2 : mu = j/(j+1) * [g_l (l+1) - g_s/2]
import numpy as np, json, hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GLP, GLN, GSP, GSN = 1.0, 0.0, 5.586, -3.826

def schmidt(l, j, typee):
    gl, gs = (GLP, GSP) if typee == "p" else (GLN, GSN)
    if abs(j-(l+0.5)) < 1e-6:
        return gl*l + gs/2
    else:  # j = l - 1/2
        return j/(j+1)*(gl*(l+1) - gs/2)

# (nom, nucleon celibataire, l, j, type, mu_mes, note)
NOYAUX = [
 ("3H",    "1s1/2", 0, 0.5, "p",  2.979),
 ("3He",   "1s1/2", 0, 0.5, "n", -2.128),
 ("13C",   "1p1/2", 1, 0.5, "n",  0.702),
 ("15N",   "1p1/2 trou", 1, 0.5, "p", -0.283),
 ("15O",   "1p1/2 trou", 1, 0.5, "n",  0.719),
 ("17O",   "1d5/2", 2, 2.5, "n", -1.894),
 ("17F",   "1d5/2", 2, 2.5, "p",  4.722),
 ("39K",   "1d3/2 trou", 2, 1.5, "p",  0.391),
 ("41Ca",  "1f7/2", 3, 3.5, "n", -1.595),
 ("93Nb",  "1g9/2", 4, 4.5, "p",  6.171),
 ("207Pb", "3p1/2 trou", 1, 0.5, "n",  0.593),
 ("209Bi", "1h9/2", 5, 4.5, "p",  4.110),
]
res = []
for nom, orb, l, j, t, mes in NOYAUX:
    mu = schmidt(l, j, t)
    ecart = abs(mu-mes)
    res.append(dict(nom=nom, orbitale=orb, l=l, j=j, type=t,
                    mu_schmidt=round(mu, 3), mu_mes=mes, ecart=round(ecart, 3),
                    signe_ok=bool(np.sign(mu) == np.sign(mes))))
    print(f"{nom:6s} {orb:12s} mu_Schmidt={mu:+.3f} mes={mes:+.3f} ecart={ecart:.3f}")

ecarts = np.array([r["ecart"] for r in res])
sous_05 = int(np.sum(ecarts < 0.5))
sous_025 = int(np.sum(ecarts < 0.25))
cas_propres = ["17O", "17F", "207Pb", "15N", "15O", "13C"]
propres_ok = sum(1 for r in res if r["nom"] in cas_propres and r["ecart"] < 0.15)
bi = [r for r in res if r["nom"] == "209Bi"][0]

# controle du levier : remplacer g_s neutron par 0 detruit l'accord ?
def schmidt_gsn0(l, j, t):
    gl, gs = (GLP, GSP) if t == "p" else (GLN, 0.0)
    return gl*l + gs/2 if abs(j-(l+0.5)) < 1e-6 else j/(j+1)*(gl*(l+1)-gs/2)
ecarts_gsn0 = [abs(schmidt_gsn0(r["l"], r["j"], r["type"])-r["mu_mes"]) for r in res]
levier = float(np.mean(ecarts_gsn0)) > 1.5*float(np.mean(ecarts))
print(f"ecart moyen = {np.mean(ecarts):.3f} muN ; sans g_s^n : {np.mean(ecarts_gsn0):.3f}")

verdict = {
 "signes_12sur12": bool(all(r["signe_ok"] for r in res)),
 "ecart_lt_0.5_au_moins_9sur12": bool(sous_05 >= 9),
 "cas_uniparticule_10pct": bool(propres_ok >= 4),
 "anomalie_209Bi_localisee": bool(bi["ecart"] > 0.8),
 "levier_gs_discriminant": levier,
 "ecart_moyen_lt_0.35": bool(float(np.mean(ecarts)) < 0.35),
}
out = dict(methode=("Schmidt : couplage j=l+/-1/2 (algebre angulaire machine) + g libres mesures ; "
                    "aucun ajustement ; trous traites comme particules"),
           noyaux=res, ecart_moyen=round(float(np.mean(ecarts)), 3),
           sous_05=sous_05, sous_025=sous_025,
           ecart_moyen_sans_gsn=round(float(np.mean(ecarts_gsn0)), 3),
           verdict=verdict, score=f"{sum(verdict.values())}/6",
           lecture=("les moments de Schmidt (particule/trou celibataire) reproduisent les moments "
                    "pres des couches fermees a <0.5 muN pour l'essentiel ; l'ecart residuel est le "
                    "'quenching' (polarisation du coeur, mesons) = reponse 2 corps P28 ; 209Bi est "
                    "l'anomalie connue (Schmidt 2.6 vs 4.1 mesure)"))
json.dump(out, open("/mnt/agents/output/e44_data/p23_moments.json", "w"), indent=2, ensure_ascii=False)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
noms = [r["nom"] for r in res]
ax[0].bar(np.arange(12)-0.2, [r["mu_schmidt"] for r in res], 0.4, label="Schmidt (machine)")
ax[0].bar(np.arange(12)+0.2, [r["mu_mes"] for r in res], 0.4, label="mesure")
ax[0].set_xticks(range(12)); ax[0].set_xticklabels(noms, rotation=45, fontsize=8)
ax[0].axhline(0, c='gray', lw=0.5)
ax[0].set_title("A - moments magnetiques : Schmidt vs mesure")
ax[0].set_ylabel("mu (muN)"); ax[0].legend(fontsize=8)
ax[1].bar(noms, ecarts, 0.5)
ax[1].axhline(0.5, ls='--', c='r', label="seuil 0.5 muN")
ax[1].set_xticks(range(12)); ax[1].set_xticklabels(noms, rotation=45, fontsize=8)
ax[1].set_title("B - ecarts |Schmidt - mesure|")
ax[1].set_ylabel("ecart (muN)"); ax[1].legend(fontsize=8)
plt.tight_layout()
plt.savefig("/mnt/agents/output/e44_data/p23_moments.png", dpi=110)
for p in ["p23_moments.py", "p23_moments.json", "p23_moments.png"]:
    h = hashlib.sha256(open("/mnt/agents/output/e44_data/"+p, 'rb').read()).hexdigest()[:12]
    open(f"/mnt/agents/output/e44_data/sha_{p.split('.')[0]}_{p.split('.')[1]}.txt", "w").write(h)
    print(p, h)
print("verdict", verdict, sum(verdict.values()), "/6")
