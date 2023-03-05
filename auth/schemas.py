from ninja import ModelSchema, Schema, Field

from .models import User


class LoginRequest(Schema):
    username: str
    password: str


class LoginResponse(Schema):
    sub: str
    access_token: str = Field(..., description="eyJxxx.yyy.zzz")


class UserRequest(ModelSchema):
    class Config:
        model = User
        model_fields = ["email", "password"]


class UserResponse(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "email"]
