from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..models import models

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/bot/messages")
def bot_messages(message: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    text = message.get("text", "")
    response = "Unknown command"
    if text.startswith("/timesheet suggest"):
        response = "AI suggestions ready: open portal to review."
    if text.startswith("/timesheet status"):
        resource = db.query(models.Resource).filter(models.Resource.user_id == current_user.id).first()
        timesheet = (
            db.query(models.Timesheet)
            .filter(models.Timesheet.resource_id == resource.id)
            .order_by(models.Timesheet.week_start_date.desc())
            .first()
        )
        response = f"Current week status: {timesheet.status if timesheet else 'N/A'}"
    return {"reply": response}


@router.get("/tab/config")
def tab_config():
    return {"validDomains": ["localhost"], "name": "Resource Portal"}
