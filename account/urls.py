from django.contrib import admin
from django.urls import path
from ninja import Router
from ninja.security import django_auth, HttpBearer

from .routers import admin_router

urlpatterns = [path("", admin_router.urls)]
