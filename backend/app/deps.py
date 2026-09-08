from app.base import Base
from app.db import create_session_factory

engine, SessionLocal = create_session_factory(
    "sqlite:///./app.db", connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
