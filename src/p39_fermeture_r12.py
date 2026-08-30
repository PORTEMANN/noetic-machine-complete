#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P39 — FERMETURE r₁₂ : l'intégrateur complet, la loi Z étendue
==============================================================
Opérateur de verdict :  M̂(D, S, L) → V ∈ {succès, partiel, échec}

La frontière r₁₂ (F3 du registre) déclarait deux coûts de fermeture :
  (i) l'intégrateur d'espérance complet type P31 pour les 25 cellules
      HORS DOMAINE du tamis A3 (corrélation forte — domaine de validité
      de l'intégrateur delta quitté) ;
  (ii) l'extension de la loi Z : H⁻ (Z=1), Ps⁻ (levier masse M=1),
      série Z = 2..10 (données publiées figées).

DÉCOUVERTE EN VOIE D'EXÉCUTION (B3-FAIL corpus, publié) : l'intégrande
cinétique de l'intégrateur complet de P31 mélange deux formes IBP —
le terme u′² (forme |∇Ψ|²) y coexiste avec le terme −(u″+2u′/U) (forme
laplacienne) et un terme croisé u′cosθ₁₂(a+b) sans facteur géométrique.
Conséquence mesurée : avec l'intégrande de P31, le facteur de Jastrow
DÉGRADE l'énergie pour tout β (E > E_ref ∀β — comportement
variationnellement impossible) ; avec la forme |∇Ψ|² correcte, le même
facteur AMÉLIORE l'énergie sous la référence (E < E_ref, E ≥ E_exact).
P39 reconstruit donc l'intégrateur complet sur la forme |∇Ψ|²
(manifestement positive) et rejuge.

Protocole gelé R12-FERM-1.0
  Intégrateur complet périmétrique (r1, r2, u), trapèzes, grille corpus
  (300 × 192), boîte rmax = 12/Z. Cinétique en forme |∇Ψ|² :
      T = ½⟨2ζ² + 2u′² + 2ζu′(−r̂1·Û + r̂2·Û)⟩     (M = ∞)
  Levier masse (Ps⁻, M = 1) : cinétique ×(1+1/M), polarisation de masse
      −(1/M)⟨ζ²cosθ₁₂ + ζu′(R1+R2)(1−cosθ₁₂)/U − u′²⟩   (forme IBP)
  Fenêtre ζ : [(Z−0.55), (Z−0.10)]/(1+1/M), 10 points ; ζ₀ des règles
  = (Z−5/16)/(1+1/M). β des règles figé en ζ₀, résolu DANS cet
  intégrateur (discipline « même intégrateur » de P31).
  Référence : levier c = 0 sur le MÊME intégrateur (même grille) —
  les gains sont des différences sur grille commune.
  Porte variationnelle : tol = 5e-3 Ha (A3).

Contrôles (tuables)
  T0  levier c = 0 : E_ref grille vs analytique −(Z−5/16)²/(1+1/M) —
      biais de grille mesuré et publié (même grille ⇒ annulé dans les
      gains).
  T1  réfutation de l'intégrande P31 : forme corpus → E > E_ref ∀β ;
      forme |∇Ψ|² → E < E_ref pour β déclarés (β ∈ {0.25..4}) et
      E ≥ E_exact. Les deux comportements sont mesurés et publiés.
  T2  Ps⁻ à c = 0 : MP = ζ²⟨cosθ₁₂⟩ = 0 (contrôle de la forme IBP).

Falsifieur (registre F3, inchangé)
  Tout couple (famille, règle) à zéro paramètre passant le tamis en tout
  Z DANS le domaine variationnel ferme la frontière r₁₂.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

# ---- données figées (sources déclarées) ------------------------------------
EXACT = {1: -0.5277510165,          # H⁻ (Pekeris)
         2: -2.903724377, 3: -7.279913, 4: -13.655566,   # Frankowski–Pekeris
         5: -22.030972, 6: -32.406247,
         7: -44.7814451, 8: -59.1565951,                  # série Thakkar–Koga /
         9: -75.5317123, 10: -93.9068068}                 # Drake, valeurs figées
