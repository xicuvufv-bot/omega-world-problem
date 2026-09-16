# 04 — New Hypotheses

## Hypothesis H5: Interval Decomposition via Parity Splitting

**Statement:** For an interval [2^(n-1), 2^n - 1], the odd and even halves contain approximately equal numbers of valid keys. Splitting the interval by parity and running independent kangaroo walks on each half could reduce the effective W by 2× (one bit of information gained for free).

**Why it might work:** The parity of a private key determines the parity of the x-coordinate of k·G (on secp256k1 with a=0, doubling preserves y, so even k maps to a specific parity class). If the target public key's x-coordinate parity is known, we can eliminate half the interval immediately.

**Test:** For each of the 83 solved keys, compute parity of k and parity of x-coordinate of k·G. Check if the mapping is deterministic. If so, for an R2 puzzle, check if the target's x-coordinate parity eliminates one half.

**Status:** UNTESTED. Potential for 2× reduction in W if parity is deterministic.

## Hypothesis H6: Bit-Position Correlation in Scalar Multiplication

**Statement:** The high bits of k strongly determine the high bits of k·G. For secp256k1, the mapping from k to x(k·G) is "almost" order-preserving in the high bits (due to the group structure). This could allow a binary search: determine the highest bit of k from the highest bit of x(k·G), then refine.

**Why it might fail:** ECDLP is designed to prevent exactly this — the "avalanche effect" of scalar multiplication means one bit change in k changes ~50% of bits in k·G. But on secp256k1 specifically, the structure of a=0 might create partial correlations at the very top of the range.

**Test:** For the 83 solved keys, compute the correlation between high bits of k and high bits of x(k·G). Check if r > 0.1 for the top 4 bits.

**Status:** UNTESTED. Low probability but cheap to check.

## Hypothesis H7: Cold Boot Reconstruction from Partial Information

**Statement:** If an attacker knows the high bits of k (e.g., from a side-channel or partial leak), the remaining unknown bits can be solved with a kangaroo walk in the reduced interval. For puzzle #140, if the top 20 bits are known, the remaining 120 bits are still infeasible. But for puzzle #66 (33 bits), knowing the top 10 bits reduces the interval to 2^23, which is trivially solvable.

**Why it's useful:** This defines the "information budget" for each puzzle — how many bits of side-channel information would make the puzzle tractable.

**Test:** For each unsolved puzzle, compute: given N_known high bits, how many GPU-yr to solve the remaining (bits - N_known) bits?

**Status:** THEORETICAL. Useful for threat modeling, not a direct attack.

## Hypothesis H8: Multi-Target Kangaroo

**Statement:** If multiple public keys share the same interval (e.g., #140, #145, #150, #155, #160 are all in [2^(N-1), 2^N - 1] for different N), a single kangaroo walk could potentially solve multiple targets simultaneously by recording the tame trail and checking against all targets.

**Why it might work:** The tame trail is the expensive part (O(√W) storage). If the trail is shared across 5 targets, the amortized cost per target is 1/5. But the wild walks are independent per target (different Q), so the savings come only from the tame build.

**Test:** For the 5 R2 puzzles, compute: shared tame trail size vs independent tame trails. Is the savings > 10%?

**Status:** UNTESTED. Probably marginal since wild walks dominate at large W.
