# Dossier d'accès aux données — ADNI & HCP (MCS-28)

**Date :** 2026-10-28 · **Tiroir :** opérationnel (préparation de demandes ;
aucune donnée personnelle, aucune carte gelée modifiée).
**Filiation :** NOTE-MCS-28-CONNECTOME-AAL116 (§8, suite) ·
`src/mcs28_connectome_aal116.py` · règle 1.2 (démonstration de puissance).

---

## 1. Procédures vérifiées ce jour

### ADNI (adni.loni.usc.edu)
- Création de compte en ligne, **formulaire web d'utilisation des
  données** + signature de la **Data Use Agreement (DUA)**.
- Champs requis : nom, adresse et contact, affiliation académique (le
  cas échéant) ou institution/entreprise, **analyses proposées avec un
  investigateur responsable nommé par analyse**, certification point
  par point de la DUA.
- Le **Data Sharing and Publications Committee (DPC)** examine les
  demandes « généralement sous deux semaines » (site officiel ADNI) ;
  des publications 2026 rapportent des réponses en 1–2 jours. Retenons
  **2 semaines** pour le calendrier, tout en espérant moins.
- La DUA interdit la redistribution des données : les données restent
  en local, le code reste ouvert — conforme au modèle déjà pratiqué
  (moteur public, données jamais publiées).
- Mises à jour annuelles de la demande demandées par ADNI ; les
  informations du demandeur sont visibles des autres utilisateurs.

