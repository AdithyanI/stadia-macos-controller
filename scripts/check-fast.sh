#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_FAST_CHECK="${REPO_FAST_CHECK:-$HOME/GitHub/scripts/bin/repo-fast-check}"

cd "$ROOT_DIR"

"$REPO_FAST_CHECK" \
  --repo-root "$ROOT_DIR" \
  --scope staged \
  --check-shell \
  --check-json \
  --no-input

python3 scripts/check-controller-guide-static.py
python3 scripts/check-mappings.py

echo "[check-fast] checks passed"
