# COMPETITOR_ANALYSIS.md - Market Landscape

## Direct Competitors (Model Optimization)

### 1. hoof.ai
- **What**: Task-specific LLM pruning → offline executables
- **Approach**: Strip vocabulary, attention heads, layers irrelevant to task
- **Strength**: Zero-dependency output, complete privacy
- **Weakness**: Only pruning, no duplication; task-specific only
- **Pricing**: Custom enterprise pricing
- **Gap**: Doesn't boost reasoning; only reduces size

### 2. Model Surgery (model-surgery.com)
- **What**: Knowledge transplantation between models
- **Approach**: Rank-k conjugation, Procrustes alignment
- **Strength**: 99%+ alignment at frontier scale, zero training
- **Weakness**: Focused on knowledge transfer, not reasoning enhancement
- **Pricing**: Enterprise sales
- **Gap**: Different capability (transfer vs enhancement)

### 3. Dystrio
- **What**: Structural inference recompilation
- **Approach**: Physically rewrite MLP dimensions
- **Strength**: Composable with quantization, no runtime overhead
- **Weakness**: Width optimization only, not depth/circuit-based
- **Pricing**: Not yet public
- **Gap**: Different approach (width vs depth optimization)

### 4. Condense
- **What**: Model compression platform
- **Approach**: Knowledge distillation, GPTQ, pruning, LoRA
- **Strength**: Multiple compression strategies, token-based pricing
- **Weakness**: Focused on compression, not reasoning enhancement
- **Pricing**: Token-based ($15-100/month)
- **Gap**: Compression ≠ Enhancement

### 5. Perimattic
- **What**: AI model optimization services
- **Approach**: Quantization, pruning, distillation, serving optimization
- **Strength**: Full-stack service, enterprise clients
- **Weakness**: Consultative model, not self-serve
- **Pricing**: Custom enterprise
- **Gap**: Service-heavy, not productized

## Indirect Competitors (Inference Optimization)

### 6. OptiLLM
- **What**: Inference-time optimization proxy
- **Approach**: 20+ techniques (MCTS, best-of-N, self-consistency)
- **Strength**: No model changes, works with any API
- **Weakness**: Adds latency per request, doesn't change model
- **Pricing**: Open source (self-hosted)
- **Gap**: Prompt-level vs architecture-level optimization

### 7. ThinkBooster
- **What**: Test-time compute scaling framework
- **Approach**: 9 scaling strategies with PRMs
- **Strength**: Visual debugger, OpenAI-compatible endpoint
- **Weakness**: Requires additional compute per request
- **Pricing**: Open source
- **Gap**: Inference-time only, no model improvement

## Our Differentiation

| Feature | NeuroForge | hoof | Model Surgery | Dystrio | Condense | OptiLLM |
|---------|-----------|------|---------------|---------|----------|---------|
| Reasoning boost | YES | No | No | No | No | Partial |
| Zero training | YES | YES | YES | YES | No | YES |
| Automated detection | YES | No | No | Partial | No | No |
| Architecture change | YES | YES | YES | YES | No | No |
| Composable with others | YES | YES | YES | YES | YES | YES |
| Self-serve API | YES | No | No | No | YES | YES |
| Per-model pricing | YES | No | No | No | YES | No |

**Our unique position**: Only solution that automatically detects AND enhances reasoning circuits without training, offered as a self-serve service.
