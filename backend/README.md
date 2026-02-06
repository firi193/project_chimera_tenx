# Chimera Backend

Autonomous Influencer Network – orchestration, Planner, Worker, Judge, HITL API.

## Setup

From repo root:

```bash
cd backend
uv sync
cp .env.example .env   # edit .env with DATABASE_URL, etc.
```

## Run API

The `api` module lives in `src/`, so **you must set `PYTHONPATH=src`** (or use a run script). Otherwise you get `ModuleNotFoundError: No module named 'api'`.

**One-line (Bash / Git Bash) – copy this exactly:**
```bash
cd backend
PYTHONPATH=src uv run uvicorn api.main:app --reload --port 8000
```

**Or use the run script (Bash):**
```bash
cd backend
./run.sh
```

**PowerShell:**
```powershell
cd backend
$env:PYTHONPATH="src"; uv run uvicorn api.main:app --reload --port 8000
```

Or run script: `.\run.ps1`

## Run tests

From `backend/` with `PYTHONPATH=src`:

**Bash / Git Bash:**
```bash
cd backend
PYTHONPATH=src uv run pytest tests -v
```

**PowerShell:**
```powershell
cd backend
$env:PYTHONPATH="src"; python -m pytest tests -v
```

Tests include: Goals API (POST/GET list/GET by id, validation, 404) and Judge unit tests (confidence and routing).

**Red→green demo:** To show failing tests, in `src/api/routers/goals.py` temporarily remove `"total": len(items)` from the GET list return. Run pytest — `test_get_goals_list_returns_items` fails (missing `total`). Restore the line and run again to see all pass.

## Endpoints

- `POST /api/v1/goals` – create goal (body: `{"description": "..."}`)
- `GET /api/v1/goals` – list goals
- `GET /api/v1/goals/{goal_id}` – get goal with tasks

See `specs/001-autonomous-influencer-network/contracts/` for full API contracts.

## Quickstart

See `specs/001-autonomous-influencer-network/quickstart.md`.
