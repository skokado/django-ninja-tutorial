from typing import TypeAlias

from django.conf import settings
from django.shortcuts import get_object_or_404
import jwt
from jwt.exceptions import DecodeError

from ninja.security import HttpBearer, APIKeyHeader

from auth.models import ApiKey, User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> str | None:
        # if returns None, will be raised 401 Unauthorized.
        if settings.DEBUG and token == "supersecret":
            request.user = User.objects.first()
            return token

        try:
            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_SIGNING_ALGORITHM]
            )
        except DecodeError:
            return None

        email = decoded["sub"]
        user = get_object_or_404(User, email=email)
        request.user = user
        return token


class APiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"
    
    def authenticate(self, request, key: str) -> str | None:
        # if returns None, will be raised 401 Unauthorized.
        if settings.DEBUG and key == "supersecret":
            return key

        if ApiKey.objects.filter(key=key).exists():
            return key
        
        return None
