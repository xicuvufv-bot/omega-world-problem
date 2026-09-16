"""Native kangaroo runner: solve an R2 puzzle's interval DLP.

The ONLY legal targets are official Bitcoin-Puzzle addresses that are (a)
NOT solved and (b) regime R2 -- i.e. the public key is exposed and the
tameness interval is fully known, which is exactly what the λ-method needs.
This is enforced through ``production.registry``: you pass ``--number`` or
``--address`` and the puzzle must resolve to an unsolved R2 row, else the
runner refuses to start.

The engine walks tame herds from the interval's low bound and wild herds
from the target point, sharing a distinguished-point table, and returns the
private key at the first verified x-collision.  Every candidate is verified
against the reference EC implementation (``algorithms/curve.py``) before it
is accepted -- never trust a native engine with a claimed solution without
independent confirmation.

Usage:
    python -m production.kangaroo_cli --number 140 [--threads 8]
    python -m production.kangaroo_cli --address <addr>

Checkpointing: ``--checkpoint FILE`` backs the DP table with a persistent
mmap file.  Re-run with the same FILE and a fresh ``--seed`` to resume that
table (progress accumulates; herds restart).  Leave out to use anonymous
memory (a fresh table every run).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.curve import point_from_mult_affine
from production.registry import RegistryError, resolve_target
from production.native import kangaroo_ffi as kangaroo


def verify_k(puzzle, k):
    """Independent confirmation: does k*G reproduce the puzzle's pubkey?"""
    px, py = point_from_mult_affine(k)
    prefix = 2 | (py & 1)
    ref = "%02x" % prefix + "%064x" % px
    return ref == puzzle.pubkey.lower()


def _pick_args(puzzle, args):
    nt = args.tame or max(1, args.threads or 1) * 4
    nw = args.wild or max(1, args.threads or 1) * 4
    return dict(n_threads=args.threads or None, ntame=nt, nwild=nw,
                dpbits=args.dpbits, seed=args.seed,
                budget=args.budget, checkpoint=args.checkpoint,
                dp_slots=args.slots, pin=not args.no_pin)


def _fmt(hex_str):
    return hex_str if len(hex_str) <= 8 else (hex_str[:4] + "..." + hex_str[-4:])


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--number", type=int, default=None,
                    help="official puzzle number (must be unsolved R2)")
    ap.add_argument("--address", default=None,
                    help="official puzzle address (must be unsolved R2)")
    ap.add_argument("--threads", type=int, default=None,
                    help="worker threads (default: half the cores)")
    ap.add_argument("--tame", type=int, default=None,
                    help="tame kangaroos total (default: 4/thread)")
    ap.add_argument("--wild", type=int, default=None,
                    help="wild kangaroos total (default: 4/thread)")
    ap.add_argument("--dpbits", type=int, default=14,
                    help="distinguished-point bits (default 14)")
    ap.add_argument("--budget", type=int, default=1 << 44,
                    help="global walk-step budget (default 2^44)")
    ap.add_argument("--seed", type=int, default=None,
                    help="RNG seed (default: fresh random)")
    ap.add_argument("--slots", type=int, default=None,
                    help="DP table slots (default derived from dpbits)")
    ap.add_argument("--checkpoint", default=None,
                    help="persistent DP-table file for resume (default: none)")
    ap.add_argument("--no-pin", action="store_true",
                    help="do not pin worker threads to cores")
    args = ap.parse_args(argv)

    try:
        puzzle = resolve_target(address=args.address, number=args.number)
    except RegistryError as exc:
        print("refusing to start: %s" % exc)
        return 2

    if puzzle.solved:
        print("refusing to start: puzzle #%d is already solved" % puzzle.n)
        return 2
    if puzzle.regime != "R2" or not puzzle.pubkey:
        print("refusing to start: puzzle #%d has no exposed public key "
              "(R1 only; kangaroo cannot run)" % puzzle.n)
        return 2

    print("target:  puzzle #%d  (%s)" % (puzzle.n, puzzle.address))
    print("TLB:     [%s, %s]  (width 2^%d)" %
          (puzzle.lo_hex[:16] + "...", puzzle.hi_hex[:16] + "...",
           puzzle.width.bit_length()))
    print("pubkey:  %s" % _fmt(puzzle.pubkey))

    lo, hi = int(puzzle.lo_hex, 16), int(puzzle.hi_hex, 16)
    kwargs = _pick_args(puzzle, args)
    if args.checkpoint:
        if os.path.exists(args.checkpoint):
            print("resuming DP table from %s" % args.checkpoint)
        else:
            print("checkpoint: %s" % args.checkpoint)

    result = kangaroo.solve(lo, hi, bytes.fromhex(puzzle.pubkey), **kwargs)

    print("steps:   %d" % result.steps)
    print("dps:     %d   cross: %d   elapsed: %.1fs" %
          (result.dps, result.cross, result.elapsed_s))
    if not result.found:
        print("no solution within budget; rerun with a fresh --seed "
              "to keep accumulating DPs%s" %
              (" (the checkpoint file was preserved)" if args.checkpoint else ""))
        return 1

    if not verify_k(puzzle, result.k):
        print("ERROR: engine returned k=%d but k*G does not match the "
              "registered pubkey -- refusing" % result.k)
        return 3

    print("PRIVATE KEY FOUND: %064x" % result.k)
    print("verified: k*G == registered pubkey")
    return 0


if __name__ == "__main__":
    sys.exit(main())