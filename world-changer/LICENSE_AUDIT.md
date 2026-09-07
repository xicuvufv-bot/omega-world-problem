# LICENSE_AUDIT.md

License compliance check for every project deployed or synthesized in the
prototype.

| project | license | commercial | modify | redistribute | verdict |
|---|---|---|---|---|---|
| ekzhu/datasketch | MIT | ✓ | ✓ | ✓ | clear |
| allenai/dolma | Apache-2.0 | ✓ | ✓ | ✓ | clear |
| google-research/deduplicate-text-datasets | Apache-2.0 | ✓ | ✓ | ✓ | clear |
| huggingface/datatrove | Apache-2.0 | ✓ | ✓ | ✓ | clear |
| rapidfuzz/RapidFuzz | MIT | ✓ | ✓ | ✓ | clear |
| tigerwill90/fastcdc | MIT | ✓ | ✓ | ✓ | clear |

**Decision:** the whole fusion is MIT/Apache-2.0-compatible. Re-using the
algorithms (FastCDC is a published algorithm; MinHash-LSH standard) allows us
to keep dependencies minimal and license posture clean.

## Rejected candidates on license alone

| project | license | reason |
|---|---|---|
| Zabuzard/FastCDC4J | GPL-3.0 | incompatible with reproducing engine internals |
| acoustid/chromaprint | LGPL-ish/NOASSERTION | not needed for winner; only adjacent |
| mk-fg/image-deduplication-tool | WTFPL | phrasing permissive but non-standard for a product |
| frankmcsherry/dynamic-datalog | NOASSERTION | no declared license → avoid |

## Notes

- No training-data / model-weights licensing applies (no models used).
- Our built artifacts (corpus generator, engine, benchmark) can be released
  under MIT.