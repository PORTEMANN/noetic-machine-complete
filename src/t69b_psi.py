#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T69b — passe 2 : LA FORMULE EXPLICITE EN psi(x) (von Mangoldt)
================================================================
Operateur de verdict : M(D, S, L, pi) -> V   [T69-PSI-2.0 gele]

FICHE (gelee avant run — 02/11/2026, suite du verdict 1/4 de T69)
  La forme li a ete refusee en passe 1 (structure Pi/pi). La passe 2,
  gelee ici, attaque la forme psi — la mieux conditionnee :
      psi(x) = x - Somme_rho x^rho/rho - log(2 pi) - 1/2 log(1 - x^-2)
  somme sur rho ordonnee par |gamma|, appariement (rho, rho*) :
  paire = 2 Re(x^rho / rho). Cesaro sur fenetre declaree.
  VERITE DE REFERENCE : calculee exactement en seance (crible premiers,
  somme de log p sur puissances premieres) — rien n'est lu de memoire.
  Points de test : x in {100, 500, 1000} — tous sans saut (aucun
  n'est puissance premiere : 100 = 10^2, 500 = 2^2 5^3, 1000 = 10^3,
  10 etant non premier) — continuite, pas de convention de mi-saut.
  CRITERES GELES :
    C1  cache : 800 zeros (gamma monotone, gamma_1 = 14.1347...)
    C2  |psi_chapeau(100)  - psi_exact(100)|  <= 1.0  (Cesaro 200)
    C3  |psi_chapeau(500)  - psi_exact(500)|  <= 1.5
    C4  |psi_chapeau(1000) - psi_exact(1000)| <= 2.5
    C5  levier : somme sans zeros -> ecart > 50
    C6  regression identite : |li(e^3) - ei(3)| <= 1e-38 en dps 40
  Falsifieur : tout ecart hors tolerance — la forme psi telle qu'impl.
  mentee serait declaree non conforme, sans recours.
"""
import json
import re
import hashlib
import time
import os
import numpy as np
import re as regex
from mpmath import mp, mpf, mpc, ei, li, log, zetazero, fabs, conj

DPS = 25
N_ZEROS = 800
FENETRE = 200
ZERO_CACHE = "../data/t69_zeros_cache.json"


def crible(n):
    p = np.ones(n + 1, bool)
    p[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if p[i]:
            p[i * i::i] = False
    return np.where(p)[0]


def psi_exact(x):
    """Somme de log p sur les puissances premieres <= x (exact, local)."""
    x = int(x)
    primes = crible(x)
    total = 0.0
    for p in primes:
        pk = int(p)
        while pk <= x:
            total += float(np.log(int(p)))
            pk *= int(p)
    return total


def zeros():
    """Cache incremental (reprise sure) : paquets de 100, dps 20."""
    mp.dps = 20
    cache = ZERO_CACHE + ".part"
    done = []
    if os.path.exists(cache):
        done = json.load(open(cache))
    while len(done) < N_ZEROS:
        k0 = len(done)
        k1 = min(k0 + 100, N_ZEROS)
        done.extend(str(zetazero(k + 1)) for k in range(k0, k1))
        json.dump(done, open(cache, "w"))
        print(f"  zeros {len(done)}/{N_ZEROS}", flush=True)
    if not os.path.exists(ZERO_CACHE):
        json.dump(done, open(ZERO_CACHE, "w"))
    out = []
    for z in done:
        m = regex.match(r"\(([^+]+)\+(.+)j\)", z.replace(" ", ""))
        out.append(mpc(mpf(m.group(1)), mpf(m.group(2))))
    return out


def psi_chapeau(x, zs):
    x = mpf(x)
    tot = mpf(0)
    partiels = []
    for rho in zs:
        tot += 2 * ((x ** rho) / rho).real
        partiels.append(tot)
    s = sum(partiels[-FENETRE:]) / FENETRE
    return x - s - log(2 * mp.pi) - mpf("0.5") * log(1 - 1 / x ** 2)


def main():
    t0 = time.time()
    result = {"chantier": "T69b-Q-KO6-PSI-2026-11",
              "protocole": "T69-PSI-2.0 (gele)", "n_zeros": N_ZEROS}
    mp.dps = DPS
    zs = zeros()
    C1 = (len(zs) == N_ZEROS
          and fabs(zs[0].imag - mpf("14.1347251417347")) < mpf("1e-6")
          and all(zs[k].imag < zs[k + 1].imag for k in range(50)))
    result["C1_cache_zeros"] = bool(C1)

    criteres = ((100, 1.0), (500, 1.5), (1000, 2.5))
    v = {}
    score_detail = {}
    for i, (x, tol) in enumerate(criteres, start=2):
        pe = psi_exact(x)
        ph = psi_chapeau(x, zs)
        ecart = fabs(ph - pe)
        ok = bool(ecart.real <= tol)
        score_detail[f"C{i}"] = ok
        v[str(x)] = {"psi_exact": pe, "psi_chapeau": float(ph.real),
                     "ecart": float(ecart.real), "tolerance": tol, "ok": ok}
        print(f"x={x}: psi_exact={pe:.3f} psi_chapeau={float(ph.real):.3f} "
              f"ecart={float(ecart.real):.3f} tol={tol} {'OK' if ok else 'REFUS'}")

    # C5 levier : sans zeros non triviaux
    ph0 = mpf(100) - log(2 * mp.pi) - mpf("0.5") * log(1 - mpf(1) / 10000)
    ecart_sans = fabs(ph0 - psi_exact(100))
    C5 = bool(ecart_sans.real > 50)
    print(f"levier sans zeros : ecart={float(ecart_sans.real):.1f}")

    # C6 regression identite en dps 40
    mp.dps = 40
    v6 = fabs(li(mp.e ** 3) - ei(mpf(3)))
    C6 = bool(v6 <= mpf("1e-38"))
    mp.dps = DPS
    print(f"identite li=ei o log en dps 40 : ecart={float(v6):.2e}")

    score = (int(C1) + int(all(score_detail.values())) + int(C5) + int(C6))
    result["details"] = v
    result["C1"] = bool(C1)
    result["C2_C3_C4"] = score_detail
    result["C5_levier"] = bool(C5)
    result["C6_identite_dps40"] = bool(C6)
    result["score"] = f"{score}/5"
    result["statut"] = ("SUCCES — la forme psi de la somme explicite reproduit "
                        "psi(x) aux tolerances gelees sur trois points ; "
                        "l'identite Li=Ei o log tient a 1e-38 ; le levier "
                        "confirme que les zeros portent la correction"
                        if score == 5 else
                        "ECHEC — au moins un critere gele refuse")
    result["duree_s"] = round(time.time() - t0, 2)
    result["sha256_script"] = hashlib.sha256(
        open(__file__, "rb").read()).hexdigest()
    with open("../data/t69b_psi_verdict.json", "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print(json.dumps({k: result[k] for k in
                      ("C1", "C2_C3_C4", "C5_levier", "C6_identite_dps40",
                       "score", "statut")}, indent=1, ensure_ascii=False))
    print("verdict : data/t69b_psi_verdict.json")


if __name__ == "__main__":
    main()
