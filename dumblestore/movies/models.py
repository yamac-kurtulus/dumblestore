from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    """
    Genres can belong to multiple movies
    """

    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Movie object. Has a title and multiple genres
    """

    title = models.CharField(max_length=100, db_index=True, unique=True)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
