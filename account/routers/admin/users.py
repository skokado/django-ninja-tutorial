from uuid import UUID

from asgiref.sync import sync_to_async
from ninja import Router
from ninja.errors import HttpError

from config.security import APiKeyAuth
from config.common.schemas.error import (
    Http404Response,
    Http409Response,
)

from ...models import User
from ...schemas import UserRequest, UserResponse

router = Router(auth=APiKeyAuth())


@router.get("/", response=list[UserResponse])
async def list_users(request):
    # https://stackoverflow.com/questions/62530017/django-3-1-async-views-working-with-querysets
    return await sync_to_async(list)(User.objects.all())


@router.post("/", response={201: UserResponse, 409: Http409Response})
async def create_user(request, data: UserRequest):
    user = await User.objects.create_user(email=data.email, password=data.password)
    return 201, user


@router.get("/{user_id}", response={200: UserResponse, 404: Http404Response})
async def get_user(request, user_id: UUID):
    try:
        return await User.objects.aget(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")


@router.delete("/{user_id}", response={204: None, 404: Http404Response})
async def delete_user(request, user_id: UUID):
    try:
        user = await User.objects.aget(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")

    await sync_to_async(user.delete)()
    return 204, None
