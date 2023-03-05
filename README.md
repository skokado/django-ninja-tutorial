# django-ninja-tutorial

django-ninja is very cool framework for:

- Integrate Django (ORM, admin, etc)
- Schema based request validation, typing
- Auto generate OpenAPI document (`/docs`)

# Versions

- Python: 3.11.x
- Django: 3.2.x
- django-ninja: ^0.21.0
- PyJWT: ^2.6.0

# Getting started

```shell
$ git clone https://github.com/skokado/django-ninja-tutorial.git
$ cd django-ninja-tutorial
$ python3 -m venv venv
$ source venv/bin/activate
$ poetry install
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```

then, you can see OpenAPI (Swagger) in http://localhost:8000/api/docs
