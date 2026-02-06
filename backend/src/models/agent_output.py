from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AgentOutputBase(BaseModel):
    task_id: UUID
    content_type: str = "text"
    content_ref: str | None = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    routing: str = Field(
        ..., pattern="^(auto_approved|review_queue|rejected)$"
    )
    sensitive_topic_flags: list[str] | None = None


class AgentOutput(AgentOutputBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
