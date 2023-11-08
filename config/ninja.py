from http import HTTPStatus

from django.conf import settings
from ninja.errors import HttpError

from ninja import NinjaAPI

from .common.schemas import error


api = NinjaAPI(
    title="My ninja tutorial",
    version="ninja-1.0b2",
    docs_url=None,
)

if settings.DEBUG:
    api.docs_url = "/docs"


@api.exception_handler(HttpError)
def handler(request, exc: HttpError):
    if 400 <= exc.status_code < 500:
        detail=exc.args[1]
    else:
        detail = "Internal Server Error"

    body = error.HttpErrorResopnse(
        code=HTTPStatus(exc.status_code).phrase,
        detail=detail,
    )
    return api.create_response(
        request,
        body.dict(),
        status=exc.status_code,
    )
