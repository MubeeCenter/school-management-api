# app/services/student_service.py

from fastapi import HTTPException
from app.repositories.student_repo import StudentRepository
from app.repositories.mongo_repo import MongoRepository
from app.models.pydantic import StudentCreate, StudentOut, StudentUpdate


class StudentService:
    def __init__(self, db):
        self.repo = StudentRepository(db)
        self.mongo = MongoRepository()  # full-sync repo

    # ---------------------------------------------------------
    # GET ALL
    # ---------------------------------------------------------
    def get_all_students(self):
        students = self.repo.get_all()
        return [StudentOut.from_orm(s) for s in students]

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------
    def get_student_by_id(self, student_id: int):
        student = self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentOut.from_orm(student)

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create_student(self, payload: StudentCreate):
        # avoid duplicate email
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        # avoid duplicate username
        if hasattr(payload, "username") and self.repo.get_by_username(payload.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        # create in SQL
        student = self.repo.create(payload)

        # MIRROR TO MONGODB
        self.mongo.upsert_student(student.as_dict())

        return StudentOut.from_orm(student)

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def update_student(self, student_id: int, payload: StudentUpdate):
        student = self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        updated = self.repo.update(student_id, payload.dict(exclude_unset=True))

        # SYNC TO MONGO
        self.mongo.upsert_student(updated.as_dict())

        return StudentOut.from_orm(updated)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete_student(self, student_id: int):
        student = self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # delete from SQL
        self.repo.delete(student_id)

        # delete from Mongo
        self.mongo.delete_student(student_id)

        return {"message": "Student deleted successfully"}

    # ---------------------------------------------------------
    # GPA (Mongo analytics only)
    # ---------------------------------------------------------
    def get_student_gpa(self, username: str):
        gpa = self.mongo.gpa_for_student(username)
        if gpa is None:
            raise HTTPException(status_code=404, detail="GPA not found")
        return gpa
