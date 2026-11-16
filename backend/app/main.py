from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine
from .security import (
    create_access_token,
    get_current_user_id,
    hash_password,
    verify_password,
)

app = FastAPI(
    title="AI Support Desk API",
    description="Backend API for the AI-powered support platform.",
    version="0.1.0",
)

@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine) 


# Allow the React app on port 5173 to call this API on port 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

class RegisterRequest(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(min_length=8, max_length=128)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/db-health", tags=["health"])
def database_health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "database connected"}

@app.post(
    "/api/auth/register",
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
def register(request: RegisterRequest) -> dict[str, str | int]:
    email = request.email.strip().lower()

    with Session(engine) as session:
        existing_user = session.scalar(
            select(models.User).where(models.User.email == email)
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        user = models.User(
            email=email,
            password_hash=hash_password(request.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "id": user.id,
            "email": user.email,
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }

@app.post("/api/auth/login", tags=["auth"])
def login(request: RegisterRequest) -> dict[str, str | int]:
    email = request.email.strip().lower()

    with Session(engine) as session:
        user = session.scalar(
            select(models.User).where(models.User.email == email)
        )

        if not user or not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "id": user.id,
            "email": user.email,
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
        }


@app.post("/api/chat", tags=["chat"])
def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
) -> dict[str, str]:
    return {"reply": f"Thanks for reaching out. I received: {request.message}"}