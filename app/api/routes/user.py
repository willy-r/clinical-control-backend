from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UsersResponseSchema,
    UserUpdateSchema,
)
from app.core.security import hash_password
from app.repositories.user import UserRepository, get_user_repository

router = APIRouter(prefix='/users', tags=['users'])

UserRepositoryDependency = Annotated[
    UserRepository, Depends(get_user_repository)
]


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
def create_user(
    user: UserCreateSchema,
    user_repository: UserRepositoryDependency,
):
    db_user = user_repository.find_by_email(user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Email already exists'
        )
    hashed_password = hash_password(user.password)
    user = user.model_dump(exclude={'password'})
    user['hashed_password'] = hashed_password
    created_user = user_repository.create_user(user)
    return UserResponseSchema(id=str(created_user['_id']), **created_user)


@router.get('/', response_model=UsersResponseSchema)
def read_users(
    user_repository: UserRepositoryDependency,
    skip: int = 0,
    limit: int = 100,
):
    return {
        'users': [
            UserResponseSchema(id=str(db_user['_id']), **db_user)
            for db_user in user_repository.find_all(skip, limit)
        ]
    }


@router.put('/{user_id}/', response_model=UserResponseSchema)
def update_user(
    user_id: str,
    user: UserUpdateSchema,
    user_repository: UserRepositoryDependency,
):
    if user_repository.find_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    updated_user = user_repository.update_user_by_id(
        user_id, user.model_dump()
    )
    return UserResponseSchema(id=str(updated_user['_id']), **updated_user)


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, user_repository: UserRepositoryDependency):
    if user_repository.find_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    user_repository.delete_user_by_id(user_id)
