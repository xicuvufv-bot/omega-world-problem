# GITHUB COMPONENT ATLAS

## Discovered Projects and Their Capabilities

### TIER 1: Core Infrastructure

| Project | Capability | License | Stars | GameForge Usage |
|---------|-----------|---------|-------|----------------|
| `GameTechDev/PresentMon` | ETW frame time capture, GPU telemetry | MIT | 2.8k | Frame time measurement engine |
| `LibreHardwareMonitor/LibreHardwareMonitor` | Cross-vendor hardware sensors | MPL-2.0 | 4.5k | CPU/GPU temp, clock, usage monitoring |
| `aneeskhan47/fps-overlay` | ETW-based FPS overlay, anti-cheat safe | GPL-3.0 | 96 | Lightweight real-time FPS measurement |
| `barknq11/fps-monitor` | PresentMon + LibreHardwareMonitor overlay | MIT | 150 | Frame time graph + hardware sensor display |

### TIER 2: Game Detection & Library Management

| Project | Capability | License | Stars | GameForge Usage |
|---------|-----------|---------|-------|----------------|
| `bensheed/OpenGameBoost` | Game detection via process names | MIT | 50 | Process-based game detection engine |
| `lhceist41/GameShift` | ETW-based game detection, 80+ games | GPL-3.0 | 200 | Sub-millisecond game launch detection |
| `Segergren/Segra` | WMI + foreground hook game detection | MIT | 300 | Multi-strategy game detection |
| `FabioZumbi12/game-detector` | Steam/Epic library scanning | GPL-2.0 | 100 | Game library discovery |

### TIER 3: System Optimization

| Project | Capability | License | Stars | GameForge Usage |
|---------|-----------|---------|-------|----------------|
| `maxrenke/game-optimizer` | CPU affinity, process demotion, timer resolution | MIT | 300 | CPU core pinning engine |
| `mojouto3/mojo-gaming-mode` | 29 system tweaks, GPU vendor themes | MIT | 100 | System tweak library |
| `thisath111/ssm` | Rust-based kernel tuning daemon | GPL-3.0 | 50 | Deep system optimization patterns |
| `CRTYPUBG/ultimate-optimizer` | Hardware-aware Windows optimization | MIT | 80 | GPU-specific optimization UI |

### TIER 4: Configuration Management

| Project | Capability | License | Stars | GameForge Usage |
|---------|-----------|---------|-------|----------------|
| `CTOUT/ReFrame` | Game config parser, 26 game profiles | MIT | 100 | Config file analysis engine |
| `Game-Performance-Optimizer` | UE5 stutter fix, config management | MIT | 50 | UE5-specific optimization |

### TIER 5: Diagnostics & Analysis

| Project | Capability | License | Stars | GameForge Usage |
|---------|-----------|---------|-------|----------------|
| `nikicat/fpsdoctor` | GPU/CPU/thermal throttle verdict | MIT | 200 | Diagnostic verdict engine |
| `poli0981/FrameLedger` | Settings-aware performance ledger | GPL-3.0 | 80 | Historical performance tracking |
| `crased/paper_engine` | 6-source game analysis pipeline | MIT | 30 | Multi-source game analysis |

## Capability Mapping

```
PRESENTMON (frame times) + LIBREHARDWAREMONITOR (sensors)
          |
          v
    PERF_MONITOR (real-time analysis)
          |
          v
    STUTTER_ANALYZER (diagnosis)
          |
          v
    HARDWARE_DETECTOR (hardware tier classification)
          |
          v
    GAME_DETECTOR (running game identification)
          |
          v
    GAME_PROFILES (per-game optimization knowledge)
          |
          v
    SYSTEM_OPTIMIZER + CPU_OPTIMIZER + GPU_OPTIMIZER
          |
          v
    CONFIG_MANAGER (game config optimization)
          |
          v
    NETWORK_OPTIMIZER (latency reduction)
```
