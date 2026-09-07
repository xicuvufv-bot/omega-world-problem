# Crypto Trading & Quantitative Analysis Tools Database

> Compiled from GitHub research — September 2026

---

## 1. EXCHANGE CLIENTS & DATA COLLECTION

### CCXT (CryptoCurrency eXchange Trading Library)
- **GitHub**: https://github.com/ccxt/ccxt
- **Stars**: ~43,700
- **Status**: ✅ Active (last updated continuously)
- **Language**: Python, JavaScript/TypeScript, PHP, C#, Go, Java, Ruby
- **What it does**: Unified API for 104+ crypto exchanges — market data, order placement, account management, WebSocket feeds
- **Pipeline role**: Foundation layer for all exchange interaction; normalized data across exchanges enables cross-exchange arbitrage, portfolio tracking, and multi-exchange backtesting
- **Key features**: REST + WebSocket APIs, normalized OHLCV/ticker/orderbook data, 104 exchanges, prediction market support (Polymarket, Kalshi)

### go-binance
- **GitHub**: https://github.com/ad䨞h/GoBi-nance
- **Stars**: ~1,886
- **Status**: ✅ Active
- **Language**: Go
- **What it does**: Go SDK for Binance API — spot and futures, websocket streams
- **Pipeline role**: High-performance Binance-specific connectivity for latency-sensitive strategies

### node-binance-api
- **GitHub**: https://github.com/nodejsexplor/node-binance-api
- **Stars**: ~1,663
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: Async Node.js library for Binance API
- **Pipeline role**: JavaScript/Node.js ecosystem integration for real-time Binance data

### binance-rs
- **GitHub**: https://github.com/binance-exchange/binance-rs
- **Stars**: ~845
- **Status**: ✅ Active
- **Language**: Rust
- **What it does**: Rust library for Binance API — low-latency, high performance
- **Pipeline role**: Ultra-low-latency exchange connectivity for HFT strategies

---

## 2. MARKET DATA LIBRARIES & DATA COLLECTION

### yfinance
- **GitHub**: https://github.com/ranaroussi/yfinance
- **Stars**: ~14,500
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Yahoo Finance API wrapper — historical OHLCV, fundamentals, options
- **Pipeline role**: Free historical data for backtesting stocks and crypto; used extensively in quantitative analysis tools

### CoinGecko API (Free)
- **URL**: https://api.coingecko.com/api/v3/
- **Status**: ✅ Active
- **Language**: REST API
- **What it does**: Free crypto market data — prices, market cap, volume, historical data for 10,000+ coins
- **Pipeline role**: Primary free data source for crypto market intelligence, sentiment analysis, and portfolio tracking

### DeFiLlama API
- **URL**: https://defillama.com/docs/api
- **Status**: ✅ Active
- **Language**: REST API (free, no auth)
- **What it does**: DeFi data — TVL, yields, DEX volumes, stablecoins across 19,000+ pools and 119 chains
- **Pipeline role**: Essential for DeFi yield optimization, protocol analytics, and on-chain intelligence

### Dune Analytics (Spellbook)
- **GitHub**: https://github.com/duneanalytics/spellbook
- **Stars**: ~2,000+
- **Status**: ✅ Active
- **Language**: SQL (DuneSQL/Trino)
- **What it does**: Community-curated blockchain data — decoded contract events, aggregated tables for DEX trades, NFTs, tokens, wallets
- **Pipeline role**: On-chain analytics, wallet tracking, protocol revenue analysis, DeFi volume monitoring

### Flipside Crypto
- **GitHub**: https://github.com/FlipsideCrypto/flipside-tools
- **Stars**: ~500+
- **Status**: ✅ Active (migration to Dune ongoing)
- **Language**: SQL (Snowflake)
- **What it does**: Blockchain analytics across 40+ chains — wallet activity, token transfers, protocol metrics
- **Pipeline role**: Cross-chain analytics and wallet intelligence

---

## 3. BACKTESTING ENGINES

