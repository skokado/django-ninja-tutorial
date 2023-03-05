from ninja import Router

from django_project.security import APiKeyAuth, AuthBearer

router = Router()

from .auth import router as auth
router.add_router("", auth, tags=["Auth"])

from .users import router as users
router.add_router(
    "/users", users,
    auth=AuthBearer(),
    tags=["Auth/Users"],
)

from .admin_users import router as admin_users
router.add_router(
    "/admin/users", admin_users,
    auth=APiKeyAuth(),
    tags=["Auth/Admin/Users"],
)
