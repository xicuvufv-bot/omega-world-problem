# COMPETITOR_MAP.md

## Who already does "provenance / contamination / dedup"?

| name | category | what it does | what's still missing |
|---|---|---|---|
| datasketch (ekzhu) | prob. sketches | document-level near-dup similarity | no spans, no splice, no byte attribution |
| deduplicate-text-datasets (Google) | batch dedup | exact+LSH cluster docs at corpus scale | destructive batch; no per-query provenance |
| dolma (AllenAI) | corpus toolkit | exact match/fuzzy dedup + inspect | build-time only, corpus-level, no new-doc query |
| datatrove (HF) | pipeline | filter/dedup services/executors | no byte-region attribution index |
| Turnitin/ZEROGRID/Copyscape | commercial plagiarism | doc-vs-web exact/fuzzy matching | closed, doc-vs-*their* index, no local self-hosted corpus, per-doc splice detail limited |
| sentence-transformers / embeddings | semantic sim | doc or chunk embedding near-dup | no byte-exact provenance; approximate; heavy; need GPU/space for corpus embeddings |
| lucene/bleve FS | full-text exact | substring-ish exact search, tokenized | no content-defined chunking; tokenization ≠ byte regions, no edit tolerance at byte span level |

## What is still missing after we checked all of these

1. **An open, self-hosted, queryable byte-precise provenance index** for *any
   consumer corpus* (model training data, internal document lake, crawled web).
2. **Splice-level multi-source attribution** ("30% from source A, 40% from
   source B") vs. doc-level near-dup.
3. Cheap CRUD: add new corpus docs incrementally and query a *new* document
   immediately — batch tools can't stream this.
4. Composability: license-permissive (MIT/Apache-2.0 stack) so it can be
   embedded in eval harnesses and data pipelines rather than being a walled
   service.

## Why the winner is not a wrapper

It wraps three libraries but adds the missing distributed state: a chunk-hash
inverted index keyed on content-defined boundaries + fused scoring. Nothing
else in the map keeps byte offsets *and* corpus scale *and* edit tolerance *and*
incremental indexing in one open package.