from fastapi import status


def test_should_create_user(test_client):
    response = test_client.post(
        '/users/',
        json={'name': 'test', 'email': 'test@test.com', 'password': '123'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.json()
    assert 'created_at' in response.json()
    assert 'updated_at' in response.json()
    assert 'password' not in response.json()
    assert response.json()['name'] == 'test'
    assert response.json()['email'] == 'test@test.com'


def test_should_not_create_user(test_client, test_user):
    response = test_client.post(
        '/users/',
        json={'name': 'test', 'email': test_user['email'], 'password': '123'},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_should_return_users(test_client, test_user):
    response = test_client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'users': [
            {
                'id': str(test_user['_id']),
                'name': test_user['name'],
                'email': test_user['email'],
                'updated_at': test_user['updated_at'].isoformat(),
                'created_at': test_user['created_at'].isoformat(),
            }
        ]
    }


def test_should_not_return_users(test_client):
    response = test_client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': []}


def test_should_update_user(test_client, test_user):
    response = test_client.put(
        f"/users/{test_user['_id']}",
        json={
            'name': 'update',
            'email': 'test@update.com',
            'password': '1234',
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'password' not in response.json()
    assert response.json()['id'] == str(test_user['_id'])
    assert response.json()['created_at'] == test_user['created_at'].isoformat()
    assert response.json()['updated_at'] != test_user['updated_at'].isoformat()
    assert response.json()['name'] == 'update'
    assert response.json()['email'] == 'test@update.com'


def test_should_not_update_user_and_return_404(test_client):
    response = test_client.put(
        '/users/652db0169324e9d8df2b0507',
        json={
            'name': 'update',
            'email': 'test@update.com',
            'password': '1234',
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_should_delete_user(test_client, test_user):
    response = test_client.delete(f"/users/{test_user['_id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_should_not_delete_user_and_return_404(test_client):
    response = test_client.delete('/users/652db0169324e9d8df2b0507')
    assert response.status_code == status.HTTP_404_NOT_FOUND
