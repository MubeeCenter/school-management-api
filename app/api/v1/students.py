from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import StudentCreate, StudentOut, StudentUpdate
from app.services.student_service import StudentService
from app.core.security import get_current_user, role_required
from app.repositories.mongo_repo import MongoRepository

router = APIRouter(prefix="/students", tags=["Students"])


# -----------------------------
# 🧾  Get all students  (Admin/Lecturer)
# -----------------------------
@router.get("/", response_model=list[StudentOut],
            dependencies=[Depends(role_required(["admin", "lecturer"]))])
def get_students(db: Session = Depends(get_db)):
    return StudentService(db).get_all_students()


# -----------------------------
# ➕  Create new student  (Admin only)
# -----------------------------
@router.post("/", response_model=StudentOut,
             dependencies=[Depends(role_required(["admin"]))])
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    return StudentService(db).create_student(payload)


# -----------------------------
# 🎓  Student self GPA view  (Student ONLY)
# -----------------------------
@router.get("/me/gpa")
def my_gpa(
    current_user: dict = Depends(get_current_user),
    repo: MongoRepository = Depends()
):
    # ✅ FIXED: use dict access instead of .role
    if current_user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Students only")

    gpa = repo.gpa_for_student(current_user["username"])

    return {
        "username": current_user["username"],
        "gpa": gpa
    }


# -----------------------------
# 🎓  Admin general students GPA view  (Admin ONLY)
# -----------------------------
@router.get("/gpa")
def all_students_gpa(
    current_user: dict = Depends(get_current_user),
    repo: MongoRepository = Depends()
):
    # ✅ Already correct, left intact
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return repo.gpa_for_all_students()


# -----------------------------
# 🔍  Get a single student  (Admin/Lecturer)
# -----------------------------
@router.get("/{student_id}", response_model=StudentOut,
            dependencies=[Depends(role_required(["admin", "lecturer"]))])
def get_student(student_id: int, db: Session = Depends(get_db)):
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
    StudentService(db).delete_student(student_id)
    return {"message": "Student deleted successfully"}
