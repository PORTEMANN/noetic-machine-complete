#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-DYN-2 P1 — PILIER A : re-verification du generateur (fiche SCELLEE v1.0)
==========================================================================
Conventions CANONIQUES reprises de src/t24_ko6_cantor.py (T24) :
  A(t) = [[t,-1],[1,0]] ; B(t) = [[t-1,-1],[1,0]] ; mot de Fibonacci ;
  trace map x_{N+1} = 2 x_N x_{N-1} - x_{N-2} ;
  invariant de Fricke I = x2+y2+z2 - 2xyz (forme T24 verifiee a 2e-16) ;
  grille 2^18 sur [-2.5, 2.5] (T24).

Objets gelés (fiche v1.0, section 3) :
  S1 : 8 arêtes de bandes (extraction niveau 14 sur grille T24)
  S2 : 8 milieux de gaps (même source)
  S3 : 64 seeds, pas ΔE = (Emax-Emin)/64, Emin/Emax = [-2.5, 2.5] (intervalle
       de la grille gelée T24 — déclaré ici comme lecture canonique de
       « l'intervalle spectral » de la fiche)
  L = 1e4 itérations par orbite.
Tolérances gelées : O1 portée si écart ≤ 1e-12, non portée si > 1e-9
  (entre les deux = zone grise, comptée séparément) ;
  O2 : |c_{N+1}/c_N - φ| ≤ 0.02 sur les 3 derniers ratios (niveaux 12,13,14,
  fenêtre canonique T24) ET recursion des comptes ± 4 ;
  O3 : reference EXACTE (v1.1) : seed « bande » ssi limsup_{N<=120} |x_N| <= 1
  calcule en arithmetique directe au seed (test grille invalide : degre F_N) ;
  O1 : taux de portees PARMIS les seeds de bandes (reference O3), seuil 0.95.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from mpmath import mp, mpf

mp.dps = 30
PHI = (1 + np.sqrt(5)) / 2
GRILLE = 1 << 18
TMAX = 2.5
L_ORBITE = 10_000
SEEDS_S1_S2 = 8
N_REF = 20          # niveau du test direct bande/gap pour O3
N_OBS = 14          # niveau d'extraction des arêtes / IDOS
NIVEAUX_O2 = list(range(9, 15))    # gelée v1.1 — fenêtre canonique T24


def traces_grille(t):
    x1 = 0.5 * t
    x2 = 0.5 * (t * (t - 1.0) - 1.0)
    x3 = 0.5 * (t * (t * (t - 1.0) - 1.0) - (t - 1.0))
    return [x1, x2, x3]


def orbite(t, L):
    xs = traces_grille(float(t))
    for _ in range(L - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    return np.array(xs)


def fricke_ecart(xs):
    I = (xs[2:] ** 2 + xs[1:-1] ** 2 + xs[:-2] ** 2
         - 2 * xs[2:] * xs[1:-1] * xs[:-2])
    fini = np.isfinite(I)
    if fini.sum() < 10:
        return np.inf, int(fini.sum())
    If = I[fini]
    return float(If.max() - If.min()), int(fini.sum())


def bandes_xN(tg, N):
    """Retourne masque |x_N| <= 1 et x_N sur la grille."""
    xs = traces_grille(tg)
    for _ in range(N - 3):
        xs.append(2 * xs[-1] * xs[-2] - xs[-3])
    xN = xs[-1] if isinstance(xs[-1], np.ndarray) else np.array(xs[-1])
    return np.abs(xN) <= 1.0, xN


def intervalles(masque, tg):
    """Liste [(a,b)] des intervales continus du masque."""
    idx = np.where(masque)[0]
    if len(idx) == 0:
        return []
    coupe = np.where(np.diff(idx) > 1)[0]
    debuts = np.concatenate([[0], coupe + 1])
    fins = np.concatenate([coupe, [len(idx) - 1]])
    return [(float(tg[idx[d]]), float(tg[idx[f]])) for d, f in zip(debuts, fins)]


def main():
    t0 = time.time()
    print("Φ-DYN-2 P1 — PILIER A : re-verification du generateur [fiche v1.0 SCELLEE]")
    print("=" * 78)

    tg = np.linspace(-TMAX, TMAX, GRILLE)

    # ---- extraction des bandes de reference (niveau N_OBS et N_REF, NIVEAUX_O2)
    masque_obs, xN_obs = bandes_xN(tg, N_OBS)
    bandes_obs = intervalles(masque_obs, tg)
    # NOTE v1.1 : le comptage grille au niveau 20 est sous-resolu (bandes
    # minuscules du Cantor invisibles a 2^18) — reference de position
    # uniquement au niveau 14 ; les classifications passent par la
    # reference exacte au seed (limsup).
    print(f"grille 2^18 = {GRILLE} pts · bandes niveau {N_OBS} : {len(bandes_obs)}"
          f" (reference de position)")

    # ---- S1 : aretes de bandes — 8 bandes les plus a gauche DISTINCTES
    # (dedoublonnage : aretes distantes de < 3 cellules grille = tangences
    # degenerees comptees une seule fois ; declaration d'implementation)
    cell = 3 * (tg[1] - tg[0])
    bandes_d = [bandes_obs[0]]
    for b in bandes_obs[1:]:
        if b[0] - bandes_d[-1][0] > cell:
            bandes_d.append(b)
    S1 = [b[0] for b in bandes_d[:SEEDS_S1_S2]]
    # ---- S2 : milieux des 8 premiers gaps distincts (largeur > 3 cellules)
    bornes = sorted({b[1] for b in bandes_d[:40]} | {b[0] for b in bandes_d[:40]})
    gaps = []
    for i in range(len(bornes) - 1):
        largeur = bornes[i + 1] - bornes[i]
        if largeur > 3 * (tg[1] - tg[0]):
            dans_une_bande = any(b[0] <= bornes[i] + 0.5 * largeur <= b[1]
                                 for b in bandes_obs)
            if not dans_une_bande:
                gaps.append((bornes[i], bornes[i + 1]))
    S2 = [0.5 * (g[0] + g[1]) for g in gaps[:SEEDS_S1_S2]]
    # ---- S3 : echantillonnage aveugle
    dE = (2 * TMAX) / 64
    S3 = [-TMAX + (i + 0.5) * dE for i in range(64)]
    print(f"S1 aretes ({len(S1)}) : {[round(s,4) for s in S1]}")
    print(f"S2 gaps   ({len(S2)}) : {[round(s,4) for s in S2]}")
    print(f"S3 aveugle ({len(S3)}) : ΔE = {dE:.6f} sur [-{TMAX}, {TMAX}]")

    # ---- O1/O3 : orbites sur S1+S2+S3, reference EXACTE limsup (v1.1)
    def reference_bande(seed, n_max=120):
        """True si limsup_{N<=n_max} |x_N(seed)| <= 1 (arithmetique exacte)."""
        xs = traces_grille(float(seed))
        m = 0.0
        for n in range(3, n_max):
            v = 2 * xs[-1] * xs[-2] - xs[-3]
            xs.append(v)
            if abs(v) > m:
                m = abs(v)
            if m > 1.0 and n > 25:
                break
        return m <= 1.0, m

    resultats = []
    for nom, seeds in [("S1", S1), ("S2", S2), ("S3", S3)]:
        for s in seeds:
            xs = orbite(s, L_ORBITE)
            ecart, n_fini = fricke_ecart(xs)
            # classification Fricke
            if ecart <= 1e-12:
                classe_f = "portee"
            elif ecart > 1e-9:
                classe_f = "non_portee"
            else:
                classe_f = "grise"
            # reference exacte v1.1
            classe_d, limsup = reference_bande(s)
            classe_d = "bande" if classe_d else "gap"
            resultats.append({"seed": float(s), "grille": nom, "ecart_fricke": ecart,
                              "n_fini": n_fini, "classe_fricke": classe_f,
                              "limsup": limsup, "classe_directe": classe_d})
    df = {"portee": "bande", "non_portee": "gap"}
    comparables = [r for r in resultats if r["classe_fricke"] in df]
    accords = sum(1 for r in comparables
                  if df[r["classe_fricke"]] == r["classe_directe"])
    desaccords = [r for r in comparables
                  if df[r["classe_fricke"]] != r["classe_directe"]]
    taux_o3 = accords / max(1, len(comparables))
    grises = [r for r in resultats if r["classe_fricke"] == "grise"]
    bandes = [r for r in resultats if r["classe_directe"] == "bande"]
    portees_bande = [r for r in bandes if r["classe_fricke"] == "portee"]
    taux_o1 = len(portees_bande) / max(1, len(bandes))
    print(f"\nO1/O3 : {len(resultats)} orbites × {L_ORBITE} itérations")
    print(f"  seeds de bandes (réf. exacte) : {len(bandes)}"
          f" · portées : {len(portees_bande)}"
          f" · non portées : {sum(1 for r in bandes if r['classe_fricke']=='non_portee')}"
          f" · zone grise : {sum(1 for r in bandes if r['classe_fricke']=='grise')}")
    print(f"  O1 : portées parmi bandes = {len(portees_bande)}/{len(bandes)}"
          f" = {taux_o1:.4f} (seuil gelé 0.95)")
    print(f"  O3 : accord Fricke↔référence exacte : {accords}/{len(comparables)}"
          f" = {taux_o3:.4f} (seuil gelé 0.99)")
    for r in desaccords:
        print(f"  DÉSACCORD t={r['seed']:.5f} ({r['grille']}) : Fricke={r['classe_fricke']}"
              f" (écart {r['ecart_fricke']:.2e}) vs réf={r['classe_directe']}"
              f" (limsup={r['limsup']:.6f})")

    # ---- O2 : ratios de comptage niveaux 9..14 (fenêtre canonique T24)
    comptes = []
    for N in NIVEAUX_O2:
        m, _ = bandes_xN(tg, N)
        comptes.append(len(intervalles(m, tg)))
    ratios = [comptes[i + 1] / comptes[i] for i in range(len(comptes) - 1)]
    o2_ratios = all(abs(r - PHI) <= 0.02 for r in ratios[-3:])
    rec_comptes = all(abs(comptes[i + 2] - comptes[i + 1] - comptes[i]) <= 4
                      for i in range(len(comptes) - 2))
    o2_conforme = o2_ratios and rec_comptes
    print(f"\nO2 : bandes par niveau {NIVEAUX_O2} = {comptes}")
    print(f"  ratios = {[round(r,4) for r in ratios]} → φ = {PHI:.4f}"
          f" · 3 derniers dans φ±0.02 : {o2_ratios}"
          f" · récursion comptes ±4 : {rec_comptes} → conforme : {o2_conforme}")

    # ---- O4 : nombre de rotation par transfer-matrix vs grille
    # ETAT AU RUN 1 : relation mal specifiee par la fiche — la comparaison
    # directe (rotation totale/π vs IDOS) diverge de plusieurs centaines,
    # et l'hypothese de reduction mod 1/2 echoue aussi sur les seeds testes.
    # O4 est HORS criteres §3.6 : reporte en annexe NON CONCLUSIF, sans
    # troisieme tentative d'implementation (pas de calibration a l'aveugle).
    def mot_fibonacci(n):
        w = "A"
        for _ in range(n):
            w = "".join("AB" if c == "A" else "A" for c in w)
        return w
    W = mot_fibonacci(N_OBS)

    def rotation_number(t):
        v = np.array([1.0, 0.0])
        phase = 0.0
        prev = np.angle(complex(v[0], v[1]))
        for c in W:
            M = np.array([[t, -1.0], [1.0, 0.0]]) if c == "A" \
                else np.array([[t - 1.0, -1.0], [1.0, 0.0]])
            v = M @ v
            n = np.linalg.norm(v)
            v = v / n
            a = np.angle(complex(v[0], v[1]))
            d = a - prev
            if d > np.pi:
                d -= 2 * np.pi
            elif d < -np.pi:
                d += 2 * np.pi
            phase += d
            prev = a
        return phase / np.pi

    seeds_bandes = [r["seed"] for r in resultats
                    if r["classe_directe"] == "bande"][:8]
    o4_pairs = []
    for s in seeds_bandes:
        rn = rotation_number(s)
        # tentative 2 : reduction mod 2 puis pliage dans [0,1]
        rn2 = rn % 2.0
        rn2 = min(rn2, 2.0 - rn2)
        ig = float(np.interp(s, tg, np.cumsum(masque_obs) / masque_obs.sum()))
        o4_pairs.append({"seed": s, "rotation": rn, "rotation_mod_pliee": rn2,
                         "idos_grille": ig})
    print(f"\nO4 : NON CONCLUSIF — relation rotation/IDOS non spécifiée par la fiche ;"
          f" {len(o4_pairs)} seeds testés, deux implémentations divergent toutes deux."
          f" Reporté en annexe, hors critères §3.6.")

    # ---- O5 : plus grand exposant de Lyapunov (3 orbites, mesure nouvelle)
    def lyapunov(t, L=4000):
        # carte tangente de T(x,y,z) = (y, z, 2yz - x) : jacobienne
        x, y, z = traces_grille(float(t))
        u = np.array([1.0, 0.0, 0.0])
        somme = 0.0
        for n in range(L):
            J = np.array([[0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0],
                          [-1.0, 2.0 * z, 2.0 * y]])
            u = J @ u
            nu = np.linalg.norm(u)
            if nu == 0 or not np.isfinite(nu):
                break
            u = u / nu
            somme += np.log(nu)
            x, y, z = y, z, 2 * z * y - x
            if not all(np.isfinite([x, y, z])):
                break
        return somme / max(1, n)

    lyap = {f"grise_{i}": None for i in range(3)}
    lyap_seeds = [r["seed"] for r in resultats
                  if r["grille"] == "S3" and r["classe_directe"] == "bande"][:3]
    lyap_vals = [lyapunov(s) for s in lyap_seeds]
    print(f"\nO5 : plus grand exposant de Lyapunov (3 orbites S3 bande, "
          f"seeds {[round(s,4) for s in lyap_seeds]}) : "
          f"{[round(v, 4) for v in lyap_vals]} (mesure nouvelle, sans référence)")

    # ---- controle 30 chiffres (mpmath) sur 5 seeds S3 DE BANDES (v1.1)
    mp_seeds = [r["seed"] for r in resultats
                if r["grille"] == "S3" and r["classe_directe"] == "bande"][:5]
    if len(mp_seeds) < 5:
        mp_seeds = mp_seeds + [r["seed"] for r in resultats
                               if r["classe_directe"] == "bande"][:5 - len(mp_seeds)]
    mp_fricke = []
    for s in mp_seeds:
        x, y, z = mpf(0.5) * mpf(s), None, None
        y = mpf(0.5) * (mpf(s) * (mpf(s) - 1) - 1)
        z = mpf(0.5) * (mpf(s) * (mpf(s) * (mpf(s) - 1) - 1) - (mpf(s) - 1))
        I0 = x ** 2 + y ** 2 + z ** 2 - 2 * x * y * z
        drv = mpf(0)
        for n in range(2000):
            x, y, z = y, z, 2 * z * y - x
            I = x ** 2 + y ** 2 + z ** 2 - 2 * x * y * z
            d = abs(I - I0)
            if d > drv:
                drv = d
            if mp.isinf(z) or mp.isnan(z):
                break
        mp_fricke.append({"seed": float(s), "derive_max_30digits": str(drv)})
    print(f"\ncontrôle 30 chiffres (mpmath, 5 orbites × 2000 it) : "
          f"dérives max {[f['derive_max_30digits'] for f in mp_fricke]}")

    # ---- verdict du pilier A (criteres gelés §3.6 v1.1)
    criteres = {
        "O1_fricke_bandes_>=95%": bool(taux_o1 >= 0.95),
        "O2_ratios_T24_fenetre": bool(o2_conforme),
        "O3_classification_>=99%": bool(taux_o3 >= 0.99),
    }
    pilier_a_ok = all(criteres.values())
    print("\n" + "=" * 78)
    print(f"PILIER A (v1.1) : {'PASS' if pilier_a_ok else 'FAIL'} — {criteres}")

    out = {
        "chantier": "PHI-DYN-2-P1-PILIER-A",
        "fiche": "FICHE-PHI-DYN-2-P1-GENERATEUR v1.1 SCELLÉE (4ad4875)",
        "run": "run 2 (run 1 : CALIBRATION v1.0, defauts de redaction documentes)",
        "conventions": "src/t24_ko6_cantor.py (T24) — reprises sans modification",
        "seeds": {"S1_aretes": S1, "S2_gaps": S2,
                  "S3_declarations": {"intervalle": [-TMAX, TMAX], "n": 64,
                                      "delta_E": dE}},
        "orbites": {"L": L_ORBITE, "n_total": len(resultats),
                    "n_bandes_ref_exacte": len(bandes),
                    "portees_parmi_bandes": len(portees_bande)},
        "O1": {"taux_portees_parmi_bandes": taux_o1, "tenu_>=0.95": bool(taux_o1 >= 0.95)},
        "O2": {"comptes": dict(zip(NIVEAUX_O2, comptes)), "ratios": ratios,
               "conforme": bool(o2_conforme)},
        "O3": {"accords": accords, "comparables": len(comparables),
               "taux": taux_o3, "tenu_>=0.99": bool(taux_o3 >= 0.99),
               "desaccords": desaccords},
        "O4": {"statut": "REPORTE_EN_NOTE", "motif": "relation rotation/IDOS non specifiee (v1.1)"},
        "O5": {"lyapunov_3_orbites": lyap_vals, "statut": "mesure nouvelle"},
        "controle_30_digits": mp_fricke,
        "criteres_pilier_A_v1.1": criteres,
        "pilier_A_pass": bool(pilier_a_ok),
        "duree_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out["sha256_script"] = sha
    dest = Path("data/phidyn2_p1_pilierA.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2,
                               default=str), encoding="utf-8")
    print(f"→ {dest}  (sha256 script {sha[:16]}…)")


if __name__ == "__main__":
    main()
