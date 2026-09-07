# Knowledge Forge

**Autonomous Knowledge Operations Platform**

An autonomous platform that crawls the web, parses any document, extracts knowledge, builds living knowledge graphs, and makes everything queryable by any AI agent.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE FORGE                               │
│                                                                  │
│  INGESTION         PARSING           UNDERSTANDING               │
│  ─────────         ───────           ────────────               │
│  Crawl4AI     →    MinerU       →    sift-kg                    │
│  (Web)             (Documents)        (Entity Extraction)        │
│                                                                  │
│  STORAGE           RETRIEVAL         ACCESS                      │
│  ───────           ─────────         ──────                      │
│  kektordb      ←   Hybrid        →   MCP Server                 │
│  (Vector+Graph)    Search            (Any AI Agent)              │
└─────────────────────────────────────────────────────────────────┘
```

## Components

| Component | Purpose | License |
|-----------|---------|---------|
| Crawl4AI | Web crawling | AGPL-3.0 |
| MinerU | Document parsing | Apache-2.0 |
| sift-kg | Entity extraction | MIT |
| kektordb | Hybrid search | Custom |
| Dagu | Workflow orchestration | GPL-3.0 |

## Quick Start

```bash
# Clone with submodules
git clone --recursive <repo-url>

# Install Python dependencies
pip install -e core/

# Run demo
python core/demo.py
```

## Usage

```bash
# Crawl URLs
knowledge-forge crawl https://example.com https://docs.example.com

# Parse documents
knowledge-forge parse ./documents/

# Search knowledge
knowledge-forge search "your query here"

# Start KektorDB server
knowledge-forge server
```

## Project Structure

```
knowledge-forge/
├── crawl4ai/          # Web crawler (AGPL-3.0)
├── mineru/            # Document parser (Apache-2.0)
├── sift-kg/           # Entity extraction (MIT)
├── kektordb/          # Hybrid search (Custom)
├── dagu/              # Workflow engine (GPL-3.0)
└── core/              # Integration layer (MIT)
    ├── knowledge_forge/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── crawler.py
    │   ├── parser.py
    │   ├── graph.py
    │   ├── store.py
    │   ├── pipeline.py
    │   └── cli.py
    ├── demo.py
    └── pyproject.toml
```

## License

Core integration layer: MIT

Individual components retain their original licenses (see LICENSE_MATRIX.md).
