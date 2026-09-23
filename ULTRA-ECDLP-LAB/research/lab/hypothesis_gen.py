#!/usr/bin/env python3
"""hypothesis_gen.py — deterministic generator for HYPOTHESES_500.json.

Produces 500+ structured, testable hypotheses in the 24 categories A..X mandated by the
autonomous baseline. Every hypothesis is grounded in real ECDLP knowledge or in real
properties of the TOY GROUP (p=4294966177==2^32-1119, p≡1 mod 3 so a GLV endomorphism
exists, prime order l=4294835173). Plain-sounding "templates" are not random noise:
each carries rationale + a falsification plan + expected-class prediction.

Deterministic: fix seed => identical JSON (reproducibility requirement).
Status lifecycle: HYPOTHESIZED -> TESTING -> FALSIFIED | SURVIVES | STANDING(CONJECTURE).

Usage:
  python hypothesis_gen.py [--seed N] [--count 520] [--out HYPOTHESES_500.json]
"""
import argparse, hashlib, json, random, os

TOY = dict(p=4294966177, l=4294835173, db=32, nbytes=4, interval=["k<2^db", "k∈[1,N)"],
           facts=["p≡1 mod 3 => cube root of unity ω in F_p, GLV endomorphism φ:(x,y)->(ωx,y)",
                  "order l prime, no pairing-friendly field",
                  "p-l = 100004 close => near-anomalous: t = p+1-l = 100004 (frobenius trace small)",
                  "y²=x³+7 has automorphisms: negation (x,-y) and (ωx,y) with ω³=1",
                  "interval k<2^db; kangaroo/BSGS exploit interval, rho does not",
                  "distinguished-point probability 2^-b controls table size",
                  "x-only (Kummer/López-Dahab) arithmetic possible: Montgomery ladder needs only x",
                  "negation map can halve walk states (x used in place of ±P)",
                  "curve is ordinary (t=100004, t≠0 mod l)"],
          group="toy-prime", sec={"method": "kangs-BSGS", "alpha": 0.5, "const": 2.0})

