# BOTTLENECKS.md — Systematic Bottleneck Analysis

## Mission
Map every bottleneck in the hash computation stack, from physics to algorithms.
Each bottleneck is a potential attack surface for a breakthrough.

---

## 1. Transistor-Level Bottlenecks

### 1.1 Sub-threshold Leakage
- **Problem**: At 5nm, transistor threshold voltage (Vt) is ~0.3V. Thermal voltage
  kT/q = 26mV at 300K. The ratio Vt/(kT/q) ≈ 11.5, meaning ~1 in 100,000
  electrons tunnel through the barrier thermally.
- **Impact**: 15-25% of total power is pure waste leakage.
- **Scaling**: Gets WORSE at 3nm/2nm as oxide thickness shrinks.
- **Attack vector**: Cryogenic operation (reduce kT), or entirely different switch
  mechanism (e.g., tunnel FET, superconducting logic).

### 1.2 Gate Oxide Tunneling
- **Problem**: At 5nm, gate oxide is ~2-3 atomic layers thick. Electrons tunnel
  directly through the insulator.
- **Impact**: Additional static power, reliability degradation.
- **Attack vector**: High-κ dielectrics (already in use), or non-electronic switches.

### 1.3 Velocity Saturation
- **Problem**: At short channel lengths, carrier velocity saturates at ~10⁷ cm/s.
  Further voltage increase doesn't speed up switching.
- **Impact**: Limits maximum clock frequency per voltage step.
- **Attack vector**: Ballistic transport (carbon nanotubes), optical interconnects.

### 1.4 Random Dopant Fluctuation
- **Problem**: At 5nm, a transistor channel may have only 20-50 dopant atoms.
  Statistical variation of ±5 atoms changes Vt by ~50mV.
- **Impact**: Forces voltage margins (worst-case Vdd > typical needed Vdd).
- **Attack vector**: Undoped channels (FD-SOI already partially addresses this).

---

## 2. Logic-Level Bottlenecks

### 2.1 Instruction Decode Overhead (CPU/GPU)
- **Problem**: CPU decodes variable-length x86 instructions. Even RISC-V needs
  decode logic. For SHA-256, the "instructions" are fixed — decode is pure waste.
- **Impact**: 10-20% of core power in CPU/GPU goes to decode.
- **Solution in ASIC**: Hard-wired pipeline. Already done. No more gain here.

### 2.2 Branch Prediction (CPU)
- **Problem**: SHA-256 has no branches (pure dataflow). But CPU still allocates
  branch predictors, reorder buffers, etc.
- **Impact**: ~5-10% of core power wasted.
- **Solution in ASIC**: Already eliminated.

### 2.3 Speculative Execution Overhead (CPU)
- **Problem**: CPU speculatively executes ahead, then rolls back if wrong.
  SHA-256 has perfect predictability — speculation is always right but costs power.
- **Impact**: ~3-8% power waste.
- **Solution in ASIC**: Already eliminated.

### 2.4 Clock Distribution
- **Problem**: A global clock must reach every flip-flop on the chip. At 2 GHz,
  clock wire RC delay causes skew. Buffer tree to fix skew consumes ~10% of power.
- **Impact**: 8-15% of total dynamic power.
- **Attack vector**: Clockless (asynchronous) design. Eliminate global clock entirely.
  Each pipeline stage handshakes with its neighbor. Estimated saving: 10-15%.

### 2.5 Register File Overhead
- **Problem**: Each SHA-256 round needs 8 working variables (a-h) plus 64 message
  words. At 32 bits each = 2304 bits = ~9000 transistors. At 4 transistors/bit SRAM,
  this is trivial but the register file read/write ports consume energy.
- **Impact**: ~2-5% of pipeline energy.
- **Attack vector**: Use flip-flops instead of SRAM for small register files (already
  done in most ASICs).

---

## 3. Memory-Level Bottlenecks

### 3.1 Cache Hierarchy (CPU/GPU)
- **Problem**: CPU/GPU has L1→L2→L3→DRAM hierarchy. SHA-256 working set is ~2.3 KB
  (fits in L1), but the nonce search loop touches the header (80 bytes) repeatedly.