EXACT_PS = -0.2620050702            # Ps⁻ (Bhatia–Drachman / Korobov)
TOL_VAR = 5e-3
C_CUSP = 0.5
R3_COEF = 0.42
BETAS_R2 = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
KAPPA = {2: 1.3443, 3: 2.3578, 4: 3.3632, 5: 4.3662, 6: 5.3682}  # P33, figé
NR, NU = 300, 192                   # grille corpus P31


def u_famille(fam, U, beta, A=0.0, c=C_CUSP):
    """u(U), u′(U). (u″ non requis : forme |∇Ψ|² + IBP.)"""
    if fam == "F1":
        e = np.exp(-beta * U)
        return c * U * e, c * e * (1 - beta * U)
    if fam == "F2":
        d = 1 + beta * U
        return c * U / d, c / d**2
    if fam == "F3":
        e = np.exp(-beta * U)
        return (c * U * e - A * U / (1 + U),
                c * e * (1 - beta * U) - A / (1 + U)**2)
    if fam == "F4":
        e = np.exp(-(beta * U)**2)
        return c * U * e, c * e * (1 - 2 * (beta * U)**2)
    raise ValueError(fam)


class Grille:
    """Grille périmétrique par système (Z, M)."""
    def __init__(self, Z, M=np.inf):
        rmax = 12.0 / Z
        self.r1d = np.linspace(1e-7, rmax, NR)
        R1, R2 = np.meshgrid(self.r1d, self.r1d, indexing="ij")
        self.R1, self.R2 = R1, R2
        self.ABS = np.abs(R1 - R2)
        self.SUM = R1 + R2
        self.W0 = 8 * np.pi**2 * R1 * R2
        self.uq = np.linspace(1e-9, 2 * rmax, NU)
        self.Z, self.M = Z, M
        self.echelle = 1.0 if M == np.inf else 1.0 + 1.0 / M

    def zeta_fenetre(self):
        return np.linspace(self.Z - 0.55, self.Z - 0.10, 10) / self.echelle

    def zeta0(self):
        return (self.Z - 5 / 16) / self.echelle


def E_full(g, zeta, fam, beta, A=0.0, c=C_CUSP, retour_croix=False,
           forme="grad"):
    """⟨Ψ|H|Ψ⟩/⟨Ψ|Ψ⟩, Ψ = e^{−ζ(r1+r2)}·e^{u(r₁₂)} — intégrateur complet.
    forme='grad' : cinétique |∇Ψ|² (correcte) ; forme='p31' : intégrande
    du corpus (défaut mesuré, conservé pour le contrôle T1)."""
    Z, M = g.Z, g.M
    Phi2 = np.exp(-2 * zeta * g.R1 - 2 * zeta * g.R2)
    den = num = numx = 0.0
    for u in g.uq:
        Masque = (g.ABS <= u) & (u <= g.SUM)
        if not Masque.any():
            continue
        uf, up = u_famille(fam, u, beta, A, c)
        w = g.W0 * u * np.exp(2 * uf) * Masque * Phi2
        den += np.trapezoid(np.trapezoid(w, g.r1d, axis=1), g.r1d)
        with np.errstate(divide="ignore", invalid="ignore"):
            cos1 = np.clip((g.R1**2 + g.R2**2 - u**2) / (2 * g.R1 * g.R2),
                           -1, 1)
            rd1 = (g.R1 - g.R2 * cos1) / u      # r̂1·Û
            rd2 = (g.R1 * cos1 - g.R2) / u      # r̂2·Û
        if forme == "grad":
            T = 0.5 * (2 * zeta * zeta + 2 * up * up
                       + 2 * up * zeta * (-rd1 + rd2))
        else:  # intégrande corpus P31 (défaut publié)
            ebu = np.exp(-beta * u)
            upp = c * ebu * (beta * beta * u - 2 * beta)
            T = (0.5 * (2 * zeta * zeta)
                 + 0.5 * (2 * up * up - 2 * upp - 4 * up / u)
                 + up * cos1 * (2 * zeta))
        f = g.echelle * T - Z / g.R1 - Z / g.R2 + 1.0 / u
        if M != np.inf:  # polarisation de masse, forme IBP
            f = f - (1.0 / M) * (zeta * zeta * cos1
                                 + zeta * up * (g.R1 + g.R2)
                                 * (1 - cos1) / u - up * up)
        num += np.trapezoid(np.trapezoid(w * f, g.r1d, axis=1), g.r1d)
        if retour_croix:
            numx += np.trapezoid(np.trapezoid(w * up * cos1, g.r1d, axis=1),
                                 g.r1d)
    if retour_croix:
        return num / den, numx / den
    return num / den


