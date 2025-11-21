from sqlalchemy.orm import Session
from app.models.sqlalchemy_models import Course

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create
    def create(self, payload):
        course = Course(
            title=payload.title,
            code=payload.code,
            unit=payload.unit,
            semester=payload.semester,
            lecturer_id=payload.lecturer_id,
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    # Get all
    def get_all(self):
        return self.db.query(Course).all()

    # Get one
    def get_by_id(self, course_id: int):
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_by_code(self, code: str):
        return self.db.query(Course).filter(Course.code == code).first()

    # Update
    def update(self, course_id: int, payload):
        course = self.get_by_id(course_id)
        if not course:
            return None

        if payload.title is not None:
            course.title = payload.title
        if payload.code is not None:
            course.code = payload.code
        if payload.unit is not None:
            course.unit = payload.unit
        if payload.semester is not None:
            course.semester = payload.semester
        if payload.lecturer_id is not None:
            course.lecturer_id = payload.lecturer_id

        self.db.commit()
        self.db.refresh(course)
        return course

    # Delete
    def delete(self, course_id: int):
        course = self.get_by_id(course_id)
        if not course:
            return False

        self.db.delete(course)
        self.db.commit()
        return True
