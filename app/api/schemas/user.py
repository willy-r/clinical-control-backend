from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UsersResponseSchema(BaseModel):
    users: list[UserResponseSchema]


class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=50)
    password: str


class UserUpdateSchema(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=50)
    password: str


class UserDbSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    password: str
