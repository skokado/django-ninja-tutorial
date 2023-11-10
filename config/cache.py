from typing import Literal

type Email = str


class CacheKeyPrefix:
    @staticmethod
    def me(sub: Email) -> str:
        return f"me:{sub}"
