# VoiceStack — Self-Hosted Voice Agent Platform

> Voice AI agents that know your business and take action. Self-hosted. Private. 10x cheaper than cloud.

## What is VoiceStack?

VoiceStack is an open-source, self-hosted voice agent platform that combines:
- **Voice AI** — Natural voice conversations via phone, web, or WhatsApp
- **Knowledge Base** — Agents that understand your documents and data
- **Workflow Automation** — Agents that take actions in your systems

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    VoiceStack                        │
├─────────────────────────────────────────────────────┤
│  Voice Layer (Dograh + VibeVoice)                   │
│  ├── Phone (Twilio/Vonage)                          │
│  ├── Web (WebSocket)                                │
│  ├── WhatsApp                                       │
│  └── Telegram                                       │
├─────────────────────────────────────────────────────┤
│  Intelligence Layer (LLM + Knowledge)               │
│  ├── LLM Provider (OpenAI/Anthropic/Local)          │
│  ├── Knowhere (Document Memory)                     │
│  └── Vector Search + Knowledge Graph                │
├─────────────────────────────────────────────────────┤
│  Action Layer (Conductor Workflows)                 │
│  ├── CRM Integration                                │
│  ├── Ticket Creation                                │
│  ├── Data Lookup                                    │
│  └── Custom Actions                                 │
├─────────────────────────────────────────────────────┤
│  Infrastructure                                     │
│  ├── PostgreSQL (Metadata)                          │
│  ├── Redis (Cache/Sessions)                         │
│  ├── Qdrant (Vectors)                               │
│  └── Docker Compose                                 │
└─────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/voicestack.git
cd voicestack

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start the platform
docker compose up -d

# Access the dashboard
open http://localhost:3000
```

## Components Used

| Component | Source | License | Purpose |
|-----------|--------|---------|---------|
| Dograh | github.com/dograh-hq/dograh | BSD-2 | Voice agent platform |
| VibeVoice | github.com/microsoft/VibeVoice | MIT | ASR + TTS models |
| Knowhere | github.com/Ontos-AI/knowhere | Apache-2.0 | Document memory |
| Conductor | github.com/conductor-oss/conductor | Apache-2.0 | Workflow engine |

## License

MIT License — use freely, modify freely, deploy freely.
