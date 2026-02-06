#!/usr/bin/env bash
# Start Chimera backend API (run from repo root or with BACKEND_DIR set)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="${BACKEND_DIR:-$REPO_ROOT/backend}"
cd "$BACKEND_DIR"
export PYTHONPATH=src
exec uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
