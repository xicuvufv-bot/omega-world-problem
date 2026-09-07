# IDEAS.md — 50+ Ideas for Compute Breakthrough

## Scoring System
Each idea scored 1-5 on four axes:
- **Novelty**: Is this genuinely new or just incremental?
- **Physics**: Does physics allow it? Theoretical basis?
- **Manufacturability**: Can it be built with known processes?
- **Expected Performance**: GH/s/W improvement potential over current ASICs

Total = sum of scores (max 20)

---

## CATEGORY A: Novel Transistor/Switch Mechanisms

### A1. Carbon Nanotube FET (CNFET) SHA-256 Pipeline
- **Principle**: Replace silicon channels with carbon nanotubes (ballistic transport)
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 2 | **Performance**: 4
- **Total**: 14
- **Notes**: IBM demonstrated 5nm CNFET. Ballistic transport = no velocity saturation.
  Could allow 0.1V operation. Major challenge: CNT alignment, purity.

### A2. Tunnel FET (TFET) Ultra-Low-Voltage Pipeline
- **Principle**: Use band-to-band tunneling instead of thermal injection.
  Sub-60mV/decade subthreshold swing (vs 60mV for MOSFET at 300K).
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 14
- **Notes**: Can operate at 0.1-0.2V. Trade-off: lower on-current → lower frequency.
  Net: may improve energy per hash even at lower speed.

### A3. Superconducting RSFQ Logic
- **Principle**: Use flux quanta in superconducting loops as bits.
  Switching energy ~10⁻¹⁹ J (10,000x less than CMOS).
- **Novelty**: 4 | **Physics**: 5 | **Manufacturability**: 1 | **Performance**: 5
- **Total**: 15
- **Notes**: Requires 4K cryogenic cooling. Net system energy may be worse unless
  cooling energy is negligible. Active research for HPC.

### A4. Spintronic Logic (MTJ-based)
- **Principle**: Use magnetic tunnel junctions for non-volatile logic.
  Zero leakage when idle. Potential for in-memory computation.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 13
- **Notes**: STT-MTJ already in MRAM. Could build SHA-256 pipeline with
  spin-based flip-flops. Leakage eliminated.

### A5. Phase-Change Logic
- **Principle**: GeSbTe switches between crystalline/amorphous states.
  Non-volatile, can be used for in-memory computing.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 13
- **Notes**: Intel/Optane demonstrated. Slow switching (~100ns) limits frequency.
  Better for memory-bound than compute-bound.

### A6. MEMS-Based Mechanical Logic
- **Principle**: Nano-scale mechanical switches. Zero leakage. Radiation-hard.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 1
- **Total**: 9
- **Notes**: Impractical speed. More novelty than performance.

### A7. Photonic Crystal Transistor
- **Principle**: Use photonic crystal cavities to create all-optical switches.
  Speed of light propagation, potential for extremely low energy.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 4
- **Total**: 12
- **Notes**: All-optical logic demonstrated in labs. Cannot scale to millions of gates
  yet. Nonlinear optical materials are lossy.

---

## CATEGORY B: Optical/Photonic Computing

### B1. SHA-256 via Fourier-Optic Matrix Multiply
- **Principle**: Use lens Fourier transforms to perform additions via interference.
  SHA-256 additions become optical wave superposition.
- **Novelty**: 5 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 5
- **Total**: 14
- **Notes**: Can theoretically perform 256 additions in parallel at speed of light.
  Challenge: converting between electronic and optical domains. Lossy.

### B2. WDM (Wavelength Division Multiplexing) Parallel Hash
- **Principle**: Encode different nonces on different wavelengths in a single fiber.
  Process all wavelengths simultaneously through shared optical SHA-256 logic.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 5
- **Total**: 15
- **Notes**: 100+ wavelengths in telecom. Each wavelength = independent hash pipeline.
  Total: 100x parallelism in a single waveguide. Huge potential if optical SHA-256 works.

### B3. Reservoir Computing (Optical)
- **Principle**: Use nonlinear optical fiber as a reservoir. Train readout weights.
  SHA-256-like function learned as a dynamical system.
