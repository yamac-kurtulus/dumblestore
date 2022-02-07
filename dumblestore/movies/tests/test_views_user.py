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
        RandomUserFactory.create_batch(5)

        self.postData = UserSerializer(instance=RandomUserFactory.build()).data
        self.postData.pop("id")  # id must not be present when creating

    def test_customers_cannot_view_users(self):
        """
        Ensure a logged in customer cannot view user list
        """
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_view_user_details(self):
        """
        Ensure a logged in customer cannot view other users' details
        """
        resp = self.client.get(self.url + "1/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_create_users(self):
        """
        Ensure a logged in customer cannot create a new user
        """
        resp = self.client.post(path=self.url, data=self.postData)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_update_users(self):
        """
        Ensure a logged in customer cannot update a user
        """
        resp = self.client.put(self.url + "3/", data=self.postData)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_cannot_delete_users(self):
        """
        Ensure a logged in customer cannot delete a user
        """
        resp = self.client.delete(self.url + "3/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_can_view_own_details(self):
        resp = self.client.get(self.url + "me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], self.APIuser.email)
        pass


class AdminUserTests(APITestCase):
    def test_admin_can_view_users(self):
        """
        Ensure superuser can view user list
        """
        pass

    def test_admin_can_view_users_with_pagination(self):
        """
        Ensure superuser can view user list
        """
        pass

    def test_admin_can_view_user_details(self):
        """
        Ensure superuser can view user details
        """
        pass

    def test_admin_can_create_user(self):
        """
        Ensure superuser can Create User
        """

    def test_admin_can_update_user(self):
        """
        Ensure superuser can Update User
        """
        pass

    def test_admin_can_delete_user(self):
        """
        Ensure superuser can Delete User
        """
        pass
