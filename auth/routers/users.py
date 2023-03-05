from ninja import Router

from ..schemas import UserResponse

router = Router()


@router.get("/me", response=UserResponse)
def me(request):
    return request.user
