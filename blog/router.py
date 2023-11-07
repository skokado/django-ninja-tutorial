from logging import getLogger

from asgiref.sync import sync_to_async
from ninja import Router
from ninja.errors import HttpError

from account.models import User
from config.security import BearerAuth
from config.common.schemas.error import Http404Response

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
        raise HttpError(404, "Blog author not found")

    author = await qs_author.aget()
    logger.info("Create Blog")
    obj = await Blog.objects.acreate(**data.dict())
    logger.info("Created Blog")
    obj.author = author
    return 201, obj


@router.get("/{blog_id}", response={200: BlogResponse, 404: Http404Response})
async def get_blog(request, blog_id: int):
    try:
        blog = await Blog.objects.select_related("author").aget(pk=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, "Blog not found")
    return blog


@router.delete("/{blog_id}", response={204: None, 404: Http404Response})
async def delete_blog(request, blog_id: int):
    try:
        blog = await Blog.objects.aget(pk=blog_id)
    except Blog.DoesNotExist:
        raise HttpError(404, "Blog not found")
    await sync_to_async(blog.delete)()
    return 204, None
