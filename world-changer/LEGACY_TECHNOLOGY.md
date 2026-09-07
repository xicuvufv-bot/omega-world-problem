# LEGACY_TECHNOLOGY.md

Ideas that failed once and may be re-born now that constraints changed.

## 1. Content-defined chunking as a *search* primitive

**Old use:** FastCDC and similar (LBFS, rabin-Karp CDC) were built for
storage-level dedup (backups, syncing, restic/rclone world). It was famously
successful *there*, but never crossed into text search/provenance, in part
because word-level/n-gram search was the default and chunking felt redundant.

**Why it failed then:** search was document-level; nobody asked "what is this
text region-by-region"; storage dedup vendors kept CDC in the storage domain.

**What changed now:**
- Corpus-scale text is the dust of the ML boom → *region provenance* is a new
  demand.
- Doc-level similarity (datasketch) and byte-level identity (CDC) can be fused
  cheaply on modern hardware.
- Per-query byte-precise provenance is finally valuable (contamination,
  copyright).

**Rebirth:** chaining a CDC chunk-hash inverted index with an LSH index + fuzzy
verify = provenance-as-a-query. (§The winner.)

## 2. Audio fingerprinting inverted indexes (chromaprint/acoustid-index)

**Old idea:** fingerprint audio, then answer "which song is this clip from?"
via an inverted index.

**Not dead** — AcousticID is alive. But the pattern generalizes: *any*
perceptual hash (video, image, mesh) → inverted index. The current bottleneck
was niche tooling (acoustid-index early Zig), not demand.

## 3. "Search over git as a database" (gitql/GQL)

Old, still exploratory. Why it stalled: git is not a data store and most people
don't need SQL over commits. Rebirth possibility is low unless combined with
provenance graphs (issue-tracking → regulatory audit), N/A scope here.

## 4. Compression-as-classifier (biden_nlp, zrip dictionaries)

**Old idea:** train a zstd dictionary over class corpora, then use compressed
size as a similarity signal (NN via compressor). Fun research, weak in practice
for semantic tasks.

**Legacy matter:** dictionaries hint at *domain membership* — could be a
zero-token "domain sketch" complementing LSH. Kept on the watchlist, not
promoted to the winner.

## Rebirth candidate kept

1. CDC-as-search (winner)
2. perceptual-hash→inverted-index generalization (videos/images, media corpus)