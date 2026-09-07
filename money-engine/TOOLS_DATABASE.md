# TOOLS DATABASE - Money Opportunity Engine

## TRACK A: BUG BOUNTY & SECURITY TOOLS

### Tier 1 - Core Recon (Must-Have)

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| subfinder | projectdiscovery/subfinder | ~10k | Go | Subdomain Enum | Discovery |
| amass | owasp-amass/amass | ~13k | Go | Attack Surface | Deep Discovery |
| httpx | projectdiscovery/httpx | ~7k | Go | HTTP Probe | Validation |
| nuclei | projectdiscovery/nuclei | **31k** | Go | Vuln Scanner | Detection |
| naabu | projectdiscovery/naabu | ~4k | Go | Port Scanner | Service Discovery |

### Tier 2 - Deep Analysis

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| ffuf | ffuf/ffuf | **16.6k** | Go | HTTP Fuzzer | Path Discovery |
| dirsearch | maurosoria/dirsearch | **14.5k** | Python | Dir Scanner | Endpoint Discovery |
| katana | projectdiscovery/katana | ~4k | Go | Web Crawler | JS Endpoint Discovery |
| gau | lc/gau | ~7k | Go | URL Harvest | Historical URLs |
| dalfox | hahwul/dalfox | ~4k | Go | XSS Scanner | XSS Detection |

### Tier 3 - Source & Dependency Analysis

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| Semgrep | semgrep/semgrep | **11k** | OCaml | SAST | Code Analysis |
| gitleaks | gitleaks/gitleaks | **17k** | Go | Secret Detection | Secret Scanning |
| trivy | aquasecurity/trivy | **26k** | Go | Supply Chain | Dependency Scanning |
| sqlmap | sqlmapproject/sqlmap | **35k** | Python | SQLi | Injection Testing |

### Tier 4 - Specialized

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| Prowler | prowler-cloud/prowler | **11k** | Python | Cloud Security | AWS/Azure/GCP |
| MobSF | MobSF/Mobile-Security-Framework-MobSF | **17k** | Python | Mobile Security | APK/IPA Analysis |
| corsy | s0md3v/Corsy | ~1.5k | Python | CORS Testing | Header Analysis |
| Interactsh | projectdiscovery/interactsh | ~2k | Go | OOB Server | SSRF Confirmation |
| wafw00f | EnableSecurity/wafw00f | ~4k | Python | WAF Detection | Protection Mapping |

---

## TRACK B: MARKET INTELLIGENCE TOOLS

### Tier 1 - Data Foundation

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| CCXT | ccxt/ccxt | **43.7k** | JS/Py | Exchange Client | Data Collection |
| pandas | pandas-dev/pandas | **44k** | Python | Data Analysis | Normalization |
| numpy | numpy/numpy | **28k** | Python | Numerical | Signal Processing |

### Tier 2 - Signal Generation

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| TA-Lib | TA-Lib/ta-lib | **12.2k** | C/Python | Technical Indicators | Signal Generation |
| pandas-ta | twopirllc/pandas-ta | ~5k | Python | Indicators | Signal Generation |
| statsmodels | statsmodels/statsmodels | ~11k | Python | Statistics | Statistical Analysis |
| scikit-learn | scikit-learn/scikit-learn | **62k** | Python | ML | Pattern Recognition |

### Tier 3 - Backtesting & Execution

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| Freqtrade | freqtrade/freqtrade | **53.4k** | Python | Trading Bot | Backtest + Live |
| VectorBT | polakowo/vectorbt | **8.4k** | Python | Fast Backtest | Parameter Sweep |
| Jesse | jesse-ai/jesse | **8.4k** | Python | Strategy Framework | Research |
| Backtrader | mementum/backtrader | ~14k | Python | Backtest | Classic Backtest |

### Tier 4 - Risk & Portfolio

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| Riskfolio-Lib | riskfolio/Riskfolio-Lib | **4.4k** | Python | Portfolio Opt | Risk Management |
| pyportfolioopt | robertmartin8/PyPortfolioOpt | ~4k | Python | Portfolio | Allocation |
| Hummingbot | hummingbot/hummingbot | ~9k | Python | Market Making | Liquidity |

### Tier 5 - On-Chain & DeFi

| Tool | GitHub | Stars | Language | Category | Pipeline Role |
|------|--------|-------|----------|----------|---------------|
| web3.py | ethereum/web3.py | ~24k | Python | Ethereum Client | On-Chain Data |
| Dune Analytics | duneanalytics/spellbook | ~3k | SQL | Analytics | On-Chain Queries |
| DeFi Yield Scanner | Various | - | Python | Yield | DeFi Opportunities |

---

## UTILITY TOOLS (Both Tracks)

| Tool | GitHub | Stars | Language | Purpose |
|------|--------|-------|----------|---------|
| jq | jqlang/jq | **30k** | C | JSON Processing |
| anew | tomnomnom/anew | ~2k | Go | Deduplication |
| SQLite | - | - | SQL | Local Storage |
| rich | Textualize/rich | ~17k | Python | CLI Formatting |
