# GITHUB ATOMIC DATABASE

## Capability Domain: AI Agent Frameworks

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| open-gitagent/gitagent | 670 | Agent-as-repo: identity, memory, tools, skills in git | Natural language, files | Agent actions, code | TypeScript | MIT | Alpha | CLI/SDK |
| kritird/Cortex-Agent-Framework | 1 | YAML-driven agent, fan-out/fan-in, MCP-native, multi-agent mesh | Config YAML, tasks | Results, deployments | Python | MIT | Pre-alpha | CLI/API |
| LumoraX/taifeng | 5 | Microkernel agent: skills=markdown, cache-aware compaction, HITL | Skills MD, tasks | Results | Python | Apache-2.0 | Pre-alpha (622 tests) | Python lib |
| open-strix/open-strix | 84 | Long-running agent, self-scheduled, git memory, pollers | Discord/UI messages | Scheduled work, insights | Python | MIT | Beta | Discord/Web UI |
| Omnis Agents/OmniAgent | 2557 | Full self-evolution (skill+context+brainmodel), Hyper-Harness, security | Tasks | Evolved agent | Python | Other | Beta | API/CLI |
| letta-ai/letta (MemGPT) | 24631 | Stateful agents with advanced reasoning, transparent long-term memory | Tasks, context | Decisions, actions | Python | Apache-2.0 | Stable | Python lib/API |
| openinterpreter/openinterpreter | 68249 | Natural language interface for local code execution, full file system access | Commands, code | Execution results | Python | Apache-2.0 | Stable | CLI/Python |

## Capability Domain: Browser Automation & Computer Use

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| agent-browser (calebdane7) | 12 | Raw CDP, real Chrome, 93% less context, 200-400 tokens/page | URLs, actions | Snapshots, DOM | JavaScript | Apache-2.0 | Stable | CLI |
| bladebro | 79 | 5 tools only, stealth 6-layer, diff-first, self-healing | URLs | Delta content | Rust | Apache-2.0 | Stable | MCP/CLI |
| ghostchrome | 3 | Go binary, CDP-native, 19MB, daemon | URLs | Snapshots, content | Go | MIT | Stable | CLI/MCP/SDK |
| Crawl4AI (unclecode) | 50k+ | LLM-ready markdown, async browser pool, adaptive intelligence | URLs, JS | Clean markdown, structured data | Python | AGPL-3.0 | Production | CLI/API/Docker |
| Lightpanda browser | 0 | From-scratch headless browser, Zig, 16x less memory, 9x faster | URLs | HTML/JS content | Zig | AGPL-3.0 | Beta | CDP |
| Chromex | 0 | CDP CLI, 85 MCP tools, zero deps, per-tab daemons | URLs | Snapshots, DevTools | Node.js | MIT | Stable | CLI/MCP |
| browser-use/browser-use | High | Browser automation, cloud + open source | URLs | Page state | Python | MIT | High | Python/MCP |
| microsoft/Webwright | 6k | Minimal browser agent, code-as-action SOTA | URLs | Actions | Python | MIT | High | Python |

## Capability Domain: Document Parsing & Understanding

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| opendatalab/MinerU | 10k+ | PDF/DOCX/PPTX/XLSX to MD/JSON, VLM+OCR, 109 languages | Documents | Markdown, JSON | Python | Apache-2.0 custom | Production | CLI/API |
| baidu/Unlimited-OCR | 24k+ | One-shot long-horizon OCR, 32K context | Images, PDFs | Structured text | Python | MIT | Production | vLLM/SGLang |
| numindai/nuextract | 202 | 4B VLM, structured extraction, doc-to-markdown | Documents | JSON, Markdown | Python | MIT | Production | vLLM |
| IBM/docling | 1k+ | Multi-format parsing, advanced PDF understanding | Documents | Markdown, HTML, JSON | Python | MIT | Production | LangChain/LlamaIndex |
| abhichat85/papyrus | 0 | Universal document ingestion, no LLM in conversion path, MCP server | Any file | Markdown, chunks | Python | Apache-2.0 | Alpha | CLI/API/MCP |

