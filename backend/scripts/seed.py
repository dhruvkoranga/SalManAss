"""Populate app.db with 10,000 synthetic employees for local dev/demo use.

Run from backend/ with the venv active:

    python -m scripts.seed

Re-running this script clears existing Employee/Currency rows first, so it's
safe to run more than once.
"""

from app.base import Base
from app.deps import SessionLocal, engine
from app.models import Currency, Employee
from app.seed_data import CURRENCIES, build_employees

EMPLOYEE_COUNT = 10_000


def main() -> None:
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        session.query(Employee).delete()
        session.query(Currency).delete()
        session.commit()

        currencies = [Currency(**data) for data in CURRENCIES]
        session.add_all(currencies)
        session.flush()
        currency_ids = {currency.code: currency.id for currency in currencies}

        employees = build_employees(EMPLOYEE_COUNT, currency_ids)
        session.add_all(employees)
        session.commit()

        print(f"Seeded {len(employees)} employees across {len(currencies)} currencies.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
