"""
app/security.py
Cryptographic security module: direct bcrypt password hashing and PyJWT token generation.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import bcrypt
import jwt
from fastapi import HTTPException, status
from app.config import settings

# Pre-computed static dummy bcrypt hash (cost factor 12) used to execute a constant-time check
# when a user is not found, mitigating time-based account enumeration (CWE-208).
_DUMMY_SALT = b"$2b$12$e8Y4L9u20X4mJ875qg3F3."
_DUMMY_HASH = b"$2b$12$e8Y4L9u20X4mJ875qg3F3.kUj3kG5W0Z0n3oF9K1b5T3qW0E3tK4W"


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt with an adaptive cost factor of 12 rounds.
    Enforces the 72-byte limit to prevent truncation attacks and CPU DoS.
    """
    password_bytes = password.encode("utf-8")
    if not password or len(password_bytes) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be between 1 and 72 bytes"
        )
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def dummy_verify_password(plain_password: str) -> None:
    """
    Executes a dummy bcrypt check against a constant static hash to ensure
    identical latency (~250ms) even if an email is not present in the database.
    """
    try:
        bcrypt.checkpw(plain_password.encode("utf-8"), _DUMMY_HASH)
    except Exception:
        pass


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Encodes claims into a signed JSON Web Token (JWT) with HS256 and expiration.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any] | None:
    """
    Decodes and validates a signed JWT token, returning the payload if valid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        return None
