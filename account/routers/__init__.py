from ninja import Router

from .auth import router as auth_router
from .users import router as users_router
from .admin.users import router as admin_users_router

router = Router()

router.add_router("", auth_router, tags=["Auth"])

router.add_router(
    "/users",
    users_router,
    tags=["Auth/Users"],
)

router.add_router(
    "/admin/users",
    admin_users_router,
    tags=["Auth/Admin/Users"],
)
