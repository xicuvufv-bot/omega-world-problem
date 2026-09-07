# OLD_TECHNOLOGY_DATABASE.md

## Catalog of Discovered Old/Abandoned Technologies

### TIER 1: HIGHEST LEVERAGE (Algorithmic Breakthroughs)

#### 1. Fast-WaveNet Generation Algorithm
- **Repository**: tomlepaine/fast-wavenet (1772 stars, archived 2017)
- **Year**: 2016
- **Language**: Python/TensorFlow
- **License**: GPL-3.0
- **Core Innovation**: Reduces autoregressive generation from O(2^L) to O(L)
- **Algorithm**: Convolution queue caching - stores recurrent states instead of recomputing
- **Impact**: Still cited in 2026 papers (MusicDiffusionNet, Intel FPGA implementation)
- **Forgotten Because**: WaveNet was superseded by Parallel WaveNet, WaveRNN, etc.
- **Modern Relevance**: The algorithm applies to ANY causal dilated convolutional network, not just WaveNet
- **Reusable Components**: `generation_model` (RNN-like step), `convolution_queue` (circular buffers)

#### 2. PAQ Context Mixing Compression
- **Repository**: Multiple forks (paq8px, paq8pxd, cmix, etc.)
- **Year**: 2002-present (community maintained)
- **Language**: C++
- **License**: GPL
- **Core Innovation**: Ensemble of 50+ models predicting each bit, neural network mixer
- **Impact**: Best compression ratios ever achieved on standard benchmarks
- **Forgotten Because**: Too slow for general use (MB/s, not GB/s)
- **Modern Relevance**: LLM context compression market ($10+/M tokens), archival storage
- **Reusable Components**: Context model architecture, mixer design, SSE post-processing

#### 3. GraphChi Disk-Based Graph Processing
- **Repository**: GraphChi/graphchi-cpp (500+ stars, archived)
- **Year**: 2012
- **Language**: C++
- **License**: BSD
- **Core Innovation**: Parallel Sliding Windows algorithm for out-of-core graph processing
- **Impact**: Process 6.7B edges on a single Mac Mini (8GB RAM, SSD)
- **Forgotten Because**: Distributed systems (Spark, GraphX) became dominant
- **Modern Relevance**: NVMe SSDs (7 GB/s) make single-machine graph processing competitive with clusters
- **Reusable Components**: Edge blocking strategy, vertex-centric async execution model

### TIER 2: HIGH LEVERAGE (Production-Tested Systems)

#### 4. Hank Distributed Key-Value Store
- **Repository**: LiveRamp/hank (deprecated)
- **Year**: 2010
- **Language**: Java
- **License**: Apache 2.0
- **Core Innovation**: <2 disk seeks per read at 1000:1 data-to-RAM ratio
- **Impact**: Used in production at LiveRamp with >99.9% availability
- **Forgotten Because**: LiveRamp moved to different architecture
- **Modern Relevance**: Edge computing, IoT data stores, cold storage analytics
- **Reusable Concepts**: Rendezvous hashing, proactive indexing, sequential batch writes

#### 5. MegaKV GPU-Accelerated KV Store
- **Repository**: pzrq/megakv (28 stars, archived)
- **Year**: 2015
- **Language**: C++/CUDA
- **License**: Custom
- **Core Innovation**: Offloads index operations to GPU for in-memory caching
- **Impact**: Demonstrated GPU-accelerated KV store on AWS p2.xlarge
- **Forgotten Because**: Niche use case, GPU programming was harder then
- **Modern Relevance**: GPU computing is mainstream (CUDA, ROCm), edge GPU available
- **Reusable Components**: GPU index management, hash table on GPU

#### 6. BoltDB Embedded Key-Value Store
- **Repository**: boltdb/bolt (13K+ stars, complete/stable)
- **Year**: 2013
- **Language**: Go
- **License**: MIT
- **Core Innovation**: Pure Go B+tree with ACID transactions, lock-free MVCC
- **Impact**: Used by Shopify, Heroku in production, up to 1TB databases
- **Forgotten Because**: Creator declared it "complete" and stopped maintenance
- **Modern Relevance**: Foundation for bbolt (CoreOS), still used in etcd
- **Reusable Components**: B+tree implementation, MVCC protocol, single-file format

#### 7. GecoNet Game Transport Protocol
- **Repository**: Kiddinglife/geconet (63 stars)
- **Year**: 2016
- **Language**: C
- **License**: GPL-3.0
- **Core Innovation**: Complete SCTP-like transport for games with multihoming, encryption
- **Impact**: RFC-4960 based with game-specific optimizations
- **Forgotten Because**: Game networking moved to proprietary solutions
- **Modern Relevance**: WebRTC limitations for gaming, real-time communication needs
- **Reusable Components**: Message-oriented transport, LZF compression, congestion control

### TIER 3: MEDIUM LEVERAGE (Specialized Capabilities)

#### 8. DFC High-Performance String Matching
- **Repository**: nfsp3k/dfc (30 stars)
- **Year**: 2016
- **Language**: C
- **License**: Unknown
- **Core Innovation**: Network-speed string pattern matching (NSDI 2016 paper)
- **Impact**: Academic paper with real implementation
- **Forgotten Because**: Research project, no commercial push
- **Modern Relevance**: Network security, DPI, content filtering at line rate
- **Reusable Components**: SIMD-optimized matching engine

#### 9. Aang Rule-Based NLU System
- **Repository**: DannyNemer/aang (deprecated 2017)
- **Year**: 2017
- **Language**: JavaScript/Node.js
- **License**: Not specified
- **Core Innovation**: A* graph search through parse forests, ~20ms full NLU
- **Impact**: Complete NLU with semantic trees, anaphora resolution
- **Forgotten Because**: Developer believed deep learning would obsolete it
- **Modern Relevance**: Deterministic, auditable NLU for compliance-critical applications
- **Reusable Components**: A* parse forest search, semantic reduction, text conjugation

#### 10. Sosistab Obfuscated Transport
- **Repository**: geph-official/sosistab (43 stars, archived)
- **Year**: 2021
- **Language**: Rust
- **License**: Not specified
- **Core Innovation**: Obfs4-like obfuscation + Reed-Solomon FEC + dynamic batching
- **Impact**: Used by Geph VPN for anti-censorship
- **Forgotten Because**: Replaced by sosistab2 (multi-transport)
- **Modern Relevance**: Growing demand for censorship-resistant communication
- **Reusable Components**: FEC implementation, obfuscation layer, adaptive batching

#### 11. dsp.js Digital Signal Processing
- **Repository**: corbanbrook/dsp.js (1769 stars, abandoned)
- **Year**: 2010
- **Language**: JavaScript
- **License**: MIT
- **Core Innovation**: Complete DSP library: oscillators, FFT, filters, envelopes, reverb
- **Impact**: Pioneer of browser-based audio processing
- **Forgotten Because**: Web Audio API became standard, author lost interest
- **Modern Relevance**: WASM compilation, server-side audio processing, IoT audio
- **Reusable Components**: FFT implementation, IIR filters, ADSR envelopes

#### 12. Pequod Distributed Cache with Materialized Views
- **Repository**: bryankate/pequod (low stars)
- **Year**: 2014
- **Language**: C++
- **License**: Not specified
- **Core Innovation**: Cache joins - automatically materializing views across distributed cache
- **Impact**: Published at NSDI 2014
- **Forgotten Because**: Research prototype, no production adoption
- **Modern Relevance**: Real-time analytics, CDN edge caching, streaming joins
- **Reusable Components**: Cache join algorithm, distributed materialized view maintenance
