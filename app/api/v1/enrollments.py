# app/api/v1/enrollments.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.sql_db import get_db
from app.models.pydantic import EnrollmentCreate, EnrollmentOut, EnrollmentUpdate
from app.services.enrollment_service import EnrollmentService
from app.core.security import role_required

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

def get_service(db: Session = Depends(get_db)):
    return EnrollmentService(db)

# Public: list enrollments (or protect as you prefer)
@router.get("/", response_model=list[EnrollmentOut])
def list_enrollments(service: EnrollmentService = Depends(get_service)):
    return service.list_enrollments()

# Create enrollment (admins/lecturers may be required depending on policy)
@router.post("/", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, service: EnrollmentService = Depends(get_service)):
    return service.create_enrollment(payload)

# Get single
@router.get("/{enr_id}", response_model=EnrollmentOut)
def get_enrollment(enr_id: int, service: EnrollmentService = Depends(get_service)):
    return service.get_enrollment(enr_id)

# Update (grade / semester) - default admin/lecturer only; change decorator to allow others
@router.put("/{enr_id}", response_model=EnrollmentOut, dependencies=[Depends(role_required(["admin", "lecturer"]))])
def update_enrollment(enr_id: int, payload: EnrollmentUpdate, service: EnrollmentService = Depends(get_service)):
    return service.update_enrollment(enr_id, payload)

# Delete (admin only)
@router.delete("/{enr_id}", dependencies=[Depends(role_required(["admin"]))])
def delete_enrollment(enr_id: int, service: EnrollmentService = Depends(get_service)):
    return service.delete_enrollment(enr_id)
