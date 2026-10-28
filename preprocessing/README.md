# Pré-traitement — infrastructure branche B

**Date :** 2026-10-28 · **Statut :** infrastructure de chantier, non scellée.
**Filiation :** NOTE-MCS-28 (§7.3 pipeline versionné) · NOTE-DEMANDE-ACCES-DONNEES (§5, branche B).

## Deux voies

| Voie | Quand | Statut ce jour |
|---|---|---|
| **B-light : ANTsPy natif** (`ants_pipeline.py`) | cette machine, sans reboot | **v0.1 écrite, en test** |
| **B : fMRIPrep (Docker/WSL2)** | standard du domaine, requis pour le scellement | bloquée : WSL2 absent, `wsl --install` demande un reboot + droits admin (action P.) |

La voie fMRIPrep reste la voie de scellement (reconnaissance par les
reviewers, qualité de référence). B-light sert à développer, valider et
débloquer les cohortes sans dérivés publics (COBRE, MCIC, QTIM, ADNI
brut) dès ce soir, avec une chaîne versionnée et un sidecar JSON par
sujet.

## B-light v0.1 — chaîne figée (PARAMS.json)

BIDS brut → T1 : N4 + SyNRA vers MNI 2 mm → EPI : correction de
mouvement rigide → EPI→T1 rigide → compose vers MNI → nuisance (moyennes
WM/CSF, 6 paramètres de mouvement, dérive) → band-pass 0.01–0.1 Hz →
séries AAL-116 (SPM12, NiftiLabelsMasker, standardisées) → corrélation +
Fisher z → `connectome_fisherz_116.npy` + `sidecar.json` (versions,
paramètres, FD moyen, durée).

Réutilisation : le connectome produit se projette directement dans le
moteur `src/mcs28_connectome_aal116.py` (|W| sur le z de Fisher — déjà
la convention de l'instrument).

## Usage

```
python ants_pipeline.py --t1 sub-XX/anat/*_T1w.nii.gz \
    --bold sub-XX/func/*task-rest_bold.nii.gz --out out/sub-XX
```

## Limites déclarées de B-light

1. Pas de segmentation FreeSurfer (surfaces, épaisseur corticale).
2. Normalisation T1 par SyNRA 2 mm — pas de contrôle qualité visuel
   automatisé (seulement FD moyen journalisé).
3. Nuisance par masques template (ICBM) — approximation du standard
   fMRIPrep (aCompCor non implémenté).
4. Slice-timing non corrigé (ordre d'acquisition non géré en v0.1).

Chaque limite est un chantier d'amélioration versionné, pas une
concession silencieuse.
