from typing import Optional

from ninja.errors import HttpError
from ninja.security import HttpBearer, APIKeyHeader
from django.conf import settings
from django.core.cache import cache
import jwt
from jwt.exceptions import DecodeError

from account.models import ApiKey, User
from config.cache import CacheKeyPrefix


class BearerAuth(HttpBearer):
    async def authenticate(self, request, token: str) -> Optional[str]:
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGNING_ALGORITHM]
            )
        except DecodeError:
            return None

        # Check from me/ cache
        email = decoded["sub"]
        cache_me_key = CacheKeyPrefix.me(email)

        user_from_cache = cache.get(cache_me_key)
        if user_from_cache:
            request.user = user_from_cache
            return token

        try:
            user = await User.objects.aget(email=decoded["sub"])
            request.user = user
            cache.set(cache_me_key, user)
        except User.DoesNotExist:
            raise HttpError(401, "Invalid token")

        return token


class APiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    async def authenticate(self, request, key: Optional[str] = None) -> Optional[str]:
        if not key:
            return None

        # Only debug mode
        if settings.DEBUG and key == "secret":
            return key

        if await ApiKey.objects.filter(key=key, active=True).aexists():
            return key

        return None
