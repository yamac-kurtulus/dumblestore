import json
from urllib.parse import urljoin
from django.urls import reverse
from django.views import View
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
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

        self.m1 = MovieWithManyGenresFactory(genre_count=3)
        self.m2 = MovieWithManyGenresFactory(genre_count=2)
        self.m3 = MovieWithManyGenresFactory(genre_count=3)
        self.m4 = MovieWithManyGenresFactory(genre_count=1)

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
        url = urljoin(self.url, self.m2.slug + "/")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_admin_can_create_movie(self):
        data = {"title": "New Movie", "genres": ["Scifi", "Drama", "New Genre"]}
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # ensure it is created correctly
        self.client.get(self.url)
        self.assertEqual(resp.data["title"], "New Movie")
        self.assertCountEqual(resp.data["genres"], ["Scifi", "Drama", "New Genre"])

    def test_admin_can_update_movie(self):
        self.url = urljoin(self.url, self.m2.slug + "/")
        putData = {"title": "New Title", "genres": ["Scifi", "Comedy"]}
        resp = self.client.put(self.url, putData, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # ensure it is updated correctly
        self.client.get(self.url, putData)
        self.assertEqual(resp.data["title"], "New Title")
        self.assertCountEqual(resp.data["genres"], ["Scifi", "Comedy"])

    def test_admin_can_delete_user(self):
        url = urljoin(self.url, self.m2.slug + "/")
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_create_movies_without_genre(self):
        data = {"title": "New Movie"}
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cache_invalidated_on_delete(self):
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 4)
        url = urljoin(self.url, self.m2.slug + "/")
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 3)

    def test_cache_invalidated_on_create(self):

        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 4)
        data = {"title": "New Movie", "genres": ["Scifi", "Drama", "New Genre"]}
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 5)

    def test_cache_invalidated_on_update(self):
        self.url = urljoin(self.url, self.m2.slug + "/")
        putData = {"title": "New Title", "genres": ["Scifi", "Comedy"]}
        resp = self.client.put(self.url, putData, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # ensure it is updated correctly
        self.client.get(self.url, putData)
        self.assertEqual(resp.data["title"], "New Title")


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

        # populate
        scifi = Genre.objects.create(name="Scifi")
        action = Genre.objects.create(name="Action")
        romance = Genre.objects.create(name="Romance")
        drama = Genre.objects.create(name="Drama")
        comedy = Genre.objects.create(name="Comedy")
        adventure = Genre.objects.create(name="Adventure")

        self.m1 = MovieWithManyGenresFactory(
            title="Matrix", genre_order_index="Action|Scifi"
        )
        self.m1.genres.set([scifi, action])
        self.m2 = MovieWithManyGenresFactory(
            title="Blade Runner", genre_order_index="Adventure|Drama|Scifi"
        )
        self.m2.genres.set([scifi, adventure, drama])

        self.m3 = MovieWithManyGenresFactory(
            title="Titanic", genre_order_index="Drama|Romance"
        )
        self.m3.genres.set([drama, romance])
        self.m4 = MovieWithManyGenresFactory(
            title="Harry Potter", genre_order_index="Action|Adventure|Comedy"
        )
        self.m4.genres.set([adventure, action, comedy])

    def test_customer_can_view_movies(self):
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.data["results"]), 4)

    def test_customer_can_view_movies_with_pagination(self):
        MovieWithManyGenresFactory.create_batch(100, genre_count=2)
        url = urljoin(self.url, "?page=3")
        resp = self.client.get(url)
        self.assertEqual(len(resp.data["results"]), 20)

    def test_customer_can_view_movie_details(self):
        url = urljoin(self.url, self.m2.slug + "/")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_customer_can_not_create_movie(self):
        data = {"title": "New Movie", "genres": ["Scifi", "Drama", "New Genre"]}
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_can_not_update_movie(self):
        self.url = urljoin(self.url, self.m2.slug + "/")
        putData = {"title": "New Title", "genres": ["Scifi", "Comedy"]}
        resp = self.client.put(self.url, putData, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_can_not_delete_user(self):
        url = urljoin(self.url, self.m2.slug + "/")
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_sorted_by_title_by_default(self):
        resp = self.client.get(self.url)
        data = resp.json()
        results = data["results"]
        titles = [item["title"] for item in results]
        self.assertListEqual(
            titles, ["Blade Runner", "Harry Potter", "Matrix", "Titanic"]
        )
        for item in results:
            genres = item["genres"]
            self.assertListEqual(genres, sorted(genres))

    def test_can_be_sortable_by_genre(self):
        sorted_url = urljoin(self.url, "?ordering=genres")
        resp = self.client.get(sorted_url)
        data = resp.json()
        results = data["results"]
        titles = [item["title"] for item in results]
        print(results)
        self.assertListEqual(
            titles, ["Harry Potter", "Matrix", "Blade Runner", "Titanic"]
        )
        for item in results:
            genres = item["genres"]
            self.assertListEqual(genres, sorted(genres))
        print(titles)
