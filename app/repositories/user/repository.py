from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument

from app.database.mongodb import get_users_collection
from app.repositories.user import BaseUserRepository


class UserRepository(BaseUserRepository):
    def __init__(self, users_collection: Collection) -> None:
        self.users_collection = users_collection

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        return self.users_collection.find_one({'email': email})

    def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        user = user.copy()
        user['created_at'] = datetime.now(tz=timezone.utc)
        user['updated_at'] = datetime.now(tz=timezone.utc)
        result = self.users_collection.insert_one(user)
        return self.users_collection.find_one({'_id': result.inserted_id})

    def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        return self.users_collection.find().limit(limit).skip(skip)

    def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self.users_collection.find_one({'_id': ObjectId(user_id)})

    def update_user_by_id(
        self, user_id: str, user: dict[str, Any]
    ) -> dict[str, Any]:
        user = user.copy()
        user['updated_at'] = datetime.now(tz=timezone.utc)
        return self.users_collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': user},
            return_document=ReturnDocument.AFTER,
        )

    def delete_user_by_id(self, user_id: str) -> None:
        self.users_collection.delete_one({'_id': ObjectId(user_id)})


def get_user_repository() -> UserRepository:  # pragma: no cover
    return UserRepository(get_users_collection())
