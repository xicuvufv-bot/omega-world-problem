#!/usr/bin/env bash
# ============================================================
# ULTRA-ECDLP V5 Kaggle T4x2 onboarding
#
# Run inside a Kaggle notebook cell or a terminal after the
# repository has been cloned into the session:
#
#   cd <repo>/research/v4 && bash kaggle_onboard.sh
#
# What it does:
#   1. records the REAL environment (must show 2x T4 + nvcc)
#   2. runs the full gated v5 pipeline (builds, selftests,
#      benchmarks, solves, reports)
#
# It never claims a GPU that is not visible to nvidia-smi.
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"

echo "== [1/2] environment probe =="
python detect_env.py

echo "== [2/2] v5 gated pipeline =="
python kaggle_v5_run.py

echo "== done: open KAGGLE_V5_FINAL_REPORT.md =="