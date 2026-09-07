# TOP_20_FUSIONS.md

The 20 fusions from the 100-grid that survive "does a single project already
do this?" and "does it map to a MASSIVE/LARGE problem?".

| rank | fusion | why it survives | blocker |
|---|---|---|---|
| 1 | CDC×LSH×Fuzzy → byte provenance | no dedicated open tool; demand (contamination, copyright) huge | winner, built |
| 2 | CDC chunk-inverted-index × eval harness | eval-harness plugin for leak audits | needs harness adapter |
| 3 | C01×C03 → streaming dedup w/ sketches | datatrove misses byte-precise ops | perf on true multi-TB |
| 4 | C07×C08 → audio provenance | media corp audit | fingerprint index early |
| 5 | C09×C13 → video provenance | same class as winner, media | needs video corpus |
| 6 | C10×C01 → image clump dedup | enterprise asset cleanliness | marginal demand |
| 7 | C11×C05 → tolerant prob. filters | probabilistic fuzzy set-membership | conceptual novelty thin |
| 8 | C14×C15 → VCS as provenance graph | regulatory/audit "when/why changed" | GQL/GQL ecosystem small |
| 9 | C17×C01 → compressed-size domain sketch | zero-token embedding / privacy | quality unproven |
| 10 | C16×C06 → deterministic replay of dedup tests | testability of pipelines | niche |
| 11 | C02×C03 → Rust core inside datatrove | raw speed | maintenance cost |
| 12 | C11×C03 → bloom-first pipelines | cheap prefilter for web crawl | additive |
| 13 | C01×C16 → noise-tolerant sketch sim | observability drift | speculative |
| 14 | C05×C03 → fuzzy filters service | fuzzy filtering block | single-feature wrapper |
| 15 | C12×C01 → SIMD sketch join | fast set membership | internal detail |
| 16 | C13×C05 → ANN + fuzzy rank | hybrid rank is generic (retrieval) | not novel enough |
| 17 | C08×C15 → dynamic index over hashes | incremental search infra | deep, early |
| 18 | C06×C03 → chunk-sharded crawler store | scale trick | not consumer-visible |
| 19 | C06×C09 → unified chunk+perceptual | multi-media dedup | wide scope |
| 20 | C10×C13 → image ANN near-dup | exists via Faiss approx | duplicated |

Rule: winner = #1, with #2–#6 as expansions, #8 as long research.