from .v1_bruteforce import scan_naive
from .v2_bitmask import solve_stride, build_bitmask, scan_masked, keys_per_second
from .v3_bsgs import solve_bsgs
from .v4_kangaroo import KangarooSolver

VERSION_LOG = {
    1: "naive per-key scalar multiplication; correctness baseline",
    2: "stride point-add (O(1) per key) + hash160 bitmask prefilter",
    3: "Baby-step Giant-step: O(sqrt(W)) time with O(sqrt(W)) memory",
    4: "Pollard kangaroo: O(sqrt(W)) time, O(1) memory, parallelizable",
}

__all__ = [
    "scan_naive", "solve_stride", "build_bitmask", "scan_masked", "keys_per_second",
    "solve_bsgs", "KangarooSolver", "VERSION_LOG",
]