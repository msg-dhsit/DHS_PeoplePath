from datetime import datetime, date
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Enum, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from ..core.database import Base


class RoleEnum(str):
    ADMIN = "admin"
    MANAGER = "manager"
    HR = "hr"
    RESOURCE = "resource"


class TimesheetStatus(str):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default=RoleEnum.RESOURCE, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    team = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    manager = relationship("User", remote_side=[id])
    resource = relationship("Resource", uselist=False, back_populates="user")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    skills = Column(ARRAY(String))
    location = Column(String, nullable=True)
    status = Column(String, default="available")
    capacity_hours_per_week = Column(Integer, default=40)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resource")
    allocations = relationship("Allocation", back_populates="resource")
    timesheets = relationship("Timesheet", back_populates="resource")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    allocations = relationship("Allocation", back_populates="project")


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    allocation_percent = Column(Integer, default=100)

    resource = relationship("Resource", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")


class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    week_start_date = Column(Date, nullable=False)
    status = Column(String, default=TimesheetStatus.DRAFT)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    resource = relationship("Resource", back_populates="timesheets")
    entries = relationship("TimesheetEntry", back_populates="timesheet", cascade="all, delete-orphan")


class TimesheetEntry(Base):
    __tablename__ = "timesheet_entries"

    id = Column(Integer, primary_key=True, index=True)
    timesheet_id = Column(Integer, ForeignKey("timesheets.id"), nullable=False)
    date = Column(Date, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task = Column(String, nullable=False)
    hours = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    source = Column(String, default="manual")
    confidence = Column(Float, default=1.0)

    timesheet = relationship("Timesheet", back_populates="entries")
    project = relationship("Project")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    diff_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AiPromptTemplate(Base):
    __tablename__ = "ai_prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    template_text = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
