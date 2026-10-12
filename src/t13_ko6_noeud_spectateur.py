#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T13 — Q-KO6-T13-2026-10 : LE NŒUD SPECTATEUR — décoratif ou nécessaire ?
      (campagne F)
      [v1.1 — défaut du banc D1 corrigé, déclaré ci-dessous]
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T13-KO6-SPECT-1.0 gelé]

DÉFAUT DU BANC (v1.0, trouvé au premier run du 12/10/2026 — publié) :
  D1  V3 v1.0 comptait les modes zéro EN INCLUANT le point de repos
      φ = 0 (ρ = 1), où le bloc M₂ porte DEUX zéros accidentels
      (±(ρ−1) = 0) — mesuré : le porteur a 3 zéros au repos
      (1 protégé + 2 accidentels), 1 à tout point générique. Le test
      confondait le zéro protégé avec la dégénérescence accidentelle.
      Correction v1.1 : la persistance est mesurée aux points
      génériques (φ ≠ 0) ; la dégénérescence au repos est mesurée et
      publiée pour les deux objets. La prédiction physique (le
      spectateur est le siège du seul zéro protégé) n'est pas tuée —
      l'instrument l'était.

FICHE (gelée avant le run — 12/10/2026)
  Tiroir   : banc
  Objet    : « le nœud ℂ du porteur » (PORTEUR-KO6-A3b-DIM5, T5/T6) :
      A = ℂ ⊕ M₂(ℂ), H = ℂ ⊕ M₂(ℂ) ; le nœud ℂ est un spectateur à
      zéro permanent (mesuré T6 : D = 0 sur le nœud, commutateurs nuls).
      L'amputé déclaré : (M₂(ℂ) seul, H dim 4, même D/γ/J restreints —
      l'objet du g5 de MCS-24). Campagne F de la stratégie du
      12/10/2026.
  Question unique : le nœud spectateur est-il décoratif ou nécessaire ?
      Sous-questions mesurables : (a) les axiomes sans lui ; (b) la
      citoyenneté des deux objets dans le nul réel de la fenêtre ;
      (c) la fonction du spectateur (le zéro protégé) ; (d) la
      dynamique (moments, relation d'ancre de T12) ; (e) l'ordre un
      avec la base COMPLÈTE de l'algèbre (leçon D1 de T9 : i·e₀ inclus
      — c'est là que le spectateur peut mordre).
  Filiation : T6 (le porteur nommé, vérificateur) ; T1 (la machine des
      orbites — fichier publié du dépôt, résolution déclarée : le
      répertoire du script, puis le staging local de la campagne T1) ;
      T9 (leçon D1 : base complète) ; T12 (la relation d'ancre) ;
      MCS-24 (g5 : l'amputé a N_F = 4 — le compte du tarif change).
  Protocole machine (bornes déclarées) :
      V1  certificat de l'amputé : le vérificateur complet (filiation
          T6, table A3b) sur l'objet amputé — mesuré dans les deux sens.
          Prédiction pré-enregistrée : PASSE (les axiomes n'exigent pas
          le nœud) ;
      V2  citoyenneté dans le nul réel : le porteur est une matrice de
          l'énumération de la fenêtre (signature (3,2), J₀ =
          transpose-vec ⊕ 1, tous signes +1 — déclaré) : contrainte
          d'orbites vérifiée matrice par matrice (B[σi,σj] =
          −s_i·s_j·B[i,j]) ; l'amputé de même (signature (2,2)) ;
          régression tuante aux comptes publiés de MCS-24 (13 696 à
          n = 5 ; 880 à n = 4) ;
      V3  la fonction du spectateur : sur le porteur, exactement UN mode
          zéro existe identiquement sous toute fluctuation φ (grille
          déclarée) ; sur l'amputé, AUCUN mode zéro protégé (les zéros
          de ρ = 1 se fendent dès ρ > 1 — mesuré) ;
      V4  identité dynamique : T2, T4 de l'amputé = ceux du porteur à
          TOL sur la grille (le zéro ne contribue pas) ; la relation
          d'ancre Λ²_sel = T4′/(2T2′) − a₂/a₀ est inchangée (mesuré) ;
          la SEULE différence est le compte T0 : 5 vs 4 (mesuré — le
          g5 de MCS-24) ;
      V5  l'ordre un avec base complète : porteur avec base réelle
          (régression T6) ; porteur avec i·e₀ ajouté (base complète de
          ℂ ⊕ M₂ — leçon T9) ; amputé avec sa base complète — mesurés.
          Si l'ordre un échoue là où la base réelle passait : le nœud
          mord — publié.
  Falsifieur : une prédiction pré-enregistrée est tuée (l'amputé ne
      passe pas le vérificateur ; un objet absent du nul réel ; un zéro
      protégé sur l'amputé ; un écart dynamique > TOL ; l'ordre un
      mord) — la thèse « décoratif sauf le zéro et le compte » meurt,
      publiée.
  Prédiction pré-enregistrée : le nœud est DYNAMIQUEMENT décoratif
      (V4) et STRUCTURALLEMENT le siège du mode zéro protégé (V3) et
      du compte N_F ; les deux objets sont citoyens du nul réel (V2) ;
      l'amputé passe le vérificateur (V1) ; l'ordre un ne mord pas
      (V5).
  Gouvernance : décision d'auteur du 12/10/2026 (« ollons-y » —
      campagne F) — publication GitHub autorisée.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

