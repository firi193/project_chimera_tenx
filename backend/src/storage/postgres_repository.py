"""PostgreSQL repository layer - CRUD for goals, tasks, outputs.

Migrations and async engine setup (T006) to be added; this module provides
the interface and in-memory stub for development.
"""
from datetime import datetime
from uuid import UUID, uuid4

# In-memory stub until T006 migrations and engine are in place
_goals: dict[UUID, dict] = {}
_tasks: dict[UUID, dict] = {}
_outputs: dict[UUID, dict] = {}


async def create_goal(description: str, operator_id: str | None = None, campaign_id: UUID | None = None) -> dict:
    goal_id = uuid4()
    now = datetime.utcnow()
    _goals[goal_id] = {
        "id": goal_id,
        "description": description,
        "operator_id": operator_id,
        "campaign_id": campaign_id,
        "status": "draft",
        "created_at": now,
        "updated_at": now,
    }
    return _goals[goal_id]


async def get_goal(goal_id: UUID) -> dict | None:
    return _goals.get(goal_id)


async def list_goals(status: str | None = None, limit: int = 20) -> list[dict]:
    out = list(_goals.values())
    if status:
        out = [g for g in out if g["status"] == status]
    return out[:limit]


async def update_goal_status(goal_id: UUID, status: str) -> None:
    if goal_id in _goals:
        _goals[goal_id]["status"] = status
        _goals[goal_id]["updated_at"] = datetime.utcnow()


async def create_task(
    goal_id: UUID,
    type: str,
    payload: dict | None = None,
    dependency_ids: list[UUID] | None = None,
) -> dict:
    task_id = uuid4()
    now = datetime.utcnow()
    _tasks[task_id] = {
        "id": task_id,
        "goal_id": goal_id,
        "type": type,
        "status": "pending",
        "payload": payload or {},
        "retry_count": 0,
        "max_retries": 3,
        "dependency_ids": list(dependency_ids or []),
        "created_at": now,
        "updated_at": now,
    }
    return _tasks[task_id]


async def get_task(task_id: UUID) -> dict | None:
    return _tasks.get(task_id)


async def get_tasks_for_goal(goal_id: UUID) -> list[dict]:
    return [t for t in _tasks.values() if t["goal_id"] == goal_id]


async def update_task_status(task_id: UUID, status: str) -> None:
    if task_id in _tasks:
        _tasks[task_id]["status"] = status
        _tasks[task_id]["updated_at"] = datetime.utcnow()


async def create_output(
    task_id: UUID,
    content_type: str,
    content_ref: str | None,
    confidence_score: float,
    routing: str,
    sensitive_topic_flags: list[str] | None = None,
) -> dict:
    output_id = uuid4()
    now = datetime.utcnow()
    _outputs[output_id] = {
        "id": output_id,
        "task_id": task_id,
        "content_type": content_type,
        "content_ref": content_ref,
        "confidence_score": confidence_score,
        "routing": routing,
        "sensitive_topic_flags": sensitive_topic_flags or [],
        "created_at": now,
    }
    return _outputs[output_id]


async def get_outputs_for_goal(goal_id: UUID) -> list[dict]:
    """Return all outputs for tasks belonging to this goal (for pipeline visibility)."""
    task_ids = {t["id"] for t in _tasks.values() if t["goal_id"] == goal_id}
    return [o for o in _outputs.values() if o["task_id"] in task_ids]
