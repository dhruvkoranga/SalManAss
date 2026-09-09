import random

from app.models import Currency, Employee
from app.seed_data import COUNTRY_CURRENCY, CURRENCIES, ROLES, build_employees


def _insert_currencies(session) -> dict[str, int]:
    currencies = [Currency(**data) for data in CURRENCIES]
    session.add_all(currencies)
    session.flush()
    return {c.code: c.id for c in currencies}


def test_build_employees_generates_requested_count(db_session):
    currency_ids = _insert_currencies(db_session)
    employees = build_employees(200, currency_ids, rng=random.Random(42))
    db_session.add_all(employees)
    db_session.commit()

    assert db_session.query(Employee).count() == 200


def test_build_employees_have_unique_emails(db_session):
    currency_ids = _insert_currencies(db_session)
    employees = build_employees(200, currency_ids, rng=random.Random(1))

    emails = [employee.email for employee in employees]
    assert len(emails) == len(set(emails))


def test_build_employees_reference_valid_currency_and_positive_salary(db_session):
    currency_ids = _insert_currencies(db_session)
    employees = build_employees(200, currency_ids, rng=random.Random(2))
    db_session.add_all(employees)
    db_session.commit()

    valid_currency_ids = set(currency_ids.values())
    for employee in employees:
        assert employee.currency_id in valid_currency_ids
        assert employee.salary_amount > 0


def test_build_employees_use_known_countries_departments_and_roles(db_session):
    currency_ids = _insert_currencies(db_session)
    employees = build_employees(200, currency_ids, rng=random.Random(3))

    known_department_role_pairs = {(department, job_title) for department, job_title, _, _ in ROLES}
    for employee in employees:
        assert employee.country in COUNTRY_CURRENCY
        assert (employee.department, employee.job_title) in known_department_role_pairs
