from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from .factories import CustomerUserFactory

from ..models import User
from .factories import CustomerUserFactory, RandomUserFactory


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

    def test_user_should_be_unique(self):
        harry = CustomerUserFactory.create()
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=harry.email,
                password=harry.password,
                first_name=harry.first_name,
                last_name=harry.last_name,
            )

    def test_user_should_not_be_created_with_empty_required_fields(self):
        """
        Ensures user is not created when any of the following is empty:
        first_name, last_name, email, password
        """
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
