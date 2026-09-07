# MASSIVE_PROBLEMS.md

Classified by evidence, not by vibes.

## 1. LLM benchmark contamination — GLOBAL

**Problem:** Eval/test sets leak into training corpora; every published score
on a leaked benchmark is inflated. Labs keep publishing gated or hedged scores
and the community keeps doing post-hoc hunts.

**Evidence:**
- Web-scale corpus construction (C4/RedPajama/OLMo) repeatedly reports
  dedup as a mandatory, multi-TB step — the underlying cost is duplication.
- deduplicate-text-datasets (Rust) & dolma (AllenAI) exist precisely because
  corpora are full of near-dup text; removing it is a first-class task.
- Public discussion (HN, ML forums): contamination is the default suspicion
  for any surprising new benchmark result; no standard open *queryable*
  attestation exists.

**Who is hurt:** every researcher reading benchmark tables; every org that
offers competitive evaluations; model consumers.

## 2. Copyright / license provenance for model training data — LARGE

**Problem:** If a model's output resembles a copyrighted document, there is no
cheap way to show which corpus source it trained on. This is increasingly a
legal question, not a curiosity.

**Evidence:** high-profile copyright litigation over training data, artist and
writer injunctions; ML licensing docs (DataComp, etc.) centered on provenance
resurfacing as a compliance need.

## 3. Copy-paste / duplication on the web — GLOBAL

**Problem:** A single web page template duplicated across many domains inflates
crawler budgets, ranking, training corpora, and dashboards.

**Evidence:** same C4/RedPajama dedup pipelines; SEO duplication discussions;
the existence of an entire class of dedup tools.

## 4. Report / research integrity audits — NICHE→LARGE

**Problem:** detecting whether a new document (report, patent, submission)
reuses text across sources *and* which sources — the "splice" we demonstrate —
has no cheap open tool.

We selected #1/#2 as the primary market the new layer serves, with #3/#4 as
direct secondary uses.

## Evidence links (representative, not exhaustive)

- ekzhu/datasketch README + API docs (versions 2026)
- allenai/dolma GitHub README (OLMo data toolkit)
- google-research/deduplicate-text-datasets README (C4-scale method ref)
- huggingface/datatrove README (pipeline blocks catalog)
- RapidFuzz docs (QRatio/partial_ratio behavior, edge cases)