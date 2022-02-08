from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from .factories import CustomerUserFactory

from ..models import User, Movie, Genre
from .factories import CustomerUserFactory


class UserTests(TestCase):
    def test_user_created_with_email(self):
        user = User.objects.create(
            email="test@test.com",
            password="Asd1234!",
            first_name="test",
            last_name="tester",
        )
        assert User.objects.first() is not None
        assert user.username is None

    def test_user_is_unique(self):
        harry = CustomerUserFactory.create()
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=harry.email,
                password=harry.password,
                first_name=harry.first_name,
                last_name=harry.last_name,
            )

    def test_user_not_created_with_empty_required_fields(self):
        required_data = {
            "first_name": "Lord",
            "last_name": "Voldi",
            "email": "noseless@voldi.com",
            "password": "Asd1234!",
        }

        for field_name in required_data:
            subtest_description = f"Missing '{field_name}'"
            with self.subTest(subtest_description):
                # Remove the missing field from the minimum_required_data
                data = required_data.copy()
                data.pop(field_name)
                user = User(**data)
                self.assertRaises(ValidationError, user.full_clean)


class GenreTests(TestCase):
    def test_genre_is_created(self):
        genre = Genre(name="Scifi")
        genre.full_clean()
        genre.save()

    def test_genre_not_created_with_empty_name(self):
        with self.assertRaises(ValidationError):
            genre = Genre(name="")
            genre.full_clean()
            genre.save()

    def test_genre_not_created_with_empty_name(self):
        with self.assertRaises(ValidationError):
            genre = Genre(name="")
            genre.full_clean()
            genre.save()

    def test_genre_ordered_by_name(self):
        Genre.objects.bulk_create(
            [
                Genre(name="Scifi"),
                Genre(name="Action"),
                Genre(name="Romance"),
                Genre(name="Drama"),
            ]
        )
        first = Genre.objects.first()
        last = Genre.objects.last()
        self.assertEqual(first.name, "Action")
        self.assertEqual(last.name, "Scifi")

    def test_genre_not_created_with_duplicate_name(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="Action")
            Genre.objects.create(name="Action")


class MovieTests(TestCase):
    def test_movie_is_created_with_existing_genres(self):
        genre1 = Genre.objects.create(name="Scifi")
        genre2 = Genre.objects.create(name="Action")
        movie = Movie.objects.create(
            title="Blade Runner",
        )
        movie.genres.set([genre1, genre2])
        movie.save()
        self.assertEqual(movie.title, "Blade Runner")
        self.assertEqual([x.name for x in movie.genres.all()], ["Action", "Scifi"])

    def test_movie_not_created_with_no_name(self):
        with self.assertRaises(ValidationError):
            movie = Movie(title="")
            movie.full_clean()

    def test_movie_not_created_with_duplicateName(self):
        with self.assertRaises(IntegrityError):
            Movie.objects.create(title="Blade Runner")
            Movie.objects.create(title="Blade Runner")
