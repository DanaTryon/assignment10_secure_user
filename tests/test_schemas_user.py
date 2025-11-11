import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.base import UserCreate, UserLogin
from app.schemas.user import UserResponse, Token, TokenData

# --- UserCreate Schema Tests ---

def test_valid_user_create():
    user = UserCreate(
        first_name="Dana",
        last_name="Tryon",
        email="dana@example.com",
        username="danat",
        password="Secure123"
    )
    assert user.username == "danat"

@pytest.mark.parametrize("password", [
    "short",               # too short
    "nouppercase123",      # no uppercase
    "NOLOWERCASE123",      # no lowercase
    "NoDigitsHere",        # no digits
])
def test_invalid_passwords(password):
    with pytest.raises(ValueError):
        UserCreate(
            first_name="Dana",
            last_name="Tryon",
            email="dana@example.com",
            username="danat",
            password=password
        )

def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            first_name="Dana",
            last_name="Tryon",
            email="not-an-email",
            username="danat",
            password="Secure123"
        )

# --- UserLogin Schema Tests ---

def test_valid_user_login():
    login = UserLogin(username="danat", password="Secure123")
    assert login.username == "danat"

def test_user_login_missing_username():
    with pytest.raises(ValidationError):
        UserLogin(password="Secure123")

# --- UserResponse Schema Tests ---

def test_user_response_from_orm():
    user_dict = {
        "id": uuid4(),
        "username": "danat",
        "email": "dana@example.com",
        "first_name": "Dana",
        "last_name": "Tryon",
        "is_active": True,
        "is_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    user = UserResponse(**user_dict)
    assert user.username == "danat"
    assert user.is_active is True

# --- Token Schema Tests ---

def test_token_schema():
    user = UserResponse(
        id=uuid4(),
        username="danat",
        email="dana@example.com",
        first_name="Dana",
        last_name="Tryon",
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    token = Token(access_token="abc123", user=user)
    assert token.token_type == "bearer"
    assert token.user.email == "dana@example.com"

# --- TokenData Schema Tests ---

def test_token_data_optional():
    data = TokenData(user_id=None)
    assert data.user_id is None

def test_token_data_with_uuid():
    uid = uuid4()
    data = TokenData(user_id=uid)
    assert data.user_id == uid
