# Architecture Strategy: Project Chimera

## Context: Before We Code, We Plan

This document outlines the core architectural choices for **Project Chimera**, an Autonomous Influencer Network designed for enterprise-grade, commercial autonomous agents. The architecture is derived directly from the Software Requirements Specification (SRS) and prioritizes **governance, reliability, scalability, and safe commercialization**.

---

## 1. Agent Pattern: Hierarchical Swarm (FastRender Swarm)

**Chosen Pattern: Planner–Worker–Judge**

Project Chimera adopts a **hierarchical, role-based swarm architecture**, explicitly defined in the SRS (Section 3.1). This pattern rejects monolithic agents in favor of specialized, decoupled roles that optimize throughput, fault tolerance, and decision quality.

| Component   | Role & Rationale                                                                                                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Planner** | Decomposes high-level business goals into concrete, executable task graphs (DAGs). Responsible for strategy formulation, task prioritization, and dynamic re-planning. |
| **Worker**  | Stateless, ephemeral agents that execute single atomic tasks (e.g., drafting captions, generating images). Optimized for parallel execution and efficient tool usage.  |
| **Judge**   | Governance and quality assurance layer. Reviews Worker outputs, applies Optimistic Concurrency Control (OCC), and manages Human-in-the-Loop (HITL) escalation.         |

**Rationale**
Hierarchical swarms enable Chimera to scale safely while maintaining brand consistency and operational control. By isolating planning, execution, and validation, the system can recover from failures, retry tasks intelligently, and enforce governance policies without halting the entire workflow.

---

## 2. Human-in-the-Loop (HITL) Safety Layer

**Location: Judge Service & Review Dashboard**

Human oversight is implemented as a first-class architectural concern, governed by the **Judge** agent and surfaced through a dedicated review interface.

### Escalation Framework

* **Trigger Mechanism**
  Each Worker action emits a `confidence_score` ranging from **0.0–1.0**, representing the system’s confidence in the output quality and safety.

* **Escalation Tiers**

  * **High Confidence (> 0.90):** Auto-approved with no human review.
  * **Medium Confidence (0.70–0.90):** Asynchronous human approval. The task is paused and routed to the Review Queue.
  * **Low Confidence (< 0.70):** Automatic reject/retry. The task is returned to the Planner for reprocessing.

* **Mandatory Review**
  Any task flagged by **Sensitive Topic Filters** (e.g., politics, health advice, regulated content) is always routed to human reviewers, regardless of confidence score.

* **Human Action**
  Reviewers interact via a streamlined dashboard to **approve, reject, or edit** agent-generated content.

**Rationale**
This confidence-based HITL model balances safety and scalability. High-quality outputs flow through automatically, while ambiguous or sensitive content receives human oversight, minimizing bottlenecks without compromising compliance or brand integrity.

---

## 3. Database Strategy: Hybrid SQL + NoSQL

Project Chimera handles high-velocity content generation and metadata storage by combining transactional and retrieval-optimized data stores.

| Database                         | Primary Use Case                                                                                                | Rationale                                                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **PostgreSQL (SQL)**             | Transactional, structured metadata (video ID, agent ID, campaign ID, publish timestamp, financial cost, status) | Provides ACID guarantees, aligns with existing SRS choices, and ensures integrity for financial and operational data. |
| **Weaviate (Vector DB / NoSQL)** | Semantic tags, embeddings, and rich metadata for search and retrieval                                           | Supports Retrieval-Augmented Generation (RAG), fast semantic queries, and leverages Chimera’s semantic memory layer.  |
| **Redis (In-Memory Cache)**      | Short-term, episodic memory during task execution                                                               | Reduces latency and supports rapid iteration within Planner–Worker workflows.                                         |

**Rationale**
This hybrid approach preserves correctness for critical records while enabling fast, flexible retrieval for agent reasoning and content reuse.

---

## 4. System Architecture Overview

### Core Responsibilities

* **Orchestrator**: Maintains global system state, lifecycle management, and high-level coordination.
* **Planner**: Reads goals and semantic context, decomposes work, and schedules tasks.
* **Worker**: Executes atomic tasks and interacts with external systems via MCP.
* **Judge**: Validates outputs, enforces governance rules, and manages HITL escalation.
* **HITL Review Dashboard**: Human interface for reviewing medium-confidence and sensitive outputs.

### External Interfaces

* **Model Context Protocol (MCP)**: Standardized, auditable interface for accessing external tools and resources.
* **External Platforms**: Social media networks, payment systems, and third-party services (e.g., Coinbase AgentKit).

---

## 4.1 Architectural Diagram (Logical Flow)

**Core System**
Orchestrator → Planner → Task Queue → Worker → Review Queue → Judge

**Data & Persistence Layer**

* Weaviate: Semantic Memory (RAG)
* PostgreSQL: Transactional Logs & Financial Data
* Redis: Episodic Cache

**External Interfaces**

* MCP → Social Media Platforms / AgentKit
* HITL Dashboard → Approve/Edit → External Platforms

---

## Key Flow Highlights

* The **Planner** reads semantic context from Weaviate and budget or campaign constraints from PostgreSQL.
* **Workers** execute tasks and interact with external systems exclusively through MCP.
* The **Judge** validates outputs, applies confidence-based HITL escalation, and persists approved results to Weaviate and PostgreSQL.
* **Human reviewers** approve, edit, or reject flagged content via the HITL Dashboard, with outcomes fed back into the planning loop.
* **Redis** supports low-latency task coordination and short-term memory during execution.

---

This architecture establishes Project Chimera as a governed, scalable orchestration layer for commercial autonomous agents, designed to integrate safely with external ecosystems while maintaining enterprise-grade control.
