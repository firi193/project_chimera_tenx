# Local dev and testing (Bash)

All commands below are for **Bash** (e.g. Git Bash on Windows). Run from repo root: `c:\Users\HP\Documents\project_chimera` (or `~/Documents/project_chimera` in Bash).

---

## 1. Backend: set Python path and start the API

```bash
cd backend
export PYTHONPATH=src
uv run uvicorn api.main:app --reload --port 8000
```

Or with `python`:

```bash
cd backend
export PYTHONPATH=src
python -m uvicorn api.main:app --reload --port 8000
```

Leave this terminal running. In another terminal, run the test commands below.

---

## 2. Test goals API (curl)

**Create a goal** (expect 201 and a goal object with `id`):

```bash
curl -s -X POST http://localhost:8000/api/v1/goals \
  -H "Content-Type: application/json" \
  -d '{"description": "My first goal"}' | jq .
```

**List goals** (expect `{"items": [...], "next_cursor": null}`):

```bash
curl -s http://localhost:8000/api/v1/goals | jq .
```

**Get one goal** (replace `{goal_id}` with the `id` from the create response):

```bash
curl -s http://localhost:8000/api/v1/goals/{goal_id} | jq .
```

If you don’t have `jq`, omit `| jq .` to see raw JSON.

---

## 3. Frontend

In a **new** terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL it prints (e.g. `http://localhost:5173`) and confirm the Chimera HITL dashboard page loads.

---

## 4. Confirm routing

With the backend running, the Goals API is at `/api/v1/goals`. The frontend Vite config proxies `/api` to port 8000, so `fetch('/api/v1/goals')` in the app will hit the backend.

---

## 5. Continue with T016–T023 (MCP, Planner, Worker, Judge, Orchestrator)

**Option A – You implement**

- Open `specs/001-autonomous-influencer-network/tasks.md` and do T016–T023 in order.
- Use:
  - `specs/001-autonomous-influencer-network/plan.md` – structure and tech stack
  - `specs/001-autonomous-influencer-network/contracts/api-goals.yaml` – goals API
  - `specs/001-autonomous-influencer-network/data-model.md` – entities

Tasks summary:

| Task | What to implement |
|------|--------------------|
| T016 | `backend/src/mcp/client.py` – invoke tools via MCP only |
| T017 | `backend/src/services/planner/service.py` – goal → task DAG, read semantic + DB |
| T018 | `backend/src/services/worker/service.py` – stateless, run one task via MCP |
| T019 | `backend/src/services/judge/service.py` – validate output, confidence, route |
| T020 | Confidence config (e.g. `backend/src/config.py` or `backend/src/services/judge/config.py`) |
| T021 | `backend/src/services/orchestrator/service.py` – Planner → task queue → Worker → Judge |
| T022 | In `backend/src/api/routers/goals.py`, on POST goal call orchestrator (create plan and run pipeline) |
| T023 | Persist goal/task status so GET goal returns up-to-date pipeline stages |

**Option B – Agent implements**

In Cursor chat, run:

```text
/speckit.implement Continue from T016: implement MCP client, Planner, Worker, Judge, Orchestrator, wire goal creation to the pipeline (T016–T023).
```

or:

```text
/speckit.implement Implement tasks T016 through T023 from tasks.md.
```

If the agent redoes T001–T015, say: *"T001–T015 are already done; only implement T016–T023 and mark those complete."*

---

## 6. Run /speckit.implement again from T016

1. In Cursor, open the project (where `specs/` and `backend/` live).
2. In AI chat run:
   - `/speckit.implement Continue from T016: implement MCP client, Planner, Worker, Judge, Orchestrator, wire goal creation to the pipeline (T016–T023).`
   - or: `/speckit.implement Implement tasks T016 through T023 from tasks.md.`
3. The command will read `tasks.md` and run the next tasks (T016–T023).
4. If it starts from T001 again, reply: *"T001–T015 are already done; only implement T016–T023 and mark those complete."* Or confirm in `specs/001-autonomous-influencer-network/tasks.md` that T001–T015 are `[x]`, then run the command again.
