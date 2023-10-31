from django.shortcuts import get_object_or_404
from django.http import Http404
from ninja import Router

from account.models import User
from config.security import BearerAuth
from .models import Blog
from .schemas import BlogRequest, BlogResponse

router = Router(auth=BearerAuth(), tags=["Blog"])


@router.get("", response=list[BlogResponse])
async def list_blogs(request):
    return Blog.objects.all()


@router.post("", response={201: BlogResponse})
async def create_blog(request, data: BlogRequest):
    # check author_id
    qs_author = User.objects.filter(pk=data.author_id)
    if not await qs_author.aexists():
        raise Http404()

    obj = await Blog.objects.acreate(**data.dict())
    return 201, obj


@router.get("/{blog_id}", response=BlogResponse)
async def get_blog(request, blog_id: int):
    try:
        blog = await User.objects.aget(pk=blog_id)
    except User.DoesNotExist:
        raise Http404()
    return blog


@router.delete("/{blog_id}", response={204: None})
async def delete_blog(request, blog_id: int):
    blog = await User.objects.aget(pk=blog_id)
    blog.delete()
    return 204, None
