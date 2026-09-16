# SEARCH_PLAN.md — Attack plan for #67 (R1) and #140 (R2)

This is the executable plan for the two ranked tracks. Both require hardware
this machine does not have; numbers are computed from OUR measured rates
(lab benchmarks) and external published GPU rates (clearly labeled).

## Track A — Puzzle #67 (R1, 67-bit, primary)
- Interval: [2^66, 2^67 - 1]; expected keys to test: **~2^66 ≈ 7.4e19**.
- Address: `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ`.
- Attack: hash160 bloom-scan (BitCrack / KeyHunt "secp address" mode).
  No kangaroo; no pubkey to anchor a tame trail.
- Measured OUR rate (pure CPU, EC-mult + hash160): 125,471 keys/s (repo
  benchmarks). That is 2^66/125471 s ≈ **1.9e7 years** on this machine —
  proof single-CPU is hopeless, used only as the honest benchmark basis.
- Published GPU rate: **~2-6 Gkey/s per RTX 4090** (Hashcat/BitCrack-class
  published figures). At 5 Gkey/s effective, one 4090 = ~470 yr; a 400-GPU
  cluster = **~2.3 yr** expected; a 2000-GPU distributed effort (community
  style, as for #66) = **~6 months**.
- Parallelism: fully embarrassingly parallel across key ranges; safe.
- Checkpointing: split into 2^22 range chunks of 2^44 keys; each chunk seeds
  a RNG-free linear counter; results written incrementally; resume = skip
  completed chunks (no work ever lost).
- Requires: (a) hash160 bloom filter built from the address (public data),
  (b) GPU scalar-mult engine, (c) chunk scheduler. ~4-6 person-weeks to build
  if a CUDA dev joins; otherwise run published BitCrack/KeyHunt directly.

## Track B — Puzzle #140 (R2, 140-bit, v5 kangaroo)
- Interval: [2^139, 2^140 - 1]; expected ops ≈ 2^71 post-negation.
- Pubkey: `031f6a33...`, address `1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo`.
- Our v5 (fused + negation) is the only solver with a verified advantage here:
  measured 2.54x avg / 2.69x median over v4, correct 49/49 (w=20-34).
- Measured OUR CPU hop rate: v4 ~7k hops/s (bench); v5 ~14k hops/s (fused).
  Single-CPU expected wall: ≈ 2^71/1.4e4 s ≈ **4e6 years** — single CPU hopeless.
- Published GPU rate (RCKangaroo-class): ~3-8 Gkey/s per RTX 4090. With our
  negation already standard there, #140 ≈ **1,400 GPU-yr single** / **~3.5-4 yr
  on 400 GPUs**.
- Parallelism: distinguished-point (van Oorschot-Wiener) kangaroo is
  embarrassingly parallel; wild kangaroos independent, shared DP table.
- Checkpointing: DP table saved every 30 min + start/endpoints recorded;
  resume rebuilds tame trail from offsets (cheap) and re-serves wild range.
- Requires: v5 GPU port (negation + fused already verified in Python; port is
  mechanical), DP table store, cluster. ~3-6 person-weeks GPU port.

## Sequence if a cluster becomes available
1. Stand up BitCrack/KeyHunt on GPU; run #67 chunks (Track A) — cheapest
   absolute search in the unsolved corpus.
2. In parallel, port v5 to CUDA; enter the race whenever a pubkey target
   (#140) is the focus — our negation + fused are confirmed wins there.
3. Golden-rule "benchmark before committing": 10-min GPU benchmarks for the
   actual config, then extrapolate with the measured keys/s — never a claimed
   estimate from thin air.

## What we are NOT doing here
- Not launching any scan on this machine (2^33x short of even #140's cluster
  scale; single CPU proven < any estimate).
- Not touching live funded addresses from this environment at all.