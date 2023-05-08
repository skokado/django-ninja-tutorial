from typing import Optional
import uuid
import secrets

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, username: Optional[str] = None):
        if not username:
            username = email
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username: Optional[str] = None):
        user = self.create_user(email, password, username)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("Eメールアドレス", unique=True, db_index=True)

    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー一覧"


class ApiKeyManager(models.Manager):
    pass


class ApiKey(models.Model):
    key = models.CharField("key", max_length=64, db_index=True, default=secrets.token_hex)
    memo = models.CharField("メモ", max_length=512)

    objects = ApiKeyManager()

    @classmethod
    async def create_key(cls, memo: Optional[str] = None):
        if not memo:
            memo = "auto generated"

        return await cls.objects.acreate(memo=memo)
