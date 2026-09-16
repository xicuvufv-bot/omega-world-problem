"""Puzzle registry: the ONLY allowed attack surface in this pipeline.

Every scan target must resolve to one of the 160 official Bitcoin-Puzzle
addresses published by the puzzle creator (1PWoZ, tx 08389f34..., 2015).
The frozen table in ``registry_data.py`` was generated from
``dataset/raw_tracker.txt`` (the canonical roadhero tracker) + ``puzzles_meta.csv``.

Hard rules enforced here:
  * any address passed in by the user is looked up in the registry ONLY;
  * arbitrary addresses (not in the table) raise ``RegistryError``;
  * scan ranges must be a sub-range of the puzzle's official interval
    [2^(n-1), 2^n - 1]; anything wider/foreign is refused;
  * solved puzzles can never be selected as targets.
"""

from .registry_data import PUZZLE_TABLE, SOLVED_COUNT, UNSOLVED_COUNT


class RegistryError(ValueError):
    pass


def all_rows():
    return [Puzzle(n=n, lo_hex=lo_hex, hi_hex=hi_hex, address=addr,
                   pubkey=pub, solved=solved)
            for (n, lo_hex, hi_hex, addr, pub, solved) in PUZZLE_TABLE]


class Puzzle:
    __slots__ = ("n", "lo_hex", "hi_hex", "address", "pubkey", "solved",
                 "_lo", "_hi")

    def __init__(self, n, lo_hex, hi_hex, address, pubkey, solved):
        self.n = n
        self.lo_hex = lo_hex
        self.hi_hex = hi_hex
        self.address = address
        self.pubkey = pubkey            # hex compressed pubkey or None
        self.solved = solved
        self._lo = int(lo_hex, 16)
        self._hi = int(hi_hex, 16)

    # -- range helpers ----------------------------------------------------
    @property
    def lo(self):
        return self._lo

    @property
    def hi(self):
        return self._hi

    @property
    def width(self):
        return self._hi - self._lo + 1      # == 2^(n-1)

    @property
    def bits(self):
        return self.n

    @property
    def regime(self):
        """R1 = address-only brute force; R2 = pubkey exposed (interval DLP)."""
        if self.solved:
            return "SOLVED"
        if self.pubkey:
            return "R2"
        return "R1"

    @property
    def keyspace_hex(self):
        return "%s:%s" % (self.lo_hex, self.hi_hex)

    def __repr__(self):
        return "Puzzle(%d, %s, %s)" % (self.n, self.regime, self.address)


_INDEX = {p.address: p for p in all_rows()}
_BY_N = {p.n: p for p in all_rows()}


def get_by_number(n):
    """Puzzle by number 1..160. Refuses solved puzzles as scan targets."""
    p = _BY_N.get(int(n))
    if p is None:
        raise RegistryError("no puzzle #%s in the official 1..160 table" % n)
    return p


def get_by_address(address):
    """Puzzle by official address (exact match). NO arbitrary addresses."""
    p = _INDEX.get(address)
    if p is None:
        raise RegistryError(
            "address is not in the official Bitcoin-Puzzle registry: %s" % address)
    return p


def resolve_target(address=None, number=None):
    """Return a Puzzle given exactly one of address / number."""
    if address and number:
        raise RegistryError("pass EITHER --address OR --number, not both")
    if number is not None:
        return get_by_number(number)
    if address is None:
        raise RegistryError("a target is required: --address <addr> or --number <n>")
    return get_by_address(address)


def unsolved():
    return [p for p in all_rows() if not p.solved]


def unsolved_by_regime():
    r1 = [p for p in all_rows() if not p.solved and p.regime == "R1"]
    r2 = [p for p in all_rows() if not p.solved and p.regime == "R2"]
    return r1, r2


def summary():
    return {"total": len(PUZZLE_TABLE), "solved": SOLVED_COUNT,
            "unsolved": UNSOLVED_COUNT,
            "r1": len([p for p in all_rows() if not p.solved and p.regime == "R1"]),
            "r2": len([p for p in all_rows() if not p.solved and p.regime == "R2"])}