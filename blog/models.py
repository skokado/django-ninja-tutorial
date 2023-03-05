from django.db import models


class Blog(models.Model):
    title = models.CharField("タイトル", max_length=64)
    body = models.TextField("本文")

    author = models.ForeignKey("ninja_auth.User", on_delete=models.PROTECT)
