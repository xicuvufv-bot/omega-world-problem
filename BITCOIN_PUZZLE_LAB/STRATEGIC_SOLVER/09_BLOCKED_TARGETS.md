# 09 — Blocked Targets

## Why Each Target Is Currently Infeasible

### Puzzle #140 (R2, 140-bit) — PRIMARY TARGET
- **Status:** Active target, not blocked by knowledge but by compute.
- **Work:** ~1,400 GPU-years (v5 fused+negation) on single RTX 4090
  (~3,505 fused-only; ~7,000 v4 baseline).
- **With 400 GPUs:** ~3.5-4 years wall-time.
- **Blocker:** Need a 400× RTX 4090 cluster for ~4 years. RetiredCoder has this hardware class.
- **Path forward:** GPU implementation of v5 (fused + negation); merge into RCKangaroo; partnership.

### Puzzle #71 (R1, 71-bit) — CHEAPEST R1
- **Status:** Infeasible on single GPU.
- **Work:** ~15,000 GPU-years (brute-force hash scan).
- **Blocker:** No public key; must scan all 2^70 hashes.
- **Path forward:** GPU hash cracking (BitCrack/Hashcat class). Not our focus.

### Puzzle #145 (R2, 145-bit)
- **Status:** 8× harder than #140.
- **Work:** ~11,200 GPU-years (v5).
- **Blocker:** Same as #140 but 8× more compute.
- **Path forward:** Wait for #140 solve; apply same method.

### Puzzle #135 (R2, 135-bit) — ALREADY SOLVED
- **Status:** Solved 2026-07-28 by RetiredCoder (RCKangaroo, ~400× RTX4090, ~2 months).
- **Key:** `0x6d9392...`
- **Prize:** 13.5 BTC.
- **Relevance:** Proves the 400-GPU cluster can solve 135-bit in ~2 months. #140 is 5 bits harder = ~4× more work = ~8-10 months.

### Puzzle #160 (R2, 160-bit) — THE LAST LINE
- **Status:** Infeasible with any foreseeable technology.
- **Work:** ~1,436,000 GPU-years (v5).
- **Blocker:** Even with 10,000 GPUs, ~144 years wall-time.
- **Path forward:** Would require a fundamentally new algorithm (asymptotic breakthrough). EX5 confirms no such breakthrough exists for secp256k1.

## Summary

| Puzzle | Regime | GPU-yr (v5) | Blocked By | Can We Help? |
|---|---|---|---|---|
| #140 | R2 | 1,400 | Compute (cluster needed) | Yes — GPU implementation |
| #71 | R1 | 15,000 | Compute (no pubkey) | No — wrong algorithm |
| #145 | R2 | 11,200 | Compute (8× #140) | Indirectly — solve #140 first |
| #135 | R2* | — | Already solved | N/A — reference point |
| #160 | R2 | 1,436,000 | Fundamental (Θ(√W) floor) | No — need asymptotic breakthrough |