## Capability Domain: Knowledge Management & Memory

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| topoteretes/cognee | 30518 | Persistent long-term memory for AI agents, self-hosted KG engine | Any format | Knowledge graph, recall | Python | Apache-2.0 | Stable | Python/MCP |
| letta-ai/letta | 24631 | Stateful agents, advanced reasoning, transparent long-term memory | Tasks, context | Decisions, actions | Python | Apache-2.0 | Stable | Python/API |
| FalkorDB/itext2kg | 1k+ | Incremental KG from text, zero-shot, entity resolution | Documents | KG (Neo4j) | Python | MIT | Production | Python lib |
| sift-kg | 788 | Documents → KG, entity resolution, 75+ formats, interactive viewer | Documents | KG (JSON/GraphML) | Python | MIT | Production | CLI |
| myKG | 0 | Schema-guided KG, RDFS/OWL ontology, MCP server, Obsidian vault | Documents | KG (JSONL/TTL) | Python | N/A | Alpha | CLI/MCP |
| kg-gen (NeurIPS) | 0 | KG from any text, NeurIPS paper, DSPy, LiteLLM | Text | KG | Python | MIT | Research | Python lib |
| Khora | 98 | Knowledge repositories, entity+vector+graph, multi-signal retrieval | Documents | Queryable KB | Python | Apache-2.0 | Beta | Python lib |

## Capability Domain: Workflow Orchestration & Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| dagucloud/dagu | 3721 | Single-binary DAG engine, YAML, distributed workers, MCP | Scripts, commands | Execution results | Go | GPL-3.0 | Production | CLI/Web UI/gRPC |
| n8n-io/n8n | 201K | Visual workflow, 1500+ integrations, AI-native | Flows, code | Results | TypeScript | Sustainable Use | Very High | Web UI/API |
| RunLoop | 0 | Visual DAG, 4 queue backends, AI/LLM nodes, AES-256 vault | Flows, code | Results | Go+Next.js | AGPL-3.0 | Beta | API/Web UI |
| bj-qizhi/trigix | 1 | Rust engine, 140+ node types, RAG, agents, MCP | Workflows | Results | Rust+Python | MIT | Alpha | Web UI/API |
| Flow_Forge | 0 | TypeScript DAG, Bull queues, LangChain AI nodes | Workflows | Results | TypeScript | Apache-2.0 | Alpha | API/Web UI |
| Maia | 1 | Self-hosted DAG, SQLite persistence, SSE observability | Workflows | Results | TypeScript | MIT | Beta | Web UI |

## Capability Domain: Semantic Search & Vector DB

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| kektordb | 83 | Vector+BM25+graph hybrid, MCP server, ONNX embedder, temporal KG | Queries | Results | Go | Other | Beta | REST/MCP/SDK |
| localdb | 0 | Single binary, hybrid BM25+vector, MCP server, no daemon needed | Files | Search results | Rust | AGPL-3.0 | Pre-release | CLI/MCP |
| fidx | 3 | Local AI search, hybrid BM25+vector, 18-49ms queries | Files | Search results | Python | Other | Alpha | CLI |
| symaira-seek | 3 | CGO-free Go, hybrid search, Ollama integration | Files | Search results | Go | Apache-2.0 | Stable | CLI/MCP/HTTP |
| Vantadb | 2 | Embedded Rust+Python, HNSW+BM25+RRF, WAL recovery | Data | Search results | Rust | Apache-2.0 | Alpha | Python SDK |

## Capability Domain: Security & Code Analysis

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| opengrep/opengrep | 2661 | SAST engine, 30+ languages, taint analysis, Semgrep rules | Code | Vulnerabilities | OCaml | LGPL-2.1 | Production | CLI |
| medusa | 5k+ | 40k+ patterns, AI security, supply chain, Claude Code vetting | Code | SARIF/JSON | Python | MIT | Production | CLI |
| depsec | 2 | Supply chain scanner, AST-aware, LLM triage, sandbox protection | Projects | Findings | Rust | N/A | Beta | CLI |
| code-pathfinder | 0 | Cross-file taint analysis, call graphs, MCP server | Code | SARIF | Go | Apache-2.0 | Beta | CLI/MCP |
| MoSec | 2 | LLM-augmented SAST, PoC generation, CVSS scoring | Code | SARIF/Report | Python | AGPL-3.0 | Alpha | CLI |

