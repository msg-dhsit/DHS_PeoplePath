from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas.auth import LoginResponse, UserBase
from ..services import auth as auth_service
from ..core.database import get_db
from ..core.security import get_current_user
from ..models import models

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = auth_service.create_access_token({"sub": user.email})
    return {"token": token, "user": user}


@router.get("/me", response_model=UserBase)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
