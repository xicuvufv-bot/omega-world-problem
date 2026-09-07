# FUSION_GRAPH.md

The funnel that survived: components → capabilities → fusions → systems →
prototype.

## A + B + C → NEW CAPABILITY (this project)

```
A = fastcdc (C06, content-defined chunk boundaries)
B = datasketch (C01, MinHash + LSH recall)
C = RapidFuzz (C05, edit-tolerant fuzzy verify)
       │
       ▼
NEW = byte-precise, multi-source provenance attribution for arbitrary
      new documents against a corpus index
```

- **A contributes:** chunk identity + byte offsets → "this file is 68% inside
  that file, spans [0:4120] of the source". Enables splice detection.
- **B contributes:** sublinear candidate recall; without it every query is
  corpus-wide.
- **C contributes:** admits near-dups (empty chunk overlap but real parent
  doc) that A alone would reject and B alone cannot locate.

**NEW CAPABILITY** that none of A/B/C alone provides: one query → structured
attribution report with *regions*, *coverage fractions*, and *confidence*.
Verified: recall 1.0, precision 0.875 on our benchmark (see PROTOTYPE_RESULTS).

## Other candidate fusions (explored, not built)

| fusion | promoted capability | verdict |
|---|---|---|
| chromaprint + acoustid-index | audio→hash→index search | strong but C08 is niche/early |
| videohash + arroy/PDX | video near-dup at scale | plausible; needs media corpus eval |
| Callidon/bloom-filters + datatrove | probabilistic pipeline primitives | folding, not new |
| GQL + dynamic-datalog | git-as-provenance-graph queries | research-y, unclear owner |
| zrip dict + cdc | compression-side dedup | already a dev-adjacent practice |
| pitgun + keermat-kv | deterministic DB sim testing | interesting, different domain |