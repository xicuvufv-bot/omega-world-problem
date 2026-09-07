# Professional Trading Bot for QX/Quotex

A rigorous, research-grade trading bot for Quotex/QXBroker binary options platform.
Built with institutional-level engineering practices.

## ⚠️ CRITICAL DISCLAIMERS

1. **NO OFFICIAL API** - Quotex has NO official API. This bot uses reverse-engineered WebSocket protocol.
2. **USE DEMO ACCOUNT ONLY** - Unofficial clients carry account risk per broker ToS.
3. **NOT FINANCIAL ADVICE** - This is a research framework, not a guaranteed profit system.
4. **PAST PERFORMANCE ≠ FUTURE RESULTS** - Backtest results are historical simulations only.

## Architecture Overview

```
trading_bot/
├── broker/           # WebSocket adapter for Quotex (unofficial)
├── data/             # Data cleaning & validation
├── features/         # Technical indicator computation
├── strategies/       # Strategy implementations
├── models/           # ML/Ensemble models
├── backtesting/      # Realistic backtesting engine
├── walk_forward/     # Walk-forward analysis
├── monte_carlo/      # Monte Carlo simulation
├── risk/             # Risk management & confidence scoring
├── execution/        # Order execution (demo only)
├── dashboard/        # Real-time monitoring
├── experiments/      # Experiment tracking
├── reports/          # Research report generation
├── config/           # Configuration management
├── tests/            # Unit & integration tests
└── main.py           # Entry point
```

## 28-Phase Development Process

### Phase 1-3: Data Pipeline
- **Phase 1**: WebSocket data collection from Quotex
- **Phase 2**: Data cleaning (dedup, outliers, gaps, OHLC validation)
- **Phase 3**: Feature engineering (50+ indicators)

### Phase 4-6: Strategy Research
- **Phase 4-5**: Backtesting engine with realistic simulation
- **Phase 6**: Strategy optimization framework

### Phase 7-8: Validation
- **Phase 7**: Walk-forward analysis (train/val/test sliding windows)
- **Phase 8**: Paper/demo trading

### Phase 9-10: Robustness
- **Phase 9**: Monte Carlo simulation (10,000+ scenarios)
- **Phase 10**: Stress testing (execution delay, payout drop, volatility, etc.)

### Phase 11-14: Risk & Decision
- **Phase 11**: Independent risk manager
- **Phase 12**: Ensemble meta-model
- **Phase 13**: Confidence scoring with NO TRADE logic
- **Phase 14**: NO TRADE as valid outcome

### Phase 15-17: ML & Quality
- **Phase 15**: ML models (baseline vs complex comparison)
- **Phase 16**: Overfitting prevention (train/val/test monitoring)
- **Phase 17**: Honest reporting (no cherry-picking)

### Phase 18-22: Operations
- **Phase 18**: Experiment manager (EXP-0001, EXP-0002...)
- **Phase 19**: Self-iteration (run → analyze → fix → repeat)
- **Phase 20**: Comprehensive test suite
- **Phase 21**: Real-time dashboard
- **Phase 22**: Standardized research reports

### Phase 23-28: Final Validation
- **Phase 23**: Capital projection (historical only)
- **Phase 24**: NO auto live trading
- **Phase 25**: Broker abstraction layer
- **Phase 26**: Clean architecture
- **Phase 27**: Edge-focused, not win-rate focused
- **Phase 28**: Honest final verdict

## Quick Start

### 1. Install Dependencies
```bash
cd trading_bot
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings (NEVER commit real credentials)
```

### 3. Run Backtest
```bash
python -m trading_bot.main --mode backtest --data data/eurusd_1m.csv
```

### 4. Run Walk-Forward
```bash
python -m trading_bot.main --mode backtest --data data/eurusd_1m.csv
```

### 5. Run Demo Mode
```bash
python -m trading_bot.main --mode demo
```

## Configuration

All settings via environment variables (`.env`):

