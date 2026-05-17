#!/usr/bin/env bash
# Local validation harness for shield__lattice-archive-traversal_001.
#
# Usage:
#   ./run_tests.sh vulnerable  # hidden tests only; confirms exploit tests fail
#   ./run_tests.sh fixed       # hidden tests only; confirms gold patch fixes them
#   ./run_tests.sh both        # default; runs vulnerable and fixed validation

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-both}"

case "$MODE" in
  vulnerable|fixed|both)
    python3 "$ROOT_DIR/grader/grade.py" --mode "$MODE"
    ;;
  *)
    python3 "$ROOT_DIR/grader/grade.py" "$@"
    ;;
esac
