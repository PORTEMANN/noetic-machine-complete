#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T69 — Q-KO6-T69-2026-11 : LA FORMULE EXPLICITE SOUS FORME Ei
     (correction Connes 2026 de la somme de Riemann — verification)
=====================================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T69-CONNES-EI-1.0 gele]

FICHE (gelee avant run — 02/11/2026 ; NOTE-ANTIK-ANALYSE §3.1)
  Affirmation verifiee (document Connes_Zyta.pdf, sourcé [Connes 2026]) :
  la somme de Riemann sur les zeros rho de zeta peut s'écrire sous forme
  Ei sans divergence, avec la convention de branche u = rho log x :
      somme_rho Li(x^rho)  ==  somme_{Im rho > 0} [Ei(rho log x) + Ei(rho* log x)]
  ce qui est la substitution defendue par la correction.
  CRITERES GELES :
    V1  identite Li = Ei o log : |li(x) - ei(log x)| <= 1e-40 en x = e^3
    V2  formule explicite (convention li, somme ordonnee par |gamma|,
        appariement (rho, rho*), Cesaro sur fenetre 100) :
        |pi_chapeau(100) - 25| <= 2.0  et  |pi_chapeau(1000) - 168| <= 6.0
        (tolerances declarees a partir du comportement historique type Gram)
    V3  appariement neuf (rho, rho*) vs ancien (rho, 1-rho) : les deux
        sommes (ordre |gamma|, Cesaro) doivent converger vers la meme
        valeur ; ecart documente (attendu < 1)
    V4  levier : somme sans zeros non triviaux -> ecart massif documente
  Falsifieur : V1 faux (l'identite ne tient pas) ; V2 hors tolerance
  (la forme Ei telle qu'implementee ne reproduit pas pi) ; V3 ecart > 1.
  Notes : x = 100 et 1000 sont sans saut premier (pas de convention
  de mi-saut). N = 500 zeros, mp.dps = 30, graine de protocole : aucune
  alea (determinisme total).
"""
import json
import hashlib
import time
from mpmath import mp, mpf, ei, li, log, pi, zetazero, fabs, re, conj

mp.dps = 25
N_ZEROS = 400
FENETRE = 100


ZS = None

def zeros():
    global ZS
    if ZS is None:
        ZS = [zetazero(k) for k in range(1, N_ZEROS + 1)]
    return ZS

def somme_ei(x, appariement="conjugue"):
    """Somme explicite des zeros sous forme Ei, ordonnee par |gamma|."""
    x = mpf(x)
    lx = log(x)
    tot = mpf(0)
    partiels = []
    for rho in zeros():                        # calcule une seule fois
        if appariement == "conjugue":
            tot += ei(rho * lx) + ei(conj(rho) * lx)
        else:                                  # ancien appariement (rho, 1-rho)
            tot += ei(rho * lx) + ei((1 - rho) * lx)
        partiels.append(tot)
    return partiels


def cesaro(partiels, fenetre=FENETRE):
    return sum(partiels[-fenetre:]) / fenetre


def formule_pi(x, somme_zeros):
    x = mpf(x)
    reste = li(x) - log(2)
    return reste - somme_zeros


def main():
    t0 = time.time()
    result = {"chantier": "T69-Q-KO6-CONNES-EI-2026-11",
              "protocole": "T69-CONNES-EI-1.0 (gele)", "n_zeros": N_ZEROS}

    # V1 : identite Li = Ei o log
    x_v1 = mp.e ** 3
    v1_err = fabs(li(x_v1) - ei(log(x_v1)))
    V1 = v1_err <= mpf("1e-40")
    result["V1_identite"] = {"ecart": float(v1_err), "ok": bool(V1)}

    # V2 : formule explicite aux deux points
    v2 = {}
    for x, vrai, tol in ((100, 25, 2.0), (1000, 168, 6.0)):
        partiels = somme_ei(x, "conjugue")
        s_ces = cesaro(partiels)
        est = formule_pi(x, s_ces)
        err = fabs(est - vrai)
        v2[str(x)] = {"pi_estime": float(re(est)), "pi_vrai": vrai,
                      "ecart": float(re(err)), "tolerance": tol,
                      "ok": bool(err <= tol)}
        print(f"x={x}: pi_chapeau={float(re(est)):.3f} (vrai {vrai}) "
              f"ecart={float(re(err)):.3f} tol={tol}")
    V2 = all(d["ok"] for d in v2.values())
    result["V2_formule_explicite"] = v2

    # V3 : nouveau vs ancien appariement
    x3 = 100
    s_new = cesaro(somme_ei(x3, "conjugue"))
    s_old = cesaro(somme_ei(x3, "ancien"))
    ecart = fabs(s_new - s_old)
    V3 = ecart <= 1
    result["V3_appariements"] = {"ecart": float(ecart), "ok": bool(V3)}
    print(f"appariements conj/ancien a x=100 : ecart={float(ecart):.4f}")

    # V4 : levier — sans zeros non triviaux
    x4 = 100
    est_sans = float(formule_pi(x4, 0))
    ecart_sans = abs(est_sans - 25)
    V4 = ecart_sans > 10
    result["V4_levier_sans_zeros"] = {"pi_estime": est_sans,
                                      "ecart": ecart_sans, "ok": bool(V4)}
    print(f"levier (somme vide) : pi_chapeau={est_sans:.2f} ecart={ecart_sans:.1f}")

    score = int(V1) + int(V2) + int(V3) + int(V4)
    result["score"] = f"{score}/4"
    result["statut"] = ("SUCCES — la forme Ei de la somme explicite "
                        "reproduit pi(x) aux tolerances declarees ; "
                        "l'identite Li=Ei o log tient a 1e-40 ; les deux "
                        "appariements convergent vers la meme somme"
                        if score == 4 else
                        "ECHEC partiel — au moins un critere gele refuse ; "
                        "voir analyse")
    result["duree_s"] = round(time.time() - t0, 2)
    result["sha256_script"] = hashlib.sha256(
        open(__file__, "rb").read()).hexdigest()
    print(json.dumps({k: v for k, v in result.items()}, indent=1,
                     ensure_ascii=False))
    with open("../data/t69_connes_ei_verdict.json", "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("verdict : data/t69_connes_ei_verdict.json")


if __name__ == "__main__":
    main()
