# Project Chimera

Autonomous Influencer Network — goals become tasks, agents execute and get judged, outputs are confidence-routed (auto-approve / human review / reject). Human review via the HITL Dashboard.

## What you can run right now

### 1. Backend (Goals API)

From repo root in **Bash** (e.g. Git Bash):

```bash
cd backend
export PYTHONPATH=src
uv run uvicorn api.main:app --reload --port 8000
```

Or use the script:

```bash
./scripts/start-backend.sh
```

### 2. Frontend (HITL Review Dashboard)

In a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

Or:

```bash
./scripts/start-frontend.sh
```

Open the URL shown (e.g. **http://localhost:5173**).

### 3. Where to see “trails” of influencing

| What | Where |
|------|--------|
| **Goals you create** | **API**: `GET http://localhost:8000/api/v1/goals` or open **http://localhost:8000/docs** and try the goals endpoints. |
| **One goal and its tasks** | **API**: `GET http://localhost:8000/api/v1/goals/{goal_id}` — today `tasks` is empty until the pipeline is wired. |
| **Dashboard** | **Frontend**: http://localhost:5173 — Home and Review Queue (queue fills when the Review API and Judge are implemented). |

**Create a goal (example):**

```bash
curl -s -X POST http://localhost:8000/api/v1/goals \
  -H "Content-Type: application/json" \
  -d '{"description": "Launch product X campaign next week"}'
```

Then list goals and get that goal by `id` to see the record (the “trail” of that goal).

---

## Full “AI Influencer” pipeline and full trails

Right now, **creating a goal only stores it**. You get:

- Trails of **goals** (create/list/get) and a **dashboard** shell.

You do **not** yet get:

- **Task plan** from the goal (Planner)
- **Execution** by Workers (via MCP)
- **Confidence scores** and **routing** (Judge): auto-approve / review queue / reject
- **Review queue** items and approve/reject/edit in the UI

Those need **T016–T023** (Orchestrator, Planner, Worker, Judge, MCP client, Goals API wired to the pipeline). After that, the same flow will give you:

- **Trails**: goal → tasks (with status) → agent outputs (with confidence and routing) → review queue items when applicable.

To have the agent implement the pipeline:

```text
/speckit.implement Implement tasks T016 through T023 from tasks.md.
```

See **docs/local-dev-bash.md** and **specs/001-autonomous-influencer-network/tasks.md** for the full task list.

---

## Repo layout

- **backend/** — FastAPI app, goals API, (future) Planner, Worker, Judge, Review API
- **frontend/** — HITL Review Dashboard (React + Vite)
- **specs/001-autonomous-influencer-network/** — spec, plan, data model, contracts, tasks
- **scripts/** — start-backend.sh, start-frontend.sh, test-goals-api.sh

Architecture: **architecture.md**  
Constitution: **.specify/memory/constitution.md**
