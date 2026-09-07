# MUSIC CAPABILITY GRAPH
## How Components Connect in Sonic Fusion

---

## PIPELINE FLOW

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                               │
│  Genre │ Mood │ Tempo │ Key │ Chords │ Structure │ Instruments    │
│  Energy │ Dynamics │ Vocal Style │ Lyrics │ Length                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    1. IDEA LAYER                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ LLM      │  │ Song     │  │ Chord    │  │ Structure│          │
│  │ Composer │→ │ Structure│→ │ Progress.│→ │ Planner  │          │
│  │ (GPT/Claude) │ Generator │ │ Engine   │  │          │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│  Output: Musical Blueprint (JSON)                                   │
│  { key, tempo, time_sig, chords, sections, instruments, mood }     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    2. COMPOSITION LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ MIDI-GPT │  │ ACE-Step │  │ DiffRhyth│  │ PhraseLDM│          │
│  │ (multitrk)│ │ (full   │  │ (diffusn)│  │ (symbolic│          │
│  │           │  │  song)   │  │          │  │  music)  │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│                    ┌────▼────┐                                      │
│                    │ MIDI    │ ← Central interchange format         │
│                    │ Hub     │                                      │
│                    └────┬────┘                                      │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    3. ANALYSIS LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Essentia │  │ All-In-  │  │ MuQ/     │  │ sonara   │          │
│  │ (MIR)    │  │ One      │  │ MuLan    │  │ (Rust)   │          │
│  │          │  │ (struct) │  │ (embed)  │  │          │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│  Metrics: Tempo │ Key │ Chords │ Structure │ Loudness │ Balance    │
│  Output: Analysis Report + Weakness Detection                      │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    4. AUDIO GENERATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ libsonare│  │ Chord    │  │ web-     │  │ BELLOWS  │          │
│  │ (MIDI→   │  │ (Rust    │  │ synth    │  │ (browser │          │
│  │  audio)  │  │  synth)  │  │ (FM/VA)  │  │  synth)  │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│                    ┌────▼────┐                                      │
│                    │ Audio   │ ← Per-stem audio rendering           │
│                    │ Stems   │                                      │
│                    └────┬────┘                                      │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    5. VOCALS LAYER                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ DiffSinger│ │ TCSinger │  │ SoulX-   │  │ VocalRend│          │
│  │ (SVS)    │  │ (zero-   │  │ Singer   │  │ (score-  │          │
│  │          │  │  shot)   │  │          │  │  native) │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│  ┌─────┴────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐          │
│  │ YingMusic│  │ RVC      │  │ ACE-Step │  │ HeartMuLa│          │
│  │ -SVC     │  │ (voice   │  │ (vocal   │  │ (full    │          │
│  │ (convert)│  │  convert)│  │  track)  │  │  song)   │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    6. STEMS LAYER                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Demucs   │  │ Spleeter │  │ Open-    │  │ stem-    │          │
│  │ v4       │  │          │  │ Unmix    │  │ splitter │          │
│  │ (HT)     │  │          │  │          │  │ (Rust)   │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│  Output: Drums │ Bass │ Vocals │ Other │ (+ Guitar │ Piano)       │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    7. MIXING LAYER                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ libsonare│  │ Keel     │  │ DSPark   │  │ Voxis    │          │
│  │ (channel │  │ (auto-   │  │ (90+     │  │ (95      │          │
│  │  strip)  │  │  mix)    │  │  DSP)    │  │  effects)│          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│  Per-stem: EQ │ Compression │ Reverb │ Delay │ Saturation │ Pan    │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    8. MASTERING LAYER                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ libsonare│  │ damp     │  │ oXygen   │  │ Sovereign│          │
│  │ (76 DSP) │  │ (6 modes)│  │ (JUCE    │  │ -DSP     │          │
│  │          │  │          │  │  plugin) │  │          │          │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │              │              │                │
│        └────────────┴──────────────┴──────────────┘                │
│                         │                                          │
│  Chain: EQ → Dynamics → Multiband → Stereo → Limit → Dither       │
│  Target: -14 LUFS │ -1.0 dBTP │ Streaming-safe                    │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    9. EVALUATION LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Tempo    │  │ Key      │  │ Loudness │  │ Spectral │          │
│  │ Check    │  │ Check    │  │ Check    │  │ Check    │          │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤          │
│  │ Timing   │  │ Structure│  │ Stem     │  │ clipping │          │
│  │ Check    │  │ Check    │  │ Balance  │  │ Check    │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                     │
│  Output: Quality Score │ Weakness Report │ Suggestions             │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    10. ITERATION LOOP                               │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │  IF weaknesses detected:                                │       │
│  │    → Identify weak section (e.g., Chorus harmony weak)  │       │
│  │    → Keep strong parts (Verse melody, Bridge vocals)    │       │
│  │    → Regenerate ONLY weak section                       │       │
│  │    → Re-analyze                                          │       │
│  │    → Compare versions                                    │       │
│  │    → Keep best parts                                     │       │
│  │    → Loop until quality threshold met                    │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                     │
│  VERSION CONTROL: v001 → v002 → v003 → ... → FINAL                │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    11. EXPORT LAYER                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ WAV      │  │ MP3      │  │ Stems    │  │ MIDI     │          │
│  │ (24-bit) │  │ (320kbps)│  │ ZIP      │  │ (SMF)    │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                     │
│  Metadata: BPM │ Key │ LUFS │ True Peak │ Duration │ Structure    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## COMPONENT MAPPING

