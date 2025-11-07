# app/repositories/student_repo.py
from app.db.sql_db import SessionLocal
from app.db.mongo_db import students_col
from app.models.sqlalchemy_models import Student


class StudentRepository:
    def __init__(self, db=None):
        """
        Optionally accepts an existing SQLAlchemy session (db) from the service.
        Falls back to creating its own SessionLocal() if none provided.
        """
        self.db = db or SessionLocal()

    def get_all(self):
        """
        Fetch all students — prefer SQLAlchemy if available,
        otherwise fall back to MongoDB and normalize field names.
        """
        students = self.db.query(Student).all()
        if students:
            # Convert SQLAlchemy model objects to dictionaries
            return [s.as_dict() for s in students]

        # ✅ Fallback to MongoDB
        docs = list(students_col.find({}, {"_id": 0}))
        normalized = []

        for d in docs:
            normalized.append({
                "id": d.get("StudentID") or 0,
                "name": d.get("Name") or "Unknown",
                "age": d.get("Age") or 0,
                "gender": d.get("Gender") or "Not specified",
                "email": d.get("Email") or "unknown@example.com"
            })
        return normalized

    def get_by_id(self, student_id: int):
        """
        Retrieve a single student by ID from SQL or MongoDB.
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            return student.as_dict()

        # ✅ Fallback to MongoDB
        doc = students_col.find_one({"StudentID": student_id}, {"_id": 0})
        if doc:
            return {
                "id": doc.get("StudentID") or 0,
                "name": doc.get("Name") or "Unknown",
                "age": doc.get("Age") or 0,
                "gender": doc.get("Gender") or "Not specified",
                "email": doc.get("Email") or "unknown@example.com"
            }
        return None

    def get_by_email(self, email: str):
        """
        Retrieve a single student by email.
        """
        student = self.db.query(Student).filter(Student.email == email).first()
        if student:
            return student.as_dict()

        # ✅ Fallback to MongoDB
        doc = students_col.find_one({"Email": email}, {"_id": 0})
        if doc:
            return {
                "id": doc.get("StudentID") or 0,
                "name": doc.get("Name") or "Unknown",
                "age": doc.get("Age") or 0,
                "gender": doc.get("Gender") or "Not specified",
                "email": doc.get("Email") or "unknown@example.com"
            }
        return None

    def create(self, student_data):
        """
        Create a new student — insert into SQL first, then sync to Mongo.
        """
        student = Student(**student_data.dict())
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

        # ✅ Sync to MongoDB (normalized)
        students_col.insert_one({
            "StudentID": student.id,
            "Name": student.name,
            "Age": student.age,
            "Gender": student.gender,
            "Email": student.email
        })

        return student

    def delete(self, student_id: int):
        """
        Delete student by ID from SQL or Mongo.
        """
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            self.db.delete(student)
            self.db.commit()
            return True

        # ✅ Fallback delete from MongoDB
        mongo_result = students_col.delete_one({"StudentID": student_id})
        return mongo_result.deleted_count > 0
