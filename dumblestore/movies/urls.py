from django.urls import include, path
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

# urlpatterns = [
#     path("movies/", views.movie_list),
#     path("movies/<int:pk>/", views.movie_detail),
# ]
