from app.models.sqlalchemy_models import Course

class CourseRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_all(self):
        return self.db.query(Course).all()

    def get_by_code(self, code: str):
        return self.db.query(Course).filter(Course.code == code).first()

    def create(self, course_data):
        course = Course(**course_data.dict())
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
