from uuid import UUID
from ninja import Schema, Field


class LoginRequest(Schema):
    username: str
    password: str


class LoginResponse(Schema):
    sub: str = Field(json_schema_extra={"example": "email"})
    access_token: str = Field(json_schema_extra={"example": "eyJxxx.yyy.zzz"})


class UserRequest(Schema):
    email: str
    password: str


class UserResponse(Schema):
    id: UUID
    email: str
