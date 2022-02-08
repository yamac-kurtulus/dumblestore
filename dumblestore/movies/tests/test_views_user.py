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

    def test_customers_cannot_view_users(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_view_user_details(self):
        url = urljoin(self.url, "1/")
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
            "email": "voldi@voldecorp.com",
        }
        resp = self.client.put(self.url + "2/", data=postData)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_delete_users(self):
        resp = self.client.delete(self.url + "2/")
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
        self.assertEqual(len(resp.data["results"]), 4)

    def test_admin_can_view_users_with_pagination(self):
        RandomUserFactory.create_batch(100)
        self.url = urljoin(self.url, "?page=3")
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 20)

    def test_admin_can_view_user_details(self):
        self.url = urljoin(self.url, "2/")
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_admin_can_create_user(self):
        data = {
            "email": "voldi@voldecorp.com",
            "first_name": "Lord",
            "last_name": "Voldi",
            "password": "Asd1234!",
        }
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        pass

    def test_admin_can_update_user(self):
        self.url = urljoin(self.url, "2/")
        putData = {
            "email": "voldi@voldecorp.com",
            "first_name": "Lord",
            "last_name": "Voldi",
            "password": "Asd1234!",
        }
        resp = self.client.put(self.url, putData)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_user(self):
        self.url = urljoin(self.url, "2/")
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
