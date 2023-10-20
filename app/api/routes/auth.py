from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.auth import Login, Token
from app.core.security import create_access_token, verify_password
from app.repositories.user import UserRepository, get_user_repository

router = APIRouter(prefix='/auth', tags=['auth'])

UserRepositoryDependency = Annotated[
    UserRepository, Depends(get_user_repository)
]


@router.post('/login/', response_model=Token)
def login(login: Login, user_repository: UserRepositoryDependency):
    user = user_repository.find_by_email(login.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email or password incorrect',
        )
    if not verify_password(login.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email or password incorrect',
        )
    access_token = create_access_token({'sub': user['email']})
    return Token(access_token=access_token)
