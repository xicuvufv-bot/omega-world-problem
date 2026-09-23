import re, sys

def extract(sfile, name):
    s = open(sfile, encoding="utf-8", errors="replace").read()
    pat = re.compile(r"^" + re.escape(name) + r":$", re.M)
    m = pat.search(s)
    if not m: return None
    lines = s[m.start():].split("\n")
    out = []
    for ln in lines[1:]:
        t = ln.strip()
        if re.match(r"^[A-Za-z_]", ln) and not t.startswith((".", "L", "SEH", "ret", "jmp")):
            # a new local function label region starting
            if re.search(r":", ln) and not ln.strip().startswith("L") and "def" not in ln and "proc" not in ln:
                break
        out.append(ln)
        if t.startswith("ret") and out:
            # keep until next blank then stop at next non-. label
            pass
    return "\n".join(out)

# jacobian dbl for each field
names = {
    "jac_dbl_naive": "_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS3_",
    "jac_dbl_barrett": "_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS3_",
    "jac_dbl_mont": "_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS3_",
    "jac_dbl_pseudo": "_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS3_",
    "inv_naive": "_ZN2fp7FpNaiveILj4294966177EE3invEj",
    "inv_mont": "_ZN2fp6FpMontILj4294966177EE3invEj",
}
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for tag, f in names.items():
    m = re.search(r"^" + re.escape(f) + r":$", s, re.M)
    if not m:
        print(f"===== {tag}: <NOT FOUND> ({f})")
        continue
    # collect until next .def/.globl for a _Z function
    end = s.find("\n.section", m.start())
    if end == -1: end = len(s)
    body = s[m.start():end]
    print(f"===== {tag} =====")
    print(body[:3500])
    print()