## Capability Domain: Voice AI & Multi-Modal

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| microsoft/VibeVoice | 53K | Frontier TTS + ASR, 90-min long-form | Audio/Text | Speech/Text | Python | MIT | High | Python/MCP |
| k2-fsa/OmniVoice | 9.6K | 600+ language TTS, voice cloning | Text | Speech | Python | Apache-2.0 | High | CLI/Python |
| dograh-hq/dograh | 5.2K | Voice agent platform, self-hosted Vapi alternative | Audio | Voice agent | TypeScript | BSD-2 | High | Web API |
| fluxions-ai/vui | 754 | Real-time voice assistant, WebRTC, barge-in | Audio | Voice response | Python | Apache-2.0 | Medium | WebRTC/CLI |
| OpenMOSS/MOSS-TTS | 4K | Long-form TTS, dialogue, voice design | Text | Speech | Python | Apache-2.0 | High | Python |

## Capability Domain: Screen Observation & Desktop Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| Screenpipe | 40K+ | Screen capture + OCR, always-on, local processing | Screen | Text, UI elements | Rust | Source-available | Production | CLI/Python |
| GenericAgent | 14114 | Self-evolving agent, 3K lines, skill tree | Tasks | Evolved agent | Python | MIT | Production | Python/MCP |
| Understudy | 451 | Teach by demonstration, multi-channel | Demo videos | Workflows | Python | MIT | Beta | Python |
| ScreenMind | New | Screen memory, Gemma 4, agent platform | Screen | Memory | Python | MIT | Alpha | Python |
| AgentHandover | New | Learns workflows from observation | Observation | Workflows | Python | MIT | Alpha | Python |

## Capability Domain: App Integration & Data Transfer

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| ComposioHQ/composio | 30019 | 1000+ pre-authenticated toolkits, OAuth flows, per-user sessions | API calls | Authenticated actions | Python | MIT | Stable | Python/MCP |
| CrossPaste | 2211 | Universal pasteboard across devices | Clipboard | Synced clipboard | Rust | AGPL-3.0 | Stable | Desktop app |
| Quark | New | AI-native clipboard, MCP, cross-platform | Clipboard | AI-enhanced clipboard | Python | MIT | Alpha | MCP |
| CtxPort | New | Export AI conversations as structured markdown | Conversations | Structured markdown | Python | MIT | Alpha | CLI |

## Capability Domain: LLM Observability & Debugging

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| langfuse/langfuse | 25000+ | LLM observability: tracing, evaluation, prompt management, metrics | LLM calls | Traces, metrics | TypeScript | MIT | Production | Web UI/API |
| Phoenix (Arize) | 5000+ | LLM observability, tracing, eval, RAG analysis | LLM calls | Traces, analysis | Python | Apache-2.0 | Production | Python/Web |
| LangSmith | N/A | LLM debugging, evaluation, monitoring (proprietary) | LLM calls | Traces | Cloud | Commercial | Production | API/Web |

## Capability Domain: Local/Edge AI & Inference

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| mudler/LocalAI | 49K | Universal local AI engine, any model/hardware, OpenAI-compatible | Prompts | Responses | Go | MIT | Very High | API/Docker |
| ollama/ollama | 100K+ | Local LLM runner, model management, simple API | Prompts | Responses | Go | MIT | High | CLI/API |
| open-webui/open-webui | 151110 | ChatGPT-like interface, RAG, voice, web search, image gen | Conversations | Responses | TypeScript | Open WebUI License | High | Docker/Web |

## Capability Domain: Multi-Modal Knowledge Extraction

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| Graphify-Labs/graphify | 3700+ | Turn codebase/docs/papers/images/videos into queryable KG | Any content | Knowledge graph | Python | MIT | Stable | Python/CLI |
| langchain-ai/langchain | 95K+ | Framework for LLM apps, chains, agents, retrieval | LLM calls | Applications | Python | MIT | Production | Python/JS |
| run-llama/llama_index | 35K+ | Data framework for LLM, RAG, agents | Documents | Indices | Python | MIT | Production | Python |

## Capability Domain: Local LLM Inference

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| mudler/LocalAI | 49K | Universal local AI engine, any model/hardware | Prompts | Responses | Go | MIT | Very High | API/Docker |
| ollama/ollama | 100K+ | Local LLM runner, model management | Prompts | Responses | Go | MIT | High | CLI/API |
| vllm-project/vllm | 40K+ | High-throughput LLM serving, PagedAttention | Prompts | Responses | Python | Apache-2.0 | Production | API |

