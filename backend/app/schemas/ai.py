from datetime import date
from typing import List, Optional
from pydantic import BaseModel, validator


class AiEntrySuggestion(BaseModel):
    date: date
    project: str
    task: str
    hours: float
    comment: str
    confidence: float
    reason: str

    @validator("hours")
    def hours_range(cls, v):
        if v < 0 or v > 24:
            raise ValueError("Invalid hours value")
        return v


class AiSuggestionResponse(BaseModel):
    week_start: date
    entries: List[AiEntrySuggestion]
    warnings: List[str]
    questions: List[str]


class AiSuggestRequest(BaseModel):
    resource_id: int
    week_start: date
    context: Optional[str] = None


class AiApplyRequest(BaseModel):
    timesheet_id: int
    suggestions: List[AiEntrySuggestion]
    confirmation_token: str
