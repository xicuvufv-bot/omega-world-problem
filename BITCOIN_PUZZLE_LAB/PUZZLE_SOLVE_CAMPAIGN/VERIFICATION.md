# VERIFICATION.md — The exact chain any candidate must pass

Written once, used for every candidate, never modified for a target.

## For an R2 candidate (e.g. #140) — kangaroo result
1. **Interval check:** 2^(N-1) ≤ k ≤ 2^N - 1.
2. **Scalar recomputation (independent):** compute pub = kG from scratch with
   a second implementation or a fresh run of `algorithms/curve.scalar_mult`.
3. **Pubkey match:** derived x/y (compressed form) == the puzzle's published
   public point byte-for-byte.
4. **Address derivation (original puzzle method):**
   pubkey -> SHA256 -> RIPEMD160 -> prefix 0x00 + hash -> double-SHA256
   checksum -> base58check == the puzzle's published address string.
5. **Ledger append:** record k (hex), both implementations' outputs, timestamps,
   and the verifier script invocation.

## For an R1 candidate (e.g. #67) — hash scan result
1. Same interval check.
2. kG -> pubkey -> hash160 -> base58check. Compare with the target address.
3. Full equality required; no partial-match scoring is accepted.
4. Recompute kG independently; append evidence.

## Reproducibility of inputs
- Data: interval bounds, published pubkey/address = `dataset/raw_tracker.txt`
  (public record, row N).
- Solver: pinned commit/tag + seed of the KangarooSolver (R2).
- Work chunk: RNG-free linear counter + chunk id (R1), so any candidate can be
  reproduced from its chunk offset alone.

## Explicit exclusions (from the campaign rules)
- "Looks plausible" — rejected.
- "Pubkey resembles target" — rejected.
- "Hash partially matches" — rejected.
- "Solver reports a candidate" without steps 1-5 — rejected.
- No verification method in this file is ever altered to accommodate a
  near-miss.