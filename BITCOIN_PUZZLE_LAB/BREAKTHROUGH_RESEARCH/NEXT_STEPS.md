# Next Steps

## Immediate (Ready to Execute)

### 1. Solve Puzzle #66 (CPU, ~1 hour)
Run the fused kangaroo on the real public key of puzzle #66 (33 bits).
This is the first unsolved puzzle in sequence and is within reach of
the CPU implementation at 2.0x fused speedup. Estimated time: 30–60
minutes. Would be the first real puzzle solved by this lab.

### 2. Apply Fused Inversion to v4_kangaroo.py
Integrate the fused `_step` design into the production solver.
This is a drop-in improvement: same API, same correctness, 2x faster.

## Medium-Term (Weeks)

### 3. GPU Kangaroo
Port the fused kangaroo to CUDA. A modern GPU (RTX 4090) can run
thousands of kangaroo walks in parallel. With the fused inversion,
effective throughput scales to w=40–48 within months of wall time.

### 4. SIMD Point Addition
Vectorize the field arithmetic (P-256 modular add/mul) using AVX2/AVX-512.
Combined with the fused inversion, this could yield a further 2–4x on CPU.

## Long-Term (Months+)

### 5. Puzzle #68+ (35–40 bits)
With GPU acceleration, puzzles #68–#76 (35–76 bits) become targetable.
Each doubling of bits = 4x more compute. The fused inversion and GPU
parallelism together push the CPU+GPU ceiling to ~40 bits.

### 6. Asymptotic Research
The Θ(√W) floor (EX5) is confirmed. Breaking it requires either:
- A mathematical breakthrough on secp256k1 ECDLP (unlikely, decades
  of research have not found one).
- A new approach exploiting the specific interval structure (not generic
  ECDLP). This remains an open research question.

## What NOT to Do
- Do not waste compute searching for PRNG patterns in the keys (EX2 negative).
- Do not modify bucket selection based on low-bit degeneracy (EX1 disproven).
- Do not apply GLV to walk steps (EX5: no benefit for point additions).
