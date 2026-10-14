#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T19 — Q-KO6-T19-2026-10 : LE PONT φ — trois faces d'un nombre
      (chaîne du seesaw ↔ icosaèdre ↔ Ê8) — la carte E8 déclarée à T18
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T19-KO6-PONT-1.0 gelé]

DÉFAUT DU BANC (v1.0, trouvé au premier run du 14/10/2026 — publié) :
  D1  v1.0 identifiait les éléments d'ordre 5 par leur partie scalaire
      φ/2 — mesuré : ce sont les éléments d'ordre 10 (la rotation de
      72° a pour quaternion (cos 36°, …) = (φ/2, …), dont la 5ᵉ
      puissance vaut −e, pas e). Les éléments d'ordre 5 véritables
      (g⁵ = e exact) ont partie scalaire cos 72° = 1/(2φ) ou
      cos 144° = −φ/2 — et leurs traces SO(3) valent respectivement
      −1/φ et φ : c'est-à-dire EXACTEMENT les deux valeurs propres de
      la chaîne du seesaw. Correction v1.1 : l'ordre est mesuré par la
      puissance exacte (g⁵ = e, g ≠ e), pas par la partie scalaire.
      La prédiction (identité des trois faces) n'est pas tuée — elle
      est renforcée ; l'instrument l'était.

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « le pont φ » — l'entrée E8 déclarée (non mesurée) au
      dictionnaire T18. Le nombre d'or apparaît dans trois constructions
      disjointes du corpus : (a) le rayon spectral de la chaîne du
      seesaw à M_R = y = 1 (T14 : ±φ, ±1/φ) ; (b) la trace de la
      rotation d'ordre 5 de l'icosaèdre (le groupe A5, géométrie) ;
      (c) l'arithmétique exacte Q(φ) du groupe icosaédrique binaire 2I
      et du pont de McKay vers Ê8 (P42 : |2I| = 120 = racines⁺(Ê8),
      A·d = 2d exact). Le pont est-il un objet unique, mesuré ?
  Filiation : P42 (pont 120/Ê8 — fichier publié, IMPORTÉ ici) ; T14 (la
      chaîne — forme close) ; T17 (le mot Fibonacci) ; T18 (le
      dictionnaire — l'entrée que cette carte éprouve).
  Convention déclarée (gelée) : sympy n'est requis que par C3/C5 de P42
      (Ricci, Molien théorique — hors périmètre T19) ; un stub sympy est
      injecté dans sys.modules avant l'import de P42, déclaré ici.
      L'environnement déclaré du dépôt (Python + NumPy) suffit.
  STATUT DU MOT (déclaré, gelé) : PONT INTER-DOMAINES — si les trois
      faces coïncident, c'est un théorème (mesuré à zéro paramètre) ;
      AUCUNE prédiction d'expérience nouvelle. Le physique du corpus
      (59 meV, ordre, Majorana) n'est pas touché par cette carte.
  Question unique : les trois faces de φ coïncident-elles à TOL_REG,
      le pont 120 ↔ Ê8 régresse-t-il à P42, et les leviers tuent-ils
      les faces comme déclaré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  |2I| = 120 par fermeture exacte (régression P42 C1) ;
          racines⁺(Ê8) = 120 (P42 C6) ;
      F2  face géométrique (v1.1, D1 corrigé) : les 24 éléments
          d'ordre 5 de 2I (g⁵ = e exact, g ≠ e) ont pour traces SO(3)
          4s² − 1 ∈ {φ, −1/φ} — 12 chacun : la partie scalaire vaut
          cos 72° = 1/(2φ) (trace −1/φ) ou cos 144° = −φ/2 (trace φ),
          exact en Q(φ). Les valeurs propres de la chaîne du seesaw
          sont donc aussi les traces des rotations d'ordre 5 de
          l'icosaèdre ;
      F3  face spectrale : ρ(C(1)) = φ pour la chaîne à sauts (1, 1, 1)
          (régression T14) ;
      F4  pont de McKay : A·d = 2d exact, Σd² = 120,
          dims triées = [1, 2, 2, 3, 3, 4, 4, 5, 6] (régression P42 C4) ;
      F5  leviers : l'aplatissement (φ remplacé par 8/5 dans les
          coordonnées icosaédriques) tue la fermeture et la trace ;
          y = 1/4 tue la face spectrale (régression T17) ; le contrôle
          faux (2cos(π/7) ≈ 1,802) échoue contre φ.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5 (régressions
      tuantes aux fichiers publiés des ancêtres).
  Falsifieur : F1…F4 hors TOL_REG (tue V1…V4) ; un levier non détecté
      (tue V5) ; la régression P42 perdue (tue le banc).
  Prédiction pré-enregistrée : 5/5 — les trois faces coïncident, le pont
      régresse, les leviers tuent.
  Gouvernance : décision d'auteur du 14/10/2026 (« attaque la carte E8 »)
      — run local exécuté avant tout push, empreinte figée au verdict.
