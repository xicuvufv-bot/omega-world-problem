# Solver Campaign — Experiment Log (EXP-N1 .. EXP-N4)

Date: 2026-09-15. Machine: Windows, Python 3.11.9, 4 logical CPUs, 14 GB RAM.

Every solver candidate below is verified on EACH solve by BOTH channels:
`point_equal_jac(scalar_mult(k), target)` and the independent native C
`secp256k1.dll` (`privkey_to_pubkey`). Zero tolerance for LookupError in
any reported block; all runs use synthetic generated keys on test intervals
(no live puzzle addresses touched).

Measured machine constants (this box):
  * v5 fused+negation kangaroo: ~2,600 steps/s single core
    (w=24 mean 2,982 / median 2,934; w=28 mean 2,479 / median 2,498).
  * native engine brute scan: 150,495 keys/s single, 239,289 keys/s 4-thread
    (~1.6x ceiling).
  * parallel ceiling of the host ~1.6x (scan benchmark).

=====================================================================
## EXP-N1  — v5 baseline reproduction (v4 vs v5)
=====================================================================
Solver: v4 = raw-scalar kangaroo (JUMP_FRACS, W-sized jumps). v5 = fused
single-inversion + even-y negation store (Weff = W/2). K :=
(tame_trail + hops)/sqrt(W), 12 seeds per block, keys generated with
`random.Random(seed*1000 + width)`.

Gate (w in {16,20,24} x 12 seeds):       v4 36/36, v5 36/36, all correct.
Result: v5 reproduces the recorded advantage over v4.
  w=20  v4 meanK=5.99 (5.20..6.78)   v5 meanK=4.20 (3.57..4.79)   ratio 0.70
  w=24  v4 meanK=5.94 (5.12..6.86)   v5 meanK=4.97 (3.67..9.65)   ratio 0.84
  w=28  v4 meanK=5.99 (5.11..7.81)   v5 meanK=4.43 (3.56..6.20)   ratio 0.74

=====================================================================
## EXP-N2 — v6: GLV order-3 endomorphism x negation (6-class quotient)
=====================================================================
Hypothesis tested (from 11_VERDICT next-step #2): walk the full
automorphism quotient {P, psi P, psi^2 P, -P, -psi P, -psi^2 P}, class
size 6, store W/6, aiming at K-floor sqrt(pi/12) ~ 0.51. GLV constants
re-verified computationally: psi(kG) == (LAMBDA*k mod n) G including 20
random spot checks (BETA order-3 root mod p, LAMBDA order-3 root mod n).

Finding (measured): **the automorphism quotient does not reduce the meeting
space for a bounded-interval additive kangaroo.** The 6/36 candidate sets
never fire a folded member:
  * instrumented v5 recovery: negation candidate `k2 = n - (t_off + wild_d)`
    fired 0/16 solves; all recoveries used raw-scalar equality `k1`.
  * reasoning confirmed by measurement: a canonical x-collision between raw
    scalars a, b needs `b == +-LAMBDA^i * a (mod n)`. For LAMBDA^i != 1 the
    class member has scalar ~ lambda*a mod n, astronomically outside the
    small interval both herds occupy, so only a == b matches. The quotient
    store reduces to identity; the shorter W/6 trail then *worsens* density.

Two failed quotient-walk drafts (both logic reasons recorded in-code):
  draft-1 raw-follow + min-x bucket  -- measured catastrophic tails
    (w=14 s2: 19,253 hops / 70 empty passes; w=12/16 timeouts).
  draft-2 canonical-state walk        -- bucket on min-x canonical x
    collapses the step map: w=16 -> 13 distinct canonical states in 372
    steps (disjoint tame/wild components, 0 trail hits in 3 passes x w=24).
  draft-3 (final v6) raw walk (v4/v5 mixing) + 6-class canonical store +
  exact integer distances + 6/x36 candidate grid:
    CORRECTNESS GATE 36/36 (v6), then:
    w=20 v6 meanK=3.84 vs v5 4.20  (min 2.08, max 8.49)
    w=24 v6 meanK=16.10 vs v5 4.97 (min 2.17, max 69.62) -- heavy tail
    w=28 v6 meanK=4.11 vs v5 4.43  (min 2.06, max 8.80)
  v6 cannot beat v5: at equal-mixing jumps the 6-class store adds nothing
  (folded candidates never fire) and shorter trail risks tails.

Mechanistic attribution of v5's real gain (measured): NOT the negation
folding. Re-running v4 with v5's jump sizing (V4Tuned:
v4 raw store + jump_weff W/2, trail geometry W-based):
  w=20: v4=5.99  V4Tuned=5.39  v5=4.20 ;  w=24: v4=5.94  V4Tuned=5.91  v5=4.97
