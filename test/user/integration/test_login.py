import pytest
from test.utils.cleanup import cleanup_users_db
from test.utils.db_seeding import seed_database_user
from fastapi.testclient import TestClient

LOGIN_URL = "/api/user/login"
TEST_USER_EMAIL = "test@test.com"
VALUE_ERROR_MISSING = "value_error.missing"


@pytest.fixture
def seed_database():
    seed_database_user()


def test_login_success(test_client: TestClient, seed_database: str):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": TEST_USER_EMAIL,
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


def test_login_invalid_password(test_client: TestClient):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": TEST_USER_EMAIL,
            "password": "1234567",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": [{"message": "Incorrect email or password", "code": None}]
    }


def test_login_invalid_username(test_client: TestClient):
    response = test_client.post(
        LOGIN_URL,
        data={
            "username": "test@bla.com",
            "password": "password",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": [{"message": "Incorrect email or password", "code": None}]
    }


def test_missing_details(test_client: TestClient):
    response_missing_email = test_client.post(
        LOGIN_URL,
        data={"password": "password"},
    )
    assert response_missing_email.status_code == 422
    assert response_missing_email.json() == {
        "detail": [
            {
                "code": VALUE_ERROR_MISSING,
                "message": "field required",
            }
        ]
    }
    response_missing_password = test_client.post(
        LOGIN_URL,
        data={"username": TEST_USER_EMAIL},
    )
    assert response_missing_password.status_code == 422
    assert response_missing_password.json() == {
        "detail": [
            {
                "code": VALUE_ERROR_MISSING,
                "message": "field required",
            }
        ]
    }


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    cleanup_users_db()
    yield
