# -*- coding: utf-8 -*-
"""Pipeline de pre-traitement reproductible — branche B-light (ANTsPy).

Version 0.1 (28/10/2026). Parametres figes : PARAMS.json (meme dossier).
Chaine : BIDS brut -> T1 MNI (SyNRA, 2 mm) -> EPI mouvement (rigide)
-> EPI->T1 (rigide) -> normalisation MNI -> regression de nuisance
(WM, CSF, mouvement, derive) -> band-pass 0.01-0.1 Hz -> series AAL-116
-> connectome de Fisher z (116x116) + JSON sidecar.

Usage :
    python ants_pipeline.py --t1 <t1w.nii.gz> --bold <rest_bold.nii.gz> \
        --tr <secondes> --out <dossier_sortie>

Positionnement : voie intermediaire sans reboot (WSL2/Docker absents).
La voie principale de scellement reste fMRIPrep (Docker/WSL2) ; ce
pipeline sert de banc de developpement et de secours reproductible.
"""

import argparse
import json
import time

import os

import ants
import nibabel as nib
import numpy as np
from nilearn.maskers import NiftiLabelsMasker

PARAMS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "PARAMS.json")))


def load_bids_tr(bold_path):
    """TR depuis le sidecar BIDS JSON, sinon erreur (pas de magie)."""
    sidecar = bold_path.replace(".nii.gz", ".json")
    try:
        with open(sidecar) as f:
            return float(json.load(f)["RepetitionTime"])
    except Exception as e:
        raise RuntimeError(f"TR introuvable dans {sidecar} : {e}")


