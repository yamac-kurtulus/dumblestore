from rest_framework.test import APITestCase, APIRequestFactory
from movies.serializers import UserSerializer
from .factories import RandomUserFactory


class UserSerializerTests(APITestCase):
    def setUp(self):
        self.randomUser = RandomUserFactory.create()
        request_stub = APIRequestFactory()
        self.serializer = UserSerializer(
            instance=self.randomUser, context={"request": request_stub.get("/")}
        )

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ["id", "first_name", "last_name", "email", "url"]
        )
