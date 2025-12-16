from app.models.sqlalchemy_models import Grade


class GradeRepository:
    def __init__(self, db):
        self.db = db

    def create_grade(self, grade_data):
        grade = Grade(**grade_data.dict())
        self.db.add(grade)
        self.db.commit()
        self.db.refresh(grade)
        return grade

    def update_grade(self, grade_id: int, new_score: float):
        grade = self.db.query(Grade).filter(Grade.id == grade_id).first()

        if not grade:
            return None

        grade.score = new_score
        self.db.commit()
        self.db.refresh(grade)
        return grade

    def get_student_grades(self, student_id: int):
        return self.db.query(Grade).filter(Grade.student_id == student_id).all()
