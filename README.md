🎓 School Management API
FastAPI • SQLAlchemy • SQLite • MongoDB • JWT Authentication • Analytics

A modern, production-ready backend system for managing students, courses, lecturers, and academic analytics.
This API implements clean architecture, secure authentication, dual-database integration, and Power BI–ready endpoints.

🚀 Features
🔐 Authentication

POST /auth/register — Register new user

POST /auth/login — Login and obtain JWT token

Supports roles:

Admin

Lecturer

Student

👨‍🎓 Students

GET /students/ — Get all students

POST /students/ — Create student

GET /students/{student_id} — Get student

PUT /students/{student_id} — Update student

DELETE /students/{student_id} — Delete student

GET /students/me/gpa — Get current user's GPA

📘 Courses

GET /courses/ — Get all courses

POST /courses/ — Create course

GET /courses/{course_id} — Get a course

PUT /courses/{course_id} — Update course

DELETE /courses/{course_id} — Delete course

👨‍🏫 Lecturers

GET /lecturers/ — Get all lecturers

POST /lecturers/ — Create lecturer

GET /lecturers/{lecturer_id} — Get lecturer

PUT /lecturers/{lecturer_id} — Update lecturer

DELETE /lecturers/{lecturer_id} — Delete lecturer

📊 Analytics (MongoDB)

GET /analytics/gpa — Average GPA per course

GET /analytics/top-students — Top students by GPA

GET /analytics/enrollments — Course enrollment count

These endpoints are optimized for BI tools like Power BI, Tableau, Metabase, and Grafana.

🏥 Health & Root

GET / — API home route

GET /healthz — Health check endpoint

🧱 Tech Stack
Layer	Technology
Framework	FastAPI
ORM	SQLAlchemy
Databases	SQLite (transactions), MongoDB Atlas (analytics)
Auth	JWT (python-jose)
Hashing	passlib[bcrypt]
Config	pydantic-settings
Server	Uvicorn
Optional	Docker, Docker Compose

📁 Project Structure
app/
 ├── api/
 │   └── v1/
 │       ├── students.py
 │       ├── courses.py
 │       ├── lecturers.py
 │       └── analytics.py
 ├── core/
 │   ├── security.py
 │   ├── exceptions.py
 │   └── utils.py
 ├── services/
 ├── repositories/
 ├── models/
 │   ├── pydantic_schemas.py
 │   └── sqlalchemy_models.py
 ├── db/
 │   ├── sql_db.py
 │   └── mongo_db.py
 ├── main.py
 └── config.py
