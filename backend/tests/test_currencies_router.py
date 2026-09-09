from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.deps import get_db
from app.main import app
from app.models import Currency


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_currencies_returns_all_currencies_sorted_by_code(client, db_session):
    db_session.add_all(
        [
            Currency(code="USD", symbol="$", exchange_rate_to_inr=83),
            Currency(code="EUR", symbol="€", exchange_rate_to_inr=90),
        ]
    )
    db_session.commit()

    response = client.get("/api/currencies")

    assert response.status_code == 200
    body = response.json()
    assert [c["code"] for c in body] == ["EUR", "USD"]
    assert body[0]["symbol"] == "€"
    # exchange_rate_to_inr is required by the frontend to convert amounts
    # between currencies for the "display currency" selector.
    assert Decimal(body[0]["exchange_rate_to_inr"]) == Decimal("90")
    assert Decimal(body[1]["exchange_rate_to_inr"]) == Decimal("83")
