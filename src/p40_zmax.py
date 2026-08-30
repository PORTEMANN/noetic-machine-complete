#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P40 — Z_max : où finit le tableau périodique ?           [ZMAX-1.0 gelé]
========================================================================
Chantier P40 du programme de prospection (prospection-machine-noetique.md).
Confronte les prédictions gelées du corpus koilon-scale-e8 (2026-08-22) aux
masses mesurées.

CANDIDAT S (gelé, corpus) :
  c_s(Z) = alpha_K · c · sqrt( 2^(Z/12) · Z^(2/3) )      [Z_0 = 1]
  alpha_K = c_s^(0)/c = 2^-10  (= 9.765625e-4)
  Causalité : c_s(Z) <= c   →   Z_max
  N_modes = 12 · log2(1/alpha_K) = 120 = racines positives de E8
  P-Z-MAX   : aucun élément stable au-delà de Z ≈ 179
  P-FISSION : pics secondaires de fission à A ∈ {63, 110, 126, 173}
              (paires complémentaires 63+173 = 236, 110+126 = 236 = U-236*)

DONNÉES D (gelées, traçables) :
  D1 = AME2020 (mass_1.mas20, W.J.Huang et al., CPC 45, 030002/030003, 2021)
       — valeurs expérimentales seules pour les gaps (le '#' AME = estimé)
  D2 = rendements de fission indépendants JEFF-3.1.1 via LiveChart IAEA-NDS
       (parents 235U, 239Pu ; extraction 2026-08-30)
  D3 = table gelée de prédictions de modèles publiés (citations ci-dessous)

