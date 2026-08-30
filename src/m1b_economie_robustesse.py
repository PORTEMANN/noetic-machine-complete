"""M1b — Robustesse de l'inversion mesurée en M1  [ECO-1.1 gelé]

Contexte : M1 (ECO-1.0) a RÉFUTÉ la prédiction brute « le ratio V/S
s'effondre à r₁₂ » avec INVERSION mesurée (médiane ρ F > NF sur les deux
métriques). Objection possible : le SLOC est un mauvais proxy de la
longueur de Kolmogorov de S.

PRÉDICTION PRÉ-ENREGISTRÉE (gelée avant calcul, annoncée dans la note M1) :
  « l'inversion devrait survivre [au changement de métrique], parce que
   son mécanisme (diagnostics minimaux à la frontière) est structurel ».
  Opérationnellement : médiane(ρ|F) > médiane(ρ|NF) sur ρ₁ ET ρ₂ avec
  S = taille gzip du script.

PROTOCOLE ECO-1.1 (gelé)
========================
Identique à ECO-1.0 (même corpus, mêmes exclusions, mêmes V₁ et V₂,
même groupe frontière F = {P31, P32, P33, P39}, même critère médiane+Q3),
SAUF :
  S₂ = taille en octets du script compressé gzip (niveau 9, mtime=0 —
       déterministe). Proxy de Kolmogorov plus fidèle que le SLOC (le
       SLOC compte les lignes ; gzip compte l'information réelle,
       redondance déduite).
Contrôle interne gelé : corrélation de rang (Spearman) entre SLOC et S₂
sur tout le corpus — si ρ_s < 0.5, les deux métriques racontent des
histoires trop différentes pour que le test soit un contrôle de
robustesse (B3-FAIL protocole déclaré, verdict suspendu).
Enrichissement descriptif (sans critère, déclaré) : V₃ = nombre de
littéraux numériques DISTINCTS dans la source du script (tokens NUMBER
via tokenize, 0/1/2 exclus — bruit syntaxique), proxy des données
embarquées dans S.

Falsifieur : si l'inversion disparaît (médiane F ≤ médiane NF sur l'une
des deux métriques S₂), la prédiction ci-dessus tombe et le verdict M1
devient « réfutation fragile » — publié comme tel.
"""
import base64
import gzip
import hashlib
import json
import re
import tokenize
from io import BytesIO
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "m1_corpus"

FRONTIERE = {"P31", "P32", "P33", "P39"}          # gelé, identique à M1
EXCLUS_V1 = {"P28"}
CLES_EXCLUES = re.compile(r"(sha|empreinte|date|^tag$)", re.I)

LOCAUX = {f"P{n}": (f"p{n}_{suf}.py", f"p{n}_{suf}_verdict.json")
          for n, suf in [(34, "neurone"), (35, "neurone_biologique"),
                         (36, "profondeur"), (37, "neurone_fractionnaire"),
                         (38, "attention"), (39, "fermeture_r12"),
                         (40, "zmax"), (41, "neurones_reels"),
                         (42, "pont_120_e8")]}
CLES_TESTS = {"P34": ["verdicts_C1"], "P39": None}
VOLETS_P39 = ["T1_réfutation_intégrande_P31",
              "volet_A_cellules_hors_domaine_rejugées",
              "volet_B_H-_et_Ps-", "volet_C_série_Z7_10"]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sloc(source):
    return sum(1 for l in source.splitlines()
               if l.strip() and not l.strip().startswith("#"))


def s_gzip(source):
    return len(gzip.compress(source.encode("utf-8"), compresslevel=9,
                             mtime=0))


def litteraux_numeriques(source):
    """V₃ : littéraux numériques distincts, 0/1/2 exclus."""
    vals = set()
    try:
        lignes = iter(source.splitlines(keepends=True))
        for tok in tokenize.generate_tokens(lambda: next(lignes)):
            if tok.type == tokenize.NUMBER:
                s = tok.string
                if "j" in s or "J" in s:
                    continue
                try:
                    v = float(s.replace("_", ""))
                except ValueError:
                    continue
                if v not in (0.0, 1.0, 2.0):
                    vals.add(s)
    except (tokenize.TokenError, IndentationError, SyntaxError,
            StopIteration):
        pass
    return len(vals)


def source_corpus(f):
    brut = Path(f).read_bytes()
    try:
        txt = brut.decode("utf-8")
        if txt.lstrip().startswith(('"""', "#", "import", "from")):
            return txt, False
    except UnicodeDecodeError:
        pass
    try:
        return base64.b64decode(brut).decode("utf-8"), True
    except Exception:
        return brut.decode("utf-8", errors="replace"), False


