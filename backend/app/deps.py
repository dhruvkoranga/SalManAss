from app.db import create_session_factory

# Schema is owned by Alembic migrations (see backend/alembic/) — run
# `alembic upgrade head` before starting the app, not create_all() here.
engine, SessionLocal = create_session_factory(
    "sqlite:///./app.db", connect_args={"check_same_thread": False}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
