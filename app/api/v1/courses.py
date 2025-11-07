from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import CourseCreate, CourseOut
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return CourseService(db).get_all_courses()

@router.post("/", response_model=CourseOut)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    return CourseService(db).create_course(payload)