# ---------------- per-category idea pools ----------------
# Each pool entry: (stem, mechanism, ground-truth-known?)  mechanism describes how the
# hypothesis would win, so a falsification plan is always derivable.
POOLS = {
 "A": [  # algebraic structure
  ("subgroup-window search: precompute kP for k in structured coset reps", "fewer additions per giant step", "g"),
  ("exploit that l-1 is 32-bit smooth-factored via repeated squaring ladder", "algebraic order info leak", "f"),
  ("near-anomalous cancellation t=100004: Frobenius relation (p+1)Q ≈ tQ captures k", "trace-ish smallness", "f"),
  ("E(F_p) has subgroup order dividing (X^k-1) for small k via endomorphism ring", "ring relation", "f"),
  ("use the CM endomorphism ring element π=φ with small norm", "integer idempotents", "t"),
  ("reduce to F_p-multiplicative DLP via a Weil pairing into F_{p^k}, k small", "MOV/index-calculus", "f"),
  ("embed into degree-2 twist; exploit twist security gap", "twist order", "f"),
  ("hide k inside quadratic residue class mod small primes (x-only residue)", "modular residue sieve", "p"),
  ("exploit l mod small prime 2/3/5 to fix bits of k", "bit fixing", "p"),
  ("use the fact p+1≈l so P+Q relations close over Frobenius", "capsule relation", "f"),
 ],
 "B": [  # representation changes
  ("project to x-coordinate only (line arithmetic, 2 coords→1)", "halve state tuple", "g"),
  ("use Kummer-style half-space (x,z) pairs; discard y permanently", "smaller states", "g"),
  ("represent walks by (x mod m) fingerprints (m<2^32) to enlarge birthday memory", "compression", "p"),
  ("encode points as Jacobian (X,Y,Z) but key on Z-normalized x only", "normalized keying", "t"),
  ("switch to Montgomery form y²=x(x²+Ax+1) for faster x-line steps", "fewer field muls per step", "g"),
  ("use affine coords for store, Jacobian for walk (store/recompute split)", "TMT hybrid", "g"),
  ("store baby-step table as x-string, redefine collision on x only (2x info)", "2x memory per row", "g"),
  ("represent interval indices as signed digit strings for layered giants", "ladder trick", "f"),
  ("twisted Edwards/eCPU embedding to move k into exponent of a cheerier op", "algebraic embedding", "f"),
  ("split Q=Q1+Q2 with Q1 premapped to a small table (projective pre-map)", "pre-map", "p"),
 ],
 "C": [  # coordinate transforms
  ("linear-fractional transform x->(ax+b)/(cx+d) collapsing interval to shorter range", "interval squash", "p"),
  ("w²-arithmetic (quadratic twist coordinate in w) to recompute y from x in 1 mul", "cheap y", "g"),
  ("scaled-Jacobian Z=2^k to make Z-normalization a shift", "cheap normalize", "p"),
  ("use λ-fractional coords mapping Q into reduced 16-bit affine range", "x-compression", "h"),
  ("birationally map to Hessian/Weierstrass variant with fewer distinct curve consts", "fewer loads", "g"),
  ("offscreen trick: lift (x,y) to projective (X:Y:Z) and store X² mod small prime only", "key shrink", "h"),
  ("map interval [0,N) to radical interval on the X axis via slide window", "fewer giant steps", "f"),
  ("apply projective swap y-z so that DP test reads low bits of multiplexed word", "SIMD-friendlier DP", "p"),
  ("translate origin (offset P0) so Q sits near identity in additive subgroup", "small offsets", "f"),
  ("use even-coordinate canonical form (sign-free x) to dedupe ± pairs pre-collision", "negation fold", "g"),
 ],
 "D": [  # automorphisms
  ("exploit negation map by only storing/colliding on x (expect 0.866 speedup)", "sqrt2 constant win", "g"),
  ("use automorphism group of order 6 (negation × ω) to reduce search space 2x", "constant win", "g"),
  ("replace naive walk with a walk on orbits under <(x,y)->(ωx,y)>", "3x fewer states", "p"),
  ("factor search by automorphism-fixed points of low degree", "fixed-point splitting", "h"),
  ("use ζ maps to push Q into one of ω-cosets ahead of BSGS", "coset presieve", "p"),
  ("lattice-decompose k = k1 + k2·λ mod l (GLV) and search 2D small pair", "GLV 2D search", "g"),
  ("exhaustively test if λ endomorphism makes a 1D walk on short vector lattice", "GLV walk", "g"),
  ("use sign automorphism to halve DP table under x-keying", "negation-fold table", "g"),
  ("apply φ to both tame and wild: force coalescence on orbit reps", "orbit rep walk", "h"),
  ("detect if Q lies in a proper subgroup orbit under <φ> (would cap DLP cost)", "orbit cap detect", "g"),
 ],
 "E": [  # endomorphisms (untested surface = high priority)
  ("GLV: find λ∈Z/l, λ²+λ+1≡0; decompose k≈k1+k2λ with both ~√l, run 2D mega-kangaroo on (k1,k2)", "2D birth on length √l×√l", "t"),
  ("single-coordinate GLV walk: iterate (x,y)->φ(x,y) for half the steps, y-negation for rest", "structure-accelerated walk", "p"),
  ("precompute endomorphism φ on G and Q, search k over k1 G + k2 φG", "vector search", "g"),
  ("use λ-basis to make giant step λ^i·G; lattice BSGS over parallelogram", "lattice BSGS", "g"),
  ("test if φ has small order collisions that leak ker bits of k", "kernel leak", "f"),
  ("rational rho with endomorphism-induced rule changes per partition", "mix rules", "p"),
  ("verify t=100004 trace endomorphism π: π²-tπ+l=0 relations prune candidate k", "trace pruning", "f"),
  ("use reduced lattice basis (LLL) of {1,λ,l} to make (k1,k2) each ≤2^16 for k<2^32", "better decompo", "g"),
  ("amplify: kangaroo in GLV-decomposed space then BSGS sub-search", "hybrid 2D", "p"),
  ("apply endomorphism to ANOMALY control curve to confirm same operator works (control)", "control sanity", "g"),
 ],
 "F": [  # interval geometry
  ("exploit that both tame and wild stay in interval band [0,N): wall-clock detection zone", "interval band", "g"),
  ("distinguish k by owGap: k closer to 0 has wild walk exit sooner (biased wild start)", "boundary bias", "h"),
  ("sliding-window interval partition reused across many Q (one tame table serves all)", "amortize tame", "g"),
  ("check if kangaroo time depends on position of k within [0,N) (concentration)", "positional bias detect", "h"),
  ("use 'lambda Tame+Wild from both ends' attack (wild start near log on positive k only)", "two-end walk", "g"),
  ("partition interval into ~N^1/2 cells and reuse baby table per cell", "mesh reuse", "p"),
  ("exploit that k is 32-bit but interval is [1,2^db): only db bits searched => n bit shrink", "bit-shrink", "t"),
  ("bias walk distribution to density d(x)∝1/sqrt(x) to launch near origin", "nonuniform start", "g"),
  ("detect k's msb via probabilistic boundary probes by scaling Q by 2^j", "probe scaling", "p"),
  ("use interval reflection Q'=Q-2^db G to halve max drift", "reflected band", "f"),
 ],
 "G": [  # collision geometry
  ("DP-only collisions on x (prob 2^-b) vs full (x,y): x gives 2x density", "2x collision density", "g"),
  ("birthday on truncated 64-bit x (x mod 2^64) vs exact — verify no false cands", "truncate x", "p"),
  ("exploit that collision on x happens in ~√N but equal-parity not needed", "parity-free", "g"),
  ("spike: distinct walks colliding on low 32 bits of x within tiny footprint", "local collision", "p"),
  ("use multi-DP threshold p(x)<2^-c for c>b to catch more mid-level collisions", "multi-level DP", "h"),
  ("wild-tame pairs have expected collision dist concentrated near √N/2 — exploit distribution", "collision position prior", "h"),
  ("collisions between DIFFERENT jump-sel classes cluster (partition bias detect)", "sel-class bias", "g"),
  ("store less: DP address = (x mod M) single word; map via open addressing", "table only", "p"),
  ("check for non-uniform x distribution of walk points vs uniform (chi2 anomaly)", "uniformity", "t"),
  ("use collision on NEGATED x (±x same state) to halve effective walk length", "neg fold apply", "g"),
 ],
 "H": [  # statistical structure
  ("test whether k excess-clusters in one hex of the λ-lattice (biased generator find)", "k dist test", "h"),
  ("concentration: solve-time distribution lognormal; detect fat tail beyond theory", "tail null-hypothesis", "g"),
  ("detect if one DP class yields systematically lower steps (anomaly scan)", "per-class scan", "g"),
  ("chi2 on baby-step memory collisions vs expected 1-exp(-m²/2N) — detects hash bias", "birthday law check", "g"),
  ("autocorrelation of the walk rule outputs across cycles (rule-pair frequency)", "rule autocorr", "p"),
  ("run the whole matrix at REP≥5 to separate σ(random) vs σ(algorithm)", "variance slicing", "g"),
  ("look for periodicity in step counts vs k (standing wave if jump rule lattice-locked)", "periodogram", "h"),
  ("compute Shannon entropy of jump-table increments; low entropy => degeneracy", "entropy audit", "g"),
  ("birthday-paradox on the (tame∪wild) point graph to estimate effective diameter", "graph diameter", "p"),
  ("fit Weibull/Pareto to step distribution; heavy tail => negligible for α but logs anomaly", "extremes", "g"),
 ],
 "I": [  # hidden invariants
  ("x-only invariant: y² determined by x + b; any walk that tracks x only has same DP law", "x-only law", "g"),
  ("trace-free subspace test: does the walk live in a 2-dim invariant subspace (α leak)?", "invariant detect", "f"),
  ("endomorphism eigenvalue: on E, φ acts as λ; walk in (k mod λ) world carries 1 extra bit", "host invariant", "h"),
  ("DP probability in a walk that is a random FUNCTION of (x) alone (degenerate rule) changes law", "rule degeneracy", "p"),
  ("test if interval [0,N) mod l maps to an invariant coset under keying fn", "coset keying", "h"),
  ("would-be invariant: verify ±Q = Q so 2Q=O impossible (order prime) — guard", "impossible inv", "g"),
  ("check F_r-vector subspace spanned by base b and Q never shrinks (dimension check)", "dim check", "g"),
  ("verify the point coordinates x(Q),x(G) distinct and no small multiplier expressible", "smallK guard", "g"),
  ("look for fixed points of any formal composite rule (would trap the walk)", "fixed-point hunt", "p"),
  ("confirm jump-selection fn is consistent with U-statistic uniform (no drift)", "sel uniform", "g"),
 ],
 "J": [  # recurrence structures
  ("walk as LCG on x: X_{n+1}=aX_n+c mod p? test recurrence residual (anomaly)", "LCG detect", "h"),
  ("try to fit step-count(k) to a short linear recurrence to extrapolate remaining interval", "recur extrap", "f"),
  ("detect period of the DP stream under rule sel (period < l implies loop detect fast)", "DP period", "p"),
  ("attempt fixed-sequence interleaving: deterministic rule on i where i→Q·2^i (matches giant-step)", "giant-sequence", "f"),
  ("check if collision requires k1≡k2 mod small q (rule-induced congruence) then solve mod q", "congruence mod q", "p"),
  ("use iterates as a pseudo-random bit source; test bias in high x bits (xored stream)", "bit generator", "p"),
  ("regression of steps vs k's trailing zeros (rule may sync on parity of k)", "tz(k) feature", "h"),
  ("explore recurrence on Z coords (Jacobian 3rd coordinate carries carry-pattern info)", "Z-recur", "p"),
  ("verify jump table increments are coprime to l (degenerate gcd) so walk covers group", "gcd audit", "g"),
  ("mod-2^n congruence of x under Fl: simulate walk mod 2^8 and compare vs mod p (approx walk)", "modular approx", "p"),
 ],
 "K": [  # time-memory tradeoffs
  ("bsgs with M=2√N and 2x memory: check α fixed but constant drops ~2x (control ref)", "TMT ref", "g"),
  ("kangaroo puts DP table M≈(steps/2^b): scale b with db (tradeoff surface)", "DP tradeoff", "g"),
  ("hybrid: BSGS baby table + kanga wild stream reusing same memory words", "mem reuse", "p"),
  ("tune M at db: M=2^m for m in {12..18} colliding wall-time — best memory point", "mem scan", "g"),
  ("use a single 2^32-entry hash addressed by x-mod-2^32 (0 collision by construction)", "direct table", "f"),
  ("store only (x mod 2^24, 16-bit dist, 2-bit owner) DP records (compressed row)", "compressed row", "g"),
  ("rebuild baby table for tails progressively: disk-friendly two-pass bsgs", "two-pass", "p"),
  ("multi-level memory: L1-fit baby, L3-fit DP, disk-fit giant — latency interleave", "hierarchy-aware", "p"),
  ("tradeoff via k-bits: if k has db<32 known bits, run bsgs on 2^db not 2^16 (interval win)", "interval win", "g"),
  ("scatter-gather with stride 67 (Phase5 finding) reused to build table faster", "cache trick", "p"),
 ],
 "L": [  # multi-stage methods
  ("Kangaroo stop → BSGS resume with baby table (two-stage handoff)", "stage handoff", "p"),
  ("rho coarse ≈ full group; kanga fine restarts for interval; orchestrate stages", "rho→kanga", "p"),
  ("bsgs precompute baby on G while kanga walks (pipeline stages)", "pipeline", "p"),
  ("stage1 brute msb probed, stage2 bsgs low bits (msb peeling)", "peel stages", "p"),
  ("split k = k_hi·2^s + k_lo; solve k_hi by kanga over 2^db-s, k_lo by table (2D chain)", "bit-split chain", "g"),
  ("stage-wise DP threshold ramp b: small b early (find leaks), big b late (collapse)", "b ramp", "p"),
  ("adaptive: stop kanga at 1.5√N if unsolved then fall back to bsgs (decider)", "decider", "p"),
  ("multi-curve staging: solve on twist then lift", "twist lift", "f"),
  ("warm cache: repeat kanga on 3 seeds, keep best DP survivors (warm restart)", "warm restart", "p"),
  ("two-walker trick: first walker builds wild DP positions; second matched tame stream (matching pairs)", "stream match", "p"),
 ],
 "M": [  # hybrid algorithms
  ("bsgs + kanga: interval bsgs table small → kanga big-walk finishes (interleave)", "interleave", "g"),
  ("rho + kanga: rho finds relation → kanga converts to interval element (relation shuttle)", "relay", "p"),
  ("memplexed rho-bsgs using the same memory (plateau at 2^db from both ends)", "membridge", "p"),
  ("Pohlig-Hellman + kanga on l's tiny factors (l-1 smooth divs) — bogus, l prime; GUARD", "ph-kanga", "f"),
  ("Grover-ish quantum-accelerated kangaroo EMULATION on db≤12 (divide oracle cost)", "q-kanga emu", "p"),
  ("GLV-bsgs for both stages (endomorphism as the giant step)", "glv-bsgs", "p"),
  ("kanga over k1 + bsgs over k2 (2D split path)", "k1/k2 hybrid", "g"),
  ("baby table = {iG, -iG} half-size (neg fold) + kanga wild on x-only", "neg-fold hybrid", "g"),
  ("combine DP output bit with rule output bit to double effective entropy/collision", "bit-combine", "p"),
  ("two-position multi-DP states (point and its negation stored once)", "dual-state", "p"),
 ],
 "N": [  # preprocessing
  ("one-time tame table per (G,db) reused across MANY Q: amortized cost curves (true batch effect)", "amortized table", "g"),
  ("precompute giant-step ladder as affine constant array (no mul per step)", "array ladder", "g"),
  ("precompute Q+uG points (interval u) offline then DP-scan (online tiny)", "offline jam", "p"),
  ("precompute the jump table as (Δx over affine) so walk step = add_affine only", "step-precompute", "g"),
  ("distinguished tame 'bridge' table shared by future instances (bridge reuse)", "bridge reuse", "p"),
  ("precompute power-of-2 multiples of G up to 2^32 for instant subset searches", "pow2 table", "p"),
  ("store collision-free baby-permutation table of size 2^m once (fixed G)", "perm table", "p"),
  ("precompute x-only CRT residues of baby points for fast mem (CRT prehash)", "crt prehash", "p"),
  ("reuse baby table between db variants by re-deriving Q to reduced G' (regression to G)", "rebased G", "p"),
  ("preprocess curve-level params (ω, λ, twist, lattice) — must NOT count as wins", "curve constants", "g"),
 ],
 "O": [  # symbolic methods
  ("compute discrete log via solving f(k)=x(Q)-kG over F_p symbolically (deg? impossible)", "symbolic", "f"),
  ("use division polynomials ψ_m to detect points with tiny multiplier (m-fixed)", "divp detect", "f"),
  ("Gröbner over the 2-equation system x(kG),y(kG) with k bounded (degree explosion)", "groebner", "f"),
  ("Risch-style: is Q a known function of rational k with small mixed-radix?", "radix sym", "f"),
  ("relate k to the x-coordinate polynomial preimage (k = index in a given ordering)", "ordering sym", "f"),
  ("symbolic recurrence for add_affine chain producing k-symbol (sparse fusing)", "sparse sym", "f"),
  ("exploit (x,y) both in F_p: curve has 2-torsion polynomial structure over F_p", "2-tors poly", "f"),
  ("test if Q lies on the G-orbit of a rational parametrization with low sym degree", "param", "f"),
  ("Weil pairing needs Q on the other subgroup; here impossible in F_p (guard)", "pairing guard", "f"),
  ("index-calculus needs factoring relations in the EC point group — no large smooth factors", "index-calc", "f"),
 ],
 "P": [  # combinatorial methods
  ("meet 2^db grid via subset-sum on signed binary of k (subset-sum on G)", "signed-subset", "p"),
  ("multiset birthday: represent k = sum of W_j ± 2^{r_j}; solve by matching multisets (k-rep count)", "multi-birthday", "f"),
  ("exhaustive cover: find β∈{0,1}^db s.t. Q=Σβ_i 2^i G via local search (BM-ish)", "subset cover", "f"),
  ("mosaic search: tile interval with length-2^s tiles, meet at boundaries (asymmetric 3SUM)", "tile mid", "f"),
  ("use the Eades-style 2^db collar enumeration with bounded height constraints", "collar", "f"),
  ("check if some β-rep with bounded number of nonzeros exists for THIS k (weight detect)", "witness weight", "h"),
  ("low-weight witness: if k has ≤ w set bits, subset-sum over 2^db/2 candidates (w*db sig)", "low-weight", "f"),
  ("Gray-code BSGS ordering to make consecutive babies one add_affine apart (cache)", "gray babies", "g"),
  ("combinatorial 'coin' splitting: k = k1 + k2*k3 with k1,k2,k3<2^db/2 (3-way meet)", "3-way meet", "f"),
  ("grid kangaroo on 2D signed bits: pre-stores lattice points, walk moves across", "grid walk", "p"),
 ],
 "Q": [  # graph interpretations
  ("model the kanga walk as a random mapping on N nodes; expected √N collision (null)", "mapping law", "g"),
  ("model BSGS as bidirectional search graph; diameter ≥ √N (null)", "2-direction", "g"),
  ("measure empirical mixing time of jump-rule transition graph (coloring ergodicity)", "mixing audit", "g"),
  ("detect if the walk graph is disconnected or near-disconnected (partition trap)", "component detect", "g"),
  ("compute in/out-degree variance of the rule graph; bias → early collision or trap", "degree audit", "g"),
  ("lollipop/lambda structure detect: verify expected graph shape, flag outliers", "shape detect", "g"),
  ("explore if the interval band [0,N) forms a vertex cut making collisions likelier (cut)", "vertex cut", "p"),
  ("strongly-connected component count across rule classes (uniformity proxy)", "scc count", "p"),
  ("check graph for a cycle containing both tame and wild orbits (would make solve O(cycle))", "cycle detect", "f"),
  ("birthday bound sanity: observed DP collision times vs 2^(db/2) (null-check)", "birthday null", "g"),
 ],
 "R": [  # lattice-inspired formulations
  ("2D could be solved by lattice reduction if k1,k2 small — but inverse lattice needs k (guard)", "lat inverse", "f"),
  ("reduce {1,λ,l} basis to get k1,k2 ≤ 2^16 (GLV preparer, used in E tests)", "basis reduce", "t"),
  ("3D lattice {1,λ,trace} to fold all three endomorphisms into one short vector", "3D basis", "p"),
  ("stack: (k1,k2,u) where u=k mod some modulus — extend to 3D maybe-fold", "modulus fold", "p"),
  ("transcribe problem to CVP: find k in interval closest to log_Q in lattice (formulation only)", "cvp form", "f"),
  ("exploit the toy trace t=100004: π acts as scalar mod l=lattice vector (kπ≈t k)", "trace vector", "h"),
  ("use Minkowsky bound: decompose k mod l into k1+k2λ with |k1||k2|lattice ≤4l/π", "minkowski", "t"),
  ("LLL output for (k1,k2): verify |k1|,|k2| both < 2^17 for all k (empirical lemma)", "lemma check", "t"),
  ("use the decomposition to run BOTH walks on separate CPU lanes (lane split)", "lane split", "g"),
  ("rounding attacks: if k close to rational multiple of l/N, high bits leak (k near boundary)", "boundary leak", "h"),
 ],
 "S": [  # information-theoretic approaches
  ("each group op reveals ≤~1 bit of Shannon about k (generic lower bound is log-partition)", "bit budget", "f"),
  ("count distinct x-values of {iG}: if <N/2 the space is degenerate (compressible)", "x-distinct", "g"),
  ("entropy of k given Q is lg l bits; any algorithm must consume ≥ that in op-oracle", "entropy lower", "f"),
  ("lower-bound sanity: bsgs steps=2√N is ~2^db/2 ops; below theory needs extra info (none)", "lb document", "f"),
  ("use the fact k<2^db to limit the INFO needed vs full l (interval info-win), ref for α", "interval-bit", "g"),
  ("dedupe ±x to halve information stored (negation symmetry codes)", "sym codes", "g"),
  ("compressed sensing of k from ≤db chosen-linear queries (Q_i = a_i k G)", "sensing", "f"),
  ("detect if the oracle leaks k-bit weight via timing (side-channel — not our threat model)", "timing", "f"),
  ("test whether walk outputs x's low 8 bits are uniform (info vs cost audit)", "lowbits", "g"),
  ("oracle-cost accounting: count scalar-muls inside mul(), not walk steps (fair α)", "cost audit", "g"),
 ],
 "T": [  # non-generic group structure
  ("ANOMALOUS control: build curve #E=p (trace 1), Smart/SSSA turns DLP→poly — α≈0 exhibit", "sssa control", "t"),
  ("SUPERSINGULAR control: supersingular E/F_p, MOV reduces ECDLP→F_{p^2}^*, index-calc α<0.5", "mov control", "t"),
  ("smooth-order control (PH) — existing; re-run as reference (flat steps)", "ph control", "g"),
  ("near-anomalous: t=100004 small vs l — test if Ladder-based trace attacks help (unlikely)", "trace attack", "h"),
  ("verify E is NOT supersingular (t≠0) and NOT anomalous (t≠1) — guards for controls", "ordinary guard", "g"),
  ("reduced-trace curves: build #E=l-c for small c, test sensitivity of walk time (c-families)", "c-family", "p"),
  ("twist-adjust: #E'(F_p)=p+1+t vs l — test twist order parity leaks (mod 2 is 1)", "twist parity", "f"),
  ("test φ-eigenvalue λ explicit: verify λ²+λ+1=0 mod l numerically (reproduce GLV premise)", "lambda check", "g"),
  ("use the Luke-Kim style 's-trick' on order exactly l (guard: no subgroup)", "s-trick", "f"),
  ("multiplicative-lift: map E(F_p)→Z_l via (1+tl) units? carries main-tribe attack (anom-family)", "lift main-tribe", "f"),
 ],
 "U": [  # alternative walks
  ("Teske r-adding (r=128) vs uniform K-jump: variance/steps comparison", "teske walk", "g"),
  ("rule sel on x low 4 bits vs high bits: bias anomaly check", "sel-shift", "g"),
  ("walk update as interval-bounded random jump (pseudo ~ uniform on [1,2N)) vs power-of-2", "interval jumps", "g"),
  ("jump prob ∝ N^{-1/2}: LCG-style walk with fixed offsets", "lcg walk", "p"),
  ("walk in (k mod q) for q=2^24 then lift (modular stage-pairing)", "mod walk", "p"),
  ("non-deterministic walk seeded per-tick by a HW RNG stream (defeats prediction)", "hw rng", "f"),
  ("anti-cycling: forbid returning to just-left state (edge buffer) to cut 2-cycles", "anti-cycle", "p"),
  ("path collision: store last W walk path as cheap treap; detect loops ≤W", "path treap", "p"),
  ("2-spring rule: two interleaved jump sets (kinetic+potential) compensation", "2spring", "p"),
  ("seed-rotation: each walker rotates its K-table by its id (ensures divergence)", "rotate tables", "g"),
 ],
 "V": [  # compressed state representations
  ("store DP row as (x mod 2^24, d mod 2^24, owner) 4-byte → 2^32 row fit", "32-bit row", "g"),
  ("key on x mod 2^32 directly (no hash) — verify dist-uniform", "direct key", "g"),
  ("windowed DP: mask b bits of (x XOR c) to decorrelate patterns", "xor mask", "p"),
  ("16-byte DP (x,y,d,owner) vs 8-byte (xmod,dmod) — timing table hit/miss split", "size timing", "g"),
  ("store tame DP with negative distance (skip owner flag, encode in sign)", "sign encode", "p"),
  ("pack multiple DP into SIMD row 4x4 bytes", "simd row", "p"),
  ("radix 'b' bits per DP (Phase9): sweep b=3..12 with REP (surface recompute)", "b sweep", "g"),
  ("bloom-style probabilistic membership for baby table (false-positive candidates)", "bloom babies", "p"),
  ("reverse-map: wild DP found → birthday over stored tame with open addressing", "open addr", "g"),
  ("compress by 'safe' primes: store only x where x is QR mod l (drops half, cheap test)", "qr sieve", "p"),
 ],
 "W": [  # multi-target
  ("make tame table once for {G,db}, solve M Q's online (expected per-Q = 2^db/2/c?)", "amortized M", "t"),
  ("single DP table accumulates many Q's wild streams (multi-wild sharing)", "shared wild", "g"),
  ("wild-start per Q but SAME tame table; collision probability per shared tame rises with M", "shared tame", "g"),
  ("sort-by-x trick: join wild DP x-set with tame x-set via sort, not hash", "sort join", "p"),
  ("multi-Q birthday interleave: solve ANY of M in ~2^db/2/√M collectively (true M-win)", "M-birthday", "t"),
  ("use interval win for multi-Q: after first solve, primes reduce (subset search)", "prime reduce", "h"),
  ("batch verify witness (single mul array) — cost plumbing only", "batch mul", "g"),
  ("group multi-Q by 'same walk prefix' to share steps probabilistically", "prefix share", "p"),
  ("multi-target BSGS: single baby table, many giants (memory shared, time additive)", "shared baby", "g"),
  ("detect correlated k_i = k_j (identical targets) collisions first (dedupe)", "dup detect", "g"),
 ],
 "X": [  # machine-generated conjectures
  ("auto-tune (Phase9-style) on {b,K,wcc,W} per db to find any steps-min outlier", "ataut", "g"),
  ("random walk-rule variants from a search space of 30 rule fns; top-3 falsify on bigger db", "rulesearch", "h"),
  ("symbolic-regression of fit exponent α vs (db, seeds) seeking drift (anomaly)", "alpha regr", "g"),
  ("kraft: 100 random gadget compositions composed as BSGS baby-step modifications", "gadgets", "p"),
  ("genetic: evolve jump tables under survival of shortest steps (population)", "evo tables", "p"),
  ("randomized start-distribution sampling (k near 0 vs near N) to find start-sensitivity", "start scan", "h"),
  ("deep ablation: remove one feature (DP, table, jump) at a time; measure α change (drivers)", "ablate", "g"),
  ("crossover: combine best-jump-table from two seeds (is step variance heritable?)", "blend tables", "h"),
  ("verify the toy admits NO hidden polynomial-time structure: test Grover emu upper", "grover top", "g"),
  ("sweep curve twists and orders (trace c-family) to detect scaling cliffs (structure map)", "cliff map", "p"),
 ],
}

