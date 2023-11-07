from http import HTTPStatus

from django.conf import settings
from ninja.errors import HttpError

from ninja import NinjaAPI, Schema

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
    body: Schema
    if exc.status_code == 400:
        body = error.Http400Response(detail=exc.args[0])
    elif exc.status_code == 401:
        body = error.Http401Response(detail=exc.args[0])
    elif exc.status_code == 403:
        body = error.Http403Response(detail=exc.args[0])
    elif exc.status_code == 404:
        body = error.Http404Response(detail=exc.args[0])
    elif exc.status_code == 409:
        body = error.Http409Response(detail=exc.args[0])
    else:
        body = error.HttpErrorResopnse(
            code=HTTPStatus(exc.status_code).phrase,
            message="Internal Server Error",
        )
    return api.create_response(
        request,
        body.dict(),
        status=exc.status_code,
    )
