#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py - portable build driver for ULTRA-ECDLP-LAB.

Cross-platform (Windows / Linux / Kaggle). Resolves every path relative to
this script, so it works from a clean git checkout on any machine.

  python build.py cpu     build research/v4/v4_cpu_engine(.exe) with g++
  python build.py cuda    build research/v4/kangaroo_cuda with nvcc (GPU required)
  python build.py micro   build the v1-v2 microbench variants (g++)
  python build.py tools   build tools/cpuid_probe(.exe) with gcc
  python build.py all     cpu + cuda(kaggle-only) + micro + tools
  python build.py clean   remove all build products named below

No fakery: `cuda` refuses to run (exit 1) if nvcc is missing. The CUDA binary
is only ever produced on a real NVIDIA host.

Exact flags mirror what the v5 pipeline uses:
  CPU  : g++ -O3 -march=native -std=c++17 -pthread
  CUDA : nvcc -O3 -std=c++17 -arch=sm_75 -Xptxas -O3 -lineinfo \
             -maxrregcount=80 -Xcompiler -pthread   (T4 = sm_75)
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

BINS = {
    "cpu": {
        "src": ["research", "v4", "v4_cpu_engine.cpp"],
        "out": ["research", "v4", "v4_cpu_engine"],
        "cmd": ["g++", "-O3", "-march=native", "-std=c++17", "-pthread"],
    },
    "cuda": {
        "src": ["research", "v4", "kangaroo_cuda.cu"],
        "out": ["research", "v4", "kangaroo_cuda"],
        "cmd": ["nvcc", "-O3", "-std=c++17", "-arch=sm_75",
                "-Xptxas", "-O3", "-lineinfo", "-maxrregcount=80",
                "-Xcompiler", "-pthread"],
    },
    "micro": [
        {"src": ["src", "micro_main.cpp"], "out": ["micro_O2"],
         "cmd": ["g++", "-O2", "-std=c++17"]},
        {"src": ["src", "micro_main.cpp"], "out": ["micro_O3"],
         "cmd": ["g++", "-O3", "-std=c++17"]},
        {"src": ["src", "micro_main.cpp"], "out": ["micro_Ofast"],
         "cmd": ["g++", "-Ofast", "-std=c++17"]},
        {"src": ["src", "micro_main.cpp"], "out": ["micro_native"],
         "cmd": ["g++", "-O3", "-march=native", "-std=c++17"]},
    ],
    "tools": {
        "src": ["tools", "cpuid_probe.c"],
        "out": ["tools", "cpuid_probe"],
        "cmd": ["gcc", "-O2", "-std=c11"],
    },
}

SUFFIX = ["-I.", "-o"]


def _join(*parts):
    return os.path.join(HERE, *parts)


def _ext():
    return ".exe" if os.name == "nt" else ""


def _run(argv):
    print("+", " ".join(argv))
    return subprocess.run(argv, cwd=HERE).returncode


def _build_single(spec, label):
    src = _join(*spec["src"])
    if not os.path.isfile(src):
        print("ERROR: missing source: %s" % src)
        return 1
    compiler = shutil.which(spec["cmd"][0])
    if not compiler:
        print("SKIP[%s]: compiler not found: %s" % (label, spec["cmd"][0]))
        return 0 if label == "cuda" else 2
    out = _join(*spec["out"]) + _ext()
    argv = list(spec["cmd"]) + SUFFIX + [out, src]
    rc = _run(argv)
    if label == "cuda":
        print("CUDA build: rc=%d (COMPILED ON REAL NVIDIA HOST ONLY)" % rc)
    else:
        print("built %s %s" % (label, out))
    return rc


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == "cpu":
        return _build_single(BINS["cpu"], "cpu")
    if cmd == "cuda":
        if not shutil.which("nvcc"):
            print("GPU VALIDATION BLOCKED - nvcc not found (no CUDA host).")
            return 1
        return _build_single(BINS["cuda"], "cuda")
    if cmd == "micro":
        rc = 0
        for spec in BINS["micro"]:
            rc = max(rc, _build_single(spec, "micro"))
        return rc
    if cmd == "tools":
        return _build_single(BINS["tools"], "tools")
    if cmd == "all":
        rc = _build_single(BINS["cpu"], "cpu")
        if shutil.which("nvcc"):
            rc = max(rc, _build_single(BINS["cuda"], "cuda"))
        for spec in BINS["micro"]:
            rc = max(rc, _build_single(spec, "micro"))
        rc = max(rc, _build_single(BINS["tools"], "tools"))
        return rc
    if cmd == "clean":
        outs = [BINS["cpu"]["out"], BINS["cuda"]["out"], BINS["tools"]["out"]]
        outs += [s["out"] for s in BINS["micro"]]
        for o in outs:
            p = _join(*o) + _ext()
            if os.path.exists(p):
                os.remove(p)
                print("removed", p)
        return 0
    print("unknown subcommand: %s" % cmd)
    return 1


if __name__ == "__main__":
    sys.exit(main())