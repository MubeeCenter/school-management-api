from pydantic import BaseModel, EmailStr
from typing import Optional


# ---------- STUDENT MODELS ----------
class StudentCreate(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr

class StudentOut(StudentCreate):
    id: int

    class Config:
        from_attributes = True  # replaces orm_mode = True


# ---------- COURSE MODELS ----------
class CourseCreate(BaseModel):
    title: str
    code: str
    semester: str

class CourseOut(CourseCreate):
    id: int

    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "student"

class UserLogin(BaseModel):
    username: str
    password: str
