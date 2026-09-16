"""Bitcoin Puzzle intervals, tracker parsing, and per-puzzle classification.

The tracker first column is a hex range ``lo:hi``; the puzzle number n is the
bit length of lo, i.e. the interval is [2^(n-1), 2^n - 1] wrapped as [lo, hi].
"""

from dataclasses import dataclass

RAW_TRACKER = "dataset/raw_tracker.txt"
NOT_SOLVED = "NOT SOLVED"


@dataclass(frozen=True)
class PuzzleRow:
    n: int
    lo: int
    hi: int
    address: str
    status: str        # one of SOLVED / UNSOLVED
    pub: str           # hex compressed pubkey or "NOT SOLVED"
    priv: str          # hex secret or "NOT SOLVED"

    @property
    def solved(self) -> bool:
        return self.status == "SOLVED"

    @property
    def exposed_pubkey(self) -> bool:
        return (not self.solved) and self.pub != NOT_SOLVED

    @property
    def regime(self) -> str:
        """R1: address-only (no pubkey). R2: public-key exposed (unsolved)."""
        if self.solved:
            return "SOLVED"
        if self.exposed_pubkey:
            return "R2"
        return "R1"


def bounds(n: int):
    """Standard interval for puzzle n: lo = 2^(n-1), hi = 2^n - 1."""
    return (1 << (n - 1)), ((1 << n) - 1)


def width(n: int) -> int:
    lo, hi = bounds(n)
    return hi - lo + 1  # == 2^(n-1)


def parse_tracker(path: str = None) -> list:
    path = path or RAW_TRACKER
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or not line.startswith("|"):
                continue
            parts = [c.strip() for c in line.split("|")]
            if len(parts) < 6:
                continue
            lo_s, hi_s = parts[1].split(":")
            lo, hi = int(lo_s, 16), int(hi_s, 16)
            n = lo.bit_length()
            addr = parts[2]
            status = "SOLVED" if parts[3] == "SOLVED" else "UNSOLVED"
            pub = parts[4]
            priv = parts[5]
            rows.append(PuzzleRow(n=n, lo=lo, hi=hi, address=addr,
                                  status=status, pub=pub, priv=priv))
    return rows


def classify(rows: list) -> dict:
    solved = [r for r in rows if r.solved]
    r1 = [r for r in rows if r.regime == "R1"]
    r2 = [r for r in rows if r.regime == "R2"]
    return {"total": len(rows), "solved": len(solved), "unsolved": len(r1) + len(r2),
            "r1": len(r1), "r2": len(r2)}


def sample_rows(rows, n) -> list:
    return [r for r in rows if r.n == n]