# -*- coding: utf-8 -*-
"""runner_one.py <solver> <jsonrowfile> — run ONE solver in its own process with
a wall-clock cap (defensive countdown in-process), print result line. Used by
smoke_real2.py to isolate which solver hangs."""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RESEARCH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [RESEARCH]

import solvers

def main():
    name = sys.argv[1]
    row = json.load(io.open(sys.argv[2], encoding="utf-8"))["row"]
    N = int(row["l"])
    db = int(row["db"])
    t0 = time.time()
    try:
        fn = getattr(solvers, name)
        if name == "bsgs":
            out = fn(row, N, seed=3)
        else:
            out = fn(row, N, seed=3)
        dt = time.time() - t0
        k = out.get("k") if isinstance(out, dict) else out
        print("RES %s db=%d k=%r dt=%.3f" % (name, db, k, dt))
    except Exception as e:
        print("ERR %s db=%d %s: %s dt=%.3f" % (name, db, type(e).__name__, e, time.time() - t0))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
