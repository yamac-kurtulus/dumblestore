from rest_framework import serializers
from .models import Genre, Movie, User
from django.utils.text import slugify


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class that binds User model to REST API
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "url"]


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class that binds Movie model to REST API.
    A bit more constrained than user in terms of ordering and format
    """

    genres = serializers.ListSerializer(child=serializers.CharField())
    slug = serializers.SerializerMethodField("slugify", read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "url", "genres", "slug"]

    def create(self, validated_data):
        """
        Override to add genre if not exists
        """
        genres = validated_data.pop("genres")
        movie = super().create(validated_data)
        existing_genres = Genre.objects.filter(name__in=genres).all()
        existing_genre_set = set(str(genre) for genre in existing_genres)
        missing_genres = set(genres) - existing_genre_set
        Genre.objects.bulk_create(Genre(name=genre) for genre in missing_genres)
        movie_genres = existing_genres = Genre.objects.filter(name__in=genres).all()
        movie.genres.set(movie_genres)
        return movie

    def slugify(self, obj):
        return slugify(obj.title)


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer class that binds Genre model to REST API.
    """

    name = serializers.CharField(max_length=30)

    class Meta:
        model = Genre
        fields = ["id", "name"]

    def validate(self, data):
        """
        Ensure name is saved in title case
        """
        data["name"] = data["name"].title()
        return data
