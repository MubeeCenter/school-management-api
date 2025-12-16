# tests/test_students_unit.py

from app.services.student_service import StudentService
from unittest.mock import MagicMock
from types import SimpleNamespace

def test_create_student_valid():
    mock_repo = MagicMock()

    # ✅ Prevent duplicate checks
    mock_repo.get_by_email.return_value = None
    mock_repo.get_by_username.return_value = None

    # ✅ FAKE returned student object
    fake_student = SimpleNamespace(
        id=1,
        name="Ali",
        email="ali@test.com",
        age=20,
        gender="M",
        user_id=1,
        as_dict=lambda: {
            "id": 1,
            "name": "Ali",
            "email": "ali@test.com",
            "age": 20,
            "gender": "M",
            "user_id": 1
        }
    )

    mock_repo.create.return_value = fake_student

    # ✅ Create service
    svc = StudentService(db=None)
    svc.repo = mock_repo
    svc.mongo = MagicMock()    # ✅ Prevent real MongoDB calls

    payload = SimpleNamespace(
        name="Ali",
        email="ali@test.com",
        age=20,
        gender="M",
        user_id=1
    )

    # ✅ Execute
    svc.create_student(payload)

    # ✅ Assertions
    mock_repo.create.assert_called_once()
    svc.mongo.upsert_student.assert_called_once()
