import json
d = json.load(open("SOLVER_LAB/reports/exp_n2_results.json", encoding="utf-8"))
for r in d["trials"]:
    if r["solver"]=="v6" and r["width_bits"] in (24,28):
        print(f"w={r['width_bits']} seed={r['seed']:>2} ok={r['ok']} K={ (r['tame_trail']+r['hops'])/((1<<(r['width_bits']-1))**0.5):8.2f} hops={r['hops']:>8} passes={r['passes']:>6} wall={r['wall_s']:7.2f}")
