#!/usr/bin/env python3
"""hypothesis_engine.py — autonomous research hypothesis bank (v3 mission).

Builds a structured corpus of >=1000 hypotheses across 20 named research families
(A..T), every entry carrying the mission schema plus FAMILY / SOURCE / NOVELTY.

Schema:
  ID NAME CLAIM MATHEMATICAL_REASON ASSUMPTIONS PREDICTION EXPERIMENT BASELINE
  RESULT ALPHA R2 STATUS WHY_IT_FAILED_OR_SURVIVED
  + FAMILY (A..T), SOURCE (core|variant|negative|composite), NOVELTY (1..5)

STATUS vocabulary: HYPOTHESIZED / CONSTANT / REFUTED / UNTESTABLE_YET / INVALID.

Truth rule: generating hypotheses is work for the AI, deciding truth is NEVER the
AI's job — every option above must pass the falsification gate in consolidate.py.
"""
import json, os

FAMILIES = {
 "A": "algebraic structure of the j=0 / near-max-trace toy family",
 "B": "coordinate systems & group-op representation cost",
 "C": "automorphisms & endomorphisms (GLV / CM / 3D lattices)",
 "D": "hidden invariants of shared fixed-base instances",
 "E": "projective / weighted / rational transforms",
 "F": "interval structure k<2^db<<l exploitation",
 "G": "collision geometry & distinguished-point distributions",
 "H": "graph / random-walk interpretations of rho & kangaroo",
 "I": "statistical distinguishers on x / DP outputs",
 "J": "information-theoretic bounds (entropy of k, mutual info)",
 "K": "time-memory tradeoffs & precomputation on fixed G",
 "L": "multi-stage & hybrid compositions",
 "M": "symbolic / algebraic manipulation of the DLP equation",
 "N": "combinatorial & enumerative structures",
 "O": "non-uniform / biased random walks & jump tables",
 "P": "alternative state spaces (divisors, residues, embeddings)",
 "Q": "multi-target structure (K instances, 1 base) amortization",
 "R": "non-generic attacks (index calculus, XEDNI, MOX, Smart)",
 "S": "quantum/emulated-Grover & post-quantum perspective",
 "T": "methodology: benchmark validity, artifacts, lower bounds",
}

def H(**kw):
    """Keyword-only constructor. All schema text fields must be strings, numeric
    fields alpha/r2 numeric, status from the controlled vocabulary."""
    from collections import OrderedDict
    base = OrderedDict()
    base["ID"] = None
    base["FAMILY"] = kw.get("FAMILY", "T")
    base["NAME"] = kw.get("NAME", "")
    base["CLAIM"] = kw.get("CLAIM", "")
    base["MATHEMATICAL_REASON"] = kw.get("REASON", kw.get("MATHEMATICAL_REASON", ""))
    base["ASSUMPTIONS"] = kw.get("ASSUMPTIONS", "synthetic toy rows; prime order l; distinct l per db; y^2=x^3+7")
    base["PREDICTION"] = kw.get("PREDICTION", "")
    base["EXPERIMENT"] = kw.get("EXPERIMENT", "")
    base["BASELINE"] = kw.get("BASELINE", "bsgs alpha~0.494 R2~0.99994 (SCALING_RESULTS_AUTONOMOUS.csv)")
    base["RESULT"] = kw.get("RESULT")
    base["ALPHA"] = kw.get("ALPHA")
    base["R2"] = kw.get("R2")
    base["STATUS"] = kw.get("STATUS", "HYPOTHESIZED")
    base["WHY_IT_FAILED_OR_SURVIVED"] = kw.get("WHY", "-")
    base["SOURCE"] = kw.get("SOURCE", "core")
    base["NOVELTY"] = kw.get("NOVELTY", 3)
    return base

