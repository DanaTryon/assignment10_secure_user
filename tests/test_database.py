#tests/test_database.py
from app.database import get_engine, get_sessionmaker, get_db

def test_get_engine_returns_engine():
    engine = get_engine("sqlite:///:memory:")
    assert engine is not None

def test_get_sessionmaker_binds_engine():
    engine = get_engine("sqlite:///:memory:")
    SessionLocal = get_sessionmaker(engine)
    session = SessionLocal()
    assert session.bind == engine
    session.close()

def test_get_db_yields_session():
    gen = get_db()
    session = next(gen)
    assert session is not None
    gen.close()