def feuilles(o, acc, cle=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if CLES_EXCLUES.search(str(k)):
                continue
            feuilles(v, acc, k)
    elif isinstance(o, list):
        for v in o:
            feuilles(v, acc, cle)
    elif isinstance(o, bool):
        return
    elif isinstance(o, (int, float)):
        acc.append(o)
    elif isinstance(o, str):
        s = o.strip()
        try:
            float(s)
            acc.append(s)
            return
        except ValueError:
            pass
        if re.fullmatch(r"-?\d+/\d+", s):
            acc.append(s)


def scores_readme(texte):
    out = {}
    for m in re.finditer(r"\|\s*(P\d+)\s*\|[^|]+\|\s*(\d+)/(\d+)\s*\|",
                         texte):
        out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def spearman(xs, ys):
    def rangs(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0 + 1
            i = j + 1
        return r
    rx, ry = rangs(xs), rangs(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    return cov / (vx * vy) ** 0.5 if vx and vy else 0.0


def main():
    print("M1b — ROBUSTESSE DE L'INVERSION   [ECO-1.1 gelé]")
    print("=" * 72)
    print("Prédiction pré-enregistrée : l'inversion (médiane ρ F > NF)")
    print("survit au changement S SLOC → S gzip.")

    readme = (CORPUS / "README.md").read_text(encoding="utf-8")
    tab = scores_readme(readme)
    mesures, b3 = {}, []

    for n in range(20, 34):
        cid = f"P{n}"
        if cid not in tab:
            continue
        scripts = sorted(CORPUS.glob(f"src/p{n}_*.py"))
        jsons = sorted(CORPUS.glob(f"data/p{n}_*.json"))
        if not scripts:
            b3.append(f"{cid} : script absent — chantier sauté")
            continue
        src, _ = source_corpus(scripts[0])
        acc = []
        for j in jsons:
            if "protocole" in j.name:
                continue
            try:
                feuilles(json.loads(j.read_text(encoding="utf-8")), acc)
            except json.JSONDecodeError:
                b3.append(f"{cid} : JSON illisible {j.name}")
        succ, deno = tab[cid]
        mesures[cid] = {"S_sloc": sloc(src), "S_gzip": s_gzip(src),
                        "V3_littéraux": litteraux_numeriques(src),
                        "V1_feuilles": None if cid in EXCLUS_V1
                        else len(acc),
                        "V2_confrontations": deno, "succes": succ,
                        "sha_script_mesuré": hashlib.sha256(
                            src.encode()).hexdigest()}

    for cid, (script, vjson) in LOCAUX.items():
        fp, fv = HERE / script, HERE / vjson
        if not fp.exists() or not fv.exists():
            b3.append(f"{cid} : artefact local absent — chantier sauté")
            continue
        src = fp.read_text(encoding="utf-8")
        d = json.loads(fv.read_text(encoding="utf-8"))
        acc = []
        feuilles(d, acc)
        if cid == "P39":
            deno = sum(1 for k in VOLETS_P39 if k in d)
        else:
            vdict = {}
            for k in (CLES_TESTS.get(cid) or ["verdicts"]):
                v = d.get(k)
                if isinstance(v, dict):
                    vdict.update(v)
            deno = len(vdict)
        mesures[cid] = {"S_sloc": sloc(src), "S_gzip": s_gzip(src),
                        "V3_littéraux": litteraux_numeriques(src),
                        "V1_feuilles": len(acc),
                        "V2_confrontations": deno, "succes": None,
                        "sha_script_mesuré": sha256(fp)}

    # ---- contrôle interne : SLOC vs gzip ---------------------------------
    ids = sorted(mesures, key=lambda c: int(c[1:]))
    rs = spearman([mesures[c]["S_sloc"] for c in ids],
                  [mesures[c]["S_gzip"] for c in ids])
    controle_metrique = rs >= 0.5
    print(f"\nC0  Spearman(SLOC, gzip) = {rs:.3f} — contrôle "
          f"{'PASS' if controle_metrique else 'FAIL — B3-FAIL protocole'}")

    # ---- ratios S₂ et critère gelé ----------------------------------------
    def med(xs):
        xs = sorted(xs)
        n = len(xs)
        return (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2)

    def q3(xs):
        xs = sorted(xs)
        return xs[int(0.75 * (len(xs) - 1))]

    print(f"\n{'ch.':<5} {'S_gz':>5} {'V₁':>5} {'V₂':>3} {'V₃':>4} "
          f"{'ρ₁′':>6} {'ρ₂′':>6}  groupe")
    for cid in ids:
        m = mesures[cid]
        S2 = m["S_gzip"]
        m["rho1_gz"] = (m["V1_feuilles"] / S2) if m["V1_feuilles"] else None
        m["rho2_gz"] = m["V2_confrontations"] / S2
        g = "FRONTIÈRE" if cid in FRONTIERE else "discret"
        print(f"{cid:<5} {S2:>5} {str(m['V1_feuilles']):>5} "
              f"{m['V2_confrontations']:>3} {m['V3_littéraux']:>4} "
              f"{m['rho1_gz'] if m['rho1_gz'] is not None else float('nan'):>6.3f}"
              f" {m['rho2_gz']:>6.3f}  {g}")

    F = [c for c in mesures if c in FRONTIERE]
    NF = [c for c in mesures if c not in FRONTIERE]
    resultats = {}
    for cle in ("rho1_gz", "rho2_gz"):
        vf = [mesures[c][cle] for c in F if mesures[c][cle] is not None]
        vn = [mesures[c][cle] for c in NF if mesures[c][cle] is not None]
        inversion = med(vf) > med(vn)
        resultats[cle] = {"médiane_F": med(vf), "médiane_NF": med(vn),
                          "max_F": max(vf), "Q3_NF": q3(vn),
                          "inversion_survit": inversion}
        print(f"\n{cle}  médiane F = {med(vf):.4f} vs NF = {med(vn):.4f}"
              f" → inversion {'SURVIT' if inversion else 'DISPARAIT'}")

    survie = all(resultats[c]["inversion_survit"] for c in resultats)
    prediction = "CONFIRMÉE" if (survie and controle_metrique) else \
        "RÉFUTÉE" if controle_metrique else "SUSPENDUE (contrôle métrique FAIL)"
    if not controle_metrique:
        b3.append("protocole : Spearman(SLOC, gzip) < 0.5 — les deux "
                  "métriques de S divergent trop, le test de robustesse "
                  "n'est pas valide (verdict suspendu)")

    verdict_global = (
        f"Robustesse de l'inversion M1 au proxy de Kolmogorov gzip : "
        f"prédiction {prediction}. ρ₁′ médiane F "
        f"{resultats['rho1_gz']['médiane_F']:.4f} vs NF "
        f"{resultats['rho1_gz']['médiane_NF']:.4f} ; ρ₂′ médiane F "
        f"{resultats['rho2_gz']['médiane_F']:.4f} vs NF "
        f"{resultats['rho2_gz']['médiane_NF']:.4f} ; Spearman(SLOC, gzip) "
        f"= {rs:.3f}. L'inversion est structurelle : elle ne dépend pas "
        f"du compteur de longueur choisi."
        if prediction == "CONFIRMÉE" else
        f"L'inversion M1 NE survit PAS au changement de métrique "
        f"(prédiction {prediction}) — la réfutation de M1 est fragile, "
        f"publié comme tel.")

    out = {
        "chantier": "M1B-ECONOMIE-ROBUSTESSE",
        "protocole": "ECO-1.1 (gelé) — identique à ECO-1.0 sauf S = "
                     "taille gzip du script (niveau 9, mtime=0) ; contrôle "
                     "Spearman(SLOC, gzip) ≥ 0.5 ; V₃ littéraux descriptif",
        "prédiction_pré_enregistrée": "l'inversion (médiane ρ F > NF) "
                                      "survit au changement de métrique S",
        "données": {"mêmes_que_M1": "m1_corpus miroir SHA-vérifié + "
                                    "verdicts locaux P34–P42"},
        "mesures": mesures,
        "contrôle_métrique": {"spearman_sloc_gzip": rs,
                              "seuil": 0.5, "pass": controle_metrique},
        "ratios_critères": resultats,
        "verdicts": {"C0_contrôle_métrique": controle_metrique,
                     "inversion_ρ₁′_survit": resultats["rho1_gz"]["inversion_survit"],
                     "inversion_ρ₂′_survit": resultats["rho2_gz"]["inversion_survit"]},
        "verdict_global": verdict_global,
        "prédiction": prediction,
        "comptage_ddll": {"verdict": "déficit",
                          "justification": "le proxy gzip et le seuil de "
                          "contrôle 0.5 sont des conventions payées une "
                          "fois, gelées avant calcul"},
        "b3_fail": b3,
        "falsifieur": "l'inversion disparaît sur l'une des deux métriques "
                      "gzip → la réfutation M1 était fragile (publié)",
        "sha256_script": hashlib.sha256(Path(__file__).read_bytes())
        .hexdigest(),
    }
    out_path = HERE / "m1b_economie_robustesse_verdict.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("\n" + "-" * 72)
    print("VERDICT :", verdict_global)
    print(f"PRÉDICTION : {prediction}   |   SHA-256 : "
          f"{out['sha256_script'][:16]}…   |   {out_path.name}")


if __name__ == "__main__":
    main()
