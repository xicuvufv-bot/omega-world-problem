# CAPABILITY_ATLAS.md

Every repository is treated as a *capability*, not a product. Capabilities are
what can fuse.

## Capabilities discovered

| # | capability | donor projects | strength |
|---|---|---|---|
| C01 | probabilistic equality/similarity sketches (MinHash, HLL, HNSW) | ekzhu/datasketch | strong |
| C02 | corpora-scale near-dup dedup with 16k perms | google-research/deduplicate-text-datasets | strong |
| C03 | platform-agnostic stream pipeline blocks (filters, dedup, mapping) | huggingface/datatrove | strong |
| C04 | build+audit pre-training data (exact matches, fuzzy) | allenai/dolma | strong |
| C05 | SIMD fuzzy string distance (QRatio, partial_ratio) | rapidfuzz/RapidFuzz | strong |
| C06 | content-defined chunking (FastCDC) | tigerwill90/fastcdc, jogfs/fastcdc-go, askeladdk/fastcdc | strong |
| C07 | perceptual hashing / fingerprint (audio) | acoustid/chromaprint | medium |
| C08 | fingerprint→inverted index search | acoustid/acoustid-index | medium |
| C09 | perceptual video hash (64-bit) | akamhy/videohash | medium |
| C10 | pHash image dedup with tree traversal | mk-fg/image-deduplication-tool | medium |
| C11 | probabilistic DS toolkit (Bloom, cuckoo, IBLT, HLL, CM, MinHash) | Callidon/bloom-filters | strong |
| C12 | sub-ms SIMD vector search | cwida/PDX | strong |
| C13 | ANN random-projection forests, mem-mapped | meilisearch/arroy | strong |
| C14 | SQL-over-git table queries | AmrDeveloper/GQL, filhodanuvem/gitql | medium |
| C15 | incremental Datalog / provenance queries | frankmcsherry/dynamic-datalog | medium |
| C16 | deterministic sim→telemetry replay | loicbelec/pitgun | medium |
| C17 | memory-safe zstd codec + dict training | paddor/zrip | medium |

## Capability fusion template

x) C06(content-defined chunking) gives *byte-locality* — the ability to ask
   "which part of this file is which part of that file", not just "are they
   similar".

x) C01/C02 gives *candidate recall at corpus scale* — narrowing a full-corpus
   search to a handful of plausible sources.

x) C05 gives *edit tolerance* — accepting near-dups that byte-exact methods
   reject.

→ **C06 + C01/C02 + C05 = a localized provenance query layer.**