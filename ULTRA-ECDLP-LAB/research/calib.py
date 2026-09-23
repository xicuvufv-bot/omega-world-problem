import math, time, random
from gen import add, mul, TOY_P, TOY_L, TOY_G
from solvers import bsgs
rng = random.Random(7)
for db in (24, 26, 28):
    N = 1 << db
    k = rng.randrange(1, N)
    Q = mul(k, TOY_G, TOY_P)
    row = {"db": db, "p": TOY_P, "l": TOY_L, "Gx": TOY_G[0], "Gy": TOY_G[1],
           "Qx": Q[0], "Qy": Q[1], "k": k}
    t0 = time.time(); r = bsgs(row, N, 1); dt = time.time() - t0
    us = dt * 1e6 / r["steps"] if r["steps"] else 0
    print("db=%d steps=%d time=%.0fms ok=%s us/step=%.2f" % (db, r["steps"], dt * 1000, r["ok"], us))