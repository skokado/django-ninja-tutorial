from uuid import UUID
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from account.models import User
from config.security import BearerAuth
from .models import Blog
from .schemas import BlogRequest, BlogResponse

router = Router(auth=BearerAuth(), tags=["Blog"])


@router.get("", response=list[BlogResponse])
def list_blogs(request):
    return Blog.objects.all()


@router.post("", response={201: BlogResponse})
def create_blog(request, data: BlogRequest):
    # check author_id
    get_object_or_404(User, pk=data.author_id)
    obj = Blog.objects.create(**data.dict())
    return 201, obj


@router.get("/{blog_id}", response=BlogResponse)
def get_blog(request, blog_id: int):
    obj = get_object_or_404(User, pk=blog_id)
    return obj


@router.delete("/{blog_id}", response={204: None})
def delete_blog(request, blog_id: int):
    obj = get_object_or_404(User, pk=blog_id)
    # skip delete for example
    # obj.delete()
    return 204, None