- **Novelty**: 5 | **Physics**: 3 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 13
- **Notes**: Fundamental issue: SHA-256 is deterministic and exact. Reservoir computing
  is approximate. Cannot produce correct hashes.

### B4. Diffractive Neural Network for Hash
- **Principle**: Design diffractive layers that optically compute SHA-256.
  Each layer = one round. Speed of light propagation.
- **Novelty**: 5 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 4
- **Total**: 13
- **Notes**: MIT demonstrated diffractive networks for inference. SHA-256 requires
  exact modular arithmetic — very hard optically.

### B5. Integrated Photonic ASIC
- **Principle**: Silicon photonic chip with on-chip laser, modulators, detectors.
  Compute SHA-256 in optical domain, minimal electronic conversion.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 4
- **Total**: 14
- **Notes**: Most practical optical approach. Intel/Marvell already have silicon
  photonics fabs. Need to design optical SHA-256 datapath.

---

## CATEGORY C: In-Memory Computing

### C1. SRAM-Based Compute-in-Memory SHA-256
- **Principle**: Use SRAM bitlines as analog adders. Charge sharing performs
  addition of multiple bits simultaneously.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 4 | **Performance**: 3
- **Total**: 14
- **Notes**: Well-researched for ML inference. Adapting to SHA-256 modular addition
  is possible but precision (8-bit per addition) may not be enough for 32-bit math.

### C2. RRAM Crossbar SHA-256
- **Principle**: Resistive RAM crossbar performs matrix-vector multiply in one step.
  SHA-256 σ functions implemented as matrix operations.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 12
- **Notes**: RRAM variability is a major issue for exact computation.
  Better for approximate/AI workloads than deterministic hashing.

### C3. DRAM DIMM as Massive Lookup Table
- **Principle**: Pre-compute SHA-256 intermediate results for common patterns.
  Store in 64GB DRAM DIMM. Hash = series of lookups.
- **Novelty**: 2 | **Physics**: 3 | **Manufacturability**: 5 | **Performance**: 2
- **Total**: 12
- **Notes**: SHA-256 has 2^256 possible states — cannot precompute all.
  But for specific nonce ranges, partial precomputation could help.

### C4. ReRAM-Based In-Memory SHA-256
- **Principle**: Use ReRAM analog computing for the XOR operations in SHA-256.
  Multiple XOR operations performed in parallel on ReRAM array.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 12
- **Notes**: Analog XOR is lossy. Need ADC at output = energy cost.

### C5. 3D-Stacked SRAM + Logic Die
- **Principle**: Logic die on top, SRAM cache on bottom, connected by TSVs.
  SHA-256 state lives in the SRAM stack, reducing wire length.
- **Novelty**: 2 | **Physics**: 4 | **Manufacturability**: 4 | **Performance**: 3
- **Total**: 13
- **Notes**: HBM already does this. Adaptation for SHA-256 is straightforward.
  Benefit: ~30% reduction in wire energy.

---

## CATEGORY D: 3D/Advanced Packaging

### D1. Wafer-Scale SHA-256 Engine
- **Principle**: One entire 300mm wafer = single SHA-256 chip.
  ~70,000 mm² of compute. ~100,000 parallel pipelines.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 5
- **Total**: 14
- **Notes**: Cerebras demonstrated wafer-scale for ML. Needs defect tolerance.
  Power delivery across entire wafer is a challenge.

### D2. Chiplet-Based SHA-256 Array
- **Principle**: Many small SHA-256 chiplets (5mm² each) on organic interposer.
  Each chiplet = 100 pipelines. 1000 chiplets = 100,000 pipelines.
- **Novelty**: 2 | **Physics**: 4 | **Manufacturability**: 4 | **Performance**: 4
- **Total**: 14
- **Notes**: AMD already does chiplet. High yield (small die = cheap).
  Inter-chiplet communication overhead is the challenge.

### D3. Monolithic 3D (Sequential 3D)
- **Principle**: Build transistor layers on top of each other on same wafer.
  4-layer 3D = 4x compute density, shorter vertical wires.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 4
