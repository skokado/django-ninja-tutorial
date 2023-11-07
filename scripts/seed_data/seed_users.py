import asyncio

from account.models import User

password = "password"

emails_to_create = [
    # email, is_superuser
    ("admin@example.com", True),
    ("user1@example.com", False),
    ("user2@example.com", False),
]


async def main():
    for (email, is_superuser) in emails_to_create:
        if is_superuser:
            print(f"created superuser email={email}")
            user = await User.objects.create_superuser(email, password)
        else:
            user = await User.objects.create_user(email, password)
            print(f"created user email={email}")


if __name__ == "django.core.management.commands.shell":
    asyncio.run(main())
