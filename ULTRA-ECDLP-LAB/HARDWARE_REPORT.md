# HARDWARE_REPORT — ULTRA-ECDLP-LAB

Audit date: 2026-09-22. All facts measured/probed by scripts in `tools/`
(cpuid_probe.c) or system queries (wmic/PowerShell/clinfo). No assumptions.

## CPU
| property | value | source |
|---|---|---|
| Model | AMD Ryzen 3 3200G with Radeon Vega Graphics | wmic |
| Nominal clock | 3600 MHz | wmic MaxClockSpeed |
| Cores / threads | 4 / 4 (no SMT) | wmic |
| SIMD | SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AVX, FMA, MOVBE | cpuid probe |
| BMI1 / BMI2 | 1 / 1 | cpuid probe |
| ADX | 1 | cpuid probe |
| AVX2 | 1 | cpuid probe |
| AVX-512 (F/DQ/BW/VL/CD) | 0 / 0 / 0 / 0 / 0 | cpuid probe |
| Hypervisor present | 1 (VM / EPV host) | cpuid leaf1 |
| Vendor string | AuthenticAMD | cpuid |
| Max CPUID leaf | 0x0D (cache leaf 4 not exposed) | cpuid |

Notes:
- Zen+ microarchitecture (Picasso). No AVX-512 in any configuration.
- ADX + BMI2 present => a fast path exists for 2-limb / multi-limb big-integer
  carries (adcx/adox, mulx) AND for 64-bit Barrett/Montgomery helpers if a
  hardware 128-bit multiply (mulq) is used; no 256x256 needed for toy fields <=2^32.
- Because we run inside a hypervisor, published clock may not reflect guest
  frequency exactly; all reported numbers are wall/Loop-timer measured, not
  spec-derived. Cache topology not exposed by leaf 4 here; behavioral
  bandwidth tests in Phase 6 will bound L1/L2/L3 behavior empirically.

## Memory
| property | value |
|---|---|
| Total physical RAM | 14,951,428,096 B (~14.9 GiB) |
| Working set used by lab | reported per run in benchmarks |

## GPU (compute-capable, validated presence — compute behavior tested in Phase 9)
| property | value |
|---|---|
| Device | AMD Radeon Vega 8 Graphics (iGPU, shares system RAM) |
| OpenCL platform | AMD-APP 3584.0, OpenCL 2.1 FULL_PROFILE |
| Compute units | 8 |
| Work group max | 256 |
| Clock | 1250 MHz |
| Global memory | 7,552,630,784 B (~7.5 GiB) |
| Max mem alloc | 4,594,375,065 B |
| double FMA | IEEE, round-to-nearest |
| Native pref. widths | char4 / short2 / int1 / long1 / float1 / double1 |
| Cache | 16 KB L2-equivalent, line 64 B |

Other compute check results:
- CUDA (nvcc / NVIDIA driver): NOT present.
- Vulkan runtime: vulkan-1.dll + vulkaninfo.exe present (not benchmarked in
  this phase; OpenCL chosen as the only cross-vendor GPU path with a CLI).
- MSVC `cl`: NOT on PATH (checked Program Files LLVM + where). Only GCC bin
  on PATH.

## Toolchain (the only full C/C++ toolchain present)
| tool | version |
|---|---|
| g++ | 16.1.0 (MinGW-Builds x86_64-posix-seh-rev0) |
| gcc | 16.1.0 (same) |
| clang++ | not found |
| cmake | not found |
| python | 3.11 (stdlib; used for harness/plot orchestrations) |

Implication: all C/C++ builds in this lab use GCC with the flags actually
benchmarked. There is no MSVC/Clang comparison available in this environment;
that part of the requested comparison is recorded as NOT-APPLICABLE rather
than fabricated.

## Reference timers
- Headless/benchmark timing: chrono::steady_clock (min resolution ~ns; we use
  long loops).
- x86-64 RDTSC not used for cross-machine claims; steady_clock for all
  reported seconds; cycles estimated as seconds x measured-clock.