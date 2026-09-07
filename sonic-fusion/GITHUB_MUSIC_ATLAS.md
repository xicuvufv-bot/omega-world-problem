# GITHUB MUSIC ATLAS
## Complete Open-Source Music Technology Landscape (2025-2026)

---

## 1. MUSIC GENERATION (Full Song)

| Project | Stars | License | What It Does | Quality | Limitations |
|---------|-------|---------|--------------|---------|-------------|
| **HeartMuLa** | 3802 | Apache 2.0 | Music language model, lyrics+tags → full song. 3B/7B params. Comparable to Suno. | Very High | RTF≈1.0, needs GPU |
| **ACE-Step 1.5** | ~500+ | Apache 2.0 | DiT + CoT LM. Full song in <2s on A100. 50+ languages. LoRA support. | Very High | 4-24GB VRAM |
| **SongGeneration/LeVo 2** | ~200+ | Apache 2.0 | 4B params. PER 8.55%. Multi-lingual. Dual-track output. | Very High | 22-28GB VRAM |
| **DiffRhythm** | 2305 | Apache 2.0 | Diffusion-based. Full-length 285s songs. Fast. | High | Less controllable |
| **MiniMax Music 3** | 98 | Unknown | 8B Global + 0.6B Local LLM. 5min songs. Flow Matching. | Very High | Needs 2 GPUs |
| **Shao** | ~100+ | CC-BY-NC 4.0 | Acoustic-token pipeline. 64-layer RVQ. Complete system. | Very High | GPU sensitive, NC license |

## 2. MIDI GENERATION

| Project | Stars | License | What It Does | Strengths |
|---------|-------|---------|--------------|-----------|
| **MIDI-GPT** | 74 | MIT | GPT-2 multitrack. DAW OSC integration. Control note density/polyphony. | DAW integration, controllable |
| **MIDI-LLM** | 120 | Other | Llama 3.2 1B → MIDI. NeurIPS AI4Music. | Research quality, vLLM support |
| **Midra** | 58 | Apache 2.0 | Agentic prompt-to-code MIDI. Checkpoint JSON. Editable MIDI. | Inspectable, resumable |
| **Cadenza** | 9 | MIT | Go. BPM+Key → 3-7 MIDI stems. Deterministic. | Fast, seed-based, offline mode |
| **Conductr** | 52 | Apache 2.0 | Browser. Real-time MIDI. C Engine (WASM) + AI Director. | Real-time, WebMIDI |
| **PhraseLDM** | 25 | Apache 2.0 | Latent diffusion for full-song multitrack symbolic music. | Full-song structure |

## 3. STEM SEPARATION / SOURCE SEPARATION

| Project | Stars | License | What It Does | Quality |
|---------|-------|---------|--------------|---------|
| **Demucs (v4)** | 10360 | MIT | Hybrid Transformer. 4/6 stems. SDR 9.20 dB. | Gold Standard |
| **Spleeter** | 28414 | MIT | Deezer. 2/4/5 stems. Fast. | Good, fast |
| **Open-Unmix** | 1491 | MIT | PyTorch reference. 4 stems. | Good baseline |
| **ZeroSep** | ~50+ | Unknown | Zero-shot. Text-guided diffusion. Any sound. | Novel, flexible |
| **GuideSep** | ~30+ | Unknown | User-guided. Humming input. Diffusion-based. | Flexible |
| **stem-splitter-core** | 23 | Other | Pure Rust. ONNX. GPU acceleration. | Fast, no Python |

## 4. SINGING VOICE SYNTHESIS

| Project | Stars | License | What It Does | Languages |
|---------|-------|---------|--------------|-----------|
| **DiffSinger** | 3189 (fork) | Apache 2.0 | SVS via shallow diffusion. Production-ready. | Chinese, English |
| **DiffSinger (original)** | 4829 | MIT | AAAI 2022. Foundation for SVS. | Chinese, English |
| **TCSinger** | 386 | MIT | Zero-shot SVS. Style transfer + control. | Multilingual |
| **TCSinger 2** | ~100+ | MIT | ACL 2025. Custom audio encoder. Cus-MOE. | Multilingual |
| **YingMusic-Singer** | 74 | MIT | Zero-shot SVS. Annotation-free melody. | Chinese, English |
| **SoulX-Singer** | ~50+ | Apache 2.0 | Zero-shot. F0/MIDI control. 42K hours. | Chinese, English, Cantonese |
| **VocalRender** | 104 | Apache 2.0 | Score-native SVS. AR diffusion. | Any language |

