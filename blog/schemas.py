from uuid import UUID
from ninja import Schema

from account.schemas import UserResponse


class BlogRequest(Schema):
    author_id: UUID
    title: str
    body: str


class BlogResponse(Schema):
    id: UUID
    title: str
    body: str
    author: UserResponse
