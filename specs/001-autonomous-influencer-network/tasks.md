# Tasks: Autonomous Influencer Network

**Input**: Design documents from `specs/001-autonomous-influencer-network/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not requested in feature specification; no test tasks included.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3) for story phases only
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure per plan

- [x] T001 Create backend and frontend directory structure per plan in backend/ and frontend/
- [x] T002 Initialize Python 3.11+ project with pyproject.toml and dependencies (FastAPI, MCP SDK, Weaviate client, Redis client, asyncpg/SQLAlchemy) in backend/
- [x] T003 Initialize frontend project (e.g. React/Vite or chosen stack) in frontend/
- [x] T004 [P] Configure ruff and formatting for backend in backend/pyproject.toml or backend/ruff.toml
- [x] T005 [P] Add environment and config placeholder (e.g. .env.example, config module) in backend/src/storage/ or backend/config/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story. No user story work can begin until this phase is complete.

- [x] T006 Setup PostgreSQL schema and migrations framework in backend/ (e.g. Alembic or SQLAlchemy migrations)
- [x] T007 Configure Weaviate client and schema for semantic memory in backend/src/storage/weaviate_client.py
- [x] T008 Configure Redis client for episodic cache in backend/src/storage/redis_client.py
- [x] T009 [P] Create BusinessGoal model in backend/src/models/business_goal.py
- [x] T010 [P] Create Campaign model in backend/src/models/campaign.py
- [x] T011 [P] Create Task model in backend/src/models/task.py
- [x] T012 [P] Create AgentOutput model in backend/src/models/agent_output.py
- [x] T013 Implement PostgreSQL repository layer for goals, tasks, outputs (CRUD) in backend/src/storage/postgres_repository.py
- [x] T014 Add error handling and structured logging in backend (e.g. backend/src/api/middleware/ or backend/src/services/)
- [x] T015 Setup API routing and FastAPI app skeleton with /api/v1 prefix in backend/src/api/main.py

**Checkpoint**: Foundation ready – user story implementation can begin.

---

## Phase 3: User Story 1 – Goal to Executed Tasks with Confidence-Based Routing (Priority: P1) – MVP

**Goal**: Operator submits a goal; system produces task plan, executes tasks via Planner/Worker/Judge, assigns confidence and routes outputs (auto-approve / review queue / reject). Pipeline stages observable.

**Independent Test**: Submit one business goal; verify task plan produced, tasks executed, each output has confidence score and correct routing; pipeline stages visible via API.

- [x] T016 [US1] Implement MCP client adapter layer (invoke tools via MCP only) in backend/src/mcp/client.py
- [x] T017 [US1] Implement Planner service: decompose goal into task DAG, read from semantic memory and transactional DB in backend/src/services/planner/service.py
- [x] T018 [US1] Implement Worker service: stateless single-task execution via MCP only in backend/src/services/worker/service.py
- [x] T019 [US1] Implement Judge service: validate output, assign confidence score, apply routing (auto_approved / review_queue / rejected) per thresholds in backend/src/services/judge/service.py
- [x] T020 [US1] Implement confidence threshold configuration (e.g. high > 0.90, medium 0.70–0.90, low < 0.70) in backend config or backend/src/services/judge/config.py
- [x] T021 [US1] Implement Orchestrator service: coordinate plan → task queue → execute → route (call Planner, dispatch tasks to Worker, pass outputs to Judge) in backend/src/services/orchestrator/service.py
- [x] T022 [US1] Implement Goals API – POST /api/v1/goals (create goal, trigger orchestration), GET /api/v1/goals (list), GET /api/v1/goals/{goal_id} (goal with tasks) per contracts/api-goals.yaml in backend/src/api/goals.py
- [x] T023 [US1] Persist goal and task status updates so pipeline stages (plan, task queue, execute, review/approve) are queryable in backend/src/storage/postgres_repository.py and/or backend/src/api/goals.py

**Checkpoint**: User Story 1 independently testable – submit goal, see tasks and confidence-based routing.

---

## Phase 4: User Story 2 – Human Review for Medium-Confidence and Sensitive Content (Priority: P2)

**Goal**: Medium-confidence and sensitive-topic outputs go to review queue; reviewers use dashboard to approve, reject, or edit; actions recorded and affect publish or retry.

**Independent Test**: Place medium-confidence and sensitive-topic items in queue; resolve via dashboard; verify outcomes recorded and sensitive content never auto-approved.

- [ ] T024 [P] [US2] Create ReviewQueueItem model in backend/src/models/review_queue_item.py
- [ ] T025 [P] [US2] Create ReviewerAction model in backend/src/models/reviewer_action.py
- [ ] T026 [US2] Add ReviewQueueItem and ReviewerAction to migrations and repository in backend/src/storage/postgres_repository.py
- [ ] T027 [US2] Implement Judge integration: create ReviewQueueItem when routing is review_queue or sensitive_topic in backend/src/services/judge/service.py
- [ ] T028 [US2] Implement Review service: list queue, get item, submit approve/reject/edit and persist ReviewerAction in backend/src/services/review/service.py
- [ ] T029 [US2] Implement Review API – GET /api/v1/review/queue, GET /api/v1/review/queue/{item_id}, PATCH /api/v1/review/queue/{item_id} per contracts/api-review.yaml in backend/src/api/review.py
- [ ] T030 [US2] Build HITL Review Dashboard – list pending items, view item detail, approve/reject/edit actions in frontend/src/pages/review/ (e.g. list page and detail page)
- [ ] T031 [US2] Connect dashboard to Review API and persist reviewer actions with feedback path (e.g. approved → publish path; rejected → retry path) in frontend/src/services/review_api.ts or .js and backend/src/services/review/service.py

**Checkpoint**: User Stories 1 and 2 independently testable – goals pipeline plus review dashboard.

---

## Phase 5: User Story 3 – Re-Plan and Retry on Failure or Rejection (Priority: P3)

**Goal**: On task failure or output rejection, notify Planner; support re-plan or revised tasks re-entering pipeline; retry limits and operator visibility.

**Independent Test**: Trigger failure or rejection; verify Planner notified, new/revised tasks re-enter pipeline; operator can see status without manual reassembly.

- [ ] T032 [US3] Implement failure/rejection notification to Planner (when task fails or output rejected) in backend/src/services/orchestrator/service.py
- [ ] T033 [US3] Implement re-plan and task re-entry: Planner produces new or revised tasks that re-enter task queue in backend/src/services/planner/service.py and backend/src/services/orchestrator/service.py
- [ ] T034 [US3] Add retry limits and surface repeated failures to operator (e.g. goal status or alert) per spec edge case in backend/src/services/orchestrator/service.py and backend/src/models/task.py

**Checkpoint**: All three user stories independently functional; pipeline recovers from failure/rejection.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting improvements and validation

- [ ] T035 [P] Add PublishLog model and optional publish-path stub (for approved content) in backend/src/models/publish_log.py
- [ ] T036 [P] Documentation: update README with run instructions and link to quickstart in docs/ or README.md
- [ ] T037 Run quickstart.md validation (start services, submit goal, use dashboard, trigger retry)
- [ ] T038 Security hardening: ensure review API and dashboard use auth where required; validate inputs in backend/src/api/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies – start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 – BLOCKS all user stories.
- **Phase 3 (US1)**: Depends on Phase 2 – MVP.
- **Phase 4 (US2)**: Depends on Phase 2; integrates with US1 (review queue fed by Judge).
- **Phase 5 (US3)**: Depends on Phase 2; integrates with US1/US2 (re-plan and retry).
- **Phase 6 (Polish)**: Depends on Phases 3–5 as needed.

### User Story Dependencies

- **US1 (P1)**: After Foundational only – no dependency on US2/US3.
- **US2 (P2)**: After Foundational; consumes Judge output (US1); independently testable.
- **US3 (P3)**: After Foundational; extends Orchestrator and Planner; independently testable.

### Parallel Opportunities

- Phase 1: T004, T005 [P]. Phase 2: T009–T012 [P] (models). Phase 3: T016–T020 can be parallelized where files differ. Phase 4: T024–T025 [P]; T030 and backend tasks can proceed in parallel once API exists. Phase 6: T035, T036 [P].

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup  
2. Complete Phase 2: Foundational  
3. Complete Phase 3: User Story 1  
4. **STOP and VALIDATE**: Run quickstart steps for goal submit and pipeline visibility.  
5. Deploy/demo if ready.

### Incremental Delivery

1. Setup + Foundational → foundation ready.  
2. Add US1 → test goal → tasks → confidence routing (MVP).  
3. Add US2 → test review queue and dashboard.  
4. Add US3 → test re-plan and retry.  
5. Polish and quickstart validation.

---

## Notes

- Each task has checkbox, Task ID, optional [P], optional [USn], and file path(s).
- No test tasks: spec did not request TDD or explicit test tasks.
- Backend paths under `backend/src/`; frontend under `frontend/src/`.
- Commit after each task or logical group; validate at each checkpoint.
