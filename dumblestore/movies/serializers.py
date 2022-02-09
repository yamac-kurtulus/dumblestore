from django.forms import SlugField
from django.urls import reverse
from rest_framework import serializers
from .models import Genre, Movie, User
from django.utils.text import slugify


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class that binds User model to REST API
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "url", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer class that binds Movie model to REST API.
    A bit more constrained than user in terms of ordering and format
    """

    genres = serializers.ListSerializer(child=serializers.CharField())
    genre_order_index = serializers.HiddenField(default="")

    class Meta:
        model = Movie
        fields = ["title", "url", "genres", "slug", "genre_order_index"]
        extra_kwargs = {"url": {"lookup_field": "slug", "read_only": "True"}}
        lookup_field = "slug"

    def create(self, validated_data):
        """
        Override to add genre if not exists
        """

        genres = validated_data.pop("genres")
        instance = super().create(validated_data)
        instance = self.handle_genres(genres, instance)
        return instance

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"slug": self.slug})

    def update(self, instance, validated_data):
        """
        Custom update function to update the genre fields
        """
        genres = validated_data.pop("genres")
        instance = super().update(instance, validated_data)
        instance = self.handle_genres(genres, instance)
        return instance

    def handle_genres(self, genres, instance):
        existing_genres = Genre.objects.filter(name__in=genres).all()
        existing_genre_set = set(str(genre) for genre in existing_genres)
        missing_genres = set(genres) - existing_genre_set
        Genre.objects.bulk_create(Genre(name=genre) for genre in missing_genres)
        movie_genres = Genre.objects.filter(name__in=genres).distinct().all()
        instance.genres.set(movie_genres)
        instance.genre_order_index = "|".join(str(genre) for genre in movie_genres)
        # print(instance.genre_order_index)
        instance.save()
        return instance


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
