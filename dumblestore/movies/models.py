from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where we use emails to authenticate. Also it is good practice to not use Django's default User model.
    """

    def create_user(self, email, password, **kwargs):
        """
        Create and save a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):

    """
    User model that uses the custom manager to manage auth
    """

    username = None
    email = models.EmailField("Email Address", unique=True)
    first_name = models.CharField("first_name", max_length=50, blank=False)
    last_name = models.CharField("last_name", max_length=50, blank=False)
    objects = UserManager()

    # Override Django's default Username Field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


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

    title = models.CharField(max_length=100, db_index=True, unique=True, blank=False)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
