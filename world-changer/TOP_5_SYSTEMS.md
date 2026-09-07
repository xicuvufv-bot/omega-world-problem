# TOP_5_SYSTEMS.md

The five full systems the funnel produced. Three prototyped ideas ranked; one
built for real. (See FUSION_GRAPH.md for the map.)

## System 1 — Provenance Vetting Engine (WINNER, built)

- **Purpose:** given any new document → which corpus sources it derives from,
  byte-precise, with edit tolerance + splice attribution.
- **Components:** FastCDC chunk-hash inverted index + datasketch MinHash-LSH +
  RapidFuzz QRatio.
- **Proof:** real benchmark (8 query classes, 40-doc corpus): recall 1.0,
  precision 0.875, byte localization 0.68, ~30 ms/query.

## System 2 — Eval-Harness Contamination Adapter

- **Purpose:** `bench --against corpus` → per-question leaked-span report.
- **Verdict:** merges System 1 into lm-eval-style harnesses. Expansion.

## System 3 — Media Provenance (audio/video/image)

- **Purpose:** generalized perceptual-hash inverted index (chromaprint,
  videohash, pHash + arroy/PDX) for media corpora.
- **Verdict:** plausible, but fingerprint index tooling (acoustid-index) is
  too early → keep on watchlist, build after System 1 solidifies.

## System 4 — VCS-as-Provenance-Graph

- **Purpose:** SQL/datalog over git history for regulatory audit "when/why did
  this line change".
- **Verdict:** research; GQL/gitql ecosystem small. Watchlist.

## System 5 — Streamlined Corpus Govern Layer

- **Purpose:** datatrove + dolma + System 1 as one governed data pipeline with
  attribution available at any stage.
- **Verdict:** the expansion horizon of System 1; NOT built now because it
  would have been a wrapper (instruction: no wrappers).

The winner earned the slot: it has a real problem, a real new capability, and
a working measured prototype.