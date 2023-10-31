from ninja import Router

from config.security import APiKeyAuth, BearerAuth
from .auth import router as auth
from .users import router as users
from .admin.users import router as admin_users

router = Router()

router.add_router("", auth, tags=["Auth"])

router.add_router(
    "/users",
    users,
    auth=BearerAuth(),
    tags=["Auth/Users"],
)

router.add_router(
    "/admin/users",
    admin_users,
    auth=APiKeyAuth(),
    tags=["Auth/Admin/Users"],
)
