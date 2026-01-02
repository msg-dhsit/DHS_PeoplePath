from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..schemas import resource as resource_schema
from ..models import models

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=List[resource_schema.ResourceBase])
def list_resources(
    search: Optional[str] = None,
    team: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(models.Resource).join(models.User)
    if search:
        like = f"%{search.lower()}%"
        query = query.filter(models.User.name.ilike(like))
    if team:
        query = query.filter(models.User.team == team)
    if status:
        query = query.filter(models.Resource.status == status)
    return query.all()


@router.get("/{resource_id}", response_model=resource_schema.ResourceDetail)
def get_resource(resource_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    resource = (
        db.query(models.Resource)
        .join(models.User)
        .filter(models.Resource.id == resource_id)
        .first()
    )
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    allocations = [
        resource_schema.ProjectAllocation(
            project_id=a.project_id,
            project_name=a.project.name,
            start_date=a.start_date,
            end_date=a.end_date,
            allocation_percent=a.allocation_percent,
        )
        for a in resource.allocations
    ]
    return resource_schema.ResourceDetail(
        **resource_schema.ResourceBase.from_orm(resource).dict(),
        name=resource.user.name,
        email=resource.user.email,
        team=resource.user.team,
        allocations=allocations,
    )


@router.post("", response_model=resource_schema.ResourceBase)
def create_resource(payload: resource_schema.ResourceCreate, db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "hr"]))) -> resource_schema.ResourceBase:
    resource = models.Resource(**payload.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.patch("/{resource_id}", response_model=resource_schema.ResourceBase)
def update_resource(resource_id: int, payload: resource_schema.ResourceUpdate, db: Session = Depends(get_db), current_user=Depends(require_role(["admin", "hr"]))) -> resource_schema.ResourceBase:
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(resource, k, v)
    db.commit()
    db.refresh(resource)
    return resource
