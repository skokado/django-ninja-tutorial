from django.conf import settings
from django.shortcuts import get_object_or_404
import jwt
from jwt.exceptions import DecodeError

from ninja.security import HttpBearer, APIKeyHeader

from account.models import ApiKey, User


class BearerAuth(HttpBearer):
    def authenticate(self, request, token: str) -> str | None:
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGNING_ALGORITHM]
            )
        except DecodeError:
            return None

        email = decoded["sub"]
        user = get_object_or_404(User, email=email)
        if not user:
            return None
        request.user = user
        return token


class APiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key: str) -> str | None:
        if settings.DEBUG and key == "supersecret":
            return key

        if ApiKey.objects.filter(key=key).exists():
            return key

        return None