def run(t1_path, bold_path, tr, out_dir):
    import os
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    log = {}

    # --- T1 : N4 puis normalisation MNI (SyNRA, 2 mm)
    t1 = ants.image_read(t1_path)
    t1c = ants.n4_bias_field_correction(t1)
    from nilearn.datasets import load_mni152_template
    mni_nib = load_mni152_template(resolution=2)
    try:
        mni2 = ants.from_nibabel(mni_nib)
    except AttributeError:
        aff = mni_nib.affine
        mni2 = ants.from_numpy(
            np.ascontiguousarray(mni_nib.get_fdata(), dtype=np.float32),
            origin=tuple(aff[:3, 3]),
            spacing=tuple(np.abs(aff.diagonal()[:3])),
            direction=aff[:3, :3] / np.abs(aff.diagonal()[:3]))
    reg = ants.registration(fixed=mni2, moving=t1c,
                            type_of_transform=PARAMS["t1_to_mni"]["transform"])
    log["t1_to_mni_transform"] = PARAMS["t1_to_mni"]["transform"]

    # --- EPI : correction de mouvement (rigide)
    bold = ants.image_read(bold_path)
    moco = ants.motion_correction(bold, type_of_transform="Rigid")
    bold_mc = moco["motion_corrected"]
    fd_arr = np.asarray(moco["FD"], dtype=float).ravel()
    fd = float(fd_arr.mean()) if fd_arr.size else float("nan")
    log["mean_fd_mm"] = fd
    epi_mean = ants.from_numpy(
        np.ascontiguousarray(bold_mc.numpy().mean(axis=3), dtype=np.float32),
        origin=bold_mc.origin[:3], spacing=bold_mc.spacing[:3],
        direction=np.asarray(bold_mc.direction)[:3, :3])

    # --- EPI -> T1 (rigide), puis compose vers MNI
    reg_e = ants.registration(fixed=t1c, moving=epi_mean,
                              type_of_transform=PARAMS["epi_to_t1"]["transform"])
    fwd = reg["fwdtransforms"] + reg_e["fwdtransforms"]
    bold_mni = ants.apply_transforms(
        fixed=mni2, moving=bold_mc, transformlist=fwd,
        interpolator="linear", whichtoinvert=[False] * len(fwd),
        imagetype=3)
    log["epi_to_t1_transform"] = PARAMS["epi_to_t1"]["transform"]

    # --- Nuisance : masques WM/CSF du template ICBM dans l'espace MNI 2mm
    from nilearn.datasets import fetch_icbm152_2009
    icbm = fetch_icbm152_2009()
    wm = ants.image_read(icbm["wm"]).resample_image_to_target(mni2, interp_type=1)
    csf = ants.image_read(icbm["csf"]).resample_image_to_target(mni2, interp_type=1)
    wm_m = wm.numpy() > PARAMS["nuisance"]["wm_threshold"]
    csf_m = csf.numpy() > PARAMS["nuisance"]["csf_threshold"]
    Y = bold_mni.numpy().reshape(-1, bold_mni.shape[3])
    wm_sig = Y[wm_m.ravel()].mean(axis=0) if wm_m.any() else np.zeros(Y.shape[1])
    csf_sig = Y[csf_m.ravel()].mean(axis=0) if csf_m.any() else np.zeros(Y.shape[1])
    nvol = Y.shape[1]
    t = np.arange(nvol)
    # v0.1 : les parametres de mouvement ne sont pas rejetes en tant que
    # regresseurs (ants.motion_correction ne les expose que sous forme de
    # fichiers .mat par volume). La correction spatiale rigide reste
    # appliquee ; la regression motion est un chantier v0.2 (voir README).
    X = np.column_stack([wm_sig, csf_sig,
                         t / nvol, np.ones(nvol)])
    beta, *_ = np.linalg.lstsq(X, Y.T, rcond=None)
    Y = (Y.T - X @ beta).T

    # --- Band-pass 0.01-0.1 Hz
    from scipy.signal import butter, filtfilt
    fs = 1.0 / tr
    b, a = butter(PARAMS["filter"]["order"],
                  [PARAMS["filter"]["fmin_hz"], PARAMS["filter"]["fmax_hz"]],
                  btype="band", fs=fs)
    Y = filtfilt(b, a, Y, axis=1)

    clean_img = nib.Nifti1Image(Y.reshape(bold_mni.shape),
                                mni_nib.affine)

    # --- Extraction AAL-116 (SPM12) et connectome de Fisher z
    from nilearn.datasets import fetch_atlas_aal
    aal = fetch_atlas_aal(version="SPM12")
    masker = NiftiLabelsMasker(labels_img=aal.maps,
                               standardize=PARAMS["atlas"]["standardize"],
                               detrend=False, verbose=0)
    series = masker.fit_transform(clean_img)  # (nvol, 116)
    C = np.corrcoef(series.T)
    Cz = np.arctanh(np.clip(C, -0.9999, 0.9999))
    # ROIs hors champ (variance nulle apres extraction) -> NaN ; mis a 0
    # et journalises (limitation v0.1 : pas d'interpolation de couverture)
    n_nan = int(np.isnan(Cz).sum())
    Cz = np.nan_to_num(Cz, nan=0.0)
    np.fill_diagonal(Cz, 0.0)
    log["nan_pairs_set_to_zero"] = n_nan
    np.save(f"{out_dir}/connectome_fisherz_116.npy", Cz.astype(np.float32))

    log.update({
        "pipeline": "ants_pipeline v0.1 (branche B-light)",
        "params_version": PARAMS["version"],
        "tr_s": tr,
        "n_volumes": int(nvol),
        "n_rois": int(series.shape[1]),
        "antspyx": ants.__version__,
        "duration_s": round(time.time() - t0, 1),
    })
    with open(f"{out_dir}/sidecar.json", "w") as f:
        json.dump(log, f, indent=2)
    print(json.dumps(log, indent=2))
    return Cz


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", required=True)
    ap.add_argument("--bold", required=True)
    ap.add_argument("--tr", type=float, default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    tr = args.tr or load_bids_tr(args.bold)
    run(args.t1, args.bold, tr, args.out)
