from django.apps import AppConfig
from movies.util import init_db


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"

    def ready(self):
        import movies.signals

        init_db()
