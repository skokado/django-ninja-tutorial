from uuid import UUID
from ninja import ModelSchema, Schema, Field


class LoginRequest(Schema):
    username: str
    password: str


class LoginResponse(Schema):
    sub: str
    access_token: str = Field(..., description="eyJxxx.yyy.zzz")


class UserRequest(Schema):
    email: str
    password: str


class UserResponse(Schema):
    id: UUID
    email: str
