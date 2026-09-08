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


def test_get_analytics_summary_returns_expected_shape(client, db_session):
    currency = Currency(code="INR", symbol="₹", exchange_rate_to_inr=1)
    db_session.add(currency)
    db_session.flush()
    employee = Employee(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        country="India",
        department="Engineering",
        job_title="Software Engineer",
        salary_amount=Decimal("1000000"),
        currency_id=currency.id,
        hire_date=date(2023, 1, 15),
    )
    db_session.add(employee)
    db_session.commit()

    response = client.get("/api/analytics/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["by_country"][0]["group"] == "India"
    assert body["by_country"][0]["count"] == 1
    assert "salary_distribution" in body
