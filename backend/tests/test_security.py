from datetime import timedelta

import pytest
from jose import JWTError

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_hash_password_and_verify_password() -> None:
    password = "super-secret"

    password_hash = hash_password(password)

    assert isinstance(password_hash, str)
    assert password_hash != password
    assert verify_password(password, password_hash) is True


def test_verify_password_rejects_incorrect_password() -> None:
    password_hash = hash_password("super-secret")

    assert verify_password("wrong-password", password_hash) is False


def test_create_and_decode_access_token_preserves_payload() -> None:
    token = create_access_token(
        {
            "sub": "7",
            "role": "user",
        }
    )

    decoded = decode_access_token(token)

    assert decoded["sub"] == "7"
    assert decoded["role"] == "user"
    assert "exp" in decoded


def test_decode_access_token_rejects_expired_token() -> None:
    token = create_access_token(
        {
            "sub": "7",
            "role": "user",
        },
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(JWTError):
        decode_access_token(token)
