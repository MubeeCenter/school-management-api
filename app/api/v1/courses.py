from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import CourseCreate, CourseOut, CourseUpdate
from app.services.course_service import CourseService
from app.core.security import role_required

router = APIRouter(prefix="/courses", tags=["Courses"])

# 🔍 Public route
@router.get("/", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return CourseService(db).get_all_courses()

# ➕ Admin-only: Create
@router.post(
    "/",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(role_required(["admin"]))],
)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    return CourseService(db).create_course(payload)

# ✏️ Admin-only: Update
@router.put(
    "/{course_id}",
    response_model=CourseOut,
    dependencies=[Depends(role_required(["admin"]))],
)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    return CourseService(db).update_course(course_id, payload)

# ❌ Admin-only: Delete
@router.delete(
    "/{course_id}",
    dependencies=[Depends(role_required(["admin"]))],
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return CourseService(db).delete_course(course_id)
