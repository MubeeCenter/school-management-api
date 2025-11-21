from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import StudentCreate, StudentOut, StudentUpdate
from app.models.sqlalchemy_models import Student
from app.services.student_service import StudentService
from app.core.security import get_current_user, role_required
from app.repositories.student_repo import StudentRepository
from app.repositories.mongo_repo import MongoRepository

router = APIRouter(prefix="/students", tags=["Students"])


# -----------------------------
# 🧾  Get all students  (Admin/Lecturer)
# -----------------------------
@router.get("/", response_model=list[StudentOut],
            dependencies=[Depends(role_required(["admin", "lecturer"]))])
def get_students(db: Session = Depends(get_db)):
    """
    Return all registered students (Admin or Lecturer only)
    """
    return StudentService(db).get_all_students()


# -----------------------------
# ➕  Create new student  (Admin only)
# -----------------------------
@router.post("/", response_model=StudentOut,
             dependencies=[Depends(role_required(["admin"]))])
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """
    Admin can create new student records.
    """
    return StudentService(db).create_student(payload)


# -----------------------------
# 🔍  Get a single student  (Admin/Lecturer)
# -----------------------------
@router.get("/{student_id}", response_model=StudentOut,
            dependencies=[Depends(role_required(["admin", "lecturer"]))])
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Fetch one student record by ID (Admin or Lecturer only)
    """
    result = StudentService(db).get_student_by_id(student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result


# -----------------------------
# ✏️  Update a student record  (Admin only)
# -----------------------------
@router.put("/{student_id}",
            dependencies=[Depends(role_required(["admin"]))])
def update_student(student_id: int, payload: StudentUpdate,
                   db: Session = Depends(get_db)):
    """
    Admin can edit student details by ID.
    """
    updated = StudentService(db).update_student(student_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


# -----------------------------
# ❌  Delete a student  (Admin only)
# -----------------------------
@router.delete("/{student_id}",
               dependencies=[Depends(role_required(["admin"]))])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Admin can delete a student record by ID.
    """
    StudentService(db).delete_student(student_id)
    return {"message": "Student deleted successfully"}


# -----------------------------
# 🎓  Student self GPA view  (Student/Admin)
# -----------------------------
@router.get("/me/gpa")
def my_gpa(current_user: dict = Depends(get_current_user)):
    """
    Student or Admin can view GPA.
    - Student: sees own GPA only.
    - Admin: can use username query to view any student's GPA.
    """
    if current_user["role"] not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    repo = MongoRepository()
    username = current_user["username"]

    gpa = repo.gpa_for_student(username)
    if gpa is None:
        raise HTTPException(status_code=404, detail="GPA record not found")

    return {"student": username, "gpa": gpa}
