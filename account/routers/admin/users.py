from uuid import UUID

from asgiref.sync import sync_to_async
from ninja import Router
from ninja.errors import HttpError

from config.error_message import Http4xxMessage

from ...models import User
from ...schemas import UserRequest, UserResponse

router = Router()


@router.get("/", response=list[UserResponse])
def list_users(request):
    return User.objects.all()


@router.post("/", response={201: UserResponse, 409: Http4xxMessage})
async def create_user(request, data: UserRequest):
    user = await User.objects.create_user(email=data.email, password=data.password)
    return 201, user


@router.get("/{user_id}", response={200: UserResponse, 404: Http4xxMessage})
async def get_user(request, user_id: UUID):
    try:
        return await User.objects.aget(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")


@router.delete("/{user_id}", response={204: None, 404: Http4xxMessage})
async def delete_user(request, user_id: UUID):
    try:
        user = await User.objects.aget(pk=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")

    await sync_to_async(user.delete)()
    return 204, None