- **Impact**: SHA-256 is NOT memory-bound — the hierarchy is irrelevant waste.
- **Solution in ASIC**: No cache at all. Direct register file. Done.

### 3.2 Memory Wall (For Memory-Bound Algorithms)
- **Problem**: DRAM latency ~50-100ns, bandwidth ~50 GB/s. For algorithms that
  need large random reads (ethash, randomX), this is the true bottleneck.
- **Impact**: For ethash, 4GB DAG read per hash dominates time.
- **Attack vector**: Near-memory computing (process data where it sits).
  In-memory computing (use DRAM capacitors as computation units).

### 3.3 SRAM Area
- **Problem**: SRAM at 7nm: ~0.027 µm² per bit (6T cell). For 1 MB SRAM = 27 mm².
  This is significant compared to die size.
- **Impact**: Limits on-chip buffer sizes, increases cost.
- **Attack vector**: Compute-in-memory using memristors or RRAM.

---

## 4. Interconnect Bottlenecks

### 4.1 On-Chip Wiring
- **Problem**: Metal wire RC delay scales poorly. At 7nm, minimum pitch is ~36nm.
  A wire spanning 1mm has ~10ps delay and ~10 fJ/mm energy.
- **Impact**: For SHA-256 pipeline with 64 stages, total wire length ~5-10mm.
  = ~50-100 ps delay, ~100 fJ energy from wiring alone.
- **Attack vector**: 3D stacking (shorter vertical wires), photonic interconnects.

### 4.2 Global Signal Distribution
- **Problem**: Reset, start, nonce counter must reach all pipeline instances.
  For 5000+ parallel pipelines, fan-out and wire length cause skew.
- **Impact**: Limits parallelism scaling efficiency.
- **Attack vector**: Hierarchical clock树, asynchronous design.

### 4.3 Chip-to-Chip Interconnect
- **Problem**: Multi-chip ASIC miners use serial links between chips. Latency and
  power for serialization/deserialization.
- **Impact**: ~5-10% overhead in multi-chip designs.
- **Attack vector**: Wafer-scale integration (no chip-to-chip needed).

---

## 5. Cooling Bottlenecks

### 5.1 Heat Density
- **Problem**: ASIC at 5nm, 3500W, ~80,000 mm² total die area = ~44 W/cm².
  Air cooling practical limit: ~100 W/cm² with extreme measures.
  Water cooling: ~1000 W/cm².
- **Impact**: Limits how much compute can be packed per unit area.
- **Attack vector**: Microfluidic cooling (channels in the chip), phase-change
  cooling, thermoelectric harvesting.

### 5.2 Thermal Throttling
- **Problem**: As temperature rises, leakage increases exponentially (roughly
  doubles per 10°C). This creates positive feedback: hot → more leakage → hotter.
- **Impact**: Forces over-provisioning of cooling, limits operating frequency.
- **Attack vector**: Cryogenic operation eliminates this entirely.

### 5.3 Temperature Non-Uniformity
- **Problem**: Hot spots on chip cause local thermal runaway. Some transistors
  run 30-50°C hotter than average.
- **Impact**: Worst-case thermal design must handle hot spots, not average.
- **Attack vector**: 3D stacking with distributed cooling channels.

---

## 6. Algorithm-Level Bottlenecks

### 6.1 SHA-256 Intrinsic Sequentiality
- **Problem**: Each compression round depends on the previous round's output.
  64 rounds × sequential dependency = minimum 64 cycles per block (pipelined:
  1 hash per 64 cycles throughput, but latency = 64 cycles).
- **Impact**: Sets the minimum time per hash for a single pipeline.
- **Attack vector**: 
  - Pre-compute round functions for known message patterns (lookup tables)
  - Approximate computing (skip rounds for "good enough" hashes)
  - Alternative hash functions with more parallelism
  - ASIC-level: interleave independent hashes perfectly

### 6.2 SHA-256d Double Hash
- **Problem**: Bitcoin uses SHA-256(SHA-256(block)). The second hash cannot start
  until the first completes. Adds 64 cycles of latency.
- **Impact**: 2x latency, but can be pipelined across nonces.
- **Attack vector**: Fuse both hashes into a single pipeline (already done in ASICs).

