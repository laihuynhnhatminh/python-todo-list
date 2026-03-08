from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from database.db import get_db
from dtos.users import CreateUserDTO, LoginUserDTO
from models.users import Users

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "your_secret_key"  # To be moved to env
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    db: db_dependency,
    user: CreateUserDTO,
):
    exist_user = (
        db.query(Users)
        .filter((Users.email == user.email) | (Users.username == user.username))
        .first()
    )

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )

    user_model = Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role,
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    token = create_access_token(
        user.email, user_id=user_model.id, expires_delta=timedelta(minutes=30)
    )

    return {
        "message": "User registered successfully",
        "access_token": token,
    }


@router.post("/login")
async def login(
    db: db_dependency,
    user: LoginUserDTO,
):
    valid_user = authenticate_user(db, user.email, user.password)

    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user.email, user_id=valid_user.id, expires_delta=timedelta(minutes=30)
    )

    return {"message": "Login successful", "access_token": token}
