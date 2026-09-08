from datetime import date
from decimal import Decimal

import pytest

from app.db import update_employee_salary
from app.exceptions import EmployeeNotFoundError, InvalidCurrencyError
from app.models import Currency, Employee
from app.schemas import EmployeeUpdate


def _create_employee(db_session, currency):
    employee = Employee(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        country="United States",
        department="Engineering",
        job_title="Software Engineer",
        salary_amount=Decimal("120000"),
        currency_id=currency.id,
        hire_date=date(2023, 1, 15),
    )
    db_session.add(employee)
    db_session.commit()
    return employee


def _create_currency(db_session):
    usd = Currency(code="USD", symbol="$", exchange_rate_to_inr=83)
    db_session.add(usd)
    db_session.flush()
    return usd


def test_update_employee_salary_updates_fields(db_session):
    usd = _create_currency(db_session)
    employee = _create_employee(db_session, usd)

    update = EmployeeUpdate(
        department="Sales",
        job_title="Sales Manager",
        salary_amount=Decimal("95000"),
        currency_id=usd.id,
    )
    updated = update_employee_salary(db_session, employee.id, update)

    assert updated.department == "Sales"
    assert updated.job_title == "Sales Manager"
    assert updated.salary_amount == Decimal("95000")


def test_update_employee_salary_rejects_unknown_currency(db_session):
    usd = _create_currency(db_session)
    employee = _create_employee(db_session, usd)

    update = EmployeeUpdate(
        department="Sales",
        job_title="Sales Manager",
        salary_amount=Decimal("95000"),
        currency_id=999,
    )
    with pytest.raises(InvalidCurrencyError):
        update_employee_salary(db_session, employee.id, update)


def test_update_employee_salary_rejects_unknown_employee(db_session):
    usd = _create_currency(db_session)

    update = EmployeeUpdate(
        department="Sales",
        job_title="Sales Manager",
        salary_amount=Decimal("95000"),
        currency_id=usd.id,
    )
    with pytest.raises(EmployeeNotFoundError):
        update_employee_salary(db_session, 999, update)
