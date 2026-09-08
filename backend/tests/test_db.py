from datetime import date
from decimal import Decimal

import pytest

from app.db import list_employees, update_employee_salary
from app.exceptions import EmployeeNotFoundError, InvalidCurrencyError
from app.models import Currency, Employee
from app.schemas import EmployeeUpdate


def _create_currency(db_session, code="USD", symbol="$", rate=83):
    currency = Currency(code=code, symbol=symbol, exchange_rate_to_inr=rate)
    db_session.add(currency)
    db_session.flush()
    return currency


def _make_employee(db_session, currency, **overrides):
    defaults = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "country": "United States",
        "department": "Engineering",
        "job_title": "Software Engineer",
        "salary_amount": Decimal("120000"),
        "currency_id": currency.id,
        "hire_date": date(2023, 1, 15),
    }
    defaults.update(overrides)
    employee = Employee(**defaults)
    db_session.add(employee)
    db_session.commit()
    return employee


def test_update_employee_salary_updates_fields(db_session):
    usd = _create_currency(db_session)
    employee = _make_employee(db_session, usd)

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
    employee = _make_employee(db_session, usd)

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


def test_list_employees_returns_all_when_no_filters(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, first_name="Jane", last_name="Doe", email="jane@example.com")
    _make_employee(db_session, usd, first_name="John", last_name="Smith", email="john@example.com")
    _make_employee(
        db_session, usd, first_name="Amit", last_name="Shah", email="amit@example.com", country="India"
    )

    items, total = list_employees(db_session)

    assert total == 3
    assert len(items) == 3


def test_list_employees_filters_by_country(db_session):
    usd = _create_currency(db_session)
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, usd, email="us@example.com", country="United States")
    _make_employee(db_session, inr, email="in@example.com", country="India")

    items, total = list_employees(db_session, country="India")

    assert total == 1
    assert items[0].country == "India"


def test_list_employees_filters_by_department(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", department="Engineering")
    _make_employee(db_session, usd, email="sales@example.com", department="Sales")

    items, total = list_employees(db_session, department="Sales")

    assert total == 1
    assert items[0].department == "Sales"


def test_list_employees_filters_by_job_title(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", job_title="Software Engineer")
    _make_employee(db_session, usd, email="mgr@example.com", job_title="Sales Manager")

    items, total = list_employees(db_session, job_title="Sales Manager")

    assert total == 1
    assert items[0].job_title == "Sales Manager"


def test_list_employees_search_matches_name_case_insensitive(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, first_name="Jane", last_name="Doe", email="jane@example.com")
    _make_employee(db_session, usd, first_name="John", last_name="Smith", email="john@example.com")

    items, total = list_employees(db_session, search="jane")

    assert total == 1
    assert items[0].first_name == "Jane"


def test_list_employees_search_matches_email(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, first_name="Jane", last_name="Doe", email="jane.doe@example.com")
    _make_employee(db_session, usd, first_name="John", last_name="Smith", email="john.smith@example.com")

    items, total = list_employees(db_session, search="john.smith")

    assert total == 1
    assert items[0].email == "john.smith@example.com"


def test_list_employees_paginates(db_session):
    usd = _create_currency(db_session)
    for i in range(5):
        _make_employee(
            db_session,
            usd,
            first_name=f"Employee{i}",
            last_name="Test",
            email=f"employee{i}@example.com",
        )

    first_page, total = list_employees(db_session, page=1, page_size=2)
    second_page, _ = list_employees(db_session, page=2, page_size=2)

    assert total == 5
    assert len(first_page) == 2
    assert len(second_page) == 2
    assert {e.id for e in first_page}.isdisjoint({e.id for e in second_page})
