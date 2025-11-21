# app/services/enrollment_service.py
from fastapi import HTTPException
from app.repositories.enrollment_repo import EnrollmentRepository
from app.models.pydantic import EnrollmentCreate, EnrollmentOut, EnrollmentUpdate
from app.db.mongo_db import mongo_db

# small helper conversion (safe - doesn't require other modules)
def _enrollment_to_doc(enr):
    return {
        "id": enr.id,
        "student_id": enr.student_id,
        "course_id": enr.course_id,
        "grade": float(enr.grade) if enr.grade is not None else None,
        # include semester if present on SQL model
        **({"semester": enr.semester} if hasattr(enr, "semester") else {})
    }

class EnrollmentService:
    def __init__(self, db):
        self.repo = EnrollmentRepository(db)

    def list_enrollments(self):
        items = self.repo.get_all()
        return [EnrollmentOut.from_orm(e) for e in items]

    def create_enrollment(self, payload: EnrollmentCreate):
        # optional: prevent duplicate (simple check)
        existing = self.repo.get_by_student_course(payload.student_id, payload.course_id)
        if existing:
            raise HTTPException(status_code=400, detail="Student already enrolled in this course")

        enr = self.repo.create(payload)

        # sync to Mongo (wrapped to avoid raising if Mongo not available)
        try:
            if getattr(mongo_db, "enrollments", None):
                mongo_db.sync_enrollment(_enrollment_to_doc(enr))
        except Exception:
            # don't fail the API if Mongo sync has issues
            pass

        return EnrollmentOut.from_orm(enr)

    def get_enrollment(self, enr_id: int):
        enr = self.repo.get_by_id(enr_id)
        if not enr:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        return EnrollmentOut.from_orm(enr)

    def update_enrollment(self, enr_id: int, payload: EnrollmentUpdate):
        enr = self.repo.get_by_id(enr_id)
        if not enr:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        updated = self.repo.update(enr_id, payload)

        try:
            if getattr(mongo_db, "enrollments", None):
                mongo_db.sync_enrollment(_enrollment_to_doc(updated))
        except Exception:
            pass

        return EnrollmentOut.from_orm(updated)

    def delete_enrollment(self, enr_id: int):
        success = self.repo.delete(enr_id)
        if not success:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        try:
            if getattr(mongo_db, "enrollments", None):
                mongo_db.enrollments.delete_one({"id": enr_id})
        except Exception:
            pass
        return {"message": "Enrollment deleted successfully"}