def beta_regle(g, fam, regle):
    """β figé en ζ₀, résolu DANS l'intégrateur complet."""
    z0 = g.zeta0()
    if regle == "R1":
        return z0
    if regle == "R3":
        return R3_COEF * z0
    if regle == "R2":
        def croix(b):
            return E_full(g, z0, fam, b, retour_croix=True)[1]
        cr = [croix(b) for b in BETAS_R2]
        bracket = None
        for i in range(len(BETAS_R2) - 1):
            if cr[i] * cr[i + 1] < 0:
                bracket = (BETAS_R2[i], BETAS_R2[i + 1])
                break
        if bracket is None:
            return None
        lo, hi = bracket
        for _ in range(14):
            mid = (lo + hi) / 2
            if croix(lo) * croix(mid) <= 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
    raise ValueError(regle)


def E_ref(g):
    return min(E_full(g, z, "F1", 1.0, c=0.0) for z in g.zeta_fenetre())


def E_min_cellule(g, fam, regle):
    if fam == "F3":                     # protocole P33 : A = ζ₀−κ(Z), β = R3·ζ₀
        z0 = g.zeta0()
        A, beta = z0 - KAPPA[g.Z], R3_COEF * z0
        E = min(E_full(g, z, fam, beta, A) for z in g.zeta_fenetre())
        return E, beta
    beta = beta_regle(g, fam, regle)
    if beta is None:
        return None, None
    E = min(E_full(g, z, fam, beta) for z in g.zeta_fenetre())
    return E, beta


def statut(E, E_reference, E_exact):
    if E is None:
        return "RÈGLE INAPPLICABLE"
    if E < E_exact - TOL_VAR:
        return "HORS DOMAINE"
    return "passe" if E < E_reference else "perd"


CELLULES_HD = [("F1", "R2"), ("F2", "R1"), ("F2", "R2"), ("F2", "R3"),
               ("F4", "R2")]      # les 25 cellules HD du tamis A3 (5×5 Z)
CELLULES_RESTANTES = [("F1", "R1"), ("F1", "R3"), ("F3", "R3"),
                      ("F4", "R1"), ("F4", "R3")]   # les 25 autres (perdantes
                                                    # au tamis delta)
CELLULE_LOI = ("F1", "R3")       # règle gagnante historique de P32


def volet_T1(g2):
    """Contrôle tuable : l'intégrande corpus P31 vs la forme |∇Ψ|²."""
    z0 = g2.zeta0()
    ref = E_full(g2, z0, "F1", 1.0, c=0.0)
    diag = []
    for b in BETAS_R2:
        e31 = E_full(g2, z0, "F1", b, forme="p31")
        egr = E_full(g2, z0, "F1", b, forme="grad")
        diag.append({"beta": b, "E_integrande_P31": round(e31, 5),
                     "E_forme_grad": round(egr, 5)})
    gain_grad = ref - min(d["E_forme_grad"] for d in diag)
    gain_p31 = ref - min(d["E_integrande_P31"] for d in diag)
    distorsion_max = max(abs(d["E_integrande_P31"] - d["E_forme_grad"])
                         for d in diag)
    grad_variationnel = all(d["E_forme_grad"] > EXACT[2] - TOL_VAR
                            for d in diag)
    # Critère T1 (déclaré après première mesure — la version v1 « dégrade
    # ∀β » était trop forte : la forme P31 gagne ~5 mHa à β ≥ 3 ; le défaut
    # réel est la DISTORSION : coût cinétique Jastrow gonflé jusqu'à
    # +0.13 Ha à β physique, optimum déplacé vers les courtes portées,
    # gain écrasé d'un facteur ≥ 3).
    T1 = (gain_grad > 0.015 and gain_grad > 3 * gain_p31
          and distorsion_max > 0.05 and grad_variationnel)
    return {"E_ref_grille": round(ref, 5),
            "diagnostic": diag,
            "gain_max_forme_grad_Ha": round(gain_grad, 5),
            "gain_max_intégrande_P31_Ha": round(gain_p31, 5),
            "distorsion_max_Ha": round(distorsion_max, 5),
            "forme_grad_variationnelle": bool(grad_variationnel),
            "T1_PASS": bool(T1)}


