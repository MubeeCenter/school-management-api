# app/repositories/enrollment_repo.py
from sqlalchemy.orm import Session
from app.models.sqlalchemy_models import Enrollment

class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload):
        enr = Enrollment(
            student_id=payload.student_id,
            course_id=payload.course_id,
            grade=payload.grade,
        )
        # optional semester in payload; if your model has it, include it
        if hasattr(Enrollment, "semester") and getattr(payload, "semester", None):
            enr.semester = payload.semester

        self.db.add(enr)
        self.db.commit()
        self.db.refresh(enr)
        return enr

    def get_all(self):
        return self.db.query(Enrollment).all()

    def get_by_id(self, enr_id: int):
        return self.db.query(Enrollment).filter(Enrollment.id == enr_id).first()

    def get_by_student_course(self, student_id: int, course_id: int):
        return self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()

    def update(self, enr_id: int, payload):
        enr = self.get_by_id(enr_id)
        if not enr:
            return None
        if getattr(payload, "grade", None) is not None:
            enr.grade = payload.grade
        if getattr(payload, "semester", None) is not None and hasattr(Enrollment, "semester"):
            enr.semester = payload.semester
        self.db.commit()
        self.db.refresh(enr)
        return enr

    def delete(self, enr_id: int):
        enr = self.get_by_id(enr_id)
        if not enr:
            return False
        self.db.delete(enr)
        self.db.commit()
        return True
