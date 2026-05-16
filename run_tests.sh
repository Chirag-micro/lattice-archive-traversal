#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)

if [ "$#" -eq 0 ]; then
  python3 "$ROOT_DIR/grader/grade.py" --mode both
else
  python3 "$ROOT_DIR/grader/grade.py" "$@"
fi