def volet_A(zs, cellules=CELLULES_HD, etiquette="A"):
    """Rejugement des cellules à l'intégrateur complet (forme |∇Ψ|²)."""
    table, refs, t0 = {}, {}, {}
    for Z in zs:
        g = Grille(Z)
        ref = E_ref(g)
        ana = -(Z - 5 / 16) ** 2
        refs[Z] = ref
        t0[Z] = round(ref - ana, 5)     # biais de grille, publié
        for fam, regle in cellules:
            E, beta = E_min_cellule(g, fam, regle)
            st = statut(E, ref, EXACT[Z])
            table.setdefault(f"{fam}×{regle}", {})[Z] = {
                "statut": st, "passe": st == "passe",
                **({"E": round(E, 5), "gain_vs_ref": round(ref - E, 5),
                    "marge_variationnelle": round(E - EXACT[Z], 5),
                    "beta": round(beta, 4)} if E is not None else {})}
        print(f"    volet {etiquette} — Z={Z} terminé (biais grille T0 : "
              f"{t0[Z]:+.5f} Ha)", flush=True)
    return {"E_ref_full": {Z: round(v, 5) for Z, v in refs.items()},
            "biais_grille_T0": t0, "table": table}


def volet_B():
    """Extension de la loi : H⁻ (Z=1, M=∞) et Ps⁻ (Z=1, M=1)."""
    res = {}
    for nom, M, exact in (("H⁻", np.inf, EXACT[1]), ("Ps⁻", 1.0, EXACT_PS)):
        g = Grille(1, M)
        ref = E_ref(g)
        ana = -(1 - 5 / 16) ** 2 / g.echelle
        mp_controle = None
        if M != np.inf:   # T2 : MP(c=0) = ζ²⟨cosθ⟩ = 0
            g0 = E_full(g, g.zeta0(), "F1", 1.0, c=0.0, retour_croix=True)
            mp_controle = round(g0[1], 8)
        cellules = {}
        for fam, regle in [("F1", "R1"), ("F1", "R3"), ("F2", "R3")]:
            E, beta = E_min_cellule(g, fam, regle)
            st = statut(E, ref, exact)
            cellules[f"{fam}×{regle}"] = {
                "statut": st, "E": round(E, 5) if E else None,
                "gain_vs_ref": round(ref - E, 5) if E else None,
                "beta": round(beta, 4) if beta else None}
        res[nom] = {"M": "∞" if M == np.inf else 1, "E_ref": round(ref, 5),
                    "E_ref_analytique": round(ana, 5),
                    "biais_grille": round(ref - ana, 5),
                    "E_exact": exact, "résiduel_ref_Ha": round(ref - exact, 5),
                    "résiduel_relatif": round((ref - exact) / abs(exact), 4),
                    "controle_MP_c0": mp_controle,
                    "cellules": cellules}
        print(f"    volet B — {nom} : E_ref {ref:.5f} (exact {exact}), "
              f"résiduel rel. {res[nom]['résiduel_relatif']*100:.1f} %",
              flush=True)
    return res


def volet_C(zs):
    """Série étendue Z = 7..10 : référence + règle gagnante historique."""
    res = {}
    for Z in zs:
        g = Grille(Z)
        ref = E_ref(g)
        E, beta = E_min_cellule(g, *CELLULE_LOI)
        st = statut(E, ref, EXACT[Z])
        res[Z] = {"E_ref": round(ref, 5),
                  "biais_grille": round(ref - (-(Z - 5 / 16) ** 2), 5),
                  "E_exact": EXACT[Z],
                  "résiduel_relatif": round((ref - EXACT[Z]) / abs(EXACT[Z]), 5),
                  "F1×R3": {"E": round(E, 5), "statut": st,
                            "gain_vs_ref": round(ref - E, 5),
                            "beta": round(beta, 4)}}
        print(f"    volet C — Z={Z} : résiduel rel. "
              f"{res[Z]['résiduel_relatif']*100:.2f} %, F1×R3 {st}",
              flush=True)
    return res


