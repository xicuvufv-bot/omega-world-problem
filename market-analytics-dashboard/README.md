# Market Analytics Dashboard - Project Summary

## Overview
A professional web platform for real-time market analysis focused on **education and simulation only**. No real money trading, no guaranteed profits, and no financial data storage.

## Project Structure

```
market-analytics-dashboard/
├── frontend/          # React + Vite + TypeScript + Tailwind CSS
│   ├── src/           # Source files
│   ├── index.css      # Tailwind directives
│   ├── tailwind.config.cjs
│   └── postcss.config.js
├── server/            # Node.js + Express API
│   ├── index.js       # Main server file
│   ├── package.json   # Dependencies
│   └── indicators.js  # Technical indicators library
└── .gitignore         # Git ignore file
```

## Technical Stack

**Frontend:**
- React 19 with TypeScript
- Vite 8.2.2 (dev server + HMR)
- Tailwind CSS 4.3.3 (for styling)
- Chart.js 2 via react-chartjs-2 (for charts)

**Backend:**
- Node.js with Express
- HTTP polling for real-time data (WebSocket had module compatibility issues with Node.js 24)
- Custom technical indicator calculations
- In-memory simulation history

**Indicators Calculated:**
- EMA (Exponential Moving Average) - 20 period
- SMA (Simple Moving Average) - 20 period
- RSI (Relative Strength Index) - 14 period
- MACD (Moving Average Convergence Divergence) - 12/26/9
- Bollinger Bands - 20 period, 2 std dev
- ATR (Average True Range) - 14 period

## Key Features Implemented

### 1. Real-Time Market Data
- 7 assets: Gold (XAUUSD), Silver (XAGUSD), EUR/USD, GBP/USD, USD/JPY, BTC/USD, ETH/USD
- Live price display with change percentages
- Online/Offline status indicators
- Automatic data refresh every 2 seconds

### 2. Multi-Factor Technical Analysis
All these indicators are calculated for each asset:
- **Trend**: EMA vs SMA alignment
- **Momentum**: RSI (overbought >70, oversold <30)
- **MACD**: Convergence/divergence histogram
- **Bollinger Bands**: Price position relative to bands
- **Support/Resistance**: Recent high/low levels
- **Volatility**: ATR-based filtering
- **Price Action**: Trend direction and momentum

### 3. Scoring System
- **Score range**: 0-100 based on indicator alignment
- **Label**: "Analysis Score: XX/100" (NOT "guaranteed profit")
- **Historical confidence message**: "This score represents the strength of the available technical signals. It is NOT a guarantee of future performance."
- **Signal reasons**: List of which indicators contributed to the score

### 4. Educational Signal Cards
When score >= 70, a signal card is generated with:
- Asset name and direction (UP/DOWN)
- Analysis score / 100
- Timeframe (5 MINUTES by default)
- Signal time and expiry time
- Technical reasons bullet list
- Risk level (HIGH/MEDIUM/LOW based on volatility)
- Status: "SIMULATION ONLY"
- Historical confidence disclaimer

### 5. Simulation Engine
- Tracks signal results (WIN/LOSS)
- Records: signal time, asset, direction, price at signal, price at expiry, PnL
- Calculates statistics:
  - Total signals, wins, losses
  - Win rate percentage
  - Average move percentage
  - Max winning/losing streaks
  - Performance by asset
  - Performance by timeframe
- No look-ahead bias in calculations

### 6. Backtesting Support
- API endpoints for signal history
- Performance statistics by asset and timeframe
- Configurable strategy parameters
- Historical data structure ready for integration

### 7. Proper Disclaimers
- No "guaranteed profits" or "95% winning rate"
- All scores labeled as "Analysis Score" with proper explanation
- Signals marked as "SIMULATION ONLY"
- Clear separation between analysis and real trading

### 8. Error Handling
- API offline status displayed
- No fabricated prices when data fails
- Graceful degradation when indicators can't be calculated
- Timestamp on all data and signals

### 9. Responsive UI
- Dark mode compatible ( Tailwind dark classes)
- Glassmorphism-inspired design
- Animated market data cards
- Responsive grid layout (mobile-first)
- Signal countdown timers
- Performance statistics dashboard

## How to Run the Project

### Prerequisites
- Node.js v20+ (v24 confirmed working)
- npm v11+ (or yarn/pnpm)

### Installation

1. **Navigate to project directory:**
   ```bash
   cd C:\Users\Administrator\Documents\Default Project\market-analytics-dashboard
   ```

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies:**
   ```bash
   cd ../server
   npm install
   ```

### Running the Project

1. **Start the backend server:**
   ```bash
   cd server
   node index.js
   ```
   Server will run on `http://localhost:3000`
   - API health: `GET http://localhost:3000/api/health`
   - Assets: `GET http://localhost:3000/api/assets`
   - Market data: `GET http://localhost:3000/api/market-data?asset=gold`
   - Signals: `GET http://localhost:3000/api/signals`
   - Simulation stats: `GET http://localhost:3000/api/simulation-stats`
   - Submit result: `POST http://localhost:3000/api/simulation/result`

2. **Start the frontend development server:**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

3. **Access the dashboard:**
   Open your browser to `http://localhost:5173`

   The dashboard will automatically connect to the backend API and display:
   - Live market data for all 7 assets
   - Recent trading signals
   - Performance statistics
   - Signal cards with analysis details

### Project Verification

Both servers should be running:
- Backend: Console shows "Market Analytics Server running on port 3000"
- Frontend: Vite shows "Local: http://localhost:5173/"

Visit `http://localhost:5173` to verify the dashboard loads correctly.

## Extending the Project

### Real Data Integration
To integrate real market data:
1. Obtain an API key from a financial data provider (Alpha Vantage, CryptoCompare, Polygon, etc.)
2. Replace the `mockData` object in `server/index.js` with real API calls
3. Adjust the `fetchPrice` function to match the API response format
4. The indicator calculation logic remains the same

### Additional Features
- **Backtesting UI**: Add a strategy configuration panel
- **More timeframes**: Add 1m, 15m, 1h, 4h, 1D timeframe analysis
- **More indicators**: Stochastic Oscillator, Ichimoku, OBV, etc.
- **User accounts**: Persist simulation results to a database
- **Alert system**: Email/desktop notifications for high-scoring signals
- **Chart interactions**: Clickable charts for detailed analysis

### Important Notes
- This project is for **educational and simulation purposes only**
- No real money trading functionality is implemented or enabled
- All data is simulation/mock unless explicitly integrated from a real API
- Proper disclaimers are displayed everywhere
- Never use this for actual financial trading without proper licensing and risk management