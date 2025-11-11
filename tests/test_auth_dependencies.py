# tests/test_auth_dependencies.py

import pytest
from fastapi import HTTPException
from app.auth.dependencies import get_current_user, get_current_active_user
from app.models.user import User
import uuid

def test_get_current_user_valid_token(db_session, test_user):
    token = User.create_access_token({"sub": str(test_user.id)})
    user_response = get_current_user(db_session, token)
    assert user_response.email == test_user.email

def test_get_current_user_invalid_token(db_session):
    with pytest.raises(HTTPException) as exc:
        get_current_user(db_session, "invalid.token.here")
    assert exc.value.status_code == 401

def test_get_current_user_missing_user(db_session):
    token = User.create_access_token({"sub": str(uuid.uuid4())})
    with pytest.raises(HTTPException) as exc:
        get_current_user(db_session, token)
    assert exc.value.status_code == 401

def test_get_current_active_user_success(db_session, test_user):
    token = User.create_access_token({"sub": str(test_user.id)})
    user = get_current_user(db_session, token)
    active = get_current_active_user(user)
    assert active.is_active is True

def test_get_current_active_user_failure(db_session, test_user):
    test_user.is_active = False
    db_session.commit()
    token = User.create_access_token({"sub": str(test_user.id)})
    user = get_current_user(db_session, token)
    with pytest.raises(HTTPException) as exc:
        get_current_active_user(user)
    assert exc.value.status_code == 400