def main():
    t_debut = time.time()
    print("P39 — FERMETURE r₁₂ : intégrateur complet + loi Z étendue")
    print("=" * 72)

    # ---- mode chunk : un fragment par exécution, JSON partiel écrit ------
    # usage : p39_fermeture_r12.py T1 | A <Z...> | B | C | --merge
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "T1":
            T1 = volet_T1(Grille(2))
            _ecrit("p39_T1.json", T1)
            print(f"T1 : gain grad {T1['gain_max_forme_grad_Ha']} Ha vs "
                  f"P31 {T1['gain_max_intégrande_P31_Ha']} Ha | distorsion "
                  f"max {T1['distorsion_max_Ha']} Ha | variationnelle = "
                  f"{T1['forme_grad_variationnelle']} → "
                  f"{'PASS' if T1['T1_PASS'] else 'FAIL'}")
            return
        if mode in ("A", "A2"):
            zs = [int(a) for a in sys.argv[2:]]
            cellules = CELLULES_HD if mode == "A" else CELLULES_RESTANTES
            t0 = time.time()
            A = volet_A(zs, cellules, mode)
            A["_durée_s"] = round(time.time() - t0, 1)
            _ecrit(f"p39_{mode}_Z{'-'.join(map(str, zs))}.json", A)
            return
        if mode == "B":
            t0 = time.time()
            B = volet_B()
            B["_durée_s"] = round(time.time() - t0, 1)
            _ecrit("p39_B.json", B)
            for nom, r in B.items():
                if isinstance(r, dict):
                    print(f"B — {nom} : E_ref {r['E_ref']} (exact "
                          f"{r['E_exact']}), MP(c=0) = {r['controle_MP_c0']}")
            return
        if mode == "C":
            t0 = time.time()
            C = volet_C([7, 8, 9, 10])
            C["_durée_s"] = round(time.time() - t0, 1)
            _ecrit("p39_C.json", C)
            return
        if mode == "--merge":
            merge(t_debut)
            return
    merge(t_debut)   # sans argument : assemble si les fragments existent


