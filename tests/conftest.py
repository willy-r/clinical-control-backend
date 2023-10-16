from datetime import datetime, timezone

import mongomock
import pytest
from fastapi.testclient import TestClient

from app.database.mongodb import get_users_collection
from app.main import app


@pytest.fixture
def mongomock_client():
    return mongomock.MongoClient('mongodb://test:123')


@pytest.fixture
def test_users_collection(mongomock_client):
    return mongomock_client.test_db.users


@pytest.fixture
def test_client(test_users_collection):
    def get_users_collection_override():
        return test_users_collection

    app.dependency_overrides[
        get_users_collection
    ] = get_users_collection_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_users_collection):
    created_user = test_users_collection.insert_one(
        {
            'name': 'test',
            'email': 'test@test.com',
            'password': '123',
            'created_at': datetime.now(tz=timezone.utc),
            'updated_at': datetime.now(tz=timezone.utc),
        }
    )
    return test_users_collection.find_one({'_id': created_user.inserted_id})
