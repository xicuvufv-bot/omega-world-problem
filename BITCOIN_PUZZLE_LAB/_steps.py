import json, math
d = json.load(open("SOLVER_LAB/reports/exp_n2_results.json", encoding="utf-8"))
# per-solver step rate from wall & (trail+hops), v5 only, pooled over w=24/28 solves
rows = [r for r in d["trials"] if r["solver"]=="v5" and r["ok"] and r["width_bits"] in (24,28)]
steps = [r["tame_trail"]+r["hops"] for r in rows]
wall  = [r["wall_s"] for r in rows]
print("v5 pooled w=24/28:", len(rows), "solves, mean steps/s =", round(sum(steps)/sum(wall),1))
m = {24: [], 28: []}
for r in rows: m[r["width_bits"]].append((r["tame_trail"]+r["hops"])/r["wall_s"])
for wb in (24,28):
    v = m[wb]; print(f"  w={wb}: mean {round(sum(v)/len(v),1)} steps/s, median {round(sorted(v)[len(v)//2],1)}")
