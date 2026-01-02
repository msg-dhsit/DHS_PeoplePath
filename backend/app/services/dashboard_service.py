from datetime import date, timedelta
from collections import Counter
from sqlalchemy.orm import Session

from ..models import models


def summarize(db: Session):
    resources = db.query(models.Resource).all()
    total = len(resources)
    available = len([r for r in resources if r.status == "available"])
    partial = len([r for r in resources if r.status == "partial"])
    full = total - available - partial
    pending_timesheets = db.query(models.Timesheet).filter(models.Timesheet.status == models.TimesheetStatus.SUBMITTED).count()

    start = date.today() - timedelta(weeks=5)
    utilization = []
    for wk in range(5):
        week_start = start + timedelta(weeks=wk)
        entries = db.query(models.TimesheetEntry).join(models.Timesheet).filter(models.Timesheet.week_start_date == week_start).all()
        total_hours = sum([e.hours for e in entries])
        capacity = sum([r.capacity_hours_per_week for r in resources]) or 1
        utilization.append({"week_start": week_start, "utilization": round((total_hours / capacity) * 100, 2)})

    timesheets = db.query(models.Timesheet).filter(models.Timesheet.week_start_date == start + timedelta(weeks=4)).all()
    status_counts = Counter([t.status for t in timesheets])

    team_breakdown = Counter([r.user.team for r in resources if r.user and r.user.team])
    project_breakdown = Counter()
    for alloc in db.query(models.Allocation).all():
        project_breakdown[alloc.project.name] += alloc.allocation_percent

    return {
        "summary": {
            "total_resources": total,
            "available": available,
            "partially_allocated": partial,
            "fully_allocated": full,
            "pending_timesheets": pending_timesheets,
        },
        "utilization": utilization,
        "timesheets": {
            "week_start": start + timedelta(weeks=4),
            "pending": status_counts.get(models.TimesheetStatus.SUBMITTED, 0),
            "approved": status_counts.get(models.TimesheetStatus.APPROVED, 0),
            "rejected": status_counts.get(models.TimesheetStatus.REJECTED, 0),
        },
        "team_breakdown": dict(team_breakdown),
        "project_breakdown": dict(project_breakdown),
    }
