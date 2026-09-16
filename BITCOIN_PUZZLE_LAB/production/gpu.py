"""GPU inventory: enumerate CUDA devices via nvidia-smi (if present).

Only does READ-ONLY enumeration. No driver install, no OC, no changes.
Used to size the worker fan-out (one BitCrack/Kangaroo per GPU).
"""

import shutil
import subprocess


def _run(args):
    try:
        out = subprocess.run(args, capture_output=True, timeout=30,
                             text=True)
        if out.returncode != 0:
            return None
        return out.stdout
    except (OSError, subprocess.SubprocessError):
        return None


def has_nvidia_smi():
    return shutil.which("nvidia-smi") is not None


def devices():
    """Return list of dicts: {id, name, memory_gb} for each CUDA GPU."""
    if not has_nvidia_smi():
        return []
    out = _run(["nvidia-smi", "--query-gpu=index,name,memory.total",
                "--format=csv,noheader,nounits"])
    if not out:
        return []
    res = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        try:
            res.append({"id": int(parts[0]), "name": parts[1],
                        "memory_gb": float(parts[2]) / 1024.0})
        except ValueError:
            continue
    return res


def compute_capabilities():
    """Best-effort per-GPU compute capability via `nvidia-smi --help` of
    `nvidia-smi -q` -> 'CUDA Version' is the driver CUDA; actual CC needs
    device query. BitCrack auto-selects; this is informational only."""
    out = _run(["nvidia-smi"])
    return (out or "")


def recommend_grid(gpu_cls_hint="auto"):
    """Simple heuristic grid. BitCrack defaults are usually fine; this is
    exposed as a dial, not a magic number."""
    return gpu_cls_hint


def summary():
    d = devices()
    return {"present": bool(d), "count": len(d), "devices": d}