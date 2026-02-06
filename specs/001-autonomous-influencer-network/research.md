# Research: Autonomous Influencer Network (Phase 0)

**Feature**: 001-autonomous-influencer-network  
**Purpose**: Resolve technical context and document decisions for Planner–Worker–Judge swarm, data stores, and MCP.

## 1. Hierarchical Swarm (Planner–Worker–Judge)

- **Decision**: Use three distinct roles: Planner (goal → task DAG, reads semantic + transactional state), Worker (stateless, single-task execution via MCP only), Judge (validates outputs, assigns confidence, applies HITL routing).
- **Rationale**: Aligns with constitution (decoupled, independently testable); enables scaling and fault isolation; clear audit trail.
- **Alternatives considered**: Monolithic agent (rejected – violates separation); two roles only (rejected – validation and routing need dedicated component).

## 2. Confidence Thresholds and HITL Routing

- **Decision**: Use constitution thresholds: high > 0.90 → auto-approve; medium 0.70–0.90 → human review queue; low < 0.70 → reject and return to Planner for retry. Sensitive-topic content always → review queue.
- **Rationale**: Constitution already defines escalation tiers; implementation will make thresholds configurable.
- **Alternatives considered**: Fixed thresholds in code (rejected – policy must be configurable); different bands (deferred to config).

## 3. Data Stores: PostgreSQL, Weaviate, Redis

- **Decision**: PostgreSQL for transactional metadata (campaigns, costs, status, publish logs, goals, tasks, review decisions); Weaviate for semantic memory and RAG; Redis for episodic/short-term cache during execution.
- **Rationale**: Matches architecture and constitution (single source of truth for transactional; semantic/cache for retrieval and short-term state only).
- **Alternatives considered**: Single DB for everything (rejected – different consistency and query needs); other vector DBs (Weaviate chosen for RAG/semantic use in spec).

## 4. Model Context Protocol (MCP) for External Access

- **Decision**: All external access (social platforms, payments, e.g. Coinbase AgentKit) goes through MCP. Workers call MCP only; no direct third-party SDKs in Worker code.
- **Rationale**: Auditable, standardized interface; keeps Workers stateless and tool-agnostic.
- **Alternatives considered**: Direct API clients in Workers (rejected – constitution and architecture require MCP); multiple protocols (rejected – MCP as single integration surface).

## 5. HITL Review Dashboard

- **Decision**: Dedicated dashboard (frontend) that consumes review queue from backend API; reviewer actions (approve, reject, edit) persisted and fed back into planning loop.
- **Rationale**: Spec and constitution require dedicated review interface and feedback to planning.
- **Alternatives considered**: CLI-only review (rejected – spec requires dashboard); external tool (rejected – feedback loop must be in-system).

## 6. Re-Plan and Retry on Failure

- **Decision**: Failed tasks or rejected outputs trigger notification to Planner; Planner can produce new or revised tasks that re-enter the task queue. No automatic infinite retry without operator visibility.
- **Rationale**: Spec and constitution require re-plan/retry and observable pipeline; edge case (repeated failures) requires escalation to operator.
- **Alternatives considered**: Automatic retry with no cap (rejected – edge case); manual-only retry (accepted as optional mode; automatic retry supported as primary).

All NEEDS CLARIFICATION from Technical Context have been resolved via architecture and user input. No open research items.
