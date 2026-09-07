# TOP_3_PROTOTYPES.md — Built Prototypes

## Prototype 1: VoiceStack (WINNER)

**Status:** Scaffold Complete
**Location:** PROTOTYPES/voicestack/

### What's Built
- Core agent orchestration logic (`core/agent.py`)
- FastAPI REST API server (`core/server.py`)
- Voice service (ASR/TTS) scaffold (`voice/server.py`)
- Docker Compose full-stack deployment
- Configuration system
- Knowledge retrieval integration
- Workflow execution integration

### What's NOT Built Yet
- Actual VibeVoice model integration (needs GPU)
- Dograh voice platform integration
- Conductor workflow definitions
- Web UI dashboard
- Telephony integration (Twilio)
- Real testing

### How to Test
```bash
cd PROTOTYPES/voicestack
docker compose up -d
curl http://localhost:8000/health
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"test","name":"Test Agent","system_prompt":"You are a helpful assistant."}'
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"test","message":"Hello, who are you?"}'
```

---

## Prototype 2: DocuVideo (Planned)

**Status:** Not Built
**Components:** Knowhere + OpenMontage + VibeVoice
**Concept:** Upload documents → AI generates training videos

---

## Prototype 3: SupportAI (Planned)

**Status:** Not Built
**Components:** DeerFlow + Knowhere + Browser Use
**Concept:** AI handles complete customer support tickets