- **Total**: 13
- **Notes**: MIT/Stanford research. Thermal stacking is the main issue.
  Bottom layers heat up top layers.

### D4. Through-Silicon Via (TSV) Mesh
- **Principle**: 3D stack of logic dies connected by dense TSV mesh.
  Communication between layers at >100 GB/s.
- **Novelty**: 2 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 13
- **Notes**: Already used in HBM. Adaptation for SHA-256: pipeline stages
  distributed across vertical layers, reducing horizontal wire length.

### D5. Glass Core Substrate Packaging
- **Principle**: Replace organic interposer with glass. 10x better wiring density.
  Enable massive fan-out for chiplets.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 13
- **Notes**: Intel/Corning research. Not a compute breakthrough but enables
  higher density packaging.

---

## CATEGORY E: Novel Architectures

### E1. Systolic Array SHA-256
- **Principle**: 2D array of SHA-256 processing elements, each feeding its
  neighbor. Data flows through the array like a wave.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 15
- **Notes**: Google TPU uses this for matrix multiply. SHA-256 is not matrix-based,
  but systolic dataflow reduces wire length and control overhead.

### E2. Dataflow SHA-256 (No Von Neumann)
- **Principle**: No program counter, no instruction memory. Each PE is hardwired
  for one SHA-256 round. Data flows PE-to-PE.
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 4 | **Performance**: 4
- **Total**: 16
- **Notes**: Maximizes compute/energy by eliminating all control overhead.
  Each PE is just adders + muxes + registers. ~10,000 transistors per PE.

### E3. Reconfigurable SHA-256 Mesh
- **Principle**: Fine-grained mesh of ALUs, each configurable for one SHA-256
  operation. Run-time reconfigurable for different hash functions.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 13
- **Notes**: Like an FPGA but SHA-256-optimized. Flexible but less efficient
  than hardwired.

### E4. Wave Computing (Pulse-Driven)
- **Principle**: Instead of clock-driven flip-flops, use traveling pulses on
  transmission lines. Each pulse = one bit of computation.
- **Novelty**: 5 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 4
- **Total**: 13
- **Notes**: Theoretical concept. May work at microwave frequencies.
  Very hard to implement reliably.

### E5. Residue Number System (RNS) SHA-256
- **Principle**: Represent numbers in residue form (mod p1, p2, p3, ...).
  Addition/multiplication in RNS is fully parallel across moduli.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 14
- **Notes**: SHA-256 uses modular arithmetic. RNS can parallelize the additions.
  Conversion back from RNS is the bottleneck (Chinese Remainder Theorem).

### E6. Stochastic Computing Hash
- **Principle**: Represent numbers as random bit streams. AND gate = multiply.
 population count = value. SHA-256 in stochastic domain.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 2 | **Performance**: 2
- **Total**: 11
- **Notes**: Stochastic computing is inherently approximate. SHA-256 needs exact
  results. Could work for approximate pre-filtering.

### E7. Ternary Logic SHA-256
- **Principle**: Use 3-state logic (-1, 0, 1) instead of binary.
  Can represent larger numbers with fewer signals.
- **Novelty**: 3 | **Physics**: 3 | **Manufacturability**: 2 | **Performance**: 2
- **Total**: 10
- **Notes**: Doubled-balanced ternary has been explored. No compelling advantage
  for SHA-256 specifically.

---

## CATEGORY F: Algorithm-Hardware Co-Design

### F1. SHA-256 Round Precomputation ASIC
- **Principle**: Pre-compute common round function combinations.
  Store as lookup tables. Reduces 64 rounds to ~16 effective rounds.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 14
- **Notes**: Depends on message schedule predictability. For SHA-256, the message
  words are mostly fixed (block header). Can precompute W[0..15] combinations.

### F2. Pipelined Double-Hash Fusion
- **Principle**: Fuse SHA-256(SHA-256(x)) into a single pipeline.
  Second hash starts as soon as first partial state is available.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 15
