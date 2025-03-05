from fastapi.testclient import TestClient
import pytest
from test.utils.cleanup import cleanup_users_db

SIGNUP_URL = "/api/user"
TEST_USER_EMAIL = "test@test.com"


def test_signup_success(test_client: TestClient):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": TEST_USER_EMAIL, "password": "123456", "username": "test"},
    )
    assert response.status_code == 201


def test_signup_invalid_email(test_client: TestClient):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test", "password": "123456", "username": "test"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "message": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
                "code": "value_error",
            }
        ]
    }


def test_signup_missing_details(test_client: TestClient):
    response_missing_email = test_client.post(
        SIGNUP_URL,
        json={"password": "123456", "username": "test"},
    )
    assert response_missing_email.status_code == 422
    print(response_missing_email.json())
    assert response_missing_email.json() == {
        "detail": [{"message": "Field required", "code": "missing"}]
    }

    response_missing_password = test_client.post(
        SIGNUP_URL,
        json={"email": TEST_USER_EMAIL, "username": "test"},
    )
    assert response_missing_password.status_code == 422
    assert response_missing_password.json() == {
        "detail": [{"message": "Field required", "code": "missing"}]
    }


def test_signup_duplicate_emails(test_client: TestClient):
    # Second signup with the same email
    response_second_signup = test_client.post(
        SIGNUP_URL,
        json={"email": TEST_USER_EMAIL, "password": "123456", "username": "test"},
    )
    assert response_second_signup.status_code == 400
    assert response_second_signup.json() == {
        "detail": [{"message": "Email already exists", "code": "email"}]
    }


def test_signup_sets_cookie(test_client: TestClient):
    response = test_client.post(
        SIGNUP_URL,
        json={"email": "test1@test.com", "password": "123456", "username": "test"},
    )
    assert response.status_code == 201
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    cleanup_users_db()
    yield
