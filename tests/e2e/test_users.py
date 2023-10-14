from fastapi import status


def test_should_create_user(test_client):
    response = test_client.post(
        '/users',
        json={'name': 'test', 'email': 'test@test.com', 'password': '123'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_should_return_users(test_client):
    response = test_client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('users') is not None
    assert response.json()['users'] == [
        {
            'name': 'test',
            'email': 'test@test.com',
            'id': 1,
        }
    ]


def test_should_update_user(test_client):
    response = test_client.put(
        '/users/1',
        json={'name': 'test2', 'email': 'test2@test.com', 'password': '1234'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'test2',
        'email': 'test2@test.com',
        'id': 1,
    }


def test_should_not_update_user_and_return_404(test_client):
    response = test_client.put(
        '/users/2',
        json={'name': 'test2', 'email': 'test2@test.com', 'password': '1234'},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_should_delete_user(test_client):
    response = test_client.delete('/users/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_should_not_delete_user_and_return_404(test_client):
    response = test_client.delete('/users/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND
