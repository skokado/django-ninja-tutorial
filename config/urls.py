"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from account.routers import router as account_router
from blog.router import router as blog_router

from .security import BearerAuth
from .ninja import api

api.add_router("/account", account_router)

api.add_router("/blogs", blog_router, auth=BearerAuth())


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
