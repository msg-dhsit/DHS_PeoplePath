from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, validator


class TimesheetEntryBase(BaseModel):
    id: Optional[int]
    date: date
    project_id: int
    task: str
    hours: float
    comment: Optional[str]
    source: str = "manual"
    confidence: float = 1.0

    @validator("hours")
    def hours_limit(cls, v):
        if v < 0 or v > 24:
            raise ValueError("Hours must be between 0 and 24")
        return v


class TimesheetBase(BaseModel):
    id: int
    resource_id: int
    week_start_date: date
    status: str
    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    approved_by: Optional[int]

    class Config:
        orm_mode = True


class TimesheetCreate(BaseModel):
    resource_id: int
    week_start_date: date


class TimesheetEntriesUpdate(BaseModel):
    entries: List[TimesheetEntryBase]


class TimesheetResponse(TimesheetBase):
    entries: List[TimesheetEntryBase]


class TimesheetApprovalRequest(BaseModel):
    approver_id: int
    comments: Optional[str]
