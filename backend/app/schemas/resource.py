from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    id: int
    user_id: int
    title: str
    skills: Optional[List[str]]
    location: Optional[str]
    status: str
    capacity_hours_per_week: int
    created_at: datetime

    class Config:
        orm_mode = True


class ResourceCreate(BaseModel):
    user_id: int
    title: str
    skills: Optional[List[str]] = []
    location: Optional[str]
    status: str = "available"
    capacity_hours_per_week: int = 40


class ResourceUpdate(BaseModel):
    title: Optional[str]
    skills: Optional[List[str]]
    location: Optional[str]
    status: Optional[str]
    capacity_hours_per_week: Optional[int]


class ProjectAllocation(BaseModel):
    project_id: int
    project_name: str
    start_date: date
    end_date: date
    allocation_percent: int


class ResourceDetail(ResourceBase):
    name: str
    email: str
    team: Optional[str]
    allocations: List[ProjectAllocation] = []