- **Notes**: Already done in Bitcoin ASICs. But could be improved by
  interleaving nonces to hide second-hash latency.

### F3. Nonce-Parallel Architecture
- **Principle**: Each pipeline instance searches a different nonce simultaneously.
  No shared state between instances = perfect parallelism.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 15
- **Notes**: This IS what current ASICs do. The optimization is in maximizing
  instances per watt, not per chip.

### F4. Block-Header Partial Hash
- **Principle**: For Bitcoin, 76 of 80 header bytes are fixed for a difficulty
  period. Pre-compute intermediate hash state for fixed bytes.
  Only the 4-byte nonce varies.
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 4
- **Total**: 17
- **Notes**: HIGHEST SCORING IDEA. The first 3 message schedule words are
  derived from the fixed header. Pre-computing these saves 3 rounds of
  message schedule computation. ASIC already partially does this, but
  a dedicated "header precomp" unit could save ~5% power.

### F5. Alternative Hash Function Design
- **Principle**: Design a new hash function optimized for hardware implementation.
  More parallelizable than SHA-256, same security level.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 15
- **Notes**: BLAKE3, Keccak are more parallelizable. But Bitcoin uses SHA-256 —
  can't change the algorithm. This idea is for NEW applications.

### F6. Incremental Hashing
- **Principle**: When nonce changes by +1, only a few bits of the input change.
  Use incremental hash update instead of recomputing from scratch.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 15
- **Notes**: SHA-256 is NOT incremental by design (avalanche effect). But the
  message schedule partially reuses previous values. Could save ~30% of
  computation per incremental nonce.

---

## CATEGORY G: Cooling & Power

### G1. Immersion Cooling ASIC
- **Principle**: Submerge ASIC in dielectric fluid. 10x better heat transfer
  than air. Allows higher clock, lower voltage.
- **Novelty**: 1 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 14
- **Notes**: Already used in data centers. Not a compute breakthrough, but enables
  denser packing and ~20% better efficiency.

### G2. Thermoelectric Heat Recovery
- **Principle**: Use TEG (thermoelectric generator) to convert waste heat
  back to electricity. ~5% recovery.
- **Novelty**: 2 | **Physics**: 4 | **Manufacturability**: 4 | **Performance**: 2
- **Total**: 12
- **Notes**: TEG efficiency is low (5-8%). Small gain, not a breakthrough.

### G3. Microfluidic In-Package Cooling
- **Principle**: Etch cooling channels directly into the chip package.
  Liquid flows millimeters from the die surface.
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 14
- **Notes**: Allows 300+ W/cm² heat removal. Enables denser compute packing.

### G4. Cryogenic CMOS
- **Principle**: Operate CMOS at 77K (liquid nitrogen) or 4K.
  Leakage drops 1000x. Mobility increases 2-3x. Can reduce Vdd to 0.1V.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 3 | **Performance**: 5
- **Total**: 15
- **Notes**: Intel/IBM research. Net system efficiency depends on cooling cost.
  For hash computation (small chip), LN2 cost may be acceptable.

### G5. Adiabatic CMOS
- **Principle**: Recover energy during logic transitions by slowly charging/discharging
  capacitors through resonant circuits. ~90% energy recovery.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 12
- **Notes**: Limits frequency (slow transitions). May work for low-speed,
  high-efficiency hash computation.

---

## CATEGORY H: Unconventional Computing

### H1. Analog SHA-256
- **Principle**: Represent SHA-256 operations as analog voltage computations.
  Operational amplifiers for addition, multiplier circuits.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 12
- **Notes**: Precision is the killer. SHA-256 needs 32-bit integer math.
  Analog noise at 32-bit precision is extremely challenging.

### H2. Biological/Molecular Computing
- **Principle**: Use DNA or protein-based computation for hashing.
  Massive parallelism (10^18 molecules).
- **Novelty**: 5 | **Physics**: 2 | **Manufacturability**: 1 | **Performance**: 2
- **Total**: 10
- **Notes**: DNA computing is slow (hours per operation). Fun but impractical.

