# LEGACY MECHANISMS
## Economic Mechanisms Found in Old Source Code

Each mechanism was extracted by reading actual source files from cloned repositories.

---

## 1. LIMIT ORDER BOOK (LOB) MATCHING ENGINE

**Source**: BristolStockExchange/BSE.py (Dave Cliff, 2012-2024)
**Lines of Code**: 3,484
**License**: MIT

### Mechanism
```
TRADER ORDERS → ORDER BOOK → MATCHING ENGINE → TRADES → TAPE
```

### How It Works
1. Traders submit buy (bid) or sell (ask) orders with prices
2. Orders are stored in two sorted lists: bids (highest first) and asks (lowest first)
3. When a bid price ≥ ask price, a TRADE executes
4. Both orders are removed from the book
5. A trade record is added to the tape

### Key Code (BSE.py:329-405)
```python
def process_order(self, time, order, tape_file, vrbs):
    [qid, response] = self.add_order(order, vrbs)
    best_ask = self.asks.best_price
    best_bid = self.bids.best_price
    if order.otype == 'Bid':
        if self.asks.n_orders > 0 and best_bid >= best_ask:
            counterparty = best_ask_tid
            price = best_ask
            self.asks.delete_best()
            self.bids.delete_best()
```

### Value Creation
- **Input**: Trader capital + information
- **Output**: Price discovery + executed trades
- **Multiplier**: Price represents MORE VALUE than individual orders (consensus)
- **Repeat**: Every order cycle
- **Scale**: Millions of orders per second

### Why It Failed Originally
- Limited to single exchange, no cross-exchange
- High latency (sequential processing)
- No automated market makers

---

## 2. CONSTANT PRODUCT AUTOMATED MARKET MAKER (x*y=k)

**Source**: uniswap-v2-core/contracts/UniswapV2Pair.sol (Uniswap, 2020)
**Lines of Code**: 201
**License**: GPL-2.0

### Mechanism
```
LIQUIDITY DEPOSIT → x*y=k FORMULA → SWAP → FEES → MORE LIQUIDITY
```

### How It Works
1. Liquidity providers (LPs) deposit two tokens in a pair
2. The contract enforces: reserve0 * reserve1 = k (constant)
3. When someone swaps token0 for token1:
   - They add token0 to the pool (increasing reserve0)
   - They receive token1 from the pool (decreasing reserve1)
   - The price adjusts automatically via x*y=k
4. A 0.3% fee is taken on every swap
5. Fees are added back to the pool, growing k

### Key Code (UniswapV2Pair.sol:110-131)
```solidity
function mint(address to) external lock returns (uint liquidity) {
    (uint112 _reserve0, uint112 _reserve1,) = getReserves();
    uint balance0 = IERC20(token0).balanceOf(address(this));
    uint balance1 = IERC20(token1).balanceOf(address(this));
    uint amount0 = balance0.sub(_reserve0);
    uint amount1 = balance1.sub(_reserve1);
    if (_totalSupply == 0) {
        liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
    } else {
        liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
    }
    _mint(to, liquidity);
}
```

### Value Creation
- **Input**: Token pair liquidity
- **Output**: Automatic price + fee income
- **Multiplier**: 0.3% fee on EVERY trade compounds
- **Repeat**: Every swap
- **Scale**: Unlimited new pairs

### Why It's Revolutionary
- No order book needed
- No market maker needed
- No counterparty risk
- Fully automated
- Anyone can create a market

---

## 3. ORDER MATCHING ENGINE (Price-Time Priority)

**Source**: OrderBook/orderbook/orderbook.py
**Lines of Code**: 235

### Mechanism
```
ORDERS → PRICE-TIME PRIORITY → MATCHES → TRADES → AUDIT TRAIL
```

### How It Works
1. Limit orders are placed in a price-sorted tree
2. Market orders execute immediately against best prices
3. Limit orders execute when price crosses
4. FIFO priority at each price level
5. Complete audit trail maintained

### Key Code (orderbook.py:114-146)
```python
def process_limit_order(self, quote, from_data, verbose):
    if side == 'bid':
        while (self.asks and price >= self.asks.min_price() and quantity_to_trade > 0):
            best_price_asks = self.asks.min_price_list()
            quantity_to_trade, new_trades = self.process_order_list('ask', best_price_asks, quantity_to_trade, quote, verbose)
```

---

## 4. PAYMENT CHANNEL NETWORK (Lightning Network)

**Source**: lnd (Lightning Network Daemon)
**Repository**: lightningnetwork/lnd

### Mechanism
```
ON-CHAIN LOCKUP → OFF-CHAIN TRANSACTIONS → SETTLEMENT → FEES → MORE CHANNELS
```

