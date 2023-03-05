from django.contrib import admin
from django.contrib.auth.models import Group

from .models import ApiKey, User


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
