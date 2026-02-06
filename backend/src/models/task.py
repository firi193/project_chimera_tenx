from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    goal_id: UUID
    type: str = Field(..., pattern="^(planning|execution|validation)$")
    payload: dict | None = None
    retry_count: int = 0
    max_retries: int = 3
    dependency_ids: list[UUID] | None = None


class Task(TaskBase):
    id: UUID
    status: str = Field(
        ..., pattern="^(pending|running|completed|failed|rejected)$"
    )
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskSummary(BaseModel):
    id: UUID
    type: str
    status: str
