"""
Pydantic schemas for ScamGuard AI
"""

from pydantic import BaseModel, Field


class ScamAnalysis(BaseModel):

    classification: str = Field(
        description="Scam, Not Scam, or Uncertain"
    )

    intent_type: str = Field(
        description="Detected scam intent"
    )

    risk_score: int = Field(
        ge=0,
        le=100
    )

    reason: str

    safe_action: str