## 5. SINGING VOICE CONVERSION

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **YingMusic-SVC** | 157 | MIT | Zero-shot SVC. Flow-GRPO. RVC timbre shifter. |
| **SoulX-Singer-SVC** | (part of SoulX) | Apache 2.0 | Audio-to-audio SVC. No transcription needed. |
| **UtaiSynthesizer** | 25 | AGPL-3.0 | Full DAW. Piano-roll → SVC. RVC + So-VITS-SVC. |

## 6. AUDIO ANALYSIS / MIR

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **Essentia** | 3602 | AGPL-3.0 | C++ library. 500+ algorithms. Python bindings. |
| **All-In-One-Infer** | 23+ | Other | Tempo, beats, downbeats, structure segments. |
| **MOSS-Music** | ~100+ | Unknown | 8B model. Captioning, lyrics ASR, chords, key, structure. |
| **MuQ** | ~200+ | Unknown | Self-supervised music SSL. SOTA on MIR tasks. |
| **MuQ-MuLan** | (part of MuQ) | Unknown | Music-text joint embedding. CLIP-like. |
| **MERIT** | 28 | MIT | Disentangled melody/rhythm/timbre similarity. |
| **mir-feature-extraction** | ~20 | Unknown | 97+ MIR features. Stable Audio conditioning. |
| **sonara** | 2 | Unknown | Rust. 100+ analysis functions. 48-dim similarity. |

## 7. AUDIO DSP / EFFECTS

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **DSPark** | ~50+ | Free | C++20 header-only. 90+ processors. VST3/CLAP/AU. |
| **libsonare** | ~100+ | Apache 2.0 | C++ engine. 76 mastering DSP. WASM. Headless DAW. |
| **Voxis** | ~20 | Unknown | Python+C++. 95 chainable effects. Browser realtime. |
| **damp** | ~30+ | AGPL-3.0 | C++ mastering. 6 engines. 38 presets. |
| **Keel** | 1 | AGPL-3.0 | Python. Deterministic automix + automaster. |
| **oXygen** | ~20+ | BSD-3 | JUCE. Mastering plugin. Auto assistant. |

## 8. SYNTHESIS / INSTRUMENTS

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **Chord** | ~50+ | Unknown | Rust/WASM. 47 node types. 6 sequencers. Real-time. |
| **web-synth** | 565 | Other | Browser DAW. FM synth. Faust/Soul dynamic compilation. |
| **SuperSonic** | 205 | GPL/GPL | SuperCollider scsynth as WASM AudioWorklet. |
| **zaltz** | 8 | AGPL-3.0 | 165KB WASM. Zero-glitch. Strudel-compatible. |
| **BELLOWS** | ~10+ | Unknown | Browser. VA/FM/additive/wavetable/granular/KS. EBU R128. |

## 9. DAW COMPONENTS

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **MAGDA** | 151 | GPL-3.0 | Open DAW with AI. JUCE + Tracktion. DSL commands. |
| **ACE-Step DAW** | 76 | AGPL-3.0 | Browser DAW. 5 track types. Strudel live code. |
| **OpenStudio** | 61 | GPL-3.0 | Browser+Desktop. AI Agent. Web Audio. |
| **OpenDaw** | ~30+ | Unknown | Qt 6 + Tracktion. VST3. Claude AI assistant. |
| **YAWN** | 3 | MIT | Ableton-like. C++17. 23 effects. 15 instruments. |
| **Qtractor** | 594 | GPL-2.0 | Linux. JACK + ALSA. Mature multi-track. |

## 10. LYRICS / TRANSCRIPTION

| Project | Stars | License | What It Does |
|---------|-------|---------|--------------|
| **HeartTranscriptor** | (part of HeartMuLa) | Apache 2.0 | Whisper-based lyrics transcription. |
| **MOSS-Music** | ~100+ | Unknown | Lyrics ASR. 15.88% avg WER/CER. |
| **Basic Pitch** | ~200+ | Apache 2.0 | Spotify. Audio → MIDI (polyphonic). |

---

## LICENSE DISTRIBUTION SUMMARY

| License | Count | Commercial OK? |
|---------|-------|----------------|
| Apache 2.0 | ~15 | YES |
| MIT | ~12 | YES |
| GPL-3.0 / AGPL-3.0 | ~8 | YES (with copyleft) |
| BSD-3 | ~2 | YES |
| CC-BY-NC 4.0 | 1 | NO (commercial) |

## KEY FINDING: THE GAP

**No existing open-source system provides:**
1. Stem-first architecture with per-stem generation/editing/replacement
2. Iterative music creation loop (generate → analyze → edit → regenerate weak parts)
3. Version control for music projects
4. True DAW + AI integration without compromise
5. User-controllable arrangement, structure, and mixing at every stage

**This is our opportunity.**
