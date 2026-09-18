#!/bin/bash
# kangaroo_puzzle70.sh - Complete build and run script for Puzzle 70
# Usage: bash kangaroo_puzzle70.sh [puzzle_number] [checkpoint_dir]

set -euo pipefail

# ─── Configuration ──────────────────────────────────────────────────────────
PUZZLE="${1:-70}"
CHECKPOINT_DIR="${2:-./checkpoints}"
ARCH="${ARCH:-sm_75}"  # T4 default
WITHGPU=1

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# ─── 1. Check GPU ──────────────────────────────────────────────────────────
log "🔍 Detecting GPU..."
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,compute_cap,memory.total --format=csv,noheader | head -1)
    GPU_NAME=$(echo "$GPU_INFO" | cut -d',' -f1 | xargs)
    GPU_CC=$(echo "$GPU_INFO" | cut -d',' -f2 | xargs)
    GPU_MEM=$(echo "$GPU_INFO" | cut -d',' -f3 | xargs)
    log "GPU: $GPU_NAME ($GPU_MEM)"
    
    case "$GPU_CC" in
        "7.5") ARCH="sm_75" ;;   # T4
        "8.0") ARCH="sm_80" ;;   # A100
        "8.6") ARCH="sm_86" ;;   # A100 80GB
        "8.9") ARCH="sm_89" ;;   # H100
        "9.0") ARCH="sm_90" ;;   # H100
        *) ARCH="sm_75"; warn "Unknown CC $GPU_CC, defaulting to sm_75" ;;
    esac
    log "Using ARCH: $ARCH"
else
    error "No NVIDIA GPU detected! Ensure GPU is available."
fi

# ─── 2. Setup Repository ───────────────────────────────────────────────────
REPO_DIR="BITCOIN_PUZZLE_LAB"
if [ ! -d "$REPO_DIR" ]; then
    log "📥 Cloning repository..."
    git clone https://github.com/xicuvufv-bot/BITCOIN_PUZZLE_LAB.git "$REPO_DIR" 2>/dev/null || {
        git clone https://github.com/JeanLucPons/Kangaroo.git "$REPO_DIR"_orig 2>/dev/null
        cp -r "$REPO_DIR"_orig "$REPO_DIR" 2>/dev/null || true
    }
fi

cd "$REPO_DIR/production/native"
success "Working in $(pwd)"

# ─── 3. Fix hardcoded CUDA paths ──────────────────────────────────────────
log "🔧 Checking for hardcoded CUDA paths..."
if grep -q "cuda-8.0\|cuda-10\|cuda-11\|cuda-12" kangaroo_glv_gpu.cu 2>/dev/null; then
    sed -i 's|/usr/local/cuda-8.0|/usr/local/cuda|g; s|/usr/local/cuda-10|/usr/local/cuda|g; s|/usr/local/cuda-11|/usr/local/cuda|g; s|/usr/local/cuda-12|/usr/local/cuda|g' kangaroo_glv_gpu.cu
    success "Fixed hardcoded CUDA paths"
fi

# ─── 4. Build with GPU support ────────────────────────────────────────────
log "🔨 Building with ARCH=$ARCH, WITHGPU=1..."
make clean 2>/dev/null || true
make WITHGPU=1 ARCH=$ARCH 2>&1 | tail -20

if [ ! -f "kangaroo_glv_gpu" ]; then
    log "Make failed, trying direct nvcc..."
    nvcc -O3 -arch=$ARCH -Xcompiler=/O2 -Xptxas -O3 -I. -std=c++17 -o kangaroo_glv_gpu kangaroo_glv_gpu.cu -lcudart
fi

if [ ! -f "kangaroo_glv_gpu" ]; then
    error "Build failed - binary not created"
fi
success "Build successful!"

# ─── 5. Sanity Test ───────────────────────────────────────────────────────
log "🧪 Running sanity test..."
./kangaroo_glv_gpu -test
success "Sanity test passed!"

# ─── 6. Setup Checkpoint Directory ────────────────────────────────────────
mkdir -p "$CHECKPOINT_DIR"
CHECKPOINT_FILE="$CHECKPOINT_DIR/puzzle_${PUZZLE}.work"
log "💾 Checkpoint: $CHECKPOINT_FILE"

# ─── 7. Calculate Puzzle Range ────────────────────────────────────────────
# Puzzle 70: [2^69, 2^70-1]
log "🎯 Target: Puzzle #$PUZZLE"
log "Range: [2^$((PUZZLE-1)), 2^$PUZZLE - 1]"

# ─── 8. Launch Search ─────────────────────────────────────────────────────
log "🚀 Launching search for Puzzle #$PUZZLE..."
log "Checkpoint: $CHECKPOINT_FILE (auto-save every 5 min)"
log "Press Ctrl+C to stop (progress auto-saved)"

# Trap Ctrl+C
trap 'echo -e "\n🛑 Interrupted - checkpoint saved"; exit 0' INT TERM

./kangaroo_glv_gpu \
    -p "$PUZZLE" \
    -c "$CHECKPOINT_FILE" \
    -dpbits 26 \
    -budget 35 \
    -sleep 300 \
    2>&1 | tee -a "kangaroo_puzzle_${PUZZLE}.log"

# ─── Cleanup ──────────────────────────────────────────────────────────────
log "🏁 Search completed or interrupted"
log "Checkpoint saved to: $CHECKPOINT_FILE"
log "Log saved to: kangaroo_puzzle_${PUZZLE}.log"

# To resume after interruption, just run this script again!
EOF
echo "kangaroo_puzzle70.sh created"