from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.core.security import role_required
from app.services.lecturer_service import LecturerService
from app.models.pydantic import LecturerCreate, LecturerUpdate, LecturerOut

router = APIRouter(prefix="/lecturers", tags=["Lecturers"])


# --------------------------------------------------------
# ➕ Create Lecturer (Admin only)
# --------------------------------------------------------
@router.post(
    "/",
    dependencies=[Depends(role_required(["admin"]))],
    status_code=status.HTTP_201_CREATED,
    response_model=LecturerOut
)
def create_lecturer(payload: LecturerCreate, db: Session = Depends(get_db)):
    return LecturerService(db).create_lecturer(payload)


# --------------------------------------------------------
# ✏ Update Lecturer (Admin only)
# --------------------------------------------------------
@router.put(
    "/{lecturer_id}",
    dependencies=[Depends(role_required(["admin"]))],
    response_model=LecturerOut
)
def update_lecturer(lecturer_id: int, payload: LecturerUpdate, db: Session = Depends(get_db)):
    return LecturerService(db).update_lecturer(lecturer_id, payload)


# --------------------------------------------------------
# 📖 Get all lecturers (Public)
# --------------------------------------------------------
@router.get("/", response_model=list[LecturerOut])
def get_all_lecturers(db: Session = Depends(get_db)):
    return LecturerService(db).get_all_lecturers()


# --------------------------------------------------------
# 🔍 Get Lecturer by ID (Public)
# --------------------------------------------------------
@router.get("/{lecturer_id}", response_model=LecturerOut)
def get_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    return LecturerService(db).get_lecturer_by_id(lecturer_id)


# --------------------------------------------------------
# ❌ Delete lecturer (Admin only)
# --------------------------------------------------------
@router.delete(
    "/{lecturer_id}",
    dependencies=[Depends(role_required(["admin"]))],
)
def delete_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    return LecturerService(db).delete_lecturer(lecturer_id)
