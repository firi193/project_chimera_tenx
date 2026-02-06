from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1)
    external_id: str | None = None
    status: str = Field(..., pattern="^(active|paused|completed)$")
    cost_ceiling: float | None = None
    metadata: dict | None = None


class Campaign(CampaignBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