### Freqtrade
- **GitHub**: https://github.com/freqtrade/freqtrade
- **Stars**: ~53,400
- **Status**: ✅ Active (releases monthly)
- **Language**: Python
- **What it does**: Full-featured crypto trading bot — backtesting, hyperopt (ML optimization), live/dry-run trading, Telegram control, web UI
- **Pipeline role**: End-to-end trading system: strategy development → backtesting → optimization → live deployment. The gold standard for crypto algo trading

### VectorBT
- **GitHub**: https://github.com/polakowo/vectorbt
- **Stars**: ~8,400
- **Status**: ✅ Active
- **Language**: Python (Numba, Rust optional)
- **What it does**: Vectorized backtesting engine — runs thousands of parameter combinations in parallel via NumPy/Numba matrices
- **Pipeline role**: Rapid strategy research and large-scale parameter sweeps; turns hours of grid search into seconds

### backtesting.py
- **GitHub**: https://github.com/kernc/backtesting.py
- **Stars**: ~8,500
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Lightweight backtesting framework with built-in optimizer, interactive Plotly visualizations, library-agnostic indicators
- **Pipeline role**: Quick strategy prototyping with excellent visualization; ideal for individual traders

### Jesse
- **GitHub**: https://github.com/jesse-ai/jesse
- **Stars**: ~8,400
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Advanced crypto trading framework — 300+ indicators, multi-symbol/timeframe, research API, Jupyter integration, significance testing, Monte Carlo
- **Pipeline role**: Research-focused backtesting with statistical rigor; good for strategy validation and publication-quality analysis

### FinRL-X
- **GitHub**: https://github.com/AI4Finance-Foundation/FinRL-Trading
- **Stars**: ~3,500
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: AI-native quantitative trading infrastructure — ML-based stock selection, DRL portfolio allocation, backtesting with Alpaca integration
- **Pipeline role**: Deep reinforcement learning for portfolio optimization; bridges academic ML research with live trading

### OctoBot
- **GitHub**: https://github.com/Drakkar-Software/OctoBot
- **Stars**: ~6,400
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Free crypto trading bot — AI strategies, Grid, DCA, TradingView integration, 15+ exchanges
- **Pipeline role**: User-friendly bot with AI/ML strategy support; good for non-developers via web interface

### Algo.Py
- **GitHub**: https://github.com/himanshu2406/Algo.Py
- **Stars**: ~362
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Python-first algo trading framework — unified data layer, backtesting engine, live deployment, AI-enhanced OMS/RMS
- **Pipeline role**: Bridge between backtesting and live trading; supports crypto, Indian, and US markets

### basana
- **GitHub**: https://github.com/gbeced/basana
- **Stars**: ~350
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Async event-driven algo trading framework for crypto — backtesting exchange, live via CCXT, pairs trading support
- **Pipeline role**: Async-first architecture for event-driven strategies; good for pairs/cointegration trading

---

## 4. QUANTITATIVE LIBRARIES & STATISTICAL ANALYSIS

### TA-Lib (Python Wrapper)
- **GitHub**: https://github.com/TA-Lib/ta-lib-python
- **Stars**: ~12,200
- **Status**: ✅ Active
- **Language**: Python (Cython wrapper for C library)
- **What it does**: 150+ technical indicators (ADX, MACD, RSI, Stochastic, Bollinger Bands), candlestick pattern recognition
- **Pipeline role**: Industry-standard indicator computation; used by most trading frameworks for technical analysis

### pandas-ta-classic
- **GitHub**: https://github.com/xgboosted/pandas-ta-classic
- **Stars**: ~361
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: 252 unique indicators and patterns — pandas extension, no TA-Lib dependency, optional TA-Lib acceleration
- **Pipeline role**: Pure Python alternative to TA-Lib; 62 candlestick patterns without C dependencies

