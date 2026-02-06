"""Planner service (T017): decompose goal into task DAG, read from semantic memory and transactional DB."""
from __future__ import annotations

from uuid import UUID

from storage import postgres_repository as repo


async def plan_goal(goal_id: UUID) -> list[dict]:
    """Produce a task DAG for the goal. Creates planning and execution tasks and returns them.

    Reads goal from repository; Weaviate/Redis can be added for semantic context.
    """
    goal = await repo.get_goal(goal_id)
    if not goal:
        return []

    planning = await repo.create_task(
        goal_id=goal_id,
        type="planning",
        payload={"goal_description": goal["description"]},
    )
    execution = await repo.create_task(
        goal_id=goal_id,
        type="execution",
        payload={"plan_ref": str(planning["id"])},
        dependency_ids=[planning["id"]],
    )
    return [planning, execution]
