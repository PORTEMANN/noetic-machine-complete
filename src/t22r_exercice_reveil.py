#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXERCICE T22-R — LE RÉVEIL VIRTUEL DU TARIF (drill local, 14/10/2026)
=====================================================================
⚠ EXERCICE — AUCUN FAIT DE LABORATOIRE. Source SYNTHÉTIQUE déclarée.
   Ce script n'est PAS une campagne et ne produit PAS un verdict :
   il exécute localement, sur le nombre qui engage la machine
   (Σm_ν = 58,99 meV, SYNTHÉTIQUE), les quatre étapes du protocole
   d'attente scellé au verdict T22 — pour mesurer CE QUI TOURNE et
   CE QUI MANQUE avant le vrai réveil. Règle de la maison : un exercice
   ne devient jamais une lecture à chaud ; il est daté, étiqueté, et
   ses lacunes sont le livrable.
"""
import hashlib
import importlib.util
import json
import time
from pathlib import Path

import numpy as np

T0 = time.time()
PHI = (1 + np.sqrt(5)) / 2
RACINE = Path(__file__).resolve().parent
MCS24 = RACINE.parents[1] / "coincidences-stables" / "resultats" / \
    "mcs24_resultats.json"
T11 = RACINE / "t11_ko6_famille_varietes.py"

print("EXERCICE T22-R — le réveil virtuel du tarif (source SYNTHÉTIQUE)")
print("=" * 76)

# ---- étape 1 : déclencheur (source synthétique hachée, étiquetée)
source = {"carte": "T22 protocole d'attente — EXERCICE",
          "fait_declare": "Σm_ν = 58,99 meV",
          "nature": "SYNTHÉTIQUE — exercice local, aucun fait de laboratoire",
          "date_exercice": "2026-10-14"}
emp_source = hashlib.sha256(json.dumps(source, ensure_ascii=False,
                                       sort_keys=True).encode()).hexdigest()
declenche = (58.99 < 64.0)  # condition d'exclusion >= 64 meV non violée
print(f"étape 1 — déclencheur (exercice) : source hashée {emp_source[:16]}… · "
      f"centrale 58,99 < borne 64 : {'DÉCLENCHÉ (virtuel)' if declenche else 'non'}")

# ---- étape 2 : le cadran — relation d'ancre T12 (filiation : t11 importé)
spec = importlib.util.spec_from_file_location("t11", str(T11))
t11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t11)
a0, a2, a4 = t11.S4(1.0)
rho_sim = 58.99          # MAPPING PLACEHOLDER déclaré (non scellé — trou n° 1)
lambda2_sel = rho_sim ** 2 + 3 - a2 / a0
lambda_sel = float(np.sqrt(lambda2_sel))
print(f"étape 2 — cadran (relation d'ancre T12, filiation t11) :")
print(f"   a₂/a₀ = {a2/a0:.9f} (S⁴(1)) · ρ_sim = {rho_sim} (PLACEHOLDER)")
print(f"   Λ²_sel = ρ² + 3 − a₂/a₀ = {lambda2_sel:.4f} · Λ_sel = "
      f"{lambda_sel:.4f} (unité placeholder = 1 meV)")
print("   ⚠ TROU N° 1 : le mapping Σm_ν → ρ n'est scellé nulle part — "
      "l'exercice utilise un placeholder déclaré ; il doit être gelé "
      "avant le vrai réveil.")

# ---- étape 3 : re-mesure du tarif — numérateur mécanique
m24 = json.loads(MCS24.read_text(encoding="utf-8"))
M_P_meV = 1.2209e28      # M_P = 1.2209e19 GeV (gelé MCS-24), en meV
N_REQ_BASE = m24["constantes_gelees"]["N_REQ_BASE"]
m_par = m24["m_par_config"]
lambda_sim_mev = lambda_sel            # conversion placeholder 1 unité = 1 meV
n_req_sealed = N_REQ_BASE              # Λ = M_P canonique (m_p/Λ = 1)
n_req_sim = N_REQ_BASE * (M_P_meV / lambda_sim_mev) ** 2
print(f"étape 3 — re-mesure du tarif (numérateur) :")
print(f"   N_req(scellé, Λ = M_P) = {n_req_sealed:.6f} · "
      f"N_req(Λ_sim = {lambda_sim_mev:.2f} meV) = {n_req_sim:.3e}")
lignes = []
for g, m in m_par.items():
    n_eff = n_req_sealed * 10 ** m     # N_eff récupéré du scellé
    m_prime = -abs(np.log10(n_eff / n_req_sim))
    lignes.append((g, m, m_prime))
    print(f"   {g:6s} : m scellé = {m:+.6f} → m'(Λ_sim) = {m_prime:+.6f}")
z_sealed = m24["z_par_g"]
print("   ⚠ TROU N° 2 : z' exige le nul PAR CADRAN (nul_reel dépend de "
      "n_req — moteur MCS-24 complet, non relancé ici). Le numérateur "
      "tourne ; la signature z est bloquée à l'exercice.")

# ---- étape 4 : machine à seuils (dry-run logique sur l'orbite scellée)
print("étape 4 — machine à seuils (dry-run sur l'orbite scelle MCS-24) :")
classes = {}
for g, z in z_sealed.items():
    classe = ("stable" if abs(z) >= 3 else
              "partiel" if abs(z) >= 2 else "sommeil")
    classes[g] = classe
    print(f"   {g:32s} z = {z:+9.4f} → {classe.upper()}")
signes = {np.sign(z) for z in z_sealed.values()}
clause_orbite = (len(signes) == 1
                 and all(c == "stable" for c in classes.values()))
print(f"   clause d'ORBITE (signe unique sous tous les cadrans + stable "
      f"partout) : {clause_orbite} — signes presents : {signes}")
print("   ⚠ TROU N° 3 (faille du protocole) : les seuils scelles de T22 "
      "classent cadran par cadran ('|z| >= 3 → stable') — l'orbite "
      "MCS-24 serait 'STABLE' partout alors que son verdict est CSi "
      "ANTI-STABLE, precisement par inversion de signe. La machine a "
      "seuils manque de la clause d'orbite : stable AU SENS ORBITE = "
      "meme signe ET |z| >= 3 sous tous les cadrans ; sinon anti-stable.")

# ---- livrable de l'exercice
rapport = {
    "nature": "EXERCICE — réveil virtuel, source synthétique, aucun fait de labo",
    "empreinte_source_synthetique": emp_source,
    "etapes": {
        "1_declencheur": "exécuté (virtuel) — source hashée et étiquetée",
        "2_cadran": f"exécuté avec placeholder — Λ_sel = {lambda_sel:.4f} "
                    f"(unité placeholder) ; a₂/a₀ = {a2/a0:.9f}",
        "3_tarif_numerateur": "exécuté — m'(Λ_sim) par cadran calculé ; "
                              "z' bloqué (nul par cadran requis)",
        "4_seuils": "exécuté — machine à seuils dry-run sur l'orbite scellée"},
    "trous_identifies": [
        "TROU N° 1 : le mapping Σm_ν → ρ (cadran) n'est scellé nulle part "
        "— à geler avant le vrai réveil (fiche T23 candidate)",
        "TROU N° 2 : la re-mesure de z exige le moteur MCS-24 complet "
        "(nul par cadran) — relançable, non relancé à l'exercice",
        "TROU N° 3 (faille du protocole) : les seuils scellés de T22 "
        "classent cadran par cadran — l'orbite MCS-24 y serait 'stable' "
        "partout alors qu'elle est CSi anti-stable par inversion de "
        "signe ; la clause d'orbite manque (addendum de gouvernance "
        "proposé, approuvé le 14/10/2026 : stable AU SENS ORBITE = même "
        "signe ET |z| ≥ 3 sous tous les cadrans ; sinon anti-stable)"],
    "clause_orbite_mesuree": {
        "signe_unique": bool(len(signes) == 1),
        "classe_orbite": ("stable (orbite)" if clause_orbite
                          else "ANTI-STABLE (orbite) — inversion de signe"),
        "applicable_au_cas_MCS24": "anti-stable — cohérent avec le "
                                   "verdict CSi scellé"},
    "m_prime_par_cadran": {g: mp for g, _, mp in lignes},
    "regle": "un exercice ne devient jamais une lecture à chaud",
    "duree_s": round(time.time() - T0, 2),
}
out = RACINE.parent / "data" / "t22r_exercice_reveil_virtuel.json"
out.write_text(json.dumps(rapport, ensure_ascii=False, indent=2),
               encoding="utf-8")
print("\n" + "=" * 76)
print("EXERCICE terminé — rapport →", out)
print("Bilan : 3 trous identifiés (mapping ρ à sceller ; moteur nul à "
      "reprendre ; clause d'orbite ajoutée par addendum de gouvernance "
      "approuvé le 14/10/2026) — le protocole est prêt, ses lacunes "
      "sont nommées, datées, et n'attendent plus qu'une fiche gelée.")
