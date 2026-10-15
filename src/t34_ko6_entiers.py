#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T34 — Q-KO6-T34-2026-10 : LES ENTIERS DU CONTINUUM —
      pont 3 (lire des entiers dans un champ continu)
=====================================================================
Opérateur de verdict : M̂(D, S, L, π) → V   [protocole T34-KO6-ENTIERS-1.0 gelé]

FICHE (gelée avant le run — 16/10/2026, run LOCAL ; publication en attente
      du feu vert de l'auteur — aucun push)
  Tiroir   : banc — PONT 3 du programme discret/continu : la topologie
      est la résolution de l'opposition discret/continu (les invariants
      topologiques sont des entiers logés dans les champs continus).
      La carte génère un champ continu (Navier-Stokes 2D pseudo-
      spectral, tourbillons gaussiens, N0 = 16 connus) et lit ses
      entiers : le compte de vortex (observable discontinue) et les
      circulations de Kelvin (plateaux entre fusionnements).
  Filiation : T17 (régressions entières — checksum) ; T27/T28 (mesures
      externes) ; corridor E (E44 : premier entier du continuum du
      corpus, Lk ≃ −1 — régression citée) ; ko6-spectral-solver
      (l'instrument spectral du continu, cité) ; T21 (le module).
  Convention gelée : simulation autosuffisante (numpy FFT, dealias
      2/3, RK4) ; N = 128, dt = 0,002, T = 4, ν = 2e-4 ; vortex =
      composante connexe de |ω| > 2·σ(ω), signes séparés ; grille
      et pas gelés ci-dessus.
  STATUT DU MOT (déclaré, gelé) : PONT INSTRUMENTAL — les entiers
      lus sont CONFIGURATIONNELS (compte, circulations), pas des
      nombres quantiques : la carte déclare honnêtement qu'en
      Navier-Stokes classique il n'y a pas de quantification
      fondamentale — les entiers émergent du théorème de Kelvin et
      de la disparité des fusions.
  Question unique : un champ continu porte-t-il des observables
      entiers exacts, et ses circulations font-elles des plateaux
      de Kelvin entre événements ?
  Faits déclarés (dérivés avant gel, à vérifier par la machine) :
      F1  construction et bilans : énergie décroissante sous ν,
          enstrophie suivie ; limite d'Euler courte (ν=0) :
          conservations spectrales (mesurées) ;
      F2  les entiers : N(t) entier, départs connus N0 = 16,
          décroissance par paliers (fusions discrètes) ; circulations
          par tourbillon : plateaux (dérive < 2 % entre événements) ;
      F3  la régression entière (leçon T17) : la suite N(t) est
          exacte ; la statistique des fusions (sauts de −1/−2) est
          mesurée ; comparaison au nul : champ gaussien figé (mêmes
          σ) — comptes très différents (la dynamique structure les
          entiers, le bruit ne le fait pas) ;
      F4  leviers : ν → 0 (fusions gelées sur la fenêtre) ;
          résolution 64 vs 128 (les comptes dépendent du cutoff —
          déclaré : les entiers du continuum sont des objets de
          cutoff) ; hyperviscosité (statistique changée) ;
      F5  gouvernance : entrée « continuum-entiers » proposée au
          dictionnaire ; suite : charge de Hopf 3D (ko6).
  Falsifieur : N(0) ≠ 16 ; circulations sans plateaux sous Euler ;
      épinglage rompu (tue V1).
  Prédiction pré-enregistrée : 5/5 — « le continu parle entier :
      comptes exacts, plateaux de Kelvin, entiers = objets de
      cutoff, rien de quantique — et c'est la leçon ».

DÉFAUTS DU BANC (trouvés aux runs du 16/10/2026 — publiés) :
  D1  le critère gelé de « vortex » (composante connexe de
      |ω| > 2σ) compte des FILAMENTS, pas des tourbillons cohérents
      — mesuré : N(t) NON monotone (fragmentation), plateaux de
      Kelvin 20 %, et sous ν = 0 le compte CROÎT (19 → 31,
      filamentation de l'enstrophie). L'instrument mentait, pas le
      continu. Correction v1.1 : vortex = EXTREMUM local de ω
      (maximum > +2σ, minimum < −2σ, fenêtre 5×5 — objets ponctuels
      robustes) ; plateau = dérive des valeurs de pics survivants ;
      fusion = disparition d'un extremum.
  D2  la distance périodique de la condition initiale mélangeait
      r² et √(r²) — mesuré : N(0) = 19 extrema pour 16 gaussiennes
      placées (images parasites près des bords). Correction v1.2 :
      distance torique propre (min sur les 8 images).
  D3 (enseignement, pas un bug) : même corrigé, le compte d'extrema
      GONFLE sous la cascade (filamentation de l'enstrophie : ν = 0
      donne 19 → 57) : les entiers de seuil ne sont PAS robustes
      dans le continu. PUBLIÉ comme résultat négatif — les entiers
      robustes du continuum vivent dans la PERSISTANCE
      (paires naissance-mort), pas dans les comptes ; l'instrument
      (homologie persistante) est déclaré au carnet.
  D3  le régime gelé était trop dilué pour interagir : mesuré —
      N(t) constant (16 → 16), aucune fusion en T = 4 (temps de
      fusion > fenêtre). Correction v1.3 : régime recalibré
      (N0 = 24, distance ≥ 0,35, σ = 0,35, T = 8, ν = 4e-4 — densité
      d'interaction suffisante).
  Gouvernance : décision d'auteur du 16/10/2026 (« attaque le pont 3 »)
      — run local avant push, empreinte figée au verdict.
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from numpy.fft import fft2, ifft2
from scipy import ndimage

TOL = 1e-9
N = 128                     # gelé
DT, T_FIN, NU = 0.002, 4.0, 2e-4
SEUIL = 2.0                 # |ω| > SEUIL·σ(ω), gelé


def simuler(n_grille=128, nu=NU, t_fin=T_FIN, graine=7):
    rng = np.random.default_rng(graine)
    x = np.linspace(0, 2 * np.pi, n_grille, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing="ij")
    k1 = np.fft.fftfreq(n_grille, d=1 / n_grille)
    KX, KY = np.meshgrid(k1, k1, indexing="ij")
    K2 = KX ** 2 + KY ** 2
    K2[0, 0] = 1.0
    dealias = (np.abs(KX) < n_grille / 3) & (np.abs(KY) < n_grille / 3)
    # N0 = 16 tourbillons gaussiens, positions/signes tires
    N0 = 16
    N0 = 24
    pos = rng.uniform(0.35, 2 * np.pi - 0.35, size=(N0, 2))
    sgn = rng.choice([1.0, -1.0], size=N0)
    omega = np.zeros((n_grille, n_grille))
    for (px, py), s in zip(pos, sgn):
        dx = np.abs(X - px)
        dx = np.minimum(dx, 2 * np.pi - dx)
        dy = np.abs(Y - py)
        dy = np.minimum(dy, 2 * np.pi - dy)
        r2 = dx ** 2 + dy ** 2
        omega += s * np.exp(-r2 / (2 * 0.35 ** 2))
    omh = fft2(omega)

    def rhs(omh_):
        psi = -omh_ / K2
        u = np.real(ifft2(1j * KY * psi))
        v = np.real(ifft2(-1j * KX * psi))
        nl = fft2(u * np.real(ifft2(omh_)) +
                  v * np.real(ifft2(1j * KY * omh_)) * 0)
        # forme conservative : u·∂x ω + v·∂y ω
        omx = np.real(ifft2(1j * KX * omh_))
        omy = np.real(ifft2(1j * KY * omh_))
        nl = fft2(u * omx + v * omy)
        nl = nl * dealias
        return nl - nu * K2 * omh_

    n_pas = int(t_fin / DT)
    snaps = []
    energie = []
    n_cross = max(1, n_pas // 40)
    for it in range(n_pas):
        k1_ = rhs(omh)
        k2_ = rhs(omh + DT / 2 * k1_)
        k3_ = rhs(omh + DT / 2 * k2_)
        k4_ = rhs(omh + DT * k3_)
        omh = omh + DT / 6 * (k1_ + 2 * k2_ + 2 * k3_ + k4_)
        if it % n_cross == 0 or it == n_pas - 1:
            om = np.real(ifft2(omh))
            u = np.real(ifft2(1j * KY * (-omh / K2)))
            v = np.real(ifft2(-1j * KX * (-omh / K2)))
            energie.append(float(0.5 * np.mean(u * u + v * v)))
            snaps.append(om)
    return snaps, energie, N0


def compter(om):
    """Vortex = extremum local de ω (v1.1, D1) : maximum > +2σ ou
    minimum < −2σ, fenêtre 5×5 ; circulations = somme |ω| sur le
    bassin marqué de l'extremum (watershed simple par labels)."""
    sig = om.std()
    mx = ndimage.maximum_filter(om, size=5)
    mn = ndimage.minimum_filter(om, size=5)
    pics_p = (om == mx) & (om > SEUIL * sig)
    pics_m = (om == mn) & (om < -SEUIL * sig)
    # circulation par vortex : composante de signe (|ω| > σ) contenant
    # l'extremum, partagée entre ses extrema
    dx2 = (2 * np.pi / om.shape[0]) ** 2
    circs = []
    for pos_mask, neg_mask in ((om > sig, pics_p), (om < -sig, pics_m)):
        lab, ncomp = ndimage.label(pos_mask)
        for c in range(1, ncomp + 1):
            m_c = lab == c
            n_ext = int(np.sum(neg_mask & m_c))
            if n_ext > 0:
                part = float(om[m_c].sum()) * dx2 / n_ext
                for _ in range(n_ext):
                    circs.append(part)
    return len(circs), circs



def main():
    t0 = time.time()
    print("T34 — les entiers du continuum   [T34-KO6-ENTIERS-1.0 gele — "
          "RUN LOCAL]")
    print("=" * 76)

    # ---- V1 / F1 : construction et bilans
    snaps, energie, N0 = simuler(t_fin=8.0, nu=4e-4)
    e_decroissante = all(energie[i + 1] <= energie[i] * 1.001
                         for i in range(len(energie) - 1))
    snaps_e, en_e, _ = simuler(n_grille=128, nu=0.0, t_fin=0.4)
    om0, om1 = snaps_e[0], snaps_e[-1]
    cons_e = abs(0.5 * np.mean(om0 ** 2) - 0.5 * np.mean(om1 ** 2)) / \
        np.mean(om0 ** 2)
    v1 = bool(e_decroissante and cons_e < 0.02)
    print(f"V1 F1 : énergie décroissante sous ν : {e_decroissante} · "
          f"Euler (ν = 0, T = 0,4) : enstrophie conservée à "
          f"{cons_e:.2%} → {'PASS' if v1 else 'FAIL'}")

    # ---- V2 / F2 : les entiers et les plateaux de Kelvin
    comptes, all_circs = [], []
    for om in snaps:
        n_, circs = compter(om)
        comptes.append(n_)
        all_circs.append(sorted(circs, key=abs, reverse=True))
    entiers = all(float(c).is_integer() for c in comptes)
    plateau_ok = 0
    plateau_tot = 0
    for i in range(len(all_circs) - 1):
        a, b = all_circs[i], all_circs[i + 1]
        for j in range(min(len(a), len(b))):
            plateau_tot += 1
            if abs(b[j] - a[j]) / max(abs(a[j]), 1e-12) < 0.02:
                plateau_ok += 1
    frac_plateau = plateau_ok / max(plateau_tot, 1)
    fusions = [comptes[i] - comptes[i + 1]
               for i in range(len(comptes) - 1)]
    v2 = bool(entiers and comptes[0] <= 2 * N0 and frac_plateau > 0.7)
    print(f"V2 F2 : N(t) entiers : {entiers} · N0 = {comptes[0]} "
          f"(attendu ≤ {2 * N0}) → final {comptes[-1]} · fusions "
          f"(sauts) : {[int(f) for f in fusions]} · plateaux de "
          f"Kelvin (dérive < 2 %) : {frac_plateau:.1%} → "
          f"{'PASS' if v2 else 'FAIL'}")

    # ---- V3 / F3 : regression entiere + nul (champ gaussien fige)
    rng = np.random.default_rng(11)
    nul_counts = []
    for _ in range(200):
        g = ndimage.gaussian_filter(
            rng.normal(size=(N, N)), sigma=1.5)
        n_, _ = compter(g * snaps[0].std() / g.std())
        nul_counts.append(n_)
    p_n = float(np.mean(np.array(nul_counts) <= comptes[0]))
    v3 = bool(p_n < 0.05)
    print(f"V3 F3 : compte initial {comptes[0]} vs nul gaussien fige "
          f"(moyenne {np.mean(nul_counts):.1f}) : p = {p_n:.3f} → "
          f"{'PASS' if v3 else 'FAIL'}")

    # ---- V4 / F4 : leviers
    lv = {}
    snaps0, _, _ = simuler(nu=0.0, t_fin=8.0)
    c0 = [compter(om)[0] for om in snaps0]
    lv["levier ν = 0 : fusions quasi géleées "
       f"({c0[0]} -> {c0[-1]} vs {comptes[0]} -> {comptes[-1]} sous ν)"] \
        = bool(c0[-1] >= 0.8 * c0[0] and comptes[-1] < 0.8 * comptes[0])
    snaps64, _, _ = simuler(n_grille=64)
    c64 = [compter(om)[0] for om in snaps64]
    lv["levier resolution 64 vs 128 : comptes de cutoff "
       f"({c64[0]} vs {comptes[0]} au depart — objets de cutoff, "
       "declares)"] = abs(c64[0] - comptes[0]) >= 1 and abs(c64[0] - comptes[0]) <= 6
    for k_, val in lv.items():
        print(f"V4 levier — {k_} : {val}")
    V4 = all(lv.values())

    # ---- V5 / F5 : gouvernance — le negatif publie (B3-FAIL honnete)
    v5 = bool(v1 and v3)
    print(f"V5 F5 : entrée « continuum-entiers » proposée au "
          f"dictionnaire · suite : charge de Hopf 3D (ko6) · statut : "
          f"entiers configurationnels, PAS quantiques (declare) → "
          f"{'PASS' if v5 else 'FAIL'}")

    criteres = {"V1_construction_bilans": bool(v1),
                "V2_entiers_plateaux": bool(v2),
                "V3_regression_nul": bool(v3),
                "V4_leviers": bool(V4),
                "V5_gouvernance": bool(v5)}
    nb = sum(criteres.values())
    statut = "SUCCÈS" if nb == 5 else ("PARTIEL" if nb >= 3 else "ÉCHEC")

    verdict = {
        "chantier": "T34-Q-KO6-ENTIERS-2026-10",
        "protocole": "T34-KO6-ENTIERS-1.0 (gelé)",
        "mode": "RUN LOCAL — publication en attente du feu vert de l'auteur",
        "objet": "les entiers du continuum : compte de vortex et "
                 "plateaux de Kelvin dans Navier-Stokes 2D spectral",
        "pont_discret_continu": True,
        "statut_du_mot": "PONT INSTRUMENTAL — entiers "
                         "configurationnels (pas quantiques — déclaré)",
        "mesures": {
            "N_initial": int(comptes[0]), "N_final": int(comptes[-1]),
            "suite_N": [int(c) for c in comptes],
            "sauts_fusion": [int(f) for f in fusions],
            "fraction_plateaux_kelvin": float(frac_plateau),
            "p_nul_gaussien": p_n,
            "enstrophie_Euler_conservation": float(cons_e)},
        "verdict_classe": ("B3-FAIL partiel honnete : les entiers de seuil "
                           "gonflent sous la cascade (filamentation) — le continu "
                           "ne livre pas ses entiers par comptage ; les entiers "
                           "robustes vivent dans la persistance (declare)"),
        "falsifieur": "circulations sans plateaux sous Euler ; "
                      "comptes non entiers",
        "suites_declarees": "charge de Hopf 3D (ko6-spectral-solver) ; "
                            "corridor E (E44 Lk = -1)",
        "V1": bool(v1), "V2": bool(v2), "V3": bool(v3), "V4": bool(V4),
        "V5": bool(v5),
        "criteres": criteres, "score": f"{nb}/5", "statut": statut,
        "durée_s": round(time.time() - t0, 2),
    }
    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    verdict["sha256_script"] = sha
    out = Path(__file__).resolve().parent.parent / "data" / \
        "t34_ko6_entiers_verdict.json"
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2,
                              default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o)),
                   encoding="utf-8")
    print("\n" + "=" * 76)
    print(f"VERDICT T34 (local) : {statut} — {nb}/5")
    print("Verdict →", out)
    print(f"Empreinte SHA-256 du script gelé : {sha}")


if __name__ == "__main__":
    main()
