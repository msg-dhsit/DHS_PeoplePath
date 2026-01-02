import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..schemas import ai as ai_schema
from ..services.ai_provider import get_ai_provider
from ..services import timesheet_service
from ..models import models

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/timesheet/suggest", response_model=ai_schema.AiSuggestionResponse)
def suggest(payload: ai_schema.AiSuggestRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    provider = get_ai_provider()
    resource = db.get(models.Resource, payload.resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    projects = [alloc.project.name for alloc in resource.allocations]
    prompt = {
        "week_start": payload.week_start.isoformat(),
        "resource": resource.user.name,
        "projects": projects,
        "capacity_hours_per_week": resource.capacity_hours_per_week,
    }
    suggestion = provider.suggest({"week_start": payload.week_start.isoformat(), "project_name": projects[0] if projects else "Internal", "prompt": json.dumps(prompt)})
    return suggestion


@router.post("/timesheet/apply", response_model=ai_schema.AiSuggestionResponse)
def apply(payload: ai_schema.AiApplyRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    timesheet = db.get(models.Timesheet, payload.timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    if payload.confirmation_token != "CONFIRM":
        raise HTTPException(status_code=400, detail="User confirmation required")
    project_lookup = {p.name: p.id for p in db.query(models.Project).all()}
    timesheet_service.apply_ai_suggestions(db, timesheet, payload.suggestions, current_user.id, project_lookup)
    return ai_schema.AiSuggestionResponse(
        week_start=timesheet.week_start_date,
        entries=payload.suggestions,
        warnings=[],
        questions=[],
    )
