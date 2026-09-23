import re, sys, collections

def extract(sfile, name):
    s = open(sfile, encoding="utf-8", errors="replace").read()
    # find label line
    pat = re.compile(r"^" + re.escape(name) + r":$", re.M)
    m = pat.search(s)
    if not m:
        return None
    lines = s[m.start():].split("\n")
    out = []
    for ln in lines[1:]:
        if re.match(r"^[A-Za-z_.$].*:$", ln) and any(k in ln for k in ("_Z", ".text", ".def")):
            # only stop at a new global label
            if re.match(r"^[A-Za-z_]", ln) and not ln.strip().startswith((".", "L", "SEH")):
                break
        out.append(ln)
        if ln.strip().startswith("ret") or ln.strip().startswith("jmp"):
            pass
    return "\n".join(out)

names = {
    "naive_mul":  "_ZN2fp7FpNaiveILj4294966177EE3mulEjj",
    "naive_sub":  "_ZN2fp7FpNaiveILj4294966177EE3subEjj",
    "barrett_mul":"_ZN2fp9FpBarrettILj4294966177EE3mulEjj",
    "barrett_red":"_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey",
    "mont_mul":   "_ZN2fp6FpMontILj4294966177EE3mulEjj",
    "pseudo_mul": "_ZN2fp8FpPseudoILj4294966177EE3mulEjj",
    "pseudo_red": "_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey",
}

for tag, f in names.items():
    body = extract(sys.argv[1], f)
    print(f"===== {tag} : {f} =====")
    print(body if body else "<not found>")
    print()