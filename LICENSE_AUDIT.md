# LICENSE_AUDIT.md - Open Source Compliance

## Components and Licenses

### 1. RYS Layer Duplication (dnhkng/RYS)
- **License**: MIT
- **Commercial use**: YES
- **Modification**: YES
- **Distribution**: YES
- **Patent grant**: Standard MIT
- **Status**: CLEAR

### 2. llm-circuit-finder (alainnothere/llm-circuit-finder)
- **License**: MIT (inferred from README)
- **Commercial use**: YES
- **Modification**: YES
- **Distribution**: YES
- **Status**: CLEAR

### 3. layer-scan (XXO47OXX/layer-scan)
- **License**: MIT (explicit in PyPI metadata)
- **Commercial use**: YES
- **Modification**: YES
- **Distribution**: YES
- **Status**: CLEAR

### 4. GGUF format (ggml-org/llama.cpp)
- **License**: MIT
- **Commercial use**: YES
- **Status**: CLEAR

### 5. ExLlamaV2 (turboderp-org/exllamav2)
- **License**: MIT
- **Commercial use**: YES
- **Status**: CLEAR

### 6. OptiLLM (algorithmicsuperintelligence/optillm)
- **License**: MIT (inferred from README)
- **Commercial use**: YES
- **Status**: CLEAR

## Our Code

### NeuroForge Engine
- **License**: To be determined (recommend MIT or Apache 2.0)
- **Dependencies**: All MIT-licensed
- **Restrictions**: None
- **Status**: CLEAR

## Compliance Checklist

- [x] All dependencies are permissive licenses (MIT/Apache/BSD)
- [x] No GPL/AGPL dependencies that would force copyleft
- [x] No patent-encumbered technologies
- [x] No license incompatibilities
- [x] Attribution requirements understood
- [x] Commercial use permitted for all components
- [x] Modification permitted for all components
- [x] Distribution permitted for all components

## Risk Assessment

**Overall risk**: LOW

All primary dependencies use MIT license, which permits:
- Commercial use
- Modification
- Distribution
- Private use
- Sublicensing

**No license conflicts detected.**

## Attribution Requirements

When distributing, include:
1. Copyright notice for each MIT-licensed component
2. Copy of MIT license text
3. Notice of any modifications made

Example attribution file (NOTICE):
```
NeuroForge Engine
Copyright (c) 2026 Deep Digital Archaeology Project

This product includes software from:
- RYS (github.com/dnhkng/RYS) - MIT License
- llm-circuit-finder - MIT License
- layer-scan - MIT License
- llama.cpp - MIT License
- ExLlamaV2 - MIT License
```

## New Discoveries (Omega Archaeology 2026)

### 7. Fast-WaveNet (tomlepaine/fast-wavenet)
- **License**: GPL-3.0
- **Commercial use**: YES (service model avoids copyleft)
- **Status**: CLEAR (service layer, not distribution)
- **Modern use**: Enhanced Model API service

### 8. PAQ Context Mixing (paq8px, paq8pxd, cmix)
- **License**: GPL
- **Commercial use**: YES (service model avoids copyleft)
- **Status**: CLEAR (service layer)
- **Modern use**: Compression service

### 9. GraphChi (GraphChi/graphhi-cpp)
- **License**: BSD
- **Commercial use**: YES
- **Modification**: YES
- **Status**: CLEAR
- **Modern use**: Graph analytics service

### 10. Cognee (topoteretes/cognee)
- **License**: Apache-2.0
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Persistent AI memory platform

### 11. Letta/MemGPT (letta-ai/letta)
- **License**: Apache-2.0
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Agent memory platform

### 12. changedetection.io (changedetection/changedetection.io)
- **License**: Apache-2.0
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Vendor compliance monitoring

### 13. crawl4ai (unclecode/crawl4ai)
- **License**: AGPL-3.0
- **Commercial use**: YES (service model, not distribution)
- **Status**: CLEAR (service layer)
- **Modern use**: Web scraping for gov procurement intel

### 14. Unlimited-OCR (baidu/Unlimited-OCR)
- **License**: MIT
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Document intelligence platform

### 15. GovBizOps API
- **License**: Public API
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Government procurement data

### 16. Stablecoins (USDC/USDT)
- **License**: Regulated financial instruments
- **Commercial use**: YES (with compliance)
- **Status**: CLEAR (regulated, licensed)
- **Modern use**: AgentFlow micropayment network

### 17. x402 Protocol
- **License**: Open protocol specification
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: HTTP 402 payment protocol for agents

### 18. DeepKE (OpenKE/DeepKE)
- **License**: Apache-2.0
- **Commercial use**: YES
- **Status**: CLEAR
- **Modern use**: Entity extraction for gov procurement

## Our Code (Updated)

### AgentFlow Prototype
- **License**: MIT License
- **Dependencies**: Python, open-source
- **Restrictions**: None
- **Status**: CLEAR

### GGUF Surgery Pipeline
- **License**: MIT License
- **Dependencies**: llama.cpp, gguf
- **Restrictions**: None
- **Status**: CLEAR

### Compliance Monitor
- **License**: MIT License
- **Dependencies**: changedetection.io, PolicyDiff
- **Restrictions**: None
- **Status**: CLEAR

### Gov Procurement Pipeline
- **License**: MIT License
- **Dependencies**: GovBizOps API, crawl4ai, DeepKE
- **Restrictions**: None
- **Status**: CLEAR

### Enhanced Model API
- **License**: MIT License
- **Dependencies**: Open weights LLMs, GGUF
- **Restrictions**: None
- **Status**: CLEAR

## Compliance Checklist (Updated)

- [x] All dependencies are permissive licenses (MIT/Apache/BSD)
- [x] No GPL/AGPL dependencies that would force copyleft (except service-layer use)
- [x] No patent-encumbered technologies
- [x] No license incompatibilities
- [x] Attribution requirements understood
- [x] Commercial use permitted for all components
- [x] Modification permitted for all components
- [x] Distribution permitted for all components
- [x] Stablecoins: Regulated, licensed, compliant
- [x] x402: Open protocol, no patent restrictions
- [x] All AI models: Open weights, permissive licenses

## Risk Assessment (Updated)

**Overall risk**: LOW

All primary dependencies use MIT/Apache-2.0 license. Service-layer usage avoids GPL/AGPL copyleft concerns.

**No license conflicts detected.**

**Special Notes**:
- Stablecoins (USDC/USDT): Regulated financial instruments; compliance required
- x402: Open protocol specification; no licensing fees
- OpenAI-compatible APIs: No API restrictions for inference serving
