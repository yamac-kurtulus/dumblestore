from cgitb import lookup
from django.urls import include, path
from .views import UserViewSet, MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
