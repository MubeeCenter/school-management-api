# app/repositories/student_repo.py

from sqlalchemy.orm import Session
from app.models.sqlalchemy_models import Student


class StudentRepository:
    """
    SQL-only repository.
    Handles all CREATE/READ/UPDATE/DELETE ops using SQLAlchemy.
    Mongo sync is handled in StudentService, not here.
    """

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------
    # GET ALL
    # ------------------------------
    def get_all(self):
        return self.db.query(Student).all()

    # ------------------------------
    # GET BY ID
    # ------------------------------
    def get_by_id(self, student_id: int):
        return self.db.query(Student).filter(Student.id == student_id).first()

    # ------------------------------
    # GET BY EMAIL
    # ------------------------------
    def get_by_email(self, email: str):
        return self.db.query(Student).filter(Student.email == email).first()

    # ------------------------------
    # GET BY USERNAME
    # ------------------------------
    def get_by_username(self, username: str):
        return self.db.query(Student).filter(Student.username == username).first()

    # ------------------------------
    # CREATE STUDENT
    # ------------------------------
    def create(self, payload):
        student = Student(
            name=payload.name,
            age=payload.age,
            gender=payload.gender,
            email=payload.email,
            username=getattr(payload, "username", None)
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student  # ORM instance

    # ------------------------------
    # UPDATE STUDENT
    # ------------------------------
    def update(self, student_id: int, payload_dict: dict):
        student = self.get_by_id(student_id)
        if not student:
            return None

        for field, value in payload_dict.items():
            if value is not None and hasattr(student, field):
                setattr(student, field, value)

        self.db.commit()
        self.db.refresh(student)
        return student

    # ------------------------------
    # DELETE STUDENT
    # ------------------------------
    def delete(self, student_id: int) -> bool:
        student = self.get_by_id(student_id)
        if not student:
            return False

        self.db.delete(student)
        self.db.commit()
        return True
