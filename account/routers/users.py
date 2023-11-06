from ninja import Router

from config.security import BearerAuth
from ..schemas import UserResponse

router = Router(auth=BearerAuth())


@router.get("/me", response=UserResponse)
async def me(request):
    return request.user
