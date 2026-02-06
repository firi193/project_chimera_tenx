<!--
Sync Impact Report
Version change: (template/placeholder) → 1.0.0
Modified principles: N/A (initial adoption)
Added sections: Core Principles (5), Safety and HITL, Development Workflow, Governance
Removed sections: None
Templates: plan-template.md ✅ (Constitution Check aligns); spec-template.md ✅ (no new constraints); tasks-template.md ✅ (task types align)
Follow-up TODOs: None
-->

# Project Chimera Constitution

## Core Principles

### I. Governance and Human Oversight

Every agent output MUST be reviewable and MUST carry a confidence score. The system MUST support routing outputs by confidence tier (auto-approve, human review queue, or reject/retry). Rationale: Ensures traceability and enables Human-in-the-Loop (HITL) as a first-class control.

### II. Code Quality and Testing

Planner, Worker, and Judge components MUST be decoupled and independently testable. No component MAY bypass boundaries (e.g., Workers must not perform planning; Judge must not execute tasks). Rationale: Enables safe scaling, clear fault isolation, and regression testing per role.

### III. Safety and Compliance

Sensitive or low-confidence content MUST NOT auto-publish and MUST go through the human review queue. Content flagged by sensitive-topic filters (e.g., politics, health advice, regulated domains) MUST always require human review regardless of confidence score. Rationale: Reduces compliance and brand risk while keeping high-confidence flows efficient.

### IV. Scalability and Reliability

Workers MUST be stateless and ephemeral. The system MUST support fault-tolerant task retries and clear separation between planning, execution, and validation. Orchestration MUST allow re-planning on failure without corrupting shared state. Rationale: Supports throughput and resilience without sacrificing governance.

### V. Data Integrity

Transactional metadata (e.g., campaign ID, costs, status, publish logs) MUST live in a single source of truth with ACID guarantees. Semantic memory and caches MUST be used only for retrieval and short-term state, not as the system of record for financial or operational commitments. Rationale: Ensures auditability and correctness for commercial and compliance needs.

## Safety and Human-in-the-Loop Requirements

- **Escalation tiers**: High confidence (>0.90) → auto-approved; medium (0.70–0.90) → human review queue; low (<0.70) → reject and return to Planner for retry.
- **Mandatory review**: Any output flagged by sensitive-topic filters MUST be routed to human reviewers regardless of confidence.
- **Human actions**: Reviewers MUST be able to approve, reject, or edit agent-generated content via a dedicated review interface; outcomes MUST feed back into the planning loop.

## Development Workflow

- All implementation plans MUST include a Constitution Check section; gates MUST pass before Phase 0 research and after Phase 1 design.
- PRs and design reviews MUST verify compliance with these principles; violations require explicit justification and documentation in the plan.
- Task breakdown MUST reflect principle-driven categories (e.g., testing per component, observability, data integrity checks) where applicable.

## Governance

This constitution supersedes ad-hoc practices for Project Chimera. Amendments require: (1) documentation of the change and rationale, (2) version bump per semantic versioning (MAJOR for removals/redefinitions, MINOR for new principles/sections, PATCH for clarifications), (3) update of LAST_AMENDED_DATE. Compliance MUST be reviewed when adopting new features or changing architecture.

**Version**: 1.0.0 | **Ratified**: 2025-02-06 | **Last Amended**: 2025-02-06
