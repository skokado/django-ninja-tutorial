from django.contrib import admin

from .models import ApiKey, User


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    readonly_fields = ("key",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
