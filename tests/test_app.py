from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


def test_should_return_status_200_and_hello_world():
    test_client = TestClient(app)
    response = test_client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, World!'}