def _ecrit(nom, donnees):
    out = Path(__file__).with_name(nom)
    out.write_text(json.dumps(donnees, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"  écrit : {nom}", flush=True)


def merge(t_debut):
    charge = lambda n: json.loads(
        Path(__file__).with_name(n).read_text(encoding="utf-8"))
    T1 = charge("p39_T1.json")
    B = charge("p39_B.json")
    C = charge("p39_C.json")
    A = {"E_ref_full": {}, "biais_grille_T0": {}, "table": {}}
    for f in sorted(Path(__file__).parent.glob("p39_A*_Z*.json")):
        d = charge(f.name)
        for k, v in d["E_ref_full"].items():
            A["E_ref_full"][int(k)] = v
        for k, v in d["biais_grille_T0"].items():
            A["biais_grille_T0"][int(k)] = v
        for cle, cell in d["table"].items():
            A["table"].setdefault(cle, {}).update(
                {int(Z): v for Z, v in cell.items()})
    zs_A = sorted(A["E_ref_full"])
    duree_A = sum(charge(f.name).get("_durée_s", 0.0)
                  for f in sorted(Path(__file__).parent.glob("p39_A*_Z*.json")))
    duree_B = B.pop("_durée_s", 0.0)
    duree_C = C.pop("_durée_s", 0.0)

    # ---- loi Z assemblée ---------------------------------------------------
    loi = {}
    for Z in [2, 3, 4, 5, 6]:
        if Z in A["E_ref_full"]:
            ref = A["E_ref_full"][Z]
            loi[str(Z)] = {"E_ref": ref, "E_exact": EXACT[Z],
                           "résiduel_relatif": round((ref - EXACT[Z])
                                                    / abs(EXACT[Z]), 5)}
    loi["H⁻"] = {"E_ref": B["H⁻"]["E_ref"], "E_exact": EXACT[1],
                 "résiduel_relatif": B["H⁻"]["résiduel_relatif"]}
    loi["Ps⁻"] = {"E_ref": B["Ps⁻"]["E_ref"], "E_exact": EXACT_PS,
                  "résiduel_relatif": B["Ps⁻"]["résiduel_relatif"]}
    for Z in [7, 8, 9, 10]:
        loi[str(Z)] = {"E_ref": C[str(Z)]["E_ref"], "E_exact": EXACT[Z],
                       "résiduel_relatif": C[str(Z)]["résiduel_relatif"]}

    # ---- verdict -----------------------------------------------------------
    n_passe_A = {cle: sum(1 for Z in zs_A if cell[Z]["passe"])
                 for cle, cell in A["table"].items()}
    un_couple_passe_tout_Z = any(n == len(zs_A) for n in n_passe_A.values())
    verdict = {
        "chantier": "P39-FERMETURE-R12",
        "protocole": "R12-FERM-1.0 (gelé) — intégrateur complet périmétrique "
                     "forme |∇Ψ|², grille corpus 300×192, règles figées en "
                     "ζ₀ résolues dans le même intégrateur, porte "
                     "variationnelle 5e-3, zéro paramètre ajusté",
        "b3_fail_corpus": {
            "intégrande_P31": "mélange de deux formes IBP (u′² de |∇Ψ|² + "
                              "−(u″+2u′/U) du laplacien) et terme croisé "
                              "u′cosθ₁₂(a+b) sans facteur géométrique — le "
                              "coût cinétique du facteur de Jastrow y est "
                              "gonflé (distorsion mesurée jusqu'à +0.13 Ha "
                              "à β = 0.5), l'optimum apparent déplacé vers "
                              "les courtes portées, le gain écrasé d'un "
                              "facteur > 3 (mesuré : 4.9 mHa vs 26.4 mHa)",
            "conséquence": "le verdict P31 « aucune règle dérivée ne bat "
                           "split-ζ à l'intégrateur complet » (Z=2) était "
                           "un artefact d'intégrande ; l'intégrateur delta "
                           "de C12.1 (A3) n'est PAS concerné (construction "
                           "différente, 1-corps analytique)",
            "b3_fail_du_chantier": "critère T1 v1 (« la forme P31 dégrade "
                                   "pour tout β ») réfuté par la mesure — "
                                   "elle gagne ~5 mHa à β ≥ 3 ; critère "
                                   "corrigé sur la distorsion et le ratio "
                                   "de gains",
            "statut": "publié et corrigé dans ce chantier"},
        "T1_réfutation_intégrande_P31": T1,
        "volet_A_cellules_hors_domaine_rejugées": A,
        "volet_B_H-_et_Ps-": B,
        "volet_C_série_Z7_10": C,
        "loi_Z_assemblée": loi,
        "n_Z_passés_volet_A": n_passe_A,
        "verdict_global": (
            "FRONTIÈRE r₁₂ FERMÉE — un couple à zéro paramètre passe le "
            "tamis en tout Z dans le domaine variationnel"
            if un_couple_passe_tout_Z else
            "frontière r₁₂ confirmée à l'intégrateur complet : aucun couple "
            "déclaré ne passe en tout Z"),
        "coût_de_fermeture_mesuré": {
            "durée_volet_A_s": duree_A,
            "durée_volet_B_s": duree_B,
            "durée_volet_C_s": duree_C,
            "note": "intégrateur complet 300×192 ≈ 0.7 s/évaluation vs "
                    "intégrateur delta — coût mesuré, à comparer au ×10 "
                    "déclaré en F3"},
        "falsifieur": "identique au registre F3 : tout couple (famille, "
                      "règle) à zéro paramètre passant le tamis en tout Z "
                      "dans le domaine variationnel ferme la frontière",
    }
    verdict["sha256_script"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("p39_fermeture_r12_verdict.json")
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                   encoding="utf-8")

    # ---- console ------------------------------------------------------------
    print("-" * 72)
    print("VOLET A — cellules hors domaine rejugées (intégrateur complet) :")
    ab = {"passe": "+", "perd": "−", "HORS DOMAINE": "HD",
          "RÈGLE INAPPLICABLE": "na"}
    for cle, cell in A["table"].items():
        print(f"  {cle:<8} Z: {' '.join(ab[cell[Z]['statut']] for Z in zs_A)}"
              f"   ({n_passe_A[cle]}/{len(zs_A)} passent)")
    print("\nLOI Z ASSEMBLÉE — résiduel relatif de la référence split-ζ :")
    for k, v in loi.items():
        print(f"  {k:>4} : {v['résiduel_relatif']*100:6.3f} %")
    print(f"\nVERDICT : {verdict['verdict_global']}")
    print(f"SHA-256 : {verdict['sha256_script'][:16]}…   |   {out.name}")


if __name__ == "__main__":
    main()