### H3. Quantum Annealing for Hash Search
- **Principle**: Use quantum annealer to search nonce space.
  Grover's algorithm gives quadratic speedup.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 4
- **Total**: 12
- **Notes**: Grover's gives √N speedup = 65536x for 32-bit nonce.
  But quantum error correction overhead is enormous.

### H4. Reversible Computing
- **Principle**: Design circuits where no information is erased (no Landauer cost).
  Theoretically zero energy per operation (minus leakage).
- **Novelty**: 5 | **Physics**: 4 | **Manufacturability**: 1 | **Performance**: 5
- **Total**: 15
- **Notes**: Requires keeping all intermediate states (unbounded memory).
  Practical implementations use Bennett's scheme with periodic garbage collection.
  Theoretical maximum but extremely hard to implement.

### H5. Neuromorphic SHA-256
- **Principle**: Implement SHA-256 as a spiking neural network.
  Spike-based computation is event-driven (no clock).
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 2 | **Performance**: 2
- **Total**: 11
- **Notes**: SHA-256 is deterministic digital logic. Neuromorphic is for
  pattern recognition. Not a natural fit.

### H6. Memristor Crossbar Hash
- **Principle**: Use memristor crossbar arrays for XOR operations.
  All XORs in a SHA-256 round performed in one step.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 13
- **Notes**: Memristor variability requires error correction. But the
  parallelism potential is high.

---

## CATEGORY I: Systems & Architecture

### I1. Near-Data Processing
- **Principle**: Place SHA-256 compute units next to DRAM in the DIMM slot.
  Eliminate data movement energy.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 4 | **Performance**: 3
- **Total**: 14
- **Notes**: Samsung/FUJITSU research. For memory-bound algorithms (ethash).
  Not helpful for SHA-256 (already compute-bound).

### I2. Photonic Interconnect + Electronic Compute
- **Principle**: Keep electronic SHA-256 pipelines but replace all wires
  with on-chip photonic links. Eliminate wire delay/energy.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 4
- **Total**: 13
- **Notes**: UC San Diego demonstrated on-chip optical link at 100 fJ/bit.
  Could save ~30% of pipeline energy.

### I3. Heterogeneous Pipeline
- **Principle**: Different pipeline stages optimized differently.
  Early stages (message schedule) on low-power logic, late stages
  (compression) on high-speed logic.
- **Novelty**: 2 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 3
- **Total**: 12
- **Notes**: Already done in some ASICs. Diminishing returns.

### I4. Massive SIMD Hash
- **Principle**: One instruction processes 1024+ nonces simultaneously.
  Ultra-wide datapath with minimal control.
- **Novelty**: 2 | **Physics**: 5 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 14
- **Notes**: Similar to GPU approach but without the GPU overhead.
  A dedicated "hash SIMD" processor.

### I5. Pipeline Flushing Optimization
- **Principle**: When difficulty changes, flush all pipelines and restart.
  Optimize the flush/restart transition to minimize downtime.
- **Novelty**: 1 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 2
- **Total**: 13
- **Notes**: Minor optimization. Already well-optimized in practice.

---

## CATEGORY J: Hybrid & Wild Ideas

### J1. SHA-256 on Optical Fiber + Electronic Control
- **Principle**: The compression function is computed optically (wave interference).
  The message schedule is computed electronically. Hybrid approach.
- **Novelty**: 5 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 5
- **Total**: 14
- **Notes**: Most ambitious optical approach. Combines the best of both worlds.

### J2. Superconducting + CMOS 3D Stack
- **Principle**: Superconducting RSFQ logic die on top, CMOS control/memory below.
  Communication through TSVs. Best of both worlds.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 1 | **Performance**: 5
- **Total**: 14
- **Notes**: Active research at some labs. Requires 4K cooling for SC layer.

### J3. SHA-256 on RISC-V with Custom Instructions
- **Principle**: Design RISC-V ISA extension with SHA-256-specific instructions.
  One instruction per round. Software-hardware co-design.
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 16
- **Notes**: OpenTitan already has SHA-256 instructions. This is incremental.

