# FORGOTTEN CAPABILITIES

## Hidden Technical Leverage in Abandoned Projects

---

## AUDIO CAPABILITIES

### 1. Spectral Sound Morphing (Loris)
**What:** Transform one sound into another by morphing their spectral components
**Forgotten Since:** 2015
**Modern Use:** Music production, sound design, film post-production
**Why Valuable:** No commercial tool offers this at scale

### 2. Non-Stationary Noise Reduction (noisereduce)
**What:** Remove noise without a noise sample, adapting to changing conditions
**Forgotten Since:** 2022 (research project ended)
**Modern Use:** Podcast cleaning, field recording, call centers
**Why Valuable:** Unique algorithm, no competitor does this without noise sample

### 3. 8 Pitch Detection Algorithms (audioFlux)
**What:** YIN, CEP, PEF, NCF, HPS, LHS, STFT, FFP — all in one library
**Forgotten Since:** 2024 (development stalled)
**Modern Use:** Music education, tuning apps, audio analysis
**Why Valuable:** librosa only has 2 algorithms, this has 8

### 4. Phase-Based Onset Detection (audioFlux)
**What:** PD, WPD, NWPD, CD, RCD — phase derivative features for onset detection
**Forgotten Since:** 2024
**Modern Use:** Music information retrieval, beat tracking
**Why Valuable:** More accurate than spectral flux for percussive content

### 5. Non-Stationary Gabor Transform (audioFlux)
**What:** NSGT — time-frequency transform for non-stationary signals
**Forgotten Since:** 2024
**Modern Use:** Bioacoustics, speech analysis, vibration monitoring
**Why Valuable:** Better than STFT for transient-rich signals

---

## COMPUTER VISION CAPABILITIES

### 6. Photo Restoration with Face Enhancement (Bringing Old Photos Back to Life)
**What:** Remove scratches, restore color, enhance faces from heavily degraded photos
**Forgotten Since:** 2022 (research moved on)
**Modern Use:** Photo restoration services, genealogy, archival
**Why Valuable:** 15.7K stars, MIT license, no commercial service built on it

### 7. Facial Action Unit Detection (OpenFace)
**What:** Detect 17 facial muscle movements (AU1-AU46) from webcam
**Forgotten Since:** 2018 (OpenFace 2.0 superseded)
**Modern Use:** Telehealth emotion analysis, UX research, lie detection
**Why Valuable:** Still the best AU implementation, used in clinical psychology

### 8. Stroke Width Transform (ccv)
**What:** Detect text in natural scenes using stroke width analysis
**Forgotten Since:** Never gained traction (OpenCV dominance)
**Modern Use:** Document scanning, AR translation, autonomous driving
**Why Valuable:** Works where deep learning fails (small text, unusual fonts)