"""
import hashlib
import json
import sys
import time
import types
from fractions import Fraction
from pathlib import Path

import numpy as np

TOL = 1e-9          # figé (filiation KO6-REAL-1.0)
TOL_REG = 1e-6      # tolérance de régression (déclarée)

# --- filiation P42 : sympy n'est requis que par C3/C5 (hors périmètre) —
# stub déclaré à la fiche, injecté avant l'import du fichier publié.
sys.modules.setdefault("sympy", types.ModuleType("sympy"))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "p42", str(Path(__file__).resolve().parent / "p42_pont_120_e8.py"))
p42 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p42)


def chaine(y, M):
    """La chaîne à 4 maillons de sauts (y, M, y) — construction T14."""
    return np.array([[0, y, 0, 0],
                     [y, 0, M, 0],
                     [0, M, 0, y],
                     [0, 0, y, 0]], dtype=float)


def q2f(x):
    """Q(φ) = (a, b) → flottant a + b·φ."""
    return float(x[0]) + float(x[1]) * (1 + np.sqrt(5)) / 2


def main():
    t0 = time.time()
    print("T19 — le pont φ : trois faces d'un nombre   "
          "[T19-KO6-PONT-1.0 gelé — RUN LOCAL, publication en attente]")
    print("=" * 76)

    phi = (1 + np.sqrt(5)) / 2

    # ---- V1 / F1 : |2I| = 120 par fermeture exacte ; racines⁺(Ê8) = 120
    G = p42.construire_2I()
    ens = set(G)
    fermeture = all(p42.quat_mul(G[i], G[j]) in ens
                    for i in range(0, 120, 7) for j in range(0, 120, 11))
    n_tot, n_pos = p42.racines_e8()
    v1 = len(G) == 120 and fermeture and (n_tot, n_pos) == (240, 120)
    print(f"V1 F1 : |2I| = {len(G)} (fermeture exacte : {fermeture}) · "
          f"racines Ê8 = {n_tot}, positives = {n_pos} → "
          f"{'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 (v1.1, D1) : face géométrique — l'ordre 5 par la
    # puissance exacte (g⁵ = e, g ≠ e) ; traces SO(3) = 4s² − 1
    e = (p42.UN, p42.ZERO, p42.ZERO, p42.ZERO)
    moins_e = (p42.qscale(Fraction(-1), p42.UN), p42.ZERO, p42.ZERO,
               p42.ZERO)
    def puissance5(g):
        q2 = p42.quat_mul(g, g)
        q4 = p42.quat_mul(q2, q2)
        return p42.quat_mul(q4, g)
    s5 = [g for g in G if g != e and g != moins_e
          and puissance5(g) == e]
    ordres_exact = True
    trace_phi = trace_un_sur_phi = True
    nb_phi = nb_un_sur_phi = 0
    for g in s5:
        q2 = p42.qp(g[0], g[0])
        t = p42.qm(p42.qscale(Fraction(4), q2), p42.UN)   # 4s² − 1
        if t == (Fraction(0), Fraction(1)):
            nb_phi += 1
        elif t == (Fraction(1), Fraction(-1)):            # 1 − φ = −1/φ
            nb_un_sur_phi += 1
        else:
            ordres_exact = False
    # contrôle flottant des mêmes traces
    traces = [4 * q2f(g[0]) ** 2 - 1 for g in s5]
    v2 = (len(s5) == 24 and ordres_exact
          and nb_phi == 12 and nb_un_sur_phi == 12
          and all(abs(t - phi) < TOL_REG or abs(t + 1 / phi) < TOL_REG
                  for t in traces))
    print(f"V2 F2 (v1.1) : {len(s5)} éléments d'ordre 5 (g⁵ = e exact) · "
          f"traces exactes : 12 × φ + 12 × (−1/φ) : "
          f"{ordres_exact and nb_phi == 12 and nb_un_sur_phi == 12} · "
          f"traces flottantes dans {{±φ, ±1/φ}} : "
          f"{all(abs(t - phi) < TOL_REG or abs(t + 1 / phi) < TOL_REG for t in traces)} "
          f"→ {'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : face spectrale — ρ(C(1)) = φ (régression T14)
    ev = np.linalg.eigvalsh(chaine(1.0, 1.0))
    v3 = abs(ev[-1] - phi) < TOL_REG and abs(ev[0] + phi) < TOL_REG
    print(f"V3 F3 : spectre C(1) = {np.round(ev, 9).tolist()} · ρ = φ : "
          f"{v3} → {'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : pont de McKay (régression P42 C4)
    trouves = p42.caracteres_irreductibles(G)
    A = p42.mckay(trouves, G)
    dims = sorted(int(t[e][0]) for t in trouves)
    d = np.array([int(t[e][0]) for t in trouves])
    mckay_ok = np.array_equal(A @ d, 2 * d)
    v4 = (len(trouves) == 9 and mckay_ok
          and sum(x * x for x in dims) == 120
          and dims == [1, 2, 2, 3, 3, 4, 4, 5, 6])
    print(f"V4 F4 : McKay A·d = 2d : {mckay_ok} · Σd² = "
          f"{sum(x * x for x in dims)} · dims = {dims} → "
          f"{'PASS' if v4 else 'FAIL'}")

    # ---- V5 / F5 : leviers + contrôle faux
    lv = {}
    # levier d'aplatissement : φ -> 8/5 dans les coordonnées icosaédriques
    PH2 = (Fraction(4, 5), Fraction(0))            # (8/5)/2
    U2P = (Fraction(5, 16), Fraction(0))           # 1/(2·8/5)
    base = [p42.ZERO, p42.DEMI, PH2, U2P]
    aplati = set()
    for perm in __import__("itertools").permutations(range(4)):
        inv = sum(1 for a in range(4) for b in range(a + 1, 4)
                  if perm[a] > perm[b])
        if inv % 2:
            continue
        iz = perm.index(0)
        for signs in __import__("itertools").product((1, -1), repeat=3):
            it = iter(signs)
            v = tuple(base[perm[p]] if p == iz else
                      p42.qscale(Fraction(next(it)), base[perm[p]])
                      for p in range(4))
            aplati.add(v)
    fuite = any(p42.quat_mul(aplati.__iter__().__next__(), g) not in aplati
                for g in list(aplati)[:20])
    trace_aplati = 4 * q2f(PH2) ** 2 - 1
    lv["aplatissement φ→8/5 : fermeture tuée"] = bool(fuite)
    lv["aplatissement : trace = 1,56 ≠ φ"] = abs(trace_aplati - phi) > 0.05
    evq = np.linalg.eigvalsh(chaine(0.25, 1.0))
    lv["y = 1/4 tue la face spectrale (T17)"] = abs(evq[-1] - phi) > TOL_REG
    lv["contrôle faux (2cos(π/7)) échoue"] = \
        abs(2 * np.cos(np.pi / 7) - phi) > TOL_REG
    for k, val in lv.items():
        print(f"V5 levier — {k} : {val}")
    V5 = all(lv.values())

    criteres = {"V1_2I_E8_regression_P42": bool(v1),
                "V2_face_geometrique_trace": bool(v2),
                "V3_face_spectrale_chaine": bool(v3),
                "V4_mckay_regression_P42": bool(v4),
                "V5_leviers": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T19-Q-KO6-PONT-PHI-2026-10",
        "protocole": "T19-KO6-PONT-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "le pont φ : trois faces d'un nombre (chaîne ↔ icosaèdre "
                 "↔ Ê8) — la carte E8 déclarée au dictionnaire T18",
        "statut_du_mot": "PONT INTER-DOMAINES — théorème mesuré à zéro "
                         "paramètre ; AUCUNE prédiction d'expérience "
                         "nouvelle ; le physique (59 meV) n'est pas touché",
        "convention_gelée": "stub sympy déclaré avant l'import P42 (sympy "
            "n'est requis que par C3/C5 de P42, hors périmètre)",
        "faces": {
            "spectrale": "spectre C(1) = ±φ, ±1/φ — chaîne du seesaw (T14)",
            "geometrique": "traces SO(3) des 24 rotations d'ordre 5 de "
                           "l'icosaèdre = 12 × φ + 12 × (−1/φ) (v1.1, D1 "
                           "corrigé) — les valeurs propres de la chaîne "
                           "sont les traces des rotations",
            "arithmetique": "Q(φ) exact de 2I et pont de McKay vers Ê8 "
                            "(P42) : A·d = 2d, Σd² = 120",
        },
        "V1": bool(v1), "V2": {"nb_elements": len(s5),
                               "traces_12phi_12un_sur_phi":
                                   bool(ordres_exact and nb_phi == 12
                                       and nb_un_sur_phi == 12)},
        "V3": bool(v3),
        "V4": {"mckay": bool(mckay_ok), "dims": dims},
        "V5": {k: bool(v) for k, v in lv.items()},
        "defaut_du_banc_corrigé": {
            "D1": "v1.0 : identification des éléments d'ordre 5 par la "
                  "partie scalaire φ/2 — ce sont les éléments d'ordre 10 "
                  "(cos 36° = φ/2 → g⁵ = −e). v1.1 : ordre mesuré par "
                  "g⁵ = e exact ; les éléments d'ordre 5 ont scalaire "
                  "cos 72° = 1/(2φ) (trace −1/φ) ou cos 144° = −φ/2 "
                  "(trace φ) — la correction renforce le pont : les "
                  "traces des rotations sont exactement le spectre de "
                  "la chaîne"},
        "entree_dictionnaire_T18": {
            "mot": "pont-φ-icosaédrique", "filiation": "T19 (P42, T14)",
            "polynôme": "λ⁴ − 3λ² + 1 (face A4 de la chaîne)",
            "séquence": "φ commun aux trois constructions ; pont McKay "
                        "A·d = 2d vers Ê8",
            "statut": "pont inter-domaines mesuré — entrée proposée au "
                      "dictionnaire (la modification de T18 attend sa "
                      "propre décision de gouvernance)"},
        "candidats_déclarés_non_mesurés": [
            "pavages de Penrose / quasicristaux (le φ y est diffusif, "
            "pas spectral : carte séparée requise)"],
        "falsifieur": "F1…F4 hors TOL_REG ; levier non détecté ; "
                      "régression P42 perdue",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t19_ko6_pont_phi_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T19 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