### Riskfolio-Lib
- **GitHub**: https://github.com/dcajasn/Riskfolio-Lib
- **Stars**: ~4,400
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Portfolio optimization — Mean Risk, Kelly Criterion, CVaR, risk parity, hierarchical clustering (HRP/HERC), 26+ convex risk measures
- **Pipeline role**: Institutional-grade portfolio construction and risk management; efficient frontier optimization

### OptimalPortfolios
- **GitHub**: https://github.com/ArturSepp/OptimalPortfolios
- **Stars**: ~200+
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Portfolio optimization with 7 objectives — min variance, max Sharpe, ERC, max diversification, max utility, max CARA under mixture distributions
- **Pipeline role**: Research-grade portfolio backtesting with rolling-forward methodology; includes crypto allocation research

### QuantForge
- **GitHub**: https://github.com/theNeuralHorizon/quantforge
- **Stars**: ~5
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Full-stack quant platform — options pricing (Black-Scholes, binomial, Monte Carlo), portfolio optimization, VaR, ML regime detection, GARCH, cointegration tests
- **Pipeline role**: Comprehensive quantitative research platform with 489+ tests

### je-suis-tm/quant-trading
- **GitHub**: https://github.com/je-suis-tm/quant-trading
- **Stars**: ~10,500
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Collection of proven trading strategies — VIX, pairs trading, MACD, RSI, Bollinger Bands, Bollinger Bands pattern recognition, Dual Thrust, London Breakout, etc.
- **Pipeline role**: Strategy library and educational resource; reference implementations for common quant strategies

---

## 5. RISK MANAGEMENT

### Riskfolio-Lib (see above)
- **Stars**: ~4,400
- Covers VaR, CVaR, drawdown, 26+ risk measures, portfolio optimization

### crypto-risk-toolkit
- **GitHub**: https://github.com/Ryan-Clinton/crypto-risk-toolkit
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: VaR (historical/parametric/MC), CVaR, Sharpe/Sortino/Calmar, position sizing (Kelly), regime detection, multi-asset correlation
- **Pipeline role**: Standalone risk analytics for crypto, stocks, forex

### Algo-Risk-Monitor
- **GitHub**: https://github.com/ahasdemir/Algo-Risk-Monitor
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: VaR suite, efficient frontier, Monte Carlo (10,000+ sims), GBM simulation, Streamlit dashboard
- **Pipeline role**: Interactive risk monitoring with visual dashboards

### Basel III Crypto Risk Management
- **GitHub**: https://github.com/JCP9415/basel-iii-crypto-risk-management
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: GJR-GARCH volatility modeling, Bayesian forecasting (CBQRA), Monte Carlo stress tests, Kelly Criterion scaling, flash crash detection
- **Pipeline role**: Institutional-grade risk management with GARCH and Bayesian methods

### mefai-risk-ai
- **GitHub**: https://github.com/mefai-dev/mefai-risk-ai
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: AI-powered risk assessment using Temporal Fusion Transformer (BiLSTM + attention), multi-timeframe analysis, inverse-volatility portfolio weighting
- **Pipeline role**: ML-based risk scoring and position sizing

---

## 6. ALERT SYSTEMS

### PricePulse
- **GitHub**: https://github.com/stillrun-lab/pricepulse
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Configurable price-alert bot — Telegram + Discord notifications, runs on GitHub Actions cron, zero infrastructure
- **Pipeline role**: Serverless price monitoring with state-based deduplication

### crypto-alert-system
- **GitHub**: https://github.com/danilobatson/crypto-alert-system
- **Stars**: ~1
- **Status**: ✅ Active
- **Language**: TypeScript/React
- **What it does**: Production-ready alert system — 11 alert types (price, volume, sentiment, Galaxy Score), browser notifications, LunarCrush API
- **Pipeline role**: Full-stack alert platform with social sentiment monitoring

### Arbitrage Alert Bot
- **GitHub**: https://github.com/bolgac/arbitrage-alert-bot
- **Stars**: ~2
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Cross-exchange arbitrage detection — async price fetching, Telegram/Discord alerts, Flask dashboard, CLI control
- **Pipeline role**: Real-time arbitrage opportunity detection with multi-channel notifications

