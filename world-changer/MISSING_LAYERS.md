# MISSING_LAYERS.md

The map of "layers" current technology lacks — and which the winner supplies.

## Layer model (proposed)

Any data/value stack has layers: data, computation, coordination, execution,
verification, trust, knowledge, interoperability. Tech usually focuses on data
and computation. The underserved layers for unstructured text:

| layer | exists? | gap |
|---|---|---|
| Data (collect/store) | datatrove, dolma, S3/Parquet | plentiful |
| Computation (clean/dedup) | deduplicate-text-datasets, datasketch | batch only |
| **Attribution (byte-precise, per-document, queryable)** | **no** | **the winner** |
| Verification (did it come from here?) | manual / Perplexity / embeddings | arbitrary-query, open, precise missing |
| Trust (licenses/provenance attest) | paper trails | no executable layer |

## The missing layer this project provides

**Attribution layer** — an inverted index over content-defined chunks +
MinHash-LSH recall + RapidFuzz tolerance, exposed as: *given any document,
return which corpus byte-ranges it contains, from which sources, with coverage
and confidence.*

Why it is missing today:

1. dedup tools are **destructive batch** transforms (they delete dups); they
   answer "which docs are near-dups" at build time, not "which source gave me
   this text" at query time.
2. datasketch gives similarity, not positions — no spans, no splice handling.
3. plain search (grep, Full-Text) is exact-string only — no edit tolerance, no
   chunk-boundary independence, no multi-source.

That is precisely the "missing layer" a compliance/contamination audit needs:
an executable, queryable, per-document attribution step that plugs into the
data/computation layers that already exist.