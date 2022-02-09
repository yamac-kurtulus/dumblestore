from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Allows user to only view their own information
    """

    def has_object_permission(self, request, view, obj):
        return request.method == "GET" and obj.email == request.user.email

    def has_permission(self, request, view):
        return view.action == "me"


class IsAuthenticatedReadOnly(BasePermission):
    """
    Allows:
    Admins: full-control
    Customer users: read-only
    Anon: none
    """

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return not request.user.is_anonymous and request.method in SAFE_METHODS