### Jutt-Trade-Bot (Comprehensive)
- **GitHub**: https://github.com/iamgopaul/Jutt-Trade-Bot
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Full trading signal bot — technical analysis signals, AI-powered research (Llama 3.3 70B), price alerts, news digest, anomaly detection, Telegram commands
- **Pipeline role**: End-to-end intelligence pipeline: signal detection → AI verification → multi-channel alerts

---

## 7. DASHBOARD & VISUALIZATION

### Flowtrades
- **GitHub**: https://github.com/AminMstlih/Flowtrades
- **Stars**: ~7
- **Status**: ✅ Active
- **Language**: Python + JavaScript
- **What it does**: Real-time order flow terminal — footprint charts, volume delta, absorption/exhaustion detection, 60 FPS canvas rendering from Binance/OKX/Bybit WebSocket
- **Pipeline role**: Institutional-grade order flow visualization for market microstructure analysis

### Sibyl (AI-Powered)
- **GitHub**: https://github.com/nMaroulis/sibyl
- **Stars**: ~73
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: AI-powered crypto trading hub — multi-exchange support, LLM agent integration, backtesting, strategy deployment, interactive dashboard
- **Pipeline role**: Unified platform for AI-driven trading with visualization

### Crypto Monitor (Fluent Design)
- **GitHub**: https://github.com/shiquda/crypto-monitor
- **Stars**: ~27
- **Status**: ✅ Active
- **Language**: Python (PyQt6)
- **What it does**: Desktop crypto monitor — Fluent Design UI, real-time WebSocket from OKX/Binance, DEX token support, step alerts, mini charts
- **Pipeline role**: Cross-platform desktop monitoring application

### OpenTrader
- **GitHub**: https://github.com/nodminger/OpenTrader
- **Stars**: ~13
- **Status**: ✅ Active
- **Language**: Python + JavaScript
- **What it does**: Open-source TradingView alternative — unlimited indicators, backtracking, React + TradingView Lightweight Charts
- **Pipeline role**: Free alternative to TradingView for charting and backtesting

### Crypto-Realtime-QuestDB
- **GitHub**: https://github.com/marketcalls/Crypto-Realtime-QuestDB
- **Stars**: ~2
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Real-time analytics dashboard — QuestDB time-series database, Coinbase WebSocket, 8 trading pairs, Chart.js visualization
- **Pipeline role**: Time-series data infrastructure for high-frequency crypto analytics

---

## 8. ON-CHAIN ANALYTICS

### DeFi On-Chain Analytics
- **GitHub**: https://github.com/Omnis-Labs/defi-onchain-analytics
- **Stars**: ~1
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: AI agent skill for on-chain analysis — wallet profiling, protocol analysis, DEX analytics, smart contract inspection across 6 EVM chains (108 verified RPC endpoints)
- **Pipeline role**: Raw RPC-based on-chain intelligence without API dependencies

### DeepLens
- **GitHub**: https://github.com/alanisme/deeplens
- **Stars**: ~11
- **Status**: ✅ Active
- **Language**: Rust
- **What it does**: EVM blockchain analytics desktop app — real-time monitoring, address profiling, entity mapping, fund-path tracing across 7 chains
- **Pipeline role**: Desktop investigation tool for wallet tracking and fund flow analysis

### NEXUS (1ai-tracker)
- **GitHub**: https://github.com/oyi77/1ai-tracker
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: Crypto whale tracker — smart money detection, entity mapping, flow analysis, prediction markets across ETH/SOL/BTC/ARB/BASE/OP, zero API keys
- **Pipeline role**: Real-time whale and smart money intelligence platform

### Atlas (Solana Smart Money)
- **GitHub**: https://github.com/AtlasOnchain/Atlas
- **Stars**: ~34
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: Solana capital-flow mapper — tracks origin wallets, follower propagation, sector rotation, Claude AI agent for flow alerts
- **Pipeline role**: Solana-specific smart money tracking with AI-powered alert generation

