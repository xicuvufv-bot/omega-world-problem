# MISSING LAYERS — What Prevents Existing Tools from Working Together

## The 7 Missing Layers

### Layer 1: UNIFIED ENTITY IDENTITY
**Problem:** The same person appears as "John Smith" in email, "john@company.com" in CRM, "jsmith" in Slack, and "John S." in calendar.
**What exists:** No open standard for cross-tool entity resolution
**What's needed:** A local entity resolution engine that maps identities across tools
**Existing building blocks:** spaCy NER, Open Semantic Entity Search API, KGGen entity resolution

### Layer 2: CROSS-SOURCE CHANGE PROPAGATION
**Problem:** When a document changes in Google Drive, the email about it doesn't update, the calendar event referencing it doesn't know, and the task in Jira is stale.
**What exists:** changedetection.io (web only), document diff tools (docs only)
**What's needed:** A universal change detection engine that propagates across all sources
**Existing building blocks:** changedetection.io + DocxDiff + mail-parser + file watchers

### Layer 3: TEMPORAL CORRELATION
**Problem:** "What happened before/after/during that meeting?" requires checking email, docs, calendar, and files separately.
**What exists:** TimelineBuilder (personal data only), PM4Py (business processes only)
**What's needed:** A universal temporal correlation engine
**Existing building blocks:** TimelineBuilder + PM4Py + calendar sync tools

### Layer 4: RELATIONSHIP DISCOVERY
**Problem:** "Who are the key people in this project?" requires manually tracing through emails, docs, and code commits.
**What exists:** Knowledge graph tools (text only), OSINT tools (web only)
**What's needed:** Cross-source relationship discovery
**Existing building blocks:** KGGen + DeepKE + entity extraction + email threading

### Layer 5: PROCESS DISCOVERY FROM DIGITAL TRACES
**Problem:** "How does work actually flow here?" has no answer because no tool connects email → doc review → approval → file update → notification.
**What exists:** PM4Py (requires pre-built event logs), Apromore (enterprise only)
**What's needed:** Auto-extraction of event logs from digital activity
**Existing building blocks:** PM4Py + email timestamps + file modification times + calendar events

### Layer 6: PRIVACY-PRESERVING CROSS-TOOL SEARCH
**Problem:** "Find everything about Project X" requires searching email, Drive, Slack, Jira, and GitHub separately.
**What exists:** Semantic search tools (single source), cloud-based unified search (privacy risk)
**What's needed:** Local-first semantic search across all connected sources
**Existing building blocks:** txtai + local-semantic-search + Yjs/ElectricSQL for sync

### Layer 7: PROACTIVE PATTERN DETECTION
**Problem:** "I noticed you have 3 meetings about Project X this week but the document hasn't been updated in 2 months" — no tool connects these signals.
**What exists:** Nothing — this is completely unsolved
**What's needed:** Cross-source pattern detection engine
**Existing building blocks:** Knowledge graph + process mining + change detection

## The Architecture of the Missing Layer

```
┌─────────────────────────────────────────────────────────┐
│                  PROACTIVE INTELLIGENCE                  │
│         (Pattern detection, alerts, recommendations)    │
├─────────────────────────────────────────────────────────┤
│                    QUERY LAYER                           │
│          (Semantic search, graph traversal,             │
│           natural language, visualization)              │
├─────────────────────────────────────────────────────────┤
│                 INTELLIGENCE LAYER                       │
│    ┌───────────┬──────────────┬──────────────┐         │
│    │ Knowledge │ Process      │ Change       │         │
│    │ Graph     │ Mining       │ Detection    │         │
│    └───────────┴──────────────┴──────────────┘         │
├─────────────────────────────────────────────────────────┤
│                 CORRELATION LAYER                        │
│    ┌───────────┬──────────────┬──────────────┐         │
│    │ Entity    │ Temporal     │ Relationship │         │
│    │ Resolution│ Correlation  │ Discovery    │         │
│    └───────────┴──────────────┴──────────────┘         │
├─────────────────────────────────────────────────────────┤
│                 INGESTION LAYER                          │
│    ┌──────┬────────┬──────────┬──────┬────────┐       │
│    │Email │Docs    │Calendar  │Files │Web     │       │
│    └──────┴────────┴──────────┴──────┴────────┘       │
├─────────────────────────────────────────────────────────┤
│                 STORAGE LAYER                            │
│         (Local-first SQLite + CRDT sync)                │
└─────────────────────────────────────────────────────────┘
```

## Why This Layer Doesn't Exist Yet

1. **No one owns the cross-tool problem** — Each tool vendor optimizes for their own silo
2. **Privacy barriers** — Cloud-based solutions can't aggregate across providers
3. **Integration complexity** — 20+ data sources × 100+ edge cases each
4. **No business model** — Hard to monetize a neutral layer
5. **Technical difficulty** — Entity resolution across sources is an open research problem

## Why NOW Is the Right Time

1. **LLMs make entity extraction trivial** — What required custom ML now works with prompts
2. **Local-first is mature** — CRDTs, sync engines, SQLite are production-ready
3. **Open standards exist** — IMAP, iCal, SMTP, REST APIs are universal
4. **AI agents need this** — Agents without context are useless; this IS the context layer
5. **Privacy regulation** — GDPR/CCPA make local-first mandatory for many use cases
