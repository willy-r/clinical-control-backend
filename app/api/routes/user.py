from fastapi import APIRouter, HTTPException, status

from app.api.schemas.user import (
    UserCreateSchema,
    UserDbSchema,
    UserResponseSchema,
    UsersResponseSchema,
)

router = APIRouter(prefix='/users', tags=['users'])

db = []  # Just to test.


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
def create_user(user: UserCreateSchema):
    db_user = UserDbSchema(**user.model_dump(), id=len(db) + 1)
    db.append(db_user)
    return db_user


@router.get('/', response_model=UsersResponseSchema)
def read_users():
    return {'users': db}


@router.put('/{user_id}', response_model=UserResponseSchema)
def update_user(user_id: int, user: UserCreateSchema):
    if user_id > len(db) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    db_user = UserDbSchema(**user.model_dump(), id=user_id)
    db[user_id - 1] = db_user
    return db_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id > len(db) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    del db[user_id - 1]
