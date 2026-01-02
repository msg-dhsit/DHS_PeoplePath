from datetime import date
from typing import List
from pydantic import BaseModel


class SummaryStats(BaseModel):
    total_resources: int
    available: int
    partially_allocated: int
    fully_allocated: int
    pending_timesheets: int


class UtilizationPoint(BaseModel):
    week_start: date
    utilization: float


class TimesheetStatusSummary(BaseModel):
    week_start: date
    pending: int
    approved: int
    rejected: int


class DashboardResponse(BaseModel):
    summary: SummaryStats
    utilization: List[UtilizationPoint]
    timesheets: TimesheetStatusSummary
    team_breakdown: dict
    project_breakdown: dict