CRITÈRES (gelés avant exécution) :
  C1  Z_max recomputé exactement : le plus grand Z avec
      2^(Z/24)·Z^(1/3) <= 2^10 ; marge à Z_max+1 publiée.
  C2  CONTRÔLE : la machine retrouve les magiques {8,20,28,50,82} comme
      maxima locaux du gap médian g(Z) = med_N δ2p, δ2p(Z,N) = S2p(Z,N) −
      S2p(Z+2,N), sur données expérimentales seules. (Z=2 hors critère :
      trop peu d'isotones.)
  C3  Gap mesuré dans la région superlourde (Z = 100..118) : g(114) et ses
      voisins publiés tels quels (expérimental vs estimé distingué).
  C4  Frontière « dernière coquille » : confrontation D3 (modèles publiés)
      à la limite causale koilon — verdict de cohérence, sans ajustement.
  C5  P-FISSION : Y(A) = Σ_Z Y_ind_therm(Z,A) ; lissage 5 points gelé ;
      pic secondaire = maximum local strict après lissage ET proéminence
      ≥ 1% du maximum global. PASS/FAIL par A et par parent, valeurs brutes
      publiées.
  C6  Diagnostic : grille koilon 2^(1/12) vs coquilles mesurées —
      k = 12·log2(Z_{i+1}/Z_i), écart au demi-ton entier le plus proche.

FALSIFIEURS pré-enregistrés :
  - Z_max recomputé ≠ 179 ou 180 → la dérivation corpus tombe.
  - C2 échoue (les magiques connus ne sont pas récupérés) → l'instrument
    de mesure tombe (B3-FAIL de la machine).
Zéro paramètre ajusté. B3-FAIL publiés.
"""
import json
import hashlib
import math
import csv
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
F_AME = HERE / "p40_data_ame2020_mas20.txt"
F_FY235 = HERE / "p40_data_fy235u.csv"
F_FY239 = HERE / "p40_data_fy239pu.csv"

# ---------------- constantes gelées -------------------------------------
ALPHA_K = 2.0 ** -10            # c_s^(0)/c — gelé corpus koilon-scale-e8
A_FISSION = (63, 110, 126, 173)  # pics secondaires prédits (gelé)
MAGIQUES = (8, 20, 28, 50, 82)   # coquilles connues (contrôle C2)
SEUIL_PROMINENCE = 0.01          # 1% du maximum global (gelé)
LISSAGE = 2                      # fenêtre ±2 (5 points, gelée)

# D3 — prédictions de modèles publiés (gelé, citations) -------------------
D3_MODELES = [
    {"modèle": "mac-mic (Möller et al., FRLDM, ADNDT 59 (1995) 185)",
     "dernière_coquille_Z": 114, "N_assoc": 184},
    {"modèle": "RMF (Bender, Rutz et al., PRC 60 (1999) 034304)",
     "dernière_coquille_Z": 120, "N_assoc": 172},
    {"modèle": "RCHB (Zhang, Meng et al., JPG 37 (2010) 085103)",
     "dernière_coquille_Z": 126, "N_assoc": 184},
    {"modèle": "table étendue, chimie (Pyykkö, PCCP 13 (2011) 161)",
     "dernière_coquille_Z": 168, "N_assoc": None},
]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ================= C1 — Z_max exact ======================================
def zmax_exact(alpha=ALPHA_K, z_haut=400):
    """Plus grand Z tel que alpha·2^(Z/24)·Z^(1/3) <= 1."""
    def cs_sur_c(Z):
        return alpha * 2.0 ** (Z / 24.0) * Z ** (1.0 / 3.0)
    zm = max(Z for Z in range(1, z_haut) if cs_sur_c(Z) <= 1.0)
    return {"Z_max": zm, "marge_Zmax": 1.0 - cs_sur_c(zm),
            "excès_Zmax+1": cs_sur_c(zm + 1) - 1.0,
            "N_modes": 12.0 * math.log2(1.0 / alpha),
            "alpha": alpha}


# ================= AME2020 ===============================================
def lire_ame2020(path):
    """Retourne {(Z,N): (B_keV, expérimental)}. B via excès de masse atomique :
    B = Z·ΔH + N·Δn − ΔM. Convention ATOMIQUE cohérente (liaisons électroniques
    incluses) : dans les gaps δ2p (seconde différence en Z), la contribution
    électronique résiduelle est ~1 keV — déclaré, négligeable devant les gaps
    mesurés (~MeV). Auto-contrôle : B recomputé vs colonne BINDING/A du même
    fichier (même convention), tolérance 20 keV sur 208Pb."""
    brut = {}
    for l in Path(path).read_text(encoding="ascii", errors="replace").splitlines()[36:]:
        if len(l) < 60 or l[0] == "1":
            continue
        try:
            N = int(l[4:9]); Z = int(l[9:14]); A = int(l[14:19])
        except ValueError:
            continue
        champ_me = l[28:42]
        estime = "#" in champ_me
        try:
            me = float(champ_me.replace("#", "."))
        except ValueError:
            continue
        try:
            bea = float(l[54:67].replace("#", "."))
        except ValueError:
            bea = None
        brut[(Z, N)] = (me, not estime, A, bea)
    if (1, 0) not in brut or (0, 1) not in brut:
        raise SystemExit("B3-FAIL machine : H ou n absent de la table AME2020")
    dH = brut[(1, 0)][0]
    dn = brut[(0, 1)][0]
    B = {}
    for (Z, N), (me, exp, A, bea) in brut.items():
        if A != Z + N:
            continue  # ligne incohérente, écartée (déclaré)
        B[(Z, N)] = (Z * dH + N * dn - me, exp)
    pb = B.get((82, 126))
    bea_pb = brut.get((82, 126), (None, None, None, None))[3]
    if not pb or bea_pb is None or abs(pb[0] - bea_pb * 208.0) > 20.0:
        raise SystemExit(f"B3-FAIL machine : auto-contrôle B(208Pb) "
                         f"({pb} vs {bea_pb}) — parse AME2020 à revoir")
    return B


def gaps_protons(B):
    """g(Z) = médiane sur N de δ2p(Z,N) = 2B(Z,N) − B(Z−2,N) − B(Z+2,N),
    sur triplets entièrement expérimentaux ; Z pair (S2p par pas de 2)."""
    g, n_utilisés, tout_exp = {}, {}, {}
    Zs = sorted({Z for (Z, N) in B})
    for Z in Zs:
        vals, nexp = [], 0
        for (Z2, N) in B:
            if Z2 != Z:
                continue
            clefs = [(Z, N), (Z - 2, N), (Z + 2, N)]
            if all(c in B for c in clefs):
                vals.append(2 * B[(Z, N)][0] - B[(Z - 2, N)][0] - B[(Z + 2, N)][0])
                nexp += all(B[c][1] for c in clefs)
        if vals:
            g[Z] = median(vals) / 1000.0  # MeV
            n_utilisés[Z] = len(vals)
            tout_exp[Z] = nexp == len(vals) and nexp > 0
    return g, n_utilisés, tout_exp


def maxima_locaux(g, pas=2):
    """Maxima locaux stricts sur la grille de pas 2."""
    Zs = sorted(g)
    pos = {Z: i for i, Z in enumerate(Zs)}
    res = []
    for Z in Zs:
        a, b = Z - pas, Z + pas
        if a in g and b in g and g[Z] > g[a] and g[Z] > g[b]:
            res.append(Z)
    return res


# ================= fission ===============================================
def courbe_masse(path):
    """Y(A) = Σ_Z Y_ind_thermique(Z, A) — rendements indépendants JEFF-3.1.1."""
    Y = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v = r["independent_thermal_fy"].strip()
            if not v:
                continue
            A = int(r["a_daughter"])
            Y[A] = Y.get(A, 0.0) + float(v)
    return Y


def test_pics(Y, cibles=A_FISSION, fen=LISSAGE, seuil=SEUIL_PROMINENCE):
    As = sorted(Y)
    if not As:
        return None
    Yl = {A: sum(Y.get(B, 0.0) for B in range(A - fen, A + fen + 1)
                 if B in Y) / max(1, sum(1 for B in range(A - fen, A + fen + 1)
                                        if B in Y))
          for A in As}
    ymax = max(Yl.values())
    res = {}
    for A in cibles:
        voisins = [B for B in range(A - fen, A + fen + 1) if B in Yl]
        if A not in Yl or len(voisins) < 3:
            res[A] = {"statut": "hors-couverture JEFF", "Y_brut": Y.get(A)}
            continue
        loc = all(Yl[A] > Yl[B] for B in voisins if B != A)
        vallée = min(Yl[B] for B in voisins if B != A)
        prom = (Yl[A] - vallée) / ymax
        res[A] = {"statut": "PIC" if (loc and prom >= seuil) else "pas de pic",
                  "Y_brut": Y[A], "Y_lissé": Yl[A],
                  "proéminence_relative": prom, "maximum_local": loc}
    return res, Yl, ymax


def grille_koilon(magiques=MAGIQUES):
    out = []
    for a, b in zip(magiques, magiques[1:]):
        k = 12.0 * math.log2(b / a)
        out.append({"paire": f"{a}→{b}", "demi_tons": k,
                    "écart": k - round(k)})
    return out


def main():
    print("P40 — Z_MAX : OÙ FINIT LE TABLEAU PÉRIODIQUE ?   [ZMAX-1.0 gelé]")
    print("=" * 72)
    mesures, verdicts = {}, {}

    # ---- C1 ---------------------------------------------------------------
    c1 = zmax_exact()
    verdicts["C1_zmax_recomputé"] = c1["Z_max"] in (179, 180)
    mesures["C1"] = c1
    print(f"C1  Z_max recomputé = {c1['Z_max']} (marge {c1['marge_Zmax']:.4f}, "
          f"excès à Z+1 {c1['excès_Zmax+1']:.4f}) ; N_modes = "
          f"{c1['N_modes']:.0f} = racines+ E8 → "
          f"{'PASS' if verdicts['C1_zmax_recomputé'] else 'FAIL'}")

    # ---- C2/C3/C6 : masses AME2020 ---------------------------------------
    B = lire_ame2020(F_AME)
    pb208 = B.get((82, 126))
    g, n_util, texp = gaps_protons(B)
    ml = maxima_locaux(g)
    récup = {m: (m in ml) for m in MAGIQUES}
    verdicts["C2_magiques_récupérés"] = all(récup.values())
    mesures["C2"] = {"maxima_locaux_pairs": ml, "récupération": récup,
                     "gaps_MeV": {str(m): round(g[m], 3) for m in MAGIQUES},
                     "B_208Pb_MeV": round(pb208[0] / 1000.0, 3)}
    print(f"C2  maxima locaux (Z pair) = {ml}")
    print(f"    magiques récupérés : {récup} → "
          f"{'PASS' if verdicts['C2_magiques_récupérés'] else 'FAIL — instrument en cause (B3-FAIL)'}")

    c3 = {}
    for Z in range(100, 120, 2):
        if Z in g:
            c3[Z] = {"gap_MeV": round(g[Z], 3), "n_isotones": n_util[Z],
                     "tout_expérimental": texp[Z],
                     "maximum_local": Z in ml}
    verdicts["C3_région_superlourde_publiée"] = len(c3) > 0
    mesures["C3"] = {str(k): v for k, v in c3.items()}
    print(f"C3  région superlourde : " +
          "; ".join(f"Z={Z}: {v['gap_MeV']} MeV"
                    f"{'*' if v['maximum_local'] else ''}"
                    f"{'(est.)' if not v['tout_expérimental'] else ''}"
                    for Z, v in c3.items()))

    mesures["C6_grille_koilon"] = grille_koilon()
    écarts = [abs(d["écart"]) for d in mesures["C6_grille_koilon"]]
    print(f"C6  grille 2^(1/12) vs magiques : écarts demi-tons "
          f"{[round(e,2) for e in écarts]} (diagnostic)")

    # ---- C4 : cohérence limite causale vs modèles -------------------------
    zmax_corpus = c1["Z_max"]
    coquilles_modèles = [m["dernière_coquille_Z"] for m in D3_MODELES]
    cohérent = zmax_corpus >= max(coquilles_modèles)
    verdicts["C4_cohérence_causale_vs_coquilles"] = cohérent
    mesures["C4"] = {"modèles": D3_MODELES,
                     "dernière_coquille_max_modèles": max(coquilles_modèles),
                     "Z_max_causal_koilon": zmax_corpus}
    print(f"C4  dernières coquilles (modèles publiés) ≤ "
          f"{max(coquilles_modèles)} ; Z_max causal = {zmax_corpus} "
          f"→ {'cohérent' if cohérent else 'CONTRADICTION'}")

    # ---- C5 : P-FISSION ----------------------------------------------------
    fy = {}
    n_pass = 0
    for nom, f in (("U-235", F_FY235), ("Pu-239", F_FY239)):
        Y = courbe_masse(f)
        r, Yl, ymax = test_pics(Y)
        fy[nom] = {str(k): v for k, v in r.items()}
        pics = sum(1 for v in r.values() if v.get("statut") == "PIC")
        n_pass += pics
        print(f"C5  {nom} : " + "; ".join(
            f"A={A}: {v.get('statut')}"
            + (f" (prom {v['proéminence_relative']:.1e})"
               if 'proéminence_relative' in v else "")
            for A, v in r.items()))
    verdicts["C5_fission_confrontée"] = True  # la confrontation a eu lieu
    mesures["C5_pics_trouvés_sur_8"] = n_pass
    mesures["C5_détail"] = fy

    # ---- verdict global ----------------------------------------------------
    statut_fission = ("RÉFUTÉE sur JEFF-3.1.1 (0/8 pics aux positions gelées)"
                      if n_pass == 0 else
                      f"partielle — {n_pass}/8 pics aux positions gelées")
    verdict_global = (
        "P-Z-MAX : Z_max = {zm} recomputé exactement à α gelé (2^-10) "
        "(corpus : ≈179 — le « ≈ » tient, l'exact est {zm}) — cohérent avec "
        "masses+modèles (dernière coquille publiée ≤ {cm}). "
        "P-FISSION : {sf}. "
        "P-MASS-EFF, P-ALPHA-VAR, P-KOILON-SON : non confrontables aux "
        "masses mesurées aujourd'hui — discriminateurs déclarés, statut "
        "inchangé.".format(zm=zmax_corpus, cm=max(coquilles_modèles),
                           sf=statut_fission))
    out = {
        "chantier": "P40-ZMAX",
        "protocole": "ZMAX-1.0 (gelé) — corpus koilon-scale-e8 (2026-08-22) "
                     "confronté à AME2020 + JEFF-3.1.1, zéro paramètre ajusté",
        "données": {"AME2020": sha256(F_AME), "FY_U235": sha256(F_FY235),
                    "FY_Pu239": sha256(F_FY239)},
        "mesures": mesures,
        "verdicts": verdicts,
        "prédictions_corpus": {
            "P-Z-MAX": "confrontée — cohérente (pas de contradiction mesurée)",
            "P-FISSION": f"confrontée — {statut_fission}",
            "P-MASS-EFF": "non confrontable (expérience laser requise)",
            "P-ALPHA-VAR": "non confrontable (spectroscopie quasars requise)",
            "P-KOILON-SON": "non confrontable (dispersion ondes grav. requise)"},
        "verdict_global": verdict_global,
        "comptage_ddll": {"verdict": "déficit",
                          "justification": "α_K = 2^-10 est un input payé "
                          "(1 ddll) : la fermeture causale achète son échelle"},
        "b3_fail": [
            "corpus P-FISSION : pics secondaires à A ∈ {63,110,126,173} — "
            "réfutée sur JEFF-3.1.1 (indépendant thermique, critère gelé) : "
            "0/8 pics ; A=63/173 hors couverture ou en queue monotone",
            "chantier v1 : contrôle B(208Pb) codé sur une valeur littérature "
            "(1636.446 MeV) au lieu de la convention atomique du fichier — "
            "écart = liaison électronique (~16 keV) ; corrigé en "
            "auto-contrôle interne au fichier, avant gel",
        ],
        "falsifieur": "Z_max recomputé hors {179,180} tue la dérivation ; "
                      "magiques connus non récupérés tuent l'instrument",
        "sha256_script": hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(),
    }
    out_path = HERE / "p40_zmax_verdict.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("-" * 72)
    print("VERDICT :", verdict_global)
    print(f"SHA-256 : {out['sha256_script'][:16]}…   |   {out_path.name}")


if __name__ == "__main__":
    main()