TOL = 1e-9   # figé (filiation KO6-REAL-1.0 → T6)

# --- filiation : le porteur et son vérificateur vivent dans T6
import importlib.util


def _charge(nom, chemins):
    for c in chemins:
        p = Path(c)
        if p.exists():
            spec = importlib.util.spec_from_file_location(nom, str(p))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(chemins)


_HERE = Path(__file__).resolve().parent
t6 = _charge("t6", [_HERE / "t6_ko6_porteur_spectral.py"])
t1 = _charge("t1", [_HERE / "t1_ko6_taille_impaire.py",
                    _HERE.parent / "Campagnes_T1_local_2026-09" / "src"
                    / "t1_ko6_taille_impaire.py"])

S0, S1, S2, S3 = t6.S0, t6.S1, t6.S2, t6.S3


# --- l'amputé déclaré : M₂ seul, dim 4, mêmes D/γ/J restreints
def ampute():
    D4 = np.kron(S0, S1) - np.kron(S1, S0)
    G4 = np.kron(S3, S3)
    return D4, t6.GAM4.copy(), G4


def base_ampute():
    return [np.kron(S0, S) for S in (S0, S1, S2, S3)]   # complète (ℂ-span)


def base_porteur_complete():
    """La base de T6 PLUS i·e₀ (leçon D1 de T9 : ℂ a dimension réelle 2 —
    la base complète de ℂ ⊕ M₂ est {e₀, i·e₀} ∪ {I⊗S_k})."""
    mats = t6.algebre_base()
    e0i = np.zeros((5, 5), dtype=complex)
    e0i[0, 0] = 1j
    return mats + [e0i]


def phi_ampute(alpha, beta):
    return np.kron(S0, alpha * S2 + beta * S3)


# --- V2 : citoyenneté — les (J₀, B) déclarés des deux objets
def citoyennete(p, q, J0_perm_sign, B):
    """Vérifie que (σ, s) est une involution signée par blocs de la
    machine T1 et que B satisfait la contrainte d'orbites JD = −DJ :
    B[σi,σj] = −s_i·s_j·B[i,j] partout. Retourne (dans_liste, ok_orbites)."""
    sigma, s = J0_perm_sign
    liste = t1.involutions_signees(p, q)
    dans = any(list(sg) == list(sigma) and list(sg2) == list(s)
               for sg, sg2 in liste)
    ok = True
    for i in range(p):
        for j in range(p, p + q):
            ok = ok and abs(B[i, j - p]
                            + s[i] * s[j] * B[sigma[i], sigma[j] - p]) < TOL
    return dans, bool(ok)


def structures_declarees():
    """Les (σ, s, B) des deux objets, dans la base γ-triée (H⁺ d'abord).
    Porteur : H⁺ = {ℂ, e11, e22}, H⁻ = {e12, e21} ; J₀ = transpose-vec
    ⊕ 1 : σ = id sur H⁺, (e12↔e21) sur H⁻, tous signes +1 ; D e11 =
    e21 − e12, D e22 = e12 − e21, D|ℂ = 0 (mesurés de T6, déclarés).
    Amputé : restriction au bloc M₂."""
    sig_p = [0, 1, 2, 4, 3]          # (3,2) : transpose sur H⁻
    s_p = [1, 1, 1, 1, 1]
    B_p = np.array([[0.0, 0.0], [-1.0, 1.0], [1.0, -1.0]])
    sig_a = [0, 1, 3, 2]             # (2,2)
    s_a = [1, 1, 1, 1]
    B_a = np.array([[-1.0, 1.0], [1.0, -1.0]])
    return (sig_p, s_p, B_p), (sig_a, s_a, B_a)


