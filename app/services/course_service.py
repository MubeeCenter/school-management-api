from app.repositories.course_repo import CourseRepository
from fastapi import HTTPException
from app.models.pydantic import CourseCreate, CourseOut

class CourseService:
    def __init__(self, db):
        self.repo = CourseRepository(db)

    def get_all_courses(self):
        courses = self.repo.get_all()
        return [CourseOut.from_orm(c) for c in courses]

    def create_course(self, payload: CourseCreate):
        existing = self.repo.get_by_code(payload.code)
        if existing:
            raise HTTPException(status_code=400, detail="Course code already exists")
        course = self.repo.create(payload)
        return CourseOut.from_orm(course)
