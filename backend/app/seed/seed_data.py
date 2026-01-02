from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models import models
from ..services import auth

def seed():
    db: Session = SessionLocal()
    if db.query(models.User).count() > 0:
        print("Seed already applied")
        db.close()
        return
    # Users
    admin = models.User(email="admin@example.com", name="Admin User", role=models.RoleEnum.ADMIN, team="Ops", hashed_password=auth.get_password_hash("admin123"))
    manager = models.User(email="manager@example.com", name="Manager One", role=models.RoleEnum.MANAGER, team="Delivery", hashed_password=auth.get_password_hash("manager123"))
    hr = models.User(email="hr@example.com", name="HR Lead", role=models.RoleEnum.HR, team="People", hashed_password=auth.get_password_hash("hr123"))
    resource_user = models.User(email="resource@example.com", name="Resource User", role=models.RoleEnum.RESOURCE, team="Delivery", manager_id=2, hashed_password=auth.get_password_hash("resource123"))
    db.add_all([admin, manager, hr, resource_user])
    db.commit()

    resource = models.Resource(user_id=resource_user.id, title="Senior Engineer", skills=["Python", "FastAPI", "React"], location="Remote", status="available", capacity_hours_per_week=40)
    db.add(resource)
    db.commit()

    project = models.Project(name="Contoso Revamp", client="Contoso", start_date=date.today(), end_date=date.today() + timedelta(days=60))
    db.add(project)
    db.commit()

    allocation = models.Allocation(resource_id=resource.id, project_id=project.id, start_date=date.today(), end_date=date.today() + timedelta(days=30), allocation_percent=80)
    db.add(allocation)
    db.commit()

    week_start = date.today() - timedelta(days=date.today().weekday())
    timesheet = models.Timesheet(resource_id=resource.id, week_start_date=week_start)
    db.add(timesheet)
    db.commit()

    entry = models.TimesheetEntry(timesheet_id=timesheet.id, date=week_start, project_id=project.id, task="Design architecture", hours=8, comment="Initial design", source="manual", confidence=1.0)
    db.add(entry)

    template = models.AiPromptTemplate(name="Default", template_text="You are a timesheet assistant...", enabled=True)
    db.add(template)

    db.commit()
    db.close()
    print("Seed completed")


if __name__ == "__main__":
    seed()
