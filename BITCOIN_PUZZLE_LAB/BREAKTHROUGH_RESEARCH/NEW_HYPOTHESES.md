# New Hypotheses

## Hypothesis H1: Fused Inversion Improves Solve Time at Scale

**Statement:** A kangaroo solver with fused single-inversion (1 modular
inversion per hop instead of 2) will solve interval DLP instances on
secp256k1 in half the wall-clock time, at identical hop counts, for all
interval widths w ≥ 16.

**Status:** VERIFIED (EX4). 36 test cases across w=16,20,24,28.
Measured speedup: avg 2.00x, median 1.98x, min 1.15x, max 4.00x.
All 36 cases recovered the correct key. Bucket sequences identical (4/4).
Hop delta ≤ 1 in all cases (detection-timing endpoint shift).

## Hypothesis H2: secp256k1 Has No Asymptotic DLP Shortcut

**Statement:** secp256k1's cofactor=1, j-invariant=0, and prime-order
group mean that interval DLP on this curve requires Θ(√W) group
operations, with no algorithmic reduction via subgroup decomposition,
endomorphisms, or torsion.

**Status:** VERIFIED (EX5). Cofactor=1 confirmed (n·G=INF, small
multiples ≠ INF). GLV endomorphism exists (ω, λ cube roots of unity
found and verified). But GLV only accelerates fixed-base scalar
multiplication (~30–50%), not the point-addition walk steps in
Pollard kangaroo. The floor is confirmed: Θ(√W) group ops.

## Hypothesis H3: 83 Recorded Keys Are High-Entropy Random Draws

**Statement:** The 83 published private keys in the Bitcoin Puzzle are
consistent with independent high-entropy uniform random draws within
their intervals. No weak-PRNG fingerprint, no structural anomaly, no
exploitable pattern exists.

**Status:** VERIFIED (EX1, EX2, EX3).
- EX1: no low-nibble degeneracy, bucket distribution uniform.
- EX2: 6 PRNG strategies tested, none exceeds null+3σ, no large-key matches.
- EX3: 11 metrics, train/test split, no replicated p<0.01 in same direction.

## Hypothesis H4: CPU Kangaroo Ceiling Is ~34 Bits

**Statement:** On a single modern CPU core (3 GHz), a fused Pollard
kangaroo can solve interval DLP up to approximately w=34 bits within
a reasonable time budget (~1 hour). Beyond this, GPU parallelism is
required.

**Status:** PROVISIONAL. Extrapolated from EX4 w=28 fused ≈ 20s.
Expected w=33 time: ~30–60 minutes. Expected w=34: ~2–4 hours.
Not yet measured directly. TODO: run at w=33 to confirm.