### 9. GrabCut in One Cut (OneCut)
**What:** Interactive image segmentation in single iteration (vs GrabCut's multiple)
**Forgotten Since:** 2014 (no Python port)
**Modern Use:** Real-time interactive segmentation on embedded devices
**Why Valuable:** Mathematical guarantee on solution quality

### 10. Sinusoidal Partial Editing (SPEAR)
**What:** Visually edit individual frequency components of sounds
**Forgotten Since:** Desktop-only, never web-ported
**Modern Use:** Music production, sound design, audio forensics
**Why Valuable:** No web-based equivalent exists

---

## SEARCH CAPABILITIES

### 11. Probabilistic Search (Xapian)
**What:** Search engine using probability theory instead of vector space
**Forgotten Since:** 2000 (overshadowed by Lucene/Elasticsearch)
**Modern Use:** Email filtering, document retrieval
**Why Valuable:** Different ranking approach can outperform BM25 in some cases

### 12. Trigram Code Search (Zoekt)
**What:** Sub-millisecond code search using trigram indexing
**Forgotten Since:** 2022 (moved to Sourcegraph)
**Modern Use:** Code intelligence, IDE search
**Why Valuable:** Faster than traditional inverted indexes for code

### 13. In-Memory Client-Side Search (MiniSearch)
**What:** Zero-dependency search engine for browser and Node.js
**Forgotten Since:** Never gained traction (Elasticsearch dominance)
**Modern Use:** Static site search, offline apps
**Why Valuable:** No server needed, instant results

---

## DATA CAPABILITIES

### 14. Lossless JPEG Compression (Lepton)
**What:** 22% lossless JPEG compression using adaptive arithmetic coding
**Forgotten Since:** 2023 (Dropbox deprecated)
**Modern Use:** Cloud storage optimization, image CDNs
**Why Valuable:** Battle-tested at Dropbox scale, no API service exists

### 15. Immutable Key-Value Store (CDB)
**What:** O(1) lookups with atomic rebuilds, append-only design
**Forgotten Since:** 2000s (overshadowed by Redis/MongoDB)
**Modern Use:** DNS servers, configuration stores, immutable data
**Why Valuable:** Perfect for write-once-read-many workloads

### 16. Real-Time Streaming Charts (Epoch.js)
**What:** Dual-mode charting with smooth real-time updates
**Forgotten Since:** 2019 (Fastly stopped maintaining)
**Modern Use:** IoT dashboards, monitoring, live data visualization
**Why Valuable:** Still one of the few libraries with true streaming support

---

## AUTOMATION CAPABILITIES

### 17. Natural Language RPA Syntax (TagUI)
**What:** "click button", "type name as John" — plain English automation
**Forgotten Since:** 2020 (AI Singapore discontinued)
**Modern Use:** Business process automation, testing
**Why Valuable:** LLM can now replace the rigid PHP parser

### 18. Go-Native Cross-Platform RPA (RobotGo)
**What:** Mouse/keyboard/screen/window control in pure Go
**Forgotten Since:** Semi-maintained (sporadic updates)
**Modern Use:** Enterprise desktop automation, testing
**Why Valuable:** Only Go-native RPA with Wayland support

### 19. Desktop App Automation (Nightmare)
**What:** Chainable browser + Electron automation
**Forgotten Since:** 2017 (Segment archived it)
**Modern Use:** Electron app testing, desktop RPA
**Why Valuable:** Electron support is unique

### 20. Visual Regression Testing (PhantomCSS)
**What:** Pixel-perfect screenshot diffing for CSS changes
**Forgotten Since:** 2014 (PhantomJS died)
**Modern Use:** Frontend testing, design QA
**Why Valuable:** Modern Playwright + perceptual hashing would revive this

---

## NETWORKING CAPABILITIES

### 21. Multi-Protocol Proxy (3proxy)
**What:** HTTP/HTTPS, SOCKS4/5, FTP, POP3, SMTP, DNS — all in one
**Forgotten Since:** Never gained mainstream adoption
**Modern Use:** IoT gateway, legacy protocol bridging
**Why Valuable:** Single binary handles everything

### 22. Language-Agnostic Web Server (Mongrel2)
**What:** Routes HTTP/WebSocket to any backend via ZeroMQ
**Forgotten Since:** 2021 (stable but unmaintained)
**Modern Use:** Polyglot microservice gateway
**Why Valuable:** Connection ID routing enables stateful WebSocket clusters

### 23. Self-Healing P2P VPN (Tinc)
**What:** Mesh VPN that auto-discovers peers and heals connections
**Forgotten Since:** Never gained mainstream adoption
**Modern Use:** Decentralized networking, IoT VPN
**Why Valuable:** Zero infrastructure needed

---

## COMPILER CAPABILITIES

### 24. 2-File Parser Generator (Lemon)
**What:** Powers SQLite, thread-safe, reentrant, public domain
**Forgotten Since:** Known only to SQLite developers
**Modern Use:** Embedded systems parsing, DSL creation
**Why Valuable:** Most-deployed parser generator nobody's heard of

### 25. Multi-Language PEG Parser (Canopy)
**What:** Generates parsers for Java, JS, Python, Ruby from one grammar
**Forgotten Since:** 2010 (overshadowed by PEG.js/Ohm.js)
**Modern Use:** Cross-language parser generation
**Why Valuable:** Still works, generates zero-dependency parsers

---

## THE PATTERN

**Forgotten capabilities fall into 3 categories:**

1. **Technically Superior, Ecosystem Loser**
   - audioFlux (faster than librosa)
   - Xapian (different approach than Lucene)
   - Lemon (powers SQLite, nobody knows)

2. **Research Prototype, Never Productized**
   - Bringing Old Photos Back to Life
   - OpenFace
   - OneCut

3. **Working Tool, Dead Runtime**
   - PhantomCSS (PhantomJS died)
   - Nightmare (Electron focus shifted)
   - dsp.js (Web Audio API replaced it)

**The money is in category 1: take the superior technology and wrap it in modern infrastructure.**