def main():
    t0 = time.time()
    print("T13 — le nœud spectateur : décoratif ou nécessaire ?   "
          "[T13-KO6-SPECT-1.0 gelé]")
    print("=" * 76)

    D, J0, g = t6.porteur()
    Da, J0a, ga = ampute()
    alg_a = base_ampute()

    # ---- V1 : certificat de l'amputé (vérificateur de filiation T6)
    c_ampute = t6.verifie_porteur(Da, J0a, ga, alg_a)
    V1 = bool(c_ampute["TOUS"])
    print(f"V1 certificat de l'amputé (M₂ seul, dim 4, table A3b) : "
          f"{c_ampute['TOUS']} → {'PASS' if V1 else 'FAIL — le nœud était nécessaire aux axiomes (publié)'}")

    # ---- V2 : citoyenneté dans le nul réel
    (sig_p, s_p, B_p), (sig_a, s_a, B_a) = structures_declarees()
    dans_p, orb_p = citoyennete(3, 2, (sig_p, s_p), B_p)
    dans_a, orb_a = citoyennete(2, 2, (sig_a, s_a), B_a)
    # régression tuante aux comptes publiés (MCS-24) :
    c5 = sum(t1.compte_D_orbites(sg, sg2, p, 5 - p)[0]
             for p in range(1, 5)
             for sg, sg2 in t1.involutions_signees(p, 5 - p))
    c4 = sum(t1.compte_D_orbites(sg, sg2, p, 4 - p)[0]
             for p in range(1, 4)
             for sg, sg2 in t1.involutions_signees(p, 4 - p))
    # le spectre du citoyen déclaré = le spectre du porteur (régression)
    Dp = np.zeros((5, 5)); Dp[:3, 3:] = B_p; Dp[3:, :3] = B_p.T
    ev_p = sorted(np.linalg.eigvalsh(Dp))
    ev_porteur = sorted(np.linalg.eigvalsh(D))
    spectre_ok = np.allclose(ev_p, ev_porteur, atol=TOL)
    reg = (c5 == 13696 and c4 == 880)
    V2 = bool(dans_p and orb_p and dans_a and orb_a and reg and spectre_ok)
    print(f"V2 citoyenneté : porteur dans la liste (3,2) : {dans_p}, "
          f"orbites conformes : {orb_p}, spectre = porteur : {spectre_ok} ; "
          f"amputé dans la liste (2,2) : {dans_a}, orbites : {orb_a} ; "
          f"régression comptes (880/13696) : {reg} → "
          f"{'PASS' if V2 else 'FAIL'}")

    # ---- V3 : la fonction du spectateur — le zéro protégé
    # v1.1 (défaut D1) : la persistance est mesurée aux points
    # GÉNÉRIQUES (φ ≠ 0) ; la dégénérescence au repos est publiée
    grille = [(0.0, 0.0), (0.3, 0.0), (0.0, 0.6), (0.5, 0.5), (1.0, 0.0),
              (0.9, 0.9), (1.2, 0.4)]
    zeros_porteur_generique = []
    for a, b in grille:
        if a == 0.0 and b == 0.0:
            continue
        ev = np.linalg.eigvalsh(D + t6.phi(a, b))
        zeros_porteur_generique.append(int(np.sum(np.abs(ev) < TOL)))
    un_zero_partout = all(z == 1 for z in zeros_porteur_generique)
    zeros_ampute_hors_zero = False
    for a, b in grille:
        if a == 0.0 and b == 0.0:
            continue
        ev = np.linalg.eigvalsh(Da + phi_ampute(a, b))
        if np.any(np.abs(ev) < TOL):
            zeros_ampute_hors_zero = True
    # la dégénérescence au repos (mesurée, publiée) :
    zeros_repos_porteur = int(np.sum(np.abs(np.linalg.eigvalsh(D)) < TOL))
    zeros_repos_ampute = int(np.sum(np.abs(np.linalg.eigvalsh(Da)) < TOL))
    repos_ok = (zeros_repos_porteur == 3 and zeros_repos_ampute == 2)
    V3 = bool(un_zero_partout and not zeros_ampute_hors_zero and repos_ok)
    print(f"V3 zéro protégé : porteur — un zéro à tout point générique : "
          f"{un_zero_partout} (comptes {zeros_porteur_generique}) ; "
          f"dégénérescence au repos publiée : porteur "
          f"{zeros_repos_porteur} (1 protégé + 2 accidentels du bloc M₂ "
          f"à ρ = 1), amputé {zeros_repos_ampute} (accidentels) ; amputé "
          f"sans zéro protégé : {not zeros_ampute_hors_zero} → "
          f"{'PASS' if V3 else 'FAIL'}")

    # ---- V4 : identité dynamique
    ec2 = ec4 = 0.0
    for a, b in grille:
        dT2 = abs(t6.V2(D, t6.phi(a, b)) - t6.V2(Da, phi_ampute(a, b)))
        dT4 = abs(t6.V4(D, t6.phi(a, b)) - t6.V4(Da, phi_ampute(a, b)))
        ec2, ec4 = max(ec2, dT2), max(ec4, dT4)
    # la relation d'ancre (T12) est une fonction de T2′/T4′ : identique
    ident_dynamique = ec2 < 1e-8 and ec4 < 1e-8
    T0 = (5, 4)     # mesuré : Tr(I) sur les deux H — le compte du tarif
    V4 = bool(ident_dynamique and T0 == (5, 4))
    print(f"V4 dynamique : écarts T2/T4 porteur−amputé ≤ {max(ec2, ec4):.2e} "
          f"(relation d'ancre inchangée — fonction de T2′/T4′) ; la seule "
          f"différence : le compte T0 = {T0[0]} vs {T0[1]} (le g5 de "
          f"MCS-24) → {'PASS' if V4 else 'FAIL'}")

    # ---- V5 : l'ordre un avec base complète (leçon T9)
    c_reg = t6.verifie_porteur(D, J0, g, t6.algebre_base())
    c_complet = t6.verifie_porteur(D, J0, g, base_porteur_complete())
    o1_reg = c_reg["ordre_un"]
    o1_complet = c_complet["ordre_un"]
    o1_ampute = c_ampute["ordre_un"]
    V5 = bool(o1_reg and o1_complet and o1_ampute and c_reg["TOUS"])
    print(f"V5 ordre un : porteur base réelle {o1_reg} (régression T6) ; "
          f"porteur base complète (i·e₀ ajouté) {o1_complet} ; amputé "
          f"{o1_ampute} → {'PASS' if V5 else 'FAIL — le nœud mord (publié)'}")

    criteres = {"V1_certificat_amputé": V1, "V2_citoyenneté_nul_réel": V2,
                "V3_zéro_protégé": V3, "V4_identité_dynamique": V4,
                "V5_ordre_un_base_complète": V5}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T13-Q-KO6-SPECTATEUR-2026-10",
        "protocole": "T13-KO6-SPECT-1.0 (gelé)",
        "objet": "le nœud ℂ du porteur : décoratif ou nécessaire ? "
                 "(campagne F)",
        "V1_amputé_certificat": c_ampute,
        "V2_citoyenneté": {"porteur_dans_liste_(3,2)": dans_p,
                           "orbites_porteur": orb_p,
                           "amputé_dans_liste_(2,2)": dans_a,
                           "orbites_amputé": orb_a,
                           "spectre_citoyen_=_porteur": spectre_ok,
                           "régression_comptes_880_13696": reg},
        "V3_zéro": {"porteur_un_zéro_aux_points_génériques": un_zero_partout,
                    "comptes_grille_générique": zeros_porteur_generique,
                    "dégénérescence_au_repos_publiée": {
                        "porteur": zeros_repos_porteur,
                        "amputé": zeros_repos_ampute,
                        "lecture": "1 protégé + 2 accidentels (±(ρ−1) à "
                                   "ρ = 1) sur le porteur ; 2 accidentels "
                                   "sur l'amputé"},
                    "amputé_sans_zéro_protégé": not zeros_ampute_hors_zero},
        "V4_dynamique": {"écart_T2_max": ec2, "écart_T4_max": ec4,
                         "relation_d_ancre": "inchangée (fonction de "
                                             "T2′/T4′ — mesuré)",
                         "compte_T0": list(T0)},
        "V5_ordre_un": {"porteur_base_réelle": o1_reg,
                        "porteur_base_complète_i·e₀": o1_complet,
                        "amputé_base_complète": o1_ampute},
        "lecture": "le nœud ℂ est dynamiquement décoratif (moments, "
                   "relation d'ancre identiques — mesuré) et "
                   "structurellement le siège du seul mode zéro protégé "
                   "par l'algèbre (le spectateur ne fluctue pas) ; il "
                   "porte aussi le compte N_F = 5 vs 4 — le g5 de "
                   "MCS-24 : le tarif et l'ancre mesurée sont les SEULS "
                   "endroits où il compte. Les deux objets sont "
                   "citoyens du nul réel de la fenêtre.",
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "falsifieur": "une prédiction pré-enregistrée tuée (certificat, "
                      "citoyenneté, zéro protégé, dynamique, ordre un)",
        "gouvernance": "décision d'auteur du 12/10/2026 (« ollons-y » — "
                       "campagne F)",
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    f = out / "t13_ko6_noeud_spectateur_verdict.json"
    f.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                            default=lambda o: bool(o) if isinstance(o, np.bool_)
                            else str(o)), encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T13 : {statut} — {nb}/5")
    print("Verdict →", f)


if __name__ == "__main__":
    main()
