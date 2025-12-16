from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.sql_db import get_db
from app.models.pydantic import UserCreate, UserOut, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import role_required

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[]
)


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


# ----------------------------------------------------
# Public Registration (Student)
# ----------------------------------------------------
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register_user(user)


# ----------------------------------------------------
# LOGIN (OAuth2 Form)
# ----------------------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Accepts:
      username=...
      password=...
    Must be sent as: application/x-www-form-urlencoded
    """

    # 🔥 DEBUG (safe version — does NOT read raw body)
    print("\n====================== LOGIN DEBUG ======================")
    print("📌 Parsed username:", form_data.username)
    print("📌 Parsed password:", form_data.password)
    print("=========================================================\n")

    return auth_service.login_user(form_data)


# ----------------------------------------------------
# Admin Registration
# ----------------------------------------------------
@router.post(
    "/admin/register",
    response_model=UserOut,
    dependencies=[Depends(role_required(["admin"]))],
    status_code=status.HTTP_201_CREATED,
)
def admin_register(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.admin_register_user(user)
