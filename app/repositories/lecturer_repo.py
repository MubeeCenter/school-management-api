from sqlalchemy.orm import Session
from app.models.sqlalchemy_models import Lecturer


class LecturerRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------
    # Create Lecturer
    # ---------------------------------------------
    def create(self, name: str, department: str, email: str):
        lecturer = Lecturer(name=name, department=department, email=email)
        self.db.add(lecturer)
        self.db.commit()
        self.db.refresh(lecturer)
        return lecturer

    # ---------------------------------------------
    # Fetch All
    # ---------------------------------------------
    def get_all(self):
        return self.db.query(Lecturer).all()

    # ---------------------------------------------
    # Fetch one
    # ---------------------------------------------
    def get_by_id(self, lecturer_id: int):
        return self.db.query(Lecturer).filter(Lecturer.id == lecturer_id).first()

    def get_by_email(self, email: str):
        return self.db.query(Lecturer).filter(Lecturer.email == email).first()

    # ---------------------------------------------
    # Update Lecturer
    # ---------------------------------------------
    def update(self, lecturer_id: int, name: str, department: str, email: str):
        lecturer = self.get_by_id(lecturer_id)
        if not lecturer:
            return None

        if name:
            lecturer.name = name
        if department:
            lecturer.department = department
        if email:
            lecturer.email = email

        self.db.commit()
        self.db.refresh(lecturer)
        return lecturer

    # ---------------------------------------------
    # Delete Lecturer
    # ---------------------------------------------
    def delete(self, lecturer_id: int):
        lecturer = self.get_by_id(lecturer_id)
        if not lecturer:
            return None

        self.db.delete(lecturer)
        self.db.commit()
        return True
