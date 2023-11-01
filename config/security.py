from typing import Optional
from django.conf import settings
from django.http import Http404
import jwt
from jwt.exceptions import DecodeError

from ninja.security import HttpBearer, APIKeyHeader

from account.models import ApiKey, User


class BearerAuth(HttpBearer):
    async def authenticate(self, request, token: str) -> Optional[str]:
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGNING_ALGORITHM]
            )
        except DecodeError:
            return None

        try:
            # user = User.objects.get(email=decoded["sub"])
            user = await User.objects.aget(email=decoded["sub"])
        except User.DoesNotExist:
            raise Http404()

        request.user = user
        return token


class APiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    async def authenticate(self, request, key: str) -> Optional[str]:
        if settings.DEBUG and key == "supersecret":
            return key

        if await ApiKey.objects.filter(key=key).aexists():
            return key

        return None
