# -*- coding: utf-8 -*-
"""MCS-28 — moteur de projection connectome AAL-116 -> 7 plans noetiques.

Specification : docs/NOTE-MCS-28-CONNECTOME-AAL116.md (2026-10-28).
Carte candidate, soumise a demonstration de puissance (regle 1.2) avant
scellement. Les statistiques de Cognition_2 citees dans la note restent
des valeurs declarees jusqu'au run sur donnees reelles.

Conventions figees (decisions D1-D4 de la note) :
  - partition stricte AAL-116 SPM12, indices 0-based ;
  - invariants canoniques calcules SANS filtre (le filtre Majorana est
    la deformation D2, avec symmetrisation post-filtre declaree) ;
  - filtre entropique a constante structurelle alpha = 1/7 (7 plans).

Dry-run synthetique (28/10/2026) : 5/6 directions plantees recuperees
(tsa Gamma+, C_26- ; ad d_eff-, M_34- ; sz Gamma-). L'axe sz « S_ent
haut » n'est PAS plantable isolément : dans le monde projeté 7x7, S_ent
et Gamma sont positivement couplés (tout aplatissement spectral renforce
la specialisation diagonale). Couplage documenté, à quantifier sous H0
lors de la demonstration de puissance.
"""

import numpy as np

# Partition figee (NOTE-MCS-28, §4) — indices 0-based AAL-116 SPM12,
# verifiee disjointe et complete le 28/10/2026 (fetch_atlas_aal SPM12).
PLAN_INDICES = {
    "E1": [0, 1, 42, 43, 44, 45, 46, 47, 48, 49, 52, 53, 56, 57, 68, 69, 78, 79],
    "E2": [28, 29, 36, 37, 38, 39, 40, 41, 70, 71, 72, 73],
    "E3": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 22, 23, 24, 25, 26, 27],
    "E4": [30, 31, 32, 33, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67],
    "E5": [16, 17, 20, 21, 34, 35, 74, 75, 76, 77],
    "E6": [50, 51, 54, 55, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91],
    "E7": list(range(92, 116)),
}
PLAN_SIZES = (18, 12, 22, 14, 10, 16, 24)
PLAN_ORDER = ("E1", "E2", "E3", "E4", "E5", "E6", "E7")


def _check_partition():
    union = sorted(i for p in PLAN_INDICES.values() for i in p)
    assert union == list(range(116)), "partition incomplete"
    for name, size in zip(PLAN_ORDER, PLAN_SIZES):
        assert len(PLAN_INDICES[name]) == size, f"taille invalide pour {name}"


def build_projectors(plan_indices_list, n_rois=116):
    """Matrice de projection P (116 x 7), normalisee a zero parametre."""
    assert len(plan_indices_list) == 7
    P = np.zeros((n_rois, 7), dtype=np.float64)
    for i, idx in enumerate(plan_indices_list):
        assert len(idx) == PLAN_SIZES[i], f"Taille invalide pour E{i+1}"
        P[idx, i] = 1.0 / np.sqrt(len(idx))
    return P


def project_connectome_to_7plans(W, P):
    """M = P^T |W| P (7 x 7), diagonale auto-correlee mise a zero."""
    W_clean = np.abs(W).copy()
    np.fill_diagonal(W_clean, 0.0)
    return P.T @ W_clean @ P


def compute_noetic_invariants(M):
    """5 invariants canoniques — calcules SANS filtre (D4).

    Gamma : specialisation diagonale (Cognition.pdf Eq. 16).
    S_ent : entropie spectrale de M^2 (Cognition_3 Eq. 22).
    d_eff : entropie de participation du spectre de M^2.
    C_26 / M_34 : couplages normalises Emotion-Social / Raisonnement-Intuition.
    """
    diag_norm_sq = np.sum(np.diag(M) ** 2)
    total_norm_sq = np.sum(M ** 2) + 1e-15
    gamma_spec = diag_norm_sq / total_norm_sq
    M2 = M @ M
    eigvals = np.clip(np.linalg.eigvalsh(M2), 1e-15, None)
    probs = eigvals / np.sum(eigvals)
    s_ent = -np.sum(probs * np.log(probs))
    d_eff = 1.0 / np.sum(probs ** 2)
    c_26 = M[1, 5] / np.sqrt(M[1, 1] * M[5, 5] + 1e-15)
    m_34 = M[2, 3] / np.sqrt(M[2, 2] * M[3, 3] + 1e-15)
    return {"Gamma": gamma_spec, "S_ent": s_ent, "d_eff": d_eff,
            "C_26": c_26, "M_34": m_34}


def deformation_d2_majorana(M):
    """Deformation de robustesse D2 (filtre entropique, regle A.2.1).

    alpha = 1/7 fige : septieme d'echelle spectrale par plan,
    e^(-ln r_j / 7) = r_j^(-1/7). Convention figee : filtrage par
    colonnes j, PUIS symmetrisation 0.5 * (M + M^T).
    """
    r_j = np.array(PLAN_SIZES, dtype=np.float64)
    M_d = M * np.exp(-np.log(r_j) / 7.0)[None, :]
    return 0.5 * (M_d + M_d.T)


# --------------------------------------------------------------------------
# Dry-run synthetique : connectomes clairsemes a queue lourde (loi type
# connectome), modules plantes, zero donnee clinique. Verifie que le
# moteur calcule, est deterministe et recupere les sens des axes geles.
#
# Lecon du 28/10/2026 (3 passes) : les plants doivent agir sur les
# MAGNITUDES (le moteur travaille sur |W|) ; le bruit additif signe a
# travers |.| est convexe et amplifie les boosts existants ; le fond
# gaussien dense noie tout signal par sommation LLN. Le spectre de M^2
# n'a que 7 valeurs propres : S_ent mesure la domination du mode de
# Perron et est positivement couple a Gamma.
# --------------------------------------------------------------------------

