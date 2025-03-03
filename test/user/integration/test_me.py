import pytest
from test.utils.cleanup import cleanup_users_db
from test.utils.db_seeding import seed_database_user
from fastapi.testclient import TestClient


ME_ROUTE = "/api/user/me"


@pytest.fixture
def seed_database():
    return seed_database_user()


def test_read_users_me_with_valid_token(test_client: TestClient, seed_database: str):
    # Provide a valid token for testing
    valid_token = seed_database

    response = test_client.get(
        ME_ROUTE,
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    assert response.json().get("email") == "test@test.com"
    assert response.json().get("username") == "test_user"


def test_read_users_me_with_invalid_token(test_client: TestClient):
    # Provide an invalid token for testing
    invalid_token = "bleh"

    response = test_client.get(
        ME_ROUTE,
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": [{"message": "JWT Error", "code": None}]}


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    cleanup_users_db()
    yield
