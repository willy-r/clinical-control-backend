from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = 'super-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data_to_encode: dict[str, Any]) -> str:
    data_to_encode = data_to_encode.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp': expire})
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_passsword: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_passsword, hashed_password)