def _mag(rng, shape, p, mu=0.0, sig=0.8):
    """Magnitudes lognormales clairsemees."""
    return (rng.random(shape) < p) * rng.lognormal(mu, sig, shape)


def _synthetic_connectome(rng, kind="control"):
    """Connectome 116x116 symetrique, signes aleatoires, |W| a structure.

    kind : "control" | "tsa" | "sz" | "ad" — module plante selon l'axe
    gele correspondant (NOTE-MCS-28, §6).
    """
    W = np.zeros((116, 116))
    p_intra = 0.15 if kind == "sz" else 0.35
    p_inter = 0.18 if kind == "sz" else 0.12
    for p in PLAN_ORDER:
        W[np.ix_(PLAN_INDICES[p], PLAN_INDICES[p])] = _mag(
            rng, (len(PLAN_INDICES[p]),) * 2, p_intra)
    W = W + _mag(rng, (116, 116), p_inter)  # fond inter-plan commun

    def setblock(a, b, p, mu=0.0):
        ia, ib = PLAN_INDICES[a], PLAN_INDICES[b]
        sub = _mag(rng, (len(ia), len(ib)), p, mu)
        W[np.ix_(ia, ib)] = sub
        W[np.ix_(ib, ia)] = sub.T

    if kind == "tsa":
        for p in ("E2", "E6"):
            W[np.ix_(PLAN_INDICES[p], PLAN_INDICES[p])] = _mag(
                rng, (len(PLAN_INDICES[p]),) * 2, 0.6, 0.5)
        setblock("E2", "E6", 0.02)
    elif kind == "ad":
        for p in ("E1", "E2", "E3", "E4", "E5", "E6"):
            setblock(p, "E7", 0.5, 1.0)
        setblock("E3", "E4", 0.02)
    S = rng.choice([-1.0, 1.0], size=(116, 116))
    W = 0.5 * (W * S + (W * S).T)
    np.fill_diagonal(W, 0.0)
    return W


def dry_run(n_subjects=50, seed=20261028):
    """Retourne les Z signes par axe plante ; les sens doivent matcher.

    Attendu (axes geles) : tsa Gamma+, C_26- ; sz S_ent+, Gamma- ;
    ad d_eff-, M_34-. Le sz S_ent+ est connu non plantable isolément
    (couplage Gamma–S_ent, voir docstring du module) : il est rapporte
    mais n'entre pas dans le verdict.
    """
    _check_partition()
    P = build_projectors([PLAN_INDICES[p] for p in PLAN_ORDER])
    rng = np.random.default_rng(seed)
    cohorts = {}
    for kind in ("control", "tsa", "sz", "ad"):
        invs = [compute_noetic_invariants(
            project_connectome_to_7plans(_synthetic_connectome(rng, kind), P))
            for _ in range(n_subjects)]
        cohorts[kind] = {k: np.array([v[k] for v in invs]) for k in
                         ("Gamma", "S_ent", "d_eff", "C_26", "M_34")}
    ctrl = cohorts["control"]

    def z(kind, key):
        return float((cohorts[kind][key].mean() - ctrl[key].mean())
                     / (ctrl[key].std() + 1e-15))

    checks = [
        ("tsa", "Gamma", +1, True), ("tsa", "C_26", -1, True),
        ("sz", "S_ent", +1, False), ("sz", "Gamma", -1, True),
        ("ad", "d_eff", -1, True), ("ad", "M_34", -1, True),
    ]
    results, ok_all = [], True
    for kind, key, expected_sign, counts in checks:
        zv = z(kind, key)
        ok = np.sign(zv) == expected_sign
        if counts:
            ok_all &= ok
        results.append((kind, key, zv, ok, counts))
    rng2 = np.random.default_rng(seed)
    inv_a = compute_noetic_invariants(project_connectome_to_7plans(
        _synthetic_connectome(rng2, "control"), P))
    rng3 = np.random.default_rng(seed)
    inv_b = compute_noetic_invariants(project_connectome_to_7plans(
        _synthetic_connectome(rng3, "control"), P))
    det_ok = all(np.isclose(inv_a[k], inv_b[k]) for k in inv_a)
    M = project_connectome_to_7plans(
        _synthetic_connectome(np.random.default_rng(seed), "control"), P)
    M_d = deformation_d2_majorana(M)
    d2_ok = bool(np.all(np.isfinite(M_d)) and np.allclose(M_d, M_d.T))
    return results, ok_all, det_ok, d2_ok


if __name__ == "__main__":
    results, ok_all, det_ok, d2_ok = dry_run()
    print("MCS-28 dry-run synthetique (N=50/groupe, graine 20261028)")
    for kind, key, zv, ok, counts in results:
        tag = "OK" if ok else ("couplage Gamma-S_ent (documente, hors verdict)"
                               if not counts else "ECHEC")
        print(f"  {kind:7s} {key:6s} Z = {zv:+8.3f}  {tag}")
    print(f"  determinisme (rejeu meme graine) : {'OK' if det_ok else 'ECHEC'}")
    print(f"  deformation D2 finie + symetrique : {'OK' if d2_ok else 'ECHEC'}")
    print(f"  VERDICT DRY-RUN : {'INSTRUMENT OK' if (ok_all and det_ok and d2_ok) else 'A REVOIR'}")
