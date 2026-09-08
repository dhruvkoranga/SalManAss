from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import EmployeeUpdate


def _valid_payload(**overrides):
    payload = {
        "department": "Engineering",
        "job_title": "Software Engineer",
        "salary_amount": Decimal("50000"),
        "currency_id": 1,
    }
    payload.update(overrides)
    return payload


def test_accepts_a_valid_update():
    schema = EmployeeUpdate(**_valid_payload())
    assert schema.salary_amount == Decimal("50000")


def test_rejects_negative_salary():
    with pytest.raises(ValidationError):
        EmployeeUpdate(**_valid_payload(salary_amount=Decimal("-100")))


def test_rejects_zero_salary():
    with pytest.raises(ValidationError):
        EmployeeUpdate(**_valid_payload(salary_amount=Decimal("0")))


def test_requires_department():
    payload = _valid_payload()
    del payload["department"]
    with pytest.raises(ValidationError):
        EmployeeUpdate(**payload)
