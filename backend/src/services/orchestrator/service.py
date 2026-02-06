"""Orchestrator service (T021): coordinate plan → task queue → execute → route."""
from __future__ import annotations

from uuid import UUID

from services.judge import service as judge_service
from services.planner import service as planner_service
from services.worker import service as worker_service
from storage import postgres_repository as repo


async def run(goal_id: UUID) -> None:
    """Run the pipeline for a goal: plan, execute tasks, judge outputs, persist."""
    goal = await repo.get_goal(goal_id)
    if not goal:
        return
    await repo.update_goal_status(goal_id, "planned")
    tasks = await planner_service.plan_goal(goal_id)
    if not tasks:
        await repo.update_goal_status(goal_id, "failed")
        return
    await repo.update_goal_status(goal_id, "in_progress")

    for task in tasks:
        await repo.update_task_status(task["id"], "running")
        try:
            output_result = await worker_service.execute_task(task["id"])
        except Exception:
            await repo.update_task_status(task["id"], "failed")
            continue
        content_ref = output_result.get("content_ref") or ""
        sensitive = output_result.get("sensitive_topic_flags") or []
        confidence, routing = judge_service.evaluate(content_ref, sensitive)
        await repo.create_output(
            task_id=task["id"],
            content_type=output_result.get("content_type", "text"),
            content_ref=content_ref,
            confidence_score=confidence,
            routing=routing,
            sensitive_topic_flags=sensitive,
        )
        await repo.update_task_status(task["id"], "completed")
    await repo.update_goal_status(goal_id, "completed")
