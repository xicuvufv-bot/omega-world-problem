# CODE_ARCHAEOLOGY.md - Source Code Analysis

## Project: llm-circuit-finder

### Architecture
```
sweep.py          → Main orchestrator (scanning loop)
├── gguf_surgery.py  → GGUF file manipulation (core engine)
├── layer_path.py    → Layer path builder (user-facing)
├── math_probe.py    → Math evaluation probe
├── eq_probe.py      → EQ evaluation probe
├── reasoning_probe.py → BBH reasoning probe
├── compare_eval.py  → Benchmark comparison
└── visualize.py     → Heatmap generation
```

### Key Code Patterns

**1. GGUF Layer Mapping (gguf_surgery.py)**
```python
# Build layer mapping: new_idx -> original_layer_idx
layer_map = {}
for orig_idx in range(dup_end):
    layer_map[orig_idx] = orig_idx
for k in range(n_dup):
    layer_map[dup_end + k] = dup_start + k
for orig_idx in range(dup_end, orig_block_count):
    layer_map[orig_idx + n_dup] = orig_idx
```
This is the core algorithm that remaps layers for duplication.

**2. Layer Path Notation**
```
"0..14,12,13,14,15..39"
→ Layers 0-14 execute once
→ Layers 12-14 execute again (duplication)
→ Layers 15-39 execute once
Total: 43 layers (40 original + 3 duplicated)
```

**3. Sweep Strategy**
```python
# Three-phase sweep
# Pass 1: Large blocks, wide stride → find hot zone
# Pass 2: Small blocks, stride 1 → find exact boundaries
# Pass 3: Multi-pass, interleaved → explore exotic configs
```

### Dependencies
- `gguf` (GGUF file format)
- `requests` (API calls to llama-server)
- `tqdm` (progress bars)
- `numpy` + `matplotlib` (visualization)

### Size/Complexity
- Total Python: ~2000 lines
- Core surgery: ~500 lines
- Probe system: ~300 lines
- Sweep harness: ~400 lines
- Visualization: ~200 lines

## Project: layer-scan

### Architecture
```
layer-scan/
├── scanner.py      → Main scan loop
├── probes/
│   ├── math.py     → Math probe
│   ├── eq.py       → EQ probe
│   └── json.py     → JSON probe
├── backends/
│   ├── transformers.py → HuggingFace backend
│   └── exllamav2.py   → ExLlamaV2 backend
└── viz/
    └── heatmap.py  → Interactive heatmap
```

### Key Innovation
**Logit distribution scoring**: Instead of generating text and checking answers, score by comparing logit distributions to expected patterns. Deterministic, no sampling needed, much faster.

## Project: ADATE

### Architecture (1990s)
```
ADATE/
├── makespec         → Specification compiler (binary)
├── main1.sml        → SML/NJ bootstrap
├── <spec>.spec.sml  → Generated specification code
├── main2.sml        → SML/NJ runtime
├── main             → Compiled ADATE binary
└── *.spec           → Problem specifications
```

### Key Innovation
**Compound program transformations**: Neutral walks in genotype space to avoid combinatorial explosions. Each transformation is a sequence of small changes that preserve fitness.

### Modernization Path
1. Replace SML/NJ with Python or Rust
2. Replace manual fitness evaluation with LLM evaluation
3. Add modern problem domains (not just number sequences)
4. Package as API service
