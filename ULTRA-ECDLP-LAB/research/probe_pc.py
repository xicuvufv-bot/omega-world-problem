# -*- coding: utf-8 -*-
import random, sys
exec(open(r"C:\Users\Administrator\Documents\Default Project\ULTRA-ECDLP-LAB\research\prime_scaling_run.py", encoding="utf-8").read().split("def main():")[0])

# quick sanity: count orders for primes near 1024
from collections import Counter
cnt = Counter()
hits = []
for p in (1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097,
          1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193):
    l = count_curve_order(p)
    cnt[_is_prime(l)] += 1
    if _is_prime(l):
        hits.append((p, l))
print("prime-l hits:", hits)
print("distribution prime/non:", dict(cnt))

# try prime_group directly
try:
    print("prime_group(10):", prime_group(10, 20260931))
except Exception as e:
    print("prime_group(10) FAILED:", type(e).__name__, e)