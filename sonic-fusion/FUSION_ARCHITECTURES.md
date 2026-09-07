# FUSION ARCHITECTURES
## How to Combine Multiple Open-Source Systems

---

## FUSION STRATEGY 1: CLI PIPELINE

The simplest integration: each component is a CLI tool, orchestrated by a Python script.

```bash
# Step 1: Generate MIDI
midi-gpt --prompt "uplifting pop chorus" --bars 8 --output chorus.mid

# Step 2: Render to audio
libsonare render --midi chorus.mid --instrument piano --output chorus.wav

# Step 3: Analyze
essentia_extract --input chorus.wav --output analysis.json

# Step 4: Separate if needed
demucs --two-stems vocals chorus.wav --out stems/

# Step 5: Mix
libsonare mix --stems drums.wav,bass.wav,piano.wav --output mix.wav

# Step 6: Master
libsonare mastering --input mix.wav --target-lufs -14 --output master.wav
```

**Pros**: Simple, each tool independent, easy to swap
**Cons**: File I/O overhead, no shared state, sequential

---

## FUSION STRATEGY 2: PYTHON LIBRARY

Import each component as a Python library.

```python
from sonic_fusion.core import MusicEngine
from sonic_fusion.components import (
    MIDIPTGenerator,
    LibsonareRenderer,
    DemucsSeparator,
    EssentiaAnalyzer,
    LibsonareMixer,
    LibsonareMasterer
)

engine = MusicEngine()

# Register components
engine.components["midi_generator"] = MIDIPTGenerator()
engine.components["audio_renderer"] = LibsonareRenderer()
engine.components["analyzer"] = EssentiaAnalyzer()
engine.components["mixer"] = LibsonareMixer()
engine.components["masterer"] = LibsonareMasterer()

# Run
project = engine.iterate(max_iterations=3)
```

**Pros**: Shared state, in-memory processing, Pythonic
**Cons**: All components must have Python bindings

---

## FUSION STRATEGY 3: MICROSERVICES

Each component runs as a separate service, communicating via REST/gRPC.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ MIDI Gen    │────▶│ Audio Render│────▶│ Analysis    │
│ (port 5001) │     │ (port 5002) │     │ (port 5003) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Orchestrator│
                    │ (port 8000) │
                    └─────────────┘
```

**Pros**: Language-independent, scalable, fault-tolerant
**Cons**: Network overhead, complex deployment

---

## FUSION STRATEGY 4: WASM MODULES

All components compiled to WebAssembly, running in browser or Node.js.

```
┌─────────────────────────────────────────────┐
│              Browser / Node.js              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ MIDI.wasm│  │ DSP.wasm│  │ MIR.wasm│    │
│  └────┬────┘  └────┬────┘  └────┬────┘    │
│       └─────────────┴─────────────┘         │
│                     │                       │
│              ┌──────▼──────┐                │
│              │ AudioWorklet│                │
│              └─────────────┘                │
└─────────────────────────────────────────────┘
```

**Pros**: Cross-platform, no install, runs anywhere
**Cons**: Limited by WASM capabilities, no GPU access

---

## RECOMMENDED FUSION: HYBRID

Use **Strategy 2 (Python Library)** as the primary interface, with **Strategy 1 (CLI)** as fallback for components without Python bindings.

```
Python API (primary)
    │
    ├──→ Python-native components (direct import)
    │     ├── MIDI-GPT (Python)
    │     ├── Essentia (Python bindings)
    │     └── Demucs (Python)
    │
    └──→ CLI components (subprocess)
          ├── Cadenza (Go binary)
          ├── libsonare (C++ binary)
          └── damp (C++ binary)
```

This gives us:
- Easy component swapping
- Both Python and CLI interfaces
- No WASM complexity
- No microservice overhead
