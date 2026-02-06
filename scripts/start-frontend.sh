#!/usr/bin/env bash
# Start Chimera frontend (run from repo root or with FRONTEND_DIR set)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="${FRONTEND_DIR:-$REPO_ROOT/frontend}"
cd "$FRONTEND_DIR"
npm install
exec npm run dev
