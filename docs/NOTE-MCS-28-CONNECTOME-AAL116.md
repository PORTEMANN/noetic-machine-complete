# Note de consolidation — MCS-28 : Partition spectrale AAL-116 (7 plans) × connectomes cliniques

**Date :** 2026-10-28 · **Tiroir :** consolidation d'une carte candidate
(document descriptif et spécification ; aucune carte gelée modifiée).
**Filiation :** T39 (la classe « cognition/bio ~1 » déclarée non atteinte)
· Cognition.pdf, Cognition_2.pdf, Cognition_3.pdf (décembre 2025,
dossier Machine 0910) · la carte MCS-28 candidate (ALL116.md).

---

## 1. Objet et statut

Cette note consolide la carte MCS-28 candidate : **partition figée de
l'atlas AAL-116 en 7 plans noétiques E1–E7**, projection des connectomes
cliniques (ABIDE, COBRE/ds004169, ADNI) sur l'espace réduit 7 × 7, et
extraction de 5 invariants à zéro paramètre ajusté.

**Statut : carte candidate, soumise à démonstration de puissance (règle
1.2) avant tout scellement.** Elle est la première carte du domaine
bio/cognition : elle vise à fermer la classe que T39 avait déclarée non
atteinte. Rien dans cette note n'est scellé ; tout est figé *en
attente de run*.

Trois sources, trois registres — à ne jamais mélanger :

| Source | Registre | Rôle pour la carte |
|---|---|---|
| Cognition.pdf (12/2025) | spéculatif (Köïlon, Orch-OR) | cadre interprétatif ; **hors régime de pesée** ; source de la Γ (Eq. 16) |
| Cognition_2.pdf (12/2025) | déclaratif | Table 8 (tendances) gélées en axes ; **résultats non re-produits** (voir §7) |
| Cognition_3.pdf (12/2025) | modélisation | Table 1 / Annexe A1 (plans, tailles) ; Eq. 22 (entropie spectrale) ; Annexe A.2 (filtrage) |

## 2. Les 7 plans

| Plan | Sémantique | Taille | Poids (A1) |
|---|---|---|---|
| E1 | Perception | 18 | 0.18 |
| E2 | Émotion | 12 | 0.14 |
| E3 | Raisonnement | 22 | 0.21 |
| E4 | Intuition | 14 | 0.13 |
| E5 | Conscience de soi | 10 | 0.10 |
| E6 | Social | 16 | 0.15 |
| E7 | Intégration | 24 | 0.09 |
| **Total** | | **116** | 1.00 |

## 3. Décisions de figeage

**D1 — Partition stricte.** Cognition_3 (Table 1) annonce « certaines
régions partagées » tout en totalisant 116 ; la somme des tailles fait
exactement 116, ce qui n'est compatible qu'avec une partition stricte
(indices disjoints). La carte et le moteur exigeant des indices
disjoints, **le partage est écarté** : chaque région AAL appartient à
exactement un plan. Les chevauchements de l'Annexe A1 (régions nommées
dans deux plans) sont arbitrés, voir §4.

**D2 — Références d'équations resserrées.** La carte citait Γ « TSA
Eq. 16 » (juste : Eq. 16 de Cognition.pdf, matrice quasi-diagonale
M_ij = δ_ij·M_ii de l'autisme — dont Γ mesure la spécialisation
diagonale) et S_ent « Eq. 23 » (**à corriger** : l'entropie spectrale
est l'Eq. 22 de Cognition_3 ; l'Eq. 23 y est la dimension de corrélation
de Grassberger–Procaccia, objet distinct du d_eff de la carte, calculé
par entropie de participation sur le spectre de M²). Corrigé dans cette
note, qui fait référence.

**D3 — Le filtre Majorana, constante structurelle.** Cognition_2
(Annexe A.2, règle 1) écrit M_ij ← M_ij × e^(−α·ln r_j) avec α
*calibré* parmi les 28 paramètres du papier. La carte fige α = 1/7.
Justification déclarée : 7 est le nombre de plans ; en échelle
logarithmique, e^(−ln r_j / 7) = r_j^(−1/7) attribue à chaque plan un
septième d'échelle spectrale. C'est la seule constante choisie du
moteur : elle est ici documentée comme telle, conformément à la règle
« une règle gelée porte sa justification ».

**D4 — Invariants canoniques sans filtre ; le filtre est une
déformation.** Ordre figé : |W|, diagonale nulle → M = Pᵀ|W|P →
invariants (Γ, S_ent, d_eff, C_26, M_34) **avant** filtrage → le filtre
Majorana (par colonnes j, puis symétrisation ½(M+Mᵀ)) n'est appliqué
que comme déformation de robustesse **D2**. Rationale : le filtre réduit
les hors-diagonales ; un Γ mesuré après filtre serait artificiellement
gonflé. La symétrisation post-filtre est figée et déclarée (la règle
brute ne la spécifie pas).

