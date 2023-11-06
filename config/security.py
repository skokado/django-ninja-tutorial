from typing import Optional
from ninja.errors import HttpError
from django.conf import settings
import jwt
from jwt.exceptions import DecodeError

from ninja.security import HttpBearer, APIKeyHeader

from account.models import ApiKey, User


class BearerAuth(HttpBearer):
    # NOTE I DO NOT recommend to use async-auth now (2023/11)
    # Ref https://github.com/vitalik/django-ninja/issues/44
    def authenticate(self, request, token: str) -> Optional[str]:
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_SIGNING_ALGORITHM]
            )
        except DecodeError:
            return None
        try:
            user = User.objects.get(email=decoded["sub"])
            request.user = user
        except User.DoesNotExist:
            raise HttpError(401, "Invalid token")

        return token


class APiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key: Optional[str] = None) -> Optional[str]:
        # Do not use async mode because same as above
        if not key:
            return None

        # Only debug mode
        if settings.DEBUG and key == "secret":
            return key

        if ApiKey.objects.filter(key=key).exists():
            return key

        return None