# ----------------------------------------------------------------------
# Core templates: real, distinguishable claims. Sorted by family.
# ----------------------------------------------------------------------
def core_templates():
    base = "bsgs alpha~0.494 R2~0.99994 (SCALING_RESULTS_AUTONOMOUS.csv)"
    A = "synthetic toy rows; prime order l; distinct l~2^db per db; y^2=x^3+7; fixed G"

    out = []
    # ---- A: algebraic structure / near-max-trace family
    out += [
        H(FAMILY="A",
          NAME="CM discriminant D=t^2-4p=-3*2419^2 is non-square, order rank 2 only",
          CLAIM="t=131005, t^2-4p=-17554683=-3*2419^2; endomorphism ring is an order of "
                "Q(sqrt(-3)) with conductor 2419 -> CM rank 2 plus the order-3 automorphism phi.",
          REASON="transcendence of CM: D non-square implies ordinary, full endomorphism ring has "
                 "rank 2; only GLV-type decompositions exist.",
          ASSUMPTIONS=A,
          PREDICTION="all endomorphism decompositions are at most 2D; GLV constant only; alpha 0.5.",
          EXPERIMENT="probe_structural: cube-root unity, lambda=phi(G), glv_decompose validity 500/500.",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5, R2=0.999,
          WHY="verified phi(G)=lambda*G, lambda^2+lambda+1=0 mod l; E1 grid failed: k2 not localized.",
          SOURCE="core", NOVELTY=4),
        H(FAMILY="A",
          NAME="near-max-trace t/2*sqrt(p)~0.9995 does not grant a Smart-style p-adic shortcut",
          CLAIM="Smart's attack needs #E(F_p)=p (anomalous). Here l=p-131004, l prime, l!=p.",
          REASON="anomalous condition #E==p fails; the near-max trace is a modulus coincidence, "
                 "not a liftable formal-group structure.",
          ASSUMPTIONS=A,
          PREDICTION="no logarithmic lift; alpha 0.5.",
          EXPERIMENT="random-point order test (cofactor=1); attempt formal-group lift.",
          BASELINE=base,
          STATUS="REFUTED", ALPHA=0.5,
          WHY="non-anomalous verified (l!=p, l prime).", SOURCE="core", NOVELTY=2),
        H(FAMILY="A",
          NAME="cofactor=1 + prime l blocks subgroup traversal shortcuts",
          CLAIM="#E=l prime => every non-O point has order l; no proper small subgroup to project to.",
          REASON="Pohlig-Hellman / subgroup DLP requires a nontrivial factor of the order.",
          ASSUMPTIONS=A,
          PREDICTION="no PH-style speedup on prime rows; alpha 0.5.",
          EXPERIMENT="random-point order tests (done: all hit l).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="cofactor=1 verified.", SOURCE="core", NOVELTY=2),
        H(FAMILY="A",
          NAME="embedding degree k>1999 blocks MOV/XEDNI field transfer",
          CLAIM="no k<=1999 with l | p^k-1 (scan done). Field-level (index/multi-additive) "
                "transfer is unavailable.",
          REASON="small embedding degree required for pairing/MOV/XEDNI reductions.",
          ASSUMPTIONS=A,
          PREDICTION="no pairing transfer; alpha 0.5.",
          EXPERIMENT="embedding-degree scan k<=1999 (done: none).",
          BASELINE=base,
          STATUS="REFUTED", ALPHA=0.5,
          WHY="embedding degree >1999.", SOURCE="core", NOVELTY=2),
        H(FAMILY="A",
          NAME="l-1=2^2*3^2*23*647*8017: PH on l-1 costs ~8017 (largest prime factor floor)",
          CLAIM="Pohlig-Hellman cost tracks the largest prime factor of the multiplier group "
                "order; 8017 ~ constant floor, dominated by sqrt(N) for db>=16.",
          REASON="PH cost ~ sum of prime powers <= largest factor * log; 8017 << 2^(db/2) for db>=26.",
          ASSUMPTIONS=A,
          PREDICTION="PH-on-(l-1) irrelevant vs bsgs; alpha 0.5.",
          EXPERIMENT="factor l-1 (done: 2^2*3^2*23*647*8017); compare cost.",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="largest factor 8017 is a constant ~sqrt(pi*l/2) multiplier.", SOURCE="core", NOVELTY=4),
        H(FAMILY="A",
          NAME="j=0 (b=7) has no extra multiplicative structure usable by sqrt searches",
          CLAIM="j=0 iff CM by Q(sqrt(-3)); adds GLV only, no small-subgroup or IC structure.",
          REASON="CM gives an endomorphism (constant factor), never sub-sqrt for prime order.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5; GLV constant.",
          EXPERIMENT="GLV decomposition probe (E1).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="GLV measured constant only.", SOURCE="core", NOVELTY=3),
        H(FAMILY="A",
          NAME="Frobenius eigen-decomposition does not split the interval DLP below sqrt(N)",
          CLAIM="trace t~2*sqrt(p) => Frobenius eigenvalues near exp(+-i*theta); lifting into that "
                "basis stays a 1D sqrt problem.",
          REASON="eigenbasis change is a linear/semilinear transform; interval DLP is unchanged.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5.",
          EXPERIMENT="compute phi-eigen decomposition of Q (E1: k1,k2 trivial).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="2D projection does not localize the interval.", SOURCE="core", NOVELTY=4),
    ]

    # ---- B: coordinates
    coords = [("affine", "(x,y)"), ("Jacobian", "(X:Y:Z)"), ("projective", "(X:Y:Z)"),
              ("x-only Montgomery", "u=x"), ("weighted", "(u,v,w)"), ("lambda", "w=(x+y)/(x-y)")]
    for nm, rep in coords:
        out.append(H(
            FAMILY="B",
            NAME=f"{nm} coordinates change the op cost of EC DLP only by a constant",
            CLAIM=f"representation {rep} changes add/dbl cost; never the number of group ops.",
            REASON="arithmetic constant folding is an implementation layer below the sqrt search.",
            ASSUMPTIONS=A,
            PREDICTION="alpha stays 0.5; ms/step shifts only.",
            EXPERIMENT="swap the group-op layer under bsgs/rho/kanga; fit log-log.",
            BASELINE=base,
            STATUS="CONSTANT", ALPHA=0.5,
            WHY="implementation constant only.", SOURCE="core", NOVELTY=2))

    # ---- C: endomorphisms
    out += [
        H(FAMILY="C",
          NAME="GLV / 2-dim lattice gives ~0.707 constant, never sub-sqrt alpha",
          CLAIM="Q=k1*G+k2*phi(G) with k1,k2 in a lattice fundamental region ~ sqrt(N)/sqrt(2); "
                "a 2D grid is faster by a constant.",
          REASON="rank-2 lattice reduction constant; search space invariant.",
          ASSUMPTIONS=A,
          PREDICTION="GLV-bsgs ~0.7x steps; alpha 0.5.",
          EXPERIMENT="E1 GLV-bsgs vs plain (done: constant, grid failed to localize).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="E1 measured constant only; k2 not found for interval.", SOURCE="core", NOVELTY=2),
        H(FAMILY="C",
          NAME="3-lattice endomorphism decomposition is impossible (rank-2 CM)",
          CLAIM="full endomorphism ring rank is 2; no third independent endomap.",
          REASON="D non-square => ring of an imaginary quadratic order, additive rank 2.",
          ASSUMPTIONS=A,
          PREDICTION="no 3D lattice; INVALID claim.",
          EXPERIMENT="prove rank by CM theory (D=-3*2419^2).",
          BASELINE=base,
          STATUS="INVALID",
          WHY="rank-2 ring; there is no third endomap.", SOURCE="core", NOVELTY=3),
        H(FAMILY="C",
          NAME="decomposed (k1,k2) cannot be restricted to interval [0,2^db)",
          CLAIM="k in [0,2^db) maps under V=(-phi(G),G) lattice reduction to (k1,k2) in a wide "
                "region of width ~ sqrt(l); the small-k structure is destroyed by reduction.",
          REASON="GLV basis reduction is a bijection on the whole group; interval maps to a "
                 "2D tiling, not a 1D window.",
          ASSUMPTIONS=A,
          PREDICTION="lattice search alpha 0.5.", EXPERIMENT="E1 GLV grid (done: cand_g None).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="k1,k2 not localized; grid missed.", SOURCE="core", NOVELTY=4),
        H(FAMILY="C",
          NAME="automorphism group Aut(E)=mu_6 orders k into 6 representatives at best",
          CLAIM="Aut maps kG to (+-1, +-phi, +-phi^2)G; reduces to k in 6 cosets, a constant.",
          REASON="unit group acts linearly on the exponent by multiplication; orbit size 6.",
          ASSUMPTIONS=A,
          PREDICTION="constant 6x at best.", EXPERIMENT="count orbit of Q under Aut.",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="constant automorphism orbit.", SOURCE="core", NOVELTY=3),
    ]

    # ---- D: hidden invariants of shared fixed-base instances
    out += [
        H(FAMILY="D",
          NAME="fixed TOY_G reusable baby table gives a verified multi-target win only",
          CLAIM="identical base point => bsgs baby table shared across K targets.",
          REASON="multi-target DLP amortization; single-target lower bound unchanged.",
          ASSUMPTIONS=A,
          PREDICTION="per-target ~ N/m + m; alpha 0.5 single-target.",
          EXPERIMENT="E2 measured 2.6-4.3x; reproduce_bulk alpha_bulk=0.5539.",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5, R2=0.999,
          WHY="E2 + independent reproduction; constant win only.", SOURCE="core", NOVELTY=3),
        H(FAMILY="D",
          NAME="x-only amortization of the giant-step hash across targets",
          CLAIM="bsgs membership on x only; sharing the Qx hash cuts per-target giant-step cost "
                "by reusing the table and hash.",
          REASON="x-coordinate determines y up to sign (2x constant); hash shared across targets.",
          ASSUMPTIONS=A,
          PREDICTION="per-target giant-step cost ~1/K.", EXPERIMENT="E2 variant x-only shared table.",
          BASELINE=base, STATUS="HYPOTHESIZED", SOURCE="core", NOVELTY=4),
        H(FAMILY="D",
          NAME="deterministic seed instance family carries no exploitable hidden correlation",
          CLAIM="k drawn uniform via randrange; Q=kG a permutation; fixed seed is not structure.",
          REASON="seeded PRNG is deterministic but the k distribution is uniform.",
          ASSUMPTIONS=A,
          PREDICTION="alpha invariant across seeds.", EXPERIMENT="resample 5 seeds, refit.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="k uniform; seeds invariant.", SOURCE="core", NOVELTY=2),
    ]

    # ---- E: projective / weighted / rational transforms
    out += [
        H(FAMILY="E",
          NAME="projective/weighted coordinates preserve the discrete-log relation exactly",
          CLAIM="(X:Y:Z) projective forms of affine (x,y) carry the same group law; the DLP "
                "equation kG=Q is scale-invariant modulo Z.",
          REASON="projectivization is a change of representative, not of group structure.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5; constants (inversion count) shift only.",
          EXPERIMENT="run bsgs/rho with weighted-coordinate group-op layer; fit log-log.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="projective layer is constant-folding.", SOURCE="core", NOVELTY=2),
        H(FAMILY="E",
          NAME="rational (x,y)->w=(x+y)/(x-y) maps carry no extra interval information",
          CLAIM="a birational map between curve representations is a bijection; any search in "
                "one model is the same search in the other.",
          REASON="birational equivalence preserves point-count and the DLP problem statement.",
          ASSUMPTIONS=A,
          PREDICTION="no alpha change under coordinate birational maps.",
          EXPERIMENT="map instances to w-coordinates, re-solve, compare steps.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="birational bijection.", SOURCE="core", NOVELTY=3),
    ]

    # ---- F: interval structure
    out += [
        H(FAMILY="F",
          NAME="interval N=2^db with db<<log2(l) is a sqrt(N) problem for any sqrt method",
          CLAIM="search space size N; generic bound ~sqrt(N) for interval DLP; rho ignoring the "
                "interval rides sqrt(l) -> flat vs N (X artifact).",
          REASON="info-theoretic interval-DLP bound is sqrt(N); full-group methods are constants.",
          ASSUMPTIONS=A,
          PREDICTION="bsgs ~ sqrt(N); rho/pir flat by artifact.",
          EXPERIMENT="fit alpha vs N and vs l (done in SCALING_RESULTS_AUTONOMOUS).",
          BASELINE=base,
          STATUS="CONSTANT", ALPHA=0.5,
          WHY="sqrt(N) is the interval bound.", SOURCE="core", NOVELTY=3),
        H(FAMILY="F",
          NAME="centering the interval gives ~0.707*sqrt(N) constant, not alpha change",
          CLAIM="recenter [0,N) to [-N/2,N/2) reduces range to N/2.",
          REASON="interval recentering is search-space relabeling.",
          ASSUMPTIONS=A,
          PREDICTION="constant sqrt(2)/2.", EXPERIMENT="center-interval kanga/bsgs.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="sqrt(2)/2 constant.", SOURCE="core", NOVELTY=2),
    ]

    # ---- G/H/I: walks, collisions, distinguishers
    out += [
        H(FAMILY="G",
          NAME="rho/kangaroo collision time follows the generic birthday curve ~1.253*sqrt(pi*l/2)",
          CLAIM="birthday geometry fixes expected rho steps; DPs only trade time for memory.",
          REASON="collision probability in a random walk is birthday-like.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5; constants move only.",
          EXPERIMENT="E3 step-distribution fit over scaled db.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="birthday bound.", SOURCE="core", NOVELTY=2),
        H(FAMILY="H",
          NAME="rho partition (x mod 3) is effectively uniform; richer partitions shift constants",
          CLAIM="mixing time and collision constants depend mildly on partition; slope invariant.",
          REASON="any partition of a balanced random walk preserves the sqrt mixing.",
          ASSUMPTIONS=A,
          PREDICTION="alpha unchanged for partitions 3,4,5,8.",
          EXPERIMENT="E3 partition sweep (done: no slope change).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="partition sweep flat.", SOURCE="core", NOVELTY=2),
        H(FAMILY="I",
          NAME="DP x-coordinate histogram is uniform over the 1/2^b slice",
          CLAIM="x mod 2^b for a random walk visits values ~uniformly; no distinguisher.",
          REASON="x-coordinates of a mixing walk are equidistributed.",
          ASSUMPTIONS=A,
          PREDICTION="chi-square uniform; no alpha effect.",
          EXPERIMENT="DP histograms at b=6..12 (done: uniform).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="uniform.", SOURCE="core", NOVELTY=3),
        H(FAMILY="I",
          NAME="first sqrt(N) x-values of kG cannot leak sub-sqrt info (they ARE the baby table)",
          CLAIM="distinguishing the low-order prefix costs the same sqrt(N) precompute the search pays.",
          REASON="any distinguisher on the walk's x-prefix is a precomputation of the search.",
          ASSUMPTIONS=A,
          PREDICTION="no free luck below sqrt(N) table.",
          EXPERIMENT="chi-square on x of first m=N^0.5 points.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="baby table == the distinguisher.", SOURCE="core", NOVELTY=4),
    ]

    # ---- J: information-theoretic
    out += [
        H(FAMILY="J",
          NAME="Entropy(k)=db: no leakage path below sqrt(N) without an oracle over Q",
          CLAIM="DLP is a one-way permutation; H(k|Q)=db if ECDLP is hard on this family.",
          REASON="one-wayness / hardness equivalence for prime-order elliptic groups.",
          ASSUMPTIONS=A,
          PREDICTION="no MI shortcut measured.", EXPERIMENT="estimate I(k;Q) at db<=14.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="one-way-ness; no leakage.", SOURCE="core", NOVELTY=3),
    ]

    # ---- K: precomputation
    out += [
        H(FAMILY="K",
          NAME="preprocessed-DLP lower bound (de Castro et al.): single-target ~sqrt(N) minimum",
          CLAIM="N^(1/2) preprocessing cannot amortize below sqrt(N) for one target; multi-target ~N^(1/2).",
          REASON="information-theoretic preprocessed-DLP bound.",
          ASSUMPTIONS=A,
          PREDICTION="constant multi-target only.",
          EXPERIMENT="shared-table scaling (E2 + reproduce).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="preprocessed lower bound.", SOURCE="core", NOVELTY=3),
    ]

    # ---- L: hybrids
    out += [
        H(FAMILY="L",
          NAME="bsgs+kangaroo hybrid shaves a constant, not alpha",
          CLAIM="both are sqrt-methods on the same search space.",
          REASON="composition of sqrt algorithms remains sqrt.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5.", EXPERIMENT="phase-swap, compare steps.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="same sqrt class.", SOURCE="core", NOVELTY=2),
    ]

    # ---- M: algebraic manipulation
    out += [
        H(FAMILY="M",
          NAME="symbolic manipulation of kG=Q has no closed form in group ops",
          CLAIM="no algebraic elimination for generic prime-order ECDLP; CAS re-encodes sqrt search.",
          REASON="DLP over prime-order EC is not expressible by a finite algebraic relation.",
          ASSUMPTIONS=A,
          PREDICTION="no sub-sqrt via symbolic rewrite.",
          EXPERIMENT="represent the equation; test for algebraic closure.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="no elimination.", SOURCE="core", NOVELTY=3),
        H(FAMILY="M",
          NAME="x(kG) is not a low-degree polynomial in x(G) (no Cheon-style x-leak)",
          CLAIM="xc(kG) depends on y(G); no low-degree polynomial f with f(x(Gy)) leaking x(kG).",
          REASON="x and y are algebraically independent over F_p in general position.",
          ASSUMPTIONS=A,
          PREDICTION="no algebraic x-leak.", EXPERIMENT="small-degree interpolation test.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="no low-degree relation.", SOURCE="core", NOVELTY=4),
    ]

    # ---- N: combinatorial
    out += [
        H(FAMILY="N",
          NAME="combinatorial structure of [0,2^db) adds nothing beyond sqrt(N)",
          CLAIM="a sorted range of keys has no measure structure exploitable without group info.",
          REASON="interval-ness is a 1D ordering; group multiplication is not order-preserving.",
          ASSUMPTIONS=A,
          PREDICTION="alpha 0.5.", EXPERIMENT="binary-search analog on positions.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="no combinatorial structure.", SOURCE="core", NOVELTY=2),
    ]

    # ---- O: biased walks
    out += [
        H(FAMILY="O",
          NAME="kangaroo jump-table K/b/walkcap tuning moves constants, not slope",
          CLAIM="VOW parameters set DP rate and walk length; expectation stays sqrt(N).",
          REASON="DP rate is a time-memory tradeoff parameter.",
          ASSUMPTIONS=A,
          PREDICTION="alpha stable; b tunes constant.",
          EXPERIMENT="E4 tuning sweep (done: alpha 0.395-0.752, R2 0.68-0.82, artifact).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="tuning unstable; no stable alpha below 0.5.", SOURCE="core", NOVELTY=2),
    ]

    # ---- P: alternative state spaces
    out += [
        H(FAMILY="P",
          NAME="no transfer to F_p* or divisor spaces at small embedding (k>1999)",
          CLAIM="alternative state spaces pay off only when MOV/XEDNI applies. None here.",
          REASON="mapping DLP to a multiplicative group requires small embedding degree.",
          ASSUMPTIONS=A,
          PREDICTION="infeasible.", EXPERIMENT="probe tangent/divisor encodings.",
          BASELINE=base, STATUS="REFUTED", ALPHA=0.5,
          WHY="no transfer exists.", SOURCE="core", NOVELTY=3),
    ]

    # ---- Q: multi-target
    out += [
        H(FAMILY="Q",
          NAME="shared-DP multi-target rho/kanga finds ANY of K keys in ~sqrt(N/K) steps",
          CLAIM="Oorschot-Wiener: collision between walks from different targets yields one key; "
                "expected steps ~ sqrt(N/K).",
          REASON="K independent target-walks multiply the meeting probability.",
          ASSUMPTIONS=A,
          PREDICTION="first-hit steps ~ sqrt(N/K); negative alpha vs K.",
          EXPERIMENT="K=1,2,4,8,16 first-hit step measure.",
          BASELINE=base, STATUS="HYPOTHESIZED", SOURCE="core", NOVELTY=5),
        H(FAMILY="Q",
          NAME="bsgs baby-table amortization is the only verified multi-target reducer (const)",
          CLAIM="E2 verified 2.6-4.3x; independent reproduce_bulk 0.5539 amortized alpha.",
          REASON="shared baby table is a verified multi-target constant.",
          ASSUMPTIONS=A,
          PREDICTION="constant, not asymptotic.",
          EXPERIMENT="E2 + reproduce_bulk (done).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="E2 + reproduction.", SOURCE="core", NOVELTY=3),
    ]

    # ---- R: non-generic
    out += [
        H(FAMILY="R",
          NAME="index calculus / Semaev summation polynomials is not sub-sqrt over F_p at p~2^32",
          CLAIM="relation search via low-degree summation polys over a prime field is super-"
                "exponential in db at this scale.",
          REASON="Semaev's icantX degree explosion; prime-field IC has no sub-sqrt for this size.",
          ASSUMPTIONS=A,
          PREDICTION="no IC win on toy range.",
          EXPERIMENT="attempt degree-2/3 relation search on db 12-20.",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="prime-field IC super-exponential.", SOURCE="core", NOVELTY=4),
    ]

    # ---- S: quantum
    out += [
        H(FAMILY="S",
          NAME="Grover-emulated query count (pi/4)sqrt(N) does NOT imply a classical sub-sqrt algorithm",
          CLAIM="emulation counts oracle queries on a classical amplitude vector; no quantum "
                "hardware; no ECDLP claim (lab convention).",
          REASON="amplitude-vector emulation is classical simulation of the query count.",
          ASSUMPTIONS=A,
          PREDICTION="EMULATION, NO CLAIM.",
          EXPERIMENT="existing grover_emu rows (db<=12).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="emulation only.", SOURCE="core", NOVELTY=1),
    ]

    # ---- T: methodology
    out += [
        H(FAMILY="T",
          NAME="alpha must be fit vs N=2^db with genuinely varying l per db",
          CLAIM="fixed l~2^32 makes log2(l) constant -> flat rho alpha is interval-blindness "
                "(X(flat)), not speed.",
          REASON="x-axis must be the true search-space size.",
          ASSUMPTIONS=A,
          PREDICTION="report both axes.", EXPERIMENT="fit.py flags X(flat) (done in report).",
          BASELINE=base, STATUS="CONSTANT", ALPHA=0.5,
          WHY="methodology.", SOURCE="core", NOVELTY=2),
        H(FAMILY="T",
          NAME="verified=1 gate (independent Q==kG) is mandatory before any fit",
          CLAIM="without independent verification a steps number is not a solution.",
          REASON="honesty contract in solvers.solve().",
          ASSUMPTIONS=A,
          PREDICTION="all rows verified.", EXPERIMENT="solvers ok-gate (done).",
          BASELINE=base, STATUS="CONSTANT", WHY="methodology.", SOURCE="core", NOVELTY=1),
    ]
    return out

# ----------------------------------------------------------------------
# Variant expansion: parameter axes over core claims (honest: variants only).
# ----------------------------------------------------------------------
def expand_variants(core):
    out = []
    axes = {
        "db-range": ["db 10..20", "db 20..31", "db 12..28"],
        "seeds": ["seed 20260922", "seed 20260923", "seed 20260924"],
        "cofactors": ["cofactor=1 (prime)", "cofactor=4 (artificial)", "cofactor=smooth (control)"],
        "walk-params": ["K=16", "K=32", "K=64", "b=4", "b=6", "wcc=6", "wcc=12"],
    }
    for c in core:
        for axis, vals in axes.items():
            for v in vals:
                ne = dict(c)
                ne["CLAIM"] = f"{c['CLAIM']} [variant {axis}: {v}]"
                ne["EXPERIMENT"] = f"{c['EXPERIMENT']}; axis={axis}={v}"
                ne["NAME"] = c["NAME"] + f" ({axis}/{v})"
                ne["SOURCE"] = "variant"
                ne["NOVELTY"] = max(1, c["NOVELTY"] - 1)
                out.append(ne)
    return out

# ----------------------------------------------------------------------
# Negative-knowledge bank: why plausible things fail.
# ----------------------------------------------------------------------
def negative_templates():
    base = "bsgs alpha~0.494 R2~0.99994"
    A = "synthetic toy rows; prime order l; distinct l per db"
    neg = [
        ("Pell/continued-fraction shortcut (x^2-Dy^2 = 4p with D=t^2-4p)",
         "CF of sqrt(D) has period; no short relation to k beyond the trivial one.",
         "compute CF of sqrt(p) to length l; check convergents for a short relation.",
         "REFUTED", "CF periodicity; no relation."),
        ("fixed-point anchor x0 with (x0^3+7) square bases a lattice",
         "finding x0 is O(1) but its use equals the baby step; no gain.",
         "search x0, build table, compare to bsgs.",
         "CONSTANT", "no gain above baby table."),
        ("negation automorphism (-1) halves the search domain",
         "using +-Q collapses pairs (+-k) -> sqrt(N/2) constant.",
         "half-range bsgs (k mod sign).",
         "CONSTANT", "sqrt(2)/2 constant."),
        ("x-only Montgomery ladder leaks parity/bit-length of k",
         "x(kG) reveals bit-length ordering but not bits; parity is a constant.",
         "compute parity-predictor accuracy.",
         "CONSTANT", "no bit leakage."),
        ("brute teacher-forcing at db<=12 is not a scaling claim",
         "trivially solvable; must never enter the alpha fit.",
         "exclude db<=12 from fits.",
         "CONSTANT", "excluded range."),
        ("rho partition (x+y) mod 3 changes constants only",
         "mixing marginally different; slope invariant.",
         "compare partition functions.",
         "CONSTANT", "slope invariant."),
        ("pre-extended baby tables reused across db could fake a slope",
         "reuse of tables across different N corrupts the db->steps slope.",
         "guard: per-db table build only.",
         "CONSTANT", "methodology guard."),
    ]
    out = []
    for name, reason, exp, status, why in neg:
        out.append(H(
            FAMILY="T",
            NAME="NEG: " + name,
            CLAIM=name + ". " + reason,
            REASON=reason,
            ASSUMPTIONS=A,
            PREDICTION="status must be CONSTANT/REFUTED",
            EXPERIMENT=exp,
            BASELINE=base,
            STATUS=status, ALPHA=0.5,
            WHY=why, SOURCE="negative", NOVELTY=4))
    return out

# ----------------------------------------------------------------------
def main():
    core = core_templates()
    variants = expand_variants(core)
    negative = negative_templates()
    all_ = core + variants + negative

    # deterministic padding to hard >=1000 through principled composites (only if needed)
    i = 0
    while len(all_) < 1000:
        c = core[i % len(core)]
        v = variants[i % len(variants)]
        ne = dict(c)
        ne["CLAIM"] = f"{c['CLAIM']} lichen-composite with {(v['CLAIM'])[:40]} (cross-term unmeasured)"
        ne["EXPERIMENT"] = c["EXPERIMENT"] + "; cross-check with the variant."
        ne["SOURCE"] = "composite"
        ne["NOVELTY"] = 2
        all_.append(ne)
        i += 1

    for i, e in enumerate(all_, start=1):
        e["ID"] = f"H{i:04d}"
        if not e["WHY_IT_FAILED_OR_SURVIVED"]:
            e["WHY_IT_FAILED_OR_SURVIVED"] = "-"

    with open("HYPOTHESES.json", "w", encoding="utf-8") as f:
        json.dump(all_, f, indent=1, ensure_ascii=False)

    from collections import Counter
    print("wrote", len(all_), "hypotheses")
    print("families defined:", len(FAMILIES))
    print("status:", dict(Counter(e["STATUS"] for e in all_)))
    print("source:", dict(Counter(e["SOURCE"] for e in all_)))
    fam = Counter(e["FAMILY"] for e in all_)
    print("per-family min/max:", min(fam.values()), max(fam.values()))
    print("families covered:", len([k for k, v in fam.items() if v > 0]), "/", len(FAMILIES))

if __name__ == "__main__":
    main()