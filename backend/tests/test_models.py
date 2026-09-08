from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Currency, Employee


def test_employee_persists_with_its_currency(db_session):
    usd = Currency(code="USD", symbol="$", exchange_rate_to_inr=83)
    db_session.add(usd)
    db_session.flush()

    employee = Employee(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        country="United States",
        department="Engineering",
        job_title="Software Engineer",
        salary_amount=120000,
        currency_id=usd.id,
        hire_date=date(2023, 1, 15),
    )
    db_session.add(employee)
    db_session.commit()

    fetched = db_session.query(Employee).filter_by(email="jane.doe@example.com").one()
    assert fetched.first_name == "Jane"
    assert fetched.salary_amount == 120000
    assert fetched.currency.code == "USD"
    assert fetched.currency.exchange_rate_to_inr == 83


def test_rejects_employee_with_nonexistent_currency(db_session):
    employee = Employee(
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        country="India",
        department="Sales",
        job_title="Sales Manager",
        salary_amount=500000,
        currency_id=999,  # no Currency row with this id exists
        hire_date=date(2023, 1, 15),
    )
    db_session.add(employee)
    with pytest.raises(IntegrityError):
        db_session.commit()
