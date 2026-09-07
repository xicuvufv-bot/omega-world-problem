# MECHANISM DATABASE
## Structured Registry of All Discovered Economic Mechanisms

---

## MECHANISM 1: LIMIT ORDER BOOK MATCHING

```yaml
id: mechanism-001
name: "Limit Order Book Matching Engine"
source: BristolStockExchange/BSE.py
category: "Price Discovery"
input: "Trader orders with prices"
transformation: "Price-time priority matching"
output: "Executed trades at intersection prices"
repeatable: true
automated: true
scalable: true
license: MIT
evidence: "BSE.py:329-405"
economic_loop: "Orders → Matching → Trades → Price Discovery → More Orders"
multiplier: "Volume-dependent fees"
risk: "Adverse selection, latency"
```

---

## MECHANISM 2: CONSTANT PRODUCT AMM

```yaml
id: mechanism-002
name: "Constant Product Automated Market Maker (x*y=k)"
source: uniswap-v2-core/UniswapV2Pair.sol
category: "Automated Market Making"
input: "Token pair liquidity"
transformation: "x*y=k formula determines price automatically"
output: "Automatic price + 0.3% fee per swap"
repeatable: true
automated: true
scalable: true
license: GPL-2.0
evidence: "UniswapV2Pair.sol:110-131"
economic_loop: "Liquidity → Trading → Fees → More Liquidity"
multiplier: "~30% APR from fees"
risk: "Impermanent loss, smart contract risk"
```

---

## MECHANISM 3: PRICE-TIME PRIORITY MATCHING

```yaml
id: mechanism-003
name: "Price-Time Priority Order Matching"
source: OrderBook/orderbook/orderbook.py
category: "Order Matching"
input: "Market and limit orders"
transformation: "FIFO at each price level"
output: "Executed trades with full audit trail"
repeatable: true
automated: true
scalable: true
license: MIT
evidence: "orderbook.py:114-146"
economic_loop: "Orders → Priority Matching → Trades → Fair Prices"
multiplier: "0.01-0.25% per trade"
risk: "Market manipulation"
```

---

## MECHANISM 4: PAYMENT CHANNEL NETWORK

```yaml
id: mechanism-004
name: "Bidirectional Payment Channel Network"
source: lnd (Lightning Network)
category: "Payments"
input: "On-chain asset lockup"
transformation: "Off-chain transactions with cryptographic guarantees"
output: "Instant, near-zero-fee payments"
repeatable: true
automated: true
scalable: true
license: MIT
evidence: "lnd codebase"
economic_loop: "Lockup → Off-chain Txns → Settlement → More Channels"
multiplier: "5-20 bps routing fee"
risk: "Channel capacity, routing failures"
```

---

## MECHANISM 5: ALGORITHMIC INTEREST RATES

```yaml
id: mechanism-005
name: "Algorithmic Interest Rate Model"
source: compound-protocol
category: "Lending"
input: "Supplied assets"
transformation: "Utilization-based rate adjustment"
output: "Interest income for suppliers"
repeatable: true
automated: true
scalable: true
license: GPL-3.0
evidence: "compound-protocol contracts"
economic_loop: "Supply → Borrowing → Interest → More Supply"
multiplier: "2-15% APY"
risk: "Utilization spikes, rate volatility"
```

---

## MECHANISM 6: OVER-COLLATERALIZED STABLECOIN

```yaml
id: mechanism-006
name: "Over-Collateralized Stablecoin Minting"
source: dss (MakerDAO)
category: "Stablecoin"
input: "150% collateral (ETH)"
transformation: "Vault creation + stability fees"
output: "Stable $1 pegged digital dollar"
repeatable: true
automated: true
scalable: true
license: AGPL-3.0
evidence: "dss contracts"
economic_loop: "Collateral → DAI → Stability Fee → More Collateral"
multiplier: "67% capital efficiency"
risk: "Collateral crash, liquidation"
```

---

## MECHANISM 7: TRUST-BASED PAYMENT NETWORK

```yaml
id: mechanism-007
name: "Trust Graph Payment Network"
source: rippled (Ripple Protocol)
category: "Payments"
input: "Trust relationships"
transformation: "Pathfinding + IOU settlement"
output: "Multi-hop payments without intermediaries"
repeatable: true
automated: true
scalable: true
license: ISC
evidence: "rippled codebase"
economic_loop: "Trust → Pathfinding → Settlement → More Trust"
multiplier: "Network effect"
risk: "Trust defaults, centralization"
```

---

## MECHANISM 8: LOGARITHMIC MARKET SCORING RULE

```yaml
id: mechanism-008
name: "Logarithmic Market Scoring Rule (LMSR)"
source: google/arithmancer
category: "Prediction Markets"
input: "Trader beliefs about outcomes"
transformation: "LMSR pricing formula"
output: "Probability prices that aggregate information"
repeatable: true
automated: true
scalable: true
license: Apache-2.0
evidence: "arithmancer code"
economic_loop: "Beliefs → Market → Prices → Better Decisions"
multiplier: "Better-than-expert forecasting"
risk: "Low liquidity, information asymmetry"
```

---

## MECHANISM 9: OFF-CHAIN ORDER BOOK + ON-CHAIN SETTLEMENT

```yaml
id: mechanism-009
name: "Hybrid DEX Protocol"
source: 0x-monorepo
category: "Exchange"
input: "Off-chain signed orders"
transformation: "On-chain atomic settlement"
output: "Decentralized exchange without custody"
repeatable: true
automated: true
scalable: true
license: Apache-2.0
evidence: "0x-monorepo contracts"
economic_loop: "Orders → Relayers → Settlement → More Orders"
multiplier: "Network effect + protocol fees"
risk: "Front-running, MEV"
```

---

## MECHANISM 10: DAO GOVERNANCE

```yaml
id: mechanism-010
name: "Token-Weighted DAO Governance"
source: aragon
category: "Governance"
input: "Governance tokens"
transformation: "Proposal + voting + execution"
output: "Community-driven decision making"
repeatable: true
automated: true
scalable: true
license: GPL-3.0
evidence: "aragon contracts"
economic_loop: "Tokens → Voting → Treasury → More Tokens"
multiplier: "Governance + treasury growth"
risk: "Governance attacks, voter apathy"
```

---

## SUMMARY

| ID | Mechanism | Category | Multiplier | Risk |
|---|---|---|---|---|
| 001 | LOB Matching | Price Discovery | Volume fees | Medium |
| 002 | AMM | Market Making | 30% APR | Medium |
| 003 | Price-Time Priority | Order Matching | 0.1% per trade | Low |
| 004 | Payment Channels | Payments | 10-20 bps | Medium |
| 005 | Algorithmic Rates | Lending | 2-15% APY | Low |
| 006 | Stablecoin | Stablecoin | 67% efficiency | Medium |
| 007 | Trust Network | Payments | Network effect | High |
| 008 | LMSR | Prediction | Better forecasts | Medium |
| 009 | Hybrid DEX | Exchange | Protocol fees | Medium |
| 010 | DAO Governance | Governance | Treasury growth | Medium |
