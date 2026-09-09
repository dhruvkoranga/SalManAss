from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.deps import get_db
from app.main import app
from app.models import Currency, Employee


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _make_employee(db_session):
    currency = Currency(code="USD", symbol="$", exchange_rate_to_inr=83)
    db_session.add(currency)
    db_session.flush()

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
    return employee, currency


def test_get_employees_returns_list(client, db_session):
    _make_employee(db_session)

    response = client.get("/api/employees")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["first_name"] == "Jane"


def test_get_employee_by_id_returns_employee(client, db_session):
    employee, _ = _make_employee(db_session)

    response = client.get(f"/api/employees/{employee.id}")

    assert response.status_code == 200
    assert response.json()["email"] == "jane.doe@example.com"


def test_get_employee_by_id_returns_404_when_missing(client):
    response = client.get("/api/employees/999")
    assert response.status_code == 404


def test_put_employee_updates_salary(client, db_session):
    employee, currency = _make_employee(db_session)

    response = client.put(
        f"/api/employees/{employee.id}",
        json={
            "department": "Sales",
            "job_title": "Sales Manager",
            "salary_amount": "95000",
            "currency_id": currency.id,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["department"] == "Sales"
    assert Decimal(body["salary_amount"]) == Decimal("95000")


def test_put_employee_rejects_unknown_currency(client, db_session):
    employee, _ = _make_employee(db_session)

    response = client.put(
        f"/api/employees/{employee.id}",
        json={
            "department": "Sales",
            "job_title": "Sales Manager",
            "salary_amount": "95000",
            "currency_id": 999,
        },
    )

    assert response.status_code == 400


def test_get_employees_sorts_by_first_name_descending(client, db_session):
    currency = Currency(code="USD", symbol="$", exchange_rate_to_inr=83)
    db_session.add(currency)
    db_session.flush()
    for name in ["Alice", "Charlie", "Bob"]:
        db_session.add(
            Employee(
                first_name=name,
                last_name="Test",
                email=f"{name.lower()}@example.com",
                country="United States",
                department="Engineering",
                job_title="Software Engineer",
                salary_amount=Decimal("100000"),
                currency_id=currency.id,
                hire_date=date(2023, 1, 15),
            )
        )
    db_session.commit()

    response = client.get("/api/employees?sort_by=first_name&sort_order=desc")

    assert response.status_code == 200
    names = [item["first_name"] for item in response.json()["items"]]
    assert names == ["Charlie", "Bob", "Alice"]


def test_get_employees_rejects_unknown_sort_by(client):
    response = client.get("/api/employees?sort_by=not_a_real_field")
    assert response.status_code == 422


def test_get_employees_rejects_unknown_sort_order(client):
    response = client.get("/api/employees?sort_order=sideways")
    assert response.status_code == 422


def test_get_employee_filters_returns_distinct_sorted_values(client, db_session):
    currency = Currency(code="USD", symbol="$", exchange_rate_to_inr=83)
    db_session.add(currency)
    db_session.flush()
    db_session.add_all(
        [
            Employee(
                first_name="A",
                last_name="One",
                email="a@example.com",
                country="United States",
                department="Engineering",
                job_title="Software Engineer",
                salary_amount=Decimal("100000"),
                currency_id=currency.id,
                hire_date=date(2023, 1, 15),
            ),
            Employee(
                first_name="B",
                last_name="Two",
                email="b@example.com",
                country="India",
                department="Sales",
                job_title="Sales Manager",
                salary_amount=Decimal("100000"),
                currency_id=currency.id,
                hire_date=date(2023, 1, 15),
            ),
        ]
    )
    db_session.commit()

    response = client.get("/api/employees/filters")

    assert response.status_code == 200
    body = response.json()
    # A 200 with the correct body also proves /filters is matched as its own
    # route, not swallowed by /{employee_id}: int (which would 422 trying to
    # parse "filters" as an int).
    assert body == {
        "countries": ["India", "United States"],
        "departments": ["Engineering", "Sales"],
        "roles": ["Sales Manager", "Software Engineer"],
    }
