from uuid import UUID

from asgiref.sync import sync_to_async
from ninja import Router
from ninja.errors import HttpError

from ...models import User
from ...schemas import UserRequest, UserResponse

router = Router()


@router.get("/", response=list[UserResponse])
async def list_users(request):
    return await sync_to_async(User.objects.all)()


@router.post("/", response={201: UserResponse})
async def create_user(request, data: UserRequest):
    user = await sync_to_async(User.objects.create_user)(email=data.email, password=data.password)
    return 201, user


@router.get("/{user_id}")
async def get_user(request, user_id: UUID):
    try:
        return await User.objects.aget(user_id=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")


@router.delete("/{user_id}", response={204: None})
async def delete_user(request, user_id: UUID):
    try:
        user = User.objects.aget(user_id=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")

    user.delete()
    return 204, None
