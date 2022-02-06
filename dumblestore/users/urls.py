from django.urls import include, path
from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
