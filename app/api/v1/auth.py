from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.sql_db import get_db
from app.models.pydantic import UserCreate, UserOut, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import role_required

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
# LOGIN (Via OAuth2 in Swagger)
# ----------------------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Accepts form data:
       username=...
       password=...
    This allows full Swagger OAuth2 login.
    """
    return auth_service.login_user(form_data)


# ----------------------------------------------------
# Admin-Only User Registration
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
