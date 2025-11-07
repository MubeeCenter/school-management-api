from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import StudentCreate, StudentOut
from app.models.sqlalchemy_models import Student
from app.services.student_service import StudentService
from app.core.security import get_current_user
from app.repositories.student_repo import StudentRepository
from app.repositories.mongo_repo import MongoRepository

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return StudentService(db).get_all_students()

@router.post("/", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    return StudentService(db).create_student(payload)

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    result = StudentService(db).get_student_by_id(student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    StudentService(db).delete_student(student_id)
    return {"message": "Student deleted successfully"}


@router.get("/me/gpa")
def my_gpa(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    repo = MongoRepository()
    gpa = repo.gpa_for_student(current_user["username"])
    return {"student": current_user["username"], "gpa": gpa}
