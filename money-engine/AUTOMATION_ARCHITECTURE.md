# AUTOMATION ARCHITECTURE

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   MONEY OPPORTUNITY ENGINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   TRACK A    │    │   TRACK B    │    │   TRACK C    │       │
│  │ Bug Bounty   │    │ Market Intel │    │ Source Audit │       │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              SHARED INFRASTRUCTURE                   │        │
│  │  • Config Manager  • Logger  • Storage  • Alerts    │        │
│  └─────────────────────────────────────────────────────┘        │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Results    │    │   Reports    │    │   Evidence   │       │
│  │   Database   │    │  Generator   │    │   Archive    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Track A: Bug Bounty Pipeline

```
INPUT: Target Domain
  │
  ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DISCOVERY (Automated)          │
│  subfinder ──┐                          │
│  amass ──────┼──► anew (dedup)          │
│  assetfinder ┘                          │
└─────────────────┬───────────────────────┘
                  │ Subdomain List
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 2: VALIDATION (Automated)         │
│  httpx ──► Live hosts + tech stack      │
│  dnsx ──► DNS validation                │
│  naabu ──► Open ports                   │
└─────────────────┬───────────────────────┘
                  │ Validated Targets
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 3: CRAWLING (Automated)           │
│  katana ──► JS-aware URL discovery      │
│  gau ──► Historical URLs                │
│  waybackurls ──► Archive URLs           │
└─────────────────┬───────────────────────┘
                  │ URL List
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 4: SCANNING (Automated)           │
│  nuclei ──► 9000+ vulnerability checks  │
│  ffuf ──► Hidden endpoint discovery     │
│  dalfox ──► XSS detection              │
└─────────────────┬───────────────────────┘
                  │ Raw Findings
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VALIDATION (Semi-Auto)         │
│  interactsh ──► Blind vuln confirmation │
│  Manual review ──► False positive filter│
└─────────────────┬───────────────────────┘
                  │ Valid Findings
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 6: REPORTING (Automated)          │
│  Custom formatter ──► Markdown report   │
│  Severity scoring ──► Priority ranking  │
│  Evidence packaging ──► Screenshots/POC │
└─────────────────────────────────────────┘
```

## Track B: Market Intelligence Pipeline

```
INPUT: Exchange APIs
  │
  ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DATA COLLECTION (Automated)    │
│  CCXT ──► Multi-exchange price feeds    │
│  WebSocket ──► Real-time order books    │
│  Historical API ──► OHLCV data          │
└─────────────────┬───────────────────────┘
                  │ Raw Market Data
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 2: NORMALIZATION (Automated)      │
│  pandas ──► Unified data format         │
│  Cleaning ──► Remove outliers           │
│  Alignment ──► Time-series sync         │
└─────────────────┬───────────────────────┘
                  │ Clean Data
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 3: SIGNAL DETECTION (Automated)   │
│  TA-Lib ──► Technical indicators        │
│  Custom ──► Arbitrage detection         │
│  statsmodels ──► Statistical signals    │
└─────────────────┬───────────────────────┘
                  │ Signals
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 4: BACKTESTING (Automated)        │
│  VectorBT ──► Fast parameter sweep      │
│  Freqtrade ──► Strategy validation      │
│  Metrics ──► Sharpe, Sortino, MDD       │
└─────────────────┬───────────────────────┘
                  │ Validated Strategies
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 5: RISK MANAGEMENT (Automated)    │
│  Riskfolio-Lib ──► Position sizing      │
│  Custom ──► Max drawdown limits         │
│  Custom ──► Correlation checks          │
└─────────────────┬───────────────────────┘
                  │ Risk-Approved Signals
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 6: EXECUTION (Semi-Auto)          │
│  Paper Trading ──► 30-90 day validation │
│  Human Approval ──► Before live trades  │
│  Freqtrade ──► Order execution          │
└─────────────────┬───────────────────────┘
                  │ Trade Results
                  ▼
┌─────────────────────────────────────────┐
│ PHASE 7: MONITORING (Automated)         │
│  P&L Tracking ──► Real-time performance │
│  Alert System ──► Threshold breaches    │
│  Report Generator ──► Daily/weekly stats│
└─────────────────────────────────────────┘
```

## Shared Infrastructure

### Config Manager
```yaml
# config/settings.yaml
bug_bounty:
  max_threads: 50
  rate_limit: 100  # requests per minute
  scope_file: "config/scope.yaml"
  output_dir: "results/bug-bounty/"
  
market_intel:
  exchanges: ["binance", "coinbase", "kraken"]
  symbols: ["BTC/USDT", "ETH/USDT"]
  check_interval: 60  # seconds
  min_profit_pct: 0.1
  paper_trading: true
  
alerts:
  telegram: false
  discord: false
  email: false
  webhook: ""
```

### Storage Schema

```sql
-- findings.db
CREATE TABLE findings (
    id INTEGER PRIMARY KEY,
    track TEXT,  -- 'bug-bounty' or 'market-intel'
    type TEXT,
    severity TEXT,
    target TEXT,
    evidence TEXT,
    status TEXT,  -- 'new', 'validated', 'reported', 'duplicate'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- scans.db
CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    track TEXT,
    target TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    findings_count INTEGER,
    status TEXT
);

-- signals.db (market intel)
CREATE TABLE signals (
    id INTEGER PRIMARY KEY,
    strategy TEXT,
    symbol TEXT,
    signal_type TEXT,  -- 'buy', 'sell', 'arbitrage'
    confidence REAL,
    entry_price REAL,
    target_price REAL,
    stop_loss REAL,
    status TEXT,  -- 'pending', 'executed', 'expired'
    created_at TIMESTAMP
);
```

### Logger

```
logs/
├── engine.log          # Main engine log
├── bug-bounty/
│   ├── scans.log       # Scan progress
│   └── findings.log    # Discovery log
├── market-intel/
│   ├── signals.log     # Signal generation
│   └── trades.log      # Trade execution
└── errors.log          # Error tracking
```

### Alert System

```
Triggers:
  - New vulnerability found (severity >= medium)
  - Arbitrage opportunity > 0.3%
  - Strategy drawdown > 10%
  - Daily P&L summary
  - System errors

Channels:
  - Console (always on)
  - File logging (always on)
  - Telegram (optional)
  - Discord (optional)
  - Webhook (optional)
```

## Data Flow

```
                    ┌─────────────┐
                    │   Config    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │ Track A│  │ Track B│  │ Track C│
         └───┬────┘  └───┬────┘  └───┬────┘
             │           │           │
             ▼           ▼           ▼
         ┌────────────────────────────────┐
         │         Results Store          │
         │  (SQLite + JSON files)         │
         └──────────────┬─────────────────┘
                        │
              ┌─────────┼─────────┐
              │         │         │
              ▼         ▼         ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │ Reports│ │ Alerts │ │Evidence│
         └────────┘ └────────┘ └────────┘
```
