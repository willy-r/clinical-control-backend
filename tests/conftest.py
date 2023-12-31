from datetime import datetime, timezone

import mongomock
import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.main import app
from app.repositories.user import UserRepository, get_user_repository


@pytest.fixture
def mongomock_client():
    return mongomock.MongoClient('mongodb://test:123')


@pytest.fixture
def test_users_collection(mongomock_client):
    return mongomock_client.test_db.users


@pytest.fixture
def test_client(test_users_collection):
    def get_user_repository_override():
        return UserRepository(test_users_collection)

    app.dependency_overrides[
        get_user_repository
    ] = get_user_repository_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_users_collection):
    created_user = test_users_collection.insert_one(
        {
            'name': 'test',
            'email': 'test@test.com',
            'hashed_password': hash_password('123'),
            'password': '123',
            'created_at': datetime.now(tz=timezone.utc),
            'updated_at': datetime.now(tz=timezone.utc),
        }
    )
    return test_users_collection.find_one({'_id': created_user.inserted_id})
