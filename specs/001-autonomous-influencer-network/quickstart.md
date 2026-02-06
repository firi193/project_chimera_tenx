# Quickstart: Autonomous Influencer Network (001-autonomous-influencer-network)

**Purpose**: Validate the feature end-to-end after implementation. Use this to verify pipeline, HITL, and re-plan/retry behavior.

## Prerequisites

- Python 3.11+ environment
- PostgreSQL, Weaviate, Redis running (or use provided docker-compose if added)
- MCP server(s) configured for external tools (e.g. social, payments)
- Backend and frontend (HITL dashboard) built and runnable

## 1. Start Services

```bash
# From repo root
# Start data stores (example – adjust to project layout)
# docker-compose up -d postgres weaviate redis

# Start backend (orchestrator, planner, worker, judge, API)
cd backend && uv run uvicorn src.api.main:app --reload

# In another terminal: start frontend (HITL dashboard)
cd frontend && npm run dev
```

## 2. Submit a Business Goal (User Story 1)

- **Action**: POST `/api/v1/goals` with body `{"description": "Create a short campaign post for product X launch next week"}`.
- **Expected**: 201 with goal id; goal status becomes `planned` then `in_progress`; tasks appear (planning, then execution); each output has `confidence_score` and `routing` (auto_approved, review_queue, or rejected).
- **Check**: GET `/api/v1/goals/{goal_id}` shows tasks and their statuses; pipeline stages (plan → task queue → execute → review queue or approval) are observable.

## 3. Human Review (User Story 2)

- **Action**: Open HITL dashboard; filter review queue by `pending`. Open one item; choose Approve or Reject (or Edit if implemented).
- **Expected**: Item status updates to approved/rejected/edited; action is persisted; approved content can proceed toward publish; rejected content can trigger retry path.
- **Check**: Sensitive-topic content never appears as auto-approved; all such items appear in review queue.

## 4. Re-Plan / Retry (User Story 3)

- **Action**: Trigger a failure (e.g. invalid task payload or mock MCP failure) or reject an output from the dashboard.
- **Expected**: Failure or rejection is communicated to Planner; new or revised tasks are produced and re-enter the pipeline; GET `/api/v1/goals/{goal_id}` still shows coherent pipeline stages.
- **Check**: No manual reassembly of workflow required; operator can see status of goal and tasks at each stage.

## 5. Constitution Checks

- **Governance**: Every agent output has a confidence score and routing; no sensitive-topic auto-approve.
- **Decoupling**: Planner, Worker, Judge are separate; Workers use MCP only.
- **Data integrity**: Transactional data (goals, tasks, review decisions, publish logs) in PostgreSQL; semantic/cache in Weaviate/Redis for retrieval and short-term state only.

## Success Criteria Mapping

| Criterion | How to verify |
|----------|----------------|
| SC-001 Goal to outcome in timeframe | Submit goal; confirm executed tasks and routing within session/SLA |
| SC-002 100% sensitive-topic to review | Create content tagged sensitive; confirm it never has routing auto_approved |
| SC-003 Reviewers resolve via dashboard | Resolve several queue items via UI; confirm no workarounds needed |
| SC-004 Re-plan/retry cycle | Cause failure or rejection; confirm one retry cycle without manual reassembly |
| SC-005 Observable pipeline stages | Inspect goal and tasks; confirm plan, task queue, execute, review, approve/reject are distinguishable |
