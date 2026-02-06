#!/usr/bin/env bash
# Run the API so that the `api` module is found (src is on PYTHONPATH).
cd "$(dirname "$0")"
export PYTHONPATH=src
exec uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
