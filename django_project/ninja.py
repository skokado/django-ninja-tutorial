from django.conf import settings

from ninja import NinjaAPI


api = NinjaAPI(
    title="My ninja tutorial", version="1.0-beta",
    docs_url=None,
)

if settings.DEBUG:
    api.docs_url = "/docs"
