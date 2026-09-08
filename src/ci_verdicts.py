#!/usr/bin/env python3
"""
CAMPAGNE I3 — CI de reproductibilité
Question unique : les verdicts publiés dotés de données se ré-exécutent-ils
à l'identique, et les artefacts du dépôt passent-ils le contrôle SHA-256 ?
Protocole gelé le 2026-09-08 (avant run) :
  1. HASH : pour chaque ligne de data/p49_p51_shasums.txt, re-télécharger
     l'artefact depuis GitHub et comparer l'empreinte.
  2. RE-RUN P49 : script + CSV du dépôt -> comparer score, verdict, confusion,
     falsifieurs au verdict publié.
  3. RE-RUN P40 (corpus legacy) : script + 3 fichiers de données du dépôt ->
     comparer le verdict complet au verdict publié, et vérifier les
     empreintes de données embarquées dans le verdict.
  4. RE-RUN P51 : si le NPZ régénéré est disponible, comparer accuracy_globale,
     pair_accuracies et verdict au verdict publié.
Verdict gelé : REPRODUCTIBLE si tout passe ; ÉCART si un seul écart.
Auteur : Patrice Portemann — ORCID: 0009-0009-4016-8389
"""
import json, hashlib, subprocess, sys, os, shutil, urllib.request
from pathlib import Path

GH = 'https://raw.githubusercontent.com/PORTEMANN/noetic-machine-complete/main/'
WORK = Path('/tmp/local_camp/i3_run')
WORK.mkdir(parents=True, exist_ok=True)

def fetch(path):
    dest = WORK / path.replace('/', '__')
    urllib.request.urlretrieve(GH + path, dest)
    return dest

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

report = {'campagne': 'I3', 'date_gel': '2026-09-08', 'checks': []}

def check(name, ok, detail=''):
    report['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
    print(('PASS' if ok else 'FAIL'), '-', name, ('| ' + detail) if detail else '')

# ---- 1. HASH ----
shasums = fetch('data/p49_p51_shasums.txt')
n_ok = n_tot = 0
for line in Path(shasums).read_text().splitlines():
    parts = line.split()
    if len(parts) == 2 and len(parts[0]) == 64:
        n_tot += 1
        h = sha(fetch(parts[1]))
        if h == parts[0]:
            n_ok += 1
check('HASH artefacts P49-P51', n_ok == n_tot, f'{n_ok}/{n_tot} empreintes conformes')

# ---- 2. RE-RUN P49 ----
d = WORK / 'p49'; (d / 'data').mkdir(parents=True, exist_ok=True)
shutil.copy(fetch('src/p49_sqf_islands.py'), d / 'p49_sqf_islands.py')
shutil.copy(fetch('data/p49_data_nubase2020_z104.csv'), d / 'data' / 'p49_data_nubase2020_z104.csv')
published = json.loads(Path(fetch('data/p49_verdict.json')).read_text())
r = subprocess.run([sys.executable, 'p49_sqf_islands.py', 'data/p49_data_nubase2020_z104.csv'],
                   cwd=d, capture_output=True, text=True)
rerun = json.loads((d / 'data' / 'p49_verdict.json').read_text())
keys = ['score', 'score_fraction', 'verdict', 'confusion', 'levier_discriminant',
        'falsifieur_F1', 'falsifieur_F2', 'sha256']
diffs = [k for k in keys if rerun.get(k) != published.get(k)]
check('RE-RUN P49', not diffs and r.returncode == 0,
      f'score={rerun.get("score")} verdict={rerun.get("verdict")}' + (f' ÉCARTS: {diffs}' if diffs else ''))

# ---- 3. RE-RUN P40 ----
d = WORK / 'p40'; d.mkdir(parents=True, exist_ok=True)
shutil.copy(fetch('src/p40_zmax.py'), d / 'p40_zmax.py')
for f in ['p40_data_ame2020_mas20.txt', 'p40_data_fy235u.csv', 'p40_data_fy239pu.csv']:
    shutil.copy(fetch('data/' + f), d / f)
published40 = json.loads(Path(fetch('data/p40_zmax_verdict.json')).read_text())
r = subprocess.run([sys.executable, 'p40_zmax.py'], cwd=d, capture_output=True, text=True)
rerun40 = json.loads((d / 'p40_zmax_verdict.json').read_text())
diffs = [k for k in published40 if rerun40.get(k) != published40.get(k)]
check('RE-RUN P40 (legacy)', not diffs and r.returncode == 0,
      f'verdict_global={rerun40.get("verdict_global")}' + (f' ÉCARTS: {diffs}' if diffs else ''))
# empreintes de données embarquées dans le verdict P40
emb = published40.get('données', {})
emb_ok = all(sha(d / f) == h for f, h in
             [('p40_data_ame2020_mas20.txt', emb.get('AME2020')),
              ('p40_data_fy235u.csv', emb.get('FY_U235')),
              ('p40_data_fy239pu.csv', emb.get('FY_Pu239'))] if h)
check('P40 empreintes données embarquées', emb_ok)

# ---- 4. RE-RUN P51 (si NPZ disponible) ----
npz = Path('/tmp/local_camp/data/sleep_edf_segments.npz')
if npz.exists():
    d = WORK / 'p51'; (d / 'data').mkdir(parents=True, exist_ok=True)
    shutil.copy(fetch('src/p51_sleep_ash.py'), d / 'p51_sleep_ash.py')
    shutil.copy(npz, d / 'data' / 'sleep_edf_segments.npz')
    published51 = json.loads(Path(fetch('data/p51_verdict.json')).read_text())
    r = subprocess.run([sys.executable, 'p51_sleep_ash.py', 'data/sleep_edf_segments.npz'],
                       cwd=d, capture_output=True, text=True)
    rerun51 = json.loads((d / 'data' / 'p51_verdict.json').read_text())
    keys = ['accuracy_globale', 'pairs_separees_70plus', 'pair_accuracies', 'verdict',
            'levier_discriminant', 'sha256', 'n_segments']
    diffs = [k for k in keys if rerun51.get(k) != published51.get(k)]
    check('RE-RUN P51', not diffs and r.returncode == 0,
          f'accuracy={rerun51.get("accuracy_globale")} verdict={rerun51.get("verdict")}'
          + (f' ÉCARTS: {diffs}' if diffs else ''))
else:
    check('RE-RUN P51', False, 'NPZ non disponible — en attente')

ok = all(c['ok'] for c in report['checks'])
report['verdict'] = 'REPRODUCTIBLE' if ok else 'ÉCART'
out = Path('/tmp/local_camp/data/i3_ci_verdicts.json')
json.dump(report, open(out, 'w'), indent=2, ensure_ascii=False)
print('VERDICT I3 :', report['verdict'], '->', out)
