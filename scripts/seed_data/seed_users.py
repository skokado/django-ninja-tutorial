from auth.models import User

password = "H0gehoge"

emails_to_create = [
    # email, is_superuser
    ("admin@example.com", True),
    ("user1@example.com", False),
    ("user2@example.com", False),
]

for (email, is_superuser) in emails_to_create:
    if is_superuser:
        user = User.objects.create_superuser(email, password)
    else:
        user = User.objects.create_user(email, password)
    print(f"created user email={email}")
