import random
from urllib.parse import urljoin
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Genre, Movie
from .factories import (
    AdminFactory,
    CustomerUserFactory,
    MovieWithManyGenresFactory,
)


class MovieViewAdminTests(APITestCase):
    def setUp(self):
        """
        Creates or gets an admin user and uses that to test the functionality
        """
        self.APIuser = AdminFactory.create()
        self.client.force_authenticate(user=self.APIuser)
        self.url = reverse("movie-list")

        # populate
        Genre.objects.create(name="Scifi")
        Genre.objects.create(name="Action"),
        Genre.objects.create(name="Romance"),
        Genre.objects.create(name="Drama"),
        Genre.objects.create(name="Comedy"),
        Genre.objects.create(name="Adventure"),
        Genre.objects.create(name="Documentary"),

        MovieWithManyGenresFactory(genre_count=3)
        MovieWithManyGenresFactory(genre_count=2)
        MovieWithManyGenresFactory(genre_count=3)
        MovieWithManyGenresFactory(genre_count=1)

    # Test basic API access

    def test_admin_can_view_movies(self):
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 4)

    def test_admin_can_view_movies_with_pagination(self):
        MovieWithManyGenresFactory.create_batch(100, genre_count=2)
        url = urljoin(self.url, "?page=3")
        resp = self.client.get(url)
        self.assertEqual(len(resp.data["results"]), 20)

    def test_admin_can_view_movie_details(self):
        url = urljoin(self.url, "2/")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # def test_admin_can_create_movie(self):
    #     data = {"title": "New Movie", "genres": ["Scifi", "Drama", "New Genre"]}
    #     resp = self.client.post(self.url, data)
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     # ensure it is created correctly
    #     new_movie_url = urljoin(self.url, str(resp.data["id"]))
    #     self.client.get(self.url)
    #     self.assertEqual(resp.data["title"], "New Movie")
    #     self.assertCountEqual(resp.data["genres"], ["Scifi", "Drama", "New Genre"])

    # def test_admin_can_update_movie(self):
    #     self.url = urljoin(self.url, "2/")
    #     putData = {"title": "New Title", "genres": ["Scifi", "Drama", "New Genre"]}
    #     resp = self.client.put(self.url, putData)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     # ensure it is updated correctly
    #     self.client.get(self.url, putData)
    #     self.assertEqual(resp.data["title"], "New Title")
    #     self.assertCountEqual(resp.data["genres"], ["Scifi", "Drama", "New Genre"])

    def test_admin_can_delete_user(self):
        url = urljoin(self.url, "2/")
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # Rest of the tests deal with functional requirements

    # def test_cannot_create_movies_without_genre(self):
    #     data = {"title": "New Movie"}
    #     resp = self.client.post(self.url, data)
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class MovieCustomerViewTests(APITestCase):
    def setUp(self):
        """
        Sets up test class:
        1. Creates a customer user "Harry Potter" to act as a user of the API
        2. Sets url to be the API endpoint for movie-list
        3. Populates the DB
        """
        self.APIuser = CustomerUserFactory.create()
        self.client.force_authenticate(user=self.APIuser)

        self.url = reverse("movie-list")

        # populate it
        # RandomUserFactory.create(email="user1@hogwarts.com")
        # RandomUserFactory.create(email="user2@hogwarts.com")
        # RandomUserFactory.create(email="user3@hogwarts.com")


#     def test_customers_cannot_view_users(self):
#         resp = self.client.get(self.url)
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

#     def test_customers_cannot_view_user_details(self):
#         url = urljoin(self.url, "1/")
#         resp = self.client.get(self.url + "")
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

#     def test_customers_cannot_create_users(self):
#         u = RandomUserFactory.build(email="user3@hogwarts.com")
#         postData = {
#             "first_name": "Lord",
#             "last_name": "Voldi",
#             "email": "noseless@voldi.com",
#             "password": "Asd1234!",
#         }
#         resp = self.client.post(path=self.url, data=postData)
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

#     def test_customers_cannot_update_users(self):
#         postData = {
#             "first_name": "Lord",
#             "last_name": "Voldi",
#             "password": "Asd1234!",
#             "email": "voldi@voldecorp.com",
#         }
#         resp = self.client.put(self.url + "2/", data=postData)
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

#     def test_customers_cannot_delete_users(self):
#         resp = self.client.delete(self.url + "2/")
#         self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

#     def test_customers_can_view_own_details(self):
#         resp = self.client.get(self.url + "me/")
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data["email"], self.APIuser.email)
#         pass
