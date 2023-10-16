from pymongo import MongoClient

from app.core.settings import settings


def get_mongodb_client():  # pragma: no cover
    return MongoClient(settings.MONGODB_URL)


def get_users_collection():  # pragma: no cover
    mongodb_client = get_mongodb_client()
    mongodb_database = mongodb_client[settings.MONGODB_DATABASE]
    return mongodb_database[settings.MONGODB_USERS_COLLECTION]
