import re, sys

def region(s, name):
    m = re.search(r"^" + re.escape(name) + r":$", s, re.M)
    if not m: return ""
    start = m.start()
    nxt = s.find("\n\t.section", start)
    if nxt == -1: nxt = s.find("\n.section", start)
    if nxt == -1: nxt = len(s)
    return s[start:nxt]

funcs = {
    "naive_mul": "_ZN2fp7FpNaiveILj4294966177EE3mulEjj",
    "naive_sub": "_ZN2fp7FpNaiveILj4294966177EE3subEjj",
    "naive_inv": "_ZN2fp7FpNaiveILj4294966177EE3invEj",
    "barrett_mul": "_ZN2fp9FpBarrettILj4294966177EE3mulEjj",
    "barrett_red": "_ZN2fp9FpBarrettILj4294966177EE8reduce64Ey",
    "mont_mul": "_ZN2fp6FpMontILj4294966177EE3mulEjj",
    "pseudo_mul": "_ZN2fp8FpPseudoILj4294966177EE3mulEjj",
    "pseudo_red": "_ZN2fp8FpPseudoILj4294966177EE8reduce64Ey",
    "naive_dbl": "_ZN2ec8JacobianIN2fp7FpNaiveILj4294966177EEEE3dblERKS4_",
    "mont_dbl":  "_ZN2ec8JacobianIN2fp6FpMontILj4294966177EEEE3dblERKS4_",
    "pseudo_dbl":"_ZN2ec8JacobianIN2fp8FpPseudoILj4294966177EEEE3dblERKS4_",
    "barrett_dbl":"_ZN2ec8JacobianIN2fp9FpBarrettILj4294966177EEEE3dblERKS4_",
}
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
print(f"{'func':14s} {'len':>5s} {'mul':>4s} {'imul':>5s} {'div':>4s} {'idiv':>4s} {'call':>5s} {'jmp'  :>4s} {'branch':>6s} {'cmov':>5s} {'spill':>5s} {'mem_ld':>6s}")
for tag, f in funcs.items():
    body = region(s, f)
    if not body:
        print(f"{tag:14s} <missing>"); continue
    ins = re.findall(r"^\s+([a-z][a-z0-9]*)\b", body, re.M)
    inp = " ".join(ins)
    def cnt(sfx):
        pat = r"^" + sfx.split("|")[0]
        return len(re.findall(r"\b(?:%s)\b" % "|".join(sfx.split("|")), inp, re.M))
    n_mul = len(re.findall(r"\bmulq\b|\bmull?\b", inp))
    n_imul = len(re.findall(r"\bimul\w*\b", inp))
    n_div = len(re.findall(r"\bdivq?\b|\bdivl\b", inp))
    n_idiv = len(re.findall(r"\bidiv\w*\b", inp))
    n_call = len(re.findall(r"\bcall\b", inp))
    n_jmp = len(re.findall(r"\bjmp\b", inp))
    n_branch = len(re.findall(r"\bj[a-z]*\b", inp, re.M))
    n_cmov = len(re.findall(r"\bcmov\w*\b", inp))
    n_spill = len(re.findall(r"\(\s*%[er]sp|\(\s*%[er]bp|rsp\),|rbp\),", body))
    n_mem = len(re.findall(r"\(%[er][abcdsib]{2}\)|\(%[er]x\)|\(%[er]bp\)|\(%rdi\)|\(%rsi\)|\(%rdx\)", body))
    # proper instruction-level census lines (matching indented mnemonics)
    print(f"{tag:14s} {len(body.splitlines()):5d} {n_mul:4d} {n_imul:5d} {n_div:4d} {n_idiv:4d} {n_call:5d} {n_jmp:4d} {n_branch:6d} {n_cmov:5d} {n_spill:5d} {n_mem:6d}")