### How It Works
1. Two parties lock funds in a 2-of-2 multisig on-chain
2. They exchange signed transactions off-chain
3. Only the latest state is valid
4. Either party can close the channel and settle on-chain
5. Routing through intermediate nodes enables payments to anyone

### Value Creation
- **Input**: $1 locked in channel
- **Output**: Unlimited payment capacity through routing
- **Multiplier**: $1 can route $1000s of payments
- **Repeat**: Every off-chain transaction
- **Scale**: Network effect

---

## 5. TRUST-BASED PAYMENT NETWORK (Ripple)

**Source**: rippled (Ripple Protocol)
**Repository**: XRPLF/rippled

### Mechanism
```
TRUST LINES → PATHFINDING → SETTLEMENT → IOUs → MORE TRUST
```

### How It Works
1. Users establish trust lines with others (specify max trust amount)
2. Payments route through the trust graph
3. Each hop settles using IOUs
4. Final settlement can be in XRP or any currency
5. Pathfinding finds cheapest route

### Value Creation
- **Input**: Trust relationships
- **Output**: Multi-hop payments without intermediaries
- **Multiplier**: Each trust relationship enables many payments

---

## 6. ALGORITHMIC MONEY MARKET (Compound)

**Source**: compound-protocol
**Repository**: compound-finance/compound-protocol

### Mechanism
```
SUPPLY ASSETS → ALGORITHMIC RATES → BORROW → INTEREST → MORE SUPPLY
```

### How It Works
1. Users supply assets to a pool
2. Interest rates are set algorithmically based on utilization
3. Borrowers take loans against collateral
4. Interest flows to suppliers
5. Rates adjust automatically to balance supply/demand

### Value Creation
- **Input**: Idle assets
- **Output**: Interest income
- **Multiplier**: Compounding interest + governance token rewards
- **Repeat**: Every block

---

## 7. DECENTRALIZED STABLECOIN (MakerDAO DSS)

**Source**: dss (MakerDAO)
**Repository**: makerdao/dss

### Mechanism
```
COLLATERAL → VAULT → DAI MINTING → STABILITY FEE → MORE COLLATERAL
```

### How It Works
1. Users deposit ETH (150% collateralization)
2. They mint DAI (stablecoin) against it
3. Stability fees accrue on the debt
4. To retrieve collateral, users pay back DAI + fees
5. Liquidation auction if collateral ratio falls

### Value Creation
- **Input**: ETH collateral
- **Output**: Stable digital dollars
- **Multiplier**: 1 ETH → ~$2000 of DAI liquidity
- **Repeat**: Every vault creation

---

## 8. PREDICTION MARKET (LMSR)

**Source**: google/arithmancer
**Repository**: google/arithmancer

### Mechanism
```
TRADER BELIEFS → LMSR PRICING → PROBABILITY PRICES → BETTER DECISIONS → MORE PARTICIPANTS
```

### How It Works
1. Traders buy/sell shares in outcomes
2. LMSR (Logarithmic Market Scoring Rule) sets prices
3. Prices represent aggregate probability
4. Market makers provide liquidity
5. Settlement pays winners

### Value Creation
- **Input**: Trader information/opinions
- **Output**: Accurate probability forecasts
- **Multiplier**: Better than expert prediction
- **Repeat**: Continuous as new information arrives

---

## 9. DECENTRALIZED EXCHANGE PROTOCOL (0x)

**Source**: 0x-monorepo
**Repository**: 0xProject/protocol

### Mechanism
```
OFF-CHAIN ORDERS → ON-CHAIN SETTLEMENT → RELAYERS → FEES → MORE ORDERS
```

### How It Works
1. Makers create signed orders off-chain
2. Relayers host order books
3. Takers submit orders on-chain
4. Smart contract settles atomically
5. Relayers earn protocol fees

---

## 10. DAO GOVERNANCE (Aragon)

**Source**: aragon
**Repository**: aragon/aragonOS

### Mechanism
```
TOKEN HOLDERS → VOTING → TREASURY → GRANTS → MORE PARTICIPANTS
```

### How It Works
1. Holders stake governance tokens
2. Proposals are submitted
3. Voting power = token weight
4. Approved proposals execute via smart contracts
5. Treasury funds grants for ecosystem growth

---

## CROSS-MECHANISM INSIGHT

The most powerful pattern is **MECHANISM COMPOSITION**:

```
LOB + AMM + PAYMENT CHANNELS + STABLECOIN + DAO
= SELF-REINFORCING ECONOMIC ECOSYSTEM
```

Each mechanism amplifies the others:
- LOB provides price discovery
- AMM provides liquidity
- Payment channels provide scale
- Stablecoin provides stability
- DAO provides governance

This is exactly what modern DeFi has built. The SOURCE CODE for all these mechanisms exists in the repositories we cloned.