=> jump/trail density (trail points per sqrt(W) of raw-scalar space:
  v4 ~1.25, v5 ~1.77) plus trail geometry account for the constant;
  the even-y canonicalization is inert on bounded walks.

CONCLUSION: 11_VERDICT step-2 (automorphism/GLV 1.7-2x toward K=0.51) is
REFUTED by measurement for bounded-interval additive kangaroo. v5 remains
the best proven constant (~K 4.2-5.0).

=====================================================================
## EXP-N3 — multi-herd (van Oorschot-Wiener style) wall scaling
=====================================================================
One v5 tame trail shared by W independent wild passes (per-worker streams,
first-herd win, native FFI re-verification). w=28, 12 seeds, 1/2/4 workers.
Harness: SOLVER_LAB/benchmarks/bench_multiherd.py.
  workers=1: mean wall 13.95s (med 14.20)
  workers=2: mean wall 12.05s (med 12.49)
  workers=4: mean wall 12.08s (med 12.03)
No wall scaling: the serial trail build dominates at w=28 (trail ~23.7k
steps over a hop phase that averages ~8k), and the host parallel ceiling is
only ~1.6x (measured independently on scan_threaded). Multi-herd buys
nothing per-core; several-core boxes would need the distinguished-point /
shared-store engine to matter.

=====================================================================
## EXP-N4 — infeasibility bounds for live targets on THIS box
=====================================================================
Constants: v5 K ~= 4.5 (mean over w=20-28), 2,600 steps/s/core, trail
~= 3.54 * 2^((w-1)/2) stored points, scan 239,289 keys/s (4-thread).

Intervals: #67 -> w=67 (W=2^66, R1). #140 -> w=140 (W=2^139, R2).

#67  kangaroo steps ~= 4.5*2^33 ~= 3.9e10  -> ~173 CPU-days/core
     trail memory  ~= 3.54*2^32.5 ~= 1.7e10 entries -> hundreds of GB-1TB RAM
     brute scan    ~= 2^66 / 239,289 ~= 3.1e14 s ~= 10M years
#140 kangaroo steps ~= 4.5*2^69.5 ~= 3.3e21 -> ~4.1e10 core-years
     trail entries ~= 2.2e21 -> impossible
     brute scan    impossible

VERDICT: both targets remain compute- AND memory-blocked on this hardware.
A single kangaroo on #67 is ~half a core-year with ~1 TB-class trail RAM;
#140 is out of reach by ~12+ orders of magnitude even with perfect
parallelism. No algorithm-structure breakthrough for bounded-interval
additive kangaroo was found beyond v5 (density-tuned); automorphism
quotient routes are measured dead.

=====================================================================
Appendix: files
  SOLVER_LAB/candidate/v5_fused_negation.py      best proven (baseline)
  SOLVER_LAB/candidate/v6_glv_negation.py        draft-3, kept for audit
  SOLVER_LAB/benchmarks/bench_v6.py              EXP-N1/N2 harness
  SOLVER_LAB/benchmarks/bench_multiherd.py       EXP-N3 harness
  SOLVER_LAB/reports/exp_n2_results.json         every EXP-N2 trial
  SOLVER_LAB/reports/exp_n3_results.json         every EXP-N3 trial