### BaseForge
- **GitHub**: https://github.com/AmnAnon/baseforge-v1
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: Base ecosystem intelligence — TVL tracking, whale flows, MEV monitoring, gas tracking, AI agent data feeds, risk scoring across 580+ protocols
- **Pipeline role**: Chain-specific DeFi analytics with AI-ready data payloads

### Superchain Token Explorer
- **GitHub**: https://github.com/serayd61/Superchain-token-explorer
- **Stars**: ~1
- **Status**: ✅ Active
- **Language**: TypeScript
- **What it does**: Real-time token deployment tracking across Optimism Superchain (7+ OP Stack chains), AI DeFi assistant
- **Pipeline role**: L2 ecosystem monitoring and new token discovery

---

## 9. CROSS-EXCHANGE ARBITRAGE TOOLS

### crypto-arbitrage-framework
- **GitHub**: https://github.com/hzjken/crypto-arbitrage-framework
- **Stars**: ~701
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Multi-lateral arbitrage path optimization — CCXT + CPLEX solver, monitors multiple exchanges, calculates optimal trading amounts, multi-threaded execution
- **Pipeline role**: Production-grade arbitrage detection with mathematical optimization (Bellman-Ford + linear programming)

### Cross-Venue Arbitrage
- **GitHub**: https://github.com/tfrmma/cross-venue-arbitrage
- **Stars**: ~3
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: CEX-DEX arbitrage engine — Binance, Bybit, Kraken, Hyperliquid, dYdX v4, Lighter; L2 order book ingestion, concurrent execution
- **Pipeline role**: Cross-venue arbitrage between centralized and decentralized perpetual markets

### CEX-DEX Price Gap Monitor
- **GitHub**: https://github.com/Rezzecup/cex-dex-price-gap-monitor
- **Stars**: ~19
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Real-time CEX-DEX spread monitoring — Streamlit dashboard, gas-adjusted net-gap, webhook alerts, historical replay
- **Pipeline role**: CEX-DEX arbitrage opportunity detection with gas cost analysis

---

## 10. DeFi YIELD OPTIMIZATION

### DeFi Yield Aggregator (rizalcodes)
- **GitHub**: https://github.com/rizalcodes/defi-yield-aggregator
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Compares APY across Aave V3, Compound, Curve, Uniswap V3; Telegram alerts for APY spikes, stablecoin filtering
- **Pipeline role**: Real-time yield comparison across major DeFi lending/liquidity protocols

### DeFi Yield Scanner
- **GitHub**: https://github.com/Bob-QoQ/defi-yield-scanner
- **Stars**: ~0
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Scans 19,000+ pools across 119 chains — safety filters (TVL > $1M, APY < 100%), cross-chain protocol comparison, batch stablecoin scanning
- **Pipeline role**: Comprehensive yield discovery with risk-adjusted filtering

### Yield Guard Bot
- **GitHub**: https://github.com/Enricrypto/yield-guard-bot
- **Stars**: ~1
- **Status**: ✅ Active
- **Language**: Python
- **What it does**: Treasury management platform — Aave V3, Morpho, Compound V3; backtesting with real market data, 25+ performance metrics, enterprise risk management
- **Pipeline role**: Institutional-grade DeFi yield optimization with risk controls

### DeFi Yield Hunter
- **GitHub**: https://github.com/reanblock/DeFi-Yield-Hunter
- **Stars**: ~1
- **Status**: ✅ Active
- **Language**: Python/TypeScript
- **What it does**: Multi-agent portfolio scout — Alchemy RPC for wallet holdings, Athena SQL for pool yields, S3 Vectors for research, Bedrock LLM for recommendations
- **Pipeline role**: AI-powered yield optimization with qualitative research integration

---

## 11. PROVEN TRADING STRATEGIES

Based on je-suis-tm/quant-trading and other research:

