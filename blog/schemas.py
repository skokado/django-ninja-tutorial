from uuid import UUID
from ninja import ModelSchema

from account.schemas import UserResponse

from .models import Blog


class BlogRequest(ModelSchema):
    author_id: UUID

    class Config:
        model = Blog
        model_fields = ["title", "body"]


class BlogResponse(ModelSchema):
    author: UserResponse

    class Config:
        model = Blog
        model_fields = ["id", "title", "body", "author"]
