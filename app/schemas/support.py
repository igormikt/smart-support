from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Confidence(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class SupportRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class SupportResult(BaseModel):
    category: str
    summary: str
    priority: Priority
    next_action: str
    fields: dict[str, Any] = Field(default_factory=dict)
    confidence: Confidence
    escalate: bool


class IngestResponse(SupportResult):
    status: str
    audit_id: int
