from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection, ReturnDocument

from app.api.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UsersResponseSchema,
    UserUpdateSchema,
)
from app.database.mongodb import get_users_collection

router = APIRouter(prefix='/users', tags=['users'])

UsersCollectionDependency = Annotated[
    Collection, Depends(get_users_collection)
]


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
def create_user(
    user: UserCreateSchema,
    users_collection: UsersCollectionDependency,
):
    db_user = users_collection.find_one({'email': user.email})
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Email already exists'
        )
    user_data = user.model_dump()
    user_data['created_at'] = datetime.now(tz=timezone.utc)
    user_data['updated_at'] = datetime.now(tz=timezone.utc)
    created_user = users_collection.insert_one(user_data)
    db_created_user = users_collection.find_one(
        {'_id': created_user.inserted_id}
    )
    return UserResponseSchema(
        id=str(db_created_user['_id']), **db_created_user
    )


@router.get('/', response_model=UsersResponseSchema)
def read_users(
    users_collection: UsersCollectionDependency,
    skip: int = 0,
    limit: int = 100,
):
    return {
        'users': [
            UserResponseSchema(id=str(db_user['_id']), **db_user)
            for db_user in users_collection.find().limit(limit).skip(skip)
        ]
    }


@router.put('/{user_id}/', response_model=UserResponseSchema)
def update_user(
    user_id: str,
    user: UserUpdateSchema,
    users_collection: UsersCollectionDependency,
):
    user_data = user.model_dump()
    user_data['updated_at'] = datetime.now(tz=timezone.utc)
    updated_user = users_collection.find_one_and_update(
        {'_id': ObjectId(user_id)},
        {'$set': user_data},
        return_document=ReturnDocument.AFTER,
    )
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return UserResponseSchema(id=str(updated_user['_id']), **updated_user)


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, users_collection: UsersCollectionDependency):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if not result.deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
