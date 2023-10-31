from django.conf import settings
from django.contrib.auth import authenticate
import jwt
from ninja import Router
from ninja.errors import HttpError

from ..schemas import LoginRequest, LoginResponse

router = Router()


@router.post("/login", response=LoginResponse)
async def login(request, data: LoginRequest):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "invalid credentials")

    encoded = jwt.encode(
        {"sub": data.username},
        settings.SECRET_KEY,
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )
    return LoginResponse(sub="email", access_token=encoded)


@router.get("/logout", response={204: None})
async def logout(request):
    # TODO
    return 204, None
