# AUDIO COMPONENT DATABASE
## Detailed Technical Specifications

---

## 1. STEM SEPARATION

### Demucs v4 (Meta Research)
- **Repo**: facebookresearch/demucs (10,360 stars)
- **License**: MIT
- **Architecture**: Hybrid Transformer (spectrogram + waveform)
- **Models**: htdemucs, htdemucs_ft, htdemucs_6s, mdx, mdx_extra
- **Quality**: SDR 9.00-9.20 dB on MUSDB HQ
- **Stems**: 4 (vocals, drums, bass, other) or 6 (+guitar, +piano)
- **Training**: MUSDB HQ + 800 extra songs
- **Speed**: Real-time on GPU
- **Dependencies**: Python, PyTorch, torchaudio
- **Integration**: CLI `demucs --two-stems=vocals input.wav`

### stem-splitter-core (Rust)
- **Repo**: gentij/stem-splitter-core (23 stars)
- **License**: Other
- **Architecture**: ONNX Runtime (htdemucs model)
- **Stems**: 4 (drums, bass, other, vocals)
- **GPU**: CUDA, CoreML, DirectML, oneDNN, XNNPACK
- **Model Size**: ~200MB
- **Formats**: WAV, MP3, FLAC, OGG, AAC
- **Advantage**: No Python dependency

---

## 2. MIDI GENERATION

### MIDI-GPT (Metacreation Lab)
- **Repo**: Metacreation-Lab/MIDI-GPT (74 stars)
- **License**: MIT
- **Architecture**: GPT-2 transformer
- **Models**: yellow (4-8 bars), ghost (4-16 bars), expressive
- **Control**: Note density, polyphony (min/max), note duration
- **Infill**: Fill missing bars while preserving arrangement
- **OSC Server**: Real-time DAW integration via UDP
- **Python**: 3.10-3.12, pre-built wheels

### Cadenza
- **Repo**: Andrea-Cavallo/cadenza (9 stars)
- **License**: MIT
- **Language**: Go (static binary, CGO disabled)
- **Offline Mode**: 7 stems (bass-groove, bass-rolling, bass-sub, arp, melody, pad, lead)
- **LLM Mode**: 3 stems (bass, arp, melody) via Claude/Ollama/OpenAI/Gemini
- **Deterministic**: Seed-based, same seed = same output
- **Validation**: Scale membership, range, density, chord-tone ratios
- **Desktop**: Wails v2 (piano-roll preview)

### Midra
- **Repo**: XIAODUOLU/Midra (58 stars)
- **License**: Apache 2.0
- **Approach**: Agentic prompt-to-code → MIDI
- **Pipeline**: Intent → Song → Arrangement → Note planning → MIDI rendering
- **Checkpoint**: JSON files at each stage
- **Output**: Inspectable, modifiable MIDI files

---

## 3. MUSIC GENERATION (Full Song)

### ACE-Step 1.5
- **Repo**: ace-step/ACE-Step-1.5
- **License**: Apache 2.0
- **Architecture**: Chain-of-Thought DiT + LM
- **Speed**: <2s per song (A100), <10s (RTX 3090)
- **VRAM**: 4-24GB (configurable LM size)
- **Duration**: 10s to 10min
- **Languages**: 50+ with lyrics
- **Features**: Cover gen, repaint, track separation, vocal2BGM, LoRA training
- **LM Models**: 0.6B, 1.7B, 4B (Qwen3-based)

### HeartMuLa
- **Repo**: HeartMuLa/heartlib (3,802 stars)
- **License**: Apache 2.0
- **Components**: HeartMuLa (music LLM), HeartCodec (12.5Hz codec), HeartTranscriptor (lyrics), HeartCLAP (text-music alignment)
- **Size**: 3B / 7B
- **Quality**: Comparable to Suno
- **Speed**: RTF ≈ 1.0

