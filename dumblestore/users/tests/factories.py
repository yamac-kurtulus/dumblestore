import factory
from factory import Faker
from ..models import User


class CustomerUser(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "Harry"
    last_name = "Potter"
    email = "hpotter@hogwarts.com"
    password = "hermione8"


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    email = "albus@hogwarts.com"


class RandomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = None
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    password = Faker("password")
