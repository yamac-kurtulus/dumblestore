from .filters import GenreOrderingFilter
from .models import User, Movie
from .serializers import MovieSerializer, UserSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .permissions import IsAuthenticatedReadOnly, IsOwner
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator


class UserViewSet(viewsets.ModelViewSet):
    """
    Api endpoint for the Users. Admins have all the CRUD functionality whereas regular users can only get information about themselves.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner | permissions.IsAdminUser]

    @action(detail=False, permission_classes=[IsOwner])
    def me(self, request):
        """
        Information about the current logged in user
        """
        current_user = request.user
        if not isinstance(current_user, AnonymousUser):
            user = User.objects.get(pk=current_user.pk)
        else:
            raise NotFound(detail="Please login to manage your profile")

        if user:
            serializer_obj = self.get_serializer(instance=user)
        return Response(serializer_obj.data)


class MovieViewSet(viewsets.ModelViewSet):
    """
    Api endpoint for the Movies.
    Admins have all the CRUD functionality
    Customers can view movies and movie details
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedReadOnly | permissions.IsAdminUser]
    lookup_field = "slug"
    filter_backends = [GenreOrderingFilter]
    ordering_fields = ["title", "genres"]
    ordering = ["title"]

    @method_decorator(cache_page(60 * 60))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
