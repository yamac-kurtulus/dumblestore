from distutils.command.build_scripts import first_line_re
import email
import json

from django.forms import ValidationError
from .models import User, Movie, Genre


def read_data(filename):
    f = open(filename)
    data = json.load(f)

    for log in data:
        email = log["email"]
        try:
            password = f"{log['first_name']}42"
            user = User(
                first_name=log["first_name"],
                last_name=log["last_name"],
                email=email,
                password=password,
            )
            user.full_clean()
            user.save()
        except ValidationError as v:
            print(f"{email} already exists. Skipping")

        title = log["Movie Title"]
        try:
            movie, created = Movie.objects.get_or_create(title=title)
            movie.full_clean()
            movie.save()

            genres = log["Movie Genres"]
            for genre in genres.split("|"):
                g, created = Genre.objects.get_or_create(name=genre)
                movie.genres.add(g)
                movie.save()

        except ValidationError as v:
            print(f"{title} already exists. Skipping")