## 4. La partition figée

Vérifiée mécaniquement le 28/10/2026 : 7 listes d'indices 0–115,
**disjointes et de réunion complète** (assert en fin de note). Source de
la nomenclature : atlas AAL officiel *SPM12* (116 étiquettes),
récupéré via `nilearn.fetch_atlas_aal(version='SPM12')` — la table
d'indices du moteur est donc exacte et non reconstituée de mémoire.
**Risque épinglé :** nilearn ≥ 0.14 installe par défaut AAL3v2 (166
régions, numérotation différente) ; le pipeline devra épingler
explicitement l'AAL-116 SPM12.

| Plan | Régions AAL (paires L/R sauf vermis) | Indices 0-based |
|---|---|---|
| E1 Perception (18) | Precentral, Postcentral, Paracentral_Lobule, Calcarine, Cuneus, Lingual, Occipital_Sup, Occipital_Inf, Heschl | 0, 1, 42–49, 52, 53, 56, 57, 68, 69, 78, 79 |
| E2 Émotion (12) | Amygdala, Hippocampus, ParaHippocampal, Insula, Caudate, Putamen | 28–29, 36–41, 70–73 |
| E3 Raisonnement (22) | Frontal_Sup, Frontal_Sup_Orb, Frontal_Sup_Medial, Frontal_Med_Orb, Frontal_Mid, Frontal_Mid_Orb, Frontal_Inf_Oper, Frontal_Inf_Tri, Frontal_Inf_Orb, Rectus, Supp_Motor_Area | 2–15, 18, 19, 22–27 |
| E4 Intuition (14) | Cingulum_Ant, Cingulum_Mid, Precuneus, Angular, Parietal_Sup, Parietal_Inf, SupraMarginal | 30–33, 58–67 |
| E5 Conscience de soi (10) | Cingulum_Post, Rolandic_Oper, Thalamus, Pallidum, Olfactory | 16, 17, 20, 21, 34, 35, 74–77 |
| E6 Social (16) | Temporal_Pole_Sup, Temporal_Mid, Temporal_Pole_Mid, Temporal_Inf, Temporal_Sup, Fusiform, Occipital_Mid, Cerebelum_Crus1 | 50, 51, 54, 55, 80–91 |
| E7 Intégration (24) | Cerebelum_Crus2, Cerebelum_3, Cerebelum_4_5, Cerebelum_6, Cerebelum_7b, Cerebelum_8, Cerebelum_9, Cerebelum_10, Vermis_1_2 … Vermis_10 | 92–115 |

