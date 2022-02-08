import random
import factory
from factory import Faker
from ..models import Genre, Movie, User


class CustomerUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

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


class MovieWithManyGenresFactory(factory.django.DjangoModelFactory):
    """
    If called like: MovieWithManyGenresFactory(genres=3) creates a Movie with 3 genres.
    if called like: MovieWithManyGenresFactory() creates a Movie with no genres (will not be not allowed)
    """

    class Meta:
        model = Movie

    title = factory.Sequence(lambda n: "Movie #%s" % n)

    @factory.post_generation
    def genre_count(obj, create, extracted, **kwargs):

        if extracted:
            obj.genres.set(random.choices(Genre.objects.all(), k=extracted))
