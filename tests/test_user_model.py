import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import Base, get_engine, get_sessionmaker
import uuid
from app.models.user import Base # not from app.database to avoid circular import

# Use a separate test database (you can override this in your .env if needed)
TEST_DATABASE_URL = "sqlite:///:memory:"  # swap with test Postgres URL if needed

# Setup test engine and session
engine = get_engine(TEST_DATABASE_URL)
TestingSessionLocal = get_sessionmaker(engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()  # ensure clean state
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db: Session):
    user = User(
        first_name="Dana",
        last_name="Tryon",
        email="dana@example.com",
        username="danat",
        password=User.hash_password("securepass123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.email == "dana@example.com"

def test_register_duplicate_email(db_session):
    user_data = {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": "dana@example.com",
        "username": "danat",
        "password": "Secure123"
    }
    User.register(db_session, user_data)
    with pytest.raises(ValueError) as exc:
        User.register(db_session, user_data)
    assert "already exists" in str(exc.value)


def test_duplicate_email_username(db: Session):
    user1 = User(
        first_name="Test",
        last_name="User",
        email="dupe@example.com",
        username="dupeuser",
        password=User.hash_password("securepass123")
    )
    db.add(user1)
    db.commit()

    user2 = User(
        first_name="Test",
        last_name="User",
        email="dupe@example.com",  # duplicate email
        username="dupeuser",       # duplicate username
        password=User.hash_password("securepass123")
    )
    db.add(user2)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback() # rollback to clean state

def test_password_verification(db: Session):
    user = User(
        first_name="Verify",
        last_name="Pass",
        email="verify@example.com",
        username="verifier",
        password=User.hash_password("mypassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.verify_password("mypassword")
    assert not user.verify_password("wrongpassword")

def test_register_short_password(db_session):
    with pytest.raises(ValueError) as exc:
        User.register(db_session, {
            "first_name": "Dana",
            "last_name": "Tryon",
            "email": "dana@example.com",
            "username": "danat",
            "password": "123"
        })
    assert "Password must be at least 6 characters" in str(exc.value)


def test_token_round_trip():
    user_id = str(uuid.uuid4())
    token = User.create_access_token({"sub": user_id})
    decoded = User.verify_token(token)
    assert str(decoded) == user_id

def test_token_verification_failure():
    invalid_token = "abc.def.ghi"
    result = User.verify_token(invalid_token)
    assert result is None

def test_user_repr():
    user = User(
        first_name="Dana",
        last_name="Tryon",
        email="dana@example.com",
        username="danat",
        password="Secure123"
    )
    assert "User" in repr(user)

def test_authenticate_invalid_credentials(db_session):
    result = User.authenticate(db_session, "nonexistent", "wrongpass")
    assert result is None

def test_user_repr():
    user = User(
        first_name="Dana",
        last_name="Tryon",
        email="dana@example.com",
        username="danat",
        password="Secure123"
    )
    assert "<User(name=Dana Tryon" in repr(user)

def test_authenticate_success(db_session):
    unique_id = str(uuid.uuid4())[:8]

    user_data = {
        "first_name": "Dana",
        "last_name": "Tryon",
        "email": f"dana_{unique_id}@example.com",
        "username": f"danat_{unique_id}",
        "password": "Secure123"
    }

    User.register(db_session, user_data)
    result = User.authenticate(db_session, user_data["username"], user_data["password"])

    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["user"]["email"] == user_data["email"]

