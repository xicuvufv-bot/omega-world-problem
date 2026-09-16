"""Work estimates, unit conversions and difficulty tiers.

Operating assumptions (sourced in reports/08_SOURCES.md):
  * 1x RTX 4090 key-scan (SHA256+RIPEMD160 compare)  ~ 2.5e9 H/s
  * 1x RTX 4090 secp256k1 scalar multiplication       ~ 8e9 group-ops/s
    (group-ops counted as one scalar multiplication per key)
These are *estimates* for planning only; every number is labelled as such.
"""

SECS_PER_YEAR = 365.25 * 24 * 3600

GPU_HASH_PER_SEC = 2.5e9      # R1 (address-only) regime
GPU_GROUP_PER_SEC = 8e9       # R2 (public-key exposed) regime

# Interval width for puzzle n is 2^(n-1).
# R1 expected work  ~ W hashes                              = 2^(n-1)
# R2 expected work  ~ 2*sqrt(W) group-ops (kangaroo/BSGS)   = 2^((n+1)/2)


def interval_work_hashes(n: int) -> int:
    return 1 << (n - 1)


def interval_work_ops(n: int) -> int:
    return 3 * (1 << ((n - 1) // 2))


def years_for_work(ops: float, per_sec: float) -> float:
    return ops / per_sec / SECS_PER_YEAR


def gpu_years_r1(n: int) -> float:
    return years_for_work(interval_work_hashes(n), GPU_HASH_PER_SEC)


def gpu_years_r2(n: int) -> float:
    return years_for_work(interval_work_ops(n), GPU_GROUP_PER_SEC)


def format_ops(n: int) -> str:
    """Human readable like 2^70 ~ 1.18e21."""
    if n < 0:
        return "0"
    if n >= 120:
        return f"~{2.0 ** n:.2e}"
    return f"{2.0 ** n:.0f}"


def tier(single_gpu_years: float) -> str:
    """Honest labels relative to a single modern GPU."""
    if single_gpu_years < 0.01:
        return "TOY"
    if single_gpu_years < 1:
        return "EASY"
    if single_gpu_years < 10:
        return "MEDIUM"
    if single_gpu_years < 1000:
        return "HARD"
    return "EXTREME"