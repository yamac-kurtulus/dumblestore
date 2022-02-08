from django.test import TestCase
from movies.models import Genre, Movie
from movies.serializers import UserSerializer, MovieSerializer, GenreSerializer
from rest_framework.exceptions import ValidationError
from .factories import RandomUserFactory


class UserSerializerTests(TestCase):
    """
    Test class to ensure serializer level methods work as intended
    """

    def setUp(self):
        self.randomUser = RandomUserFactory.create()

    def test_contains_expected_fields(self):
        serializer = UserSerializer(instance=self.randomUser, context={"request": None})
        data = serializer.data
        self.assertCountEqual(
            data.keys(), ["id", "first_name", "last_name", "email", "url"]
        )


class GenreSerializerTests(TestCase):
    """
    Test class to ensure serializer level methods work as intended
    """

    def setUp(self):
        self.genreModel = Genre.objects.create(name="Action")

    def test_genre_contains_expected_fields(self):
        """
        Ensures GenreSerializer contains expected fields
        """
        serializer = GenreSerializer(instance=self.genreModel)
        self.assertCountEqual(serializer.data.keys(), ["id", "name"])

    def test_genre_created_correctly(self):
        """
        Ensures GenreSerializer can create object correctly. Data must be saved as title case to standardize the unique name
        """
        serializer = GenreSerializer(data={"name": "adveNture"})
        serializer.is_valid(raise_exception=True)
        new_genre = serializer.save()
        self.assertEqual(new_genre.name, "Adventure")
        self.assertEqual(new_genre.id, 2)

    def test_genre_updated_correctly(self):
        """
        Ensures GenreSerializer can update object correctly. Data must be saved as title case to standardize the unique name
        """
        serializer = GenreSerializer(data={"name": "adveNture"})
        serializer.is_valid(raise_exception=True)
        new_genre = serializer.save()
        self.assertEqual(new_genre.name, "Adventure")

    def test_genre_is_read_correctly(self):
        """
        Ensures GenreSerializer can read object correctly. Data must be saved as title case to standardize the unique name
        """
        serializer = GenreSerializer(self.genreModel)
        data = serializer.data
        self.assertEqual(data["name"], "Action")
        self.assertEqual(data["id"], self.genreModel.id)


class MovieSerializerTests(TestCase):
    """
    Test class to ensure serializer level methods work as intended
    """

    def setUp(self):
        self.movieModel = Movie.objects.create(title="Blade Runner")
        g1 = Genre.objects.create(name="Action")
        g2 = Genre.objects.create(name="Scifi")
        g3 = Genre.objects.create(name="Noir")
        self.movieModel.genres.set([g1, g2, g3])

    def test_movie_contains_expected_fields(self):
        """
        Ensures MovieSerializer contains expected fields
        """
        serializer = MovieSerializer(
            instance=self.movieModel, context={"request": None}
        )
        data = serializer.data
        self.assertCountEqual(data.keys(), ["id", "title", "url", "genres", "slug"])

    def test_movie_is_read_correctly(self):
        """
        Ensures MovieSerializer can read object correctly.
        """
        serializer = MovieSerializer(
            instance=self.movieModel, context={"request": None}
        )
        data = serializer.data
        self.assertEqual(data["title"], self.movieModel.title)
        self.assertEqual(data["id"], self.movieModel.id)
        genres = data["genres"]
        self.assertCountEqual(
            genres, [genre.name for genre in self.movieModel.genres.all()]
        )

    def test_movie_is_created_correctly(self):
        """
        Ensures MovieSerializer can create object correctly.
        """
        serializer = MovieSerializer(
            context={"request": None},
            data={"title": "The Matrix", "genres": ["Action", "Scifi"]},
        )
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()
        self.assertEqual(movie.title, "The Matrix")
        self.assertCountEqual(
            [genre.name for genre in movie.genres.all()], ["Action", "Scifi"]
        )

    def test_movie_cannot_be_saved_with_no_genres(self):
        """
        Ensures MovieSerializer does not create object with no genres
        """
        serializer = MovieSerializer(
            context={"request": None},
            data={"title": "The Matrix"},
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            movie = serializer.save()

    def test_movie_can_be_saved_with_new_genres(self):
        """
        Ensures MovieSerializer can create object correctly even when genres are not already in DB
        """
        serializer = MovieSerializer(
            context={"request": None},
            data={
                "title": "The Matrix",
                "genres": ["Action", "Scifi", "Thriller", "Crime"],
            },
        )
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()
        self.assertEqual(movie.title, "The Matrix")
        self.assertCountEqual(
            [genre.name for genre in movie.genres.all()],
            ["Action", "Scifi", "Thriller", "Crime"],
        )
