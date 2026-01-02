from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from ..models import models
from ..schemas.ai import AiEntrySuggestion


def get_or_create_timesheet(db: Session, resource_id: int, week_start):
    timesheet = (
        db.query(models.Timesheet)
        .filter(models.Timesheet.resource_id == resource_id, models.Timesheet.week_start_date == week_start)
        .first()
    )
    if not timesheet:
        timesheet = models.Timesheet(resource_id=resource_id, week_start_date=week_start)
        db.add(timesheet)
        db.commit()
        db.refresh(timesheet)
    return timesheet


def upsert_entries(db: Session, timesheet: models.Timesheet, entries: List[dict]):
    existing = {entry.date: entry for entry in timesheet.entries}
    for payload in entries:
        if payload.get("date") in existing:
            entry = existing[payload["date"]]
            entry.project_id = payload["project_id"]
            entry.task = payload["task"]
            entry.hours = payload["hours"]
            entry.comment = payload.get("comment")
            entry.source = payload.get("source", "manual")
            entry.confidence = payload.get("confidence", 1.0)
        else:
            db.add(models.TimesheetEntry(timesheet_id=timesheet.id, **payload))
    db.commit()
    db.refresh(timesheet)
    return timesheet


def submit_timesheet(db: Session, timesheet: models.Timesheet, actor_id: int):
    timesheet.status = models.TimesheetStatus.SUBMITTED
    timesheet.submitted_at = datetime.utcnow()
    _log(db, actor_id, "timesheet", timesheet.id, "submit", {})
    db.commit()
    db.refresh(timesheet)
    return timesheet


def approve_timesheet(db: Session, timesheet: models.Timesheet, approver_id: int):
    timesheet.status = models.TimesheetStatus.APPROVED
    timesheet.approved_by = approver_id
    timesheet.approved_at = datetime.utcnow()
    _log(db, approver_id, "timesheet", timesheet.id, "approve", {})
    db.commit()
    db.refresh(timesheet)
    return timesheet


def reject_timesheet(db: Session, timesheet: models.Timesheet, actor_id: int, reason: str = ""):
    timesheet.status = models.TimesheetStatus.REJECTED
    _log(db, actor_id, "timesheet", timesheet.id, "reject", {"reason": reason})
    db.commit()
    db.refresh(timesheet)
    return timesheet


def apply_ai_suggestions(db: Session, timesheet: models.Timesheet, suggestions: List[AiEntrySuggestion], actor_id: int, project_lookup: dict):
    payloads = []
    for item in suggestions:
        project_id = project_lookup.get(item.project)
        if not project_id:
            continue
        payloads.append(
            {
                "date": item.date,
                "project_id": project_id,
                "task": item.task,
                "hours": item.hours,
                "comment": item.comment,
                "source": "ai",
                "confidence": item.confidence,
            }
        )
    upsert_entries(db, timesheet, payloads)
    _log(db, actor_id, "timesheet", timesheet.id, "apply_ai", {"count": len(payloads)})
    return timesheet


def _log(db: Session, actor_id: int, entity_type: str, entity_id: int, action: str, diff_json: dict):
    db.add(
        models.AuditLog(
            actor_user_id=actor_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            diff_json=diff_json,
        )
    )
    db.commit()
