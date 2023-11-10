from logging import getLogger

from asgiref.sync import sync_to_async
from ninja import Router
from ninja.errors import HttpError

from config.security import BearerAuth
from config.common.schemas.error import Http404Response

from .models import Blog
from .schemas import BlogRequest, BlogResponse

router = Router(auth=BearerAuth(), tags=["Blog"])
logger = getLogger(__name__)


@router.get("", response=list[BlogResponse])
async def list_blogs(request):
    return await sync_to_async(list)(Blog.objects.all())


@router.post("", response={201: BlogResponse})
async def create_blog(request, data: BlogRequest):
    logger.info("Create Blog")
    data.author_id = request.user.id
    obj = await Blog.objects.acreate(**data.dict())
    obj.author = request.user
    logger.info("Created Blog")
    return 201, obj


@router.get("/{blog_id}", response={200: BlogResponse, 404: Http404Response})
async def get_blog(request, blog_id: int):
    try:
        blog = await Blog.objects.select_related("author").aget(pk=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, "Blog not found")
    return blog


@router.delete("/{blog_id}", response={204: None})
async def delete_blog(request, blog_id: int):
    await Blog.objects.filter(pk=blog_id).adelete()
    return 204, None