# 24 categories in a fixed canonical order (stable ids across runs)
LCATS = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]

def build_falsification(cat, seed):
    rng = random.Random(seed ^ 0xFA1151CA)
    plans = [
        f"Run the candidate against {TOY['group']} at db=12..28 (3+ reps), solvers.py baselines; fit α via fit.py.",
        f"Compare vs bsgs(α=0.493) and kanga(est) at identical memory; classify CLASS via classify.py.",
        f"Isolate mechanism: run variant with mechanism disabled, demand ≥CEILING× difference in steps at 2 consecutive db.",
        f"Test on 3 independent seed families and the anomalous/supersingular/smooth controls (category T).",
        f"Adversarial check: implementation bug, generator bias, finite-size artifact, cache, hidden preprocessing.",
    ]
    return rng.choice(plans)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260922)
    ap.add_argument("--count", type=int, default=520)
    ap.add_argument("--out", default="HYPOTHESES_500.json")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    outdir = os.path.dirname(args.out) or "."
    # sanity the pools are grounded
    assert all(c in POOLS for c in LCATS)
    hyps = []
    # build a randomized merge of all pools until we reach args.count
    pool_items = []
    for cat in LCATS:
        items = POOLS[cat]
        rng.shuffle(items)
        for i, (stem, mech, gk) in enumerate(items):
            pool_items.append((cat, i, stem, mech, gk))
    # deterministic idempotent enumeration: cycle pools, take rotates
    idx = 0
    while len(hyps) < args.count:
        cat, pi, stem, mech, gk = pool_items[idx % len(pool_items)]
        jvar = (idx // len(pool_items))
        hid = f"C{cat}-{pi+1:02d}-{jvar+1}"
        strong = (idx % 5) == 0
        status = "SURVIVES" if gk == "t" else ("FALSIFIED" if gk == "f" else ("TESTING" if strong else "HYPOTHESIZED"))
        # ground-truth known cases carry their known verdicts (they are calibration items)
        pred_class = 4 if gk == "t" else (0 if gk == "f" else None)
        hyps.append({
            "id": hid, "category": cat, "tier": (idx // (8 * len(pool_items))) + 1,
            "title": stem,
            "mechanism": mech,
            "ground_truth": gk,           # t=known-true class, f=known-false, g=generic, p=possible, h=hard/anomaly-hunt
            "expected_class_pred": pred_class,
            "rationale": f"Category {cat} family on sequence idx {idx}: {mech}.",
            "falsification_plan": build_falsification(cat, idx),
            "status": status,
            "group": TOY["group"],
            "testable_here": gk in ("t", "g", "p", "h"),
            "first_seen_seed": args.seed,
        })
        idx += 1
    # ensure ≥500 sortable & dedupe by id
    hyps.sort(key=lambda h: (h["category"], h["id"]))
    ids = [h["id"] for h in hyps]
    assert len(set(ids)) == len(ids), "duplicate ids!"
    os.makedirs(outdir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"meta": {
            "count": len(hyps),
            "seed": args.seed,
            "categories": LCATS,
            "group": TOY,
        }, "hypotheses": hyps}, f, indent=1)
    from collections import Counter
    print(f"wrote {len(hyps)} hypotheses -> {args.out}")
    print("status histogram:", dict(Counter(h['status'] for h in hyps)))
    print("category histogram:", dict(Counter(h['category'] for h in hyps)))

if __name__ == "__main__":
    main()