```env
# Mode: demo, backtest, paper (NEVER live by default)
DEFAULT_MODE=demo

# Risk
MAX_RISK_PER_TRADE=0.02
MAX_DAILY_LOSS=0.05
MAX_DRAWDOWN=0.30
MIN_PAYOUT=0.75

# Backtest
INITIAL_BALANCE=10000
BACKTEST_SLIPPAGE=0.01

# Walk-Forward
WF_TRAIN_RATIO=0.6
WF_VAL_RATIO=0.2
WF_TEST_RATIO=0.2
WF_N_WINDOWS=5

# Monte Carlo
MC_N_SIMULATIONS=10000

# Confidence
MIN_CONFIDENCE=55
MIN_EDGE=0.02
```

## Key Features

### Realistic Backtesting
- Payout simulation (dynamic, asset-specific)
- Execution delay & slippage
- Concurrent trade handling
- Drawdown tracking
- Break-even analysis

### Walk-Forward Analysis
- Sliding train/validation/test windows
- Out-of-sample performance aggregation
- Overfitting detection (train vs test ratio)

### Monte Carlo Simulation
- 10,000+ scenario simulation
- Ruin probability at different risk levels
- Drawdown distribution
- Losing streak analysis

### Stress Testing
- Execution delay: 100ms → 1000ms
- Win rate degradation: -5% → -20%
- Payout reduction: 85% → 60%
- Volatility increase: 1.2x → 2.0x
- Data gaps, losing streaks, noise
- Parameter perturbation: ±5%, ±10%, ±20%
- **Classification**: ROBUST / MARGINAL / FRAGILE

### Risk Management
- Fixed fractional position sizing
- Daily loss limits
- Max drawdown protection
- Consecutive loss cooldown
- Payout filtering
- Volatility filtering
- Emergency stop

### Confidence Scoring
```
WIN RATE:     58.5%
BREAK-EVEN:   54.1%
EDGE:         +4.4%
CONFIDENCE:   67%
→ TRADE ALLOWED
```

### NO TRADE Logic
```python
# NO TRADE when:
edge <= 0                    # No statistical edge
confidence < 55              # Insufficient confidence
prob <= break_even_prob      # Below break-even
```

## Report Format

```
================================
BOT RESEARCH REPORT
===================
Best Strategy: EMA_Crossover
Best Asset:    EURUSD_otc
Best Timeframe: 60s
Best Expiration: 300s
Trades:        247
Wins:          142
Losses:        105
Win Rate:      57.5%
Break-even:    54.1%
Edge:          +3.4%
Net Profit:    $1,247.50
Profit Factor: 1.35
Max Drawdown:  12.3%
Longest Loss:  6
OOS Win Rate:  55.2%
Walk Forward:  VALIDATED
Monte Carlo:   Profit Prob=68.4%
Robustness:    ROBUST
Overfitting:   LOW
Final Verdict: POTENTIAL EDGE - PROCEED TO PAPER TRADING
================================
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_all.py::TestBacktestEngine -v

# With coverage
pytest tests/ --cov=trading_bot --cov-report=html
```

## Project Status

| Component | Status |
|-----------|--------|
| Data Collection | ✅ Implemented |
| Data Cleaning | ✅ Implemented |
| Feature Engineering | ✅ Implemented |
| Strategies (4 base) | ✅ Implemented |
| Backtesting Engine | ✅ Implemented |
| Walk-Forward | ✅ Implemented |
| Monte Carlo | ✅ Implemented |
| Stress Testing | ✅ Implemented |
| Risk Management | ✅ Implemented |
| Confidence Scoring | ✅ Implemented |
| Ensemble Model | ✅ Implemented |
| Experiment Manager | ✅ Implemented |
| Dashboard | ✅ Implemented |
| Reports | ✅ Implemented |
| Tests | ✅ Implemented |

## Honest Assessment

This system implements institutional-grade research methodology. However:

1. **No strategy has been proven profitable** on live Quotex
2. **All results are backtest simulations** with known limitations
3. **Binary options have negative expected value** for retail traders
4. **The broker has structural advantages** (market maker, payout control)
5. **Automation may violate ToS** and risk account closure

**If no statistical edge is found after thorough testing, the honest answer is:**
> "لم نجد Edge قابلة للإثبات." (No provable edge found)

## License

Research use only. Not for commercial trading without proper licensing and regulatory compliance.