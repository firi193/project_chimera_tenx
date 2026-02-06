# Implementation Plan: Autonomous Influencer Network

**Branch**: `001-autonomous-influencer-network` | **Date**: 2025-02-06 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/001-autonomous-influencer-network/spec.md`

## Summary

Build an autonomous influencer network with a hierarchical swarm (Planner, Worker, Judge), confidence-based HITL routing, and a human review dashboard. Goals are decomposed into task DAGs, executed by stateless Workers via MCP, and validated by Judge with escalation to a review queue. Transactional data in PostgreSQL, semantic memory in Weaviate, episodic cache in Redis; all external access via MCP.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI (orchestrator API), MCP SDK, Weaviate client, Redis client, asyncpg/SQLAlchemy (PostgreSQL)  
**Storage**: PostgreSQL (transactional metadata: campaigns, costs, status, publish logs); Weaviate (semantic memory, RAG); Redis (episodic/short-term cache during execution)  
**Testing**: pytest, pytest-asyncio, contract tests for API and MCP boundaries  
**Target Platform**: Linux server (orchestrator, agents); web (HITL dashboard)  
**Project Type**: web (backend orchestration + frontend dashboard)  
**Performance Goals**: Task throughput suitable for commercial campaigns; review queue latency under 5s for dashboard updates  
**Constraints**: Workers stateless; Judge and Planner decoupled; no direct external API calls outside MCP  
**Scale/Scope**: Multi-tenant campaigns; configurable confidence thresholds; single review dashboard (extensible)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Governance and Human Oversight | Every agent output reviewable and confidence-scored; routing by tier | PASS – Judge assigns confidence; routing to auto-approve / review queue / reject |
| II. Code Quality and Testing | Planner, Worker, Judge decoupled and independently testable | PASS – Separate services; no role bypass |
| III. Safety and Compliance | Sensitive/low-confidence content to human review; no auto-publish | PASS – HITL escalation; sensitive-topic always to dashboard |
| IV. Scalability and Reliability | Stateless Workers; fault-tolerant retries; separation of plan/execute/validate | PASS – Workers stateless; re-plan on failure; clear pipeline |
| V. Data Integrity | Transactional metadata in single source of truth (ACID); semantic/cache for retrieval only | PASS – PostgreSQL for transactional; Weaviate/Redis for RAG and cache |

No violations. Complexity Tracking table left empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-autonomous-influencer-network/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (/speckit.tasks – not created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # Domain entities (goal, task, output, review item)
│   ├── services/
│   │   ├── orchestrator/
│   │   ├── planner/
│   │   ├── worker/      # Stateless task execution via MCP
│   │   ├── judge/       # Validation, confidence, HITL routing
│   │   └── review/      # Review queue and feedback to planner
│   ├── api/             # REST API (goals, tasks, review queue, dashboard)
│   ├── mcp/             # MCP client adapters (social, payments, etc.)
│   └── storage/         # PostgreSQL, Weaviate, Redis access
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   ├── pages/          # HITL Review Dashboard
│   └── services/
└── tests/
```

**Structure Decision**: Backend holds orchestration, Planner, Worker, Judge, and MCP adapters; frontend is the HITL Review Dashboard. Single repo with backend (Python) and frontend (e.g. React or similar) for clear separation and independent deployment if needed.

## Complexity Tracking

Not applicable – no constitution violations.
