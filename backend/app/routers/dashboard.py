from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return dashboard_service.summarize(db)


@router.get("/utilization")
def utilization(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = dashboard_service.summarize(db)
    return data.get("utilization", [])


@router.get("/timesheets")
def timesheets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = dashboard_service.summarize(db)
    return data.get("timesheets")
