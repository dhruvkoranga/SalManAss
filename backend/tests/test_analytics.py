from datetime import date
from decimal import Decimal

from app.db import get_analytics_summary
from app.models import Currency, Employee


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


def test_average_and_median_differ_when_data_is_skewed(db_session):
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, inr, email="a@example.com", salary_amount=Decimal("1000000"))
    _make_employee(db_session, inr, email="b@example.com", salary_amount=Decimal("2000000"))
    _make_employee(db_session, inr, email="c@example.com", salary_amount=Decimal("9000000"))

    summary = get_analytics_summary(db_session)

    engineering = next(g for g in summary["by_department"] if g["group"] == "Engineering")
    assert engineering["count"] == 3
    assert engineering["average_salary_inr"] == Decimal("4000000")
    assert engineering["median_salary_inr"] == Decimal("2000000")


def test_cross_currency_groups_convert_to_inr(db_session):
    usd = _create_currency(db_session, code="USD", symbol="$", rate=80)
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, usd, email="us@example.com", country="United States", salary_amount=Decimal("1000"))
    _make_employee(db_session, inr, email="in@example.com", country="India", salary_amount=Decimal("20000"))

    summary = get_analytics_summary(db_session)

    engineering = next(g for g in summary["by_department"] if g["group"] == "Engineering")
    # 1000 USD * 80 = 80,000 INR; average of 80,000 and 20,000 is 50,000
    assert engineering["average_salary_inr"] == Decimal("50000")


def test_distribution_reflects_min_and_max(db_session):
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, inr, email="a@example.com", salary_amount=Decimal("1000000"))
    _make_employee(db_session, inr, email="b@example.com", salary_amount=Decimal("2000000"))
    _make_employee(db_session, inr, email="c@example.com", salary_amount=Decimal("9000000"))

    summary = get_analytics_summary(db_session)
    distribution = summary["salary_distribution"]

    assert distribution["minimum"] == Decimal("1000000")
    assert distribution["maximum"] == Decimal("9000000")
    assert distribution["median"] == Decimal("2000000")


def test_handles_no_employees_without_crashing(db_session):
    summary = get_analytics_summary(db_session)

    assert summary["by_country"] == []
    assert summary["by_department"] == []
    assert summary["by_role"] == []
    assert summary["salary_distribution"]["minimum"] == Decimal(0)


def test_handles_single_employee(db_session):
    inr = _create_currency(db_session, code="INR", symbol="₹", rate=1)
    _make_employee(db_session, inr, email="solo@example.com", salary_amount=Decimal("500000"))

    summary = get_analytics_summary(db_session)
    distribution = summary["salary_distribution"]

    assert distribution["minimum"] == distribution["maximum"] == Decimal("500000")
