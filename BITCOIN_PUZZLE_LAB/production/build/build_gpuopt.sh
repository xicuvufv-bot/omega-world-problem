#!/usr/bin/env bash
# ============================================================================
# build_gpuopt.sh — GPUOptEngine (persistent kangaroo kernel) build, Colab-ready.
#
# Produces ONE self-contained binary: build/kangaroo (GPUOpt solver).
#
# Prereqs (Google Colab GPU runtime):
#   !apt-get -y install nvidia-cuda-toolkit g++-4.8 2>/dev/null
#   (older CUDA used g++-4.8; modern toolkits accept the system g++ — if the
#    host compiler is newer, drop the -ccbin flag below.)
#
# Usage:
#   bash production/build/build_gpuopt.sh [CCAP]
#       CCAP default = 0    (fat binary: sm_75 T4 + sm_80 A100 + sm_89 L4).
#       75 = T4 only, 80 = A100 only, 89 = L4 only (single-arch build).
#
# Flags (rationale in GPUOptLaunch.h):
#   -O3 --use_fast_math -Xptxas -v,-O3  → -O3 code + ptxas register/spill audit.
#   --use_fast_math is inert for the u64-only field path; kept for parity.
#
# TU layout (CRITICAL, do not revert to text includes):
#   GPUOptKernel.cu  → own TU (kernOpt definition; compiled EXACTLY once)
#   GPUOptEngine.cu  → host controller TU (pulls GPUOpt.h + GPUOptLaunch.h fwd decl)
#   Kangaroo.cpp/.h  → already switched to GPUOptEngine (Kangaroo.cpp:521/523)
#   GPUEngine.cu     → still needed by Check.cpp / main.cpp PrintCudaInfo
# ============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/build/src/Kangaroo"
OUT="$ROOT/build"
CCAP="${1:-0}"

command -v nvcc >/dev/null 2>&1 || { echo "ERROR: nvcc not found (CUDA toolkit missing)"; exit 1; }
command -v g++  >/dev/null 2>&1 || { echo "ERROR: g++ not found"; exit 1; }

# Fat binary when asked for it (all three datacenter arches from one source).
if [ "$CCAP" = "0" ]; then
  GENCODE=(-gencode "arch=compute_75,code=sm_75" \
           -gencode "arch=compute_80,code=sm_80" \
           -gencode "arch=compute_89,code=sm_89")
else
  GENCODE=(-gencode "arch=compute_${CCAP},code=sm_${CCAP}")
fi

CUFLAGS=(-O3 --use_fast_math -Xptxas -v,-O3 "${GENCODE[@]}" -I"$SRC" -I"$SRC/SECPK1")
HFLAGS=(-DWITHGPU -O2 -mssse3 -Wno-unused-result -Wno-write-strings -I"$SRC" -I"$SRC/SECPK1")

mkdir -p "$OUT"

echo "[gpuopt] compiling GPUOptEngine.cu  (host controller TU)"
nvcc "${CUFLAGS[@]}" -c "$SRC/GPU/GPUOptEngine.cu" -o "$OUT/GPUOptEngine.o"

echo "[gpuopt] compiling GPUOptKernel.cu   (kernel TU, compiled exactly once)"
nvcc "${CUFLAGS[@]}" -c "$SRC/GPU/GPUOptKernel.cu" -o "$OUT/GPUOptKernel.o"

echo "[gpuopt] compiling GPUEngine.cu      (legacy, needed by Check.cpp/main.cpp)"
nvcc -maxrregcount=0 -O2 "${GENCODE[@]}" -I"$SRC" -I"$SRC/SECPK1" \
     -c "$SRC/GPU/GPUEngine.cu" -o "$OUT/GPUEngine.o"

echo "[gpuopt] compiling host sources (g++)"
HOST_SRCS=(
  "$SRC/main.cpp" "$SRC/Kangaroo.cpp" \
  "$SRC/Check.cpp" "$SRC/Thread.cpp" "$SRC/HashTable.cpp" "$SRC/Timer.cpp"
  "$SRC/Backup.cpp" "$SRC/Network.cpp" "$SRC/Merge.cpp" "$SRC/PartMerge.cpp"
  "$SRC/SECPK1/Int.cpp" "$SRC/SECPK1/IntMod.cpp" "$SRC/SECPK1/IntGroup.cpp"
  "$SRC/SECPK1/Point.cpp" "$SRC/SECPK1/SECP256K1.cpp" "$SRC/SECPK1/Random.cpp"
)
_HOSTOBJ=()
for s in "${HOST_SRCS[@]}"; do
  b="$(basename "${s%.cpp}")"
  g++ "${HFLAGS[@]}" -c "$s" -o "$OUT/${b}.o"
  _HOSTOBJ+=("$OUT/${b}.o")
done

echo "[gpuopt] linking build/kangaroo"
g++ "${_HOSTOBJ[@]}" \
    "$OUT/GPUOptEngine.o" "$OUT/GPUOptKernel.o" "$OUT/GPUEngine.o" \
    -o "$OUT/kangaroo" -lpthread -lcudart

echo "[gpuopt] OK → $OUT/kangaroo"
echo "[gpuopt] run:  cd build && ./kangaroo -gpu -gpuId 0 -ws -d 24 ..."