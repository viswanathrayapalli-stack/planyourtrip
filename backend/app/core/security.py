from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from pwdlib import PasswordHash

from app.core.settings import settings
from jose import JWTError, jwt

# -------------------------
# Password Hashing
# -------------------------

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain text password against its hash."""
    return password_hasher.verify(password, password_hash)


# -------------------------
# JWT
# -------------------------

def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )