from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class that binds User model to REST API
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "url"]

    lookup_field = "email"