## Capability Domain: Workflow Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| n8n-io/n8n | 201K | Visual workflow, 1500+ integrations, AI-native | Flows, code | Results | TypeScript | Sustainable Use | Very High | Web UI/API |
| dagucloud/dagu | 3721 | Single-binary DAG engine, YAML, distributed workers, MCP | Scripts, commands | Execution results | Go | GPL-3.0 | Production | CLI/Web UI/gRPC |
| activepieces/activepieces | 15K+ | No-code workflow automation, OpenAI, webhook, email triggers | Flows, code | Results | TypeScript | MIT | Stable | Web UI/API |

## Capability Domain: Local/Edge AI

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| mudler/LocalAI | 49K | Universal local AI engine, any model/hardware | Prompts | Responses | Go | MIT | Very High | API/Docker |
| ollama/ollama | 100K+ | Local LLM runner, model management | Prompts | Responses | Go | MIT | High | CLI/API |
| pytorch/executorch | High | On-device AI, 12+ hardware backends | Models | Deployed models | C++/Python | BSD | High | Mobile/Edge |

## Capability Domain: Computer Use & Desktop Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| OpenInterpreter/open-interpreter | 68249 | Natural language interface for local code execution | Commands | Execution results | Python | Apache-2.0 | Stable | CLI/Python |
| GenericAgent | 14114 | Self-evolving agent, 3K lines, skill tree | Tasks | Evolved agent | Python | MIT | Production | Python/MCP |
| Screenpipe | 40K+ | Screen capture + OCR, always-on, local processing | Screen | Text, UI elements | Rust | Source-available | Production | CLI/Python |

## Capability Domain: Stateful Agent Memory

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| letta-ai/letta | 24631 | Stateful agents, advanced reasoning, transparent long-term memory | Tasks, context | Decisions, actions | Python | Apache-2.0 | Stable | Python/API |
| topoteretes/cognee | 30518 | Persistent long-term memory for AI agents, self-hosted KG engine | Any format | Knowledge graph, recall | Python | Apache-2.0 | Stable | Python/MCP |
| mem0ai/mem0 | 20K+ | Memory layer for AI agents, add/delete/search memories | Conversations | Memories | Python | Apache-2.0 | Stable | Python/API |

## Capability Domain: Code Understanding & Analysis

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| opengrep/opengrep | 2661 | SAST engine, 30+ languages, taint analysis, Semgrep rules | Code | Vulnerabilities | OCaml | LGPL-2.1 | Production | CLI |
| code-pathfinder | 0 | Cross-file taint analysis, call graphs, MCP server | Code | SARIF | Go | Apache-2.0 | Beta | CLI/MCP |
| greptile-apps/greptile | 30K+ | Codebase indexing, semantic search, code understanding | Code repos | Search results | Python | MIT | Production | API |

## Capability Domain: Enterprise Integration & Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| ComposioHQ/composio | 30019 | 1000+ pre-authenticated toolkits, OAuth flows, per-user sessions | API calls | Authenticated actions | Python | MIT | Stable | Python/MCP |
| langchain-ai/langchain | 95K+ | Framework for LLM apps, chains, agents, retrieval | LLM calls | Applications | Python | MIT | Production | Python/JS |
| crewAIInc/crewAI | 58K | Multi-agent orchestration, Crews + Flows | Tasks | Results | Python | MIT | High | Python/API |

## Capability Domain: Real-time Voice & Communication

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| microsoft/VibeVoice | 53K | Frontier TTS + ASR, 90-min long-form | Audio/Text | Speech/Text | Python | MIT | High | Python/MCP |
| fluxions-ai/vui | 754 | Real-time voice assistant, WebRTC, barge-in | Audio | Voice response | Python | Apache-2.0 | Medium | WebRTC/CLI |
| dograh-hq/dograh | 5.2K | Voice agent platform, self-hosted Vapi alternative | Audio | Voice agent | TypeScript | BSD-2 | High | Web API |

## Capability Domain: Web Scraping & Crawling

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| Crawl4AI (unclecode) | 50k+ | LLM-ready markdown, async browser pool, caching | URLs | Markdown | Python | AGPL-3.0 | Production | CLI/API/Docker |
| firecrawl/firecrawl | 91K+ | Turn websites into LLM-ready data, JS rendering, anti-bot | URLs | Structured data | TypeScript | AGPL-3.0 | Production | API/Docker |
| ScrapeGoat | 1 | Scrapy architecture+Go, MCP, LLM extraction, anti-bot | URLs | Structured data | Go | Apache-2.0 | Beta | CLI/MCP/REST |
| Crawlingo | 6 | Rust core, self-healing selectors, stealth TLS, 3500 req/s | URLs | JSON/CSV/Parquet | Rust | MIT | Beta | SDK (Py/Node/Go) |
| kumo | 3 | Rust async crawler, derive(Extract), LLM extraction | URLs | Structured data | Rust | MIT | Alpha | Rust lib |
| ultra-scraper | 3 | Agent-native, auto-escalation, stealth tiers, 4 tiers | URLs | Structured data | Python | MIT | Alpha | Python lib/MCP |

