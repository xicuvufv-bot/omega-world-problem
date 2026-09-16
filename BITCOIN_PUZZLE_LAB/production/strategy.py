"""Strategy selection + honest feasibility model for the production pipeline.

Two families of engines are orchestrated:

  * BitCrack (cuBitCrack / clBitCrack)  -> R1 brute-force hash160 scan.
    Work per puzzle = O(width) = 2^(n-1) hash160 comps. Rate model:
    ~5e8 .. ~8e8 keys/s per modern desktop GPU (BitCrack field we
    benchmark on the real hardware before trusting it).
  * Pollard Kangaroo (JeanLucPons/Kangaroo, RCKangaroo, colliders)
    -> R2 interval ECDLP on the exposed pubkey. Work ~ O(2 * sqrt(width)).
    Group-op rate model: ~5e9 .. ~8e9 ops/s per 4090-class GPU.

Honest posture: EVERY remaining puzzle (#71..) is 10^3..10^6 single-GPU
years. Feasibility is printed loud. The value of this pipeline is a
coordinated, checkpointed, multi-GPU/multi-host scheduler — not a miracle
shortcut. No statistical shortcut exists (see patterns/known_keys_analysis.md).
"""

import math

FULL_R1_RATE = 6e8        # keys/s conservative single desktop GPU (hash160)
FULL_R2_RATE = 6e9        # group ops/s conservative single 4090-class GPU


def choose(puzzle, measured_kps=None):
    if puzzle.regime == "SOLVED":
        return None
    if puzzle.regime == "R2":
        return {
            "engine": "kangaroo",
            "why": "public key exposed -> interval ECDLP (sqrt(width) work)",
            "steps": int(2.2 * math.sqrt(puzzle.width)) + 1,
        }
    rate = measured_kps or FULL_R1_RATE
    return {
        "engine": "bitcrack",
        "why": "address-only -> full hash160 scan over the interval",
        "width": puzzle.width,
        "steps": puzzle.width,
        "eta_years_single_gpu": puzzle.width / rate / (365 * 24 * 3600),
    }


def estimate(puzzle, gpu_count=1, measured_kps=None):
    c = choose(puzzle, measured_kps)
    if c is None:
        return None
    if c["engine"] == "kangaroo":
        r2_rate = measured_kps or FULL_R2_RATE
        seconds = c["steps"] / (r2_rate * gpu_count)
    else:
        seconds = c["width"] / ((measured_kps or FULL_R1_RATE) * gpu_count)
    return {
        "engine": c["engine"],
        "why": c["why"],
        "seconds": seconds,
        "gpu_years": seconds / (365 * 24 * 3600),
        "gpu_count": gpu_count,
    }


def plan(puzzles, gpu_count=1, measured_kps=None):
    plans = []
    for p in puzzles:
        est = estimate(p, gpu_count=gpu_count, measured_kps=measured_kps)
        if est is None:
            continue
        est["n"] = p.n
        est["address"] = p.address
        est["regime"] = p.regime
        est["keyspace"] = p.keyspace_hex
        plans.append(est)
    return sorted(plans, key=lambda e: e["seconds"])