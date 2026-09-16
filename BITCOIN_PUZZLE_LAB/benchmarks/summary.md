# Experiment digest (registry: experiments/run_all.py)

_run: 2026-09-15 12:23:59 local_

## A. Throughput (single CPU core, Py 3 stdlib)

| selector | keys/s |
|---|---|
| v1 naive (scalar-mult per key) | 13646 |
| v2 stride (point-add + full hash) | 43234 |
| v2 masked (point-add + bucket + hash) | 44763 |
| v2 pure stride loop (no hash) | 125471 |

> single-target mask cannot skip (every bucket == target bucket); masked path is ~ the stride cost + hash compare.

## B. Interval-DLP scaling (synthetic keys)

| bits | BSGS ok | BSGS s | BSGS m | kang ok | kang s | kang hops | theory | ratio |
|---|---|---|---|---|---|---|---|---|
| 16 | True | 0.062 | 182 | True | 0.391 | 212 | 226.9 | 0.93 |
| 20 | True | 0.297 | 725 | True | 1.812 | 1762 | 907.5 | 1.94 |
| 24 | True | 0.844 | 2897 | True | 5.516 | 1895 | 3630.0 | 0.52 |
| 28 | True | 3.312 | 11586 | True | 31.328 | 28845 | 14519.9 | 1.99 |

Theoretic jumps for kangaroo 2*sqrt(W) = sqrt(2W) total, so hops ~ 1.25*sqrt(W) per herd; ratio column stays ~ constant if the implementation matches theory.

## C. Solved-key statistics (see patterns/known_keys_analysis.md)

- keys=83, bits 1..135
- relative-position mean 0.514 (uniform => 0.5)
- hamming-weight fraction 0.516 (expected 0.500)
- findings: uniform top nibble ~= expected under random keys in [2^(n-1), 2^n); uniform last nibble: no mod-16 residue is favoured by the generator; relative position uniform: solved keys are not biased toward any part of the interval (no positional shortcut); hamming weight ~ n/2 as expected for uniform independent bits

## D. Full-ladder agreement (20-bit toy)

| solver | result |
|---|---|
| target k | 586742 |
| v1 naive limit 10k keys | 3.563s (scanned only) |
| v2 stride | not reached within 10k cap |
| v3 BSGS | 586742 (m=725) |
| v4 kangaroo | 586742 (146 hops) |
| agree | True |

## Log

- v1 naive measured 13646 keys/s (100k scan)
- v2 stride measured 43234 keys/s
- v2 masked measured 44763 keys/s
- v2 pure stride loop 125471 adds/s
- w=16: BSGS 0.06s (m=182, 182 pts); kangaroo 0.39s (hops=212, ok=True, ratio 0.93)
- w=20: BSGS 0.30s (m=725, 725 pts); kangaroo 1.81s (hops=1762, ok=True, ratio 1.94)
- w=24: BSGS 0.84s (m=2897, 2897 pts); kangaroo 5.52s (hops=1895, ok=True, ratio 0.52)
- w=28: BSGS 3.31s (m=11586, 11586 pts); kangaroo 31.33s (hops=28845, ok=True, ratio 1.99)
- pattern analysis -> patterns/known_keys_analysis.md
- ladder demo on k=586742: v3==v4==expected True; v1 10k keys 3.563s, v4 hops 146