## Capability Domain: MCP Integration

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| github/github-mcp-server | 32688 | Full GitHub integration, repos/issues/PR/actions | Queries | GitHub data | TypeScript | MIT | Production | MCP |
| modelcontextprotocol/servers | 15k+ | Reference MCP servers (FS, Git, Memory, etc.) | MCP calls | Results | TypeScript/Python | Apache-2.0/MIT | Reference | MCP |
| agent-mcp | 0 | Meta-MCP facade, aggregates servers, agent loops | MCP calls | Results | Python | MIT | Alpha | MCP |
| Corn Hub | 0 | 18 MCP tools, semantic memory, AST engine, quality gates | Code queries | Results | TypeScript | MIT | Alpha | MCP |
| FlowMCP/mcp-agent-server | 0 | Agent-powered MCP tools, A2A protocol, OpenRouter | MCP calls | Results | TypeScript | MIT | Alpha | MCP |

## Capability Domain: Structured Output / LLM Extraction

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| nfield | 4 | Wide schema extraction (thousands of fields), grounding, provenance | Documents+schema | JSON | Python | Other | Beta | CLI/Python |
| llm-structured-extract | 10 | Pydantic schemas, retry/repair, batch pipelines, cost tracking | LLM output | Typed data | Python | MIT | Beta | CLI/Python |
| confident-extract | 1 | Deterministic repair, zero LLM calls, confidence scoring | Raw text | Typed data | Python | MIT | Alpha | Python |
| structllm | 4 | Universal structured output via LiteLLM, any provider | LLM output | Typed data | Python | MIT | Stable | Python |
| PromptGuard | 0 | Auto-repair loop, prompt versioning, regression testing | LLM output | Typed data | Python | MIT | Beta | Python |

## NEW: Capability Domain: Agent Observability & Debugging

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| langfuse/langfuse | 25000+ | LLM observability: tracing, evaluation, prompt management, metrics | LLM calls | Traces, metrics | TypeScript | MIT | Production | Web UI/API |
| Arize-ai/phoenix | 5000+ | LLM observability, tracing, eval, RAG analysis | LLM calls | Traces, analysis | Python | Apache-2.0 | Production | Python/Web |
| langchain-ai/langsmith | N/A | LLM debugging, evaluation, monitoring (proprietary) | LLM calls | Traces | Cloud | Commercial | Production | API/Web |

## NEW: Capability Domain: Local LLM Inference

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| mudler/LocalAI | 49K | Universal local AI engine, any model/hardware | Prompts | Responses | Go | MIT | Very High | API/Docker |
| ollama/ollama | 100K+ | Local LLM runner, model management | Prompts | Responses | Go | MIT | High | CLI/API |
| vllm-project/vllm | 40K+ | High-throughput LLM serving, PagedAttention | Prompts | Responses | Python | Apache-2.0 | Production | API |

## NEW: Capability Domain: Enterprise Integration & Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| n8n-io/n8n | 201K | Visual workflow, 1500+ integrations, AI-native | Flows, code | Results | TypeScript | Sustainable Use | Very High | Web UI/API |
| activepieces/activepieces | 15K+ | No-code workflow automation, OpenAI, webhook, email triggers | Flows, code | Results | TypeScript | MIT | Stable | Web UI/API |
| ComposioHQ/composio | 30019 | 1000+ pre-authenticated toolkits, OAuth flows, per-user sessions | API calls | Authenticated actions | Python | MIT | Stable | Python/MCP |

## NEW: Capability Domain: Knowledge Graphs & Memory

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| topoteretes/cognee | 30518 | Persistent long-term memory for AI agents, self-hosted KG engine | Any format | Knowledge graph, recall | Python | Apache-2.0 | Stable | Python/MCP |
| letta-ai/letta | 24631 | Stateful agents, advanced reasoning, transparent long-term memory | Tasks, context | Decisions, actions | Python | Apache-2.0 | Stable | Python/API |
| mem0ai/mem0 | 20K+ | Memory layer for AI agents, add/delete/search memories | Conversations | Memories | Python | Apache-2.0 | Stable | Python/API |

