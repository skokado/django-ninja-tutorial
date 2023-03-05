from ninja import Router
from ninja.errors import HttpError

from django_project.security import AuthBearer
from .models import Blog
from .schemas import BlogRequest, BlogResponse

router = Router(auth=AuthBearer(), tags=["Blog"])


@router.get("", response=list[BlogResponse])
def list_blogs(request):
    return Blog.objects.all()


@router.post("", response={201: BlogResponse})
def create_blog(request, data: BlogRequest):
    obj = Blog.objects.create(**data.json())
    return 201, obj


@router.get("/{blog_id}", response=BlogResponse)
def get_blog(request, blog_id: int):
    try:
        return Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, f"blog_id={blog_id} not found")


@router.delete("/{blog_id}", response={204: None})
def delete_blog(request, blog_id: int):
    return 204, None
