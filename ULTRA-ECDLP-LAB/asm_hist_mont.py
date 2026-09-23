import re, sys
from collections import Counter
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
key = sys.argv[2]
if key == "FpNaive": pat = "_Z8bench_ecIN2fp7FpNaive"
elif key == "FpMont": pat = "_Z8bench_ecIN2fp6FpMont"
elif key == "FpBarrett": pat = "_Z8bench_ecIN2fp9FpBarrett"
else: pat = "_Z8bench_ecIN2fp8FpPseudo"
idx = s.find(pat)
if idx == -1:
    print("not found", key); sys.exit()
start = s.rfind("\n", 0, idx)+1
end = s.find("\n.section", idx)
if end == -1: end = len(s)
body = s[start:end]
ins = re.findall(r"^\t([a-z][a-z0-9]*)\b", body, re.M)
c = Counter(ins)
rel = {"imulq":"imulq(64)","mulq":"mulq(128)","shrq":"shrq","adcq":"adcq","shrdq":"shrdq","idivq":"idivq","divq":"divq","call":"call","jnb":"jnb","jb":"jb","je":"je","jne":"jne","js":"js","jg":"jg","ja":"ja","jbe":"jbe","cmovb":"cmovb","cmovnb":"cmovnb","cmova":"cmova","cmovbe":"cmovbe","cmovs":"cmovs","cmovns":"cmovns","movq":"movq","movl":"movl","movzbl":"movzbl","movabsq":"movabsq","leaq":"leaq","leal":"leal","addq":"addq","addl":"addl","subl":"subl","subq":"subq","xorl":"xorl","andl":"andl","vpand":"vpand","vpmulld":"vpmulld","vpsrld":"vpsrld","vpxor":"vpxor"}
print(f"=== bench_ec<{key}> total ins: {len(ins)} ===")
for k in ("mulq","imulq","shrq","adcq","shrdq","idivq","divq","call","jnb","jb","je","jne","js","jg","ja","jbe","cmovb","cmovnb","cmova","cmovbe","cmovs","cmovns","movq","movl","movabsq","leaq","leal","addq","addl","subl","subq","xorl","andl","vpand","vpmulld","vpsrld","vpxor"):
    if c[k]: print(f"  {k:10s} {c[k]}")