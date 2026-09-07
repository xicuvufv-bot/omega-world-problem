# TOP_100_FUSIONS.md

Systematic combinatorial sweep of the capabilities from CAPABILITY_ATLAS.md,
expressed as fusion hypotheses. Not a popularity contest — a grid over the
17 capabilities. Indexes:

- **fus_058** (CDC × LSH × fuzzy = provenance engine) → the winner.
- 99 others ranked by novelty × problem-fit; many are re-combinations of
  obvious pairs and are explicitly REJECTED as "feature-summing".

Selected rows (full grid continues in the repo's tracking sheet):

| id | fusion | new capability? | problem fit | verdict |
|---|---|---|---|---|
| f001 | C02×C03 | corpus dedup service | real but exists | fold-in |
| f002 | C01×C05 | similar-doc + fuzzy | mildly new | exists-ish |
| f003 | C06×C01 | chunking + LSH | no single-project | YES → winner |
| f004 | C06×C05 | chunk + fuzzy verify | near-dup tolerance | part of winner |
| f005 | C03×C06 | pipeline with chunking | features sum | REJECT |
| f010 | C07×C08 | audio fingerprint index | niche | REJECT (early) |
| f013 | C09×C13 | video near-dup ANN | plausible | watchlist |
| f016 | C11×C03 | probabilistic pipeline primitives | feature sum | REJECT |
| f020 | C01×C14 | git as knowledge-graph queries | research-y | watchlist |
| f030 | C17×C06 | zstd-dict + chunking | storage overlap | REJECT |
| f050 | C15×C03 | declarative-dataflow pipeline | heavy | REJECT |
| f058 | C06×C01×C05 | **byte provenance engine** | **strong** | **WIN** |
| f075 | C12×C13 | huge vec search | exists (Faiss etc.) | REJECT |
| f090 | C10×C01 | image dedup as-a-service | niche viability | watchlist |
| f100 | C04×C03×C01×C06×C05 | full corpus govern layer | strongest form | expansion |