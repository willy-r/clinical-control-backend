from fastapi import status


def test_should_authenticate_user_and_return_token(test_client, test_user):
    response = test_client.post(
        '/auth/login/',
        json={'email': test_user['email'], 'password': test_user['password']},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert 'access_token' in token
    assert 'token_type' in token


def test_should_not_authenticate_for_non_existing_user(test_client):
    response = test_client.post(
        '/auth/login/',
        json={'email': 'test@test.com', 'password': '123'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_should_not_authenticate_for_wrong_password(test_client, test_user):
    response = test_client.post(
        '/auth/login/',
        json={'email': 'test@test.com', 'password': 'wrong'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
