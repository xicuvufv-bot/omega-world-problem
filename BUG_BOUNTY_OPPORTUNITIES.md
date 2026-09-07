# BUG_BOUNTY_OPPORTUNITIES.md

## Active Bug Bounty Programs for Security Research

### TIER 1: HIGHEST REWARD PROGRAMS

#### 1. Vercel OSS Bug Bounty (HackerOne)
- **URL**: https://hackerone.com/vercel-open-source
- **Scope**: Next.js, SvelteKit, Vercel CLI, and all Vercel OSS projects
- **Rewards**: $1,000 - $50,000 per vulnerability
- **Total Pool**: $1,000,000 USD (sandbox challenge)
- **Focus**: Isolation escapes, RCE, data access across tenants
- **Requirements**: Functional PoC, demonstrated end-to-end impact
- **Timeline**: 1 business day first response, 7 days triage, 10 days bounty decision
- **Best For**: Next.js vulnerabilities, React Server Components, Edge Runtime issues

#### 2. Google OSS VRP (Bug Hunters)
- **URL**: https://bughunters.google.com/open-source-security
- **Scope**: All Google-owned GitHub repos (Golang, Angular, Fuchsia, etc.)
- **Rewards**:
  - OT0 (Flagship): $500-$7,500 product vulns, $3,133-$31,337 supply chain
  - OT1 (Important): $101-$3,133 product vulns, $1,337-$13,337 supply chain
  - OT2 (Standard): $500 supply chain
- **Focus**: Supply chain compromises, product vulnerabilities
- **Requirements**: High-quality reports with buildable PoC
- **Best For**: Golang stdlib, Angular, Chromium-related projects

#### 3. GitHub Bug Bounty (HackerOne)
- **URL**: https://hackerone.com/github
- **Rewards**:
  - Public: $250 (Low), $2,000 (Medium), $5,000 (High), $10,000 (Critical)
  - VIP: $1,000 (Low), $4,500 (Medium), $20,000 (High), $30,000+ (Critical)
- **Scope**: GitHub.com, GitHub Enterprise, Actions, Copilot
- **Focus**: Authentication, authorization, data access
- **Requirements**: HackerOne signal threshold for public program
- **Best For**: GitHub Actions supply chain, Copilot vulnerabilities

#### 4. ProjectDiscovery OSS Bounty
- **URL**: https://github.com/projectdiscovery/oss-bounty-program
- **Scope**: Nuclei, Katana, Subfinder, Httpx, Naabu, and more
- **Rewards**: Fixed/variable based on impact (amounts disclosed upfront)
- **Focus**: Bug fixes, performance improvements, features
- **Requirements**: Claim issue, complete within 2 weeks, PR linked to issue
- **Best For**: Security tool developers, vulnerability researchers

### TIER 2: SPECIALIZED PROGRAMS

#### 5. Open Bug Bounty
- **URL**: https://openbugbounty.org
- **Type**: Coordinated disclosure with bounties
- **Scope**: Any website with owner consent
- **Rewards**: Varies by severity and website
- **Best For**: Web application vulnerabilities

#### 6. SSD Secure Disclosure
- **URL**: https://ssd-disclosure.com
- **Type**: Vulnerability acquisition
- **Focus**: Critical vulnerabilities in popular software
- **Best For**: High-impact vulnerabilities with broad reach

#### 7. Zero Day Initiative (ZDI)
- **URL**: https://zerodayinitiative.com
- **Type**: Vulnerability acquisition
- **Focus**: 0-day vulnerabilities in popular software
- **Rewards**: $500 - $250,000+ depending on impact
- **Best For**: Critical vulnerabilities in widely-used software

### TIER 3: GOVERNMENT & PUBLIC INTEREST

#### 8. CISA VDP Platform (USA)
- **URL**: https://www.cisa.gov/resources-tools/services/vulnerability-disclosure-policy-vdp-platform
- **Scope**: Federal civilian executive branch agencies
- **Focus**: Critical infrastructure vulnerabilities
- **Best For**: Infrastructure security researchers

#### 9. UK NCSC VDP
- **URL**: https://www.ncsc.gov.uk
- **Scope**: UK government systems
- **Focus**: National security vulnerabilities
- **Best For**: UK-based security researchers

#### 10. Singapore GovTech VDP
- **URL**: https://www.tech.gov.sg/report-vulnerability/
- **Scope**: Singapore government digital services
- **Focus**: Government e-services
- **Best For**: Singapore-based security researchers

---

## RESEARCH STRATEGY

### High-Value Targets for Digital Archaeology Approach

1. **Next.js and React Ecosystem**
   - Server Components, App Router, Middleware
   - Edge Runtime vulnerabilities
   - Hydration mismatches leading to XSS

2. **GitHub Actions Supply Chain**
   - Action marketplace vulnerabilities
   - Workflow injection attacks
   - Secret leakage in Actions

3. **Golang Standard Library**
   - Net/http vulnerabilities
   - Crypto package issues
   - Template injection

4. **Angular Framework**
   - Template injection
   - Sanitizer bypasses
   - Server-side rendering issues

5. **Nuclei Templates**
   - Template injection
   - Template sandbox escapes
   - Custom template vulnerabilities

### Old Code Analysis for Bug Bounty

1. **Pattern Matching in Old Code**
   - Buffer overflows in C/C++ projects
   - Integer overflow in size calculations
   - Use-after-free in complex data structures

2. **Race Conditions**
   - TOCTOU (Time of Check Time of Use) bugs
   - Double-free vulnerabilities
   - Memory corruption in concurrent code

3. **Logic Bugs**
   - Authentication bypass through state confusion
   - Authorization through parameter manipulation
   - Business logic flaws in payment processing

### Recommended Approach

1. Start with Vercel OSS (highest bounties, clear scope)
2. Focus on Next.js App Router (newest, most complex)
3. Look for hydration/mutation vulnerabilities
4. Document everything with PoC
5. Submit through HackerOne with detailed reports
