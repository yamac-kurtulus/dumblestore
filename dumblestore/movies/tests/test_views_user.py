from urllib.parse import urljoin
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ..serializers import UserSerializer
from .factories import AdminFactory, CustomerUserFactory, RandomUserFactory


class UsersTests(APITestCase):
    def setUp(self):
        """
        Creates a customer user "Harry Potter" and uses this user in the requests
        """
        self.APIuser = CustomerUserFactory.create()
        self.client.force_authenticate(user=self.APIuser)
        self.url = reverse("user-list")

        # populate it
        RandomUserFactory.create(email="user1@hogwarts.com")
        RandomUserFactory.create(email="user2@hogwarts.com")
        RandomUserFactory.create(email="user3@hogwarts.com")

        # use this as post data:

    def test_customers_cannot_view_users(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_view_user_details(self):
        url = urljoin(self.url, "user1@hogwarts.com/")
        resp = self.client.get(self.url + "")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_create_users(self):
        u = RandomUserFactory.build(email="user3@hogwarts.com")
        postData = {
            "first_name": "Lord",
            "last_name": "Voldi",
            "email": "noseless@voldi.com",
            "password": "Asd1234!",
        }
        resp = self.client.post(path=self.url, data=postData)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_update_users(self):
        postData = {
            "first_name": "Lord",
            "last_name": "Voldi",
            "password": "Asd1234!",
        }
        resp = self.client.put(self.url + "user1@hogwarts.com/", data=postData)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_delete_users(self):
        resp = self.client.delete(self.url + "user1@hogwarts.com/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_can_view_own_details(self):
        resp = self.client.get(self.url + "me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], self.APIuser.email)
        pass


class AdminUserTests(APITestCase):
    def setUp(self):
        """
        Creates or gets an admin user and uses that to test the functionality
        """
        self.APIuser = AdminFactory.create()
        self.client.force_authenticate(user=self.APIuser)
        self.url = reverse("user-list")

        # populate it
        RandomUserFactory.create(email="user1@hogwarts.com")
        RandomUserFactory.create(email="user2@hogwarts.com")
        RandomUserFactory.create(email="user3@hogwarts.com")

    def test_admin_can_view_users(self):
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data), 4)

    def test_admin_can_view_users_with_pagination(self):
        RandomUserFactory.create_batch(100)
        self.url = urljoin(self.url, "?page=2")
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data), 20)

    def test_admin_can_view_user_details(self):
        self.url = urljoin(self.url, "user1@hogwarts.com/")
        resp = self.client.get(self.url)
        resp = self.client.put(self.url, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_user(self):
        pass

    def test_admin_can_update_user(self):
        self.url = urljoin(self.url, "user1@hogwarts.com/")
        resp = self.client.get(self.url)
        resp = self.client.put(self.url, resp.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_user(self):

        pass
