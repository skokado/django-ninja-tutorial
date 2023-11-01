from logging import getLogger

from asgiref.sync import sync_to_async
from django.http import Http404
from ninja import Router

from account.models import User
from config.security import BearerAuth
from .models import Blog
from .schemas import BlogRequest, BlogResponse

router = Router(auth=BearerAuth(), tags=["Blog"])
logger = getLogger(__name__)


@router.get("", response=list[BlogResponse])
def list_blogs(request):
    return Blog.objects.all()


@router.post("", response={201: BlogResponse})
async def create_blog(request, data: BlogRequest):
    # check author_id
    qs_author = await sync_to_async(User.objects.filter)(pk=data.author_id)
    if not await qs_author.aexists():
        raise Http404()

    author = await qs_author.aget()
    logger.info("Create Blog")
    obj = await Blog.objects.acreate(**data.dict())
    logger.info("Created Blog")
    obj.author = author
    return 201, obj


@router.get("/{blog_id}", response=BlogResponse)
async def get_blog(request, blog_id: int):
    try:
        blog = await Blog.objects.select_related("author").aget(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404()
    return blog


@router.delete("/{blog_id}", response={204: None})
async def delete_blog(request, blog_id: int):
    try:
        blog = await Blog.objects.aget(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404()
    await sync_to_async(blog.delete)()
    return 204, None
