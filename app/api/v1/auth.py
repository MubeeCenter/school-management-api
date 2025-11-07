from fastapi import APIRouter, HTTPException, Depends
from app.models.pydantic import UserCreate, UserLogin
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.db.sql_db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(user)

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return AuthService(db).login_user(user)
