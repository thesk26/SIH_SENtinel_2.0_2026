from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.behavior import BehaviorCollect


class ExplanationLevel(str, Enum):
    USER_SAFE = "USER_SAFE"
    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"


class SecurityAnalyzeRequest(BehaviorCollect):
    browser: str = Field(default="unknown", max_length=100)
    operating_system: str = Field(default="unknown", max_length=100)
    ip_reputation_score: float = Field(default=100, ge=0, le=100)
    is_vpn_or_proxy: bool = False
    network_changed: bool = False
    requested_explanation_level: ExplanationLevel = ExplanationLevel.USER_SAFE


class SecurityAnalysisResponse(BaseModel):
    user_id: str
    integrity_score: float
    decision: str
    signal_scores: dict[str, float]
    conflicts_detected: list[str]
    explanation: dict


class SecurityEventRead(SecurityAnalysisResponse):
    id: str
    timestamp: datetime
