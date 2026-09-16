#!/usr/bin/env bash
# Build the production engine stack on Linux (NVIDIA CUDA).
#
# Prereqs: git, gcc/g++, make, CUDA toolkit (>=10.1). Run from the lab root:
#
#   bash production/build/build_linux.sh
#
# Outputs go to production/bin/ and are resolved by production.manager.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/production/build/src"
BIN="$ROOT/production/bin"
mkdir -p "$SRC" "$BIN"

clone() {
  local url="$1" dir="$2"
  if [ -d "$dir/.git" ]; then
    echo "[skip] $dir"
  else
    echo "[clone] $url"
    git clone --recursive "$url" "$dir"
  fi
}

clone https://github.com/brichard19/BitCrack.git "$SRC/BitCrack" || true
clone https://github.com/JeanLucPons/Kangaroo.git "$SRC/Kangaroo" || true

echo ""
echo "=== BitCrack ==="
cd "$SRC/BitCrack"
make -j"$(nproc 2>/dev/null || echo 4)" >/dev/null 2>&1 \
  && cp -f cuBitCrack "$BIN/" 2>/dev/null \
  && cp -f clBitCrack "$BIN/" 2>/dev/null || {
    echo "  auto Makefile build failed; build manually:"
    echo "    cd $SRC/BitCrack && make"
  }

echo ""
echo "=== Kangaroo ==="
cd "$SRC/Kangaroo"
make gpu=1 all >/dev/null 2>&1 \
  && cp -f kangaroo "$BIN/" || {
    echo "  auto build failed; build manually:"
    echo "    cd $SRC/Kangaroo && make gpu=1 ccap=XX all   (XX = your SM, e.g. 89 for RTX40xx)"
  }

echo ""
echo "Engine binaries now live (if the above builds succeeded) in: $BIN"
ls -la "$BIN" 2>/dev/null || true
echo ""
echo "Optional replacements: RCKangaroo (RetiredCoder) for 125-bit-class"
echo "kangaroo work; theCollider for pool/RSA-encrypted distributed scanning."