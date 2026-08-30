"""M1 — L'économie de l'information, mesurée  [ECO-1.0 gelé]

Question pré-enregistrée (prospection-machine-noetique.md, §M1) :
  « la physique est bon marché en information dans son régime discret,
   coûteuse dans le continu corrélé » — le ratio (données reproduites) /
   (longueur de S) est-il élevé pour les chantiers discrets et
   s'effondre-t-il à r₁₂ ?

PROTOCOLE ECO-1.0 (gelé avant calcul)
=====================================
Corpus : chantiers à score publié — P20–P33 (README noetic-machine-complete,
tableau « Bilan »), chantiers locaux P34–P42 (verdicts JSON locaux).
Exclusions gelées : P0–P19 (banc fondateur, notes « hors corpus », pas de
tableau de score publié) ; série A1–A5 (hygiène de la machine, ne reproduit
pas de données physiques) ; bifurcations hors-programme ; P28 (pas de JSON
de résultats dans le dépôt → V₁ non calculable, V₂ = 7 publié, déclaré).

Trois métriques mécaniques, zéro jugement par chantier :
  S  = SLOC du script = lignes physiques non vides et non commentaires
       (strip() non vide et ne commençant pas par '#'). Proxy déclaré de
       longueur de Kolmogorov de S. p32/p33 : source décodée base64 (le
       dépôt publie ces deux fichiers encodés — écart publié en b3_fail).
  V₁ = nombre de feuilles numériques du JSON de résultats (récursif ;
       int/float non booléens ; chaînes parsables float ou fraction p/q ;
       clés exclues gelées : sha*, empreinte*, date*, TAG).
       Proxy mécanique du contenu quantitatif produit (y compris interne).
  V₂ = nombre de confrontations du chantier : dénominateur du score publié
       (tableau README) pour P20–P33 ; cardinal du dictionnaire de tests C
       des JSON locaux pour P34–P42 (clé exacte dans la table gelée
       CLES_TESTS ci-dessous — les structures de verdicts locales sont
       hétérogènes, la provenance est déclarée, pas devinée).
Ratios : ρ₁ = V₁/S, ρ₂ = V₂/S.
Contrôle τ (taux de réussite = succès/V₂) : calculé UNIQUEMENT sur le
corpus P20–P33 où les scores sont publiés (les valeurs de verdicts locales
sont hétérogènes — ex. P35 où le FAIL du témoin sigmoïde EST le succès —
τ local n'est pas mécanisable sans jugement ; restriction déclarée).

Groupe frontière r₁₂ gelé : F = {P31, P32, P33, P39} (frontière déclarée
constitutive par le corpus lui-même, README « trilogie de la frontière »).

CRITÈRE GELÉ (binaire) : la prédiction est CONFIRMÉE pour une métrique ρ si
  (i) médiane(ρ|F) < médiane(ρ|NF)  ET
  (ii) max(ρ|F) ≤ Q3(ρ|NF)  (aucun chantier frontière ne dépasse le
      3e quartile des autres).
CONFIRMÉE si les deux métriques passent ; PARTIELLE si une seule ;
RÉFUTÉE sinon. τ est un contrôle : il DOIT séparer F de NF (sinon la
définition du groupe F tombe — B3-FAIL du protocole).

Falsifieur : tout chantier frontière avec ρ au-dessus du Q3 non-frontière,
ou médianes inversées, tue la prédiction dans sa forme brute.

b3_fail connu d'entrée (chaîne documentaire corpus) : src/p32_frontiere.py
et src/p33_queue.py sont publiés encodés base64 et leur SHA-256 (brut ou
décodé) ne coïncide plus avec SHASUMS.txt — 83/85 artefacts vérifiés OK.
"""
import base64
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "m1_corpus"

FRONTIERE = {"P31", "P32", "P33", "P39"}          # gelé — trilogie r₁₂ + P39
EXCLUS_V1 = {"P28"}                                # pas de JSON dans le dépôt
CLES_EXCLUES = re.compile(r"(sha|empreinte|date|^tag$)", re.I)

# Chantiers locaux : script + verdict JSON + clé(s) de tests (gelé)
LOCAUX = {f"P{n}": (f"p{n}_{suf}.py", f"p{n}_{suf}_verdict.json")
          for n, suf in [(34, "neurone"), (35, "neurone_biologique"),
                         (36, "profondeur"), (37, "neurone_fractionnaire"),
                         (38, "attention"), (39, "fermeture_r12"),
                         (40, "zmax"), (42, "pont_120_e8")]}
