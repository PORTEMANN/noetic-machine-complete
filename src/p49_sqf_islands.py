#!/usr/bin/env python3
"""
CAMPAGNE P49 — Nucléaire : règle sqf des îlots de stabilité super-lourds
Protocole gelé le 2026-09-08
Auteur : Patrice Portemann — ORCID: 0009-0009-4016-8389

Version 1.1 (2026-09-08) — correctifs de traçabilité UNIQUEMENT
(la règle de prédiction gelée est inchangée) :
  - ajout des champs falsifieur_F1 / falsifieur_F2 dans le verdict
    (présents dans le JSON de démo mais non produits par la v1.0) ;
  - création automatique du dossier data/ ;
  - ajout de la matrice de confusion (TP/FP/FN/TN) dans le verdict.
Données : NUBASE2020 (Kondev et al., Chin. Phys. C45, 030001 (2021)),
converties en CSV Z,A,half_life_s,status — états fondamentaux Z>=104.
"""
import numpy as np
import json
import hashlib
import os
from datetime import datetime
import sys

def sqf(n):
    """Partie sans facteur carré (squarefree part)."""
    if n <= 0: return 0
    i, res = 2, 1
    while i * i <= n:
        if n % i == 0:
            n //= i
            if n % i != 0: res *= i
            else:
                while n % i == 0: n //= i
        i += 1
    if n > 1: res *= n
    return res

M_sqf = {n for n in range(1, 200) if sqf(n) % 2 == 1 and sqf(n) <= 7}

def predict(Z, A):
    """Structure candidate S (règle gelée — ne pas modifier)."""
    found = False
    for k in range(1, 10):
        m = A - 18 * k
        if m in M_sqf and m > 0:
            found = True
            break
    if not found: return False, 'A not in 18k+M_sqf'
    if Z > 180: return False, 'Z > 180'
    if (A - Z) % 2 != sqf(Z) % 2: return False, 'parity mismatch'
    return True, 'ok'

def predict_no_cap(Z, A):
    """Levier discriminant : sans coupure k <= 9."""
    for k in range(1, 100):
        m = A - 18 * k
        if m > 0 and m in M_sqf:
            break
    else: return False
    if Z > 180: return False
    if (A - Z) % 2 != sqf(Z) % 2: return False
    return True

def sha256_dict(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()

def main():
    import csv
    data_path = sys.argv[1] if len(sys.argv) > 1 else 'data/ame2020_mass_eval.csv'

    nuclei = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['Z']) >= 104:
                nuclei.append({
                    'Z': int(row['Z']),
                    'A': int(row['A']),
                    'half_life': float(row.get('half_life_s', 0)),
                    'status': row.get('status', 'unknown')
                })

    results = []
    correct = 0

    for nuc in nuclei:
        pred, reason = predict(nuc['Z'], nuc['A'])
        predicted_stable = pred
        actual_stable = nuc['half_life'] > 1.0  # seuil gelé : 1 seconde
        match = (predicted_stable == actual_stable)
        if match: correct += 1

        results.append({
            'Z': nuc['Z'], 'A': nuc['A'], 'N': nuc['A'] - nuc['Z'],
            'sqf_Z': sqf(nuc['Z']), 'sqf_A': sqf(nuc['A']),
            'predicted_stable': predicted_stable,
            'actual_stable': actual_stable,
            'match': match,
            'reason': reason
        })

    total = len(nuclei)
    score = correct / total if total else 0

    # Matrice de confusion
    tp = sum(1 for r in results if r['predicted_stable'] and r['actual_stable'])
    fp = sum(1 for r in results if r['predicted_stable'] and not r['actual_stable'])
    fn = sum(1 for r in results if not r['predicted_stable'] and r['actual_stable'])
    tn = sum(1 for r in results if not r['predicted_stable'] and not r['actual_stable'])

    # Levier discriminant
    stables_with_cap = sum(1 for r in results if r['predicted_stable'])
    stables_without_cap = sum(1 for nuc in nuclei if predict_no_cap(nuc['Z'], nuc['A']))

    # Falsifieurs gelés
    f1_violations = sum(1 for r, nuc in zip(results, nuclei)
                        if r['predicted_stable'] and nuc['half_life'] < 1e-3)
    f2_violations = sum(1 for r, nuc in zip(results, nuclei)
                        if not r['predicted_stable'] and nuc['half_life'] > 1.0)

    verdict = 'succès' if score >= 0.80 else ('partiel' if score >= 0.60 else 'B3-FAIL')

    output = {
        'campagne': 'P49',
        'date_gel': '2026-09-08',
        'date_execution': datetime.now().isoformat(),
        'source_donnees': 'NUBASE2020 (Kondev et al. 2021) — états fondamentaux Z>=104',
        'score': f'{correct}/{total}',
        'score_fraction': round(score, 3),
        'verdict': verdict,
        'confusion': {'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn},
        'levier_discriminant': {
            'stables_avec_coupe_k9': stables_with_cap,
            'stables_sans_coupe': stables_without_cap,
            'effondrement': stables_without_cap > stables_with_cap * 2
        },
        'falsifieur_F1': f'Noyaux prédits stables avec T1/2 < 1 ms : {f1_violations}',
        'falsifieur_F2': f'Noyaux hors zone prédite stable avec T1/2 > 1 s : {f2_violations}',
        'details': results,
        'sha256': sha256_dict({'results': results, 'score': score})
    }

    os.makedirs('data', exist_ok=True)
    with open('data/p49_verdict.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f'P49 — Score: {correct}/{total} = {score:.3f}')
    print(f'P49 — Verdict: {verdict}')
    print(f'P49 — Confusion: TP={tp} FP={fp} FN={fn} TN={tn}')
    print(f'P49 — Fichier: data/p49_verdict.json')

if __name__ == '__main__':
    main()
