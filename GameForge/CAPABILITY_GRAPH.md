# CAPABILITY GRAPH

## How Components Connect to Form Emergent Capabilities

```
                    HARDWARE_DETECTOR
                    [CPU/GPU/RAM/Storage]
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
     GPU_OPTIMIZER    CPU_OPTIMIZER   STORAGE_CHECK
     [Upscaler]      [P-core pin]    [NVMe vs HDD]
            |              |              |
            +------+-------+------+-------+
                   |              |
                   v              v
            GAME_DETECTOR    PERF_MONITOR
            [Process scan]   [Frame times]
                   |              |
                   v              v
            GAME_PROFILES   STUTTER_ANALYZER
            [Engine issues] [Root cause]
                   |              |
                   +------+-------+
                          |
                          v
                  CONFIG_MANAGER
                  [Backup/Optimize/Rollback]
                          |
                          v
                  SYSTEM_OPTIMIZER
                  [Power/Services/Tweaks]
                          |
                          v
                  NETWORK_OPTIMIZER
                  [DNS/Nagle/QoS]
                          |
                          v
                   UNIFIED OUTPUT
                   [Scan -> Diagnose -> Fix -> Verify]
```

## Data Flow

1. **Hardware Profile** determines optimization tier and upscaler recommendation
2. **Game Detection** identifies what's running and loads the right profile
3. **Performance Monitoring** captures frame times and hardware metrics
4. **Stutter Analysis** correlates frame time data with hardware state
5. **Config Manager** applies game-specific settings with backup
6. **System Optimizer** applies OS-level tweaks
7. **Network Optimizer** reduces online game latency
8. **Verification** confirms improvements with real metrics
