import django
import factory
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "Harry"
    last_name = "Potter"
    email = "hpotter@hogwarts.com"
    password = "hermione8"


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = "email"

    email = "albus@hogwarts.com"
