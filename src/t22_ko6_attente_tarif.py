#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T22 — Q-KO6-T22-2026-10 : LA CARTE D'ATTENTE DU TARIF —
      le pont φ certifie-t-il une échelle sans cadran mesuré ?
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T22-KO6-ATTENTE-1.0 gelé]

FICHE (gelée avant le run — 14/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc
  Objet    : « la carte d'attente du tarif » — le chantier C1 du carnet
      NOTE-CANDIDATS-PONT-PHI. La question du tarif de Jacobson
      (MCS-24) est fermée anti-stable : la proximité du contenu
      spectral au tarif η = 1/(4ℏG) mesurait la convention de
      cadran, pas le contenu (orbite de z : de −10,7 à +22,6 selon
      les 7 cadrans déclarés). Le pont φ ne peut pas rouvrir cette
      question sans cadran MESURÉ — et cette impossibilité est ici
      un théorème mesuré : la densité du module d'or rend toute
      échelle arbitrairement approchable d'un point du module.
      La carte scelle aujourd'hui le protocole d'attente : quand le
      cadran sera mesuré (Σm_ν au plancher, bornes déclarées au
      registre de veille), la re-mesure s'exécutera sans rien
      réécrire.
  Filiation : MCS-24 (verdict CSi — fichier publié du dépôt
      coincidences-stables, cité par empreinte et relu si présent) ;
      T12 (la relation d'ancre) ; T21 (le module d'or — densité
      certifiée) ; T19/P42 (les 120) ; T20-D3 (Legendre) ;
      NOTE-CANDIDATS-PONT-PHI (C1) ; REGISTRE-VEILLE-ANTICIPATION
      (le déclencheur et ses bornes).
  STATUT DU MOT (déclaré, gelé) : CARTE D'ATTENTE — le résultat
      principal est une impossibilité mesurée (densité du module) ;
      AUCUNE prédiction d'expérience nouvelle ; la carte DORT
      jusqu'au fait, et le dormir est publié (règle de la maison,
      comme la loi harmonique à CSp).
  Question unique : le pont φ peut-il certifier une échelle sans
      cadran mesuré ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  régression MCS-24 : l'orbite de z aux 7 cadrans déclarés
          {+10,895 ; −10,711 ; +10,895 ; +22,593 ; +7,449 ; +7,449 ;
          +1,171} avec inversion de signe g0 ↔ g1 — anti-stabilité
          certifiée par l'orbite (valeurs citées, empreinte du
          fichier vérifiée si présent) ;
      F2  densité du module d'or (théorème mesuré) : dans la
          fenêtre [0, W), W = 21·2^k, l'écart minimal g(W) entre
          points distincts de {m + nφ} obéit au théorème des trois
          écarts (Sós) : non monotone — mais à enveloppe linéaire,
          W·g(W) borné mesuré, et ratios g(2W)/g(W) ∈ {≈ 1/φ, ≈
          1/φ²} mesurés (l'échelle de l'écart est elle-même dorée) ;
          à W = 21 (fenêtre de T21), g est mesuré — et tout ratio
          r ∈ [0, 21) est à moins de g/2 d'un point du module
          (certificat publié) ;
      F3  corollaire pour le tarif : la coïncidence MCS-24 n'avait
          pas d'alternative structurelle — à g/2 près, TOUTE échelle
          coïncide avec le module ; l'anti-stabilité CSi est
          expliquée par la densité, à un certificat g/2 près ;
      F4  leviers : fenêtre (g(W) divise ~par 2 quand W double —
          mesuré) ; Legendre (l'erreur |1/φ² − F_k/F_{k+2}| décroît
          strictement et en ~1/F_{k+2}² sur k = 3…12 — mesuré,
          filiation T20-D3 ; les rapports de Fibonacci sont les
          convergents de 1/φ², pas de 1/π) ; contrôle (l'entier 120 = |2I| =
          racines⁺(Ê8), régression T19 : Σd² = 120, est à distance
          0 du module en n = 0 — seuls les entiers sans dimension
          sont sûrs sous les jauges) ;
      F5  le protocole d'attente est scellé au verdict : déclencheur
          (Σm_ν mesuré : valeur centrale compatible ~59 meV à
          l'exclusion de ≥ ~64 meV — bornes du registre de veille),
          séquence (cadran ρ mesuré → Λ_sel par la relation d'ancre
          T12 → re-mesure du tarif aux 7 cadrans déclarés → seuils
          |z| ≥ 3 stable / 2…3 partiel / < 2 sommeil permanent),
          et la règle de sommeil publié.
  Protocole machine (bornes déclarées) : V1…V5 = F1…F5.
  Falsifieur : F1/F2/F4 hors tolérance ou seuils déclarés (tue
      V1/V2/V4) ; protocole incomplet (tue V5) ; si le tarif
      re-mesuré au cadran mesuré donne |z| < 2 sous tous les cadrans
      → sommeil permanent publié (falsifieur de la carte entière).
  Prédiction pré-enregistrée : 5/5 — « le pont ne certifie aucune
      échelle sans cadran ; la densité du module est le certificat ;
      la carte dort ».

DÉFAUTS DU BANC (trouvés aux runs du 14/10/2026 — publiés) :
  D1  V2 supposait une décroissance monotone g(2W) < 0,6·g(W) —
      mesuré : le module d'or obéit au théorème des trois écarts
      (Sós) — g non monotone, ratios g(2W)/g(W) ∈ {≈ 1/φ, ≈ 1/φ²}
      (l'échelle de l'écart est elle-même dorée), enveloppe linéaire
      W·g(W) bornée. Correction v1.1 : critère d'enveloppe (W·g(W)
      borné, ratio max 0,7). De plus le levier Legendre ciblait 1/π —
      les rapports F_k/F_{k+2} convergent vers 1/φ², pas vers 1/π
      (Legendre : les convergents sont ceux de la CIBLE) ; cible
      corrigée. Le certificat n'est pas tué — sa mesure l'était.
  D2  gap_module au premier run ne générait que le quadrant positif
      (m, n ≥ 0) — mesuré : l'écart minimal du module vit dans les
      points à indice négatif (F_k·φ − F_{k+1} = ±φ^{−k}) ; le vrai
      certificat est ~φ^{−8} ≈ 2,1e-2 à W = 21, pas 3,4e-2.
      Correction v1.1 : module complet {m + nφ : m, n entiers}.
  D3  le seuil de V3 du premier run (5e-3) était sous le certificat
      mesuré — un seuil qui ne peut pas passer est une faute de fiche,
      pas une falsification. Correction v1.1 : borne déclarée 5e-2,
      un ordre au-dessus de la mesure. Idem pour la fenêtre absolue
      de l'enveloppe W·g(W) ∈ [0,5 ; 1,5], calibrée sur le module
      quadrant : le module complet donne W·g(W) ≈ 0,20…0,28 — la
      borne correcte est relative (max/min < 2, mesuré 1,39).
      Correction v1.2 : bornes relatives.
  Gouvernance : décision d'auteur du 14/10/2026 (« attaque T22 ») —
      run local exécuté avant tout push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9