**Arbitrages et substitutions déclarés** (écarts à l'Annexe A1) :

1. *Accumbens* (nommé en E2) **∉ AAL-116** → remplacé par *Putamen*
   (boucle de récompense, fonction équivalente).
2. *Occipital_Mid* nommé à la fois sous E1 (implicite, zone visuelle)
   et explicitement sous E6 → arbitré **vers E6** (A1 l'y nomme
   explicitement).
3. *SupraMarginal* nommé sous E4 **et** E5 → arbitré **vers E4**.
4. *Parietal_Inf* nommé sous E6, ajouté à **E4** (réseau du mode par
   défaut, sémantiquement E4).
5. Ajouts au-delà des exemples A1, tous sémantiquement motivés :
   E1 += Paracentral_Lobule (somatosensoriel), Occipital_Inf (visuel),
   Heschl (auditif primaire) ; E3 += les quatre paires orbitaires et
   médianes (Frontal_Sup_Orb, Frontal_Mid_Orb, Frontal_Sup_Medial,
   Frontal_Med_Orb) ; E5 += Thalamus (arousal, conscience clinique),
   Pallidum (boucle BG, monitorage), Olfactory (limbique basal) ;
   E6 += **Cerebelum_Crus1** (cérébellum cognitif, connectivité
   préfrontale documentée).
6. **E7 = complément** (règle du reste) : cervelet Crus2→10 + vermis,
   24 régions — cohérent avec « connectivités longues » de A1.

L'attribution la plus discutable est E5 (Thalamus/Pallidum/Olfactory) :
elle est maintenue mais signalée pour ré-audit à la gate atlas.

## 5. Moteur canonique (spécification v0)

Le moteur ci-dessous est la référence de la carte. Écarts par rapport au
brouillon initial : plans figés intégrés (§4) ; invariants canoniques
calculés **avant** filtre (D4) ; le filtre devient la déformation D2
(avec symétrisation déclarée). Python/numpy, déterministe à PRNG public
près.

```python
import numpy as np

# Partition figée (NOTE-MCS-28, §4) — indices 0-based AAL-116 SPM12
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

def build_projectors(plan_indices_list, n_rois=116):
    """Matrice de projection P (116 x 7), normalisée à zéro paramètre."""
    assert len(plan_indices_list) == 7
    P = np.zeros((n_rois, 7), dtype=np.float64)
    for i, idx in enumerate(plan_indices_list):
        assert len(idx) == PLAN_SIZES[i], f"Taille invalide pour E{i+1}"
        P[idx, i] = 1.0 / np.sqrt(len(idx))
    return P

def project_connectome_to_7plans(W, P):
    """M = Pᵀ|W|P (7 x 7), diagonale auto-corrélée mise à zéro."""
    W_clean = np.abs(W).copy()
    np.fill_diagonal(W_clean, 0.0)
    return P.T @ W_clean @ P

def compute_noetic_invariants(M):
    """5 invariants canoniques — calculés SANS filtre (D4)."""
    diag_norm_sq = np.sum(np.diag(M) ** 2)
    total_norm_sq = np.sum(M**2) + 1e-15
    gamma_spec = diag_norm_sq / total_norm_sq          # Γ (Cognition.pdf Eq. 16)
    M2 = M @ M
    eigvals = np.clip(np.linalg.eigvalsh(M2), 1e-15, None)
    probs = eigvals / np.sum(eigvals)
    s_ent = -np.sum(probs * np.log(probs))             # S_ent (Cognition_3 Eq. 22)
    d_eff = 1.0 / np.sum(probs**2)                     # entropie de participation
    c_26 = M[1, 5] / np.sqrt(M[1, 1] * M[5, 5] + 1e-15)  # Émotion–Social
    m_34 = M[2, 3] / np.sqrt(M[2, 2] * M[3, 3] + 1e-15)  # Raisonnement–Intuition
    return {"Gamma": gamma_spec, "S_ent": s_ent, "d_eff": d_eff,
            "C_26": c_26, "M_34": m_34}

def deformation_d2_majorana(M):
    """Déformation de robustesse (filtre entropique, règle A.2.1, α=1/7).
    Convention figée : filtrage par colonnes j, PUIS symétrisation."""
    r_j = np.array(PLAN_SIZES, dtype=np.float64)
    M_d = M * np.exp(-np.log(r_j) / 7.0)[None, :]
    return 0.5 * (M_d + M_d.T)
```

## 6. Protocole de mesure

- **Cohortes :** ABIDE I+II (N = 1 114, TSA) · COBRE + ds004169
  (N = 296, schizophrénie) · ADNI (N = 1 737, Alzheimer/MCI) · HCP-YA
  (contrôles, pour la vérité plantée).
- **Axes directionnels gelés avant mesure** (Table 8 de Cognition_2) :
  TSA → Γ↑ C_26↓ ; SZ → S_ent↑ Γ↓ ; AD → d_eff↓ M_34↓.
- **Nul :** permutations préservant la symétrie hémisphérique G/D
  (N = 10 000, PRNG public).
- **Vérité plantée (règle 1.2) :** perturbations Eq. 4–5 sur connectomes
  HCP contrôles ; exigence p < 10⁻⁴ et puissance > 0.95.
- **Déformations de robustesse :** D1 seuillage k % · D2 filtre
  Majorana (§5) · D3 harmonisation ComBat.
- **Score joint :** Z_joint = somme signée des z-scores / √6 ;
  verdicts CS+ / CSp / CS− / CSi selon la doctrine en vigueur.

## 7. Vigilances de doctrine

1. **Cognition_2 est déclaratif.** Les 84.1 %, l'AUC 0.86 et les Table 3/
   8/13 n'ont jamais été re-produits par un run traçable. Ils ont le
   statut d'arguments, pas de mesures, jusqu'à la démonstration de
   puissance. La carte est l'instrument de cette re-production — ou de
   cette réfutation.
2. **Données :** ABIDE/COBRE/ds004169 sont ouverts ; **ADNI exige une
   demande d'accès (DUA, semaines)** ; HCP-YA est à demander.
3. **Pipeline versionné :** correction de mouvement, normalisation MNI,
   filtrage 0.01–0.1 Hz, extraction AAL-116 **épinglé SPM12** (§4),
   harmonisation ComBat. La reproductibilité se joue autant dans le
   pipeline que dans le moteur ; il sera versionné avec lui.
4. **La dynamique reste hors carte.** Les équations de Cognition_3
   (Eq. 2–18, dynamiques par plan) ne sont pas utilisées : la carte est
   purement statique et spectrale. Les dynamiques restent du côté du
   modèle — ne pas mélanger les registres.

## 8. Suite

1. Versionner le moteur en fichier `.py` et le tester sur connectomes
   synthétiques à modules plantés (dry-run, zéro donnée clinique).
2. Obtenir les accès ADNI / HCP.
3. Démonstration de puissance règle 1.2 sur HCP contrôles → seulement
   alors, verdict de scellement ou retour en chantier.

---

*Note de consolidation — carte candidate, non scellée. Les statistiques
de Cognition_2 citées ici restent des valeurs déclarées jusqu'au run.*
