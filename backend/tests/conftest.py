import pytest
from sqlalchemy.pool import StaticPool

from app.base import Base
from app.db import create_session_factory


@pytest.fixture()
def db_session():
    # SQLite's :memory: database only exists within one connection. SQLAlchemy's
    # default pool opens a new connection per query, which would mean a fresh,
    # empty database each time. StaticPool forces one shared connection so the
    # schema and data created here actually persist for the duration of the test.
    engine, SessionLocal = create_session_factory(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