### HCP-YA (db.humanconnectome.org)
- Compte **ConnectomeDB** + activation par e-mail (≤ 24 h), puis
  acceptation en ligne des **HCP Open Access Data Use Terms** → accès
  immédiat à l'imagerie et à la plupart des données comportementales.
  Données *restricted* (âge exact, structure familiale…) : demande
  individuelle supplémentaire — **non nécessaire pour MCS-28** (les
  tranches d'âge suffisent).
- Téléchargements via plugin **Aspera** (prévoir l'installation).

### Cohortes ouvertes (aucune demande formelle lourde)
- **ABIDE I+II** : inscription NITRC/INDI ; dérivés pré-traités
  téléchargeables (ABIDE Preprocessed, CPAC — atlas AAL disponible).
- **COBRE** et **ds004169** (OpenNeuro) : accès ouvert ; ds004169 en
  BIDS brut (pré-traitement requis).

## 2. Vigilance de planification — le vrai N fMRI d'ADNI

La carte cite « ADNI N = 1 737 ». C'est le **N clinique/global**
(diagnoses, neuropsychologie). L'imagerie **rs-fMRI** ne couvre qu'un
**sous-ensemble d'ADNI-2/3** (ordre de grandeur usuel dans la
littérature : quelques centaines de sujets avec rs-fMRI exploitable, CN
+ MCI + AD) — ADNI reste une étude biomarqueurs dont l'IRM repose
surtout sur la structurelle et le PET. Conséquences, à écrire noir sur
blanc :

1. La demande ADNI doit porter sur **rs-fMRI + IRM structurelle +
   tables cliniques** (DXSUM, MMSE, CDR, démographie) — et la puissance
   statistique de l'axe AD devra être recalculée sur le N fMRI réel,
   pas sur 1 737.
2. L'axe AD pourrait devoir s'appuyer sur **ADNI + un complément
   ouvert** (ex. un jeu de démence sur OpenNeuro) si le N s'avère trop
   juste. À trancher après inventaire réel des scans.
3. ABIDE (TSA) et COBRE/ds004169 (SZ) ne posent pas ce problème :
   leurs N fMRI sont bien ceux de la carte.

## 3. Dossier ADNI — textes prêts (le formulaire est en anglais)

*Le dépôt de la demande doit être fait personnellement par Patrice
Portemann (identité, signature de la DUA). Tout est prêt à copier.*

**Affiliation :** *Independent researcher* (affiliation académique
absente ; le corpus public GitHub PORTEMANN/noetic-machine-complete
sert de référence vérifiable).

**Proposed analysis — Project title:**
> Zero-parameter spectral projection of brain connectomes onto a
> fixed 7-plan partition of the AAL-116 atlas: validation of clinical
> discriminative invariants in Alzheimer's disease and mild cognitive
> impairment.

**Lead investigator :** Patrice Portemann.

**Proposed analyses :**
> We will apply a fully pre-registered, zero-fitted-parameter method:
> each subject's resting-state functional connectivity matrix
> (AAL-116) is projected onto a fixed 7-plan partition (perception,
> emotion, reasoning, intuition, self-awareness, social, integration),
> yielding five algebraic invariants (diagonal specialization Γ,
> spectral entropy S_ent, effective dimension d_eff, normalized
> emotion–social coupling C_26, normalized reasoning–intuition
> coupling M_34). Group-level comparison CN vs MCI vs AD on these
> invariants; permutation null preserving inter-hemispheric symmetry
> (public PRNG seed, N = 10 000); robustness under thresholding,
> entropy filtering and ComBat harmonization. The method, frozen
> partition and analysis engine are public (GitHub: PORTEMANN/
> noetic-machine-complete), which allows full replication. Primary
> hypothesis (pre-registered direction): d_eff decreases and M_34
> decreases in AD. Data requested: resting-state fMRI and structural
> MRI of ADNI-2/3 participants, with diagnostic and neuropsychological
> tables (DXSUM, MMSE, CDR, demographics). All processing remains
> local; no data redistribution, per the DUA.

**Certification DUA :** point par point, sans réserve (usage recherche,
pas de réidentification, pas de redistribution, reconnaissance ADNI
dans toute publication).

## 4. Dossier HCP — étapes (immédiates)

1. Créer le compte ConnectomeDB (e-mail d'activation ≤ 24 h).
2. Accepter les HCP Open Access Data Use Terms en ligne.
3. Installer le plugin Aspera.
4. Télécharger les paquets rfMRI (REST1/REST2, FIX-denoised,
   minimalement pré-traités) pour les sujets contrôles — base de la
   **vérité plantée (règle 1.2)** : les connectomes HCP contrôles
   portent les perturbations Eq. 4–5 avant toute donnée clinique.

## 5. Calendrier réaliste (depuis le 28/10/2026)

| Étape | Quand | Responsable |
|---|---|---|
| Inscription ABIDE/NITRC + téléchargement dérivés CPAC (TSA) | sem. du 03/11 | machine + P. |
| COBRE + ds004169 (SZ) | sem. du 03/11 (ds004169 requiert pré-traitement) | machine |
| Compte ConnectomeDB + termes HCP | 1–2 jours | P. |
| Téléchargement rfMRI HCP contrôles (volume important, Aspera) | sem. du 10/11 | machine |
| **Dépôt demande ADNI** (textes §3) | ≤ 05/11 | **P.** |
| Réponse DPC ADNI (annonce officielle ≤ 2 sem.) | ~19/11 | ADNI |
| Pipeline de pré-traitement reproductible (branche A : dérivés ; branche B : fMRIPrep si nécessaire) | 03/11 → 28/11 | machine |
| Démonstration de puissance règle 1.2 sur HCP (vérité plantée, p < 10⁻⁴) | déc. | machine |
| Analyse ABIDE (TSA) / COBRE-ds004169 (SZ) — axes gelés + nul symétrique | déc. | machine |
| Inventaire rs-fMRI ADNI réel, recalcul de puissance axe AD | déc.–janv. | machine |
| Analyse ADNI (CN/MCI/AD) | janv.–févr. 2027 | machine |
| **Verdict de scellement ou retour en chantier** | ~févr. 2027 | maison |

**Branches d'infrastructure à trancher :** (A) s'appuyer au maximum des
dérivés pré-traités publics (ABIDE-CPAC, HCP minimal) — plus rapide,
mais hétérogène entre cohortes ; (B) repasser tout dans un pipeline
unique versionné (fMRIPrep) — homogène, conforme à la doctrine, mais
lourd en calcul (Docker/WSL2, dizaines d'heures CPU par sujet, ADNI
compris). La doctrine penche (B) pour la phase finale ; (A) sert de
banc intermédiaire pendant l'attente ADNI.

---

*Document opérationnel préparé le 28/10/2026. Aucune donnée obtenue à
cette date ; aucune demande encore déposée.*
