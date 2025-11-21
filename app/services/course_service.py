from fastapi import HTTPException
from app.repositories.course_repo import CourseRepository
from app.models.pydantic import CourseCreate, CourseOut, CourseUpdate
from app.db.mongo_db import mongo_db

class CourseService:
    def __init__(self, db):
        self.repo = CourseRepository(db)

    # Read all
    def get_all_courses(self):
        courses = self.repo.get_all()
        return [CourseOut.from_orm(c) for c in courses]

    # Create
    def create_course(self, payload: CourseCreate):
        existing = self.repo.get_by_code(payload.code)
        if existing:
            raise HTTPException(status_code=400, detail="Course code already exists")

        course = self.repo.create(payload)

        # MongoDB sync
        mongo_db.sync_course(course.__dict__)

        return CourseOut.from_orm(course)

    # Update
    def update_course(self, course_id: int, payload: CourseUpdate):
        course = self.repo.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        updated_course = self.repo.update(course_id, payload)

        # MongoDB sync
        mongo_db.sync_course(updated_course.__dict__)

        return CourseOut.from_orm(updated_course)

    # Delete
    def delete_course(self, course_id: int):
        found = self.repo.get_by_id(course_id)
        if not found:
            raise HTTPException(status_code=404, detail="Course not found")

        self.repo.delete(course_id)

        # Remove from Mongo by marking it deleted
        mongo_db.courses.update_one(
            {"id": course_id},
            {"$set": {"deleted": True}},
            upsert=True
        )

        return {"message": "Course deleted successfully"}
