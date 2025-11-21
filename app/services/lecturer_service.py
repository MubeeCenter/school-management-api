from fastapi import HTTPException
from app.repositories.lecturer_repo import LecturerRepository
from app.models.pydantic import LecturerCreate, LecturerUpdate, LecturerOut
from app.db.mongo_db import mongo_db


class LecturerService:

    def __init__(self, db):
        self.repo = LecturerRepository(db)

    # ---------------------------------------------
    # Create Lecturer (Admin)
    # ---------------------------------------------
    def create_lecturer(self, payload: LecturerCreate):
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        lecturer = self.repo.create(payload.name, payload.department, payload.email)

        # 🔄 SYNC → MongoDB
        mongo_db.sync_lecturer({
            "id": lecturer.id,
            "name": lecturer.name,
            "department": lecturer.department,
            "email": lecturer.email
        })

        return LecturerOut.from_orm(lecturer)

    # ---------------------------------------------
    # Fetch All Lecturers
    # ---------------------------------------------
    def get_all_lecturers(self):
        lecturers = self.repo.get_all()
        return [LecturerOut.from_orm(l) for l in lecturers]

    # ---------------------------------------------
    # Fetch One Lecturer
    # ---------------------------------------------
    def get_lecturer_by_id(self, lecturer_id: int):
        lecturer = self.repo.get_by_id(lecturer_id)
        if not lecturer:
            raise HTTPException(status_code=404, detail="Lecturer not found")
        return LecturerOut.from_orm(lecturer)

    # ---------------------------------------------
    # Update Lecturer (Admin)
    # ---------------------------------------------
    def update_lecturer(self, lecturer_id: int, payload: LecturerUpdate):
        lecturer = self.repo.get_by_id(lecturer_id)
        if not lecturer:
            raise HTTPException(status_code=404, detail="Lecturer not found")

        updated = self.repo.update(
            lecturer_id,
            payload.name,
            payload.department,
            payload.email,
        )

        # 🔄 SYNC → MongoDB
        mongo_db.sync_lecturer({
            "id": updated.id,
            "name": updated.name,
            "department": updated.department,
            "email": updated.email
        })

        return LecturerOut.from_orm(updated)

    # ---------------------------------------------
    # Delete Lecturer
    # ---------------------------------------------
    def delete_lecturer(self, lecturer_id: int):
        lecturer = self.repo.delete(lecturer_id)
        if not lecturer:
            raise HTTPException(status_code=404, detail="Lecturer not found")

        # 🔄 Soft-remove in MongoDB (set deleted flag)
        mongo_db.sync_lecturer({"id": lecturer_id, "deleted": True})

        return {"message": "Lecturer deleted successfully"}