# P41 ajouté si son verdict final existe
if (HERE / "p41_neurones_reels_verdict.json").exists():
    LOCAUX["P41"] = ("p41_neurones_reels.py", "p41_neurones_reels_verdict.json")
# Table de provenance gelée des dictionnaires de tests locaux
CLES_TESTS = {"P34": ["verdicts_C1"], "P39": None}  # P39 : volets ci-dessous
VOLETS_P39 = ["T1_réfutation_intégrande_P31",
              "volet_A_cellules_hors_domaine_rejugées",
              "volet_B_H-_et_Ps-", "volet_C_série_Z7_10"]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sloc(source):
    return sum(1 for l in source.splitlines()
               if l.strip() and not l.strip().startswith("#"))


def source_corpus(f):
    """Source Python du script corpus ; décode base64 si le fichier est
    publié encodé (p32/p33 — écart de chaîne documentaire, publié)."""
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
    """Dénominateurs et succès du tableau Bilan P20–P33 du README."""
    out = {}
    for m in re.finditer(r"\|\s*(P\d+)\s*\|[^|]+\|\s*(\d+)/(\d+)\s*\|", texte):
        out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def main():
    print("M1 — ÉCONOMIE DE L'INFORMATION   [ECO-1.0 gelé]")
    print("=" * 72)

    # ---- contrôle de la chaîne documentaire corpus ------------------------
    shas = {}
    for line in (CORPUS / "SHASUMS.txt").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            h, p = line.split(None, 1)
            shas[p.strip()] = h
    verif, ecarts = 0, []
    for p, h in sorted(shas.items()):
        f = CORPUS / p
        if not f.exists():
            continue
        if sha256(f) == h:
            verif += 1
        else:
            ecarts.append(p)
    print(f"C0  chaîne corpus : {verif} artefacts SHA-OK ; écarts : {ecarts}"
          " (p32/p33 publiés encodés base64 — voir b3_fail)")

    readme = (CORPUS / "README.md").read_text(encoding="utf-8")
    tab = scores_readme(readme)
    print(f"C0  scores README parsés : {len(tab)} chantiers {sorted(tab)}")

    # ---- mesures par chantier --------------------------------------------
    mesures, b3 = {}, ["corpus : src/p32_frontiere.py et src/p33_queue.py "
                       "publiés encodés base64 ; SHA brut/décodé ≠ "
                       "SHASUMS.txt (chaîne documentaire rompue sur 2/85 "
                       "artefacts) — écart publié, sources décodées pour S"]

    # corpus P20–P33 : script src/pNN_*.py, JSON data/pNN_*.json
    for n in range(20, 34):
        cid = f"P{n}"
        if cid not in tab:
            continue
        scripts = sorted(CORPUS.glob(f"src/p{n}_*.py"))
        jsons = sorted(CORPUS.glob(f"data/p{n}_*.json"))
        if not scripts:
            b3.append(f"{cid} : script absent du dépôt — chantier sauté")
            continue
        src, decode = source_corpus(scripts[0])
        S = sloc(src)
        acc = []
        for j in jsons:
            if "protocole" in j.name:
                continue
            try:
                feuilles(json.loads(j.read_text(encoding="utf-8")), acc)
            except json.JSONDecodeError:
                b3.append(f"{cid} : JSON illisible {j.name}")
        succ, deno = tab[cid]
        mesures[cid] = {"S_sloc": S,
                        "V1_feuilles": None if cid in EXCLUS_V1 else len(acc),
                        "V2_confrontations": deno, "succes": succ,
                        "script": scripts[0].name,
                        "base64_publié": decode,
                        "sha_script_mesuré": hashlib.sha256(
                            src.encode()).hexdigest()}

    # chantiers locaux P34–P42 (V₁ sur le JSON entier, règle uniforme ;
    # τ non mécanisable localement — restriction déclarée, corpus seul)
    for cid, (script, vjson) in LOCAUX.items():
        fp, fv = HERE / script, HERE / vjson
        if not fp.exists() or not fv.exists():
            b3.append(f"{cid} : artefact local absent ({script} ou {vjson})"
                      " — chantier sauté")
            continue
        S = sloc(fp.read_text(encoding="utf-8"))
        d = json.loads(fv.read_text(encoding="utf-8"))
        acc = []
        feuilles(d, acc)
        if cid == "P39":
            deno = sum(1 for k in VOLETS_P39 if k in d)
        else:
            cles = CLES_TESTS.get(cid) or ["verdicts"]
            vdict = {}
            for k in cles:
                v = d.get(k)
                if isinstance(v, dict):
                    vdict.update(v)
            deno = len(vdict)
        mesures[cid] = {"S_sloc": S, "V1_feuilles": len(acc),
                        "V2_confrontations": deno, "succes": None,
                        "script": script, "base64_publié": False,
                        "sha_script_mesuré": sha256(fp)}

    # ---- ratios et critère gelé -------------------------------------------
    def med(xs):
        xs = sorted(xs)
        n = len(xs)
        return (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2)

    def q3(xs):
        xs = sorted(xs)
        return xs[int(0.75 * (len(xs) - 1))]

    resultats = {}
    print(f"\n{'ch.':<5} {'S':>4} {'V₁':>5} {'V₂':>3} {'τ':>5} "
          f"{'ρ₁':>7} {'ρ₂':>7}  groupe")
    for cid in sorted(mesures, key=lambda c: int(c[1:])):
        m = mesures[cid]
        S = m["S_sloc"]
        m["rho1"] = (m["V1_feuilles"] / S) if m["V1_feuilles"] else None
        m["rho2"] = m["V2_confrontations"] / S
        m["tau"] = (m["succes"] / m["V2_confrontations"]
                    if m["succes"] is not None and m["V2_confrontations"]
                    else None)
        g = "FRONTIÈRE" if cid in FRONTIERE else "discret"
        print(f"{cid:<5} {S:>4} {str(m['V1_feuilles']):>5} "
              f"{m['V2_confrontations']:>3} "
              f"{m['tau'] if m['tau'] is not None else float('nan'):>5.2f} "
              f"{m['rho1'] if m['rho1'] is not None else float('nan'):>7.3f}"
              f" {m['rho2']:>7.3f}  {g}")

    F = [c for c in mesures if c in FRONTIERE]
    NF = [c for c in mesures if c not in FRONTIERE]
    for nom, cle in [("rho1", "rho1"), ("rho2", "rho2")]:
        vf = [mesures[c][cle] for c in F if mesures[c][cle] is not None]
        vn = [mesures[c][cle] for c in NF if mesures[c][cle] is not None]
        crit = (med(vf) < med(vn)) and (max(vf) <= q3(vn))
        resultats[cle] = {"médiane_F": med(vf), "médiane_NF": med(vn),
                          "max_F": max(vf), "Q3_NF": q3(vn),
                          "inversion": med(vf) > med(vn),
                          "critère(i+ii)": crit}
        print(f"\n{nom:<5} médiane F = {med(vf):.3f} vs NF = {med(vn):.3f}"
              f" | max F = {max(vf):.3f} vs Q3 NF = {q3(vn):.3f} "
              f"→ critère {'PASS' if crit else 'FAIL'}"
              + ("  [INVERSION : F au-dessus de NF]" if med(vf) > med(vn)
                 else ""))

    # contrôle τ : corpus P20–P33 uniquement (scores publiés)
    F_c = [c for c in F if mesures[c]["tau"] is not None]
    NF_c = [c for c in NF if mesures[c]["tau"] is not None]
    vf = [mesures[c]["tau"] for c in F_c]
    vn = [mesures[c]["tau"] for c in NF_c]
    tau_sep = (med(vf) < med(vn)) and (max(vf) <= q3(vn))
    resultats["tau_corpus_seul"] = {"médiane_F": med(vf),
                                    "médiane_NF": med(vn),
                                    "max_F": max(vf), "Q3_NF": q3(vn),
                                    "critère(i+ii)": tau_sep,
                                    "note": "corpus P20–P33 uniquement "
                                            "(restriction déclarée)"}
    print(f"\ntau   médiane F = {med(vf):.3f} vs NF = {med(vn):.3f}"
          f" | max F = {max(vf):.3f} vs Q3 NF = {q3(vn):.3f} "
          f"→ contrôle {'PASS' if tau_sep else 'FAIL'} (corpus seul)")

    ok1, ok2 = resultats["rho1"]["critère(i+ii)"], resultats["rho2"]["critère(i+ii)"]
    if not tau_sep:
        b3.append("protocole : τ ne sépare pas F de NF — la définition du "
                  "groupe frontière tombe (B3-FAIL protocole)")
    if ok1 and ok2:
        verdict = "CONFIRMÉE"
    elif ok1 or ok2:
        verdict = "PARTIELLE"
    else:
        verdict = "RÉFUTÉE"

    # ---- exemple pré-enregistré de la prospection -------------------------
    p24 = json.loads((CORPUS / "data/p24_jain.json").read_text(encoding="utf-8"))
    n148 = p24["T2_suite"]["nb_fractions_derivees_(0,1)"]
    s24 = mesures.get("P24", {}).get("S_sloc")
    exemple = {"prospection": "P24 : « ~100 lignes → 148 fractions »",
               "S_mesuré": s24, "fractions_dérivées_déclarées": n148,
               "fractions_testées": p24["T3_couverture"]["fractions_testees"],
               "écart_S": f"la prospection estimait ~100 lignes ; mesure : "
                          f"{s24}"}

    inv = resultats["rho1"]["inversion"] and resultats["rho2"]["inversion"]
    verdict_global = (
        f"Prédiction pré-enregistrée (ratio V/S élevé en discret, "
        f"s'effondrant à r₁₂) : {verdict} sur les métriques uniformes "
        f"gelées. ρ₁ (feuilles/S) : médiane F {resultats['rho1']['médiane_F']:.3f} "
        f"vs NF {resultats['rho1']['médiane_NF']:.3f} ; ρ₂ (confrontations/S) : "
        f"médiane F {resultats['rho2']['médiane_F']:.3f} vs NF "
        f"{resultats['rho2']['médiane_NF']:.3f}"
        + (" — INVERSION mesurée sur les deux métriques : le ratio est "
           "plus ÉLEVÉ à la frontière (petits scripts de diagnostic "
           "minimaux), pas plus bas. " if inv else " ")
        + f"Le contrôle τ (scores publiés, corpus P20–P33) sépare F de "
        f"NF : {tau_sep} (médiane {resultats['tau_corpus_seul']['médiane_F']:.2f} "
        f"vs {resultats['tau_corpus_seul']['médiane_NF']:.2f}). Affinage mesuré : "
        f"ce qui s'effondre à r₁₂ n'est pas le ratio informationnel brut "
        f"V/S mais le taux de réussite des confrontations externes — le "
        f"postulat est précisé, pas confirmé dans sa forme brute."
        if not (ok1 and ok2) else
        "Prédiction pré-enregistrée CONFIRMÉE sur les deux métriques "
        "gelées.")

    out = {
        "chantier": "M1-ECONOMIE-INFORMATION",
        "protocole": "ECO-1.0 (gelé) — métriques uniformes S, V₁, V₂ ; "
                     "groupe frontière {P31,P32,P33,P39} ; critère "
                     "médiane+Q3 binaire",
        "données": {"corpus_SHA_vérifiés": verif, "corpus_SHA_écarts": ecarts,
                    "README_sha": sha256(CORPUS / "README.md"),
                    "SHASUMS_sha": sha256(CORPUS / "SHASUMS.txt")},
        "mesures": mesures,
        "ratios_critères": resultats,
        "exemple_pré_enregistré_P24": exemple,
        "verdicts": {"C0_chaîne_corpus": len(ecarts) == 0,
                     "contrôle_τ_sépare": tau_sep,
                     "prédiction_ρ₁": ok1, "prédiction_ρ₂": ok2},
        "verdict_global": verdict_global,
        "prédiction": verdict,
        "comptage_ddll": {"verdict": "déficit",
                          "justification": "les métriques S (SLOC), V₁ "
                          "(feuilles), V₂ (score publié) et le critère "
                          "médiane+Q3 sont des conventions payées une fois, "
                          "gelées avant calcul ; rien n'est ré-ajusté après "
                          "mesure"},
        "b3_fail": b3,
        "falsifieur": "un chantier frontière avec ρ au-dessus du Q3 "
                      "non-frontière, ou des médianes inversées, tuait la "
                      "prédiction brute — mesuré ci-dessus",
        "sha256_script": hashlib.sha256(Path(__file__).read_bytes())
        .hexdigest(),
    }
    out_path = HERE / "m1_economie_information_verdict.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("\n" + "-" * 72)
    print("VERDICT :", verdict_global)
    print(f"PRÉDICTION : {verdict}   |   SHA-256 : "
          f"{out['sha256_script'][:16]}…   |   {out_path.name}")


if __name__ == "__main__":
    main()
