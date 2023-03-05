from uuid import UUID
from ninja import Router
from ninja.errors import HttpError

from ..models import User
from ..schemas import UserRequest, UserResponse

router = Router()


@router.get("/", response=list[UserResponse])
def list_users(request):
    return User.objects.all()


@router.post("/", response={201: UserResponse})
def create_user(request, data: UserRequest):
    user = User.objects.create_user(email=data.email, password=data.password)
    return 201, user


@router.get("/{user_id}")
def get_user(request, user_id: UUID):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")


@router.delete("/{user_id}", response={204: None})
def delete_user(request, user_id: UUID):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        raise HttpError(404, f"user_id={user_id} not found")

    # user.delete()
    return 204, None
    