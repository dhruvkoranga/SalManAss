import sqlite3

from alembic import command
from alembic.config import Config


def test_alembic_upgrade_head_creates_expected_tables(tmp_path):
    db_path = tmp_path / "migration_test.db"
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    command.upgrade(config, "head")

    conn = sqlite3.connect(db_path)
    try:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"currencies", "employees"}.issubset(tables)

        currency_columns = {row[1] for row in conn.execute("PRAGMA table_info(currencies)")}
        assert currency_columns == {"id", "code", "symbol", "exchange_rate_to_inr"}

        employee_columns = {row[1] for row in conn.execute("PRAGMA table_info(employees)")}
        assert employee_columns == {
            "id",
            "first_name",
            "last_name",
            "email",
            "country",
            "department",
            "job_title",
            "salary_amount",
            "currency_id",
            "hire_date",
            "created_at",
            "updated_at",
        }
    finally:
        conn.close()
