from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from app.config import settings

# -----------------------------
# PASSWORD HASHING (SAFE for Railway)
# -----------------------------
# Important: bcrypt==3.2.2 MUST be set in requirements.txt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Bcrypt only supports 72 bytes.
    Truncate manually to prevent runtime crash.
    """
    password = password[:72]   # Prevent overflow
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Truncate plain password before verifying.
    Required for bcrypt safety.
    """
    return pwd_context.verify(plain[:72], hashed)


# -----------------------------
# JWT CONFIGURATION
# -----------------------------
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# -----------------------------
# OAuth2 (Swagger Login Support)
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT Authentication"
)


# -----------------------------
# CREATE ACCESS TOKEN
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# -----------------------------
# CURRENT USER (Decode JWT)
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise credentials_exception

        return {"username": username, "role": role}

    except JWTError:
        raise credentials_exception


# -----------------------------
# ROLE-BASED ACCESS CONTROL
# -----------------------------
def role_required(roles: list[str]):
    """
    Restricts access to users with one of the required roles.
    Example use:
        Depends(role_required(["admin"]))
    """

    def wrapper(current_user=Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {roles}",
            )
        return current_user

    return wrapper