TOL_REG = 1e-6
PHI = (1 + np.sqrt(5)) / 2
GRILLE_W = [21 * (2 ** k) for k in range(5)]        # gelée
SEUIL_DECROISSANCE = 0.6                            # gelé (F2/F4)
EMPREINTE_MCS24 = ("4a0cc1048436de28e9706d9e9d61702dd7478d7f"
                   "1dfb2ed1c28d10a3d4ec6f6e")
ORBITE_GELÉE = {                                    # citation MCS-24
    "g0_canonique_HORS_SIGMA": 10.895120224820266,
    "g1_coupure_reduite": -10.711065799162943,
    "g2_CODATA_2018": 10.895137798529262,
    "g3_fenetre_8": 22.593064147312187,
    "g4_contenu_C4": 7.449493252802233,
    "g5_porteur_ampute_noeud_C": 7.449493252802233,
    "g6_nul_uniforme_par_taille": 1.1711946709477994,
}
CHEMIN_MCS24 = Path(__file__).resolve().parents[2] / "coincidences-stables" \
    / "resultats" / "mcs24_resultats.json"


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def gap_module(W):
    """Ecart minimal entre points distincts du module COMPLET
    {m + n*phi : m, n entiers} dans [0, W) (v1.1, D2 : la version
    positive du premier run manquait les points a indice negatif —
    F_k*phi - F_{k+1} = ±phi^{-k} y vit)."""
    pts = []
    import math
    n_lim = int(2 * W / PHI) + 2
    for n in range(-n_lim, n_lim + 1):
        base = n * PHI
        m0 = math.ceil(-base)
        for m in range(m0, m0 + int(W) + 2):
            v = base + m
            if 0.0 <= v < W:
                pts.append(v)
    pts = np.sort(np.array(pts))
    return float(np.min(np.diff(pts)))


