# FINAL_METHOD.md - NeuroForge: Automated LLM Enhancement via Layer Surgery

## DISCOVERY

The forgotten technology is **RYS Layer Duplication** — a technique discovered by David Noel Ng in 2025 that exploits a fundamental property of transformer neural networks: during training, transformers self-organize into functional "reasoning circuits" — contiguous blocks of middle layers that perform complete cognitive operations as indivisible units.

**Key finding**: Duplicating these specific circuit blocks (re-running the same layers twice at inference) boosts model reasoning by **17-23% with zero training, zero weight changes, zero new data**. The model simply "thinks harder" through its own reasoning pipeline.

This was initially published on HuggingFace and GitHub, produced the #1 model on the Open LLM Leaderboard, but remained a community experiment rather than a commercial service.

## SOURCE

- **Primary**: David Noel Ng's RYS method (github.com/dnhkng/RYS, March 2025)
- **Extended**: LLM Circuit Finder (github.com/alainnothere/llm-circuit-finder, March 2026)
- **Automated**: layer-scan (PyPI package, April 2026)
- **Pruning research**: Gabe Ortiz's layer pruning experiments (March 2026)
- **Academic**: EMNLP 2025 paper "Layer Duplication in LLMs" confirming the technique

## CODE

The essential code components are:
1. **gguf_surgery.py** from llm-circuit-finder — reads/writes GGUF files with modified layer structure
2. **sweep.py** — automated (i,j) configuration scanner with probe evaluation
3. **layer_path.py** — builds any GGUF with explicit layer execution path
4. **Probe suites** — math, EQ, and reasoning evaluation probes

## MODERN COMPONENTS

1. **GGUF model format** — quantized models that fit consumer GPUs
2. **ExLlamaV2/V3** — optimized inference engines for quantized models
3. **llama.cpp** — universal local LLM runtime
4. **OpenAI API standard** — compatible serving infrastructure
5. **Automated benchmarking** — lm-evaluation-harness for standardized scoring

## FUSION

```
RYS Layer Duplication (2025, forgotten technique)
    + Automated Circuit Detection (modern automation)
    + Layer Pruning (interference removal)
    + OpenAI-compatible Proxy (serving layer)
    = NEUROFORGE: Automated LLM Enhancement Service
```

The fusion creates something no single component can do:
- **Scan** any model to find its reasoning circuits automatically
- **Plan** the optimal surgery (duplicate, prune, or combined)
- **Apply** the surgery to create an enhanced GGUF
- **Verify** improvement with standardized benchmarks
- **Serve** the enhanced model via standard API

## NEW CAPABILITY

**"Reasoning-as-a-Service"**: Companies can submit any open LLM and receive an enhanced version with measurably better reasoning — without training, without fine-tuning, without new data. The model thinks harder through its own existing circuits.

This is fundamentally different from:
- Fine-tuning (changes weights, needs data, costs $5K-15K)
- Quantization (reduces precision, loses some quality)
- Prompt engineering (constrained by context window)
- Inference optimization (OptiLLM-style, adds latency per request)

Layer surgery changes the **architecture** without changing the **weights**. It's orthogonal to all other techniques and can be stacked with them.

## PROBLEM

**Enterprise LLM Performance Gap**: Companies need better reasoning from local LLMs but cannot afford:
- Fine-tuning: $5K-15K setup + $2K-10K/month retainer
- API costs: $15-60 per million tokens for frontier models
- Training from scratch: millions in compute

**The gap**: A 70B open model running locally costs ~$0.01/M tokens but reasons poorly. A frontier API model reasons well but costs 100x more and sends data externally.

**NeuroForge fills this gap**: Enhanced open models that reason better at the same local cost.

## VALUE

1. **Cost reduction**: Enhanced 70B model reasons like a 100B+ model at 70B cost
2. **Latency improvement**: Better reasoning per token = fewer retries = lower total latency
3. **Privacy preservation**: Enhanced model runs locally, no data leaves infrastructure
4. **No training required**: Enhancement takes minutes, not weeks
5. **Composable**: Can be combined with fine-tuning for additional gains

## MONEY LOOP

```
SCAN model → DETECT circuits → PLAN surgery → APPLY modifications → VERIFY improvement → SERVE enhanced model → CHARGE per-model fee
    ↑                                                                                    |
    └────────────────────────── REPEAT with next model ──────────────────────────────────┘
```

**Revenue streams**:
1. Per-model enhancement: $500-2000 one-time fee
2. Enhanced model API: $0.005-0.02/M tokens (10-50% cheaper than frontier)
3. Subscription: $500-5000/month for continuous optimization
4. Enterprise: Custom enhancement pipelines for specific domains

## FIRST RESULT

**First verifiable result**: Apply layer surgery to Qwen2.5-32B, duplicate layers 7-9, measure reasoning improvement via BBH logical deduction benchmark.

Expected: 0.22 → 0.76 on logical deduction (245% improvement, matching published results).

## TEST

1. Load Qwen2.5-32B GGUF
2. Apply layer duplication via layer_path.py
3. Run BBH logical deduction probe
4. Compare with baseline
5. Measure latency overhead

## RESULT

Based on published research:
- **Reasoning**: +17-23% improvement on combined probes
- **Math**: +5-8% improvement on arithmetic tasks
- **Latency**: +7.5% overhead per token (3 extra layers on 40-layer model)
- **Memory**: +1.5 GiB VRAM for duplicated layers
- **Cost**: $0 GPU training cost (inference-only enhancement)

## RISKS

1. **Generalization**: Technique tested primarily on Qwen and Mistral architectures. May not work equally on all transformer models.
2. **Small models**: Models below ~20B parameters show less benefit (not enough layers for distinct reasoning circuits).
3. **Task specificity**: Duplication improves reasoning but may slightly degrade instruction following and code generation in some configurations.
4. **Competitive**: hoof.ai, Model Surgery, Dystrio are adjacent competitors. Our differentiation is automated detection + zero-training service model.
5. **Market timing**: The technique is gaining awareness fast. First-mover advantage is narrow.
