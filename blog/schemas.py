from ninja import ModelSchema

from auth.schemas import UserResponse

from .models import Blog


class BlogRequest(ModelSchema):
    class Config:
        model = Blog
        model_fields = ["title", "body", "author"]


class BlogResponse(ModelSchema):
    author: UserResponse

    class Config:
        model = Blog
        model_fields = ["id", "title", "body", "author"]
