# LICENSE AUDIT
## Comprehensive License Analysis for Sonic Fusion Components

---

## TIER 1: FULLY PERMISSIVE (Apache 2.0 / MIT / BSD)

| Component | License | Commercial | Redistribution | Modification | Attribution |
|-----------|---------|------------|----------------|--------------|-------------|
| ACE-Step 1.5 | Apache 2.0 | YES | YES | YES | YES |
| HeartMuLa | Apache 2.0 | YES | YES | YES | YES |
| SongGeneration/LeVo 2 | Apache 2.0 | YES | YES | YES | YES |
| DiffRhythm | Apache 2.0 | YES | YES | YES | YES |
| Demucs v4 | MIT | YES | YES | YES | YES |
| Spleeter | MIT | YES | YES | YES | YES |
| Open-Unmix | MIT | YES | YES | YES | YES |
| DiffSinger (OpenVPI) | Apache 2.0 | YES | YES | YES | YES |
| TCSinger | MIT | YES | YES | YES | YES |
| TCSinger 2 | MIT | YES | YES | YES | YES |
| YingMusic-Singer | MIT | YES | YES | YES | YES |
| YingMusic-SVC | MIT | YES | YES | YES | YES |
| MIDI-GPT | MIT | YES | YES | YES | YES |
| Cadenza | MIT | YES | YES | YES | YES |
| MERIT | MIT | YES | YES | YES | YES |
| libsonare | Apache 2.0 | YES | YES | YES | YES |
| VocalRender | Apache 2.0 | YES | YES | YES | YES |
| SoulX-Singer | Apache 2.0 | YES | YES | YES | YES |
| Keel (engine) | AGPL-3.0 | With copyleft | YES | YES | YES |
| DSPark | Free (attribution) | YES | YES | YES | Appreciated |
| Basic Pitch | Apache 2.0 | YES | YES | YES | YES |

## TIER 2: COPYLEFT (GPL / AGPL)

| Component | License | Commercial OK? | Requirements |
|-----------|---------|----------------|--------------|
| Essentia | AGPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| MAGDA | GPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| ACE-Step DAW | AGPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| OpenStudio | GPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| damp | AGPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| Keel | AGPL-3.0 | YES (with copyleft) | Source must be open if distributed |
| Qtractor | GPL-2.0 | YES (with copyleft) | Source must be open if distributed |
| UtaiSynthesizer | AGPL-3.0 | YES (with copyleft) | Source must be open if distributed |

## TIER 3: RESTRICTIVE

| Component | License | Issue | Can Use? |
|-----------|---------|-------|----------|
| Shao | CC-BY-NC 4.0 | No commercial use | Research only |
| MIDI-LLM | Other (NOASSERTION) | Unclear | Needs verification |
| web-synth | Other | Unclear | Needs verification |
| PhraseLDM | Apache 2.0 | OK | YES |

---

## RECOMMENDED LICENSING STRATEGY

### For Sonic Fusion:

1. **Core Engine**: Apache 2.0 (allows commercial use, clear terms)
2. **AI Models**: Apache 2.0 (most foundation models already use this)
3. **DSP Components**: Apache 2.0 or MIT (most are permissive)
4. **DAW Integration**: GPL-3.0 compatible (if using MAGDA/ACE-Step DAW)

### Critical Rules:
- NEVER include CC-BY-NC code in commercial paths
- AGPL components must be in separate network-callable services OR
- Build the core without AGPL dependencies
- MIT/Apache 2.0 components are safe for all uses

### Safe Stack (All Apache 2.0/MIT):
```
Generation:    ACE-Step 1.5 (Apache 2.0)
MIDI:          MIDI-GPT (MIT), Cadenza (MIT)
Separation:    Demucs v4 (MIT)
Vocals:        DiffSinger (Apache 2.0), TCSinger (MIT)
Analysis:      sonara (free), MERIT (MIT)
DSP:           DSPark (free), libsonare (Apache 2.0)
Mixing:        libsonare (Apache 2.0)
Mastering:     libsonare (Apache 2.0), Keel (AGPL - service only)
```
