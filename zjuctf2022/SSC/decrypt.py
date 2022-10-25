em = r'PPP{D_ckvpfc_Ovri_tepc_repnn_hi_cew_poifgr_Udk_cew_fimniqc_du_ckvce_af}'
m = ''
rules = {
    'c': 't',
    'd': 'o',
    'k': 'r',
    'v': 'u',
    'f': 'n',
    'p': 'a',
}

for c in em:
    if c in rules:
        m += rules[c]
    elif c.lower() in rules:
        m += rules[c.lower()].upper()
    else:
        m += c

print(m)