"""
app/routers/auth.py
Authentication routes: User registration, login, and current user profile inspection.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
)
from app.security import (
    hash_password,
    verify_password,
    dummy_verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new customer account.
    Rejects duplicate emails with 409 Conflict.
    Enforces password hashing via bcrypt before database persistence.
    """
    # 1. Check for duplicate email using modern SQLAlchemy 2.x syntax
    stmt = select(User).where(User.email == payload.email)
    existing_user = db.execute(stmt).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # 2. Hash password (validates 72-byte limit)
    hashed_pwd = hash_password(payload.password)

    # 3. Create ORM instance explicitly with CUSTOMER role (prevents mass assignment)
    new_user = User(
        name=payload.name.strip(),
        email=payload.email.lower().strip(),
        password_hash=hashed_pwd,
        role=UserRole.CUSTOMER
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )

    return new_user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and generate signed JWT access token.
    Mitigates user enumeration and timing attacks by using constant-time checks
    and identical 401 error responses for both non-existent emails and wrong passwords.
    """
    email_clean = payload.email.lower().strip()
    stmt = select(User).where(User.email == email_clean)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        # User not found: run dummy bcrypt verification to prevent timing discrepancy
        dummy_verify_password(payload.password)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Issue JWT token with user id as subject claim
    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Protected endpoint: returns the authenticated user's profile.
    Pydantic UserResponse ensures password_hash is never exposed in the JSON response.
    """
    return current_user