## NEW: Capability Domain: Code Understanding & Analysis

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| greptile-apps/greptile | 30K+ | Codebase indexing, semantic search, code understanding | Code repos | Search results | Python | MIT | Production | API |
| code-pathfinder | 0 | Cross-file taint analysis, call graphs, MCP server | Code | SARIF | Go | Apache-2.0 | Beta | CLI/MCP |
| opengrep/opengrep | 2661 | SAST engine, 30+ languages, taint analysis, Semgrep rules | Code | Vulnerabilities | OCaml | LGPL-2.1 | Production | CLI |

## NEW: Capability Domain: Browser Automation

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| browser-use/browser-use | High | Browser automation, cloud + open source | URLs | Page state | Python | MIT | High | Python/MCP |
| microsoft/Webwright | 6k | Minimal browser agent, code-as-action SOTA | URLs | Actions | Python | MIT | High | Python |
| agent-browser (calebdane7) | 12 | Raw CDP, real Chrome, 93% less context, 200-400 tokens/page | URLs, actions | Snapshots, DOM | JavaScript | Apache-2.0 | Stable | CLI |
| bladebro | 79 | 5 tools only, stealth 6-layer, diff-first, self-healing | URLs | Delta content | Rust | Apache-2.0 | Stable | MCP/CLI |
| ghostchrome | 3 | Go binary, CDP-native, 19MB, daemon | URLs | Snapshots, content | Go | MIT | Stable | CLI/MCP/SDK |

## NEW: Capability Domain: Multi-Modal Knowledge Extraction

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| Graphify-Labs/graphify | 3700+ | Turn codebase/docs/papers/images/videos into queryable KG | Any content | Knowledge graph | Python | MIT | Stable | Python/CLI |
| langchain-ai/langchain | 95K+ | Framework for LLM apps, chains, agents, retrieval | LLM calls | Applications | Python | MIT | Production | Python/JS |
| run-llama/llama_index | 35K+ | Data framework for LLM, RAG, agents | Documents | Indices | Python | MIT | Production | Python |

## NEW: Capability Domain: Enterprise Integration

| Project | Stars | Capabilities | Inputs | Outputs | Tech | License | Maturity | Integration |
|---------|-------|-------------|--------|---------|------|---------|----------|-------------|
| ComposioHQ/composio | 30019 | 1000+ pre-authenticated toolkits, OAuth flows, per-user sessions | API calls | Authenticated actions | Python | MIT | Stable | Python/MCP |
| n8n-io/n8n | 201K | Visual workflow, 1500+ integrations, AI-native | Flows, code | Results | TypeScript | Sustainable Use | Very High | Web UI/API |
| activepieces/activepieces | 15K+ | No-code workflow automation, OpenAI, webhook, email triggers | Flows, code | Results | TypeScript | MIT | Stable | Web UI/API |

## Summary: New High-Value Projects

| Project | Stars | Unique Capability | License | Fusion Value |
|---------|-------|-------------------|---------|--------------|
| **Cognee** | 30,518 | Persistent agent memory + self-hosted KG | Apache-2.0 | CRITICAL: Fills agent memory gap |
| **Langfuse** | 25,000+ | LLM observability, tracing, evaluation | MIT | HIGH: Adds debugging/auditability |
| **Open Interpreter** | 68,249 | Natural language → local code execution | Apache-2.0 | HIGH: Desktop automation |
| **Composio** | 30,019 | 1000+ pre-authenticated integrations | MIT | HIGH: Solves integration hell |
| **Letta (MemGPT)** | 24,631 | Stateful agent memory, long-term reasoning | Apache-2.0 | HIGH: Agent persistence |
| **Open WebUI** | 151,110 | ChatGPT-like UI with RAG, voice, web search | Open WebUI License | HIGH: Zero-config UI layer |
| **Firecrawl** | 91,000+ | Turn websites into LLM-ready data | AGPL-3.0 | MEDIUM: Enhanced web extraction |
| **Graphify** | 3,700+ | Multi-modal KG builder (code, docs, images, video) | MIT | HIGH: Multi-modal knowledge |
| **Mem0** | 20K+ | Memory layer for AI agents | Apache-2.0 | HIGH: Agent memory |
| **Langfuse** | 25,000+ | LLM observability platform | MIT | HIGH: Adds observability layer |