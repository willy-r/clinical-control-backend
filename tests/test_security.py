from jose import jwt

from app.core.security import ALGORITHM, SECRET_KEY, create_access_token


def test_should_generate_valid_token():
    data = {'test': 'test'}
    token = create_access_token(data)
    data_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert data_decoded['test'] == data['test']
    assert data_decoded['exp'] is not None
