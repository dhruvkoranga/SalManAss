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


def test_list_employees_filters_by_country_case_insensitive(db_session):
    usd = _create_currency(db_session)
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, usd, email="us@example.com", country="United States")
    _make_employee(db_session, inr, email="in@example.com", country="India")

    items, total = list_employees(db_session, country="india")

    assert total == 1
    assert items[0].country == "India"


def test_list_employees_filters_by_department(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", department="Engineering")
    _make_employee(db_session, usd, email="sales@example.com", department="Sales")

    items, total = list_employees(db_session, department="Sales")

    assert total == 1
    assert items[0].department == "Sales"


def test_list_employees_filters_by_department_case_insensitive(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", department="Engineering")
    _make_employee(db_session, usd, email="sales@example.com", department="Sales")

    items, total = list_employees(db_session, department="sales")

    assert total == 1
    assert items[0].department == "Sales"


def test_list_employees_filters_by_job_title(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", job_title="Software Engineer")
    _make_employee(db_session, usd, email="mgr@example.com", job_title="Sales Manager")

    items, total = list_employees(db_session, job_title="Sales Manager")

    assert total == 1
    assert items[0].job_title == "Sales Manager"


def test_list_employees_filters_by_job_title_case_insensitive(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="eng@example.com", job_title="Software Engineer")
    _make_employee(db_session, usd, email="mgr@example.com", job_title="Sales Manager")

    items, total = list_employees(db_session, job_title="sales manager")

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


def test_list_employees_sorts_by_first_name_ascending(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, first_name="Charlie", email="c@example.com")
    _make_employee(db_session, usd, first_name="Alice", email="a@example.com")
    _make_employee(db_session, usd, first_name="Bob", email="b@example.com")

    items, _ = list_employees(db_session, sort_by="first_name", sort_order="asc")

    assert [e.first_name for e in items] == ["Alice", "Bob", "Charlie"]


def test_list_employees_sorts_by_first_name_descending(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, first_name="Charlie", email="c@example.com")
    _make_employee(db_session, usd, first_name="Alice", email="a@example.com")
    _make_employee(db_session, usd, first_name="Bob", email="b@example.com")

    items, _ = list_employees(db_session, sort_by="first_name", sort_order="desc")

    assert [e.first_name for e in items] == ["Charlie", "Bob", "Alice"]


def test_list_employees_sorts_by_hire_date(db_session):
    usd = _create_currency(db_session)
    _make_employee(db_session, usd, email="a@example.com", hire_date=date(2022, 1, 1))
    _make_employee(db_session, usd, email="b@example.com", hire_date=date(2020, 1, 1))
    _make_employee(db_session, usd, email="c@example.com", hire_date=date(2024, 1, 1))

    items, _ = list_employees(db_session, sort_by="hire_date", sort_order="asc")

    assert [e.email for e in items] == ["b@example.com", "a@example.com", "c@example.com"]


def test_list_employees_sorts_by_salary_uses_inr_equivalent_value(db_session):
    usd = _create_currency(db_session, code="USD", symbol="$", rate=83)
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, usd, email="a@example.com", salary_amount=Decimal("20000"))
    _make_employee(db_session, inr, email="b@example.com", salary_amount=Decimal("800000"))
    # Raw amounts would sort ascending as [a, b] (20000 < 800000). In INR-
    # equivalent terms a earns more (20000 * 83 = 1,660,000) than b (800,000),
    # so the correct ascending order is [b, a] — this fails if the sort ever
    # regresses to comparing raw salary_amount instead of the converted value.

    items, _ = list_employees(db_session, sort_by="salary_amount", sort_order="asc")

    assert [e.email for e in items] == ["b@example.com", "a@example.com"]


def test_list_employees_sorts_by_salary_descending_uses_inr_equivalent_value(db_session):
    usd = _create_currency(db_session, code="USD", symbol="$", rate=83)
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, usd, email="a@example.com", salary_amount=Decimal("20000"))
    _make_employee(db_session, inr, email="b@example.com", salary_amount=Decimal("800000"))

    items, _ = list_employees(db_session, sort_by="salary_amount", sort_order="desc")

    assert [e.email for e in items] == ["a@example.com", "b@example.com"]
