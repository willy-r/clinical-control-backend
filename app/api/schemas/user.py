from pydantic import BaseModel, EmailStr, Field


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr


class UsersResponseSchema(BaseModel):
    users: list[UserResponseSchema]


class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=50)
    password: str


class UserDbSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
