# 07 — Kangaroo notes (v4 engineering journey)

The most instructive solver in the lab. The final design is
`solvers/v4_kangaroo.py`; this file records **why** it looks the way it does.

## Trap 1 — the bucket function degenerate on secp256k1

First v4 bucketed walks via `x & 0xF` (low nibble). On 20-bit intervals the
x-coordinates of points in the walk are **not** uniformly distributed in the
low nibble: they collapse to ~2 residues (x ≡ 9 | 13 mod 16 was observed).
With ~2 buckets the "pseudorandom" walk is mostly deterministic → it misses
its meeting point → timeouts at 20-bit where theory says 1.3k hops.

**Fix:** bucket on `(x >> 120) & 0xF` (bits ~120-123 of the 256-bit x). These
top-ish bits are essentially uniform for either herd. After the fix a 20-bit
interval converged in ~1.3k hops (theory ≈ 1.28k).

**Lesson:** jump partitioning must be engineered against the *actual group's
x-distribution*, not assumed. On secp256k1 the low bits of x are structurally
bad; the reference literature ("use top bits") turns out to matter.

## Trap 2 — the meet-time heavy tail of twin herds

Serial twin-kangaroo (tame + wild, one pair) has a *massive* per-key meeting
variance. For a 24-bit target we measured meeting distances >12× the mean —
a real unlucky launch-bootstrap pair can run a whole Tesla lifetime for
nothing. Any "budget = 2× theory" abort cut off exactly those runs.

**Fix — "one tame trail, many wild passes":**
- tame walk is built **once** from offset 0 (records absolute offsets in
  `tame_off[]`; every landing survives);
- each wild pass restarts with a **fresh random bootstrap jump `d0`**
  (`Q + d0·G`), and the pass runs a full theory-scale hop count;
- budget is checked *between passes*; a pass that misses just restarts with a
  new `d0`.

Effect (measured): every width 16/20/24/28 solves on the **first** pass; the
historical 24-bit "bad key" (with the old twin) and a 28-bit seed sweep all
solved across seeds; ratio (hops/theory) across widths was 0.5–2.0.

## Trap 3 — formula bookkeeping (2× `lo`)

Recovery math: tame lands at `x = lo + t_abs · G`-frame; wild at
`x = Q + d2` etc. The naive code did `k = lo + t_off − wild_d`, effectively
adding `lo` twice (once via `tame_off` already being absolute in [0,W), once
explicitly). Correct:

```
k = tame_offset − wild_distance        # both absolute, relative to interval lo
```

In the fixed solver `tame_off` stores absolute offsets so `t_off − wild_d`
with no extra `lo` was the fix. This single sign/offset error previously
produced "universal ✗" that looked like a timeout, not a math bug.

## Trap 4 — `d0 == 0` is the point at infinity

The bootstrap `Q + d0·G` when `d0 = 0` returns the generator’s … no: `Q + 0G`
is `Q`; but the *wild offset* `d0` is used in recovery, and a zero jump is
non-random. The solver guards `d0 == 0` by resampling before squaring the walk
(no specialized infinity handling needed in affine/`_step` since it
regenerates). Edge cases still get exact `y`-parity confirmations on
collisions.

## Trap 5 — reproducibility: Windows `__pycache__` staleness

Edits and runs inside the same clock second reuse a stale `.pyc` (mtime 1 s
granularity) → "phantom" universal timeouts after a fix. Discipline became:
**after any edit, delete `__pycache__` before re-running.** Documented here so
future debugging isn't confused by ghosts.

## Where this left us

- Correctness in `tests/test_v4.py` (in-interval toy keys, 4 widths).
- Ladder agreement (v3 == v4 == brute) on 20-bit.
- Robustness sweep on historical bad geometries.
- Honest remaining gap: at real R2 sizes the parallelism model
  (partitioned trails + server-side collision merge) is production work,
  out of scope here — method is validated, not the cluster.