### For each stage, the BEST component:

| Stage | Primary | Fallback | Why |
|-------|---------|----------|-----|
| **Idea → Lyrics** | LLM (Claude/GPT) | - | Natural language |
| **Chords/Structure** | Cadenza (deterministic) | MIDI-GPT | Seed-based, reproducible |
| **MIDI Generation** | MIDI-GPT (multitrack) | Midra (editable) | DAW integration |
| **Full Song Gen** | ACE-Step 1.5 | HeartMuLa | Speed + quality + LoRA |
| **Audio Rendering** | libsonare (MIDI→audio) | Chord (WASM) | No samples needed |
| **Analysis** | Essentia + All-In-One | sonara (Rust) | Comprehensive MIR |
| **Singing** | DiffSinger (production) | TCSinger (zero-shot) | Proven, controllable |
| **Vocal Conversion** | YingMusic-SVC | RVC | Robust zero-shot |
| **Stem Separation** | Demucs v4 | stem-splitter-core | Gold standard |
| **Effects** | DSPark (90+) | Voxis (95) | Professional quality |
| **Mixing** | libsonare (channel strip) | Keel (auto) | Deterministic |
| **Mastering** | libsonare (76 DSP) | damp (6 engines) | Comprehensive |
| **Evaluation** | Essentia + custom | sonara | MIR metrics |

---

## SHARED STATE FORMAT

Every component reads/writes this JSON schema:

```json
{
  "project_id": "uuid",
  "version": "001",
  "created_at": "ISO8601",
  "blueprint": {
    "genre": "pop",
    "mood": "energetic",
    "tempo": 120,
    "key": "C major",
    "time_signature": "4/4",
    "chord_progression": ["C", "G", "Am", "F"],
    "structure": ["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"],
    "instruments": ["drums", "bass", "piano", "guitar", "vocals"],
    "energy": [0.3, 0.5, 0.8, 0.5, 0.8, 0.6, 0.9, 0.3],
    "vocal_style": "pop_female"
  },
  "stems": {
    "drums": "path/to/drums.wav",
    "bass": "path/to/bass.wav",
    "harmony": "path/to/harmony.wav",
    "melody": "path/to/melody.wav",
    "vocals": "path/to/vocals.wav",
    "fx": "path/to/fx.wav"
  },
  "midi": {
    "drums": "path/to/drums.mid",
    "bass": "path/to/bass.mid",
    "harmony": "path/to/harmony.mid",
    "melody": "path/to/melody.mid",
    "vocals": "path/to/vocals.mid"
  },
  "analysis": {
    "tempo_consistency": 0.95,
    "key_consistency": 0.98,
    "loudness_lufs": -14.0,
    "true_peak_dbtp": -1.0,
    "structural_coherence": 0.87,
    "stem_balance": { "drums": 0.8, "bass": 0.7, "vocals": 0.9 },
    "weaknesses": ["chorus_harmony_sparse", "bridge_too_short"]
  },
  "versions": ["001", "002", "003"],
  "current_version": "003"
}
```

---

## DATA FLOW BETWEEN COMPONENTS

```
Blueprint (JSON) ──→ MIDI Generation ──→ MIDI Files
                        │
                        ├──→ Audio Rendering ──→ WAV Stems
                        │
                        ├──→ Analysis ──→ Quality Report
                        │
                        └──→ Vocal Synthesis ──→ Vocal Stems

WAV Stems ──→ Stem Separation (if needed) ──→ Individual Stems
                │
                ├──→ Mixing ──→ Stereo Mix
                │
                ├──→ Mastering ──→ Final Master
                │
                └──→ Evaluation ──→ Version Decision

Quality Report ──→ Iteration Engine ──→ Regenerate Weak Parts
                        │
                        └──→ New Version ──→ Re-analyze ──→ Loop
```
