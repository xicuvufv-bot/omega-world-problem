# LICENSE AUDIT

## Component Licenses and Compliance

### Core Dependencies

| Component | License | Commercial Use | Modification | Redistribution | Attribution Required |
|-----------|---------|---------------|--------------|----------------|---------------------|
| PresentMon (Intel) | MIT | Yes | Yes | Yes | Yes |
| LibreHardwareMonitor | MPL-2.0 | Yes | Yes (file-level) | Yes | Yes |
| psutil | BSD-3 | Yes | Yes | Yes | Yes |

### Referenced Projects (not directly included, code patterns studied)

| Project | License | Notes |
|---------|---------|-------|
| GameShift | GPL-3.0 | GPL, cannot link proprietary code; studied patterns only |
| fps-overlay | GPL-3.0 | GPL; studied ETW approach |
| ReFrame | MIT | MIT; config parsing patterns adapted |
| Game-Optimizer | MIT | MIT; CPU affinity patterns adapted |
| mojo-gaming-mode | MIT | MIT; system tweak patterns adapted |
| ssm | GPL-3.0 | GPL; studied kernel tuning patterns |
| fpsdoctor | MIT | MIT; diagnostic verdict patterns adapted |
| FrameLedger | GPL-3.0 | GPL; studied frame analysis approach |

### License Compliance Notes

1. **GameForge itself**: Will use MIT License
2. **MPL-2.0 components** (LibreHardwareMonitor): File-level copyleft; can use in proprietary code as long as modified MPL files remain MPL
3. **GPL-3.0 references**: Code patterns were studied and reimplemented independently; no GPL code was copied verbatim
4. **All adaptations**: Written from scratch using public documentation and API references, not copied from GPL sources

### Third-Party Notices

- PresentMon: Copyright Intel Corporation. Licensed under MIT.
- LibreHardwareMonitor: Copyright LibreHardwareMonitor contributors. Licensed under MPL-2.0.
- psutil: Copyright Giampaolo Rodola. Licensed under BSD-3-Clause.
