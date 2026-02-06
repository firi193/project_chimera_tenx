#!/usr/bin/env bash
# Run backend tests (from repo root or backend/)
set -e
cd "$(dirname "$0")/../backend"
export PYTHONPATH=src
exec python -m pytest tests -v "$@"
