from http import HTTPStatus

from django.conf import settings
from ninja.errors import HttpError

from ninja import NinjaAPI

from .error_message import Http4xxMessage

api = NinjaAPI(
    title="My ninja tutorial",
    version="ninja-1.0b2",
    docs_url=None,
)

if settings.DEBUG:
    api.docs_url = "/docs"


@api.exception_handler(HttpError)
def handler(request, exc: HttpError):
    body = Http4xxMessage(
        code=HTTPStatus(exc.status_code).phrase,
        message=exc.args[0],
    )
    return api.create_response(
        request,
        body.dict(),
        status=exc.status_code,
    )
