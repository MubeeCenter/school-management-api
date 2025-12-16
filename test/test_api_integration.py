# test/test_api_integration.py

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_get_students():
    username = f"tester_{uuid.uuid4().hex[:6]}"
    password = "1234"

    # ✅ 1. REGISTER ADMIN
    reg_res = client.post("/auth/register", json={
        "username": username,
        "password": password,
        "role": "admin"
    })
    assert reg_res.status_code == 201, reg_res.text
    user_id = reg_res.json()["id"]

    # ✅ 2. LOGIN USING FORM DATA (NOT JSON)
    login_res = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_res.status_code == 200, login_res.text
    token = login_res.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ✅ 3. CREATE STUDENT WITH AUTH TOKEN
    student_res = client.post(
        "/students",
        json={
            "name": "Tester Student",
            "email": f"{username}@example.com",
            "age": 20,
            "gender": "M",
            "user_id": user_id
        },
        headers=headers
    )
    assert student_res.status_code == 200, student_res.text

    # ✅ 4. FETCH STUDENTS WITH AUTH
    res = client.get("/students", headers=headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
