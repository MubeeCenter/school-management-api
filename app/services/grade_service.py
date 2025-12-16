from app.repositories.grade_repo import GradeRepository

class GradeService:
    def __init__(self, db):
        self.repo = GradeRepository(db)

    def add_grade(self, grade_data):
        return self.repo.create_grade(grade_data)
