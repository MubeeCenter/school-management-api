# 🎓 School Management API (FastAPI + SQLite + MongoDB)

This is a backend API for managing students, lecturers, and course analytics.  
It is built with **FastAPI**, **SQLAlchemy**, and **MongoDB (Atlas)**.

---

## 🚀 Features
- Student, Course, and Lecturer CRUD
- Secure JWT authentication
- Role-based access (admin, lecturer, student)
- Dual Database Integration:
  - SQLite (transactional)
  - MongoDB (analytics)
- Power BI / Dash-ready analytics endpoints

---

## 🧱 Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** SQLite + MongoDB Atlas
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose)
- **Containerization:** Docker (optional)

---

## 🧰 Setup
```bash
git clone https://github.com/<yourusername>/school-management-api.git
cd school-management-api
pip install -r requirements.txt
uvicorn app.main:app --reload
