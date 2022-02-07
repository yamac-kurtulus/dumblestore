from django.test import TestCase
from movies.serializers import UserSerializer
from .factories import RandomUserFactory


class UserSerializerTests(TestCase):
    def setUp(self):
        self.randomUser = RandomUserFactory.create()
        self.serializer = UserSerializer(instance=self.randomUser)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ["id", "first_name", "last_name", "email", "url"]
        )
