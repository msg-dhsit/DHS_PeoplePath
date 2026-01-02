from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models import models
from ..schemas import timesheet as ts_schema
from ..services import timesheet_service

router = APIRouter(prefix="/timesheets", tags=["timesheets"])


@router.get("", response_model=List[ts_schema.TimesheetResponse])
def list_timesheets(
    resource_id: Optional[int] = None,
    week_start: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(models.Timesheet)
    if resource_id:
        query = query.filter(models.Timesheet.resource_id == resource_id)
    if week_start:
        query = query.filter(models.Timesheet.week_start_date == week_start)
    items = query.all()
    return [
        ts_schema.TimesheetResponse(
            **ts_schema.TimesheetBase.from_orm(t).dict(),
            entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in t.entries],
        )
        for t in items
    ]


@router.post("", response_model=ts_schema.TimesheetResponse)
def create_timesheet(payload: ts_schema.TimesheetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    timesheet = timesheet_service.get_or_create_timesheet(db, payload.resource_id, payload.week_start_date)
    return ts_schema.TimesheetResponse(
        **ts_schema.TimesheetBase.from_orm(timesheet).dict(),
        entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in timesheet.entries],
    )


@router.put("/{timesheet_id}/entries", response_model=ts_schema.TimesheetResponse)
def upsert_timesheet_entries(timesheet_id: int, payload: ts_schema.TimesheetEntriesUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    entries = [entry.dict(exclude={"id"}) for entry in payload.entries]
    timesheet = timesheet_service.upsert_entries(db, timesheet, entries)
    return ts_schema.TimesheetResponse(
        **ts_schema.TimesheetBase.from_orm(timesheet).dict(),
        entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in timesheet.entries],
    )


@router.post("/{timesheet_id}/submit", response_model=ts_schema.TimesheetResponse)
def submit(timesheet_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    timesheet = timesheet_service.submit_timesheet(db, timesheet, current_user.id)
    return ts_schema.TimesheetResponse(
        **ts_schema.TimesheetBase.from_orm(timesheet).dict(),
        entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in timesheet.entries],
    )


@router.post("/{timesheet_id}/approve", response_model=ts_schema.TimesheetResponse)
def approve(timesheet_id: int, payload: ts_schema.TimesheetApprovalRequest, db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "manager"])),):
    timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    timesheet = timesheet_service.approve_timesheet(db, timesheet, payload.approver_id)
    return ts_schema.TimesheetResponse(
        **ts_schema.TimesheetBase.from_orm(timesheet).dict(),
        entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in timesheet.entries],
    )


@router.post("/{timesheet_id}/reject", response_model=ts_schema.TimesheetResponse)
def reject(timesheet_id: int, payload: ts_schema.TimesheetApprovalRequest, db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "manager"])),):
    timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    timesheet = timesheet_service.reject_timesheet(db, timesheet, payload.approver_id, payload.comments or "")
    return ts_schema.TimesheetResponse(
        **ts_schema.TimesheetBase.from_orm(timesheet).dict(),
        entries=[ts_schema.TimesheetEntryBase.from_orm(e) for e in timesheet.entries],
    )