### J4. Approximate SHA-256 Pre-Filter
- **Principle**: Use approximate/partial hash to quickly eliminate 99.9% of nonces.
  Only compute full SHA-256 on the 0.1% that pass the filter.
- **Novelty**: 4 | **Physics**: 4 | **Manufacturability**: 3 | **Performance**: 4
- **Total**: 15
- **Notes**: Like Bitcoin's midstate optimization but more aggressive.
  The filter must be correct (no false negatives) but can have false positives.

### J5. SHA-256 on Memristive FPGA
- **Principle**: Replace SRAM-based FPGA LUTs with memristor-based LUTs.
  10x denser, non-volatile, faster reconfiguration.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 2 | **Performance**: 3
- **Total**: 12
- **Notes**: Memristor FPGA research at UC Santa Barbara. Not mature.

### J6. SHA-256 Blockchain (Chain of Pipelines)
- **Principle**: Instead of independent pipelines, chain them so pipeline N
  starts its hash from pipeline N-1's output. Creates a hash chain.
- **Novelty**: 3 | **Physics**: 4 | **Manufacturability**: 4 | **Performance**: 3
- **Total**: 14
- **Notes**: Not useful for Bitcoin (needs independent nonces), but could be
  useful for proof-of-work schemes that use hash chains.

### J7. SHA-256 with Pre-computed Round Keys
- **Principle**: For Bitcoin headers, the message words W[0..3] are partially fixed.
  Pre-compute K[i]+W[i] for common values. Save 3 additions per round.
- **Novelty**: 3 | **Physics**: 5 | **Manufacturability**: 5 | **Performance**: 3
- **Total**: 16
- **Notes**: This is the "Block-Header Partial Hash" idea (F4) from a different angle.
  Combining both could yield ~10% improvement.

### J8. Optical Neural Network Hash Lookup
- **Principle**: Use an optical neural network trained to approximate SHA-256.
  1000x faster than electronic. Use for approximate pre-filtering.
- **Novelty**: 5 | **Physics**: 2 | **Manufacturability**: 1 | **Performance**: 3
- **Total**: 11
- **Notes**: SHA-256 cannot be approximated — it must be exact.
  Unless used as a pre-filter only.

### J9. Quantum Dot Cellular Automata (QCA)
- **Principle**: Use quantum dot cells for computation. No current flow = zero
  dynamic energy. Coulomb interaction for logic.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 3
- **Total**: 11
- **Notes**: Very early research. Room temperature operation still a challenge.

### J10. Spin-Wave Computing
- **Principle**: Use spin waves in magnetic films for computation.
  Waves can interfere (add/multiply) at zero energy cost.
- **Novelty**: 4 | **Physics**: 3 | **Manufacturability**: 1 | **Performance**: 3
- **Total**: 11
- **Notes**: Lab demonstrations only. Encoding/decoding is the bottleneck.

---

## SCORING SUMMARY — TOP 10

| Rank | Idea | N | P | M | Per | Total |
|---|---|---|---|---|---|---|
| 1 | F4: Block-Header Partial Hash | 3 | 5 | 5 | 4 | **17** |
| 2 | E2: Dataflow SHA-256 (No Von Neumann) | 3 | 5 | 4 | 4 | **16** |
| 2 | F6: Incremental Hashing | 4 | 4 | 3 | 4 | **15** |
| 2 | F5: Alternative Hash Function | 4 | 4 | 3 | 4 | **15** |
| 2 | J3: RISC-V Custom Instructions | 3 | 5 | 5 | 3 | **16** |
| 2 | J7: Pre-computed Round Keys | 3 | 5 | 5 | 3 | **16** |
| 3 | G4: Cryogenic CMOS | 2 | 5 | 3 | 5 | **15** |
| 3 | B2: WDM Parallel Hash | 4 | 4 | 2 | 5 | **15** |
| 3 | D1: Wafer-Scale Engine | 3 | 4 | 2 | 5 | **14** |
| 3 | E1: Systolic Array | 2 | 5 | 5 | 3 | **15** |
