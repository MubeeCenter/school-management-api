from pydantic import BaseModel, EmailStr
from typing import Optional


# ============================
# AUTH / USER SCHEMAS
# ============================

class UserBase(BaseModel):
    username: str
    role: Optional[str] = "student"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2 compatible


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================
# STUDENT SCHEMAS
# ============================

class StudentBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ============================
# LECTURER SCHEMAS
# ============================

class LecturerBase(BaseModel):
    name: str
    department: Optional[str] = None


class LecturerCreate(LecturerBase):
    pass


class LecturerUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None


class LecturerOut(LecturerBase):
    id: int

    class Config:
        from_attributes = True


# ============================
# COURSE SCHEMAS
# ============================

class CourseBase(BaseModel):
    title: str
    code: str
    unit: int
    semester: str
    lecturer_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    unit: Optional[int] = None
    semester: Optional[str] = None
    lecturer_id: Optional[int] = None


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True


# ============================
# ENROLLMENT SCHEMAS
# ============================

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[float] = None
    semester: Optional[str] = None   # included if present in SQL table


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    grade: Optional[float] = None
    semester: Optional[str] = None


class EnrollmentOut(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True


# ============================
# ANALYTICS SCHEMAS
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
