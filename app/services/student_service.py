from app.repositories.student_repo import StudentRepository
from fastapi import HTTPException
from app.models.pydantic import StudentCreate, StudentOut

class StudentService:
    def __init__(self, db):
        self.repo = StudentRepository(db)

    def get_all_students(self):
        students = self.repo.get_all()
        return [StudentOut.from_orm(s) for s in students]

    def get_student_by_id(self, student_id: int):
        student = self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentOut.from_orm(student)

    def create_student(self, payload: StudentCreate):
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        student = self.repo.create(payload)
        return StudentOut.from_orm(student)

    def delete_student(self, student_id: int):
        success = self.repo.delete(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
