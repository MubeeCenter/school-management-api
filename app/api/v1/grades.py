from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.sql_db import get_db
from app.models.pydantic import GradeCreate
from app.services.grade_service import GradeService

router = APIRouter(prefix="/grades", tags=["Grades"])


@router.post("/")
def add_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db)
):
    service = GradeService(db)
    return service.add_grade(grade)
