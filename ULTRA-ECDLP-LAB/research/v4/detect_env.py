"""detect_env.py - V5 Phase 1: record the ACTUAL environment to KAGGLE_ENVIRONMENT.json.

Runs anywhere (this host or the Kaggle T4x2 box). Every probe is real.
No GPU claims unless nvidia-smi actually lists the device.
"""
import json, os, platform, shutil, subprocess, sys

def which(name):
    return shutil.which(name) or None

def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return (r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip())
    except (OSError, subprocess.TimeoutExpired):
        return (None, "", "")

def gpu_info():
    out = {"count": 0, "devices": [], "nvcc_path": None, "cuda_version": None,
           "note": ""}
    nv = which("nvidia-smi")
    nvc = which("nvcc")
    out["nvcc_path"] = nvc
    if nvc:
        rc, so, se = run([nvc, "--version"])
        out["cuda_version"] = (so or se).splitlines()[0] if (so or se) else None
    if not nv:
        out["note"] = "nvidia-smi NOT present: no GPU claims possible from this host."
        return out
    rc, so, se = run([nv, "--query-gpu=name,memory.total,compute_cap",
                      "--format=csv,noheader,nounits"])
    if rc != 0:
        out["note"] = f"nvidia-smi present but query failed: {se}"
        return out
    for line in so.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            out["devices"].append({"name": parts[0], "memory_mb": parts[1],
                                   "compute_cap": parts[2]})
    out["count"] = len(out["devices"])
    return out

def main():
    env = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "host": platform.node(),
        "platform": platform.platform(),
        "cpu": platform.processor(),
        "python": sys.version.split()[0],
        "python_path": sys.executable,
        "is_kaggle": os.path.isdir("/kaggle/input") or os.path.isdir("/kaggle/working"),
        "cwd": os.getcwd(),
        "gpu": gpu_info(),
        "tools": {"python": which("python"), "gcc": which("gcc"), "g++": which("g++"),
                  "nvcc": which("nvcc"), "make": which("make"), "git": which("git"),
                  "kaggle": which("kaggle"), "ffmpeg": which("ffmpeg")},
    }
    out_path = sys.argv[1] if len(sys.argv) > 1 else "KAGGLE_ENVIRONMENT.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)
    print(json.dumps(env, indent=2))

if __name__ == "__main__":
    main()