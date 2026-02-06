from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BusinessGoalBase(BaseModel):
    description: str = Field(..., min_length=1)
    campaign_id: UUID | None = None


class BusinessGoalCreate(BusinessGoalBase):
    operator_id: str | None = None


class BusinessGoal(BusinessGoalBase):
    id: UUID
    operator_id: str | None = None
    status: str = Field(..., pattern="^(draft|planned|in_progress|completed|failed)$")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
