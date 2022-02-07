from django.shortcuts import render

from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .permissions import IsOwner
from django.contrib.auth.models import AnonymousUser


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