### SongGeneration/LeVo 2
- **Repo**: tencent-ailab/SongGeneration
- **License**: Apache 2.0
- **Size**: 4B params
- **PER**: 8.55% (better than Suno v5's 12.4%)
- **Features**: Dual-track (vocals + accompaniment separate)
- **Languages**: Multi-lingual

---

## 4. SINGING VOICE SYNTHESIS

### DiffSinger (OpenVPI maintained)
- **Repo**: openvpi/DiffSinger (3,189 stars)
- **License**: Apache 2.0
- **Architecture**: Shallow diffusion mechanism
- **Sample Rate**: 44.1 kHz (improved from original 24 kHz)
- **Features**: Variance models for pitch, energy, breathiness control
- **Input**: MIDI + lyrics (phoneme-aligned)
- **Deployment**: OpenUTAU integration
- **Acceleration**: PNDM, DPM-Solver++, UniPC

### TCSinger 2
- **Repo**: AaronZ345/TCSinger2
- **License**: MIT
- **Architecture**: Blurred Boundary Content Encoder + Custom Audio Encoder (contrastive) + Flow-based Custom Transformer with Cus-MOE
- **Control**: F0 + style transfer + multi-level style control
- **Languages**: Multilingual
- **Zero-shot**: Yes, no fine-tuning needed

### VocalRender
- **Repo**: pymaster17/VocalRender (104 stars)
- **License**: Apache 2.0
- **Input**: Word/pitch/note interleaved score (no duration needed)
- **Architecture**: AR Transformer + LocDiT + VAE decoder
- **Output**: 48 kHz audio
- **Innovation**: Score-native, no phoneme alignment required

---

## 5. AUDIO DSP / EFFECTS

### DSPark
- **Repo**: CristianMoresi/DSPark
- **License**: Free (attribution appreciated)
- **Architecture**: Header-only C++20, zero dependencies
- **Processors**: 90+ (36 effects, 8 analyzers, 16+ dynamics, etc.)
- **Plugins**: Native VST3, CLAP, AU (no JUCE required)
- **Analysis**: EBU R128 loudness (passes official test vectors)
- **Effects**: AlgorithmicReverb (6 presets), Saturation (10 algorithms), PitchDetector (YIN), etc.
- **Platforms**: Windows, Linux, macOS, WASM, iOS, Android

### libsonare
- **Repo**: libraz/libsonare
- **License**: Apache 2.0
- **Architecture**: C++ engine, WASM + AudioWorklet
- **Mastering**: 76 named DSP processors
- **Mixing**: Channel-strip/bus model (lock-free, denormal-guarded)
- **Instruments**: NativeSynth (7 synthesis engines), SF2/GS player (16-part)
- **Analysis**: BPM, key, chords (HMM), beat/downbeat, sections, loudness
- **Headless DAW**: Audio/MIDI tracks, clips, warping, offline bounce

### Keel
- **Repo**: fcarvajalbrown/Keel
- **License**: AGPL-3.0
- **Language**: Python
- **Pipeline**: Stems → loudness-balance → sum → master
- **Mastering**: 4x oversampled true-peak limiter, BS.1770-4
- **Default**: -14 LUFS / -1.0 dBTP
- **Deterministic**: Same stems in → same master out
- **Front-ends**: CLI, GUI app, VST3/AU plugin

---

## 6. MUSIC ANALYSIS

### Essentia
- **Repo**: MTG/essentia (3,602 stars)
- **License**: AGPL-3.0
- **Language**: C++ with Python bindings
- **Algorithms**: 500+ (spectral, temporal, tonal, high-level)
- **Descriptors**: Key, chords, BPM, loudness, timbre, mood, genre
- **Vamp Plugin**: For Sonic Visualiser

### All-In-One-Infer
- **Repo**: openmirlab/all-in-one-infer
- **License**: Other
- **Input**: Audio file
- **Output**: Tempo, beats, downbeats, segment boundaries, segment labels (intro/verse/chorus/bridge/outro)
- **Models**: harmonix-all (8-fold ensemble)
- **Dependencies**: demucs-infer (separation), madmom-infer (spectrogram/beat decoding)
- **Install**: `pip install all-in-one-infer`

### sonara (Rust)
- **Repo**: kkollsga/sonara
- **Language**: Rust with Python bindings
- **Modes**: compact (11 features, ~1.2ms), playlist (30+, ~4ms), full (~50ms)
- **Features**: 100+ analysis functions
- **Similarity**: 48-dim embedding (MFCC + chroma + spectral + rhythm + dynamics)
- **Perceptual**: LUFS, energy, danceability, key, valence, acousticness
