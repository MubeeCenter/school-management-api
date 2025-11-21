# app/models/pydantic_models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# NOTE: For Pydantic v2 compatibility we include model_config.
# For v1 compatibility we keep a Config inner class with from_attributes=True.
# Adjust if your project uses strictly v2 or v1.

# ============================
# AUTH / USER SCHEMAS
# ============================
class UserBase(BaseModel):
    username: str
    role: Optional[str] = "student"

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================
# STUDENT SCHEMAS
# ============================
class StudentBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentOut(StudentBase):
    id: int

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


# ============================
# LECTURER SCHEMAS
# ============================
class LecturerBase(BaseModel):
    name: str
    department: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class LecturerCreate(LecturerBase):
    pass


class LecturerUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None


class LecturerOut(LecturerBase):
    id: int

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


# ============================
# COURSE SCHEMAS
# ============================
class CourseBase(BaseModel):
    title: str
    code: str
    semester: str
    lecturer_id: Optional[int] = None

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    semester: Optional[str] = None
    lecturer_id: Optional[int] = None


class CourseOut(CourseBase):
    id: int

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


# ============================
# ENROLLMENT SCHEMAS
# ============================
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[float] = None

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    grade: Optional[float] = None


class EnrollmentOut(EnrollmentBase):
    id: int

    model_config = {"from_attributes": True}

    class Config:
        from_attributes = True


# ============================
# ANALYTICS SCHEMAS (optional)
# ============================
class GPAAnalytics(BaseModel):
    course_name: str
    course_code: Optional[str] = None
    avg_gpa: float
    count: Optional[int] = None


class TopStudentAnalytics(BaseModel):
    name: str
    email: str
    gpa: float


class EnrollmentAnalytics(BaseModel):
    course_name: str
    course_code: Optional[str] = None
    enrollment_count: int
