# GITHUB_ATLAS.md

Curated inventory of repositories surveilled during this project. Verified via
GitHub REST API (stars, license, activity as of 2026-09-07).

## Core fusion members

| repo | lang | stars | license | activity | capability |
|---|---|---|---|---|---|
| ekzhu/datasketch | Python | 2962 | MIT | active 2026-08 | MinHash, LSH, LSH Forest, HyperLogLog, HNSW-style probabilistic sketches |
| allenai/dolma | Python | 1541 | Apache-2.0 | active 2026-08 | build + inspect OLMo pre-training corpora |
| google-research/deduplicate-text-datasets | Rust | 1270 | Apache-2.0 | 2024-07 | exact + MinHashLSH corpora dedup (16384-perm precision) |
| huggingface/datatrove | Python | 3326 | Apache-2.0 | active 2026-08 | platform-agnostic processing pipeline blocks |
| rapidfuzz/RapidFuzz | C++/Python | 4113 | MIT | active 2026-08 | SIMD fuzzy string matching, QRatio/partial_ratio |
| tigerwill90/fastcdc | Go | 31 | MIT | active 2026-08 | FastCDC content-defined chunking |

## Surveyed adjacent / candidate repositories

| repo | capability | viable? |
|---|---|---|
| acoustid/chromaprint | audio fingerprinting (C++) | adjacent |
| acoustid/acoustid-index | fingerprint→inverted index search (Zig) | adjacent |
| meilisearch/arroy | ANN random-projection forest (Rust, LMDB) | adjacent |
| cwida/PDX | sub-ms SIMD vector search (C++/MIT) | adjacent |
| akamhy/videohash | 64-bit perceptual video hash (MIT) | adjacent |
| mk-fg/image-deduplication-tool | pHash dedup (WTFPL) | adjacent |
| Callidon/bloom-filters | Bloom/cuckoo/IBLT/HLL/MinHash/Count-Min (MIT) | adjacent |
| AmrDeveloper/GQL | SQL-over-git as tables (MIT) | distant domain |
| filhodanuvem/gitql | git query language (MIT) | distant domain |
| frankmcsherry/dynamic-datalog | Datalog + dynamic queries (Rust) | distant domain |
| loicbelec/pitgun | deterministic sim→telemetry (MIT) | distant domain |
| paddor/zrip | memory-safe zstd codec (MIT) | distant domain |
| jogfs/fastcdc-go | FastCDC (Apache-2.0) | duplicate of core |
| Zabuzard/FastCDC4J | FastCDC (GPL-3.0) | license-incompatible |
| askeladdk/fastcdc | FastCDC (ISC) | duplicate of core |
| kalbasit/fastcdc | FastCDC (MIT) | duplicate of core |

## How it was done

- 160+ candidate queries via GitHub search API across distant domains
  (databases × vision × audio × compression × VCS × sim).
- Direct GETs on ~20 repos to verify metadata: stars/license/last-push.
- Shortlist funneled through capability lens, not star count.