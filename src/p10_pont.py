#!/usr/bin/env python3
# P10 - pont ANU <-> cartes d'identite : 3 livrables.
# (1) Table periodique annotee : N_ANU, N/18, masse moderne, + carte machine
#     (R_c=r0 A^(1/3), hiérarchie Rc/a0) a l'A le plus proche de N/18.
# (2) Test des ecarts : les 8 pires ecarts N/18 vs masse -> structure isotopique ?
#     On teste si N/18 pointe vers l'isotope DOMINANT (entier A_dom) plutot que la
#     moyenne ponderee (masse standard) : si oui, l'ecart est une structure.
# (3) Meta-elements : correspondance meta-comptage <-> isotope precis (P7-like).
import os, json
import numpy as np

R0FM=1.2; CONV=3.04/0.84; A0=137.036
audit=json.load(open('/mnt/agents/output/e44_data/audit_constat_anu_masse.json'))
T=audit['table']

def carte(A):
    Rc=R0FM*A**(1.0/3.0)*CONV
    return {"R_c_mailles":Rc,"R_c_fm":Rc/CONV,"hierarchie":Rc/A0}

# isotopes dominants (A le plus abondant naturellement) pour le test des ecarts
ISO_DOM={"N":14,"Si":28,"S":32,"Cl":35,"Ar":40,"K":39,"Ca":40,"Ti":48,"Cr":52,
         "Fe":56,"Ni":58,"Cu":63,"Zn":64,"Kr":84,"Nb":93,"Mo":98,"Sn":120,
         "Te":130,"Xe":132,"Sm":152,"Eu":153,"Gd":158,"Pt":195,"Au":197,
         "Hg":202,"Pb":208,"At":210,"O":16,"C":12,"Ne":20}

# --- Livrable 1 : table annotee ---
table=[]
for row in T:
    sym,Z,N,N18,masse=row[0],row[1],row[2],row[3],row[4]
    A_near=int(round(N18))
    ecart_pct=(N18-masse)/masse*100
    c=carte(A_near)
    table.append({"sym":sym,"Z":Z,"N_ANU":N,"N18":N18,"masse":masse,
                  "A_near":A_near,"ecart_pct":ecart_pct,
                  "R_c_fm":c["R_c_fm"],"hierarchie":c["hierarchie"]})
print(f"[P10] table annotee : {len(table)} elements construits",flush=True)

# --- Livrable 2 : test des ecarts ---
# les 8 pires ecarts (audit) : structure isotopique ?
pires=audit['pires_ecarts']
test_ecarts=[]
for row in T:
    sym=row[0]
    if sym in pires:
        N18=row[3]; masse=row[4]
        A_dom=ISO_DOM.get(sym)
        if A_dom:
            # ecart vs moyenne (masse standard) vs ecart vs isotope dominant
            e_moy=(N18-masse)/masse*100
            e_dom=(N18-A_dom)/A_dom*100
            verdict="STRUCTURE (isotope dominant)" if abs(e_dom)<abs(e_moy) else "BRUIT/ambigu"
            test_ecarts.append({"sym":sym,"N18":N18,"masse":masse,"A_dom":A_dom,
                "ecart_vs_moyenne":e_moy,"ecart_vs_isotope_dom":e_dom,"verdict":verdict})
            print(f"[P10 ecart] {sym:3} N/18={N18:6.2f} masse={masse:7.3f} A_dom={A_dom:3} "
                  f"e_moy={e_moy:+5.2f}% e_dom={e_dom:+5.2f}% -> {verdict}",flush=True)

# --- Livrable 3 : meta-elements ---
meta=audit['meta_elements_isotopes']
test_meta=[]
for name,info in meta.items():
    N=info['N']; N18=info['N/18']
    # l'isotope pointe (cle != 'note')
    iso=[k for k in info.keys() if k not in ('N','N/18','note')]
    iso_pt=iso[0] if iso else None
    iso_val=info[iso_pt] if iso_pt else None
    note=info.get('note','')
    # la machine : A le plus proche de N/18 -> carte
    A_near=int(round(N18))
    c=carte(A_near)
    test_meta.append({"meta":name,"N":N,"N18":N18,"isotope_pointe":iso_pt,
        "A_near":A_near,"note":note,"R_c_fm":c["R_c_fm"]})
    print(f"[P10 meta ] {name:14} N={N:5} N/18={N18:6.2f} -> A~{A_near:3} "
          f"(isotope pointe {iso_pt}={iso_val}) R_c={c['R_c_fm']:.2f} fm  {note}",flush=True)

json.dump({"table":table,"test_ecarts":test_ecarts,"test_meta":test_meta,
           "controle_nul":audit['controle_nul'],"rms_audit":audit['rms_relatif_pct']},
          open("/mnt/agents/output/e44_data/p10_pont.json","w"),indent=1)
print("[P10] sauve",flush=True)
