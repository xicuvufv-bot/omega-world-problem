# Bug Bounty Programs: Complete Research Guide (2026)

---

## 1. Top Bug Bounty Platforms

### HackerOne
- **URL:** [hackerone.com](https://hackerone.com)
- **Size:** Largest platform — ~2,000+ programs (Google, Microsoft, Dropbox, Uber, US DoD, Shopify)
- **How it works:** Companies publish programs with scope/reward tables. Researchers register, test in-scope assets, submit reports via the platform. Platform triage validates findings before they reach the company.
- **Reputation system:** Signal score (>5.0 = private invites), Impact score (>10 = top-tier programs like Shopify Plus, GitHub Sec, AWS)
- **Training:** Free Hacker101 CTF curriculum built in
- **Payouts:** $500 (mid-severity) to $100,000+ (critical). Platform pays out within 1–2 weeks of triage.
- **2025 total payouts:** $81M across the platform (+13% YoY). Top 100 programs alone paid $51M.
- **Strengths:** Widest program catalog, most private invite opportunities, transparent bounty disclosure
- **Weaknesses:** High competition (duplicates common), triage can be slow during busy periods

### Bugcrowd
- **URL:** [bugcrowd.com](https://bugcrowd.com)
- **Size:** Closest competitor to HackerOne. Strong mix of public bounties, private engagements, VDPs, and managed pentests.
- **How it works:** Researchers register, select skill areas/interests, browse public briefs or receive private invitations via CrowdMatch. Triage is managed internally for many programs.
- **Reputation system:** CrowdMatch learns your skills from submission history — the more you find in a category (XSS, IDOR, auth bypass), the more matching programs appear. Bug Bounty Hunter (BBH) levels I→IV gate access to elite programs.
- **Payouts:** $300–$3,000 average, $50,000+ top. Slightly faster payouts than HackerOne.
- **Key feature:** Transparent Vulnerability Rating Taxonomy (VRT), frequent bonus campaigns
- **Strengths:** Slightly less crowded than HackerOne, good balance of public/private, strong documentation for beginners
- **Weaknesses:** Some programs have slower triage for EU targets, UI less polished

### Intigriti
- **URL:** [intigriti.com](https://www.intigriti.com)
- **Size:** Dominant European platform. Belgium-based, GDPR-native. Growing global catalog.
- **How it works:** Similar marketplace model. Reports go through platform triage before reaching the company. SLA structure encourages 48-hour first response.
- **Reputation system:** Streak of consecutive valid reports boosts ranking. Top 100 = private invites.
- **Payouts:** Comparable to or slightly higher than HackerOne for EU programs. Faster feedback loops than both HackerOne and Bugcrowd.
- **Key feature:** Bonus system — extra payouts for particularly well-written reports or high-impact findings. Fewer unfair duplicate/informational closures.
- **Strengths:** Best new-researcher experience, fastest triage for European programs, active Discord community
- **Weaknesses:** Smaller total catalog than HackerOne/Bugcrowd, less recognition outside Europe

### YesWeHack
- **URL:** [yeswehack.com](https://www.yeswehack.com)
- **Size:** French platform, strong in EU. GDPR/NIS2-friendly.
- **Payouts:** Average comparable to Intigriti, slightly lower than HackerOne. Better acceptance rates (less competition).
- **Key feature:** Managed triage for all programs. Clear guidance on scope and rules of engagement.
- **Reputation:** Reputation > 1000 = most private invites. Top 50 in ranking = European Live Hacking Events.
- **Strengths:** Responsive triage, good for beginners building confidence, active community
- **Weaknesses:** Smaller catalog, less recognition outside Europe

### Immunefi
- **URL:** [immunefi.com](https://immunefi.com)
- **Size:** Dominant Web3/blockchain bounty platform. $162M+ in total available rewards.
- **Focus:** Smart contracts, DeFi protocols, crypto infrastructure
- **Payouts:** Median confirmed payout ~$2,000; average skewed to ~$52,800 by critical findings. Individual programs reach $10M–$16M.
- **All-time payouts:** $100M+
- **Strengths:** Deepest pool of Web3-native security talent, highest reward ceilings in any bug bounty ecosystem
- **Weaknesses:** Narrow focus — not suited for traditional web/API scope

### Synack
- **URL:** [synack.com](https://www.synack.com)
- **Model:** Invite-only, vetted researcher network (Synack Red Team). Researchers must pass skills assessment + background check.
- **Payouts:** $2,000–$10,000 average, $100,000+ top. Flat-rate subscription model for customers.
- **Strengths:** Higher payouts, lower competition, professional structured environment, FedRAMP Moderate Authorized (gov/defense clients)
- **Weaknesses:** Opaque application process, rejection common, not beginner-friendly

### Open Bug Bounty
- **URL:** [openbugbounty.org](https://www.openbugbounty.org)
- **Model:** Non-profit, coordinated disclosure. No mandatory payouts — rewards at site owner's discretion.
- **Stats:** ~2M coordinated disclosures, 1.66M+ fixed vulnerabilities
- **Best for:** Building portfolio, practicing responsible disclosure, learning the process

---

## 2. Top Public Bug Bounty Programs (Active, Paying)

### 1. Google Vulnerability Reward Program (VRP)
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | Chrome, Chrome OS, Android, Google Cloud, Google devices, YouTube, Maps, Search, all Google web properties |
| **Reward range** | $100–$250,000+ (full-chain Chrome sandbox escape = $250K) |
| **2025 payouts** | **$17.1 million total** (+40% YoY). Top researcher earned $811,000. |
| **Response time** | Fast — dedicated triage team |
| **Recent payouts** | $250K for Chrome sandbox escapes; $500 for WAF docs logic flaw |
| **Safe harbor** | Yes — explicit authorized conduct under CFAA/DMCA |

### 2. Microsoft Bug Bounty Program
| Field | Details |
|-------|---------|
| **Platform** | HackerOne (primary) |
| **Scope** | Azure, Microsoft 365, Edge, Windows, Power Platform, Dynamics, AI services. 15 separate programs. |
| **Reward range** | Up to **$250,000** per finding |
| **2025-2026 payouts** | **$20 million** to 562 researchers across 64 countries. Largest single payout: $200,000. |
| **Response time** | Defined SLAs per program |
| **Recent payouts** | $2.3M at Zero Day Quest 2026; $800K through open-source third-party code initiatives |
| **Safe harbor** | Yes — explicit "authorized conduct" language, legal safe harbor terms |

### 3. Apple Security Bounty
| Field | Details |
|-------|---------|
| **Platform** | Apple (direct) |
| **Scope** | iOS, macOS, watchOS, tvOS, iCloud, Safari, WebKit |
| **Reward range** | Up to **$2 million** (full chain with persistence) |
| **Total paid to date** | $35 million+ |
| **Response time** | Variable (Apple's internal triage) |
| **Safe harbor** | Yes — Apple explicitly authorizes good-faith research |

### 4. Shopify Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | `*.shopify.com`, Shopify admin, storefronts, APIs, Partners platform, mobile apps |
| **Reward range** | $500–$30,000+ |
| **Recent payouts** | Cache poisoning DoS: $3,800; Partners privilege escalation: $3,500; Collabs ATO: $800 |
| **Response time** | Active triage, frequent disclosures |
| **Safe harbor** | Yes |

### 5. GitHub Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | github.com, GitHub Enterprise Server, GitHub Actions, Copilot, all GitHub APIs |
| **Reward range** | $500–$30,000+ |
| **Response time** | Defined SLA |
| **Recent payouts** | Various disclosed reports in 2025-2026 |
| **Safe harbor** | Yes — explicit legal safe harbor, DMCA waiver, third-party protections |

### 6. Meta (Facebook) Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | Facebook, Instagram, WhatsApp, Messenger, Oculus VR, all Meta web/mobile properties |
| **Reward range** | $500–$100,000+ |
| **2025 payouts** | $4 million |
| **Recent payouts** | datr cookie theft chain: **$24,000** |
| **Response time** | 1–4 weeks |
| **Safe harbor** | Yes |

### 7. OpenAI Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | Bugcrowd |
| **Scope** | ChatGPT, API, model endpoints, account workflows, corporate infrastructure |
| **Reward range** | $200–$20,000+ (based on impact) |
| **Focus areas** | Data exfiltration, auth bypass, cross-tenant access, prompt injection with data exposure |
| **Response time** | Active triage |
| **Safe harbor** | Yes |
| **Note** | Focus on reproducible security impact; not model quality complaints or jailbreaks without data exposure |

### 8. GitLab Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | GitLab SaaS, self-managed instances, GitLab Runner, all web/API surfaces |
| **Reward range** | $200–$20,000+ |
| **Response time** | Defined SLA |
| **Safe harbor** | Yes |

### 9. Crypto.com Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | Full exchange — web, mobile, API, blockchain integrations |
| **Reward range** | Up to **$2,000,000** |
| **Note** | First crypto bug bounty to reach $2M on HackerOne |
| **Safe harbor** | Yes |

### 10. HackerOne (Self-Hosted) Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne (tests their own platform) |
| **Scope** | HackerOne platform, API, Triage systems |
| **Reward range** | Variable — Critical/High findings paid |
| **Recent payouts** | Critical SSRF via analytics webhook (disclosed) |
| **Note** | Good practice target — the platform rewards researchers who find issues in their own infrastructure |

### 11. Amazon Web Services (AWS) Bug Bounty
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | AWS services, console, APIs, SDKs |
| **Reward range** | $100–$100,000+ |
| **Safe harbor** | Yes |

### 12. U.S. Department of Defense (DoD) VDP
| Field | Details |
|-------|---------|
| **Platform** | HackerOne |
| **Scope** | `.mil` domains, select public-facing DoD systems |
| **Reward range** | VDP (recognition-based, not paid bounties for all reports) |
| **Note** | One of the largest VDPs — demonstrates government adoption |

---

## 3. Bug Bounty Methodology

### Phase 0: Scope & Program Analysis
**Before touching any tool, read the scope document.**

- Identify in-scope assets (domains, subdomains, APIs, mobile apps)
- Note exclusions and prohibited actions
- Study payout table (what severity = what reward)
- Check response time and triage quality
- Look for recently added domains (less tested = more opportunity)

### Phase 1: Reconnaissance (Passive)
**Zero interaction with the target.**

| Task | Tools |
|------|-------|
| Subdomain enumeration | Amass, Subfinder, crt.sh, Certificate Transparency logs |
| ASN & infrastructure mapping | whois, BGP.he.net, Shodan, Censys |
| GitHub/code search | truffleHog, gitDorks, GitHub dork queries |
| Email/account OSINT | theHarvester, Hunter.io |
| Archived URLs | Wayback Machine, Common Crawl |
| Technology fingerprinting | Wappalyzer, WhatWeb |

### Phase 2: Active Enumeration
**Direct interaction with target infrastructure.**

| Task | Tools |
|------|-------|
| DNS resolution & live host detection | httpx, massdns |
| Port scanning | nmap, masscan |
| Subdomain takeover check | SubOver, Can-I-Take-Over-XYZ |
| Screenshot/aquaton | Aquatone, GoWitness |
| JS file analysis | LinkFinder, SecretFinder, JSScanner |
| Cloud asset discovery | CloudBrute, S3Scanner |

### Phase 3: URL & Parameter Discovery
**Map the attack surface.**

| Task | Tools |
|------|-------|
| Deep crawling | Katana, Hakrawler, GoSpider |
| Archived URL mining | gau, waybackurls |
| Parameter discovery | Arjun, ParamSpider |
| Directory/content fuzzing | ffuf, dirsearch, feroxbuster |
| API route discovery | Kiterunner |

### Phase 4: Vulnerability Discovery
**The Two-Eye Approach:**

- **First Eye — Systematic Coverage:** Test every subdomain, endpoint, and parameter against the common vulnerability checklist. Methodical. No skipping.
- **Second Eye — Curiosity & Intuition:** Look for what's unusual. Unusual response sizes. Admin panels that shouldn't be indexed. S3 buckets named after internal projects.

**High-Priority Vulnerability Classes:**

| Vulnerability | What to Look For |
|---------------|-----------------|
| IDOR/BOLA | Insecure direct object references, predictable resource paths |
| XSS (Stored/DOM) | User input reflected without sanitization |
| SSRF | User-controlled URLs reaching internal services |
| SQL Injection | Database errors, blind injection points |
| Authentication bypass | Broken auth flows, session management flaws |
| Privilege escalation | Horizontal/vertical privilege abuse |
| Business logic flaws | Price manipulation, race conditions, workflow bypass |
| Open redirect | Redirect parameters accepting arbitrary URLs |
| CORS misconfiguration | Wildcard origins, credential-inclusive CORS |
| AI/ML vulnerabilities | Prompt injection, model abuse, data exfiltration via AI features |

### Phase 5: Exploitation & PoC
- Reproduce reliably from a clean session
- Escalate severity by chaining bugs
- Document everything: video (OBS Studio), screenshots (annotated), raw HTTP requests
- Keep PoC minimal — if it works in 3 steps, don't show 10

### Phase 6: Reporting
**Report structure:**

```
Title: [Severity] Short, specific description
Severity: Critical / High / Medium / Low
CVSS Score: [e.g. 9.8]
CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
Affected URL/Component: [exact location]
Vulnerability Type: [IDOR / XSS / SSRF / etc.]

Description:
[2-3 sentences — what, where, why exploitable]

Steps to Reproduce:
1. [Step-by-step, clean session]
2. [Each action with exact URL/parameter]
3. [Observed behavior]

Impact:
[Business consequences, not just technical facts]

Proof of Concept:
[Screenshots, video, raw HTTP requests/responses]

Remediation:
[Specific, actionable fixes — reference OWASP/CWE/CVE]

References:
[CVEs, CWEs, related writeups]
```

---

## 4. Legal Considerations

### What's Allowed vs Not Allowed

| Generally ALLOWED | Generally PROHIBITED |
|-------------------|---------------------|
| Testing in-scope assets | Testing out-of-scope assets |
| Using your own test accounts | Accessing/modifying other users' data |
| Demonstrating vulnerability with minimal impact | Data exfiltration beyond proof-of-vulnerability |
| Automated scanning (if permitted by program) | Denial-of-service / stress testing |
| Social engineering (only if explicitly in scope) | Phishing employees or customers |
| Reporting findings through the platform | Public disclosure before remediation |
| Chaining low-severity bugs for higher impact | Physical attacks or hardware tampering |

### Safe Harbor Policies

**What safe harbor means:** A formal statement from the program that they will not pursue civil or criminal legal action against researchers who follow the program rules in good faith.

**Key elements of good safe harbor (HackerOne Gold Standard):**
1. **Authorization:** Company considers security research "authorized conduct" under CFAA, DMCA, and equivalent laws
2. **No legal action:** Company commits to not pursuing civil/criminal action for good-faith research
3. **DMCA waiver:** Waives DMCA claims for circumventing protections within scope
4. **Third-party protection:** Limits information shared with third parties; won't share identifying info without written permission
5. **Good faith standard:** Defines what constitutes good-faith research
6. **Retroactive protection:** Safe harbor cannot be removed retroactively for research already conducted in good faith

**Red flag:** If a program has no safe harbor language, they haven't made an explicit legal commitment. The risk profile is different — proceed with caution.

### Rules of Engagement (RoE)

**Standard rules across all platforms:**

1. **Stay in scope** — Test only explicitly listed assets
2. **Use your own accounts** — Never use stolen credentials or access other users' data
3. **Don't break things** — Avoid DoS, data modification, service disruption
4. **Minimize data access** — Prove the vulnerability without exfiltrating real user data
5. **Report promptly** — Submit findings quickly after discovery
6. **Don't discuss publicly** — No public disclosure until remediation
7. **Use staging environments** — If provided, test there instead of production
8. **Stop if you hit sensitive data** — Contact the program before continuing

**Breaking RoE voids your safe harbor.** If the program offers a test environment and you test production instead, you're legally exposed.

---

## 5. High-Value Target Categories

### Tier 1: Highest Payouts

| Category | Examples | Why They Pay More |
|----------|----------|-------------------|
| **Crypto/DeFi/Web3** | Uniswap ($15.5M), LayerZero ($15M), Usual ($16M), Wormhole ($10M), Coinbase ($5M) | Smart contract exploits can drain millions in a single transaction. Bug bounties are cheaper than exploits. |
| **Tech Giants** | Google ($250K/findings), Apple ($2M max), Microsoft ($250K max) | Massive user bases, complex infrastructure, reputational risk |
| **Cloud Platforms** | AWS, Azure, GCP | Tenant isolation flaws affect thousands of businesses simultaneously |

### Tier 2: High Payouts

| Category | Examples | Why They Pay More |
|----------|----------|-------------------|
| **SaaS Companies** | Shopify, GitLab, GitHub, Salesforce | Multi-tenant architectures, API-heavy, business-critical workflows |
| **Fintech/Payments** | Stripe, PayPal, Crypto.com ($2M max) | Financial data exposure, unauthorized transfers, account takeover |
| **AI/ML Companies** | OpenAI, Anthropic | Emerging threat landscape, prompt injection, model abuse, data exfiltration |
| **Enterprise Software** | Oracle, SAP, Atlassian | Large attack surface, enterprise customer data |

### Tier 3: Medium Payouts

| Category | Examples | Notes |
|----------|----------|-------|
| **Consumer Apps** | Uber, Dropbox, Spotify | Moderate scope, competitive programs |
| **Gaming** | Rockstar Games, Electronic Arts | Growing bug bounty adoption |
| **Telecom** | AT&T, Verizon | Infrastructure-focused |

### Tier 4: Recognition/Low-Payment

| Category | Examples | Notes |
|----------|----------|-------|
| **Government VDPs** | US DoD, various agencies | Recognition, not money. Build portfolio. |
| **Open Source** | Internet Bug Bounty, Mozilla | Community contribution. Some paid bounties. |
| **Non-profits** | Open Bug Bounty | Disclosure practice, no guaranteed payout |

### Emerging High-Value Category: AI Security (2025-2026)

- Prompt injection vulnerabilities surged **540%** on HackerOne in 2025
- AI-related issues overall up **200%+**
- New categories: model abuse, cross-tenant data leakage, unsafe tool execution, supply chain attacks on AI pipelines
- OpenAI, Anthropic, Google, and Meta all expanding AI-specific bounty scope

---

## 6. Getting Started: Quick Reference

### For Beginners
1. **Start on Intigriti or Bugcrowd** — gentler learning curve, less competition
2. **Complete Hacker101** (free) and **PortSwigger Web Security Academy** (free)
3. **Practice on DVWA, OWASP WebGoat, HackTheBox** before testing real targets
4. **Pick ONE program** and read the scope document end-to-end
5. **Start with medium-severity findings** — don't chase criticals immediately
6. **Write excellent reports** — clear reproduction steps get triaged faster and paid more

### For Intermediate Researchers
1. **Diversify across 2-3 platforms** (HackerOne + Bugcrowd + Intigriti)
2. **Specialize in 2-3 vulnerability classes** (depth > breadth)
3. **Build private program access** through consistent valid reports
4. **Consider AI/ML hunting** — emerging category with less competition
5. **Target newly launched programs** — low-hanging fruit hasn't been picked

### For Advanced Researchers
1. **Apply to Synack** for higher payouts and lower competition
2. **Enter Web3/DeFi** if you have smart contract skills — six/seven-figure payouts
3. **Build relationships with program security teams** for faster triage
4. **Attend Live Hacking Events** (HackerOne LHEs paid $4.3M in 2025)

### Earning Expectations (Realistic)
| Level | Typical Payout Range | Notes |
|-------|---------------------|-------|
| Low severity | $100–$500 | Clickjacking, missing headers, informational findings |
| Medium severity | $1,000–$3,000 | IDOR, stored XSS, authentication issues |
| High severity | $3,000–$10,000 | Privilege escalation, significant data exposure |
| Critical severity | $10,000–$250,000+ | RCE, full auth bypass, mass data exposure, smart contract exploits |

**Median researcher experience:** Occasional side income, not full-time salary. Top ~5% on major platforms earn six figures annually.

### Tax Considerations
- Bug bounty income is **taxable** in most jurisdictions
- **US:** Expect a 1099 if you earn >$600 from a single platform/year
- **EU:** Generally treated as self-employment or supplementary income
- SEPA/EUR payments are simpler than USD/PayPal for EU researchers
- Talk to an accountant early if earning meaningfully

---

## 7. Key Tools Quick Reference

| Category | Tools |
|----------|-------|
| **Subdomain Enum** | Amass, Subfinder, crt.sh, DNSDumpster |
| **HTTP Probing** | httpx, massdns |
| **Port Scanning** | nmap, masscan |
| **Web Crawling** | Katana, Hakrawler, GoSpider, Burp Suite Spider |
| **Directory Fuzzing** | ffuf, dirsearch, feroxbuster |
| **Parameter Discovery** | Arjun, ParamSpider |
| **Vulnerability Scanning** | Nuclei, Burp Suite Pro |
| **JavaScript Analysis** | LinkFinder, SecretFinder, JSScanner |
| **API Discovery** | Kiterunner |
| **Cloud Assets** | CloudBrute, S3Scanner |
| **Archived URLs** | gau, waybackurls, GAU |
| **Proxy/Intercept** | Burp Suite (Community + Pro), mitmproxy |
| **OSINT** | Shodan, Censys, theHarvester, Recon-ng |
| **Reporting** | Platform-native report forms, annotated screenshots (Greenshot), video (OBS Studio) |

---

## 8. Resources

### Training
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) — Best free web security labs
- [HackerOne Hacker101](https://www.hackerone.com/hacker101) — Free CTF-style training
- [HackTheBox](https://hackthebox.com) — CTF machines
- [TryHackMe](https://tryhackme.com) — Beginner-friendly guided rooms
- [PentesterLab](https://pentesterlab.com) — Web exploitation exercises
- [OWASP WebGoat](https://owasp.org) — Deliberately vulnerable web app
- [DVWA](https://dvwa.co) — Damn Vulnerable Web Application

### Community & Tracking
- [Bug Bounty Radar](https://bbradar.io) — Latest public programs
- [BugBounty.info](https://bugbounty.info) — Methodology guides and scope reading
- [HackerOne Disclosed Reports Archive](https://github.com/ajaysenr/HackerOne-Disclosed-Reports) — Study real disclosed findings
- [getdisclosed.com](https://getdisclosed.com) — Disclosed reports newsletter

### Methodology References
- [Bug Bounty Methodology 2026 (GitHub)](https://github.com/ItsDarker/Bug-Bounty-Methodology-2026)
- [Bug Bounty Hunting Methodology 2026 (GitHub)](https://github.com/su6osec/Bug-Bounty-Hunting-Methodology-2026)
- [The Bug Hunter's Methodology (jhaddix)](https://github.com/jhaddix/tbhm)

---

*Research compiled September 2026. Program details, payout amounts, and platform features are subject to change. Always verify current scope and rules on the platform before testing.*
