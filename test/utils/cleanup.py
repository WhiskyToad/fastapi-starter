from sqlalchemy import text
import pytest
from test.conftest import TestingSessionLocal


def cleanup_users_db():
    # This fixture will be executed after all tests in the module
    # Clean up the mock database, delete all test data, etc.
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()