### Mean Reversion
- **Bollinger Bands**: Buy when price touches lower band, sell at upper band
- **RSI Reversal**: Buy when RSI < 30, sell when RSI > 70
- **Pairs Trading**: Cointegrated pairs converge to mean; statistical arbitrage

### Momentum
- **MACD Crossover**: Buy on MACD line crossing above signal line
- **Dual MA Crossover**: Fast SMA crosses above slow SMA
- **Momentum Ranking**: Buy top N assets by recent returns, rebalance monthly

### Breakout
- **Donchian Channel Breakout**: Buy on 20-day high breakout
- **Bollinger Band Squeeze**: Enter on volatility expansion after compression
- **London Breakout**: Range breakout during London session open

### Volatility
- **ATR-Based Stops**: Position sizing and stops based on Average True Range
- **Volatility Targeting**: Scale position size to target constant portfolio volatility

### Statistical Arbitrage
- **Cointegration-Based Pairs**: Engle-Granger or Johansen tests, z-score trading
- **Cross-Exchange Arbitrage**: Price discrepancies between exchanges for same asset
- **Triangular Arbitrage**: Currency triangle inefficiencies within single exchange

---

## 12. RECOMMENDED PIPELINE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                      │
├─────────────────────────────────────────────────────────────┤
│  CCXT (104 exchanges)  │  DeFiLlama (DeFi)  │  Dune (on-chain) │
│  CoinGecko (prices)    │  yfinance (stocks)  │  WebSocket feeds │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSIS & SIGNAL LAYER                    │
├─────────────────────────────────────────────────────────────┤
│  TA-Lib / pandas-ta (indicators)  │  Riskfolio-Lib (portfolio) │
│  VectorBT (backtesting)           │  Riskfolio (optimization)  │
│  Custom strategies (je-suis-tm)   │  ML models (FinRL-X)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RISK & EXECUTION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  VaR/CVaR calculations  │  Position sizing (Kelly)           │
│  Drawdown limits         │  Circuit breakers                  │
│  Portfolio optimization  │  Multi-exchange execution (CCXT)   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MONITORING & ALERTS                        │
├─────────────────────────────────────────────────────────────┤
│  PricePulse (price alerts)   │  Telegram/Discord bots        │
│  Dashboards (Streamlit/React)│  On-chain analytics (Dune)     │
│  DeepLens (wallet tracking)  │  Atlas (smart money)           │
└─────────────────────────────────────────────────────────────┘
```

---

## STAR RANKING SUMMARY (Top 20)

| Rank | Tool | Stars | Category |
|------|------|-------|----------|
| 1 | Freqtrade | ~53,400 | Backtesting/Bot |
| 2 | CCXT | ~43,700 | Exchange Client |
| 3 | yfinance | ~14,500 | Data Library |
| 4 | TA-Lib | ~12,200 | Technical Indicators |
| 5 | je-suis-tm/quant-trading | ~10,500 | Strategy Collection |
| 6 | VectorBT | ~8,400 | Backtesting |
| 7 | backtesting.py | ~8,500 | Backtesting |
| 8 | Jesse | ~8,400 | Trading Framework |
| 9 | OctoBot | ~6,400 | Trading Bot |
| 10 | Riskfolio-Lib | ~4,400 | Portfolio Optimization |
| 11 | FinRL-X | ~3,500 | AI/ML Trading |
| 12 | OptimalPortfolios | ~200+ | Portfolio Optimization |
| 13 | Sibyl | ~73 | Dashboard |
| 14 | crypto-arbitrage-framework | ~701 | Arbitrage |
| 15 | Algo.Py | ~362 | Trading Framework |
| 16 | pandas-ta-classic | ~361 | Technical Indicators |
| 17 | basana | ~350 | Event-Driven Trading |
| 18 | Crypto Monitor | ~27 | Desktop App |
| 19 | Atlas | ~34 | On-Chain Analytics |
| 20 | OpenTrader | ~13 | Charting |

---

*Database compiled September 2026. Stars are approximate and may fluctuate.*