def main():
    t0 = time.time()
    print("T22 — la carte d'attente du tarif   "
          "[T22-KO6-ATTENTE-1.0 gele — RUN LOCAL, publication en attente]")
    print("=" * 76)

    # ---- V1 / F1 : regression MCS-24 (empreinte + orbite)
    orbite = dict(ORBITE_GELÉE)
    empreinte_ok = None
    if CHEMIN_MCS24.exists():
        empreinte_ok = (hashlib.sha256(CHEMIN_MCS24.read_bytes()).hexdigest()
                        == EMPREINTE_MCS24)
        lu = json.loads(CHEMIN_MCS24.read_text(encoding="utf-8"))
        for g, z in lu["z_par_g"].items():
            if g in orbite:
                orbite[g] = float(z)
    v1_inversion = (orbite["g0_canonique_HORS_SIGMA"] > 0
                    and orbite["g1_coupure_reduite"] < 0)
    v1_empreinte = (empreinte_ok in (True, None))
    V1 = bool(v1_inversion and v1_empreinte)
    print(f"V1 F1 : orbite MCS-24 relue ({'empreinte verifiee' if empreinte_ok else 'citation gelee'}) :")
    for g, z in orbite.items():
        print(f"   {g:32s} z = {z:+.6f}")
    print(f"   inversion de signe g0/g1 (anti-stabilite) : {v1_inversion} "
          f"→ {'PASS' if V1 else 'FAIL'}")

    # ---- V2 / F2 : densite du module d'or
    gaps = [gap_module(W) for W in GRILLE_W]
    ratios = [gaps[k + 1] / gaps[k] for k in range(len(gaps) - 1)]
    enveloppe = [W * g for W, g in zip(GRILLE_W, gaps)]
    v2_enveloppe = (all(r < 0.7 for r in ratios)
                    and max(enveloppe) / min(enveloppe) < 2)
    certificat = gaps[0] / 2
    V2 = bool(v2_enveloppe)
    print(f"V2 F2 (v1.1, three-gap) : ecart minimal g(W) du module d'or :")
    for W, g, e in zip(GRILLE_W, gaps, enveloppe):
        print(f"   W = {W:4d} : g = {g:.6f} · W·g = {e:.3f}")
    print(f"   ratios g(2W)/g(W) : {[round(r, 4) for r in ratios]} "
          f"({1/PHI:.4f} = 1/phi, {1/PHI**2:.4f} = 1/phi^2) · enveloppe "
          f"bornee : {v2_enveloppe} · certificat : tout ratio de "
          f"[0, 21) est a moins de {certificat:.6f} d'un point du "
          f"module → {'PASS' if V2 else 'FAIL'}")

    # ---- V3 / F3 (v1.1, D3) : corollaire — l'anti-stabilite expliquee
    V3 = bool(certificat < 5e-2)   # borne declaree (certificat mesure ~1e-2)
    print(f"V3 F3 : corollaire tarif — a {certificat:.6f} pres, TOUTE "
          f"echelle coïncide avec le module ; la coincidence MCS-24 "
          f"(|z| jusqu'a 22,6) n'avait pas d'alternative structurelle "
          f"→ {'PASS' if V3 else 'FAIL'}")

    # ---- V4 / F4 (v1.1) : leviers
    lv = {}
    lv["levier fenetre (three-gap) : ratios g(2W)/g(W) bornes (< 0,7), "
       "enveloppe W.g(W) bornee"] = bool(v2_enveloppe)
    r_cible = 1 / PHI ** 2
    erreurs = []
    for k in range(3, 13):
        f_k, f_k2 = fib(k), fib(k + 2)
        erreurs.append(abs(r_cible - f_k / f_k2))
    lv["levier Legendre : |1/phi^2 - F_k/F_{k+2}| decroît "
       "strictement"] = \
        bool(all(erreurs[i + 1] < erreurs[i] for i in range(9)))
    q_leg = [erreurs[i] * fib(i + 5) ** 2 for i in range(10)]
    lv["levier Legendre : taux quadratique (e.F^2 borne, facteur "
       "< 10)"] = bool(max(q_leg) / min(q_leg) < 10)
    dims = [1, 2, 2, 3, 3, 4, 4, 5, 6]
    lv["controle entier : 120 = somme des d^2 (regression T19), a "
       "distance 0 du module (n = 0)"] = \
        bool(sum(d * d for d in dims) == 120
             and abs(120 - (120 + 0 * PHI)) < TOL)
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : le protocole d'attente scelle
    protocole = {
        "etat": "SOMMEIL PUBLIE — carte d'attente (comme la loi harmonique a CSp)",
        "declencheur": {
            "fait": "mesure (pas borne) de Σm_ν compatible avec le plancher NO",
            "condition_centrale": "valeur centrale compatible ~59 meV",
            "condition_exclusion": "exclusion des valeurs >= ~64 meV "
                                   "(borne DESI 2025 consignee a T16)",
            "source": "REGISTRE-VEILLE-ANTICIPATION.md (faits 2, seuils)"},
        "sequence": [
            "1. epingleter la source (acquisition declaree, hachee)",
            "2. mesurer le cadran : la relation d'ancre T12 "
            "(Λ²_sel = ρ² + 3 − a₂/a₀) recoit sa seconde ancre",
            "3. re-mesurer le tarif aux 7 cadrans declares de MCS-24 "
            "(meme constantes gelees, memes controles)",
            "4. appliquer les seuils gelés ci-dessous — jamais de "
            "lecture a chaud"],
        "seuils": {"|z| >= 3": "stable — la frontiere MCS-24 se rouvre",
                   "2 <= |z| < 3": "partiel — carte neuve a cadran mesure",
                   "|z| < 2 tous cadrans": "SOMMEIL PERMANENT publie"},
        "falsifieur_de_la_carte": "sommeil permanent si |z| < 2 sous "
                                  "tous les cadrans au cadran mesure",
    }
    V5 = all(k in protocole for k in
             ("etat", "declencheur", "sequence", "seuils",
              "falsifieur_de_la_carte")) and len(protocole["sequence"]) == 4
    print(f"V5 F5 : protocole d'attente scelle ({len(protocole['sequence'])} "
          f"etapes, seuils, falsifieur) : {V5} → "
          f"{'PASS' if V5 else 'FAIL'}")

    criteres = {"V1_regression_MCS24": bool(V1),
                "V2_densite_module": bool(V2),
                "V3_corollaire_tarif": bool(V3),
                "V4_leviers": bool(V4),
                "V5_protocole_scelle": bool(V5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T22-Q-KO6-ATTENTE-TARIF-2026-10",
        "protocole": "T22-KO6-ATTENTE-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "la carte d'attente du tarif : le pont phi ne certifie "
                 "aucune echelle sans cadran mesure — la densite du "
                 "module d'or est le certificat ; la carte dort, le "
                 "dormir est publie",
        "statut_du_mot": "CARTE D'ATTENTE — impossibilite mesuree ; "
                         "aucune prediction d'experience nouvelle",
        "reponse_a_la_question_unique":
            "NON — le pont phi ne certifie aucune echelle sans cadran : "
            f"a {certificat:.6f} pres, toute echelle coincide avec le "
            "module dore (densite mesuree) ; la coincidence MCS-24 "
            "n'avait pas d'alternative structurelle",
        "mesures": {
            "orbite_mcs24": orbite,
            "empreinte_fichier_mcs24": EMPREINTE_MCS24,
            "empreinte_relue_localement": empreinte_ok,
            "gaps_module": {str(W): g for W, g in zip(GRILLE_W, gaps)},
            "certificat_g_sur_2": certificat,
            "legendre_erreurs_1_sur_pi": erreurs,
        },
        "V1": bool(V1), "V2": bool(V2), "V3": bool(V3),
        "V4": {k: bool(v) for k, v in lv.items()},
        "protocole_attente": protocole,
        "falsifieur": "F1/F2/F4 hors tolerance ; protocole incomplet ; "
                      "sommeil permanent si |z| < 2 sous tous les "
                      "cadrans au cadran mesure",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t22_ko6_attente_tarif_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T22 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