### 6.3 Message Schedule Computation
- **Problem**: W[16..63] requires 4 operations per word. Each depends on prior words.
  Creates a serial dependency chain in the first 48 rounds.
- **Impact**: Limits pipeline depth optimization.
- **Attack vector**: 
  - Compute W on-the-fly with folded logic (already done)
  - Pre-compute W for common nonce ranges
  - Use algebraic properties to reduce operations

### 6.4 Nonce Space Search Pattern
- **Problem**: Nonce is a 32-bit counter (4 billion values). After exhaustion,
  must modify extranonce in coinbase (requires pool communication).
- **Impact**: Limits burst performance to 4B hashes before state change.
- **Attack vector**: Larger nonce space (64-bit), or parallel nonce trees.

---

## 7. System-Level Bottlenecks

### 7.1 Power Delivery
- **Problem**: ASIC at 0.4V, 3500W → 8750A current. On-chip power distribution
  requires thick metal layers and massive decap arrays. IR drop across die
  causes voltage variation ±50mV.
- **Impact**: Limits minimum voltage (and thus power efficiency).
- **Attack voltage**: 
  - Distributed on-chip voltage regulators
  - Adaptive voltage per pipeline instance
  - Superconducting power delivery (zero resistance)

### 7.2 Clock Generation
- **Problem**: PLL generates global clock. Jitter < 1% required. At 2 GHz,
  1% jitter = 5 ps, which is comparable to wire delay.
- **Impact**: Limits maximum frequency.
- **Attack vector**: Asynchronous design eliminates clock entirely.

### 7.3 Testing and Yield
- **Problem**: At 5nm, die yield is ~70-80%. Defective pipelines must be disabled.
  Reduces effective hashrate per chip.
- **Impact**: 10-20% die area wasted on redundancy.
- **Attack vector**: Built-in self-repair, modular design.

### 7.4 Supply Voltage Scaling Wall
- **Problem**: Vdd cannot go below ~0.4V for CMOS because threshold voltage is
  ~0.3V and noise margin disappears. Below Vt, current drops exponentially.
- **Impact**: Dynamic power ∝ V²f. Stalled at ~0.4V means no more V² gains.
- **Attack vector**: 
  - Adiabatic computing (recover energy during discharge)
  - Superconducting logic (zero-voltage switching)
  - Reversible computing (no Landauer erasure)

---

## 8. Bottleneck Severity Ranking

| Rank | Bottleneck | Impact | Difficulty to Overcome |
|---|---|---|---|
| 1 | CMOS voltage scaling wall | ~25% potential | Extreme (physics) |
| 2 | Leakage at advanced nodes | ~20% waste | Hard (requires new materials) |
| 3 | Clock distribution | ~10% waste | Medium (async design) |
| 4 | SHA-256 sequential rounds | Fundamental limit | Hard (need new algorithm or precomp) |
| 5 | On-chip wiring delay/energy | ~10% waste | Hard (need new interconnect) |
| 6 | Thermal density limits | Hard wall | Medium (new cooling) |
| 7 | Manufacturing cost scaling | Economic wall | Extreme (new fabs) |
| 8 | Power delivery (IR drop) | Limits Vmin | Medium (new PDN) |
| 9 | Test/yield overhead | ~10-15% waste | Easy (already optimized) |
| 10 | Nonce space exhaustion | Minor | Easy (64-bit nonce) |

---

## 9. The Fundamental Insight

The #1 bottleneck is **NOT** any single technical limitation. It is the fact that
CMOS technology has reached the point where:

1. **Voltage scaling is dead** (stalled since ~2012)
2. **Frequency scaling is dead** (stalled since ~2005)  
3. **Leakage is increasing** (worse at every new node)
4. **Wire delay is becoming dominant** (worse at every new node)

These are all manifestations of the same underlying problem: **we are approaching
the fundamental energy cost of irreversible computation** (Landauer's limit), and
the gap between current practice and that limit is closing slowly.

Any breakthrough must either:
- **A)** Drastically reduce the energy per logical operation (new switch mechanism)
- **B)** Eliminate energy waste (leakage, clock, wiring)
- **C)** Compute MORE per operation (massive parallelism at same energy)
- **D)** Use a fundamentally different computation paradigm (optical, quantum, analog)
