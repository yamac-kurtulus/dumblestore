from django.db import IntegrityError
from django.test import TestCase

from ..models import User
from .factories import UserFactory, AdminFactory


class UserTests(TestCase):
    def test_user_created_with_email(self):
        user = User.objects.create(
            email="hpotter@hogwarts.com",
            password="hermione8",
        )
        assert User.objects.first() is not None
        assert user.username is None

    def test_user_should_be_unique(self):
        harry = UserFactory()
        with self.assertRaises(IntegrityError):
            User.objects.create(email=harry.email)
