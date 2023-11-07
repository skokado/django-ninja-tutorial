from http import HTTPStatus

from ninja import Schema, Field


class Http400Response(Schema):
    code: str = Field(json_schema_extra={"example": HTTPStatus.BAD_REQUEST.phrase})
    detail: str


class Http401Response(Schema):
    code: str = Field(json_schema_extra={"example": HTTPStatus.UNAUTHORIZED.phrase})
    detail: str


class Http403Response(Schema):
    code: str = Field(json_schema_extra={"example": HTTPStatus.FORBIDDEN.phrase})
    detail: str


class Http404Response(Schema):
    code: str = Field(json_schema_extra={"example": HTTPStatus.NOT_FOUND.phrase})
    detail: str


class Http409Response(Schema):
    code: str = Field(json_schema_extra={"example": HTTPStatus.CONFLICT.phrase})
    detail: str


class HttpErrorResopnse(Schema):
    code: str
    detail: str
