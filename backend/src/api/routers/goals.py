from uuid import UUID

from fastapi import APIRouter, HTTPException

from services.orchestrator import service as orchestrator
from storage.postgres_repository import (
    create_goal,
    get_goal,
    list_goals,
    get_tasks_for_goal,
    get_outputs_for_goal,
)

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", status_code=201)
async def post_goal(body: dict):
    description = body.get("description")
    if not description or not str(description).strip():
        raise HTTPException(status_code=400, detail="description is required")
    campaign_id = body.get("campaign_id")
    goal = await create_goal(
        description=str(description).strip(),
        operator_id=body.get("operator_id"),
        campaign_id=UUID(campaign_id) if campaign_id else None,
    )
    await orchestrator.run(goal["id"])
    return await get_goal(goal["id"]) or goal


@router.get("")
async def get_goals_list(status: str | None = None, limit: int = 20):
    items = await list_goals(status=status, limit=limit)
    return {"items": items, "next_cursor": None, "total": len(items)}


@router.get("/{goal_id}")
async def get_goal_by_id(goal_id: UUID):
    goal = await get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    tasks = await get_tasks_for_goal(goal_id)
    outputs = await get_outputs_for_goal(goal_id)
    output_by_task = {o["task_id"]: o for o in outputs}
    task_list = []
    for t in tasks:
        out = output_by_task.get(t["id"])
        task_list.append({
            "id": t["id"],
            "type": t["type"],
            "status": t["status"],
            "output": {"confidence_score": out["confidence_score"], "routing": out["routing"]} if out else None,
        })
    return {**goal, "tasks": task_list}
