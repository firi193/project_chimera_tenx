# Data Model: Autonomous Influencer Network

**Feature**: 001-autonomous-influencer-network  
**Source**: spec.md entities and FR-008 (persistence for audit and recovery).

## Entities (Transactional – PostgreSQL)

### BusinessGoal

- **id** (PK), **created_at**, **updated_at**
- **operator_id** (who submitted)
- **description** (high-level goal text)
- **status**: draft | planned | in_progress | completed | failed
- **campaign_id** (optional FK to Campaign when linked to a campaign)

Validation: description non-empty. State: draft → planned → in_progress → completed | failed.

### Campaign

- **id** (PK), **created_at**, **updated_at**
- **name**, **external_id** (e.g. platform campaign id)
- **status**: active | paused | completed
- **cost_ceiling** (optional), **metadata** (JSON)

Used for campaigns, costs, and publish logs (constitution: transactional metadata).

### Task

- **id** (PK), **created_at**, **updated_at**
- **goal_id** (FK → BusinessGoal)
- **type**: planning | execution | validation
- **status**: pending | running | completed | failed | rejected
- **payload** (JSON, task-specific inputs)
- **retry_count**, **max_retries**
- **dependency_ids** (e.g. parent task ids for DAG)

Validation: goal_id required; status transitions enforced. State: pending → running → completed | failed | rejected.

### AgentOutput

- **id** (PK), **created_at**
- **task_id** (FK → Task)
- **content_type** (e.g. text, image_ref)
- **content_ref** (storage reference or inline for small content)
- **confidence_score** (0.0–1.0)
- **routing**: auto_approved | review_queue | rejected
- **sensitive_topic_flags** (array or JSON: e.g. politics, health)

Validation: confidence_score in [0, 1]; routing derived from score and sensitive_topic_flags (per constitution).

### ReviewQueueItem

- **id** (PK), **created_at**, **updated_at**
- **output_id** (FK → AgentOutput), **goal_id** (FK, denormalized for queries)
- **status**: pending | approved | rejected | edited
- **reviewed_at**, **reviewer_id**
- **edit_ref** (optional; reference to edited content if edited)

Validation: output must be in review_queue routing or sensitive_topic. State: pending → approved | rejected | edited.

### ReviewerAction

- **id** (PK), **created_at**
- **review_queue_item_id** (FK → ReviewQueueItem)
- **action**: approve | reject | edit
- **reviewer_id**, **comment** (optional)
- **edit_ref** (optional, when action = edit)

Stored for audit; influences whether content proceeds to publish or task is retried.

### PublishLog

- **id** (PK), **created_at**
- **output_id** (FK → AgentOutput), **campaign_id** (FK, optional)
- **platform**, **external_id**
- **status**: scheduled | published | failed
- **cost** (optional)

Transactional record for publish events (constitution: publish logs in single source of truth).

## Semantic / Cache (Non-Transactional)

- **Weaviate**: Semantic memory and RAG (goal context, past outputs, tags). No system-of-record for financial or operational commitments; used for retrieval and context only.
- **Redis**: Episodic/short-term cache during execution (e.g. current run context, task results for same run). TTL-based; not authoritative for persistence.

## Relationships (Summary)

- BusinessGoal 1 → N Task
- Task 1 → N AgentOutput
- AgentOutput 0..1 → ReviewQueueItem (when routing = review_queue or sensitive)
- ReviewQueueItem 1 → N ReviewerAction (audit)
- AgentOutput 0..N → PublishLog
- Campaign 1 → N BusinessGoal (optional); Campaign 1 → N PublishLog

## State Transitions (Key)

- **Goal**: draft → planned (when plan created) → in_progress (when tasks run) → completed | failed
- **Task**: pending → running → completed | failed | rejected (rejected when output rejected or low confidence)
- **ReviewQueueItem**: pending → approved | rejected | edited
