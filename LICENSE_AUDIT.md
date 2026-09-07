# LICENSE AUDIT
## Legal Status of All Cloned Repositories

---

## PERMISSIVE LICENSES (Can Use Freely)

| Repository | License | Can Use |
|---|---|---|
| BristolStockExchange | MIT | ✅ Yes |
| OrderBook | MIT | ✅ Yes |
| Agent Zero | MIT | ✅ Yes |
| CrewAI | MIT | ✅ Yes |
| Connector IPFS | MIT | ✅ Yes |
| x402 Go Demo | MIT | ✅ Yes |

## COPYLEFT LICENSES (Must Share Derivatives)

| Repository | License | Can Use |
|---|---|---|
| Uniswap V2 Core | GPL-2.0 | ⚠️ Derivatives must be GPL |
| Compound Protocol | GPL-3.0 | ⚠️ Derivatives must be GPL |
| Augur | AGPL-3.0 | ⚠️ Network use triggers AGPL |
| Raiden Network | MIT | ✅ Yes |

## PROPRIETARY/CUSTOM LICENSES

| Repository | License | Can Use |
|---|---|---|
| Open-Transactions | MIT | ✅ Yes |
| Lightning Network | MIT | ✅ Yes |
| Rippled | ISC | ✅ Yes |
| 0x Protocol | Apache-2.0 | ✅ Yes |
| Aragon | GPL-3.0 | ⚠️ Derivatives must be GPL |
| Gnosis Safe | GPL-3.0 | ⚠️ Derivatives must be GPL |
| MakerDAO DSS | AGPL-3.0 | ⚠️ Network use triggers AGPL |
| Google Arithmancer | Apache-2.0 | ✅ Yes |
| CCXT | MIT | ✅ Yes |
| CrewAI | MIT | ✅ Yes |

---

## RECOMMENDATIONS

### For Prototypes
- Use MIT-licensed components (BristolStockExchange, OrderBook, Agent Zero, CrewAI)
- Avoid GPL components in closed-source products
- AGPL components are fine for internal tools

### For Production
- If building a SaaS: avoid AGPL (MakerDAO, Augur)
- If building open-source: GPL is fine
- If building a protocol: Apache-2.0 is best (0x, Arithmancer)

### For Forks
- MIT: Can fork and keep proprietary
- GPL: Must release derivative under GPL
- AGPL: Must release source even for network use

---

## KEY INSIGHT

Most of the valuable code (Uniswap, Compound, MakerDAO) uses GPL or AGPL. This means:
1. You CAN use the mechanisms
2. You MUST open-source your derivatives
3. You CAN compete with the original

This is actually GOOD for building new economic engines. The mechanisms are free to use, you just need to share your improvements.
